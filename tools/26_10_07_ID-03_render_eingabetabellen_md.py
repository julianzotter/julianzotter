"""Rendert EINGABEDATEN_RF6_v0.1 (CSV) als prüffähige Markdown-Tabellen (Modell A + Modell B, zwei Varianten).

Aufruf: python 26_10_07_ID-03_render_eingabetabellen_md.py --data <EINGABEDATEN_RF6_v0.1> --out <datei.md>
Variante B-2 = Patch E7 Rev0 (VAR-A, zwei Fassadenanker, Kanon). Variante B-7 = G3-Siebenpunkt (Docx 07.10.),
nur zum Vergleich, Freigabe E1/E2 durch ID01 erforderlich. Es wird nichts berechnet, nur umformatiert
(Winkel rad → °, Zahlen gerundet wie in der CSV).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

G3 = {105: (122.071816, 56.970598, -0.129), 106: (151.161724, 36.990289, 0.262), 113: (171.514489, 36.430740, -0.612),
      114: (172.194131, 11.139194, -0.783), 3006: (142.074985, 58.490902, -0.038), 3007: (161.455905, 44.182774, 0.186),
      3021: (192.948951, 15.945504, 0.937)}


def rd(p: Path) -> list[dict]:
    with p.open(encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh, delimiter=";"))


def md(rows: list[dict], cols: list[str], heads: list[str] | None = None) -> str:
    heads = heads or cols
    out = ["| " + " | ".join(heads) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |")
    return "\n".join(out)


def fmt_node(r: dict) -> dict:
    return {**r, "x_m": f"{float(r['x_m']):.3f}", "y_m": f"{float(r['y_m']):.3f}", "z_m": f"{float(r['z_m']):.3f}"}


def render_a(d: Path) -> str:
    a = d / "A_BESTAND"
    s = ["## A Modell A — Bestand 5e (Quelle U10 RF5-COM-Export; Lasten model.db M5)\n"]
    s.append("### A1 Knoten (86) — RFEM lokal, Z positiv nach unten [m]\n")
    s.append(md([fmt_node(r) for r in rd(a / "01_knoten.csv")], ["no", "x_m", "y_m", "z_m"], ["Kn", "X [m]", "Y [m]", "Z [m]"]))
    s.append("\n### A2 Stäbe (88) — Typ 9 = Seil (nur Zug), Typ 1 = Balken; QS i → j = Voute\n")
    rows = [{**r, "laenge_m": f"{float(r['laenge_m']):.3f}"} for r in rd(a / "02_staebe.csv")]
    s.append(md(rows, ["no", "typ_text", "knoten_i", "knoten_j", "qs_start", "qs_ende", "laenge_m", "linie"],
                ["Stab", "Typ", "Kn i", "Kn j", "QS i", "QS j", "L [m]", "Linie RF5"]))
    s.append("\n### A3 Materialien (6) — E, G in kN/cm²\n")
    s.append(md(rd(a / "03_materialien.csv"), ["no", "bezeichnung", "E_kN_cm2", "G_kN_cm2", "nu", "gamma_kN_m3", "alpha_T_1_K", "gamma_M", "hinweis"],
                ["Mat", "Bezeichnung", "E", "G", "ν", "γ [kN/m³]", "α_T [1/K]", "γ_M", "Hinweis"]))
    s.append("\n### A4 Querschnitte (13) — cm², cm⁴\n")
    s.append(md(rd(a / "04_querschnitte.csv"), ["no", "bezeichnung", "material", "A_cm2", "Ay_cm2", "Az_cm2", "It_cm4", "Iy_cm4", "Iz_cm4", "verwendung"],
                ["QS", "Bezeichnung", "Mat", "A", "Ay", "Az", "It", "Iy", "Iz", "Verwendung"]))
    s.append("\n### A5 Lager (27 Objekte, 35 Knoten) — fest/frei, Drehung des Lager-Bezugssystems um Z\n")
    rows = [{**r, "deg": f"{math.degrees(float(r['drehung_z_rad'])):.2f}"} for r in rd(a / "05_lager.csv")]
    s.append(md(rows, ["no", "knoten", "ux", "uy", "uz", "phix", "phiy", "phiz", "deg"],
                ["Lager", "Knoten", "u_x", "u_y", "u_z", "φ_x", "φ_y", "φ_z", "Drehung Z [°]"]))
    s.append("\n### A6 Rechenparameter (RF5-Einstellungen U10)\n")
    s.append(md(rd(a / "06_rechenparameter.csv"), ["parameter", "wert", "hinweis"], ["Parameter", "Wert", "Hinweis"]))
    s.append("\n### A7 Knotenlasten (17) — kN, RFEM lokal (Z nach unten positiv)\n")
    s.append(md(rd(a / "07_knotenlasten.csv"), ["LF", "nr", "Fx_kN", "Fy_kN", "Fz_kN", "anzahl", "knoten"],
                ["LF", "Nr", "F_x", "F_y", "F_z", "n", "Knoten"]))
    s.append("\n### A8 Stablasten (18) — kN/m bzw. ΔT [K]; Richtungscode RF6-intern (gegen RF5-Ausdruck prüfen)\n")
    s.append(md(rd(a / "08_stablasten.csv"), ["LF", "lf_name", "nr", "art", "wert", "richtung_code_rf6", "anzahl", "staebe"],
                ["LF", "LF-Name", "Nr", "Art", "Wert", "Richtung", "n", "Stäbe"]))
    s.append("\n### A9 Lastfälle (19) und Lastkombinationen (21 + LK220 fehlend)\n")
    s.append(md(rd(a / "09_lastfaelle_lastkombinationen.csv"), ["typ", "nr", "name", "actionCategoryId", "definition", "quelle"],
                ["Typ", "Nr", "Name", "Kategorie-ID", "Definition / Faktoren", "Quelle"]))
    return "\n".join(s)


def render_b(d: Path) -> str:
    b = d / "B_VARA"
    nodes = {int(r["no"]): (float(r["x_m"]), float(r["y_m"]), float(r["z_m"])) for r in rd(d / "A_BESTAND" / "01_knoten.csv")}
    patch = json.loads((b / "10_patch_vara_rev0.json").read_text(encoding="utf-8"))
    s = ["## B Modell B — Ergänzung 4 (Modell A + Patch)\n",
         "### B1 Variante B-2 (Kanon, Patch E7 Rev0, Transformation T1 VAR-A, RMS 0,098 m): Knoten setzen\n"]
    rows = []
    for k in patch["knoten_setzen"]:
        bx, by, bz = nodes[k["knoten"]]
        rows.append({"kn": k["knoten"], "label": k["label"], "x": f"{k['x']:.3f}", "y": f"{k['y']:.3f}", "z": f"{k['z']:.3f}",
                     "d": f"{math.hypot(k['x'] - bx, k['y'] - by):.3f}", "basis": k["basis"]})
    s.append(md(rows, ["kn", "label", "x", "y", "z", "d", "basis"], ["Kn", "Label", "X [m]", "Y [m]", "Z [m]", "ΔXY zu 5e [m]", "Basis"]))
    s.append("\n### B2 Variante B-2: Löschen / Lager\n")
    rows = [{"o": "Stab", "n": n, "g": "Mast entfällt (C06/C07 → Fassadenanker)"} for n in patch["staebe_loeschen"]["maste_entfallen"]]
    rows += [{"o": "Knoten", "n": n, "g": "Mastfuß entfällt, Lager entfernen"} for n in patch["lager"]["entfernen"]]
    rows += [{"o": "Lager neu", "n": n, "g": "gelenkig wie Kn 105 (u fest, φ_x φ_y frei, φ_z fest); Drehung analog Wandanker (Auflage ID01)"} for n in patch["lager"]["neu_gelenkig_wie_101_106"]]
    s.append(md(rows, ["o", "n", "g"], ["Objekt", "Nr", "Aktion / Grund"]))
    s.append("\nKontrolle nach Patch: 84 Knoten / 68 Seile / 18 Maste / 25 Lagerobjekte (27 − 2 + Erweiterung Lager 105 um 3006/3007). "
             "Lasten unverändert (LF10 30 × 1,000 kN; Kabel; Wind; Eis; ΔT). LK220 = 1,35·LF10 + 1,50·LF43 ergänzen (E4).\n")
    s.append("### B3 Variante B-7 (Docx 07.10., G3-Siebenpunkt, Transformation T2, RMSE 0,62 m) — NUR VERGLEICH, nicht freigegeben (E1/E2)\n")
    rows = []
    for k, (x, y, z) in G3.items():
        bx, by, bz = nodes[k]
        rows.append({"kn": k, "x": f"{x:.6f}", "y": f"{y:.6f}", "z": f"{z:.3f}", "d": f"{math.hypot(x - bx, y - by):.3f}",
                     "h": "Wandanker: physisch unverändert, Δ = Transformationsartefakt T2" if k < 1000 else
                     ("C21: E3 Fall A/B" if k == 3021 else "C06/C07: als Mastkopf behandelt, Z = Bestand; widerspricht Ergänzung 4 (Fassadenanker, z 0,452)")})
    s.append(md(rows, ["kn", "x", "y", "z", "d", "h"], ["Kn", "X [m]", "Y [m]", "Z [m]", "ΔXY zu 5e [m]", "Befund"]))
    return "\n".join(s)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    man = json.loads((a.data / "MANIFEST.json").read_text(encoding="utf-8"))
    head = ["# EINGABETABELLEN RFEM 6 — Seilstatik Böblingen, Ergänzung 4 — aus EINGABEDATEN_RF6_v0.1 (ID-03, 07.10.2026)\n",
            "Quellen (SHA-256): " + "; ".join(f"{k} {v[:12]}…" for k, v in man["quellen_sha256"].items()) + "\n",
            "Regeln: keine Vorspannung (Sv = N(LK100) ist Ergebnis), keine Formfindung, Bestandslasten 1:1. Einheiten m, kN, kN/m, K, cm², cm⁴.\n"]
    text = "\n".join(head) + "\n" + render_a(a.data) + "\n\n" + render_b(a.data) + "\n"
    a.out.write_text(text, encoding="utf-8")
    print(a.out, hashlib.sha256(text.encode()).hexdigest()[:16], len(text.splitlines()), "Zeilen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
