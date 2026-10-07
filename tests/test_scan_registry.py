"""Smoke-Tests für tools/01_scan_registry.py (stdlib unittest, ohne externe Abhängigkeiten).

Aufruf: python -m unittest tests.test_scan_registry -v
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "01_scan_registry.py"
spec = importlib.util.spec_from_file_location("scan_registry", SCRIPT)
scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan)  # type: ignore[union-attr]


class ScanRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "PROJ"
        (self.root / "sub" / "__pycache__").mkdir(parents=True)
        (self.root / "a.txt").write_bytes(b"hello")
        (self.root / "sub" / "b.rf5").write_bytes(b"\x00" * 2048)
        (self.root / "sub" / "__pycache__" / "x.pyc").write_bytes(b"skip")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_walk_excludes_pycache(self) -> None:
        names = sorted(p.name for p in scan.iter_files(self.root, scan.EXCLUDE_DEFAULT))
        self.assertEqual(names, ["a.txt", "b.rf5"])

    def test_sha256_matches_hashlib(self) -> None:
        rec = scan.record(self.root / "a.txt", self.root, do_hash=True, limit_mb=0)
        self.assertEqual(rec["sha256"], hashlib.sha256(b"hello").hexdigest())
        self.assertEqual(rec["ext"], "txt")
        self.assertEqual(rec["size"], 5)

    def test_hash_limit_skips_large_files(self) -> None:
        rec = scan.record(self.root / "sub" / "b.rf5", self.root, do_hash=True, limit_mb=1)
        self.assertEqual(rec["sha256"], hashlib.sha256(b"\x00" * 2048).hexdigest())
        big = self.root / "big.bin"
        big.write_bytes(b"\x01" * (2 * 1024 * 1024))
        self.assertIsNone(scan.sha256_file(big, limit_mb=1))

    def test_id_is_stable_and_path_relative(self) -> None:
        r1 = scan.record(self.root / "sub" / "b.rf5", self.root, False, 0)
        r2 = scan.record(self.root / "sub" / "b.rf5", self.root, False, 0)
        self.assertEqual(r1["id"], r2["id"])
        self.assertEqual(r1["path"], "sub/b.rf5")
        self.assertEqual(len(r1["id"]), 16)

    def test_jsonl_atomic_write(self) -> None:
        out = Path(self.tmp.name) / "reg.jsonl"
        recs = [scan.record(p, self.root, True, 0) for p in scan.iter_files(self.root, scan.EXCLUDE_DEFAULT)]
        scan.write_jsonl_atomic(recs, out)
        self.assertTrue(out.exists())
        self.assertFalse(out.with_suffix(".jsonl.tmp").exists())
        rows = [json.loads(l) for l in out.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r["status"] == "FOUND" for r in rows))


if __name__ == "__main__":
    unittest.main()
