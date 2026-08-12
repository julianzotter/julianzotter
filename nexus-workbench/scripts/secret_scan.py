#!/usr/bin/env python3
"""
secret_scan.py  —  AP2 SECURITY GATE
Fast-Path/Slow-Path pre-upload secret scanner.

Usage (local, on G:\\ or any folder):
    python scripts/secret_scan.py --root "G:/Meine Ablage" --out findings.csv
    python scripts/secret_scan.py --root . --quarantine ./QUARANTINE --copy

Outputs:
    findings.csv — path, type, match_excerpt, score; REDACT before sharing
    exit 0       — clean (no hits)
    exit 1       — secrets found → quarantine / redact before upload

Security: run this BEFORE any git add / cloud upload.
DO NOT commit findings.csv if it contains secrets.
"""
from __future__ import annotations
import argparse
import csv
import os
import re
import shutil
import sys
from pathlib import Path

PATTERNS: dict[str, re.Pattern] = {
    "API_KEY":       re.compile(rb"(api[_-]?key|apikey)\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{20,})", re.I),
    "SECRET":        re.compile(rb"(secret[_-]?key?|client_secret)\s*[:=]\s*['\"]?([A-Za-z0-9_\-+/=]{16,})", re.I),
    "TOKEN":         re.compile(rb"(access_?token|auth_?token|bearer)\s*[:=]\s*['\"]?([A-Za-z0-9_\-./]{20,})", re.I),
    "PASSWORD":      re.compile(rb"(password|passwd|pwd)\s*[:=]\s*['\"]?([^\s'\",]{8,})", re.I),
    "PRIVATE_KEY":   re.compile(rb"-----BEGIN (RSA |EC )?PRIVATE KEY-----"),
    "AWS_KEY":       re.compile(rb"AKIA[0-9A-Z]{16}"),
    "GH_TOKEN":      re.compile(rb"gh[pousr]_[A-Za-z0-9]{36}"),
    "OPENAI_KEY":    re.compile(rb"sk-[A-Za-z0-9]{32,}"),
    "ANTHROPIC_KEY": re.compile(rb"sk-ant-[A-Za-z0-9\-_]{32,}"),
    "BASE64_LONG":   re.compile(rb"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{48,}={0,2}(?![A-Za-z0-9+/])"),
}

TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".java", ".c", ".cpp", ".h", ".cs", ".go", ".rs",
    ".txt", ".md", ".rst", ".env", ".cfg", ".ini", ".conf", ".yaml", ".yml",
    ".json", ".toml", ".xml", ".html", ".sh", ".bat", ".ps1", ".R", ".tex",
    ".csv", ".ipynb",
}

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}


def is_binary(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            return b"\x00" in f.read(2048)
    except OSError:
        return True


def scan_file(path: Path) -> list[dict]:
    findings: list[dict] = []
    ext = path.suffix.lower()
    if ext not in TEXT_EXTENSIONS and is_binary(path):
        return findings
    try:
        data = path.read_bytes()
    except OSError:
        return findings
    for pattern_type, pat in PATTERNS.items():
        for m in pat.finditer(data):
            start = max(m.start() - 30, 0)
            end = min(m.end() + 30, len(data))
            excerpt = data[start:end].decode("utf-8", errors="replace").replace("\n", " ")
            findings.append({
                "type": pattern_type,
                "match": m.group(0).decode("utf-8", errors="replace")[:80],
                "excerpt": excerpt[:160],
                "score": len(m.group(0)),
            })
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="NEXUS AP2 — Secret scanner before upload")
    ap.add_argument("--root", required=True, help="Root folder to scan")
    ap.add_argument("--out", default="secret_findings.csv", help="Output CSV (default: secret_findings.csv)")
    ap.add_argument("--quarantine", default=None, help="Quarantine directory for matched files")
    ap.add_argument("--copy", action="store_true", help="Copy matched files into quarantine dir")
    ap.add_argument("--max-files", type=int, default=0, help="Limit number of files (0 = unlimited)")
    ap.add_argument("--verbose", action="store_true", help="Print each finding to stdout")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    out_path = Path(args.out)
    quarantine = Path(args.quarantine) if args.quarantine else None
    if quarantine and args.copy:
        quarantine.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict] = []
    matched_files: set[Path] = set()
    scanned = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            if args.max_files and scanned >= args.max_files:
                break
            fp = Path(dirpath) / fname
            scanned += 1
            hits = scan_file(fp)
            if hits:
                matched_files.add(fp)
                rel = fp.relative_to(root)
                for h in hits:
                    row = {"path": str(rel), **h}
                    all_rows.append(row)
                    if args.verbose:
                        print(f"  [{h['type']}] {rel}  →  {h['excerpt'][:80]}")

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["path", "type", "match", "excerpt", "score"])
        writer.writeheader()
        writer.writerows(all_rows)

    if quarantine and args.copy:
        for fp in matched_files:
            try:
                rel = fp.relative_to(root)
                dest = quarantine / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(fp, dest)
            except Exception as e:
                print(f"  WARN quarantine copy failed: {fp} → {e}", file=sys.stderr)

    n_files = len(matched_files)
    n_hits = len(all_rows)
    print(f"\nScanned {scanned} files — {n_files} files with secrets, {n_hits} total hits")
    print(f"Results → {out_path}")
    if n_hits:
        print("⚠️  SECRETS FOUND — redact / quarantine before upload (exit 1)")
        return 1
    print("✅  Clean — no secrets detected (exit 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
