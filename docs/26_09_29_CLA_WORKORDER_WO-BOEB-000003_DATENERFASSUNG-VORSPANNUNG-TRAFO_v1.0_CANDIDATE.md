---
ko_id: WO-BOEB-000003
ko_type: WORKORDER
version: 1.0.0
title: Datenerfassung beider Projektordner + Klärung Vorspannung + Verifikation Koordinatentransformation
status: CANDIDATE
owner: HUM (J. Zotter)
created: 2026-09-29
ontology: {domain: [SEILSTATIK], value: P0_BLOCKER, signal: STRONG, capability: [EXTRACT, VERIFY], maturity: CANDIDATE, evidence: A3_TECHNICAL}
provenance: {source_ids: [SRC-BOEB-000006, SRC-BOEB-000008], locator: "docs/26_09_29_SEILSTATIK-BOEB_TODOS_VORSPANNUNG+TRANSFORMATION_v1.0.md", extraction_method: human, confidence: 1.0}
keyvalues:
  intent: Alle Daten der Ordner _SEILSTATIK_BOEBLINGEN und 26-03-18_Boeb_Adaptierung registrieren (ID, Hash, Pfad, Klasse); die zwei kritischen Unsicherheiten Vorspannung und Transformation mit Primärquellen schließen
  scope: "Drive 13EeKXWMpoN-FrH1oPFcOsPuK_9BqfmA3 + 1tA6hbxW3SqxyGLPY8EP1J0ESmsVuMYi5 (rekursiv); lokal G:\\Meine Ablage\\_SEILSTATIK_BOEBLINGEN + G:\\Meine Ablage\\26-03-18_Boeb_Adaptierung"
  agent: ID03 (Claude Code) für Skripte/Register; ID04 (Routine) für Index; ID02 (separate Session) für Review; ID01 für Ausführung auf G: und Entscheidungen
  budget_tokens: 400000
  gate: REVIEW
  loop_max: 5
relations:
  - {rel: DEPENDS_ON, target: WO-BOEB-000002, status: EVIDENCED, evidence_locator: "F2 Geometriebezug"}
  - {rel: SUPPORTS, target: RUN-BOEB-000001, status: EVIDENCED, evidence_locator: "VAR-A 23.09."}
labels: [datenerfassung, vorspannung, transformation, registry, drive-inventar]
---

# WO-BOEB-000003 — DATENERFASSUNG + VORSPANNUNG + TRANSFORMATION

`Ablage: LLM-LOCAL-SSOT/WORK (Drive 1HEcfQaf0JlsMPKXlDOz-z6yrVL72ifgP) · Spiegel: Repo julianzotter/julianzotter docs/ · Status CANDIDATE bis ID01 freigibt`

## 1 Ausgangslage (belegt)

- Zwei Projektordner, ein Auftrag: `26-03-18_Boeb_Adaptierung` (Auftragseingang 18.03.2026, EXPORT-Struktur 00–06, EMAILS, SEILE, SANDBOX 23.09., 26_09_18_CLA_EXTRACTED_TABLES) und `_SEILSTATIK_BOEBLINGEN` (KI-Berichte, Kanon `deepseek/`).
- Vorhandene Indexlisten, die als Wegweiser zuerst zu lesen sind: `BOEBLINGEN_LIST.txt` (507 KB, 1CxJ9DsxtAnXGlSghDdyyeiU0A39um0yW), `26-03-18_Boeb_Adaptierung_TREE.txt` (1781 Zeilen, 1cn2RGngiItetUSrqmU1JgD7CQe1xTkrk), `DIR_LIST_SEILSTATIK.txt` (1_xrN0JE1QXRcgjWpP6omcHaq_H7E7X2I), `26_07_04_CODEX_BOEB_LIST_latest_files_parse.json` (1bN6r67_8PhkUl1j7mEV0XSmW6QPL-zId), `EXPORT\26_001_BOEBLINGEN\00 DIRECTORY-LISTING MAIN INDEX.txt`, `SEARCH INDEX.txt`, `01/02/03 … DIR LIST.txt`, `DIRECTORY-LISTINGS_Systematische-Analyse+Synthese_v2–v5.txt`.
- Bereits extrahierte Tabellen (18.09., Ordner 1R-HktlRHJ4lgqzGPD6OdbODrHn_kAi9i): `00_source_hashes.csv` (40 KB), `01_load_cases_2015_vs_2026.csv`, `02_load_combinations_2015_vs_2026.csv`, `03_pfeifer_seildaten.csv` (68 Seile), `04_seil_bestand_bauteiler.csv`, `05_geometer_points_mapping_zcheck.csv`, `06_members_current_model_20260704.csv`, `07_sxx_member_register.csv`, `MANIFEST.json`. **Diese sind die Basis, nicht neu erzeugen.**
- Zwei Primärquellen, die in keinem Register standen: `Seilkraftmessung_Pfeifer.pdf` (16.06.2015, 18 Seile) und `Seilkraftmessung_Vergleich.pdf` (Messung vs. Rechnung 22 °C), Pfad `EXPORT\00 Bestandstatik fragmentiert\PDF_Finale_Dokumente_Ausgang\13bb-statik-dokumentation\`.
- Aktuelle Berichtsfassung: VORLAGE-005 (Codex, 23.09.) + Stellungnahme 23.09.; offene Entscheidungen F1–F10.

## 2 Aufgaben (Reihenfolge verbindlich)

| # | Aufgabe | Rolle | Werkzeug | Output | Gate |
|---|---|---|---|---|---|
| A1 | Drive-Inventar beider Ordner rekursiv (ID, Name, MIME, Größe, mtime, md5Checksum, Pfad, Shortcut-Ziel) | ID03/ID04 | `tools/drive_inventory.py --folder 13EeKXWMpoN… --folder 1tA6hbxW3…` | `00_REGISTRY/INVENTORY_DRIVE.jsonl` | VALIDATE: Anzahl ≥ 41 + 8 + (Tree-Zeilen) |
| A2 | Lokaler Scan mit SHA-256 (nur Windows, G:) | ID01 führt aus | `tools/01_scan_registry.py --root … --root … --out file-registry.jsonl --hash` | `00_REGISTRY/file-registry.jsonl` | VALIDATE: errors = 0 oder Fehlerliste |
| A3 | Abgleich Drive-md5 ↔ lokal-sha256 ↔ `00_source_hashes.csv` (18.09.); Dubletten (Name+Größe, Hash) | ID03 | `03_build_registry.py` (Drive `_code`) + neues `merge_registry.py` | `DUPLICATES_REPORT.csv`, `SOURCE_REGISTRY_BOEB.jsonl` | REVIEW ID02: 10 Stichproben |
| A4 | Klassifikation je Datei: PRIMARY / DERIVED / WORKFLOW / OBSOLETE / CONFLICT nach Rev01 §2–4; Indexlisten als Klasse INDEX | ID03 | Regeln aus Rev01 | Spalte `class` im Register | – |
| A5 | To-Dos Vorspannung V1–V8 abarbeiten (siehe TODOS-Dokument) | ID03, V4 ID01 | RFEM 5 Sandbox, CSV | `sv_register_68.csv`, GC-BOEB-000002, Berichtsabsatz | REVIEW ID02 |
| A6 | To-Dos Transformation G1–G8 abarbeiten | ID03, G5/G6/G8 ID01 | Python (numpy), Mails | `transform_fit_v2.json`, `streckenmatrix_7pt.csv`, VAR-B RUN | INDEPENDENT_CHECK ID02: G2 nachrechnen |
| A7 | PFEIFER-Produktdaten registrieren: ETA-11/0160 Fassung 21.02.2025 (DIBt-PDF laden, Hash), Datenblatt PE (`anhang_02-datenblatt_pfeifer_pe.pdf`, OCR), Konstruktionshilfen (`anhang_29`), `scan konstruktionsregeln pfeifer.jpeg`, Zugglieder-Prospekt 10/2015; Längendefinition Lsys/L/LA/LAG2/LB/Lo2k als FORMULA-KO | ID03 | WebFetch dibt.de, pfeifer.info; OCR | 5 SOURCE-KOs + 1 FORMULA-KO | REVIEW ID02 |
| A8 | Prüfberichte werkraum wien PB00–PB03 + TEXT-Fassungen: Prüfauflagen als CLAUSE-KOs (Schnee 0,60 kN/Leuchte, weitere) | ID03 | pdfplumber auf TEXT-PDFs | `clauses_pruefauflagen.csv` + CLAUSE-KOs | REVIEW ID02 |
| A9 | Registry-Zeile + RUNLOG-Eintrag in LLM-LOCAL-SSOT/WORK; Rev02 des Quellenverzeichnisses (VORLAGE-005 statt 002, Seilkraftmessung als U18/U19, ETA-Fassung) | ID03 | – | Rev02 im Repo + Drive | ID01 liest gegen |

## 3 Suchprompt für die automatisierte Erfassung (LLM-orchestriert, Drive-Connector oder Skript)

```text
ROLLE: ID04 Registrar. Lesend. Keine Datei ändern, verschieben oder löschen.
ZIEL: Vollständiges Inventar der Projektdaten SEILSTATIK BÖBLINGEN aus zwei Google-Drive-Ordnern
      und Ableitung eines Quellenregisters mit Klassifikation.
WURZELN (rekursiv, alle Ebenen, Shortcuts auflösen und als Shortcut kennzeichnen):
  1) _SEILSTATIK_BOEBLINGEN            Drive-ID 13EeKXWMpoN-FrH1oPFcOsPuK_9BqfmA3
  2) 26-03-18_Boeb_Adaptierung         Drive-ID 1tA6hbxW3SqxyGLPY8EP1J0ESmsVuMYi5
SCHRITT 0 INDEX-FIRST: Lies zuerst die vorhandenen Indexlisten und nutze sie als Wegweiser:
  BOEBLINGEN_LIST.txt · 26-03-18_Boeb_Adaptierung_TREE.txt · DIR_LIST_SEILSTATIK.txt ·
  EXPORT/26_001_BOEBLINGEN/00 DIRECTORY-LISTING MAIN INDEX.txt · SEARCH INDEX.txt · *DIR LIST.txt ·
  26_09_18_CLA_EXTRACTED_TABLES_v1.0/MANIFEST.json + 00_source_hashes.csv.
  Erzeuge daraus INDEX_KNOWN.jsonl (Pfad, Quelle der Indexzeile). Scanne danach nur das Delta.
SCHRITT 1 INVENTAR: Für jedes Objekt: id, name, mimeType, size, modifiedTime, md5Checksum, parents,
  path (vollständig ab Wurzel), webViewLink. Ordner je Ebene listen (der Connector listet nicht rekursiv).
  Output INVENTORY_RAW.jsonl. Nichts aus dem Gedächtnis ergänzen; nur gelistete Objekte.
SCHRITT 2 KLASSIFIKATION (Regel, kein Ermessen):
  PRIMARY  = Bestandsstatik 2015 (+Ergänzungen, Anhänge, Prüfberichte), .rf5/.rs8, Vermessung (DWG/DXF/XLSX
             7864Halterungen*), PFEIFER (K15*, Datenblatt, Seilkraftmessung*), Auftrag/Angebot/Mails, RFEM-Ausdrucke,
             DIAG-JSON, Rechenstände Sandbox, Fotos/Scans Bestand
  DERIVED  = CSV/MD/JSON-Auswertungen mit Quellenangabe (Extracted Tables, Kurzbericht, VORLAGE-00x)
  WORKFLOW = Arbeitspläne, Prompts, Pipelines, Chatprotokolle
  OBSOLETE = Dublette (gleicher Name+Größe oder gleicher md5) oder ältere Version derselben Datei
  CONFLICT = Dateien mit widerlegten Aussagen laut Sperrliste (Quellenverzeichnis Rev01 §6)
  INDEX    = Tree-/Dir-/List-Dateien
SCHRITT 3 FOKUS-TREFFER: Markiere gesondert alle Objekte zu (a) Geometrie/Vermessung/Transformation
  (7864*, *geometer*, *transform*, mapping.csv, validation_report.md, G3*), (b) Vorspannung/Seilkräfte
  (Seilkraftmessung*, K15*, *Sollast*, *LK100*, RESULTS_*.json), (c) PFEIFER-Produktdaten (Datenblatt,
  anhang_02, anhang_27, anhang_29, ETA*), (d) Prüfberichte (*Pruefbericht*, 8w4_14*).
SCHRITT 4 BERICHT: QUERY | INDEX_FILES_CHECKED | OBJECTS_FOUND | NEW_VS_INDEX | DUPLICATES |
  FOCUS_HITS a/b/c/d | MISSING_LINKS | NEXT_ACTION. FOUND heißt gefunden, nicht verifiziert.
  Keine Datei als „nicht vorhanden" melden, bevor Schritt 0 bis 3 durchlaufen sind.
```

Ausführung: entweder Skript `tools/drive_inventory.py` (empfohlen, deterministisch, liefert md5) oder der Drive-Connector mit obigem Prompt (je Ordnerebene ein `search_files parentId = '…'`, dann Klassifikation). Lokal auf G: zusätzlich `tools/01_scan_registry.py --hash` für SHA-256.

## 4 Abnahme der WorkOrder (Gate REVIEW → ENGINEER_APPROVED)

- Register enthält jedes Objekt beider Ordner genau einmal, Dubletten mit `DUPLICATE_OF`.
- Alle PRIMARY-Objekte tragen md5 (Drive) und, soweit lokal gescannt, SHA-256.
- Seilkraftmessung 2015 und ETA-11/0160 (2025) sind als SOURCE-KOs registriert.
- V1, V2, G1, G2, G3 liegen als Tabellen vor; ID02 hat G2 nachgerechnet.
- Mails G5, G6 sind versendet und im Register als Anfrage vermerkt.
- Offen bleibt bewusst: F2, F3, F4 (Entscheidungen ID01), Geometer- und Kneidinger-Antworten.

## 5 Nicht Teil dieser WorkOrder

RFEM-Neuberechnung (außer Sensitivität G7 in Sandbox), Berichtsfassung V006, Bestellfreigabe, Ankerbemessung, Normen-Slice DIN-NA (eigene WorkOrder nach Wegweiser-Reihenfolge).
