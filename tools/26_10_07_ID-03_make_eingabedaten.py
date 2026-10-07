"""Erzeugt die prüffähigen Eingabetabellen für den RF6-Neuaufbau (Modell A Bestand, Modell B VAR-A).

Quellen (alle read-only, Hashes landen im MANIFEST):
  --rf5json  input_3.json   RF5-COM-Export von U10 BOEB_BESTAND-5e_NEUBERECHNET (23.09.2026): Knoten, Stäbe,
                            Materialien, Querschnitte, Lager, Rechenparameter (SI: m, N, Pa)
  --lines    lines.csv      Linie → Knoten (TEILABGLEICH, RF5 = RF6 belegt, 0 Abweichungen)
  --modeldb  model.db       Arbeitskopie M5 (1:1-Import von V01): Lastfälle, Knoten-/Stab-/Temperaturlasten,
                            Lastkombinationen (nur Lastdaten werden hieraus entnommen)
  --patch    *_GEOMETRIE_PATCH_VARA_Rev0.json   Modell-B-Änderungen (zwei Anker, Löschlisten, Lager)
Ausgabe: <out>/A_BESTAND/*.csv, <out>/B_VARA/*.csv, MANIFEST.json. Einheiten in den CSV: m, kN, kN/m, K.
Keine Vorspannung, keine Formfindung, keine Laständerung: Bestandslasten werden 1:1 übernommen.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
from pathlib import Path



def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write(path: Path, header: list[str], rows: list[list]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def read_lines(p: Path) -> dict[int, tuple[int, int]]:
    out = {}
    with p.open(encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            a, b = json.loads(r["rf6_nodes"])
            out[int(r["line"])] = (a, b)
    return out


def tables_bestand(rf5: dict, lines: dict, out: Path) -> dict:
    n = {}
    n["01_knoten"] = write(out / "01_knoten.csv", ["no", "x_m", "y_m", "z_m", "quelle"],
                           [[k["No"], k["X"], k["Y"], k["Z"], "U10 input_3.json"] for k in rf5["nodes"]])
    mem = rf5["members"]
    n["02_staebe"] = write(out / "02_staebe.csv",
                           ["no", "linie", "knoten_i", "knoten_j", "typ_rf5", "typ_text", "qs_start", "qs_ende", "laenge_m", "quelle"],
                           [[m["No"], m["LineNo"], *lines[m["LineNo"]], m["Type"], "Seil" if m["Type"] == 9 else "Balken",
                             m["StartCrossSectionNo"], m["EndCrossSectionNo"] or m["StartCrossSectionNo"], round(m["Length"], 6), "U10 + lines.csv"]
                            for m in mem])
    n["03_materialien"] = write(out / "03_materialien.csv",
                                ["no", "bezeichnung", "E_kN_cm2", "G_kN_cm2", "nu", "gamma_kN_m3", "alpha_T_1_K", "gamma_M", "hinweis"],
                                [[m["No"], m["Description"], round(m["ElasticityModulus"] / 1e7, 3), round(m["ShearModulus"] / 1e7, 3), round(m["PoissonRatio"], 4),
                                  m["SpecificWeight"] / 1e3, m["ThermalExpansion"], m["PartialSafetyFactor"],
                                  "nicht verwendet, nu = 8,0 und E = 900 GPa sind Bestandsfehler" if m["No"] == 1 else ""] for m in rf5["materials"]])
    n["04_querschnitte"] = write(out / "04_querschnitte.csv",
                                 ["no", "bezeichnung", "material", "A_cm2", "Ay_cm2", "Az_cm2", "It_cm4", "Iy_cm4", "Iz_cm4", "verwendung"],
                                 [[c["No"], c["Description"], c["MaterialNo"], round(c["AxialArea"] * 1e4, 4), round(c["ShearAreaY"] * 1e4, 4),
                                   round(c["ShearAreaZ"] * 1e4, 4), round(c["TorsionMoment"] * 1e8, 4), round(c["BendingMomentY"] * 1e8, 4),
                                   round(c["BendingMomentZ"] * 1e8, 4), "Seile" if c["No"] == 1 else "Maste (Voute)"] for c in rf5["cross_sections"]])
    n["05_lager"] = write(out / "05_lager.csv",
                          ["no", "knoten", "ux", "uy", "uz", "phix", "phiy", "phiz", "drehung_z_rad", "hinweis"],
                          [[s["No"], s["NodeList"], *(("fest" if s[k] == -1.0 else ("frei" if s[k] == 0 else s[k])) for k in
                            ("SupportConstantX", "SupportConstantY", "SupportConstantZ", "RestraintConstantX", "RestraintConstantY", "RestraintConstantZ")),
                            s["UserDefinedReferenceSystem"]["RotationAngles"]["Z"], "Werte -1 = starr, 0 = frei, sonst Federkonstante"]
                           for s in rf5["nodal_supports"]])
    cs = {**rf5["calc_settings"], **rf5["calc_options"], **rf5["calc_precision"], "solver_code": rf5["calc_solver"], "theory_code": rf5["calc_bending_theory"]}
    n["06_rechenparameter"] = write(out / "06_rechenparameter.csv", ["parameter", "wert", "hinweis"],
                                    [[k, v, ""] for k, v in cs.items()] + [["theorie", "III. Ordnung, Newton-Raphson, g = 10,00 m/s²", "RF5-Ausdruck via BEFUND Rev0 §6 (E7 offen)"]])
    return n


def loads_from_db(db: sqlite3.Connection, out: Path) -> dict:
    q = lambda s, *a: db.execute(s, a).fetchall()
    lc = {r["id"]: r["userID"] for r in q("select id,userID from LoadCase")}
    nid = {r["id"]: r["userID"] for r in q("select id,userID from Node")}
    mid = {r["id"]: r["userID"] for r in q("select id,userID from Member")}
    lfname = {}
    for r in q("select userID,impl_table,impl_id from LoadCase"):
        lfname[r["userID"]] = q(f'select name from "{r["impl_table"]}" where id=?', r["impl_id"])[0][0]
    nodal = []
    for nl in q("select * from NodalLoad order by id"):
        t, i = nl["impl_table"], nl["impl_id"]
        d = dict(q(f'select * from "{t}" where id=?', i)[0])
        nodes = sorted(nid[r["value_id"]] for r in q(f'select * from "{t}_nodes" where id=?', i))
        f = (d["force_x"], d["force_y"], d["force_z"]) if t.endswith("Components") else (0, 0, d["magnitude"])
        nodal.append([lc[nl["parentModelObject_id"]], nl["userID"], f[0] / 1e3, f[1] / 1e3, f[2] / 1e3, len(nodes), ",".join(map(str, nodes))])
    n = {"07_knotenlasten": write(out / "07_knotenlasten.csv", ["LF", "nr", "Fx_kN", "Fy_kN", "Fz_kN", "anzahl", "knoten"], nodal)}
    member = []
    for ml in q("select * from MemberLoad order by id"):
        t, i = ml["impl_table"], ml["impl_id"]
        d = dict(q(f'select * from "{t}" where id=?', i)[0])
        mag = q(f'select * from "{t}_magnitudes" where id=? order by container_order', i)
        mem = sorted(mid[r["reference_id"]] for r in q(f'select * from "{t}_assignedTo" where id=?', i) if r["reference_table"] == "Member")
        kind = "Temperatur_dT_K" if "Temperature" in t else "Streckenlast_kN_m"
        m0 = mag[0] if mag else {}
        val = m0.get("temperaturesOrMagnitudeSecondMagnitude") if kind.startswith("Temp") else m0.get("temperaturesOrMagnitudeFirstMagnitude", 0) / 1e3
        lfno = lc[ml["parentModelObject_id"]]
        member.append([lfno, lfname.get(lfno, ""), ml["userID"], kind, round(val, 6) if val is not None else None, d["loadDirection"],
                       len(mem), ",".join(map(str, mem))])
    n["08_stablasten"] = write(out / "08_stablasten.csv", ["LF", "lf_name", "nr", "art", "wert", "richtung_code_rf6", "anzahl", "staebe"], member)
    return n


def tables_vara(patch: dict, out: Path) -> dict:
    n = {"11_knoten_patch": write(out / "11_knoten_patch.csv", ["knoten", "label", "x_m", "y_m", "z_m", "basis"],
                                  [[k["knoten"], k["label"], k["x"], k["y"], k["z"], k["basis"]] for k in patch["knoten_setzen"]])}
    rows = [["Stab", s, "Mast entfällt (C06/C07 → Fassadenanker)"] for s in patch["staebe_loeschen"]["maste_entfallen"]]
    rows += [["Knoten", k, "Mastfuß entfällt"] for k in patch["lager"]["entfernen"]]
    n["12_loeschen"] = write(out / "12_loeschen.csv", ["objekt", "nr", "grund"], rows)
    n["13_lager_patch"] = write(out / "13_lager_patch.csv", ["knoten", "aktion", "vorbild", "hinweis"],
                                [[k, "neu gelenkig", "Lager an Kn 105 (A05)", patch["lager"]["hinweis"]] for k in patch["lager"]["neu_gelenkig_wie_101_106"]] +
                                [[k, "Lager entfernen", "", ""] for k in patch["lager"]["entfernen"]])
    n["14_offen"] = write(out / "14_offen.csv", ["punkt"], [[p] for p in patch["offen_nicht_im_patch"]] +
                          [["LK220 = 1,35*LF10 + 1,50*LF43 anlegen (Erg. 2)"], ["Kontrolle nach Patch: 84 Knoten / 68 Seile / 18 Maste"]])
    return n


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    for a in ("rf5json", "lines", "modeldb", "patch"):
        ap.add_argument(f"--{a}", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    rf5 = json.loads(a.rf5json.read_text(encoding="utf-8"))
    counts = tables_bestand(rf5, read_lines(a.lines), a.out / "A_BESTAND")
    db = sqlite3.connect(f"file:{a.modeldb}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    counts |= loads_from_db(db, a.out / "A_BESTAND")
    counts |= tables_vara(json.loads(a.patch.read_text(encoding="utf-8")), a.out / "B_VARA")
    manifest = {"status": "CANDIDATE", "modell_a_quelle": rf5["info"], "zeilen": counts,
                "quellen_sha256": {p.name: sha(p) for p in (a.rf5json, a.lines, a.modeldb, a.patch)},
                "ausgaben_sha256": {str(p.relative_to(a.out)): sha(p) for p in sorted(a.out.rglob("*.csv"))},
                "regeln": ["Lasten 1:1 Bestand (LF10 = 30 x 1,000 kN)", "keine Vorspannung", "keine Formfindung",
                           "Modell B = Modell A + B_VARA/*.csv; C21/E3, E4, E6 offen"]}
    (a.out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(counts, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
