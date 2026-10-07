"""Verifikation der dlubal.api-Schreibschnittstelle – nur Introspektion, keine Änderung am Modell.

Druckt: SDK-Version, vorhandene Application-Methoden (create/update/delete/calculate),
Feldnamen der Protobuf-Klassen Node, Member, NodalSupport, LoadCombination,
und die ResultsType-Kategorien mit NODES/MEMBERS. Ergebnis als JSON für das Quellenlog RF6.

Aufruf (venv mit dlubal.api==2.13.1):
  python 26_10_06_ID-03_api_write_check.py > API_WRITE_CHECK_<Datum>.json
Kein API-Key nötig, keine Verbindung zu RFEM: es wird nur das Paket inspiziert.
"""
from __future__ import annotations

import importlib.metadata
import json
import sys

WRITE_METHODS = ["create_object", "create_object_list", "update_object", "update_object_list",
                 "delete_object", "delete_object_list", "get_object", "get_object_list",
                 "calculate_all", "calculate_specific", "has_results", "save_model", "close_model",
                 "get_active_model", "get_results", "get_result_table"]
CLASSES = {"Node": ("structure_core", "Node"), "Member": ("structure_core", "Member"),
           "NodalSupport": ("types_for_nodes", "NodalSupport"),
           "LoadCase": ("loading", "LoadCase"), "LoadCombination": ("loading", "LoadCombination"),
           "NodalLoad": ("loads", "NodalLoad")}


def fields(cls) -> list[str]:
    desc = getattr(cls, "DESCRIPTOR", None)
    return sorted(desc.fields_by_name) if desc else []


def main() -> int:
    from dlubal.api import rfem
    out = {"sdk_version": importlib.metadata.version("dlubal.api"),
           "application_methods": {m: hasattr(rfem.Application, m) for m in WRITE_METHODS},
           "classes": {}, "results_types": []}
    for label, (mod, name) in CLASSES.items():
        cls = getattr(getattr(rfem, mod, None), name, None)
        out["classes"][label] = {"found": cls is not None, "fields": fields(cls) if cls else []}
    keys = rfem.results.ResultsType.keys()
    out["results_types"] = sorted(k for k in keys if "NODES" in k or "MEMBERS" in k)
    out["verdict"] = ("WRITE_API_PRESENT" if all(out["application_methods"][m] for m in
                      ("create_object", "update_object", "delete_object", "calculate_all"))
                      else "WRITE_API_INCOMPLETE")
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
