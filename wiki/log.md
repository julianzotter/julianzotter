# Log — Chronik der Wiki-Operationen
*Append-only. Niemals löschen oder editieren. Neue Einträge immer oben.*

Format: `## [DATUM] typ | titel`  
Typen: `ingest` | `query` | `lint` | `conflict` | `schema-update`

---

## [2026-07-25] schema-update | SCAN ROUTINE + APPROVAL LAYER implementiert

**Typ:** Infrastruktur-Update (kein neuer Ingest)  
**Confidence:** HIGH

**Änderungen:**
1. `scripts/scan_dirlist.py` — Windows-DIRLIST-Parser mit Auto-Clustering (10 Cluster), Priority (P0–PX), Authority Class (A–E), Semantic Suggest
2. `wiki/source_registry.jsonl` — 145 Einträge aus Google Drive `00_WORKFLOW_PATTERN_REGISTRY`, auto-generiert via scan_dirlist.py
3. `wiki/approval-dashboard.html` — Standalone HTML Dashboard (kein CDN), embeds registry JSON, localStorage-Approval-Workflow, Cluster-Tabs, Semantic Search, JSONL-Export

**Registry-Verteilung:**
- engineering-ec2: 35 | llm-engineering: 19 | knowledge-management: 17 | registry-index: 16
- ai-os-dashboards: 26 | workflow-automation: 7 | images-visuals: 11 | bookmarks-links: 6
- tools-code: 4 | zotterconsult-projects: 4

**Priority-Verteilung:** P0: 11 | P1: 5 | P2: 27 | P3: 72 | P4: 10 | PX: 20

**Betroffene Seiten:** wiki/index.md (Statistik aktualisiert)  
**Widersprüche:** keine

---

## [2026-07-25] ingest | karpathy/llm-wiki.md (Gist: julianzotter/a4a1fe466edbb08e2bede1cb99ebe264)

**Quelle:** Gist — julianzotter/llm-wiki.md (fork von karpathy/llm-wiki.md)  
**Typ:** Konzept-Dokument, Muster-Beschreibung  
**Confidence:** HIGH (Original-Autor: Andrej Karpathy)

**Key Takeaways:**
1. LLM-Wiki als persistente, kompoundierende Wissensbasis vs. RAG (einmalig, nicht akkumulierend)
2. Drei Schichten: Raw Sources (immutabel) → Wiki (LLM-generiert) → Schema (CLAUDE.md)
3. Drei Operationen: Ingest, Query, Lint
4. index.md (Katalog) + log.md (Chronik) als Navigationshilfen
5. Obsidian als UI-Layer empfohlen; qmd für Suche bei Skalierung

**Kritische Analyse (5 Kriterien):**
- #1 Kommunikationslogik: 52% — informell, kein Session-Übergabe-Protokoll
- #2 COT-Workflows: 38% — Operationen beschrieben, nicht strukturiert
- #3 Guardrails: 24% — nur Raw-Source-Immutabilität als harte Grenze
- #4 Approval/Evidence: 20% — kein Approval-Gate im Kernmuster
- #5 Peer-Review: 15% — Lint = Self-Review, kein unabhängiger Check

**Betroffene Seiten erstellt:**
- `wiki/topics/llm-wiki-pattern.md` (neu)
- `wiki/overview.md` (neu)
- `wiki/index.md` (aktualisiert)

**Widersprüche:** keine (erste Ingestion)
