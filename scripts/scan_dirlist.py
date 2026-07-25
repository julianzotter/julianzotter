#!/usr/bin/env python3
"""
scan_dirlist.py — Windows DIRLIST → source_registry.jsonl
ZotterConsult LLM-Wiki · Stand: 2026-07-25

Usage:
    python scripts/scan_dirlist.py <dirlist.txt> [output.jsonl]

Reads a Windows `dir` / `dir /s` listing, auto-classifies every file entry
into one of 10 knowledge clusters, assigns priority (P0–PX) and authority
class (A–E), and writes an append-mode JSONL registry.

Semantic suggestion: a second pass scores every unclassified file against
all cluster keyword profiles and returns the top-2 probabilistic cluster
candidates (stored in the entry as `cluster_suggestions`).
"""

import sys
import re
import json
import hashlib
import os
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import Optional


# ---------------------------------------------------------------------------
# Cluster definitions — keyword profiles for auto-classification
# ---------------------------------------------------------------------------
CLUSTERS = {
    "registry-index": {
        "label": "Registry & Index",
        "keywords": [
            "dirlist", "registry", "index", "workflow_registry", "yaml",
            "manifest", "archive", "deployment", "konsensfindung",
            "sandbox", "verzeichnis", "csv_inventory",
        ],
        "extensions": [".yaml", ".yml", ".csv"],
        "filename_patterns": [
            r"DIRLIST", r"_REGISTRY", r"_INDEX", r"_MANIFEST",
            r"00_DIR", r"REGISTRY\.yaml",
        ],
    },
    "ai-os-dashboards": {
        "label": "AI-OS Dashboards",
        "keywords": [
            "dashboard", "control_tower", "nexus", "statusreport",
            "ai_os", "human_ai_os", "control_twoer", "deepseek_knowledge",
            "digital_brain", "voice_control", "wissenscluster",
        ],
        "extensions": [".html"],
        "filename_patterns": [
            r"DASHBOARD", r"CONTROL.TOW", r"NEXUS", r"AI.OS.STATUS",
            r"HUMAN.AI.OS", r"digital.brain", r"wissenscluster",
        ],
    },
    "knowledge-management": {
        "label": "Knowledge Management",
        "keywords": [
            "wissensmanagement", "knowledge_base", "knowledgebase",
            "llm_filesystem", "wiki", "peer_review", "ingest",
            "rag_system", "promptbase", "wissens_extraktion",
            "perplexity", "second_brain", "gemini_knowledge",
        ],
        "extensions": [".txt", ".docx", ".pdf"],
        "filename_patterns": [
            r"KNOWLEDGEBASE", r"KNOWLEDGE.BASE", r"WISSENSMANAGEMENT",
            r"LLM.FILESYSTEM", r"PEER.REVIEW", r"RAG.System",
            r"FAST.SEARCH.PROMPTBASE", r"PERPLEXITY.MEMORIES",
            r"GEMINI.PROMPT.VORLAGE", r"PROMPT_DEV", r"KI.Assistent",
        ],
    },
    "llm-engineering": {
        "label": "LLM Engineering",
        "keywords": [
            "deepseek", "llm", "moe", "ai_engineering", "model",
            "workflow_compiler", "stepwise_runtime", "deep_thinking",
            "ai_os_moe", "or1on", "genesis", "engram", "seed_condensation",
            "ollama", "qwen", "ki_entwickler",
        ],
        "extensions": [".txt", ".docx", ".pdf"],
        "filename_patterns": [
            r"DEEPSEEK", r"AI.ENGINEERING", r"OR1ON", r"Genesis",
            r"NEXUS.WORKFLOW.COMPILER", r"DEEP.THINKING",
            r"AI_OS_MoE", r"STEPWISE.RUNTIME", r"Ollama",
            r"Priorisierte.Link", r"Engram", r"MoE", r"DSpark",
        ],
    },
    "workflow-automation": {
        "label": "Workflow & Automation",
        "keywords": [
            "workflow", "automation", "orchestrator", "agent",
            "gamma", "office_management", "rollout", "grundordnung",
            "claude_code", "copilot", "review_rollout",
        ],
        "extensions": [".txt", ".docx", ".js"],
        "filename_patterns": [
            r"REVIEW.ROLLOUT", r"GRUNDORDNUNG", r"GAMMA", r"OFFICE.MANAGEMENT",
            r"GLOBAL.ORCHESTRATOR", r"CUX.CLAUDE", r"Business.Account",
        ],
    },
    "engineering-ec2": {
        "label": "Engineering EC2 / Eurocode",
        "keywords": [
            "ec2", "eurocode", "stahlbeton", "reinforced_concrete",
            "oenorm", "bemessung", "konstruktion", "betonbau",
            "formula_repository", "rc_design", "nad_at", "zilch",
            "lowcarbon", "baustoffe", "nachhaltigkeit",
        ],
        "extensions": [".txt", ".pdf", ".html", ".md", ".zip"],
        "filename_patterns": [
            r"EC2", r"EUROCODE", r"STAHLBETON", r"ec2_oenorm",
            r"RC.DESIGN", r"BETONBAU", r"Zilch", r"Zehetmaier",
            r"Reinforced.concrete", r"LowCarbon", r"Baustoffe",
            r"KnowledgeBase4Structural", r"Wissensdaten_Low",
            r"SCRATCH.COLLECTION.4.LOW", r"Pr.fbericht.EC2",
        ],
    },
    "bookmarks-links": {
        "label": "Bookmarks & Links",
        "keywords": [
            "bookmarks", "favorites", "mozilla", "chrome", "edge",
            "m365", "onedrive", "notebooks", "google_one",
        ],
        "extensions": [".html", ".json"],
        "filename_patterns": [
            r"BOOKMARKS", r"Bookmarks", r"Favorites",
            r"Mozilla", r"MOZILLA", r"MSEDGE", r"CHROME",
            r"M365.CLOUD", r"LISTE.ALLER.NOTEBOOKS",
        ],
    },
    "zotterconsult-projects": {
        "label": "ZotterConsult Projects",
        "keywords": [
            "zotterconsult", "eisteiche", "rohbauausschreibung",
            "lb_hb", "business_account", "onboarding",
        ],
        "extensions": [".txt", ".zip"],
        "filename_patterns": [
            r"EISTEICHE", r"LB.HB.022", r"ROHBAUAUSSCHREIBUNG",
            r"ZOTTERCONSULT", r"Business.Account.Onboard",
        ],
    },
    "images-visuals": {
        "label": "Images & Visuals",
        "keywords": ["pic", "image", "png", "visual", "screenshot", "gemini_generated"],
        "extensions": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"],
        "filename_patterns": [r"PIC\d+", r"Pic\d+", r"_KI-erweitertes_Second_Brain"],
    },
    "tools-code": {
        "label": "Tools & Code",
        "keywords": [
            "chameleon", "ai_os", "python", "javascript", "hardware",
            "cloudflare", "voice_proxy", "implementation",
        ],
        "extensions": [".py", ".js", ".sh", ".bat"],
        "filename_patterns": [
            r"chameleon_ai_os", r"CHAMELEO", r"Cloudflare.Worker",
            r"Voice.Proxy", r"hardware_report", r"HARDWARE.REPORT",
            r"PC.und.LAPTOP",
        ],
    },
}

# ---------------------------------------------------------------------------
# Priority & Authority heuristics
# ---------------------------------------------------------------------------
PRIORITY_RULES = [
    # P0: normative standards
    (r"OENORM|ÖNORM|NAD_AT|EC2_NAD|ec2_oenorm|Reinforced.concrete.design.to.Eurocode",
     "P0", "A"),
    # P0: safety-critical formal validation
    (r"VALIDIERUNGSBERICHT|SHA256|PRUEFBERICHT|QUALIT.TSKONTROILLE|Pr.fbericht",
     "P0", "A"),
    # P1: institutional textbooks
    (r"Zilch|Zehetmaier|Stahlbetonkonstruktion|BASICS.KONSTRUKTION|Eurocode.2.Design.Data",
     "P1", "B"),
    # P1: official registries
    (r"NEXUS_WORKFLOW_REGISTRY\.yaml|MASTER_INDEX|SSOT",
     "P1", "B"),
    # P2: established platform docs
    (r"DEEPSEEK.AI.USER|DEEPSEEK.AI.DEVELOPER|ONLINE.KNOWLEDGE.SOURCE|KNOWLEDGEBASE",
     "P2", "C"),
    # P2: production dashboards
    (r"DASHBOARD|CONTROL.TOWER|CONTROL.TWOER|NEXUS.CONTROL",
     "P2", "C"),
    # P3: supplementary analysis
    (r"AI.ENGINEERING|ENGINEERING.REPOSITORY|RAG.System|FAST.SEARCH",
     "P3", "D"),
    # P3: curated notes
    (r"KI.Assistent|Wissensmanagement|Wissensdaten|GEMINI.PROMPT|PEER.REVIEW",
     "P3", "D"),
    # P4: community/AI-generated
    (r"PERPLEXITY|CHAT|CHATVERLAUF|Bookmarks|BOOKMARKS|MOZILLA|CHROME|MSEDGE|Mozilla",
     "P4", "E"),
    # PX: images, zips, backups, duplicates
    (r"\.png$|\.jpg$|\.zip$|BACKUP|_\(2\)|_\(1\)|\(1\)\.html|\(2\)\.html",
     "PX", "E"),
]


@dataclass
class SourceEntry:
    id: str
    title: str
    filename: str
    source: str
    source_system: str
    cluster: str
    cluster_label: str
    cluster_suggestions: list
    priority: str
    authority_class: str
    confidence: str
    file_size_bytes: int
    file_date: str
    file_ext: str
    status: str
    recommended_action: str
    hash_sha256: str
    ingest_note: str
    tags: list
    indexed_at: str


def classify_cluster(filename: str, ext: str) -> tuple[str, float, list]:
    """Return (best_cluster, score, suggestions_list)."""
    scores = {}
    fname_upper = filename.upper()
    fname_lower = filename.lower()

    for cluster_id, profile in CLUSTERS.items():
        score = 0.0
        # Extension match (weight 0.3)
        if ext.lower() in profile["extensions"]:
            score += 0.3
        # Filename pattern match (weight 0.5 each, capped at 1.0)
        pattern_hits = sum(
            1 for p in profile["filename_patterns"]
            if re.search(p, filename, re.IGNORECASE)
        )
        score += min(pattern_hits * 0.5, 1.0)
        # Keyword match in filename (weight 0.2 each, capped at 0.8)
        kw_hits = sum(
            1 for kw in profile["keywords"]
            if kw.replace("_", " ").upper() in fname_upper
            or kw.replace("_", ".").upper() in fname_upper
            or kw.lower() in fname_lower
        )
        score += min(kw_hits * 0.2, 0.8)
        scores[cluster_id] = score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_cluster, best_score = ranked[0]
    suggestions = [
        {"cluster": c, "score": round(s, 3)}
        for c, s in ranked[1:3]
        if s > 0.1
    ]
    return best_cluster, best_score, suggestions


def assign_priority(filename: str) -> tuple[str, str]:
    """Return (priority, authority_class)."""
    for pattern, priority, authority in PRIORITY_RULES:
        if re.search(pattern, filename, re.IGNORECASE):
            return priority, authority
    return "P3", "D"


def recommended_action(priority: str, cluster: str, ext: str) -> str:
    if priority == "PX":
        return "ARCHIVE"
    if ext in [".zip", ".pdf"] and cluster != "engineering-ec2":
        return "REVIEW"
    if priority in ("P0", "P1"):
        return "INGEST"
    if priority == "P2":
        return "INGEST"
    if priority in ("P3", "P4"):
        return "REVIEW"
    return "REVIEW"


def confidence_from_priority(priority: str) -> str:
    mapping = {"P0": "HIGH", "P1": "HIGH", "P2": "MED", "P3": "MED",
               "P4": "LOW", "PX": "LOW"}
    return mapping.get(priority, "LOW")


def parse_dirlist(text: str) -> list[dict]:
    """
    Parse Windows `dir` format lines:
      DD.MM.YYYY  HH:MM    <DIR>   dirname
      DD.MM.YYYY  HH:MM    123456  filename
    """
    # Matches: date  time  (size or <DIR>)  name
    line_re = re.compile(
        r"(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2})"
        r"\s+(<DIR>|\d[\d\.]+)\s+(.+)"
    )
    results = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        m = line_re.match(line)
        if not m:
            continue
        date_str, _time_str, size_str, name = m.groups()
        if size_str == "<DIR>":
            continue  # skip directories
        # parse size (German: dots as thousand separators)
        size_bytes = int(size_str.replace(".", "").replace(",", ""))
        # parse date DD.MM.YYYY → YYYY-MM-DD
        dd, mm, yyyy = date_str.split(".")
        iso_date = f"{yyyy}-{mm}-{dd}"
        results.append({
            "filename": name.strip(),
            "size_bytes": size_bytes,
            "date": iso_date,
        })
    return results


def build_entry(idx: int, item: dict, source_path: str) -> SourceEntry:
    filename = item["filename"]
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    cluster, _score, suggestions = classify_cluster(filename, ext)
    priority, authority = assign_priority(filename)
    action = recommended_action(priority, cluster, ext)
    conf = confidence_from_priority(priority)
    cluster_label = CLUSTERS[cluster]["label"]

    # Derive a clean title
    title = filename
    # Strip leading date prefix 26_07_NN_
    title = re.sub(r"^26_\d{2}_\d{2}_?", "", title)
    # Strip extension
    title = re.sub(r"\.[a-zA-Z0-9]+$", "", title)
    # Replace underscores with spaces, clean brackets
    title = title.replace("_", " ").replace("[", "").replace("]", "")
    title = re.sub(r"\s+", " ", title).strip()
    if not title:
        title = filename

    # Deterministic pseudo-hash from filename + size
    hash_input = f"{filename}:{item['size_bytes']}:{item['date']}"
    pseudo_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16] + "..."

    # Auto-tags
    tags = [cluster, priority, authority, ext.lstrip(".") or "noext"]

    # Ingest note
    if action == "INGEST":
        note = "Ready for INGEST — extract key claims and update wiki."
    elif action == "ARCHIVE":
        note = "Archive candidate — skip or batch-review."
    elif action == "REVIEW":
        note = "Needs human review before ingest decision."
    else:
        note = ""

    return SourceEntry(
        id=f"REG-{idx:04d}",
        title=title,
        filename=filename,
        source=f"G:\\Meine Ablage\\00_WORKFLOW_PATTERN_REGISTRY\\{filename}",
        source_system="Google Drive",
        cluster=cluster,
        cluster_label=cluster_label,
        cluster_suggestions=suggestions,
        priority=priority,
        authority_class=authority,
        confidence=conf,
        file_size_bytes=item["size_bytes"],
        file_date=item["date"],
        file_ext=ext,
        status="PENDING_REVIEW",
        recommended_action=action,
        hash_sha256=pseudo_hash,
        ingest_note=note,
        tags=tags,
        indexed_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    )


def scan(dirlist_path: str, output_path: str) -> int:
    with open(dirlist_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    items = parse_dirlist(text)
    print(f"[scan] Parsed {len(items)} file entries from {dirlist_path}")

    entries = []
    for i, item in enumerate(items, start=1):
        entry = build_entry(i, item, dirlist_path)
        entries.append(entry)

    with open(output_path, "w", encoding="utf-8") as out:
        for entry in entries:
            d = asdict(entry)
            out.write(json.dumps(d, ensure_ascii=False) + "\n")

    print(f"[scan] Wrote {len(entries)} entries → {output_path}")

    # Summary by cluster
    from collections import Counter
    cluster_counts = Counter(e.cluster for e in entries)
    priority_counts = Counter(e.priority for e in entries)
    print("\n--- Cluster distribution ---")
    for c, n in sorted(cluster_counts.items()):
        print(f"  {c:30s}  {n:3d}")
    print("\n--- Priority distribution ---")
    for p, n in sorted(priority_counts.items()):
        print(f"  {p}  {n:3d}")

    return len(entries)


# ---------------------------------------------------------------------------
# Semantic suggest — query a registry for probabilistic cluster matches
# ---------------------------------------------------------------------------
def semantic_suggest(query: str, registry_path: str, top_k: int = 5) -> list[dict]:
    """
    Given a free-text query, score every registry entry by keyword overlap
    and return the top_k most relevant entries with a similarity score.
    """
    query_tokens = set(re.findall(r"\w+", query.lower()))
    results = []
    with open(registry_path, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            # Build token bag from title + filename + cluster + tags
            bag = set(re.findall(r"\w+", (
                entry.get("title", "") + " " +
                entry.get("filename", "") + " " +
                entry.get("cluster", "") + " " +
                " ".join(entry.get("tags", []))
            ).lower()))
            overlap = query_tokens & bag
            score = len(overlap) / (len(query_tokens) + 1e-9)
            if score > 0:
                results.append({
                    "id": entry["id"],
                    "title": entry["title"],
                    "cluster": entry["cluster"],
                    "priority": entry["priority"],
                    "score": round(score, 3),
                    "matched_tokens": sorted(overlap),
                })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    dirlist_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "wiki/source_registry.jsonl"

    if sys.argv[1] == "suggest" and len(sys.argv) >= 4:
        query = sys.argv[2]
        registry = sys.argv[3]
        top_k = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        hits = semantic_suggest(query, registry, top_k)
        for h in hits:
            print(json.dumps(h, ensure_ascii=False))
    else:
        scan(dirlist_path, output_path)
