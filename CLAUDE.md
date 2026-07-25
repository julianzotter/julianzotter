# LLM-Wiki — Schema & Guardrails
**Repo:** julianzotter/julianzotter  
**Stand:** 2026-07-25  
**Zweck:** Persistente, kompoundierende Wissensbasis für ZotterConsult

---

## Architektur

```
wiki/          ← LLM schreibt, Mensch liest
  index.md     ← Katalog aller Seiten (aktuell halten bei jedem Ingest)
  log.md       ← Append-only Chronik
  overview.md  ← Synthese-Seite
  topics/      ← Entity- und Themen-Seiten

sources/       ← LLM liest, NIEMALS schreibt
  inbox/       ← Drop-Zone für neue Quellen
  processed/   ← Nach Ingest verschobene Quellen
```

---

## GUARDRAILS — Nicht verhandelbar

1. **Raw Sources sind unveränderlich.** Kein Schreibzugriff auf `sources/`. Niemals.
2. **Jede Wiki-Behauptung braucht eine Quelle.** Format: `[Claim] (Quelle: dateiname, Abschnitt)`
3. **Confidence-Level ist Pflicht.** Jede Seite enthält im Frontmatter: `confidence: LOW|MED|HIGH`
4. **Widersprüche werden geloggt, nicht still überschrieben.** Bei Konflikt mit bestehender Aussage: Eintrag in `log.md` mit `[CONFLICT]`-Tag, beide Versionen dokumentieren, Mensch entscheidet.
5. **Kein Wiki-Update ohne Log-Eintrag.** Jede Änderung an `wiki/` → `log.md`-Zeile.

---

## Operationen

### INGEST — Neue Quelle verarbeiten

**Ablauf (COT-Template):**

1. Quelle in `sources/inbox/` lesen
2. Key-Takeaways in 3–7 Punkten extrahieren
3. `wiki/index.md` prüfen: Welche Seiten sind betroffen?
4. Bestehende betroffene Seiten lesen
5. Widersprüche zur aktuellen Datei identifizieren und `[CONFLICT]` loggen
6. Draft-Seite(n) schreiben oder bestehende Seiten aktualisieren
7. `wiki/index.md` updaten
8. Log-Eintrag appenden: `## [DATUM] ingest | Quelltitel`
9. Quelle nach `sources/processed/` verschieben (nicht löschen)
10. **STOP — Mensch reviewed Draft, bevor Merge**

### QUERY — Frage beantworten

1. `wiki/index.md` lesen → relevante Seiten identifizieren
2. Relevante Seiten lesen
3. Antwort mit Seitenreferenzen formulieren
4. Optional: Antwort als neue Wiki-Seite speichern, wenn sie Synthesewert hat
5. Log-Eintrag: `## [DATUM] query | Fragetext`

### LINT — Gesundheits-Check

1. Auf Widersprüche zwischen Seiten prüfen
2. Orphan-Seiten identifizieren (keine eingehenden Links)
3. Confidence LOW-Seiten markieren, die Verifikation benötigen
4. Fehlende Seiten für oft referenzierte Konzepte vorschlagen
5. Log-Eintrag: `## [DATUM] lint | Findings-Zusammenfassung`
6. **WICHTIG:** Lint wird als separater PR geöffnet, nicht direkt in main

---

## Approval-Workflow

Alle Wiki-Writes via Git-Commit. Commit-Message enthält:
```
wiki(ingest): <Quelltitel>

Quelle: sources/processed/<datei>
Confidence: MED
Betroffene Seiten: <liste>
Widersprüche: keine | <beschreibung>
```

Wöchentlicher Lint-Pass → eigener PR, nicht direkt commited.

---

## Frontmatter-Standard

Jede Wiki-Seite beginnt mit:

```yaml
---
title: <Seitentitel>
confidence: LOW|MED|HIGH
sources:
  - sources/processed/<dateiname>
last_updated: YYYY-MM-DD
inbound_links: []
---
```

---

## Google Drive Integration

- Drive-Ordner `llm-wiki/sources/` → Quelle der Wahrheit
- Neue Drive-Dokumente → lokal in `sources/inbox/` ablegen
- Drive-Zugriff: Read-Only für LLM-Operationen
- Drive-File-ID im Log-Eintrag festhalten für Rückverfolgbarkeit
- Bei Drive-Dokument-Update: neuer Ingest-Lauf mit Diff-Fokus

---

## Peer-Review

Alle substantiellen Wiki-Updates benötigen einen Adversarial-Check:

```
Adversarial Prompt: "Lies diese Wiki-Seite und liste konkret,
wo sie falsch, unvollständig oder nicht durch die zitierten
Quellen gedeckt sein könnte. Sei maximal kritisch."
```

Erst nach Adversarial-Check → Mensch-Review → Commit.
