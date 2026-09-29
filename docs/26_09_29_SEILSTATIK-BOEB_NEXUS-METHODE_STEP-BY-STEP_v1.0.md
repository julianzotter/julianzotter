# SEILSTATIK BÖBLINGEN × NEXUS-METHODE — STEP-BY-STEP-IMPLEMENTIERUNG v1.0

`STAND: 2026-09-29 · AGENT: Claude Code (ID03-Rolle, Entwurf) · STATUS: DONE (nicht VERIFIED) · KLASSE: WORKFLOW`
`BEZUG: docs/26_09_24_SEILNETZ-BOEB_QUELLENVERZEICHNIS_LETZTGUELTIG_Rev01.md (U1–U17, F1–F7) · AI-WORKBENCH schemas/knowledge_object.schema.json + ontology_vocab.json + tools/mcp_nexus_server.py (Branch claude/zealous-johnson-woguqi)`

## 0 TL;DR

- **Richtig**: SSOT → Registry mit ID + Hash → deterministisches Parsing → semantisches Parsing → KOs/Key-Values → Chunks/Index → Knowledge Graph → Projektkontext → Workflows je Main Goal → CoT/CoVe → gebundener Delta-Loop → Beobachtung zurück als CANDIDATE.
- **Drei Korrekturen**: (1) Das Residuum des Delta-Loops muss von einem **externen Orakel** kommen (Solver, Golden Case, Schema, unabhängige Kontrollrechnung), nie vom LLM selbst. (2) Der „Sparse-Solver"-Vergleich gilt nur, wenn **Operator (ID03) und Residuum (ID02) getrennt** sind und die Iteration **hart begrenzt** ist (loop_count ≤ 5, Stagnation → HUM). (3) Embedding ist nicht der erste Schritt: bei ~50 Primärdokumenten reicht BM25 + Registry (Stufe S), Vektor-DB erst ab Stufe M.
- **Böblingen-spezifisch**: Der deterministische Solver ist RFEM 5.29 + Python-Kontrollen. Der Golden Case existiert bereits (Reproduktion Anhang 25: Δ < 0,02 mm / 0,001 kN). Das Residuum ist damit messbar.

## 1 IST DIE METHODE RICHTIG? — PRÜFUNG DER ZEHN BAUSTEINE

| # | Baustein (deine Formulierung) | Bewertung | Korrektur / Präzisierung |
|---|---|---|---|
| 1 | SSOT anlegen, Quellen suchen, registrieren, ID | RICHTIG | Registry = Autorität, alles andere Projektion. Hash vor ID. Böblingen: U1–U17 sind identifiziert, Hashes fehlen für 9 von 17. |
| 2 | Parsing-Routinen | RICHTIG, Reihenfolge fehlt | **Deterministisch vor semantisch**: PDF-Tabellen, RFEM-Exporte, XLSX zuerst mit Code (pdfplumber, openpyxl, CSV). LLM erst danach, nur auf Text ohne Tabellenstruktur. |
| 3 | Semantisches Parsing → Key-Values | RICHTIG, mit Gate | LLM-Extraktion liefert **nur CANDIDATE** (Schema erzwingt das über `extraction_method: llm_proposed`). VERIFIED nur durch ID02 + Locator. |
| 4 | Knowledge Chunks = Embedding | TEILWEISE | Chunk ist die **Retrieval-Einheit** (Text + source_id + locator + hash), kein KO und kein Embedding. Embedding ist eine optionale Indexform des Chunks. Stufe S: BM25 (`tools/index_build.py`). |
| 5 | Knowledge Graph | RICHTIG | Kanten nur aus `relations` verifizierter KOs (kg_edge.schema). Konflikte als `CONTRADICTS`-Kante mit Evidenz, nicht als Textnotiz. Böblingen hat 4 solche Konflikte (F2, F3, F6, F4). |
| 6 | Signale / Domains / Metadatenmodell | RICHTIG | Vokabular ist geschlossen (ontology_vocab.json). `DOMAIN=SEILSTATIK` existiert. Keine freien Tags. |
| 7 | Projektkontext generieren | RICHTIG, Größe fehlt | Context Pack ≤ 1,2 k Token (MVC lt. AI-WORKBENCH README), **nur aus VERIFIED-KOs**, versioniert + gehasht. Agenten bekommen das Pack, nie Roh-Chunks. |
| 8 | Main Goals → Workflows → schlanke CoT-Pipelines | RICHTIG | Ein Workflow je Goal, jeder Schritt = Gate aus `GATE`-Vokabular. CoT nur innerhalb eines Gates, nie über Gates hinweg. |
| 9 | CoVe, Self-Refine, Peer Review, Plausibility | RICHTIG mit Einschränkung | **CoVe**: ID02 leitet Prüffragen aus der WorkOrder ab und beantwortet sie gegen Solver-Output, nicht gegen ID03-Text (Dhuliawala et al. 2023). **Self-Refine** nur für Form (Berichtstext), nie für Zahlen: LLMs korrigieren eigene Rechenfehler ohne externes Signal nicht zuverlässig (Huang et al. 2023, arXiv 2310.01798). |
| 10 | Iteratives Delta-Refinement wie Sparse Iterative Solver | ANALOGIE HÄLT NUR MIT 3 BEDINGUNGEN | (a) Residuum r = ‖Output − Referenz‖ mit **externer** Referenz; (b) Operator ≠ Residuum-Berechner (ID03 ≠ ID02); (c) Abbruch: Toleranz erreicht ODER loop_count = 5 ODER r sinkt nicht mehr → HUM. Ohne (a) ist es keine Iteration, sondern Drift. Muster entspricht „Evaluator-Optimizer" (Anthropic, Building effective agents, 2024). |

**Fazit**: Die Kette stimmt. Der Fehler, der in der Praxis passiert, ist immer derselbe: Das Delta wird vom selben Modell geschätzt, das den Output erzeugt hat. Deshalb ist die Rollentrennung ID02/ID03 keine Organisationsfrage, sondern die Konvergenzbedingung.

## 2 ROLLEN (unveränderlich)

| Rolle | Wer | Darf | Darf nicht |
|---|---|---|---|
| **ID01 Engineer (HUM)** | J. Zotter | WorkOrder freigeben, F1–F7 entscheiden, ENGINEER_APPROVED setzen, Vokabular ändern | – |
| **ID02 Reviewer** | eigene Claude-Session B (oder DeepSeek/GPT), erhält **nur Artefakte + Registry**, nicht den Chat von ID03 | CoVe-Fragen, unabhängige Kontrollrechnung, Schema-Validierung, Verdikt PASS/HOLD/FAIL | Dateien von ID03 editieren, Solver-Code ändern, Vorschläge in Registry schreiben |
| **ID03 Implementer** | Claude Code Session A | Parsing-Skripte, Solver-Anbindung (RFEM COM, Python), Tests, RUN-Objekte, ko_propose | Eigenen Output als VERIFIED markieren, Review-Verdikt setzen |
| **ID04 Registrar** | Routine W1 (Drive-Indexer) + Hash-Skript | Hashes, Index, Registry-Zeilen mit Status FOUND/REGISTERED | Status > REGISTERED vergeben |

Übergabe ausschließlich über Dateien mit Hash (JSONL/CSV/MD). ID02 bekommt den `run_id` und holt sich die Artefakte selbst. Kein gemeinsamer Chat.

## 3 STEP-BY-STEP (P0–P9)

Jede Phase: Input → Aktion → Output → Gate → Abnahmekriterium. Werkzeuge sind vorhandene Dateien; „neu" = noch zu schreiben.

### P0 Scope → formale WorkOrder (Gate CAPTURE → CLARIFY → READBACK → SCOPE_CONFIRMED)
- Input: Anfrage 06.03.2026 (U7a), Angebot final 12 000 € (U7b), Bereich RL06/RL11–A14/C21 (U7c).
- Aktion (ID03): WorkOrder-KO `WO-BOEB-000001` schreiben: intent, scope, agent, budget_tokens, gate. Readback als 5 Sätze an ID01.
- Output: `ko/WO-BOEB-000001.json` (schemavalide).
- Gate: ID01 bestätigt Readback (SCOPE_CONFIRMED).
- Kriterium: Scope nennt explizit, was **nicht** geschuldet ist (Ankerbemessung, Prüfstatik, Vermessung).

### P1 Source Freeze / SSOT (Gate RETRIEVE, Teil 1)
- Input: Quellenverzeichnis Rev01 §1 (U1–U17), lokaler Ordner `G:\Meine Ablage\26-03-18_Boeb_Adaptierung`.
- Aktion (ID04/ID03): Hash-Skript (neu, ~40 Zeilen: walk → sha256 → JSONL) auf dem Windows-PC laufen lassen, weil die .rf5 und die Sandbox nur lokal liegen. Für jede Unterlage genau **ein** kanonischer Pfad. Drive-ID ergänzen.
- Output: `00_SOURCE_REGISTRY_BOEB.jsonl` (17 SOURCE-KOs `SRC-BOEB-0000xx`, Status REGISTERED), `DATA_FREEZE_MANIFEST_26_001_v2.jsonl` ohne PENDING-Zeilen.
- Gate: RUN1B = PASS.
- Kriterium: 17/17 mit sha256, Datum, Autorität (A0–A5); kein Objekt mit zwei Pfaden; 13bb_ausführungsstatik_1 (zwei byteverschiedene Dateien) als zwei SOURCE mit `DUPLICATE_OF`-Kante und Entscheidung, welche kanonisch ist.

### P2 Deterministisches Parsing (kein LLM)
- Input: U1 (PDF Text), U3/U15/U12a (RFEM-Ausdrucke), U8 (XLSX Vermessung), U9 (K15 PDF-Tabelle), U9c (Bestandsaufnahme XLSX), U4 Anhang 27/30.
- Aktion (ID03): je Quelle ein Parser-Skript (pdfplumber / openpyxl / regex auf RFEM-Textexport). Jede Tabellenzeile bekommt `source_id`, `locator` (Seite/Blatt/Zeile), `row_hash`.
- Output: `tables/LF_LK_2015.csv`, `tables/LF_LK_2026.csv`, `tables/vermessung_2026.csv`, `tables/pfeifer_K15.csv`, `tables/bestandsaufnahme.csv`, `tables/anhang27_laengen.csv`, `tables/anhang30_anker.csv`.
- Gate: VALIDATE (ID02 stichprobt 10 % der Zeilen gegen PDF).
- Kriterium: 0 Zeilen ohne Locator; Summen-/Zählkontrollen (68 Seile, 21 LK, 11 Vermessungspunkte, 21 PFEIFER-Zeilen S01–S21).

### P3 Semantisches Parsing → CANDIDATE-KOs
- Input: P2-Tabellen + Fließtext U1/U2/U5.
- Aktion (ID03 via `ko_propose`): LLM schlägt vor: CLAUSE (Prüfauflage Schnee 0,60 kN PB03; LK220 Erg. 2; Beiwerte LK100 Erg. 2 Pkt. 02-005), MATERIAL (PE5: d, A, E, Z_Bk, F_Rd), COMPONENT (68 Seile als CABLE_RECORD: Sxx ↔ Member ↔ Knoten ↔ Lsys ↔ Sv), FORMULA (Lsys = L(LK100) − Beschlag; Transformation U8e), SOLVER (RFEM 5.29 COM-Pipeline, Python-Längenkette), GOLDEN_CASE (Anh. 25 Reproduktion), WORKORDER (F1–F7).
- Output: `ko_proposals.jsonl` (alle Status CANDIDATE, `extraction_method: llm_proposed`, Locator Pflicht).
- Gate: REVIEW durch ID02 → VERIFIED (verified_by, verified_at) oder QUARANTINE.
- Kriterium: Annahmequote und Korrekturbedarf werden gemessen (Ziel Pilot: 10 Vorschläge, ≥ 7 ohne Korrektur). Ziel Vollausbau Böblingen: ~25 KOs.

### P4 Chunks + Index (Stufe S)
- Input: Volltexte U1, U2, U5, VORLAGE-002, Kurzbericht; P2-Tabellen.
- Aktion (ID03): `chunk.schema.json` definieren (neu, minimal: chunk_id, source_id, locator, text, sha256, token_count, ko_refs[]). Chunking nach Abschnitt/Tabelle, nicht nach Zeichenzahl. Index mit `tools/index_build.py` (BM25).
- Output: `chunks.jsonl`, BM25-Index.
- Gate: keines (technisch), aber Chunks ohne source_id werden verworfen.
- Kriterium: `index_search("LK220")` liefert Erg. 2 in Top-3; `index_search("Beschlagmaß Leuchte Anker")` liefert Kurzbericht §5. Vektor-DB erst, wenn BM25-Recall bei 20 Testfragen < 80 %.

### P5 Knowledge Graph
- Input: VERIFIED-KOs aus P3.
- Aktion (ID03): kg_node/kg_edge aus `relations` generieren (Projektion, kein Handedit). Konflikte als `CONTRADICTS` mit `evidence_locator`: G3-XY vs VAR-A-XY (F2), EA 3 420 vs 4 940 (F6), Bestand 2015 vs Rückbauplan 2022 (F4), LK220 fehlt (F3). Widerlegte Aussagen (Sperrliste §6 Rev01) als Knoten Status UEBERHOLT mit `SUPERSEDES`-Kante.
- Output: `artifacts.jsonl`, `edges.jsonl`.
- Gate: VALIDATE (Schema).
- Kriterium: jeder `CONTRADICTS` hat eine offene WorkOrder; keine Kante ohne Evidenz; Graph ist aus KOs vollständig regenerierbar (löschen + neu bauen = identisch).

### P6 Projektkontext (Context Pack)
- Input: VERIFIED-KOs, offene WorkOrders, Sperrliste.
- Aktion (ID03): Generator (neu) erzeugt `CONTEXT_PACK_BOEB_vN.md`: Scope (3 Zeilen), kanonische Quellen (Tabelle U1–U17 mit Hash-Präfix), Kernzahlen mit Einheit (PE5, F_Rd 27,9 kN, LK100-Definition, Beschlagmaße), offene Entscheidungen F1–F7, Sperrliste (Kurzform), Zeiger auf Index. ≤ 1,2 k Token. Hash + Version.
- Output: Context Pack vN.
- Gate: ID01 liest gegen (READBACK), einmalig je Version.
- Kriterium: Ein Agent, der nur das Pack sieht, kann die drei Blocker (F2, F3, F6) benennen. Alles andere holt er über `index_search` / `ko_get`.

### P7 Workflows je Main Goal (CoT + CoVe)
Main Goals Böblingen: **G1** Bestelllängen S19/S22 (+ S81 prüfen) · **G2** Nachweise ULS/SLS Bereich RL06–C21 · **G3** Ankerkräfte 105/106/113/114/3006/3007/3021 als Schnittstelle · **G4** Prüfbericht VORLAGE-003.

Pipeline je Goal (Gates aus Vokabular):
1. RETRIEVE (ID03): Context Pack + `index_search` + `ko_get` → Input-Register mit KO-IDs.
2. VALIDATE (ID03): Inputs gegen Schema; jeder Zahlenwert hat KO-ID + Einheit; Einheiten-Check.
3. SOLVE (deterministisch): RFEM 5.29 via COM (Sandbox-Kopie, Bestand read-only) oder Python (Transformation, Längenkette Lsys→LA→LAG2→LB→Lo2k, Kettenlinie). Output = RUN-KO mit input_hash, solver_ko, Ergebnis-CSV.
4. INDEPENDENT_CHECK (ID02, andere Session): CoVe-Fragen aus der WorkOrder (Beispiel G1: „Welche Beschlagmaß-Annahme? Welche Trafo? Welcher Lastfall definiert L? Stimmt Δ zu Anhang 27 im Bestand?") → Antworten nur aus RUN-Artefakten. Kontrollrechnungen: Kettenlinie H·f = q·L²/8 (± 5 %), transformationsfreie Streckenkontrolle 7101/7102 ↔ A05/A06, ΣV = 0 / ΣM = 0 an Lagern, Plausibilität η ≤ 1.
5. REVIEW (ID02): Verdikt PASS / HOLD / FAIL + Residuumsliste.
6. ENGINEER_APPROVED (ID01).
7. EXPORT: erst jetzt Bestellblatt PFEIFER / Berichtskapitel. Kein Export-Tool vor diesem Gate.

CoT bleibt innerhalb eines Schritts (z. B. Herleitung Beschlagmaß), niemals als freie Kette über SOLVE hinweg.

### P8 Delta-Refinement (gebunden)
- Residuum definieren **vor** dem ersten Lauf, je Goal, als Vektor mit Toleranzen:
  - G1: |Lsys − Lsys_ref| ≤ 5 mm (Referenz: unabhängige Sehnenrechnung + Beschlag), Beschlagmaß bestätigt (bool)
  - G2: Δu ≤ 2 mm, ΔN ≤ 0,01 kN gegen Golden Case Anh. 25 (Bestandsmodell); η ≤ 1 (VAR-A)
  - G3: Gleichgewicht ΣF ≤ 0,01 kN je Richtung; Vorzeichen je LK dokumentiert
  - G4: Schema-Validität aller zitierten KOs = 100 %, alle CoVe-Fragen PASS
- Iteration: ID03 erzeugt Output v(k) → ID02 berechnet r(k) → wenn r(k) > tol: ID03 bekommt **nur r(k)** (nicht die Lösung), destilliert Kontext/Prompt neu (Pack v(k+1), Diff protokolliert) → nächster Lauf.
- Abbruch: r ≤ tol (konvergiert) ODER loop_count = 5 (Schema-Maximum) ODER r(k) ≥ r(k−1) (Stagnation) → HOLD an ID01. Keine sechste Runde.
- Self-Refine nur auf Berichtstext (G4), nie auf Zahlen.
- Alles landet als RUN-KO (run_id, input_hash, loop_count, stop_reason, tokens).

### P9 Beobachtung → Wissensupdate
- Jedes Ergebnis (neue Längen, Ankerkräfte, bestätigtes Beschlagmaß, Geometer-Antwort) geht als CANDIDATE-KO zurück (P3), nie direkt in VERIFIED.
- Neuer GOLDEN_CASE nach Freigabe: VAR-A LK100 mit Toleranz 0,5 % als Regressionsreferenz für spätere Läufe (LK220-Ergänzung, F2-Variante B).
- Context Pack v(N+1) wird regeneriert, nicht editiert.

## 4 WAS DAVON SCHON EXISTIERT (Böblingen, Stand 29.09.)

| Phase | Vorhanden | Fehlt |
|---|---|---|
| P0 | Anfrage, Angebot, Bereichsabgrenzung | WO-KO formal |
| P1 | U1–U17 identifiziert, 8 Hashes (VORLAGE-002) | 9 Hashes, Manifest v2, Kanonik 13bb-Dublette |
| P2 | K15-Tabelle (Quellenbefund §8), LF/LK 2026 (BEFUND V01) | Parser-Skripte reproduzierbar, Anh. 27/30 als CSV |
| P3 | 3 Pilot-KOs (SRC/RUN/WO, validiert) | ~22 weitere, ID02-Review |
| P4 | `index_build.py`, `index_search.py` in AI-WORKBENCH | chunk.schema, Böblingen-Index |
| P5 | kg_node/kg_edge-Schemas | Böblingen-Graph |
| P6 | Quellenverzeichnis Rev01 (zu lang für ein Pack) | Generator, Pack v1 |
| P7 | RFEM-Sandbox 23.09., VAR-A gerechnet, Prüfanmerkungen 01-001…017 | Pipeline als Datei, CoVe-Fragenkatalog |
| P8 | Golden Case Bestand (Δ < 0,02 mm / 0,001 kN) | Residuumsdefinition je Goal, Loop-Protokoll |
| P9 | – | – |

## 5 ERSTE FÜNF AKTIONEN (diese Woche)

1. **ID01**: F2, F3, F6 entscheiden (ohne F2 ist G1 nicht lösbar).
2. **ID03**: Hash-Skript + Manifest v2 (P1) → J. Zotter führt es lokal aus, Ergebnis nach Drive `SEILNETZ-DOCU`.
3. **ID03**: Schema-Fixes in AI-WORKBENCH (Platzhalter-Hash sperren, SOURCE ohne source_ids erlauben, Pflichtfelder SOURCE/MODEL/COLLECTION) + `chunk.schema.json`.
4. **ID03**: 25 Böblingen-KOs als `ko_proposals.jsonl` → **ID02 (separate Session)** reviewt, misst Annahmequote.
5. **ID03**: Context Pack v1 + G1-Pipeline als Trockenlauf auf den vorhandenen VAR-A-Ergebnissen; ID02 rechnet S19/S22-Sehnen transformationsfrei nach. Ergebnis = erstes Residuum r(0).

## 6 QUELLEN

- Madaan et al. (2023): Self-Refine. arXiv:2303.17651 — Iteration mit Selbstfeedback; Gewinn nur bei Aufgaben mit prüfbarem Feedback.
- Dhuliawala et al. (2023): Chain-of-Verification Reduces Hallucination. arXiv:2309.11495 — Prüffragen getrennt vom Erstentwurf beantworten.
- Huang et al. (2023): Large Language Models Cannot Self-Correct Reasoning Yet. arXiv:2310.01798 — ohne externes Orakel keine Verbesserung, teils Verschlechterung.
- Shinn et al. (2023): Reflexion. arXiv:2303.11366 — verbaler Speicher über Iterationen, funktioniert mit externem Signal (Tests).
- Anthropic (2024): Building effective agents — Evaluator-Optimizer-Muster, klare Abbruchkriterien.
- AI-WORKBENCH: `docs/02-KNOWLEDGE-GRAPH/KO-SCHEMA+MCP-TOOLS_NEXUS-Meta-Architektur.md`, `schemas/*.json`, `tools/mcp_nexus_server.py`.
- Dieses Repo: `docs/26_09_24_SEILNETZ-BOEB_QUELLENVERZEICHNIS_LETZTGUELTIG_Rev01.md`.
