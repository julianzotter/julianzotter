#!/usr/bin/env python3
"""01_scan_registry.py — lokaler Datei-Scan mit SHA-256 in JSONL (Phase 1 der Registry).

Verwendung (Windows, G: gemountet):
  python tools/01_scan_registry.py --root "G:\\Meine Ablage\\_SEILSTATIK_BOEBLINGEN" ^
      --root "G:\\Meine Ablage\\26-03-18_Boeb_Adaptierung" --out file-registry.jsonl --hash
Ohne --hash werden nur Metadaten erfasst (schnell). Mit --hash SHA-256 über Originalbytes.
Ausgabe: 1 Zeile = 1 Datei; Schreiben atomar (.tmp -> replace). stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Iterator

EXCLUDE_DEFAULT = ["__pycache__", ".git", "node_modules", "$RECYCLE.BIN", "System Volume Information"]
CHUNK = 1 << 20  # 1 MiB


def sha256_file(path: Path, limit_mb: int) -> str | None:
    """SHA-256 über Dateibytes; None, wenn Datei größer als limit_mb (0 = kein Limit)."""
    size = path.stat().st_size
    if limit_mb and size > limit_mb * 1024 * 1024:
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def iter_files(root: Path, exclude: list[str]) -> Iterator[Path]:
    """Alle Dateien unter root, Ausschlussordner werden nicht betreten."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for name in filenames:
            yield Path(dirpath) / name


def record(path: Path, root: Path, do_hash: bool, limit_mb: int) -> dict:
    """Ein Registry-Datensatz je Datei. id = sha256(normalisierter Relativpfad)[:16]."""
    rel = path.relative_to(root).as_posix()
    st = path.stat()
    rec = {
        "id": hashlib.sha256(f"{root.name}/{rel}".encode("utf-8")).hexdigest()[:16],
        "root": root.name,
        "path": rel,
        "name": path.name,
        "ext": path.suffix.lower().lstrip("."),
        "size": st.st_size,
        "mtime": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(st.st_mtime)),
        "sha256": None,
        "status": "FOUND",
    }
    if do_hash:
        try:
            rec["sha256"] = sha256_file(path, limit_mb)
        except OSError as exc:  # gesperrte/defekte Datei: protokollieren, nicht abbrechen
            rec["error"] = str(exc)[:200]
    return rec


def write_jsonl_atomic(records: list[dict], out: Path) -> None:
    """Atomar schreiben: erst .tmp, dann os.replace."""
    tmp = out.with_suffix(out.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    os.replace(tmp, out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", action="append", required=True, help="Wurzelordner (mehrfach erlaubt)")
    ap.add_argument("--out", default="file-registry.jsonl")
    ap.add_argument("--hash", action="store_true", help="SHA-256 über Originalbytes")
    ap.add_argument("--hash-limit-mb", type=int, default=0, help="0 = alle Dateien hashen")
    ap.add_argument("--exclude", nargs="*", default=EXCLUDE_DEFAULT)
    args = ap.parse_args()

    records: list[dict] = []
    t0 = time.time()
    for r in args.root:
        root = Path(r).expanduser().resolve()
        if not root.is_dir():
            print(f"FEHLER: kein Ordner: {root}", file=sys.stderr)
            return 2
        n0 = len(records)
        for p in iter_files(root, args.exclude):
            records.append(record(p, root, args.hash, args.hash_limit_mb))
        print(f"{root}: {len(records) - n0} Dateien")
    write_jsonl_atomic(records, Path(args.out))
    hashed = sum(1 for x in records if x.get("sha256"))
    errors = sum(1 for x in records if "error" in x)
    print(f"out={args.out} files={len(records)} hashed={hashed} errors={errors} t={time.time() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
