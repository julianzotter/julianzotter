"""
NEXUS Kernel Router — AEC nachweis_typ → kernel module mapping.
Loads routing table from config/signal_matrix.yaml.
Complements signal_matrix.py (domain scoring) and moe_router.py (expert activation).
"""
from pathlib import Path
from typing import Optional
import yaml

_YAML_PATH = Path(__file__).parent.parent / "config" / "signal_matrix.yaml"
_TABLE: list[dict] = []


def _load() -> None:
    global _TABLE
    with open(_YAML_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    _TABLE = data.get("signals", [])


def get_kernel(norm_tag: str, nachweis_typ: str) -> Optional[dict]:
    """Return the routing entry for (norm_tag, nachweis_typ) or None."""
    if not _TABLE:
        _load()
    norm_tag = norm_tag.upper()
    nachweis_typ = nachweis_typ.upper()
    for entry in _TABLE:
        if entry.get("norm_tag", "").upper() == norm_tag and \
           entry.get("nachweis_typ", "").upper() == nachweis_typ:
            return entry
    return None


def route_kernel(norm_tag: str, nachweis_typ: str) -> dict:
    """
    Primary entry point for AEC kernel dispatch.
    Returns routing dict with kernel path and status, or a NOT_FOUND sentinel.
    """
    entry = get_kernel(norm_tag, nachweis_typ)
    if entry is None:
        return {
            "norm_tag": norm_tag,
            "nachweis_typ": nachweis_typ,
            "kernel": None,
            "status": "NOT_FOUND",
            "validated": False,
        }
    return {
        "id": entry.get("id"),
        "norm_tag": entry["norm_tag"],
        "nachweis_typ": entry["nachweis_typ"],
        "norm_ref": entry.get("norm_ref"),
        "kernel": entry.get("kernel"),
        "golden_case": entry.get("golden_case"),
        "status": entry.get("status", "UNKNOWN"),
        "validated": entry.get("validated", False),
        "notes": entry.get("notes"),
    }


def list_kernels(status_filter: Optional[str] = None) -> list[dict]:
    """Return all routing entries, optionally filtered by status."""
    if not _TABLE:
        _load()
    if status_filter:
        return [e for e in _TABLE if e.get("status") == status_filter.upper()]
    return list(_TABLE)


def coverage_report() -> dict:
    """Return a summary of implementation coverage across all signals."""
    if not _TABLE:
        _load()
    counts: dict[str, int] = {}
    for entry in _TABLE:
        s = entry.get("status", "UNKNOWN")
        counts[s] = counts.get(s, 0) + 1
    total = len(_TABLE)
    implemented = counts.get("IMPLEMENTED", 0)
    return {
        "total": total,
        "implemented": implemented,
        "coverage_pct": round(implemented / total * 100, 1) if total else 0,
        "by_status": counts,
    }
