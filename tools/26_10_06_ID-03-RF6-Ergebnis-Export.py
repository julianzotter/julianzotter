"""RF6 Ergebnis-Export (Baseline) – Seilstatik Böblingen, Auftrag 1, CANDIDATE.

Liest das im Vordergrund aktive RFEM-6-Modell über die API-II (dlubal.api, gRPC
127.0.0.1:9000) und schreibt drei CSV-Dateien plus API_Log.json in einen neuen
Unterordner `API_Auszuege/RF6_EXPORT_<Stempel>_<RUN-ID>/`.

Voraussetzungen (lokal, Windows):
  - RFEM 6.12 läuft, Modell aktiv, Programm-Optionen → Dlubal API & gRPC = AN
  - venv mit dlubal.api==2.12.8 (siehe RFEM6_MCP_Bridge_Extended.py Docstring)
  - API-Key: `python 26_10_06_ID-03-RFEM6_MCP_Bridge_Extended.py --configure`
  - diese Datei liegt im selben Ordner wie 26_10_06_ID-03-RFEM6_MCP_Bridge_Extended.py

Aufruf:
  python 26_10_06_ID-03-RF6-Ergebnis-Export.py [--out API_Auszuege] [--run-id RUN-RF6-000]

Das Skript rechnet nicht, ändert nichts am Modell und nutzt ausschließlich die
read-only-Operationen der Bridge (raw_results mit Dump auf Platte, keine Paginierung).
STATUS: CANDIDATE – ohne RFEM-Umgebung nicht getestet. Terminal-Ausgabe + API_Log.json
zurückmelden.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

BRIDGE_FILE = "26_10_06_ID-03-RFEM6_MCP_Bridge_Extended.py"
# Zielkategorien: Treffer per Teilstring auf die SDK-Enum ResultsType (robust gegen
# Namensvarianten zwischen SDK-Builds). Reihenfolge = Dateinummer.
TARGETS = [
    ("01_Seilkraefte_N.csv", ["STATIC_ANALYSIS", "MEMBERS", "INTERNAL_FORCES"]),
    ("02_Lagerkraefte_global.csv", ["STATIC_ANALYSIS", "NODES", "SUPPORT_FORCES"]),
    ("03_Knotenverformungen.csv", ["STATIC_ANALYSIS", "NODES", "DEFORMATIONS"]),
]


def load_bridge(folder: Path):
    """Bridge-Modul aus Datei laden (Dateiname enthält Bindestriche → kein import)."""
    path = folder / BRIDGE_FILE
    if not path.exists():
        raise SystemExit(f"FEHLT: {path}")
    spec = importlib.util.spec_from_file_location("rfem_bridge", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def resolve_category(keys: list[str], parts: list[str]) -> str | None:
    """Erste SDK-Kategorie, die alle Teilstrings enthält; TABLE-Varianten bevorzugt vermeiden."""
    hits = [k for k in keys if all(p in k for p in parts)]
    hits.sort(key=lambda k: ("TABLE" in k, len(k)))
    return hits[0] if hits else None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=Path("API_Auszuege"))
    ap.add_argument("--run-id", default="RUN-RF6-000")
    args = ap.parse_args(argv)
    here = Path(__file__).resolve().parent
    bridge = load_bridge(here)

    health = bridge.execute({"operation": "health"})
    print("HEALTH:", json.dumps(health, ensure_ascii=False))
    if health.get("status") != "ok":
        return 1

    from dlubal.api import rfem  # erst nach Health-Check, damit Fehlermeldung klar bleibt
    keys = [k for k in rfem.results.ResultsType.keys() if k != "INVALID_RESULTS_TYPE"]

    stamp = dt.datetime.now().strftime("%y%m%d_%H%M%S")
    job = args.out / f"RF6_EXPORT_{stamp}_{args.run_id}"
    job.mkdir(parents=True, exist_ok=False)
    log = {"run_id": args.run_id, "created_at_utc": bridge.utc_now(), "health": health,
           "sdk_result_categories_total": len(keys), "files": [], "warnings": [], "status": "running"}

    for filename, parts in TARGETS:
        category = resolve_category(keys, parts)
        entry = {"file": filename, "category": category}
        if category is None:
            entry["status"] = "category_not_in_sdk"
            log["warnings"].append(f"{filename}: keine Kategorie mit {parts} in SDK")
            log["files"].append(entry)
            continue
        dump = job / (Path(filename).stem + ".jsonl")
        result = bridge.execute({"operation": "raw_results", "category": category}, dump)
        entry.update({k: result.get(k) for k in ("status", "total_rows", "model_guid",
                                                 "application_version", "api_client_version")})
        if result.get("status") in ("ok", "empty"):
            csv_tmp = dump.with_suffix(".csv")
            csv_tmp.replace(job / filename)
            entry["sha256"] = sha256_file(job / filename)
        else:
            log["warnings"].append(f"{filename}: {result.get('code')} {result.get('message')}")
        log["files"].append(entry)
        print(f"{filename}: {entry.get('status')} rows={entry.get('total_rows')} cat={category}")

    ok = [f for f in log["files"] if f.get("status") == "ok"]
    log["status"] = "ok" if len(ok) == len(TARGETS) else ("no_results" if any(
        f.get("status") == "no_results" for f in log["files"]) else "partial")
    log["model_guid"] = next((f.get("model_guid") for f in log["files"] if f.get("model_guid")), None)
    (job / "API_Log.json").write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"STATUS={log['status']}  ->  {job.resolve()}")
    return 0 if log["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
