# SEILSTATIK BÖBLINGEN — END-TO-END-WORKFLOW, TAXATIVE SCHRITTFOLGE v1.0

`STAND: 2026-09-29 · AGENT: Claude Code (ID03) · STATUS: DONE (nicht VERIFIED) · KLASSE: WORKFLOW`
`BASIS: TODOS_VORSPANNUNG+TRANSFORMATION v1.0 · WO-BOEB-000003 · DREI-ORTE-Detailanleitung · NEXUS-Methode P0–P9 · Wegweiser Normen/Parser 29.09.`
`GEPRÜFT HEUTE: _developement (1OIyJI6rljIi8zNsT-iwg47NsuguoZqTB), _INDEX_LNK/BENCHMARK-SEILSTATIK (1ZpE9ym5UVEJuiLml0YKXDQl8Qk878sZl: 5 Dateien, alle Kopien der Chatprotokolle 22.09. und des 003-Entwurfs, keine neuen Primärdaten), _INDEX.MASTER (1oWX4JbZlJkUZJWwgSA_KxuFJRemvZoxK), _INDEX (1okgsbzTD2QuHZqPGYTrzmf_NESmkkaqD)`

## 0 Wie ein Recherche-Prompt aufgebaut wird (deine Frage)

Ein Prompt für ein Skript oder einen Agenten hat sieben feste Blöcke. Reihenfolge und Namen sind fix, damit jeder Lauf vergleichbar ist:

```text
SCOPE      Projekt, Gegenstand, Zeitraum. Beispiel: SEILSTATIK BÖBLINGEN, GZ 26_001, Wiedermontage 2026.
ROLE       Welche Rolle der Agent hat und was sie nicht darf. Beispiel: ID04 Registrar, nur lesen.
SOURCES    Wo gesucht wird, als IDs oder Pfade, nicht als Beschreibung. Reihenfolge = Priorität.
TASKS      Nummerierte Schritte. Jeder Schritt hat Input, Aktion, Output. Kein Schritt ohne Output.
RULES      Filter und Verbote. Dateitypen, Keywords, Ausschlüsse, „nichts erfinden", „FOUND ≠ VERIFIED".
OUTPUT     Dateiname, Format (JSONL/CSV/MD), Pflichtfelder je Zeile.
REPORT     Eine Zeile am Ende mit festen Feldern: QUERY | CHECKED | FOUND | NEW | DUPLICATES | MISSING | NEXT.
```

Antwort auf „Sagt man da Scope ist Seilstatik?": Ja. SCOPE nennt das Projekt, ROLE die Rolle, TASK 1 ist dann die Quellenrecherche. Der fertige Prompt für deine drei Schritte steht in Schritt 12.

## 1 Dateityp- und Keyword-Heuristik (Filterregeln für RULES)

| Gesucht wird | Typen | Keywords (Name oder Inhalt) | Wo zuerst |
|---|---|---|---|
| Pläne, Aufmaß | pdf, dwg, dxf, bak | 7864Halterungen, L-182, Lampenplan, Ringleuchte, Aufmaß, system_ | `26-03-18_Boeb_Adaptierung` Root + EMAILS |
| Statikmodelle | rf5, rf5bak, rs8, rf6 | leuchtenabspannung, 13bb, Gesamtmodell, VAR-A, BESTAND-5e | EXPORT\00…\14_bb, 02 RFEM-Modelle, SANDBOX\05_RECHENSTAND |
| Statikberichte, Prüfberichte | pdf, txt | statik_leuchtenabspannung, ergänzung, anhang_, Pruefbericht, 8w4_14, Probebelastung | EXPORT\01 Bestandstatik sortiert |
| Auftrag, Angebot, Mails | pdf, docx, eml | ANBOT, KALKULATION, Wiedermontage, Vusatiuk, Kneidinger, Asmus | Root, EMAILS, 03 Bestellschein |
| Herstellerdaten | pdf, csv, jpeg | PFEIFER, K15.105, Datenblatt PE, Seilkraftmessung, ETA-11, konstruktionsregeln | SEILE, 13bb-statik-dokumentation |
| Vermessung, Transformation | xlsx, dxf, csv, json, md | Koordinaten, geometer, transform, mapping, validation_report, zcheck | EMAILS\26_04_20, rfem_transform_pipeline, EXTRACTED_TABLES |
| Vorspannung, Seilkräfte | pdf, csv, json | Vorspann, Sollast, Sv, LK100, Seilkraftmessung, RESULTS_ | 13bb-statik-dokumentation, SANDBOX\03_RUNS, EXTRACTED_TABLES |
| Index, Tree, Workflows | txt, md, json, csv, jsonl | LIST, TREE, INDEX, DIR, MANIFEST, WORKFLOW, ARBEITSPLAN, PROTOKOLL | Root beider Ordner, _INDEX, _INDEX.MASTER, LLM-LOCAL-SSOT |

## 2 Taxative Schrittfolge (End-to-End)

### Phase A — Rahmen und Rollen (Tag 0)

1. WorkOrder WO-BOEB-000003 lesen und als CANDIDATE bestätigen oder ändern. Ohne bestätigte WorkOrder kein Lauf. Rolle ID01.
2. Rollen fixieren und getrennt halten: ID01 Engineer (Freigaben, Entscheidungen F1–F10), ID02 Reviewer (eigene Session, sieht nur Artefakte), ID03 Implementer (Skripte, Läufe, Vorschläge), ID04 Registrar (Index, Hash). Rolle ID01.
3. Zielablage anlegen: `LLM-LOCAL-SSOT\PROJECTS\26_001_BOEBLINGEN\` mit `00_REGISTRY`, `01_TABLES`, `02_KO`, `03_INDEX`, `04_GRAPH`, `05_CONTEXT`, `06_RUNS`, `07_DOCU` (Shortcut auf WORK\SEILNETZ-DOCU). Rolle ID03.
4. Schreibschutz auf `26-03-18_Boeb_Adaptierung\EXPORT\` setzen und die drei Saves vom 24.09. 05:27–05:35 als Vorfall vermerken. Rolle ID01.
5. Quellenordner als feste Liste mit IDs eintragen, Reihenfolge = Priorität: `_SEILSTATIK_BOEBLINGEN` 13EeKXWMpoN-FrH1oPFcOsPuK_9BqfmA3 · `26-03-18_Boeb_Adaptierung` 1tA6hbxW3SqxyGLPY8EP1J0ESmsVuMYi5 · `_developement` 1OIyJI6rljIi8zNsT-iwg47NsuguoZqTB · `_INDEX_LNK\BENCHMARK-SEILSTATIK` 1ZpE9ym5UVEJuiLml0YKXDQl8Qk878sZl · `_INDEX.MASTER` 1oWX4JbZlJkUZJWwgSA_KxuFJRemvZoxK · `_INDEX` 1okgsbzTD2QuHZqPGYTrzmf_NESmkkaqD. Rolle ID03.

### Phase B — Erfassung: Index zuerst, dann Delta (Tag 1)

6. Vorhandene Indexlisten einlesen, bevor irgendetwas gescannt wird: `BOEBLINGEN_LIST.txt`, `26-03-18_Boeb_Adaptierung_TREE.txt`, `DIR_LIST_SEILSTATIK.txt`, `26_07_04_CODEX_BOEB_LIST_latest_files_parse.json`, `EXPORT\…\00 DIRECTORY-LISTING MAIN INDEX.txt`, `SEARCH INDEX.txt`, `01/02/03 … DIR LIST.txt`, `26_09_18_CLA_EXTRACTED_TABLES_v1.0\MANIFEST.json` + `00_source_hashes.csv`, `_INDEX.MASTER\GDRIVE-INDEX-LIST-FULL.txt`. Output `INDEX_KNOWN.jsonl` (Pfad, Herkunftsindex, Datum des Index). Rolle ID04/ID03.
7. Drive-Inventar rekursiv für alle Ordner aus Schritt 5 mit `tools/drive_inventory.py` (liefert id, name, mimeType, size, modifiedTime, md5Checksum, path, Shortcut-Ziel). Output `00_REGISTRY\INVENTORY_DRIVE.jsonl`. Rolle ID04.
8. Lokaler Scan mit SHA-256 auf dem Windows-PC (G:) mit `tools/01_scan_registry.py --hash` über beide Projektordner. Output `00_REGISTRY\file-registry.jsonl`. Rolle ID01 führt aus, ID03 wertet aus.
9. Delta bilden: Inventar gegen `INDEX_KNOWN.jsonl`. Alles, was in keinem Index steht, wird als NEW markiert (heute bekannt: Seilkraftmessung_Pfeifer.pdf, Seilkraftmessung_Vergleich.pdf, 151001-13bb-protokoll_seil-beleuchtung.pdf, 150423-montageprotokoll_wandanker_bergmeister.pdf). Rolle ID03.
10. Dubletten bestimmen: gleicher md5 oder gleicher Name+Größe. `DUPLICATE_OF` auf die älteste Datei am kanonischen Pfad. Bekannte Fälle: 13bb_ausführungsstatik_1 (2×), ChatGPT-Recherche (3×), Register_before_Deploy (3×), 003-AUSFÜHRUNGSSTATIK (3×), VORLAGE-001/002 (je 2×). Output `DUPLICATES_REPORT.csv`. Rolle ID03, Kanonik ID01.
11. Typ- und Keyword-Filter aus Tabelle 1 anwenden. Jeder Treffer bekommt `focus` ∈ {PLAN, MODELL, BERICHT, AUFTRAG, HERSTELLER, VERMESSUNG, VORSPANNUNG, INDEX}. Output Spalte `focus` im Inventar. Rolle ID03.
12. Den dreistufigen Prompt so ausführen (Connector-Variante, wenn kein Skript läuft):

```text
SCOPE   SEILSTATIK BÖBLINGEN, GZ 26_001_BOEBLINGEN, Wiedermontage 2026, Bauort DE.
ROLE    ID04 Registrar. Nur lesen. Keine Datei ändern, verschieben, löschen. Nichts aus dem Gedächtnis ergänzen.
SOURCES 1) _developement 1OIyJI6rljIi8zNsT-iwg47NsuguoZqTB  2) _SEILSTATIK_BOEBLINGEN 13EeKXWMpoN-FrH1oPFcOsPuK_9BqfmA3
        3) 26-03-18_Boeb_Adaptierung 1tA6hbxW3SqxyGLPY8EP1J0ESmsVuMYi5  4) BENCHMARK-SEILSTATIK 1ZpE9ym5UVEJuiLml0YKXDQl8Qk878sZl
        5) _INDEX.MASTER 1oWX4JbZlJkUZJWwgSA_KxuFJRemvZoxK  6) _INDEX 1okgsbzTD2QuHZqPGYTrzmf_NESmkkaqD
TASK 1  Öffne jede SOURCE und liste alle Unterordner bis Tiefe 4 (je Ebene ein Aufruf parentId = '<id>'). Output FOLDERS.jsonl.
TASK 2  Lies in jeder SOURCE zuerst die Indexdateien (Typ txt/md/json/csv/jsonl mit LIST, TREE, INDEX, DIR, MANIFEST im Namen).
        Output INDEX_KNOWN.jsonl mit Pfad und Herkunft. Scanne danach nur Ordner, die in keinem Index vorkommen.
TASK 3  Extrahiere alle Objekte mit focus VERMESSUNG, VORSPANNUNG, BERICHT nach Tabelle 1 (Typen + Keywords).
        Je Objekt: id, name, mimeType, size, modifiedTime, md5Checksum, path, webViewLink, focus, in_index (ja/nein).
RULES   FOUND ≠ VERIFIED. Kein Objekt als „nicht vorhanden" melden, bevor TASK 1–3 abgeschlossen sind. Shortcuts als Shortcut kennzeichnen.
OUTPUT  INVENTORY_FOCUS.jsonl (eine Zeile je Objekt, Pflichtfelder wie in TASK 3).
REPORT  QUERY | FOLDERS_CHECKED | INDEX_FILES_READ | OBJECTS_FOUND | NEW_VS_INDEX | DUPLICATES | FOCUS_HITS V/Vs/B | MISSING | NEXT_ACTION
```
Rolle ID04 (Routine W1 oder Claude-Session mit Drive-Connector).

### Phase C — Registry und Klassifikation (Tag 1–2)

13. Registry zusammenführen: Inventar (md5) + lokaler Scan (sha256) + `00_source_hashes.csv` (18.09.) zu `SOURCE_REGISTRY_BOEB.jsonl`. Jede Datei genau einmal, Hash-Konflikte als CONFLICT. Rolle ID03.
14. Klassifizieren nach Regel, nicht nach Ermessen: PRIMARY, DERIVED, WORKFLOW, OBSOLETE, CONFLICT, INDEX (Regeln in WO-BOEB-000003 §3). Rolle ID03.
15. Kanonische Unterlagen U1–U19 festschreiben: U1–U17 aus Quellenverzeichnis Rev01, neu U18 Seilkraftmessung_Pfeifer.pdf (16.06.2015), U19 Seilkraftmessung_Vergleich.pdf. Aktuelle Berichtsfassung ist VORLAGE-005. Output Rev02 des Quellenverzeichnisses. Rolle ID03, Gegenlesen ID01.
16. SOURCE-KOs für U1–U19 erzeugen (Schema AI-WORKBENCH), Hash, Locator, Drive-ID. Output `02_KO\ko_proposals.jsonl`. Rolle ID03.
17. Review der SOURCE-KOs in separater Session: Stichprobe 10 %, Hash gegen Datei, Locator gegen Inhalt. Output `02_KO\ko_verified.jsonl`. Rolle ID02.
18. Manifest v2 ohne PENDING-Zeilen; Gate RUN1B = PASS. Rolle ID03, Bestätigung ID01.

### Phase D — Vorspannung schließen (Tag 2–3)

19. Drei Belegstellen der Bestandsstatik als CLAUSE-KOs anlegen: „Derzeit keine Vorspannung angesetzt" (Teil I S. 18), „Ersatz der Vorspannungen … durch tatsächlich angesetzte Lasten" (Zusammenschau), „nicht über Vorspannen … sondern durch Konfektion der Seillängen bzw. der Nulllage" (Hinweise). Rolle ID03.
20. Seilkraftmessung 2015 als GOLDEN_CASE-KO: 18 Seile, Sollkraft, gemessen, nachgerechnet 22 °C, Toleranz Δ ≤ 2,0 kN. Rolle ID03.
21. Sv-Register für alle 68 Seile: Sv aus K15-Blatt (S31–S67, S81), Sv aus Messblatt (18 Seile), N(LK100) aus 5e-Export. Output `01_TABLES\sv_register_68.csv`. Rolle ID03.
22. RF-Formfindung-Flag in RFEM 5 GUI an 5e und VAR-A prüfen, Screenshot als Beleg. Rolle ID01.
23. Sollast für die neuen Seile aus VAR-A festhalten: S19 4,62 kN, S22 3,83 kN bei 10 °C. Sensitivität E = 120/130/140 GPa auf Sv und L(LK100). Rolle ID03.
24. Berichtsabsatz „Anfangszustand" schreiben: kein Vorspann-LF, Anfangszustand = Knotengeometrie, Sv = N(LK100), Validierung durch Messung 2015, Hinweis auf LF-Nummerierung Text ≠ Modell. Rolle ID03, Gegenlesen ID01.
25. Review Phase D: Werte in 20, 21, 23 nachrechnen bzw. gegen PDF prüfen. Rolle ID02.

### Phase E — Transformation verifizieren (Tag 2–4)

26. Fitpunkte festlegen: nur A05 (7100), A06 (7103), A13 (Mittel 7107/7108), A14 (Mittel 7105/7106). Prüfpunkte: 7101, 7102, 7104. Ausschluss: 7000, 7004 (Leuchte, verformt). Rolle ID03.
27. Fit rechnen: Translation + Rotation + Spiegelung auf den vier Ankern. Abnahme RMS XY ≤ 0,15 m, Z-Mismatch ≤ 0,03 m. Output `transform_fit_v2.json`. Rolle ID03.
28. Translation-only-Test: Fit ohne Rotation wiederholen und Residuen vergleichen. Entscheidet, ob die Rotation nötig bleibt. Rolle ID03.
29. Transformationsfreie Streckenmatrix: 21 Paarabstände der 7 Punkte aus Vermessung und aus RFEM (5e für Anker, VAR-A für C06/C07). Output `01_TABLES\streckenmatrix_7pt.csv`. Rolle ID03.
30. Unabhängige Nachrechnung der Streckenmatrix in eigener Session, nur aus Rohdaten U8 und DIAG-JSON. Rolle ID02.
31. C21 klären: Streckenmatrix, Mastneigung, Punktidentität; Ergebnis als Entscheidung „3021 verschieben ja/nein" mit Begründung. Rolle ID03, Entscheidung ID01.
32. Mail an Geometer: 7101/7102 = Lochmitte Ankerplatte, Bolzenachse, Höhenbezug NHN, Bedeutung von 7104. Rolle ID01.
33. Mail an Kneidinger: Ankerplattenzeichnung 2024, Versatz Lochmitte zu Gabelkopfbolzen. Ersetzt Annahme 0,193 m. Rolle ID01.
34. Variante B (G3-XY, Z = +0,451) als Sensitivität in der Sandbox rechnen; S19/S22 beider Varianten nebeneinander. Output RUN-KO VAR-B. Rolle ID03.
35. Entscheidung F2 (Geometriebezug) auf Basis 27–34. Rolle ID01.

### Phase F — Lasten und Rechnung (Tag 4–6)

36. Lastmodell einfrieren: LF10–LF63 aus U15, γ_T-Inkonsistenz LK200 vs. 201–203 entscheiden, EK1-Umfang bestätigen. Output `01_TABLES\LF_LK_freeze.csv`. Rolle ID03, Entscheidung ID01.
37. LK220 = 1,35·LF10 + 1,50·LF43 in Bestand und VAR-A ergänzen (Entscheidung F3). Beide Modelle neu rechnen, nur Sandbox. Rolle ID03.
38. Endzustand A05/RL08/S17 schriftlich vom AG bestätigen lassen (Entscheidung F4). Bis dahin Bestand 2015 als Annahme kennzeichnen. Rolle ID01.
39. Normen-Slice registrieren nach Wegweiser-Reihenfolge: DIN EN 1990, 1991-1-1/-1-3/-1-4/-1-5, 1993-1-11 jeweils mit NA-DE, EN ISO 12494:2017, ETA-11/0160 Fassung 21.02.2025. Fehlende DIN-NA-Fassungen als MISSING mit Beschaffungs-WorkOrder. VwV TB Baden-Württemberg als Rechtsgrundlage nennen. Rolle ID03, Beschaffung ID01.
40. Produktionslauf VAR-A final (nach F2, F3, F4): alle LK/RK, Th. III. O., Exporte N je Seil, u je Knoten, Lagerkräfte je LK, Längen L(LK100). Output RUN-KO mit input_hash, solver_ko, Ergebnis-CSV. Rolle ID03.
41. Wiederöffnungsprüfung des gespeicherten Rechenstands auf separater Kopie, Δ = 0 dokumentieren. Rolle ID03, Bestätigung ID02.
42. Unabhängige Kontrollrechnungen: Kettenlinie H·f = q·L²/8 an drei Seilen (± 5 %), Gleichgewicht ΣV = 0 und ΣM = 0 an den neuen Ankern, η = N/F_Rd ≤ 1 für alle Seile, Tiefpunkt ≤ 2,50 m. Rolle ID02.
43. Residuum je Goal gegen die vorab definierten Toleranzen prüfen; bei Überschreitung nur das Residuum an ID03 zurück, loop_count ≤ 5, Stagnation → HOLD an ID01. Rolle ID02.

### Phase G — Längen und Anker (Tag 6–7)

44. Beschlagmaß aus Ankerzeichnung (Schritt 33) statt aus Bestand; Längenkette je neuem Seil: L(LK100) → Lsys (Sollast Sv, 10 °C) → L (−156 mm Spannschloss) → LA (15 kN, 20 °C) → LAG2 (E_k 0,00035) → LB (Beschläge 58/69 mm) → Lo2k. Output `01_TABLES\laengenkette_S19_S22.csv`. Rolle ID03.
45. Temperaturkorrektur Montagemonat ausweisen (α = 1,6·10⁻⁵/K). Rolle ID03.
46. S81 prüfen: Länge 2015 1,002 m gegen aktuell 1,678 m; Entscheidung neu fertigen oder nicht. Rolle ID03, Entscheidung ID01.
47. Wiederverwendbarkeit Bestandsseile: ΔL und ΔN je Seil tabellieren, Zustandsbefund vor Ort anfordern (01-015). Rolle ID03, Befund ID01/bauseits.
48. Ankerkräfte je LK vorzeichenrichtig exportieren (global und lokal), Übergabeblatt an bauseitige Ankerprüfung. Rolle ID03.
49. Lichte Höhe: Geländehöhe und Leuchtenunterkante beschaffen, Nachweis ≥ 5,00 m im maßgebenden Zustand. Rolle ID01 (Daten), ID03 (Nachweis).

### Phase H — Bericht und Freigabe (Tag 7–9)

50. Berichtsfassung V006 aus VORLAGE-005: Punkte der Stellungnahme 23.09. einarbeiten (01-005, 01-013, 01-017 CLOSED), Sv-Zeile korrigieren („PFEIFER-Sollast Sv = 0 kN" statt Schubverzerrung), neue Abschnitte Anfangszustand, Transformation, Normenstand 2026, Softwarebruch RSTAB 8 → RFEM 5 → RFEM 5.29. Gliederung wie Teil I–III plus Anhänge 25/27/30 („Ergänzung 4"). Rolle ID03.
51. Ergebnistabellen je Seil und je Kombination inklusive LK220 anhängen; Ankerkräfte; Längenkette; Sperrliste widerlegter Aussagen als Anhang. Rolle ID03.
52. Chain-of-Verification durch ID02: Prüffragen aus WorkOrder ableiten, nur gegen RUN-Artefakte beantworten, Verdikt PASS/HOLD/FAIL. Rolle ID02.
53. Vier-Augen-Kontrolle und ENGINEER_APPROVED durch ID01; Prüfinstanz extern ist AG-Sache (Angebot: Prüfstatik bauseits). Rolle ID01.
54. Erst nach 53: Bestellblatt PFEIFER S19/S22 (und ggf. S81) mit Lsys, Sv, Beschlagbezug, Temperatur. Export-Gate. Rolle ID03, Versand ID01.

### Phase I — Wissensupdate und Absicherung (laufend)

55. Jeden Lauf als RUN-KO ablegen (run_id, input_hash, solver_ko, gate_reached, loop_count, stop_reason). Rolle ID03.
56. Ergebnisse als CANDIDATE-KOs zurückspielen, nie direkt VERIFIED. Neuer GOLDEN_CASE: VAR-A final mit Toleranz 0,5 %. Rolle ID03, Freigabe ID02/ID01.
57. Context Pack v(N+1) neu generieren, nicht editieren; Hash in Kopfzeile. Rolle ID03.
58. Nach Wiedermontage: Seilkraftmessung wie 2015 beauftragen (PIAB oder gleichwertig) und als GOLDEN_CASE 2026 registrieren. Rolle ID01.
59. RUNLOG-Zeile in `LLM-LOCAL-SSOT\WORK` und Rev02/Rev03 des Quellenverzeichnisses. Rolle ID03.

## 3 Denkfehler-Regel (Conditional Pattern, für die Prompt-Registry)

Der Fehler im Gespräch war: Ein Assistent hat behauptet „das haben wir schon definiert", ohne dass es eine Stelle gab, an der es definiert wurde. Das ist eine unbelegte Zustandsbehauptung. Regel zur Speicherung unter `_developement\2026-09-25_Q2_PROMPT_REGISTRY_v1`:

```text
PATTERN  CLAIM_NEEDS_LOCATOR
IF    der Agent behauptet, etwas sei bereits erledigt, definiert, vereinbart oder bekannt
THEN  er nennt Datei + Stelle (Pfad, Zeile, Abschnitt, Nachricht mit Datum), an der es steht
ELSE  er schreibt „nicht belegt" und behandelt es als offen
CHECK am Ende jeder Antwort: Liste aller Aussagen der Form „haben wir schon / ist bekannt / wurde festgelegt" mit Locator.
      Fehlt ein Locator, wird die Aussage gestrichen oder als Annahme markiert.
WHY   Ohne Locator ist eine Zustandsbehauptung nicht prüfbar. Sie erzeugt scheinbaren Fortschritt und bricht die Beweiskette.
```

Zweite Regel, gleicher Mechanismus, für Zahlen: `NUMBER_NEEDS_UNIT_AND_SOURCE` (jede Zahl mit Einheit und KO-ID oder Locator). Beide Regeln sind CoVe-Fragen, die ID02 bei jedem Review stellt. Dieses Dokument wurde nach beiden Regeln geschrieben; jede „bereits vorhanden"-Aussage in Phase B–D trägt Datei oder ID.
