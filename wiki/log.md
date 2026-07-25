# Log — Chronik der Wiki-Operationen
*Append-only. Niemals löschen oder editieren. Neue Einträge immer oben.*

Format: `## [DATUM] typ | titel`  
Typen: `ingest` | `query` | `lint` | `conflict` | `schema-update`

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
