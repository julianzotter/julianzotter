"""Phase 2 – Anpassung der RF6-Exporte (Seilstatik Böblingen), CANDIDATE Rev0.

Input  (alle read-only):
  --export  Ordner RF6_EXPORT_<...>/ aus 26_10_06_ID-03-RF6-Ergebnis-Export.py (E6a):
            01_Seilkraefte_N.csv, 02_Lagerkraefte_global.csv, 03_Knotenverformungen.csv, API_Log.json
  --model   Ordner out_rf6/ aus 26_10_06_ID-03-rf6_model_export.py (E4):
            geometry_nodes.csv, tables/LoadCase.csv, tables/LoadCombination.csv
  --mapping 26_10_06_ID-03-AEQUIVALENZ-KNOTEN-GEOMETER-RFEM_Rev0.csv (V9)
Output:
  <export>/Auswertung/26_10_06_ID-03_KERNKNOTEN_DELTA_<RUN>.csv
  <export>/Auswertung/26_10_06_ID-03_DATEN_<RUN>.xlsx  (7 Blätter)

Regeln: Verformung u ist eine Verschiebung (API-SI, m) – kein Koordinatenabzug.
Nulllage kommt aus geometry_nodes.csv des SELBEN Modells, nie aus Handwerten.
LF/LK werden aus den Modelltabellen gelesen, nicht getippt. Fehlende Spalten → Abbruch
mit Spaltenliste (fail-closed). Keine Längenkette, keine Vorspannung (P1: nicht im Modell).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

# Kernknoten lt. BEFUND Rev0 §3: Wandanker, Mastköpfe, Mastfüße. 2027/2028/2041 existieren nicht.
KERNKNOTEN = [105, 106, 113, 114, 3006, 3007, 3021, 2006, 2007, 2021]
OFFEN = [("E1", "Geometriebasis VAR-A statt G3"), ("E2", "Maste 1006/1007 entfallen, 3006/3007 gelenkig"),
         ("E3", "C21 Fall A/B (0,60 m)"), ("E4", "Kombinatorik EN 1990 vs. Bestand"),
         ("E5", "dT-Bezugsbasis vs. PFEIFER T0 10 °C"), ("E6", "Seil 35 ohne Stablasten"),
         ("E7", "g 10,00 → 9,81 m/s²"), ("E8", "Kalibriertoleranz"), ("F7", "Beschlagmaß Lsys (PFEIFER)")]


def pick(df: pd.DataFrame, *candidates: str) -> str:
    """Erste vorhandene Spalte (case-insensitiv); sonst Abbruch mit Spaltenliste."""
    low = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in low:
            return low[cand.lower()]
    raise SystemExit(f"Spalte fehlt: {candidates} – vorhanden: {list(df.columns)}")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit(f"FEHLT: {path}")
    return pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")


def kernknoten_delta(verf: pd.DataFrame, nodes: pd.DataFrame) -> pd.DataFrame:
    """Verschiebungen der Kernknoten je Loading + Nulllage aus geometry_nodes.csv."""
    n = pick(verf, "node_no", "node", "knoten")
    ux, uy, uz = (pick(verf, c) for c in ("u_x", "u_y", "u_z")) if "u_x" in [c.lower() for c in verf.columns] \
        else (pick(verf, "ux", "displacement_x"), pick(verf, "uy", "displacement_y"), pick(verf, "uz", "displacement_z"))
    load_cols = [c for c in verf.columns if "loading" in c.lower() or c.lower() in ("load_case", "load_combination", "case")]
    k = verf[verf[n].isin(KERNKNOTEN)].copy()
    k = k.rename(columns={n: "node"})
    for src, dst in ((ux, "u_x_m"), (uy, "u_y_m"), (uz, "u_z_m")):
        k[dst] = pd.to_numeric(k[src], errors="coerce")
    k["u_abs_mm"] = (k[["u_x_m", "u_y_m", "u_z_m"]].pow(2).sum(axis=1) ** 0.5) * 1000
    geo = nodes.rename(columns={pick(nodes, "node"): "node"})[["node", "x_m", "y_m", "z_m"]]
    k = k.merge(geo, on="node", how="left", validate="many_to_one")
    for ax in "xyz":
        k[f"{ax}_verformt_m"] = k[f"{ax}_m"] + k[f"u_{ax}_m"]
    keep = ["node", *load_cols, "x_m", "y_m", "z_m", "u_x_m", "u_y_m", "u_z_m", "u_abs_mm",
            "x_verformt_m", "y_verformt_m", "z_verformt_m"]
    return k[keep].sort_values(["node", *load_cols])


def quellen_blatt(log: dict, export: Path, model: Path) -> pd.DataFrame:
    rows = [("run_id", log.get("run_id")), ("model_guid", log.get("model_guid")),
            ("read_at_utc", log.get("created_at_utc")), ("status_export", log.get("status")),
            ("application_version", next((f.get("application_version") for f in log.get("files", [])), None)),
            ("api_client_version", next((f.get("api_client_version") for f in log.get("files", [])), None)),
            ("export_dir", str(export)), ("model_export_dir", str(model))]
    rows += [(f"sha256:{f['file']}", f.get("sha256")) for f in log.get("files", [])]
    return pd.DataFrame(rows, columns=["Parameter", "Wert"])


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--export", type=Path, required=True)
    ap.add_argument("--model", type=Path, required=True)
    ap.add_argument("--mapping", type=Path, required=True)
    a = ap.parse_args(argv)
    log = json.loads((a.export / "API_Log.json").read_text(encoding="utf-8"))
    if log.get("status") != "ok":
        raise SystemExit(f"Export-Status {log.get('status')!r} ≠ ok → keine Auswertung (fail-closed)")
    verf = read_csv(a.export / "03_Knotenverformungen.csv")
    nodes = read_csv(a.model / "geometry_nodes.csv")
    delta = kernknoten_delta(verf, nodes)
    out = a.export / "Auswertung"
    out.mkdir(exist_ok=True)
    run = log.get("run_id", "RUN")
    delta.to_csv(out / f"26_10_06_ID-03_KERNKNOTEN_DELTA_{run}.csv", sep=";", index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(out / f"26_10_06_ID-03_DATEN_{run}.xlsx", engine="openpyxl") as w:
        quellen_blatt(log, a.export, a.model).to_excel(w, sheet_name="QUELLEN", index=False)
        read_csv(a.model / "tables" / "LoadCase.csv").to_excel(w, sheet_name="LASTFAELLE", index=False)
        read_csv(a.model / "tables" / "LoadCombination.csv").to_excel(w, sheet_name="KOMBINATIONEN", index=False)
        read_csv(a.mapping).to_excel(w, sheet_name="KNOTEN_MAPPING", index=False)
        delta.to_excel(w, sheet_name="KERNKNOTEN_DELTA", index=False)
        read_csv(a.export / "01_Seilkraefte_N.csv").to_excel(w, sheet_name="SEILKRAEFTE_N", index=False)
        read_csv(a.export / "02_Lagerkraefte_global.csv").to_excel(w, sheet_name="LAGERKRAEFTE", index=False)
        pd.DataFrame(OFFEN, columns=["Nr", "Frage"]).assign(Status="OFFEN (ID01)").to_excel(
            w, sheet_name="OFFENE_PUNKTE", index=False)
    print(f"OK: {len(delta)} Kernknoten-Zeilen → {out.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
