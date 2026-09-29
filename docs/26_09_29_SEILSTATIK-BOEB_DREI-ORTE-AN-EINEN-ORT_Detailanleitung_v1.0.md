# SEILSTATIK BÖBLINGEN — DREI ORTE AN EINEN ORT: DETAILANLEITUNG v1.0

`STAND: 2026-09-29 · AGENT: Claude Code (ID03) · STATUS: DONE (nicht VERIFIED) · KLASSE: WORKFLOW`
`ERGÄNZT: 26_09_29_SEILSTATIK-BOEB_NEXUS-METHODE_STEP-BY-STEP_v1.0.md (P0–P9). Dieses Dokument konkretisiert P1–P7 auf reale Pfade, Drive-IDs, Skripte.`
`GEPRÜFT: Drive-Ordner LLM-LOCAL-SSOT, AI-PYTHON-PARSE, 21_PYTHON_PARSER, ENGINEERING_PARSER(_V2); AI-WORKBENCH Branch claude/zealous-johnson-woguqi; Wegweiser Normen/Parser 29.09.; Status-Quick-Task-Matrix 28.09.`

## 0 TL;DR

- **Die drei Orte**: (A) Projektdaten `26-03-18_Boeb_Adaptierung` + `_SEILSTATIK_BOEBLINGEN` · (B) Normen im Original unter `ZT-Gesellschaft\24_NORMEN\EUROCODE\` plus Parser unter `AI-PYTHON-PARSE\` · (C) Codebase = AI-WORKBENCH (Schemas, Index, MCP) + Drive `_code`/`_registry` (Parser, Register, Konventionen).
- **Der eine Ort** = `G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\` (Drive 1j3FLJkWpQv6xGA_KO0D9sMyA11f0vxBV). Dort entsteht `PROJECTS\26_001_BOEBLINGEN\` mit sechs Unterordnern. Große Binärdateien (.rf5, DXF, ZIP) werden **nicht kopiert**, nur registriert (Pfad + SHA-256 + Drive-ID).
- **Reihenfolge**: Registry (Hash) → deterministische Tabellen → CANDIDATE-KOs → Chunks + BM25 → Graph → Context Pack → Workflow G1. Kein Schritt vor dem vorherigen Gate.
- **Zwei Blocker vorab**: (1) Projekt liegt in Deutschland, der Normenbestand ist österreichisch (ÖNORM B). DIN-NA-Fassungen von EN 1990/1991/1993-1-11 müssen über den Wegweiser-Pfad gesucht werden, sonst `MISSING`. (2) `01_scan_registry.py` existiert nicht, `02_parse`/`03_build_registry` sind auf `G:\` noch nicht deployt (E2E-02/03 lt. Status-Matrix). Ohne Scan kein Hash, ohne Hash keine Registry.

## 1 DIE DREI ORTE — WAS GENAU WO LIEGT

### A Projektdaten (Statik)

| Was | Wo | ID / Pfad | Zustand |
|---|---|---|---|
| Rohdaten-Root (633 PDF, 57 RF5, 60 DWG, 34 DXF, 27 XLSX …) | lokal + Drive | `G:\Meine Ablage\26-03-18_Boeb_Adaptierung\` | PRIMARY, unsortiert, Dubletten |
| Sortierter Export | dito | `…\EXPORT\26_001_BOEBLINGEN\00…06` | Struktur vorhanden |
| Bestandsmodell 5e, Rechenstände 23.09. | lokal | `…\statistik-unterlagen-150325\…5e.rf5`, `SANDBOX_RFEM5_COM_20260923_1356\` | nur lokal, nicht in Drive gespiegelt |
| KI-Berichte, Kanon 23.09. | Drive | `_SEILSTATIK_BOEBLINGEN` (13EeKXWMpoN…), `deepseek/` (15gRtcOcLeMy…) | klassifiziert in Rev01 |
| Doku-Arbeitsordner | Drive | `LLM-LOCAL-SSOT/WORK/SEILNETZ-DOCU` (1lOJGVBVmYx7…) | 16 Objekte, davon 7 Shortcuts |
| Kanonische Quellenliste | Repo + Drive | `docs/26_09_24_…QUELLENVERZEICHNIS_LETZTGUELTIG_Rev01.md` | U1–U17, 8/17 Hashes |

### B Normen + Parser

| Was | Wo | ID / Pfad | Zustand |
|---|---|---|---|
| Normen-Original | lokal (Drive-Sync) | `G:\Meine Ablage\ZT-Gesellschaft\24_NORMEN\EUROCODE\EC3_Bem_u_Konstruktion_v_Stahlbauten\` | EN 1993-1-11:2010 + ÖNORM B 1993-1-11:2007 per Index VERIFIED_BY_INDEX, Datei noch nicht geöffnet |
| Parser-Root | Drive | `AI-PYTHON-PARSE` (1nbSlOQkCQ7Yhro3RxtIXW3QLP5yj9nBc), `NORMENPARSER.py`, Unterordner `ENGINEERING_PARSER`, `PDF_PARSER` | viele Versionen, keine Provenienzanker Parser→Seite |
| Parser-Skripte v1.x | Drive | `21_PYTHON_PARSER` (16AI_WZ6ibJjcnYBW1EENJ8oMj-Y9mP93): `NEXUS_PARSER_PIPELINE_v1_4.py`, `NEXUS RAG Chunk Validator v1.0.py`, `KB_PREPARSE_MIN.py` | 11 Varianten derselben Pipeline, keine kanonische |
| Masterindex | lokal | `G:\Meine Ablage\_INDEX.MASTER\` (`AI-PYTHON-PARSE_TREE.txt`, `GDRIVE-INDEX-LIST-FULL.txt`, `INVENTORY_GDRIVE_PDF.csv`) | Lookup-Reihenfolge lt. Wegweiser 29.09. |
| Wegweiser | Drive | `LLM-LOCAL-SSOT/00_WEGWEISER_NORMEN_PARSER_INDEX_REUSE__2026-09-29.md` (1LcigDxoDAS1v4Mb6EhufOa9i9SaZZDxl) | ACTIVE |

### C Codebase (Prompts, Workflows, Tools)

| Was | Wo | Pfad | Zustand |
|---|---|---|---|
| KO-Schema, Vokabular, kg_node/kg_edge | GitHub AI-WORKBENCH, Branch `claude/zealous-johnson-woguqi` | `schemas/` | validiert; 3 Lücken (Hash-Platzhalter, SOURCE ohne source_ids, Pflichtfelder SOURCE/MODEL/COLLECTION) |
| BM25-Index-Routine | dito | `tools/index_build.py`, `tools/index_search.py` (`--pack N` = Kontextpaket mit Tokenbudget) | stdlib, getestet auf 13 Objekten |
| MCP-Server-Skelett | dito | `tools/mcp_nexus_server.py` (index_search, ko_get, kg_edges, ko_propose, solver_verify) | fastmcp nicht installiert |
| Signal-Matrix, Router, Skill-Registry | GitHub julianzotter, Branch `claude/nexus-ai-os-dashboard-1t0lsm` | `nexus-workbench/backend/*.py`, `data/skill_registry.jsonl` | statischer Router, Skills als Prompt+Tool-Verträge |
| Parser + Register (Wiki-System) | Drive `_code` (14Bl77uPMo5QZx8P8eddbA2YQorYmt6--), `_registry` (10nI9Z9MOmN4z1Ji0cXM1fPw8ND1Y7j3V) | `02_parse_deepseek.py`, `03_build_registry.py`, `kb-register.json`, `authority-hierarchy.md`, `naming-conventions.md`, `layers.json`, `categories.json` | `01_scan_registry.py` fehlt; L-Namespace-Kollision (AUTH-L vs FILE-L) |
| Routinen | GitHub julianzotter `main` | `routines/W1_drive_indexer.md`, `W2`, `W4` | Prompts fertig, nicht aktiviert |

## 2 DER EINE ORT — ZIELSTRUKTUR

```text
G:\Meine Ablage\_developement\LLM-LOCAL-SSOT\
├── 00_WEGWEISER_…md                         (vorhanden)
├── _registry\                               (kb-register, authority, naming, layers, categories — vorhanden in Drive _registry → hierher verschieben oder Shortcut)
├── _code\                                   (01_scan / 02_parse / 03_build_registry / index_build / index_search / mcp_nexus_server — kanonische Kopie aus AI-WORKBENCH + Drive _code)
├── NORMEN\
│   ├── REGISTRY_NORMEN.jsonl                (SOURCE-KOs je Norm: EN/B/DIN-NA, Ausgabe, Hash, Originalpfad, Status FOUND/VERIFIED/ADOPTED)
│   └── PARSED\<norm_id>\                    (Raw-MD, Tabellen-CSV, meta.json — nur mit DERIVED_FROM-Anker auf Seite/Abschnitt)
└── PROJECTS\26_001_BOEBLINGEN\
    ├── 00_REGISTRY\   SOURCE_REGISTRY.jsonl · DATA_FREEZE_MANIFEST_v2.jsonl · DUPLICATES_REPORT.csv
    ├── 01_TABLES\     LF_LK_2015.csv · LF_LK_2026.csv · vermessung_2026.csv · pfeifer_K15.csv · bestandsaufnahme.csv · anhang27_laengen.csv · anhang30_anker.csv
    ├── 02_KO\         ko_proposals.jsonl (CANDIDATE) · ko_verified.jsonl (VERIFIED, nur ID02 schreibt)
    ├── 03_INDEX\      chunks.jsonl · index01.jsonl · index01.meta.json
    ├── 04_GRAPH\      artifacts.jsonl · edges.jsonl
    ├── 05_CONTEXT\    CONTEXT_PACK_BOEB_v001.md (+ .sha256)
    ├── 06_RUNS\       RUN-BOEB-000001\ … (input_hash, solver_ko, result.csv, review.md)
    └── 07_DOCU\       → Shortcut auf WORK\SEILNETZ-DOCU (bleibt, wo es ist)
```

Regeln: Binärdateien > 10 MB (.rf5, .dxf, .zip, Sovereign-PDFs) bleiben am Ursprungsort; `00_REGISTRY` hält Pfad, Drive-ID, SHA-256. Nichts wird gelöscht. Dubletten bekommen `DUPLICATE_OF`, kanonische Datei wird von ID01 festgelegt. Dateinamen nach `naming-conventions.md` (`JJ_MM_TT_AGENT_INHALT_vX_STATUS`).

## 3 SAMMELN — SCHRITT FÜR SCHRITT (Phase P1)

| # | Aktion | Rolle | Werkzeug / Kommando | Output | Abnahme |
|---|---|---|---|---|---|
| S1 | `01_scan_registry.py` schreiben (walk → sha256 → JSONL, atomar; gleiches Schema wie `02_parse`) | ID03 | neu, ~60 Zeilen stdlib | `_code/01_scan_registry.py` | Testlauf auf `EXPORT\26_001_BOEBLINGEN\01 Bestandstatik sortiert` liefert 100 % Hashes |
| S2 | Scan Projektroot lokal ausführen (nur Windows-PC, wegen G:) | ID01 (führt aus), ID04 | `python 01_scan_registry.py --root "G:\…\26-03-18_Boeb_Adaptierung" --out PROJECTS\26_001_BOEBLINGEN\00_REGISTRY\file-registry.jsonl --hash` | file-registry.jsonl (~1 000 Zeilen) | Laufzeit protokolliert, 0 Lesefehler oder Fehlerliste |
| S3 | Dubletten-Report | ID04 | `python 03_build_registry.py` (vorhanden, liest file-registry.jsonl) | DUPLICATES_REPORT.csv mit Zeilen | 13bb_ausführungsstatik_1 (2×), ChatGPT-Recherche (3×), Register_before_Deploy (3×) erscheinen |
| S4 | U1–U17 gegen Scan abgleichen, SOURCE-KOs erzeugen | ID03 | Skript `make_source_kos.py` (neu): Rev01-Tabelle → 17 KOs, Hash aus file-registry | `02_KO/ko_proposals.jsonl` (17 × SRC-BOEB) | Schema-valide; 17/17 mit sha256 |
| S5 | Manifest v2 ohne PENDING | ID03 | Ableitung aus S4 | `DATA_FREEZE_MANIFEST_v2.jsonl` | RUN1B = PASS |
| S6 | Normen-Slice Seilstatik registrieren | ID03 nach Wegweiser-Reihenfolge | Lookup in `GDRIVE-INDEX-LIST-FULL.txt`, `ZT-Gesellschaft_TREE.txt` nach: DIN EN 1990/NA, DIN EN 1991-1-1/-1-3/-1-4/-1-5 + NA, DIN EN 1993-1-11 + NA, EN ISO 12494, ETA-11/0160 | `NORMEN/REGISTRY_NORMEN.jsonl` | Je Norm Status FOUND / VERIFIED / MISSING mit `QUERY | INDEX_FILES_CHECKED | ORIGINAL_FOUND | PARSED_FOUND` |
| S7 | Kanonische Code-Kopie | ID03 | `git clone AI-WORKBENCH` → `_code/`; Drive `_code` dazu; Versionen `NEXUS_PARSER_PIPELINE_v1_4` als einzige Parser-Version festlegen, Rest `_OBS` | `_code/` mit README (Version, Hash) | kein Skript doppelt |

Erwartung S6: ÖNORM-B-Fassungen sind vorhanden, DIN-NA-Fassungen wahrscheinlich nicht → `MISSING` ist ein legitimes Ergebnis und geht als Beschaffungs-WorkOrder an ID01. Bis dahin gilt die Bestandsstatik 2015 als HISTORICAL-Normbasis (dort DIN EN + NA-DE bereits angewendet, Nachweis über U1 §1.6).

## 4 STRUKTURIEREN — DETERMINISTISCH, DANN SEMANTISCH (P2–P3)

| # | Quelle | Parser | Output | Locator-Regel |
|---|---|---|---|---|
| T1 | U15 RFEM-Ausdruck 07.09. (18 S.), U12a AP1 23.09. | Textexport → regex auf Tabellen „Lastfälle", „Lastkombinationen", „Stäbe" | `LF_LK_2026.csv`, `members_2026.csv` | `U15:p07:tab1.7:row12` |
| T2 | U3 Anhang 25 (199 S.) | pdfplumber, Seitenbereich Ergebnisse | `LF_LK_2015.csv`, `results_2015_LK100.csv` | `U3:p024:Stab34` |
| T3 | U8 Vermessung XLSX | openpyxl, Blatt „Koordinaten" | `vermessung_2026.csv` (11 Punkte, X/Y/Z NN) | `U8:Koordinaten:r7101` |
| T4 | U9 K15.105 PDF | pdfplumber Tabelle; Quellenbefund §8 als Kontrolle | `pfeifer_K15.csv` (S01–S21 Lsys/LA/LAG2/LB/Lo2k, Sv leer) | `U9:Blatt1:S19` |
| T5 | U9c Bestandsaufnahme XLSX | openpyxl | `bestandsaufnahme.csv` | `U9c:Tabelle1:r5` |
| T6 | U4 Anhang 27 / 30 | pdfplumber | `anhang27_laengen.csv`, `anhang30_anker.csv` | `U4-27:p2:S19` |
| T7 | Normen-Slice (nach S6) | `NEXUS_PARSER_PIPELINE_v1_4.py` → Raw-MD + Tabellen | `NORMEN/PARSED/EN1993-1-11/` | Parser-Version + Seite + Abschnitt Pflicht, sonst DERIVED/UNVERIFIED |

Semantisch (P3), erst nach T1–T6: `ko_propose` erzeugt CANDIDATEs für CLAUSE (LK220 Erg. 2; Schnee 0,60 kN PB03; Beiwerte LK100 Erg. 2 Pkt. 02-005), MATERIAL (PE5), COMPONENT (68 CABLE_RECORDs aus T1+T4+T5), FORMULA (Lsys = L(LK100) − Beschlag; Trafo U8e), SOLVER (RFEM-COM-Pipeline; Python-Längenkette), GOLDEN_CASE (Anhang-25-Reproduktion, tol 0,5 %), WORKORDER (F1–F7). Alle mit `extraction_method: llm_proposed`. **ID02** reviewt in separater Session gegen T1–T6 und schreibt `ko_verified.jsonl`. Messgröße: Annahmequote.

Mapping der Autoritätsstufen (Konflikt `authority-hierarchy.md` L0–L6 vs. `ontology_vocab.json` EVIDENCE A0–A5): L0/L1 → A0_NORMATIVE, L2 → A1_OFFICIAL, L3 → A2_PEER_REVIEWED, L4 → A3_TECHNICAL, L5 → A4_CURATED, L6 → A5_AI_DERIVED. Einmal festlegen, in `_registry/authority-hierarchy.md` als Tabelle ergänzen.

## 5 LADEN — INDEX, GRAPH, KONTEXT (P4–P6)

```bash
# Chunks aus 01_TABLES + Volltexten (U1, U2, U5, VORLAGE-002, Kurzbericht); chunk.schema.json vorher anlegen
python _code/chunk_build.py --in PROJECTS/26_001_BOEBLINGEN --out PROJECTS/26_001_BOEBLINGEN/03_INDEX/chunks.jsonl   # neu, ~80 Zeilen
# BM25-Index über Chunks + Registry (vorhanden)
python _code/index_build.py --root PROJECTS/26_001_BOEBLINGEN --out PROJECTS/26_001_BOEBLINGEN/03_INDEX/index01.jsonl --head 300
# Abnahmetest Recall (20 Fragen, Ziel ≥ 80 % Treffer in Top-3)
python _code/index_search.py "LK220 Ergänzung 2 Schnee" -i …/index01.jsonl -k 3
python _code/index_search.py "Beschlagmaß Leuchte Anker 0,193" -i …/index01.jsonl -k 3
# Graph-Projektion aus ko_verified.jsonl (neu, ~60 Zeilen: relations → kg_edge, KOs → kg_node)
python _code/kg_project.py --ko …/02_KO/ko_verified.jsonl --out …/04_GRAPH/
# Context Pack ≤ 1 200 Token nur aus VERIFIED (vorhandene Routine: index_search --pack)
python _code/index_search.py "Seilstatik Böblingen Scope Blocker" -i …/index01.jsonl --pack 1200 --format md > …/05_CONTEXT/CONTEXT_PACK_BOEB_v001.md
```

Context Pack Pflichtinhalt: Scope (3 Zeilen) · U1–U17 mit Hash-Präfix · Kernzahlen mit Einheit (PE5 d 8,1 mm, A 38 mm², E 130 GPa, F_Rd 27,9 kN; LK100 = 1,0·LF10 + 1,0·LF20; Beschlag 0,151/0,193/0,285 m) · offene Entscheidungen F1–F7 · Sperrliste (Kurzform) · Zeiger auf Index. Version + SHA-256 in Kopfzeile. ID01 liest einmal gegen.

## 6 ARBEITSABLAUF ZUSAMMENSTELLEN — GOAL 1 ALS ERSTER WORKFLOW (P7–P8)

Goal 1: Bestelllängen S19, S22 (+ S81 prüfen). Als Datei `WORKFLOWS/G1_bestelllaengen.yaml`:

```yaml
workflow: G1_BESTELLLAENGEN
workorder: WO-BOEB-000001
context_pack: CONTEXT_PACK_BOEB_v001 (sha256: …)
gates:
  - RETRIEVE:  {agent: ID03, tools: [index_search, ko_get], out: input_register.jsonl}   # jede Zahl mit KO-ID + Einheit
  - VALIDATE:  {agent: ID03, checks: [schema, units, F2_entschieden, F7_entschieden]}   # ohne F2 → HOLD
  - SOLVE:     {agent: ID03, solver: SLV-RFEM5-000001 (COM, Sandbox-Kopie) + SLV-PY-LAENGENKETTE-000001, out: RUN-BOEB-00000n}
  - INDEPENDENT_CHECK:
      agent: ID02   # separate Session, Input = nur RUN-Ordner + Registry
      cove_questions: [Welche Trafo (U8e vs G3)?, Welcher Lastfall definiert L?, Welches Beschlagmaß und Quelle?, Δ zu Anhang 27 im Bestand?, Sehnenlänge 7101→RL09 transformationsfrei?]
      recalcs: [Kettenlinie H·f = q·L²/8 (±5 %), Streckenkontrolle 7101/7102↔A05/A06, ΣV=0/ΣM=0 an neuen Ankern]
  - REVIEW:    {agent: ID02, verdict: PASS|HOLD|FAIL, residuum: r_vector}
  - ENGINEER_APPROVED: {agent: ID01}
  - EXPORT:    {agent: ID03, out: PFEIFER_Bestellblatt_S19_S22_v00x.csv}   # nur nach ENGINEER_APPROVED
residuum:
  tol: {Lsys_mm: 5, beschlag_bestaetigt: true, delta_anh27_bestand_mm: 2}
  loop_max: 5
  stop: [r <= tol, loop == 5, r_k >= r_k-1]
```

Delta-Loop: ID03 bekommt nur `r_vector` zurück, erzeugt Context Pack v(k+1) mit Diff, läuft erneut. Nach Stop ohne Konvergenz → HOLD an ID01 mit Residuumsliste. Jeder Lauf = RUN-KO.

## 7 WAS SOFORT GEHT UND WAS BLOCKIERT

| Sofort (ohne Windows-PC) | Blockiert bis |
|---|---|
| `01_scan_registry.py`, `make_source_kos.py`, `chunk_build.py`, `kg_project.py`, `chunk.schema.json`, 3 Schema-Fixes, G1-Workflow-YAML, CoVe-Fragenkatalog | – |
| Normen-Slice-Lookup in Masterindex (S6), soweit Indexdateien im Drive lesbar | Original-PDF öffnen nur lokal |
| 17 SOURCE-KOs mit den 8 bekannten Hashes | restliche 9 Hashes: S2 auf G: |
| Context Pack v001 aus Rev01 + VORLAGE-002 | VERIFIED-Status der KOs: ID02-Session |
| Trockenlauf G1 auf VAR-A-Ergebnissen 23.09. | Bestellfreigabe: F2, F7 (ID01) |

## 8 ROLLENTRENNUNG IM ABLAUF

- ID03 (diese Session): S1, S4, S5, S7, T1–T7, alle `_code`-Skripte, ko_propose, SOLVE, EXPORT.
- ID02 (zweite Session, bekommt nur `PROJECTS\26_001_BOEBLINGEN\` + `_registry`): S3-Kontrolle, T-Stichproben, KO-Review, INDEPENDENT_CHECK, REVIEW.
- ID01 (J. Zotter): S2 ausführen, Kanonik bei Dubletten, F1–F7, ENGINEER_APPROVED, Normen-Beschaffung bei MISSING.
- ID04 (Routine W1): täglicher Index-Diff auf `PROJECTS\26_001_BOEBLINGEN\`, meldet neue/geänderte Dateien ohne Registry-Eintrag.

Übergabe nur über Dateien mit Hash. ID02 sieht diesen Chat nicht.
