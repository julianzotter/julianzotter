#!/usr/bin/env python3
"""
scan_inventory.py  —  AP3 FAST-PATH / SLOW-PATH SCANNER
Generates SOURCE_REGISTRY.csv (canonical file inventory) + event ledger.

Fast-Path:  mtime + size change detection (O(1) per file, no hash)
Slow-Path:  SHA-256 only on changed / new files (triggered by Fast-Path delta)

Usage:
    # First run (full scan, build baseline):
    python scripts/scan_inventory.py --root "G:/Meine Ablage" --out source_registry.csv

    # Incremental run (delta only, append to ledger):
    python scripts/scan_inventory.py --root "G:/Meine Ablage" --out source_registry.csv --incremental

    # With explicit zones (8-Zonen-Modell):
    python scripts/scan_inventory.py --root "G:/Meine Ablage" --zones zones.json --out source_registry.csv

Outputs:
    source_registry.csv   — canonical file inventory (MASTER INDEX)
    scan_ledger.jsonl     — append-only event log (CREATED / MODIFIED / MOVED / DELETED)
    scan_state.json       — baseline snapshot for next incremental run

Zone file format (zones.json):
    {"Z1": ["Governance"], "Z2": ["AI WORKBENCH"], "Z6": ["Finanzen", "Buchhaltung"]}
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.1.0"
RAG_BLOCKED_ZONES = {"Z6"}  # Finanzen / Mandantentrennung — never index

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "QUARANTINE"}
SKIP_EXTS = {".exe", ".dll", ".so", ".dylib", ".bin", ".iso", ".img"}

TEXT_LIKE_EXTS = {
    ".pdf", ".docx", ".xlsx", ".pptx", ".txt", ".md", ".py", ".json",
    ".yaml", ".yml", ".csv", ".xml", ".html", ".ifc", ".dxf", ".dwg",
    ".r", ".ipynb", ".toml", ".cfg", ".ini",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def detect_zone(path: Path, root: Path, zone_map: dict[str, list[str]]) -> tuple[str, bool]:
    """Return (zone_id, rag_allowed) based on folder path."""
    rel_parts = [p.lower() for p in path.relative_to(root).parts]
    for zone_id, keywords in zone_map.items():
        for kw in keywords:
            if any(kw.lower() in part for part in rel_parts):
                return zone_id, zone_id not in RAG_BLOCKED_ZONES
    return "Z0", True


def classify_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        return "PDF"
    if ext in {".docx", ".doc"}:
        return "DOCX"
    if ext in {".xlsx", ".xls", ".ods"}:
        return "XLSX"
    if ext == ".ifc":
        return "IFC"
    if ext in {".dxf", ".dwg"}:
        return "CAD"
    if ext in {".py", ".js", ".ts", ".java", ".c", ".cpp", ".rs", ".go"}:
        return "CODE"
    if ext in {".json", ".jsonl"}:
        return "JSON"
    if ext in {".yaml", ".yml", ".toml", ".cfg", ".ini"}:
        return "CONFIG"
    if ext in {".txt", ".md", ".rst"}:
        return "TEXT"
    if ext == ".csv":
        return "CSV"
    if ext == ".ipynb":
        return "NOTEBOOK"
    return "OTHER"


def load_state(state_path: Path) -> dict[str, dict]:
    """Load previous scan state: {rel_path: {mtime, size, sha256}}"""
    if not state_path.exists():
        return {}
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state_path: Path, state: dict) -> None:
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def append_ledger(ledger_path: Path, events: list[dict]) -> None:
    with open(ledger_path, "a", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def load_zone_map(zones_path: Path | None) -> dict[str, list[str]]:
    if zones_path and zones_path.exists():
        return json.loads(zones_path.read_text(encoding="utf-8"))
    # Default 8-Zonen-Modell keywords
    return {
        "Z1": ["governance", "compliance", "protokoll"],
        "Z2": ["ai workbench", "nexus", "ki-werkzeug"],
        "Z3": ["code", "scripts", "src"],
        "Z4": ["engineering", "statik", "bemessung", "holzbau", "betonbau", "stahlbau"],
        "Z5": ["projekte", "projects", "p205", "ft-träger"],
        "Z6": ["finanzen", "buchhaltung", "stb", "banking", "invoice", "rechnung", "bekament"],
        "Z7": ["media", "fotos", "videos", "events"],
        "Z8": ["vendor", "exclude", "quarantine", "archive"],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="NEXUS AP3 — Fast-Path/Slow-Path file scanner")
    ap.add_argument("--root", required=True, help="Root folder to scan")
    ap.add_argument("--out", default="source_registry.csv", help="Output CSV (default: source_registry.csv)")
    ap.add_argument("--ledger", default="scan_ledger.jsonl", help="Event ledger JSONL (default: scan_ledger.jsonl)")
    ap.add_argument("--state", default="scan_state.json", help="Baseline state file (default: scan_state.json)")
    ap.add_argument("--zones", default=None, help="Zone map JSON file (optional)")
    ap.add_argument("--incremental", action="store_true", help="Only process Fast-Path deltas")
    ap.add_argument("--hash", action="store_true", help="Force SHA-256 on all files (Slow-Path full run)")
    ap.add_argument("--max-files", type=int, default=0, help="Limit scan (0 = unlimited)")
    ap.add_argument("--verbose", action="store_true", help="Print progress")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    out_path = Path(args.out)
    ledger_path = Path(args.ledger)
    state_path = Path(args.state)
    zones_path = Path(args.zones) if args.zones else None

    if not root.exists():
        print(f"ERROR: root does not exist: {root}", file=sys.stderr)
        return 2

    zone_map = load_zone_map(zones_path)
    prev_state = load_state(state_path) if args.incremental else {}
    now_iso = datetime.now(timezone.utc).isoformat()
    run_id = f"RUN_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"

    rows: list[dict] = []
    new_state: dict[str, dict] = {}
    events: list[dict] = []

    scanned = 0
    hashed = 0
    fast_hits = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if args.max_files and scanned >= args.max_files:
                break
            fp = Path(dirpath) / fname
            ext = fp.suffix.lower()
            if ext in SKIP_EXTS:
                continue

            scanned += 1
            rel = str(fp.relative_to(root))

            try:
                stat = fp.stat()
            except OSError:
                continue

            mtime = stat.st_mtime
            size = stat.st_size
            zone, rag_allowed = detect_zone(fp, root, zone_map)
            file_type = classify_type(fp)

            # Fast-Path: check if mtime or size changed
            prev = prev_state.get(rel)
            changed = (prev is None) or (prev["mtime"] != mtime) or (prev["size"] != size)

            sha = ""
            if changed or args.hash:
                # Slow-Path: compute SHA-256
                try:
                    sha = sha256(fp)
                    hashed += 1
                except OSError:
                    sha = "ERROR"
                if changed:
                    fast_hits += 1
                    event_type = "CREATED" if prev is None else "MODIFIED"
                    events.append({
                        "run_id": run_id,
                        "ts": now_iso,
                        "event": event_type,
                        "path": rel,
                        "sha256": sha,
                        "size": size,
                        "zone": zone,
                        "rag_allowed": rag_allowed,
                    })
                    if args.verbose:
                        print(f"  [{event_type}] {rel}")
            elif prev:
                sha = prev.get("sha256", "")

            new_state[rel] = {"mtime": mtime, "size": size, "sha256": sha}

            if not args.incremental or changed:
                rows.append({
                    "artifact_id": f"{run_id}_{sha[:8]}",
                    "path": rel,
                    "name": fp.name,
                    "ext": ext,
                    "type": file_type,
                    "size_bytes": size,
                    "mtime": datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat(),
                    "sha256": sha,
                    "zone": zone,
                    "rag_allowed": rag_allowed,
                    "status": "INDEXED",
                    "run_id": run_id,
                })

    # Detect deletions (files in prev_state but not seen)
    if args.incremental and prev_state:
        seen_rels = {r["path"] for r in rows}
        for rel, meta in prev_state.items():
            if rel not in seen_rels and rel not in new_state:
                events.append({
                    "run_id": run_id,
                    "ts": now_iso,
                    "event": "DELETED",
                    "path": rel,
                    "sha256": meta.get("sha256", ""),
                    "size": meta.get("size", 0),
                    "zone": "UNKNOWN",
                    "rag_allowed": False,
                })

    # Write outputs
    fieldnames = ["artifact_id", "path", "name", "ext", "type", "size_bytes",
                  "mtime", "sha256", "zone", "rag_allowed", "status", "run_id"]
    mode = "a" if args.incremental else "w"
    with open(out_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not args.incremental:
            writer.writeheader()
        writer.writerows(rows)

    save_state(state_path, new_state)
    if events:
        append_ledger(ledger_path, events)

    print(f"\nRun: {run_id}")
    print(f"Scanned: {scanned} files | Hashed (Slow-Path): {hashed} | Fast-Path deltas: {fast_hits}")
    print(f"Registry → {out_path} ({len(rows)} rows)")
    print(f"Ledger   → {ledger_path} ({len(events)} events)")
    print(f"State    → {state_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
