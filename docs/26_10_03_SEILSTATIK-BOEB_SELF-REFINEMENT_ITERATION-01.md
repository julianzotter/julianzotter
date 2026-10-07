# SEILSTATIK BÖBLINGEN — SELF-REFINEMENT ITERATION 01: DENKARBEIT + DATENPIPELINE

`STAND: 2026-10-03 · AGENT: Claude Code (ID03, Selbstprüfung nach eigener Regel) · STATUS: DONE (nicht VERIFIED) · KLASSE: WORKFLOW/REVIEW`
`METHODE: Residuum r(0) extern gemessen (grep, Dateisystem, git, Schema-Validator), nicht geschätzt. Fixes nur dort, wo das Residuum eindeutig ist. r(1) nach Fix gemessen. Loop 1 von max. 5.`
`GEPRÜFTE ARTEFAKTE: docs/26_09_24_…Rev01.md · docs/26_09_29_…NEXUS-METHODE…md · …DREI-ORTE…md · …TODOS…md · …WORKORDER…md · …E2E-WORKFLOW…md · tools/01_scan_registry.py · tools/drive_inventory.py · ko/seilstatik_ko_pilot.jsonl · AI-WORKBENCH schemas/`

## 0 TL;DR

- Zehn Residuen gefunden, sechs behoben, vier bleiben offen mit Owner. Der schwerste Fehler war meiner: Ich hatte „Schritte 1–8 weitgehend erledigt" behauptet, ohne dass ein Artefakt für Ziele, Use Cases, Retrieval-Fragen, Informationsbedarf und Quellenanforderungen existierte. Verstoß gegen die eigene Regel CLAIM_NEEDS_LOCATOR. Jetzt behoben durch ein eigenes Dokument.
- Zweitschwerster Fehler: Rev01 nennt VORLAGE-002 als Kanon, drei spätere Dokumente VORLAGE-005. Behoben durch Errata-Block in Rev01.
- Pipeline-Hygiene: `__pycache__` war ins Repo committed, keine `.gitignore`, keine Tests, Pilot-KOs nur im flüchtigen Scratchpad. Alles behoben.
- Nicht behebbar ohne dich oder ohne Windows-PC: neun referenzierte Artefakte existieren noch nicht (geplante Outputs), Drive-Skript ist ungetestet gegen die echte API, ID05-Gegenlesen fehlt.

## 1 RESIDUUM r(0) — WAS DIE MESSUNG ERGAB

| # | Bereich | Befund | Evidenz (Locator) | Schwere |
|---|---|---|---|---|
| R1 | Denkarbeit | Schritte 1–5 der 20-Schritt-Liste (Main Goals, Use Cases, Retrieval Questions, Required Information, Source Requirements) in keinem Artefakt; Behauptung „1–8 weitgehend erledigt" (Chat 29.09.) unbelegt | `grep -ciE 'retrieval question' docs/*.md` → 0 in allen 7 Dateien | hoch |
| R2 | Denkarbeit | Widerspruch Kanon: Rev01 Z. 9–10, 20 „VORLAGE-002"; TODOS Z. 12 „VORLAGE-005 … nicht mehr VORLAGE-002" | grep VORLAGE-002 + kanon → 3 Treffer Rev01 | hoch |
| R3 | Denkarbeit | Fünf Nummerierungssysteme ohne Crosswalk: NEXUS P0–P9, Drei-Orte S1–S7/T1–T7, To-Dos V1–V8/G1–G8, WorkOrder A1–A9, E2E 1–59, dazu F1–F10 und 01-001…017 aus VORLAGE | Dateinamen und Kopfzeilen der 6 Docs | mittel |
| R4 | Denkarbeit | Rollenmodell unvollständig: ID05 Curator erst im Chat vom 03.10. eingeführt, in keinem Doc | grep ID05 docs/ → 0 (vor diesem Lauf) | mittel |
| R5 | Pipeline | Neun referenzierte Dateien existieren nicht: chunk.schema.json, make_source_kos.py, chunk_build.py, kg_project.py, merge_registry.py, 03_build_registry.py (nur Drive `_code`), transform_fit_v2.json, streckenmatrix_7pt.csv, sv_register_68.csv; Docs unterscheiden nicht zwischen vorhanden und geplant | `ls tools/ ai-workbench/tools/ ai-workbench/schemas/` | mittel |
| R6 | Pipeline | `tools/__pycache__/*.pyc` committed (Commit 144b003), keine `.gitignore` | `git ls-files tools` | niedrig, aber Hygiene |
| R7 | Pipeline | Keine Tests für `01_scan_registry.py` (nur ein manueller Lauf auf 10 Dateien); `drive_inventory.py` nur `py_compile`, nie gegen die API | tests/ existierte nicht | mittel |
| R8 | Pipeline | Pilot-KOs (SRC/RUN/WO) lagen nur im Session-Scratchpad, nicht im Repo | Pfad `/tmp/…/scratchpad/ko/` | mittel |
| R9 | Pipeline | `INFERENCE_MODE` und die sechs Reproduzierbarkeitsfelder (Modell-ID, effort, temperature/seed, Prompt-Hash, Tool-Hash, Pack-Version) nicht im Schema; RUN-KO kann sie nicht tragen | `'INFERENCE_MODE' in ontology_vocab.json` → False; RUN keyvalues ohne diese Felder | mittel |
| R10 | Messung selbst | Mein grep auf „unbelegte Behauptungen" lieferte 0 Treffer, weil die Ausschlussliste zu breit war. Der Test war wertlos. | Regex mit 15 Ausschlüssen | Methodik |

## 2 FIXES IN DIESER ITERATION

| # | Fix | Artefakt | Verifikation |
|---|---|---|---|
| R1 | Dokument Schritte 1–6 geschrieben: 5 Main Goals, 14 Use Cases, 19 Retrieval-Fragen mit Antwortform und Pflichtquelle, 10 Informationsklassen, Quellenanforderungen mit Autoritätsstufe, Golden Slice S19 | `docs/26_10_03_SEILSTATIK-BOEB_DENKARBEIT_ZIELE-USECASES-FRAGEN-QUELLEN_v1.0.md` | Datei vorhanden; Status CANDIDATE bis ID05/ID01 gegenlesen |
| R2 | Errata-Block in Rev01 vor §0: VORLAGE-005, U18/U19, ETA-Fassung, N6 geschlossen | Rev01 Kopf | `grep -c "ERRATA (2026-10-03" Rev01` → 1 |
| R3 | Crosswalk-Tabelle, siehe §3 unten | dieses Dokument | – |
| R4 | ID05 im Denkarbeit-Dokument als Owner von Schritt 1–5 eingetragen; Rollentabelle §4 | Denkarbeit v1.0 §7, hier §4 | – |
| R6 | `git rm --cached tools/__pycache__`, `.gitignore` mit `__pycache__/`, `*.pyc`, `*.jsonl.tmp`, `token.json`, `credentials.json` | `.gitignore` | `git ls-files tools` zeigt nur .py |
| R7 | Fünf unittest-Tests für Scanner: Ausschluss, SHA-256, Größenlimit, stabile ID, atomares Schreiben | `tests/test_scan_registry.py` | 5 Tests bestanden |
| R8 | Pilot-KOs ins Repo kopiert | `ko/seilstatik_ko_pilot.jsonl` | 3 Zeilen, Schema-valide (Validator-Lauf 03.10.) |

## 3 CROSSWALK DER NUMMERIERUNGEN (Fix R3)

| NEXUS-Phase | Drei-Orte | To-Dos | WorkOrder | E2E-Schritte | 20-Schritt-Liste (GPT) | Entscheidung/Anmerkung |
|---|---|---|---|---|---|---|
| P0 Scope | – | – | – | 1–5 | 1, 2, 3, 4, 5, 6 | WO-BOEB-000001 (noch anzulegen) |
| P1 Source Freeze | S1–S7 | – | A1–A3 | 6–10, 13, 18 | 7, 8, 12 | RUN1B |
| P2 Deterministisches Parsing | T1–T7 | V2 | A3 | 11 | 14 | – |
| P3 Semantisches Parsing / KOs | – | V1, V3 | A4, A5, A7, A8 | 14–17, 19–21 | 9, 10, 11, 13, 15 | ID02-Review |
| P4 Chunks + Index | – | – | – | (Drei-Orte §5) | 16, 18 | chunk.schema fehlt |
| P5 Knowledge Graph | – | – | – | (Drei-Orte §5) | 17 | kg_project.py fehlt |
| P6 Context Pack | – | – | – | (Drei-Orte §5) | – | Generator fehlt |
| P7 Workflows G1–G4 | G1-YAML | G1–G8, V4–V8 | A6 | 22–49 | 20 | F2, F3, F4, F6, F7 |
| P8 Delta-Loop | – | – | – | 43 | 19 | loop_max 5 |
| P9 Wissensupdate | – | – | A9 | 55–59 | – | Rev02 |

Regel ab jetzt: Neue Aufgaben bekommen nur noch die E2E-Nummer (1–59, fortlaufend) und werden im Crosswalk ergänzt. Keine sechste Nummerierung.

## 4 ROLLEN (Fix R4, verbindliche Fassung)

ID01 Engineer (J. Zotter: Freigaben, F1–F10) · ID02 Reviewer (separate Session, nur Artefakte) · ID03 Implementer (Claude Code Session A) · ID04 Registrar (Routine W1 + Skripte) · **ID05 Curator** (Ziele, Use Cases, Fragen, Ontologie, Metadatenschema; Schritte 1–5 und 9–13; darf keine Dateien anlegen und nicht rechnen) · Extern (Geometer, PFEIFER, Kneidinger, Prüfstatiker).

## 5 RESIDUUM r(1) — WAS OFFEN BLEIBT, MIT OWNER

| # | Offen | Warum nicht in dieser Iteration | Owner | Nächste Iteration |
|---|---|---|---|---|
| R5 | Neun geplante Artefakte existieren nicht | Sie sind Outputs der Phasen B–E; zwei davon (make_source_kos.py, chunk.schema.json) könnte ID03 jetzt bauen, die übrigen brauchen Daten vom Windows-PC (Hash-Scan) oder Entscheidungen | ID03 (2 Skripte), ID01 (Scan auf G:) | Iteration 02: make_source_kos.py aus Rev01+Errata erzeugen, chunk.schema.json in AI-WORKBENCH |
| R7b | `drive_inventory.py` ungetestet gegen die Drive-API | kein OAuth-Client in dieser Umgebung | ID01 (credentials.json) | Trockenlauf auf `_SEILSTATIK_BOEBLINGEN`, Soll: 41 Objekte Ebene 1 |
| R9 | INFERENCE_MODE + 6 Reproduzierbarkeitsfelder nicht im Schema | Schema liegt in AI-WORKBENCH (nur lesend angebunden); Änderung braucht deine Freigabe (Vokabular ist HUM-Sache) | ID01 freigeben, ID03 umsetzen | zusammen mit den drei Schema-Fixes vom 29.09. |
| R1b | Denkarbeit-Dokument nicht gegengelesen | ID05/ID01 | ID05 | Status CANDIDATE → VERIFIED nur mit Kürzel und Datum |
| R10 | Mein Claim-Test war wertlos | Regex zu permissiv; ein echter Test braucht eine Liste der Behauptungen mit Locator-Spalte | ID03 | Iteration 02: CoVe-Fragenkatalog für ID02 schreiben, Behauptungen als Tabelle, nicht per grep |

Stagnationskriterium: Wenn Iteration 02 keines der fünf Residuen schließt, HOLD an ID01.

## 6 WAS DIESE ITERATION ÜBER DIE METHODE GELERNT HAT

1. Das größte Residuum lag nicht in der Pipeline, sondern in der Denkarbeit: Ich habe Schritte als erledigt deklariert, weil sie implizit in Dokumenten „mitgedacht" waren. Implizit ist nicht belegbar. Ab jetzt gilt: Jeder der 20 Schritte hat genau eine Datei als Beleg oder gilt als offen.
2. Grep ist kein Reviewer. Den Claim-Test hätte ID02 mit einer Fragenliste machen müssen. Die Rollentrennung ist auch für die Selbstprüfung die Konvergenzbedingung.
3. Pipeline-Hygiene (gitignore, Tests, Persistenz) kostet Minuten und wurde trotzdem übersprungen, weil der Fokus auf Inhalt lag. Deshalb gehört sie als fester Schritt vor jeden Commit in die E2E-Liste (neuer Schritt 60: „Tests laufen, kein Build-Artefakt im Commit, Artefakt-Ledger vorhanden/geplant aktualisiert").
