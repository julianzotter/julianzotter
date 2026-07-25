---
title: LLM-Wiki-Muster (Karpathy)
confidence: HIGH
sources:
  - sources/processed/llm-wiki-karpathy-gist.md
last_updated: 2026-07-25
inbound_links:
  - overview.md
---

# LLM-Wiki-Muster

Das LLM-Wiki ist ein Muster für den Aufbau persistenter, kompoundierender Wissensbasen mit LLMs.
Entwickelt von Andrej Karpathy, beschrieben in `karpathy/llm-wiki.md` (GitHub Gist).

---

## Kernidee

**Nicht RAG, sondern Kompilierung.** Bei RAG wird Wissen bei jeder Abfrage neu aus Rohdokumenten
destilliert — keine Akkumulation. Im LLM-Wiki wird Wissen einmal extrahiert, strukturiert und
in einer persistenten Wiki-Dateistruktur gespeichert. Bei neuen Quellen wird das Wiki inkrementell
aktualisiert, nicht neu aufgebaut.

> "The wiki keeps getting richer with every source you add and every question you ask."

---

## Architektur

### Drei Schichten

1. **Raw Sources** — unveränderliche Originaldokumente (Artikel, PDFs, Bilder, Daten)
2. **Wiki** — LLM-generierte Markdown-Dateien (Zusammenfassungen, Entity-Seiten, Konzepte)
3. **Schema** — CLAUDE.md / AGENTS.md: Verhaltensregeln und Workflows für den LLM

### Zwei Hilfsdateien

- `index.md` — Inhaltskatalog: alle Seiten mit Link und Ein-Satz-Zusammenfassung
- `log.md` — Append-only Chronik: Ingests, Queries, Lint-Passes mit Datum

---

## Operationen

### Ingest
Neue Quelle → LLM liest, extrahiert, schreibt/aktualisiert 10–15 Wiki-Seiten, appended Log.

### Query
Frage → LLM liest index.md → liest relevante Seiten → Antwort mit Zitaten.
Gute Antworten werden als neue Wiki-Seiten gespeichert (Kompoundierung).

### Lint
Periodische Gesundheitsprüfung: Widersprüche, Orphans, fehlende Seiten, Datenlücken.

---

## Kritische Bewertung (ZotterConsult-Analyse)

### #1 Kommunikationslogik — 52%
- Stärke: Klare Rollentrennung Mensch/LLM, CLAUDE.md als Session-Protokoll
- Schwäche: Kein formelles Session-Übergabe-Protokoll, keine Multi-Agent-Kommunikation
- Google Drive: Kein Drive-Sync-Protokoll definiert
- Personal Memory: Sessions stateless ohne explizites Memory-System

### #2 COT-Workflows / Layer — 38%
- Stärke: Schicht-Architektur konzeptuell solide
- Schwäche: Keine COT-Templates pro Operation, kein Layer-Validierungsschritt
- Google Drive: Ingest-Workflow für Drive-Quellen nicht spezifiziert

### #3 Guardrails — 24% [KRITISCH]
- Stärke: Raw Sources immutabel, Schema-Dokument, Git-History
- Schwäche: Keine Halluzinations-Schranke, kein Widerspruchs-Gate, kein Rollback-Trigger
- Google Drive: Kein Read-Only-Constraint für LLM-Zugriff

### #4 Approval / Evidence-Check — 20% [KRITISCH]
- Stärke: Community-Erweiterungen (PRs, SHA-Zitierung, Human-Annotation-Tier)
- Schwäche: Im Kernmuster kein Approval-Gate, keine Evidence-Chain, kein Audit-Trail
- Google Drive: Drive-Vorschlags-Modus als Approval-Layer ungenutzt

### #5 Peer-Review-Quality-Layer — 15% [KRITISCH]
- Stärke: Lint-Operation vorhanden
- Schwäche: Lint = Self-Review durch denselben LLM (strukturelles Bias-Problem)
- Drive/Memory: Kein unabhängiger Review vor Memory-Write

---

## Implementierungsempfehlung (ZotterConsult)

Für produktiven Einsatz müssen vier Ergänzungen zum Kernmuster hinzugefügt werden:

1. **COT-Template pro Operation** in CLAUDE.md
2. **Adversarial Second-Pass** nach jedem Ingest (separater LLM-Call)
3. **Formelles Approval-Gate** via Git-PR mit Commit-Message-Standard
4. **Wöchentlicher Lint als PR**, nicht direkt in main

Siehe `CLAUDE.md` für die vollständige Implementierung dieser Regeln.

---

## Weiterführend

- [Vannevar Bush — Memex (1945)](https://en.wikipedia.org/wiki/Memex) — konzeptioneller Vorläufer
- Obsidian + Dataview + Marp als empfohlenes UI-Ökosystem
- qmd: lokale Suchmaschine für MD-Dateien mit BM25/Vektor-Hybrid (für Skalierung)
- gserdyuk/twotakt: Praxis-Implementation mit Document Passports und Corpus/Surface-Split
