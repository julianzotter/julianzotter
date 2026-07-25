# Wiki — Index
*Zuletzt aktualisiert: 2026-07-25*

Dieser Index ist der primäre Navigationspunkt für den LLM. Bei jeder Query zuerst lesen, dann in relevante Seiten einsteigen.

---

## Übersicht

| Seite | Kategorie | Confidence | Letzte Änderung |
|---|---|---|---|
| [overview.md](overview.md) | Synthese | MED | 2026-07-25 |
| [topics/llm-wiki-pattern.md](topics/llm-wiki-pattern.md) | Konzept | HIGH | 2026-07-25 |
| [source_registry.jsonl](source_registry.jsonl) | Quellen-Register | HIGH | 2026-07-25 |
| [approval-dashboard.html](approval-dashboard.html) | Infrastruktur | HIGH | 2026-07-25 |

---

## Kategorien

### Synthese
- **[overview.md](overview.md)** — Gesamtbild der Wissensbasis, evolvierende Thesis

### Konzepte
- **[topics/llm-wiki-pattern.md](topics/llm-wiki-pattern.md)** — Das LLM-Wiki-Muster (Karpathy), kritische Analyse, Implementierungsplan

### Entitäten
*(leer — wird bei Ingest befüllt)*

### Quellen-Register & Infrastruktur
- **[source_registry.jsonl](source_registry.jsonl)** — 145 Quelldateien aus Google Drive `00_WORKFLOW_PATTERN_REGISTRY`, mit Cluster/Priority/Authority, Approval-Status (PENDING_REVIEW by default). Maschinenlesbar (JSONL), Viewer: approval-dashboard.html
- **[approval-dashboard.html](approval-dashboard.html)** — Standalone Approval Dashboard. Öffne im Browser: Cluster-Tabs, Semantic Search, Approve/Reject/Revision-Buttons, localStorage-Persistenz, JSONL-Export

### Quellen-Summaries
*(wird bei Ingest befüllt)*

---

## Infrastruktur

| Skript | Zweck |
|---|---|
| `scripts/scan_dirlist.py` | Windows-DIRLIST.txt → source_registry.jsonl; Semantic Suggest (`python scripts/scan_dirlist.py suggest "EC2 formula" wiki/source_registry.jsonl`) |

---

## Statistik

- Seiten gesamt: 4
- Quellen im Register: 145
- Quellen verarbeitet: 1
- Quellen approved: 0 (Approval-Workflow läuft im Dashboard)
- Offene Widersprüche: 0
- Confidence LOW: 0
