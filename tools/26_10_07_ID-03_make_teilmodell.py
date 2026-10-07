"""Teilmodell T (Modellreduktion um C06/C07) aus EINGABEDATEN_RF6_v0.1 ableiten.

Modellgrenze (Topologie, Ring-Analyse 02_staebe.csv): alle Ränder des Teilmodells sind echte Lager
(Wandanker 105/106/113/114, Mastfuß 2021, bei Modell A-T auch 2006/2007) bis auf EINEN Schnittknoten 8,
an dem das Netz über S16 (8-6) und S23 (8-11) weiterläuft. Randbedingung an Kn 8: R1 starr oder
R2 verschieblich (Zwangsverformung u_RF5 je LK). Lasten, Materialien, QS, LF/LK werden 1:1 gefiltert.
Aufruf: python 26_10_07_ID-03_make_teilmodell.py --data <EINGABEDATEN_RF6_v0.1> --out <Zielordner>
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

KERN = {3006, 3007}
NETZ = {9, 10, 29, 30, 330, 8}
ANKER = {105, 106, 113, 114}
MAST_BLEIBT = {3021, 2021}
MAST_ENTFAELLT = {2006, 2007}
SCHNITT = {8}
STAEBE_A = [17, 18, 19, 20, 21, 22, 60, 61, 62, 63, 64, 81, 1021, 1006, 1007]
WEG_B = {1006, 1007}
PATCH = {3006: (142.648, 58.743, 0.452), 3007: (161.883, 44.239, 0.452)}


def rd(p: Path) -> list[dict]:
    with p.open(encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh, delimiter=";"))


def wr(p: Path, rows: list[dict], cols: list[str]) -> int:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter=";", extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    return len(rows)


def ids(s: str) -> list[int]:
    out = []
    for t in str(s).replace(" ", "").split(","):
        if "-" in t:
            a, b = t.split("-"); out += list(range(int(a), int(b) + 1))
        elif t:
            out.append(int(t))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", type=Path, required=True); ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(); A = a.data / "A_BESTAND"; O = a.out; n = {}
    kn_a = KERN | NETZ | ANKER | MAST_BLEIBT | MAST_ENTFAELLT
    kn_b = kn_a - MAST_ENTFAELLT
    rolle = {**{k: "Kern (geaenderter Haltepunkt)" for k in KERN}, **{k: "Netzknoten" for k in NETZ}, **{k: "Wandanker (Lager)" for k in ANKER},
             3021: "Mastkopf C21 (bleibt)", 2021: "Mastfuss C21 (Lager)", 2006: "Mastfuss C06 (nur Modell A-T)", 2007: "Mastfuss C07 (nur Modell A-T)", 8: "SCHNITTKNOTEN (Modellgrenze, Randbedingung R1/R2)"}
    kn = [r for r in rd(A / "01_knoten.csv") if int(r["no"]) in kn_a]
    for r in kn:
        k = int(r["no"]); r["rolle"] = rolle[k]; r["in_modell_A_T"] = "ja"; r["in_modell_B_T"] = "ja" if k in kn_b else "nein (entfaellt)"
        px = PATCH.get(k); r["x_m_B"], r["y_m_B"], r["z_m_B"] = (px if px else (r["x_m"], r["y_m"], r["z_m"])) if k in kn_b else ("", "", "")
    n["T01_knoten"] = wr(O / "T01_knoten.csv", kn, ["no", "x_m", "y_m", "z_m", "x_m_B", "y_m_B", "z_m_B", "rolle", "in_modell_A_T", "in_modell_B_T", "quelle"])
    st = [r for r in rd(A / "02_staebe.csv") if int(r["no"]) in STAEBE_A]
    for r in st:
        r["in_modell_B_T"] = "nein (Mast entfaellt)" if int(r["no"]) in WEG_B else "ja"
        r["weggelassen_am_schnitt"] = ""
    st_cut = [{"no": 16, "knoten_i": 8, "knoten_j": 6, "typ_text": "Seil", "in_modell_B_T": "nein", "weggelassen_am_schnitt": "ja (ausserhalb Modellgrenze)"},
              {"no": 23, "knoten_i": 11, "knoten_j": 8, "typ_text": "Seil", "in_modell_B_T": "nein", "weggelassen_am_schnitt": "ja (ausserhalb Modellgrenze)"}]
    n["T02_staebe"] = wr(O / "T02_staebe.csv", st + st_cut, ["no", "typ_text", "knoten_i", "knoten_j", "qs_start", "qs_ende", "laenge_m", "in_modell_B_T", "weggelassen_am_schnitt", "quelle"])
    qs_used = {int(r["qs_start"]) for r in st} | {int(r["qs_ende"]) for r in st}
    qs = [r for r in rd(A / "04_querschnitte.csv") if int(r["no"]) in qs_used]
    mat_used = {int(r["material"]) for r in qs}
    n["T03_materialien"] = wr(O / "T03_materialien.csv", [r for r in rd(A / "03_materialien.csv") if int(r["no"]) in mat_used],
                              ["no", "bezeichnung", "E_kN_cm2", "G_kN_cm2", "nu", "gamma_kN_m3", "alpha_T_1_K", "gamma_M", "hinweis"])
    n["T04_querschnitte"] = wr(O / "T04_querschnitte.csv", qs, ["no", "bezeichnung", "material", "A_cm2", "Ay_cm2", "Az_cm2", "It_cm4", "Iy_cm4", "Iz_cm4", "verwendung"])
    lag = []
    for r in rd(A / "05_lager.csv"):
        hit = sorted(set(ids(r["knoten"])) & kn_a)
        if hit:
            r["knoten_im_teilmodell"] = ",".join(map(str, hit)); r["in_modell_B_T"] = "nein (Mastfuss entfaellt)" if set(hit) <= MAST_ENTFAELLT else "ja"; lag.append(r)
    lag.append({"no": "NEU-B", "knoten": "3006,3007", "knoten_im_teilmodell": "3006,3007", "ux": "fest", "uy": "fest", "uz": "fest", "phix": "frei", "phiy": "frei", "phiz": "fest",
                "drehung_z_rad": "wie Lager Kn 105 (-0.7853982), Auflage ID01", "in_modell_B_T": "ja (nur Modell B-T)", "hinweis": "Fassadenanker C06/C07, gelenkig wie Wandanker"})
    lag.append({"no": "RAND-8", "knoten": "8", "knoten_im_teilmodell": "8", "ux": "R1 fest / R2 u_x(LK)", "uy": "R1 fest / R2 u_y(LK)", "uz": "R1 fest / R2 u_z(LK)", "phix": "frei", "phiy": "frei", "phiz": "frei",
                "drehung_z_rad": "0", "in_modell_B_T": "ja", "hinweis": "Modellgrenze: R1 starr (Standard heute) oder R2 Knoten-Zwangsverformung aus RF5 (T10)"})
    n["T05_lager"] = wr(O / "T05_lager.csv", lag, ["no", "knoten", "knoten_im_teilmodell", "ux", "uy", "uz", "phix", "phiy", "phiz", "drehung_z_rad", "in_modell_B_T", "hinweis"])
    n["T06_rechenparameter"] = wr(O / "T06_rechenparameter.csv", rd(A / "06_rechenparameter.csv"), ["parameter", "wert", "hinweis"])
    kl = []
    for r in rd(A / "07_knotenlasten.csv"):
        hit = sorted(set(ids(r["knoten"])) & kn_a)
        if hit:
            r["knoten"] = ",".join(map(str, hit)); r["anzahl"] = len(hit); kl.append(r)
    n["T07_knotenlasten"] = wr(O / "T07_knotenlasten.csv", kl, ["LF", "nr", "Fx_kN", "Fy_kN", "Fz_kN", "anzahl", "knoten"])
    sl = []
    for r in rd(A / "08_stablasten.csv"):
        hit = sorted(set(ids(r["staebe"])) & set(STAEBE_A))
        if hit:
            r["staebe"] = ",".join(map(str, hit)); r["anzahl"] = len(hit); sl.append(r)
    n["T08_stablasten"] = wr(O / "T08_stablasten.csv", sl, ["LF", "lf_name", "nr", "art", "wert", "richtung_code_rf6", "anzahl", "staebe"])
    n["T09_lastfaelle_lastkombinationen"] = wr(O / "T09_lastfaelle_lastkombinationen.csv", rd(A / "09_lastfaelle_lastkombinationen.csv"), ["typ", "nr", "name", "actionCategoryId", "definition", "quelle"])
    lks = [r["nr"] for r in rd(A / "09_lastfaelle_lastkombinationen.csv") if r["typ"] == "LK"]
    n["T10_randbedingung_schnittknoten"] = wr(O / "T10_randbedingung_schnittknoten.csv",
        [{"knoten": 8, "LK": lk, "option_R1": "u_x=u_y=u_z=0 (starr)", "option_R2_ux_m": "", "option_R2_uy_m": "", "option_R2_uz_m": "", "quelle_R2": "RF5 13bb Ergebnis Knoten 8, LK " + lk + " (einzutragen)"} for lk in lks],
        ["knoten", "LK", "option_R1", "option_R2_ux_m", "option_R2_uy_m", "option_R2_uz_m", "quelle_R2"])
    n["T11_change_allowlist"] = wr(O / "T11_change_allowlist.csv", [
        {"objekt": "Knoten", "id": 3006, "aktion": "Koordinaten setzen", "alt": "141.809;58.051;-0.038", "neu": "142.648;58.743;0.452", "grund": "C06 -> Fassadenanker (Geometer 7101, T1)", "freigabe": "ID01 07.10.2026"},
        {"objekt": "Knoten", "id": 3007, "aktion": "Koordinaten setzen", "alt": "160.376;43.764;0.186", "neu": "161.883;44.239;0.452", "grund": "C07 -> Fassadenanker (Geometer 7102, T1)", "freigabe": "ID01 07.10.2026"},
        {"objekt": "Stab", "id": 1006, "aktion": "loeschen", "alt": "Mast 3006-2006", "neu": "-", "grund": "Pylon C06 entfaellt", "freigabe": "ID01 07.10.2026"},
        {"objekt": "Stab", "id": 1007, "aktion": "loeschen", "alt": "Mast 3007-2007", "neu": "-", "grund": "Pylon C07 entfaellt", "freigabe": "ID01 07.10.2026"},
        {"objekt": "Knoten+Lager", "id": 2006, "aktion": "loeschen", "alt": "Mastfuss, Lager Obj 36", "neu": "-", "grund": "Pylon C06 entfaellt", "freigabe": "ID01 07.10.2026"},
        {"objekt": "Knoten+Lager", "id": 2007, "aktion": "loeschen", "alt": "Mastfuss, Lager Obj 37", "neu": "-", "grund": "Pylon C07 entfaellt", "freigabe": "ID01 07.10.2026"},
        {"objekt": "Lager", "id": "3006,3007", "aktion": "neu gelenkig", "alt": "-", "neu": "u fest, phi_x/phi_y frei, phi_z fest, Drehung wie Kn 105", "grund": "Fassadenanker", "freigabe": "ID01 07.10.2026 (Drehung: Auflage)"},
        {"objekt": "Lager", "id": 8, "aktion": "Randbedingung Modellgrenze", "alt": "freier Netzknoten", "neu": "R1 starr / R2 Zwangsverformung", "grund": "Teilmodell-Schnitt", "freigabe": "ANNAHME ID-03, Bestaetigung ID01 (Skizze)"},
    ], ["objekt", "id", "aktion", "alt", "neu", "grund", "freigabe"])
    man = {"status": "CANDIDATE", "teilmodell": {"knoten_A_T": sorted(kn_a), "knoten_B_T": sorted(kn_b), "staebe_A_T": STAEBE_A, "staebe_B_T": [s for s in STAEBE_A if s not in WEG_B],
           "schnittknoten": sorted(SCHNITT), "weggelassene_staebe_am_schnitt": [16, 23], "kontrolle": {"A_T": f"{len(kn_a)} Kn / {len(STAEBE_A)} St", "B_T": f"{len(kn_b)} Kn / {len(STAEBE_A) - len(WEG_B)} St"}},
           "zeilen": n, "quelle_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(A.glob("*.csv"))},
           "ausgaben_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(O.glob("*.csv"))}}
    (O / "MANIFEST_TEILMODELL.json").write_text(json.dumps(man, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"zeilen": n, "kontrolle": man["teilmodell"]["kontrolle"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
