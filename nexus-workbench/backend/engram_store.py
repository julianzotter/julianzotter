"""
NEXUS Engram O(1) — deterministic key-value norm lookup, no fine-tuning.
Updates in seconds via engram_store.json; confidence=1.0 for audited entries.
"""
import json
from pathlib import Path
from functools import lru_cache

_DATA = Path(__file__).parent.parent / "data" / "engram_store.json"


@lru_cache(maxsize=1)
def _load() -> dict:
    with open(_DATA) as f:
        return json.load(f)


def lookup(key: str) -> dict | None:
    """O(1) retrieval: {val, conf, src} or None."""
    return _load().get(key)


def lookup_scope(scope: str) -> list[dict]:
    """All engrams tagged for a scope."""
    store = _load()
    return [{"key": k, **v} for k, v in store.items() if v.get("scope") == scope]


def all_keys() -> list[str]:
    return list(_load().keys())
