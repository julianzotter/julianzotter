"""
NEXUS MoE Router — sparse top-2 expert activation per scope.
"""

DOMAINS = {
    "E-STATIK": ["HOLZBAU", "BETONBAU", "STAHLBAU", "FERTIGTEIL"],
    "E-NORMEN": ["HOLZBAU", "BETONBAU", "STAHLBAU", "FERTIGTEIL", "ALLGEMEIN"],
    "E-BIM":    ["BIM"],
    "E-MAT":    ["HOLZBAU", "BETONBAU", "STAHLBAU", "FERTIGTEIL"],
    "E-KI":     ["KI-WERKZEUG"],
    "E-RPT":    ["HOLZBAU", "BETONBAU", "STAHLBAU", "BIM", "FERTIGTEIL", "ALLGEMEIN"],
}

EXPERT_SCORES = {
    "E-STATIK": 0.95, "E-NORMEN": 0.90, "E-BIM": 0.85,
    "E-MAT": 0.88,    "E-KI": 0.92,     "E-RPT": 0.80,
}


def route(scope: str, top_k: int = 2) -> list[dict]:
    """Return top-k active experts for scope with scores."""
    candidates = [
        {"expert": name, "score": EXPERT_SCORES[name], "active": True}
        for name, scopes in DOMAINS.items()
        if scope in scopes
    ]
    candidates.sort(key=lambda x: x["score"], reverse=True)
    active = candidates[:top_k]
    inactive = [
        {"expert": name, "score": EXPERT_SCORES[name], "active": False}
        for name in DOMAINS if name not in {e["expert"] for e in active}
    ]
    return active + inactive


def sparsity(scope: str, top_k: int = 2) -> float:
    total = len(DOMAINS)
    return round((total - top_k) / total, 3)
