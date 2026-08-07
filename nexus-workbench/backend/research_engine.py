"""
NEXUS Deep-Web Research Engine — generates prioritized URL lists per scope.
Integrates with ScrapeGraphAI for extraction; returns SeedContext ≤8192 tokens.
"""
import json
from pathlib import Path

_REG = Path(__file__).parent.parent / "data" / "source_registry.json"


def _registry() -> dict:
    with open(_REG) as f:
        return json.load(f)


def get_sources(scope: str, top_n: int = 7) -> list[dict]:
    """Return top-n prioritized sources for scope."""
    reg = _registry()
    sources = reg.get(scope, reg.get("ALLGEMEIN", []))
    return sorted(sources, key=lambda s: s["priority"], reverse=True)[:top_n]


def build_url_list(scope: str) -> list[str]:
    return [s["url"] for s in get_sources(scope)]


async def scrape_seed_context(scope: str, max_tokens: int = 8192) -> dict:
    """
    Stub: replace body with ScrapeGraphAI call.
    Returns {context: str, sources: list, token_count: int}.
    """
    sources = get_sources(scope, top_n=5)
    # ScrapeGraphAI integration point:
    # from scrapegraphai.graphs import SmartScraperGraph
    # results = [SmartScraperGraph(url=s["url"], ...).run() for s in sources]
    seed = f"[NEXUS SeedContext — scope={scope}]\n"
    seed += "\n".join(f"[{s['priority']}] {s['name']}: {s['domain']}" for s in sources)
    return {
        "scope": scope,
        "context": seed,
        "sources": sources,
        "token_count": len(seed.split()),
        "max_tokens": max_tokens,
    }
