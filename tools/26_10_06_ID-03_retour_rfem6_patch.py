"""Phase 3A – Retour in RFEM 6: VAR-A-Geometriepatch (Gerüst, GESPERRT, Dry-Run-Standard).

Was zurückgespielt wird (einzig zulässiger Inhalt, Patch-JSON E7 Rev0):
  1. Knotenkoordinaten 105/106/113/114/3006/3007 (VAR-A-Trafo, Bestand-5e-Anker)   [Gate E1]
  2. Stäbe 1006/1007 + Knoten 2006/2007 löschen; Lager 2006/2007 entfernen;
     3006/3007 als gelenkige Lager wie 105 (Kopie des bestehenden Lagers)          [Gate E2]
  3. Hilfsgeometrie QS 14 löschen (Stäbe 158, 178–193; 20 Knoten; QS 14–17)       [Gate P2]
  4. LK220 = 1,35·LF10 + 1,50·LF43 anlegen                                         [Gate E4]
NICHT enthalten und nie vorgesehen: Vorspannung (P1: Sv = N(LK100) ist Ergebnis),
Querschnitt 1 (A = 0,38 cm² belegt), Leuchtenlasten (1,000 kN an Kn 1–30 vorhanden).

Sicherungen:
  - läuft nur, wenn der aktive Modellname "WORKING_CALC" enthält (nie M1)
  - jedes Gate braucht "FREIGEGEBEN" in gates.json (ID01); sonst wird der Schritt übersprungen
  - --apply fehlt → Dry-Run: nur Plan ausgeben, keine Änderung
  - Snapshot-Hash vor/nach über die Bridge (E5) für das Quellenlog RF6 §3
  - API-Methoden/Feldnamen werden zur Laufzeit geprüft (fail-closed), vgl. api_write_check.py
STATUS: CANDIDATE, ungetestet. Freigabe erst nach API_WRITE_CHECK = WRITE_API_PRESENT.

gates.json (Beispiel):
  {"E1": "FREIGEGEBEN", "E2": "OFFEN", "P2": "FREIGEGEBEN", "E4": "OFFEN"}
Aufruf:
  python 26_10_06_ID-03_retour_rfem6_patch.py --patch 26_10_06_ID-03-RF6_GEOMETRIE_PATCH_VARA_Rev0.json --gates gates.json [--apply]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

BRIDGE_FILE = "26_10_06_ID-03-RFEM6_MCP_Bridge_Extended.py"
HILFSKNOTEN = [3025, 3026, 3027, 3028, 3057, 3058, 3060, 3061, 3062, 3063, 3064, 3065,
               3066, 3067, 3068, 3069, 3070, 3071, 3072, 3095]
LK220 = {"no": 220, "items": [(10, 1.35), (43, 1.50)], "name": "LK220 Erg.2 1,35*LF10 + 1,50*LF43"}


def load_bridge(folder: Path):
    spec = importlib.util.spec_from_file_location("rfem_bridge", folder / BRIDGE_FILE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def need(obj, *names: str) -> None:
    """Fail-closed: Methode oder Protobuf-Feld muss existieren."""
    desc = getattr(obj, "DESCRIPTOR", None)
    for n in names:
        ok = hasattr(obj, n) or (desc is not None and n in desc.fields_by_name)
        if not ok:
            raise SystemExit(f"API-Beleg fehlt: {getattr(obj, '__name__', obj)}.{n} → Abbruch (api_write_check.py)")


def plan(patch: dict, gates: dict) -> list[dict]:
    """Schrittliste mit Gate-Status; Reihenfolge ist verbindlich."""
    g = lambda k: gates.get(k) == "FREIGEGEBEN"
    steps = [{"gate": "P2", "ok": g("P2"), "op": "delete_members", "ids": patch["staebe_loeschen"]["hilfsgeometrie_qs14"]},
             {"gate": "P2", "ok": g("P2"), "op": "delete_nodes", "ids": HILFSKNOTEN},
             {"gate": "P2", "ok": g("P2"), "op": "delete_sections", "ids": patch["querschnitte_loeschen"]},
             {"gate": "E2", "ok": g("E2"), "op": "delete_members", "ids": patch["staebe_loeschen"]["maste_entfallen"]},
             {"gate": "E2", "ok": g("E2"), "op": "delete_nodes", "ids": patch["lager"]["entfernen"]},
             {"gate": "E2", "ok": g("E2"), "op": "support_like_105", "ids": patch["lager"]["neu_gelenkig_wie_101_106"]},
             {"gate": "E1", "ok": g("E1"), "op": "set_nodes", "ids": patch["knoten_setzen"]},
             {"gate": "E4", "ok": g("E4"), "op": "create_lk220", "ids": [LK220]}]
    return steps


def apply_step(app, rfem, model, step: dict) -> str:
    """Führt genau einen Schritt aus; Feldnamen werden vorher geprüft."""
    op, ids = step["op"], step["ids"]
    sc, tn, ld = rfem.structure_core, rfem.types_for_nodes, rfem.loading
    if op == "delete_members":
        need(app, "delete_object_list"); app.delete_object_list([sc.Member(no=i) for i in ids], model_id=model)
    elif op == "delete_nodes":
        need(app, "delete_object_list"); app.delete_object_list([sc.Node(no=i) for i in ids], model_id=model)
    elif op == "delete_sections":
        need(app, "delete_object_list"); app.delete_object_list([sc.Section(no=i) for i in ids], model_id=model)
    elif op == "set_nodes":
        need(sc.Node, "coordinate_1", "coordinate_2", "coordinate_3"); need(app, "update_object_list")
        objs = [sc.Node(no=k["knoten"], coordinate_1=k["x"], coordinate_2=k["y"], coordinate_3=k["z"]) for k in ids]
        app.update_object_list(objs, model_id=model)
    elif op == "support_like_105":
        need(tn.NodalSupport, "nodes"); need(app, "get_object_list", "update_object")
        sup = [s for s in app.get_object_list([tn.NodalSupport()], model_id=model) if 105 in list(s.nodes)]
        if len(sup) != 1:
            raise SystemExit(f"Lager an Kn 105 nicht eindeutig ({len(sup)}) → Abbruch")
        sup[0].nodes.extend(ids); app.update_object(sup[0], model_id=model)
    elif op == "create_lk220":
        need(ld.LoadCombination, "no", "items"); need(app, "create_object")
        raise SystemExit("LK220: Feldstruktur von LoadCombination.items im SDK belegen (api_write_check.py), dann freischalten")
    return f"{op} {len(ids)} Objekte"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--patch", type=Path, required=True)
    ap.add_argument("--gates", type=Path, required=True)
    ap.add_argument("--apply", action="store_true", help="ohne Flag: Dry-Run")
    a = ap.parse_args(argv)
    patch = json.loads(a.patch.read_text(encoding="utf-8"))
    gates = json.loads(a.gates.read_text(encoding="utf-8"))
    steps = plan(patch, gates)
    for s in steps:
        print(f"[{'FREI' if s['ok'] else 'GESPERRT'}] {s['gate']}: {s['op']} ({len(s['ids'])})")
    if not a.apply:
        print("DRY-RUN: keine Änderung. --apply nur nach WRITE_API_PRESENT und Freigabe ID01.")
        return 0
    bridge = load_bridge(Path(__file__).resolve().parent)
    before = bridge.execute({"operation": "snapshot"})
    if before.get("status") != "ok":
        raise SystemExit(f"Snapshot vorher fehlgeschlagen: {before}")
    name = str(before.get("model_info", {}).get("name", ""))
    if "WORKING_CALC" not in name:
        raise SystemExit(f"Aktives Modell '{name}' ist nicht WORKING_CALC → Abbruch (M1 nie beschreiben)")
    from dlubal.api import rfem
    app = rfem.Application(api_key_value=bridge.credential("RFEM_API_KEY"))
    model = app.get_active_model()
    log = {"model": name, "guid": model.guid, "snapshot_before": before["input_sha256"], "steps": []}
    try:
        for s in steps:
            log["steps"].append({**{k: s[k] for k in ("gate", "op")}, "result": apply_step(app, rfem, model, s) if s["ok"] else "übersprungen (Gate)"})
    finally:
        app.close_connection()
        after = bridge.execute({"operation": "snapshot"})
        log["snapshot_after"] = after.get("input_sha256")
        Path("RETOUR_LOG.json").write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
        print(json.dumps(log, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
