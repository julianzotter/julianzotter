# 26_001 SEILNETZ BÖBLINGEN — QUELLENVERZEICHNIS LETZTGÜLTIGE BESTANDSUNTERLAGEN + NEUERKENNTNIS-CHECK

`STAND: 2026-09-24 12:40 UTC · Rev 01 · AGENT: Claude Code (Session seilstatik-doku-overview) · MODUS: READ_ONLY (keine Rechnung, keine Freigabe) · KLASSE: DERIVED (Register über PRIMARY-Quellen)`
`QUELLEN: Drive-Ordner _SEILSTATIK_BOEBLINGEN (13EeKXWMpoN…, 41 Objekte) · Unterordner deepseek (15gRtcOcLeMy…, 8) · SEILNETZ-DOCU (1lOJGVBVmYx7…, 15) · 10 Screenshots vom 24.09. · gelesen: 22 Dateien vollständig, 5 große Protokolle nur strukturell (siehe §9)`
`GIT: julianzotter/julianzotter · Branch claude/seilstatik-doku-overview-rc0lpt · docs/26_09_24_SEILNETZ-BOEB_QUELLENVERZEICHNIS_LETZTGUELTIG_Rev01.md · Commit ccbf8b9 · Drive-Kopie 1Bztv0nNthbUdSHqvEizKqA1Rk4wEyWp8 (SEILNETZ-DOCU)`

## 0 TL;DR

- **Letztgültiger Rechen- und Dokumentationsstand = Unterordner `deepseek` vom 23.09.2026**: Kurzbericht VAR-A (LK100) + Prüfbericht VORLAGE-002 (Claude Code, ersetzt VORLAGE-001/Gemini) + Ausdruckprotokoll AP1. Alle drei tragen `STATUS=VORLÄUFIG · FREIGABE=NEIN · BESTELLREIF=NEIN`.
- **Kanonische Bestandsunterlagen** (Planungsgrundlage) sind in VORLAGE-002 §2 als U1–U12 mit Pfad + SHA-256 fixiert; dieses Verzeichnis übernimmt sie 1:1 (§1) und ergänzt Drive-IDs.
- **Wichtigste Neuerkenntnis seit 18./22.09.**: Variante A ist durchgerechnet (η ≤ 0,42, S19 ≈ 4,73 m, S22 ≈ 9,38 m Lsys), aber der **XY-Bezug der neuen Anker widerspricht der G3-Festlegung vom 06.09.** (4-Anker-Fit RMS 0,098 m vs. 7-Punkt-Starrfit RMSE 0,62 m) → S19/S22 differieren um 0,4–0,6 m → Entscheidung **F2** blockiert die Bestellung.
- **Drei weitere Blocker**: LK220 (Erg. 2, 20,16 kN) fehlt in allen Modellen (F3) · Endzustand A05/RL08/S17 lt. Rückbauplan 2022 unklar (F4) · Seilsteifigkeit EA 3 420 vs. 4 940 kN (F6).
- **Korrekturen an den beiden heute (10:16/10:19 UTC) erzeugten SEILNETZ-DOCU-Dateien** (Rev00 / BEFUND V01): 5 Sachfehler, siehe §7.
- **Sperrliste** widerlegter KI-Aussagen (§6) bleibt gültig; VORLAGE-001 (Gemini) kommt mit 8 Fehlern (B1–B8) hinzu.

---

## 1 LETZTGÜLTIGE BESTANDSUNTERLAGEN (PLANUNGSGRUNDLAGE, Status PRIMARY)

Quelle der Kanonik: `26_09_23_PRUEFBERICHT_SEILSTATIK_BOEBLINGEN_VORLAGE-002.docx` §2 (Drive 1FtxONa1pJKRb-saXxoP6YIPvvHB563LQ) + Kurzbericht 23.09. (1naQTIh4XhRuE4jaJCzF3nen6nvtU3vZw). Pfade relativ zu `G:\Meine Ablage\26-03-18_Boeb_Adaptierung\`. SHA-256 gekürzt wie in VORLAGE-002; Vollwerte in `MANIFEST.json` / `RECHENSTAND_HASHES_20260923_1437.json` (lokal, Sandbox).

### 1.1 Bestandsstatik 2015 (bauchplan, T. Baldauf) + Prüfung (werkraum wien, Th. Eschbacher)

| ID | Unterlage | Pfad | Datum | Hash / Drive | Rolle |
|---|---|---|---|---|---|
| U1 | Statik Leuchtenabspannung Teil I–III (62 S.) | `EXPORT\26_001_BOEBLINGEN\01 Bestandstatik sortiert\01-statik_leuchtenabspannung-teil1bis3_150417.pdf` | 17.04.2015 | 446D0E8D… | Lasten, System, Normen, Erläuterung |
| U2 | Ergänzungen 1–3 | `…\01 Bestandstatik sortiert\02/03/04-statik_leuchtenabspannung-ergänzung-1..3.pdf` | 21.04./28.04./19.05.2015 | – | Erg. 2 = LK220 + Beiwerte LK100 (Pkt. 02-005) |
| U3 | Anhang 25 RFEM-Ausdruck Gesamtstatik (199 S.) | `…\01-statik-Anhänge\anhang_25_leuchtenabspannung_gesamtstatik.pdf` | 17.04.2015 | 90469A67… | Modell 5e, LF/LK, Ergebnisse (max u 2 078,8 mm Kn 17) |
| U4 | Anhang 26 Lasttabellen · Anhang 27 Systemlängen PFEIFER · Anhang 30 Ankerlasten | `…\01-statik-Anhänge\anhang_26/27/30…pdf` | 2015 | 9018D191… / A7C6FD45… | Anh. 27 = L(LK100) Knoten-Knoten; Anh. 30 = Ankerlasten (B_DERIVED) |
| U5 | Prüfberichte werkraum wien PB00–PB03, GZ 8w4_14 | `…\01 Bestandstatik sortiert\20–23-Pruefbericht_0x.pdf` (+ TXT) | 01.12.2014 – 11.07.2015 | – | Prüfauflagen; Schnee-Auflage 0,60 kN/Leuchte (PB03) |
| U6 | RFEM-Bestandsmodell 5e (= Berichtsmodell Anh. 25) | `…\00 Bestandstatik fragmentiert\14_bb_Gesamtsystem_RFEM\14_bb\statistik-unterlagen-150325\leuchtenabspannung_gesamt_nachaufmassgeometer_150328_5e.rf5` (69 345 280 B) | 14.04.2015 (Aufmaß intermetric 25.03.2015) | BD77CF83… | **einzige belegte Rechenbasis Bestand**; 86 Kn, 68 Seile, 20 Maste, 19 LF, 21 LK, 2 RK |
| U6a | 13bb_ausführungsstatik_1.rf5 (Archiv 54 054 912 B / Exportkopie 54 075 392 B) | `…\statistik-unterlagen-150325\` bzw. `…\04 Berechnung Gesamtsystem\` | 01.04.2015 / 11.09.2026 | – | Vorläufer, **nicht** Berichtsmodell; zwei byteverschiedene Dateien |

### 1.2 Auftrag / Kommunikation

| ID | Unterlage | Pfad / Drive | Datum | Rolle |
|---|---|---|---|---|
| U7a | Anfrage LR (N. Vusatiuk) „Wiedermontage … 2 Fassadenanker statt Pylone“ + Mailkette Ankerbemessung 2024 (Kneidinger ↔ IEA/Asmus) | Drive `deepseek/BV Boardinghouse Böblingen _ … (2 Fassadenanker statt Pylone).pdf` (1tA7ObaeBu7zG37Dp5H42JpbwL62sEDaO); Dropbox `26_boeb_adaptierung` (Origin) | 06.03.2026 (Kette 26.02.–18.03.2024) | Scope-Definition; Anlagen: L-182-Plan, 7864Halterungen.dwg, Bestandsaufnahme Seile.xlsx |
| U7b | Angebot 18.03.2026 → Auftrag 19.03.2026 (final 12 000 €, Fassadenankerprüfung **ausgeschlossen**) | `EXPORT\…\03 Bestellschein\11-ANBOT…beauftragt_2026-03-19.pdf` | 19.03.2026 | Schnittstellenkräfte an Anker sind geschuldet, keine Ankerbemessung |
| U7c | Anmerkung Seilgeometrie (Bearbeitungsbereich RL06/RL11 bis A14/C21) | Mail 11.04.2026 | 11.04.2026 | Bereichsabgrenzung |
| U7d | Ringleuchtenplan L-182 Stand 30.03.2015 | Drive `deepseek/13_bb_5_L-182-ringleuchtenabspannung (002).pdf` (1rGG7bL_1VJUGa0q80btktJLL0t1nDwSF) | 30.03.2015 | Sxx-Lageplan; Regel „S13/18 = Lageplan/RSTAB“ |

### 1.3 Vermessung 2026 + Transformation

| ID | Unterlage | Pfad / Drive | Datum | Rolle |
|---|---|---|---|---|
| U8 | Vermessung Zizmann & Blessing, 11 Punkte 7000/7004/7100–7108 (Lochmitte Halterungen) | `EMAILS\26_04_20_DXF+Koordinatenliste\original-anhang\7864Halterungen_mit_Lampenplan_Boardinghouse.xlsx` (+ .dxf 62,5 MB) | **Messung 11./13.02.2026**, Lieferung 20.04.2026, Bestätigung 21.05.2026 (BöblingenMessung.docx, SharePoint) | PRIMARY Geometrie; Z-Werte NN |
| U8a | Transformationspaket prüffähig (8-Paar-Fit, Spiegelung + Rotation, RMSE 0,651 m) | `EXCEL-Koordinaten-Transformation\PYTHON-SCRIPT_rfem_geometer_transform_final\…prueffaehig_package.zip` | 18.05.2026 | B_DERIVED, Basis G3 |
| U8b | Pipeline-Output (7-Punkt, RIGID_OR_REFLECTION, RMSE 0,623 m, CAUTION) | `…\02 RFEM-Modelle\rfem_transform_pipeline\output\{transformed_nodes.csv, validation_report.md, audit_log.json}` | 19./20.05.2026 | B_DERIVED |
| U8c | Mapping + Transformation Geometer→RFEM (PDF) | Drive `deepseek/26_05_20_MAPPING+TRANSFORMATION_GEOM-REFEM.pdf` (1B7peI9xm6aRSDhfkZREauDevgePPXhvi) | 20.05.2026 | Mapping 105/106/113/114/3006/3007/3021 ↔ 7100/7103/7107/7105/7101/7102/7104 |
| U8d | **G3-Entscheidung** Geometrie-Transformation & Mapping-Freigabe (Zotter) | Drive `26_09_06_ZOTTER_BOEBLINGEN_G3_ENTSCHEIDUNG_FREIGABE__SEILSTATIK.docx.docx` (1ZAltNAK6WEU-IS59OlKGTyjrWpMK-Lmx) | 06.09.2026 | XY ACCEPT mit Auflagen · Z = MANUAL_ENGINEERING_Z · Modell-Hash 7DB74920…C094F96C · **bedingte Geometriefreigabe, keine Statikfreigabe** |
| U8e | Transformation 23.09. (VAR-A): x = X − 3 500 460,605 · y = −(Y − 5 394 418,936) · z = −(Z − 445,472); Fit auf A05/A06/A13/A14, RMS 0,098 m | Kurzbericht 23.09. §GRUNDLAGEN | 23.09.2026 | **CONFLICT mit U8d** (Prüfanmerkung 01-006 → F2) |

### 1.4 PFEIFER / Zulassung / Bestandsseile

| ID | Unterlage | Pfad / Drive | Datum | Kernwerte |
|---|---|---|---|---|
| U9 | PFEIFER Berechnungsblatt K15.105.01.01.00 Ind. 1 (Blatt 1 S01–S21, Blatt 2 S60–64/S81) | `SEILE\K15.105.01.01.00-Ind.1-xls.pdf`; Drive 14ayZSnQz2-bNW_LpvRl-sIr8UavjhpAQ | erstellt 31.03.2015, geändert 24.04.2015 | PE5 1×19, d 8,1 mm, A 38 mm², E 130 ± 10 kN/mm², Z_Bk 47 kN, Ablängkraft 15 kN, E_k 0,00035, Spannschloss-Abzug 156 mm, Beschläge 981/985; **Sv S01–S21 leer**, Sv S81 = 5 kN |
| U9a | Datenblatt PE (PFEIFER) | `SEILE\Datenblatt PE.pdf` | 20.03.2026 (Mail) | Text nicht extrahierbar (OCR offen) |
| U9b | Zulassung Seilsystem | ETA-11/0160 (aktuelle Rev **OPEN**); im Modell noch abZ Z-14.7-411 | – | F_Rk 46,1 kN / **F_Rd 27,9 kN** (Bestandsstatik §4.1.1) |
| U9c | Bestandsaufnahme Seile und Zubehör (LR, 24 Zeilen) | `Bestandsaufnahme Seile und Zubehoer.xlsx` | 17.03.2026 | S18 15 790 · S19 3 565 · S20 20 321 · S21 3 661 · S22 7 685 mm; 2 Zeilen „???“ 750 mm |

### 1.5 Aktuelle Rechenmodelle / Rechenstände (RFEM 5.29.01)

| ID | Unterlage | Pfad / Drive | Datum | Status |
|---|---|---|---|---|
| U10 | Rechenstand Bestand 5e neu berechnet | `SANDBOX_RFEM5_COM_20260923_1356\05_RECHENSTAND\BOEB_BESTAND-5e_NEUBERECHNET_RFEM529_20260923_1437.rf5` | 23.09.2026 | 317D78D7… · reproduziert Anh. 25 (Δ < 0,02 mm / 0,001 kN im Bereich) |
| U11 | Rechenstand **Variante A** (Pylone C06/C07 → Fassadenanker) | `SANDBOX…\05_RECHENSTAND\BOEB_VAR-A_…_GERECHNET_RFEM529_VORLAEUFIG_20260923_1437.rf5` | 23.09.2026 | EAB6A5B1… · **VORLÄUFIG**, 84 Kn / 68 Seile / 18 Maste |
| U12 | Prüfexporte, Skripte, Protokolle, Status | `SANDBOX…\06_PRUEFEXPORTE` (u. a. `VAR-A_ANKERKRAEFTE_JE_LK.csv`), `04_SKRIPTE_REPRO`, `03_RUNS`, `04_STATUS_PRUEFSTAND_20260923.md` | 23.09.2026 | lokal; nicht in Drive gespiegelt (OPEN) |
| U12a | Ausdruckprotokoll AP1 (RFEM 5.29, 23.09.) | Drive `deepseek/26_09_23_Ausdruckprotokoll - AP1.pdf` (1k9iqOuSXk8qC9Dz9isbLrmqVt_QxWR_M, 2,7 MB) | 23.09.2026 | PRIMARY Export; nicht gelesen (§9) |
| U12b | RFEM-Screenshot 23.09. | Drive `deepseek/26-09-23 rfem screenshot.png` (1w4kSZhxmFz5M_JmHQ6yDj39JehedOpuv) | 23.09.2026 | LK100 Verformung, Anzeigefaktor 2,25 |
| U13 | 01-Gesamtmodell-Seilabspannung_V01.rf5 (106 Kn = 5e + 20 Hilfsknoten + Knotenupdate 07/2026) | `…\02 RFEM-Modelle\RFEM-MODELL-Gesamt\` | mtime 07.09.2026 15:24 | **nicht Rechenbasis** (01-001); Hash-Drift gegenüber G3 (7DB74920… nicht mehr belegt); Varianten V01.a / V02 (11.09.) |
| U14 | RFEM5_ACTIVE_GEOMETRY_DIAG_20260704_074409.json | Drive 1pSgeP5K7YOfH3yxkfJoQHQSiaaRhpSNI | 04.07.2026 | PRIMARY Run-Artefakt: 106 Kn / 105 Stäbe = 68 Type 9 (Seil) + 37 Type 1 (Balken) |
| U15 | RFEM-Ausdruckprotokoll V01 (18 S.) | Drive 1LwPEUzBKqWUVV9xXv5mQ3Pjz6eDebrV4 | 07.09.2026 | PRIMARY Export: LF10–LF63, LK100–218, EK1/EK2, Material 5 „Seil PE Z-14.7-411“, **kein Vorspann-LF** |
| U16 | Scan-Modell-Knotennummern+Halterungen (PDF + 3 JPG) | Drive 1kEmvJdIQdb35mk_q1KOfn4I_rWO4VRgq, 1TvPIstK…, 1P87B0yg…, 1xe76Nvy… | 07.09.2026 | Planbilder Sxx ↔ Knoten (Mapping-Beleg) |
| U17 | RFEM SCREENSHOT01.png (Stabtabelle Balkenstäbe 1001–1021) | Drive 1WvEjjgF95rRz4e_JEhMFRp5DUuQrLxL3 | 07.09.2026 | Beleg „Balkenstab, Vouten linear, Gelenke 0/0“ |

### 1.6 Normen (CURRENT vs. HISTORICAL)

| Norm | Verwendung | Status |
|---|---|---|
| DIN EN 1990 + NA-DE | Kombinatorik γ/ψ, RK/EK | CURRENT |
| DIN EN 1991-1-1 / -1-3 / -1-4 / -1-5 + NA-DE | EG, Schnee, Wind (Zone 1, q_b,0 0,32 kN/m², q_p 0,50 kN/m²), Temperatur (+57 / −34 K) | CURRENT (Bestandswerte prüfen, B6/B7) |
| EN ISO 12494 | Raueis RD2 (0,009 kN/m Seil) | CURRENT |
| DIN EN 1993-1-11 + NA | Zugglieder, Th. III. O., SLS | CURRENT |
| ETA-11/0160 | PFEIFER-Seilsystem | CURRENT, Rev OPEN |
| EN 1992-4 / ETA-04/0095 (Würth W-VIZ) | Anker | extern (IEA), nur Schnittstelle |
| DIN 1055-4/-5, DIN 1045-1:2008, DIN 18800, abZ Z-14.7-411 | im Bestandsmodell 2015 | HISTORICAL (kennzeichnen) |
| ONR 24005:2002-11 | Gliederungsmuster Doku | nicht normativ DE |

---

## 2 ORDNER `_SEILSTATIK_BOEBLINGEN` (13EeKXWMpoN-FrH1oPFcOsPuK_9BqfmA3) — 41 OBJEKTE, KLASSIFIZIERT

Legende: **PRIMARY** = Planungsgrundlage · **DERIVED** = Ableitung, zitierfähig mit Vorbehalt · **WORKFLOW** = Prozess/Prompt · **OBSOLETE** = Dublette/überholt (READ_ONLY, nicht löschen) · **CONFLICT** = enthält widerlegte Aussagen, gesperrt

| mtime | Datei | Drive-ID | Klasse | Bewertung |
|---|---|---|---|---|
| 23.09. | `deepseek/` (Ordner, 8 Objekte → §3) | 15gRtcOcLeMyaOchzmQFmtKKDNYV29Z1d | **PRIMARY-Hub** | letztgültiger Stand |
| 22.09. | 26_02_22_LASTEN+Kombi-EXCEL2RFEM.xlsx | 1oaDsK1NJM95xtpbucmZ-oZ9cz_RadBFF | DERIVED | Kombi-Template mit **anderer LF-Nummerierung** (LF1/10/21–24/31–34/41/42) + `#NAME?`-Fehler → nicht Bestand |
| 22.09. | 26_09_22_SEIL_CHATPROTOKOLL_GPT-Business2.txt | 1nGVnkOq2l8L_8360h98t12CR-F6klBJK | WORKFLOW | RUN 03/04/05B/05C (Cloud-Rollen, Member n ↔ Snn, RSTAB-Crosswalk); Work-Order P0–P2 |
| 22.09. | 26_09_22_SEILSTATIK_BOEBLINGEN.zip (58,6 MB) | 1nDdnymqGo07YxNwy38VBO1BTCU35-LGy | OPEN | Inhalt nicht geprüft (vermutlich rf5 + Pakete) |
| 22.09. | 26_09_22_SEIL_CHATPROTOKOLL_GPT-Business.txt | 15TElh6Q1ASrzv1yrcVQRWlvIbJvCX7UI | WORKFLOW | Obermenge von …Business2 (gleiche TL;DR-Blöcke + Topologie-Auswertung DIAG-JSON) |
| 21.09. | 26_09_21_0000_SEILSTATIK_BÖBLINGEN_CHATPROTOKOLLE_DIVERSE.txt | 1btQL2N0JNlrip3oi-z7tQ_H-FcNGSwHz | WORKFLOW | Synthese Hash-Drift, Sv = N(LK100), LK220, Audio-Memo; Rest = Dlubal-API-Handbuch (projektfremd) |
| 18.09. | 26_09_18_CLA_ANALYSE_KI-BERICHTE_SEILSTATIK-BOEBLINGEN_v1.0.md | 1bPn93w54bW9f_Nm8ocK2kjTp-aLcyB4D | DERIVED | **Sperrliste** (6 widerlegte Claims), Dubletten-Matrix der 10 KI-Dateien |
| 18.09. | 26_09_18_BÖBLINGEN_CHATPROTOKOLLE_Diverse.txt | 1sD-2hJXQmav7me5sG60ZbBtMa0x3Pnxd | CONFLICT | fabrizierte Koordinaten, falsche LF-Liste, F_Rd 28,79 kN → nicht zitieren |
| 18.09. | 26_09_18_AGENTIC DEEP-PARSING PIPELINE … FINETUNE.txt | 17cEHPwaxF7p0qsaQlHiGbS9Dua9cyg8Q | WORKFLOW | Suchparameter; Annahme „Vermessung Juni 2026“ **falsch** (11./13.02.2026) |
| 18.09. | SEILSTATIK_BOEBLINGEN_Quellenbefund_2026-09-18.md (343 KB) | 17PUBwx7nMoZgJUsveGVe1Wfwfbjl55pc | DERIVED | umfangreichstes Quellenregister (Q01–Q45 + Discovery), GAP-Kette §12, Modelltabelle §3 |
| 11.09. | 26_07_04_CODEX_SEILSTATIK_BOEBLINGEN_QUELLEN_WORKFLOW_INVENTAR.md | 11sPwIAIFC8ARtJD-Akg9ypzHQb-HQgOU | DERIVED | Erstinventar 03.07.: Dateitypen (633 PDF, 57 RF5 …), Ordnerstruktur, Mapping-Tabelle, Fertigstellungsplan |
| 11.09. | 26_07_04_CODEX_BOEBLINGEN_RFEM5_API_KNOTENUPDATE.txt | 1wIc23kLXYzZOUHXlHg4p6UOfFxh6c9s6 | DERIVED | Knotenupdate-Log 04.07. (APPLIED_AND_SAVED) |
| 11.09. | 26_09_11_QUELLEN-LISTE.txt (184 KB) | 1Jqdr-XQVjFCHFMyU5rdakaBW8CfxxLkR | DERIVED | Rohliste Unterlagen + eingebettete IEA-Probebelastungs-/Anker-Texte (2014) |
| 11.09. | 26_09_11_SEILSTATIK_BOEBLINGEN_Quellenverzeichnis.docx | 1tIYZ4jT6nbJr4sQxE1hyaHYMdje8o0Jc | DERIVED | ChatGPT-Analyse: Prio-Matrix P0-A…P3, Kapitelstruktur 1–15, CABLE_RECORD; LF-Liste darin **überholt** |
| 09.09. | NEXUS AI-AEC Operation System & Stahlbetonbau-Wissensbasis.txt | 1WtEFw6S3w5TkV7OEAjebWeh_ZNpVPvoM | WORKFLOW | projektfremd |
| 09.09. | Sovereign_AEC_Operating_System_SEILSTATIK_4p.pdf / …SEILSTATIK.pdf (27,6 / 22,1 MB) | 1Wu_DuonrINZu1F_RKATLixblfz_ju9lT / 1Mhkeuu-ipHh_Vy350c4l7AUGB-r2lLV1 | WORKFLOW | Präsentation; nicht gelesen |
| 09.09. | IMPLEMENTIERUNGSLEITFADEN SEILSTATIK AEC WORKFLOW.txt | 1EuJRn9qesT70CwfyPI2prryZEqS_--tL | WORKFLOW | – |
| 09.09. | Deterministischer Workflow für Seilstatik und PFEIFER-Fertigung.txt | 1K0AmFPKTm3XplHOH-QjWaCjY6KVx0n75 | WORKFLOW | 10-Phasen-Workflow, Längenkette Lsys→LA→LAG2→LB→Lo2k |
| 07.09. | ChatGPT-Seilstatik Böblingen STATUS-QUO-05A.txt | 1pK14vQj12LqdPAeVdP1CO816EdRPanTF | DERIVED | **Kanon ChatGPT-Familie** (RUN 05B Member-Tabelle 1001–1021, Dummy-Stäbe) |
| 07.09. | K15.105.01.01.00-Ind.1-xls.pdf | 14ayZSnQz2-bNW_LpvRl-sIr8UavjhpAQ | **PRIMARY** | = U9 |
| 07.09. | ChatGPT-Seilstatik Böblingen STATUS-QUO.txt | 15l4hs2qr74vXWpKAD9ithXEtoksAduIa | OBSOLETE | 0 % unique → in 05A enthalten |
| 07.09. | GEMINI-Seilstatik Böblingen RFEM-KNOTEN.txt | 19ypRTUxQ4Qnb5dp7cU7cZ6T4NNchE4cq | DERIVED | Mastneigungen 3,4°/7,6°/2,1°; Fall D (Fassadenanker) fehlt |
| 07.09. | ChatGPT-Seilstatik Böblingen RFEM EVALUIERUNG.txt | 1CuM2hWAqrvobhIufoNFKcISv-AIqxXPm | OBSOLETE | Dublette |
| 07.09. | DeepSeek-Seilstatik Böblingen RFEM EVALUIERUNG.md (1,3 MB) | 1-6fswpXLyLf6kmXtEmJtBBoOF2fUzVSW | DERIVED | **Kanon DeepSeek-Familie**; 5 Base64-Bilder |
| 07.09. | RFEM-Ausdruckprotokoll.pdf (18 S.) | 1LwPEUzBKqWUVV9xXv5mQ3Pjz6eDebrV4 | **PRIMARY** | = U15 |
| 07.09. | RFEM SCREENSHOT01.png | 1WvEjjgF95rRz4e_JEhMFRp5DUuQrLxL3 | **PRIMARY** | = U17 |
| 07.09. | RFEM5_ACTIVE_GEOMETRY_DIAG_20260704_074409.json | 1pSgeP5K7YOfH3yxkfJoQHQSiaaRhpSNI | **PRIMARY** | = U14 |
| 07.09. | Scan-Modell-Knotennummern+Halterungen (.pdf + 3 .jpg) | 1kEmvJdIQdb35mk_q1KOfn4I_rWO4VRgq, 1TvPIstK_Ac67NfyMehTWNBF5q9LacJdS, 1P87B0ygNzA6wCIZ-r1cQ5TeR6dliVsNU, 1xe76NvyvoSyZ3M1WiUyC074zuvmJKk28 | **PRIMARY** | = U16 |
| 07.09. | SYNTHESE – DIE KERNLOGIK DES DENKALGORITHMUS.txt | 1xDWIpeQ3EPBdcFwmAycJV4zMuW4_BD8E | WORKFLOW | Problem-Muster A (Topologie) → WO-003 etc. |
| 07.09. | ChatGPT-Seilstatik Böblingen Recherche (.docx / .txt / .pdf) | 1dqsJM-YkzgBgjumuEcFUxBWNwbKnoDDW / 1TgeWp9fCSneESQXBr7egtCXjbHoNMu3d / 1ZuxcAWA0OrrxqT67LCzDNc9mCvzPykW2 | OBSOLETE | 3 Formate derselben Dublette |
| 07.09. | DeepSeek-SEILSTATIK-CHECKLISTE.md | 18K_sO0L7tfwGGX060fjXPqp5x1u3PV77 | DERIVED | Checkliste; enthält noch „20 doppelte Seile“ → mit Sperrliste lesen |
| 07.09. | NotebookLM Mind Map.png | 1qXE11TnNA5Lh3VY4AfiXER7Y05yGw-7h | WORKFLOW | – |
| 06.09. | DeepSeek-STATUSBERICHT – SEILSTATIK BÖBLINGEN.md | 1OBfU-G0Hp2jS5934O59R8dLVKkpRQwRL | OBSOLETE | Export 2 desselben Chats |
| 06.09. | 26_09_06_ZOTTER_BOEBLINGEN_G3_ENTSCHEIDUNG_FREIGABE__SEILSTATIK.docx.docx | 1ZAltNAK6WEU-IS59OlKGTyjrWpMK-Lmx | **PRIMARY** (Release, Umfang begrenzt) | = U8d; enthält noch Auflage „doppelte Seilgeometrien bereinigen (WO-003)“ → **überholt** durch U14/U15/U17 |
| 06.09. | DeepSeek-Seilstatik Böblingen Bestand.md | 1WhPHI63ve04i4EBvet5qPRo8IU1gKWYH | OBSOLETE | Export 1 desselben Chats; „20 redundante Cable-Stäbe“ widerlegt |

Bilanz: 11 PRIMARY · 12 DERIVED · 10 WORKFLOW · 7 OBSOLETE · 1 CONFLICT · 1 OPEN (ZIP).

## 3 UNTERORDNER `deepseek` (15gRtcOcLeMyaOchzmQFmtKKDNYV29Z1d) — LETZTGÜLTIGER STAND 23.09.

| mtime | Datei | Drive-ID | Klasse | Inhalt |
|---|---|---|---|---|
| 23.09. 15:14 | 26-09-23 rfem screenshot.png | 1w4kSZhxmFz5M_JmHQ6yDj39JehedOpuv | PRIMARY | U12b |
| 23.09. 15:13 | 26_09_23_Ausdruckprotokoll - AP1.pdf | 1k9iqOuSXk8qC9Dz9isbLrmqVt_QxWR_M | PRIMARY | U12a (nicht gelesen) |
| 23.09. 15:09 | 26_09_23_KURZBERICHT_RFEM_VAR-A_LK100_SEILSTATIK_BOEBLINGEN.pdf | 1naQTIh4XhRuE4jaJCzF3nen6nvtU3vZw | **DERIVED-KANON** | 1-Seiter: Berechnung, Grundlagen, Ergebnisse, Erkenntnisse, Stand (100/100/40/0 %) |
| 23.09. 15:07 | 26_09_23_PRUEFBERICHT_SEILSTATIK_BOEBLINGEN_VORLAGE-002.docx | 1FtxONa1pJKRb-saXxoP6YIPvvHB563LQ | **DERIVED-KANON** | Prüfbericht Nr. 01 ENTWURF; Unterlagen U1–U12; Prüfanmerkungen 01-001…017; Fragen F1–F7; Korrekturen B1–B8 zu V001 |
| 23.09. 15:01 | 26_09_23_PRUEFBERICHT_SEILSTATIK_BOEBLINGEN_VORLAGE-001.docx | 1IIPBjyh-d5TPb9TqDY_38R3mZnqsgdQH | **OBSOLETE / CONFLICT** | Gemini-Erstentwurf; 8 Fehler (B1–B8), u. a. unzulässiger Durchhang-Vergleich RL08, „Formfindung“, „Freigabe unter Vorbehalt“ |
| 23.09. | BV Boardinghouse Böblingen _ … (2 Fassadenanker statt Pylone).pdf | 1tA7ObaeBu7zG37Dp5H42JpbwL62sEDaO | PRIMARY | U7a |
| 23.09. | 13_bb_5_L-182-ringleuchtenabspannung (002).pdf | 1rGG7bL_1VJUGa0q80btktJLL0t1nDwSF | PRIMARY | U7d |
| 23.09. | 26_05_20_MAPPING+TRANSFORMATION_GEOM-REFEM.pdf | 1B7peI9xm6aRSDhfkZREauDevgePPXhvi | PRIMARY/DERIVED | U8c |

## 4 ORDNER `SEILNETZ-DOCU` (1lOJGVBVmYx7y2ma82-msv-bkXYbvXWUe, angelegt 24.09. 10:06 UTC) — 15 OBJEKTE

| Datei | Drive-ID | Art | Klasse |
|---|---|---|---|
| 26_09_24_SEILNETZ-BOEB_UNTERLAGENVERZEICHNIS_ONR24005_Rev00.md | 1xTKUTOnAf1lWRg9QPus_iF79LpA73NAn | Datei (10:16) | DERIVED — **Korrekturen §7** |
| 26_09_24_SEILNETZ-BOEB_BEFUND_RFEM-AUSDRUCKPROTOKOLL-V01.md | 1KMTrq7Ix8pPlK84d41s2iAc1qqAQDRsN | Datei (10:19) | DERIVED — fachlich korrekt (LF10–LF63, Balkenstäbe, kein Vorspann-LF); ergänzt Rev00 um U-35 |
| 003-AUSFÜHRUNGSSTATIK_SEILNETZ-BOEBLINGEN.txt (265 KB) | 1UhoT6IUfg7Ep9M5MxyOKXkz5sPqhXtZk (Kopie von 1X2hZwIUCRfKxXf_twUauSD99yTeU9WLI) | Datei | **CONFLICT** — nur Gliederungsreferenz (lt. CLA 18.09. + ChatGPT 11.09.) |
| 26_09_11_SEILSTATIK_BOEBLINGEN_Quellenverzeichnis.docx | 1I7qlePWXJu3PI-V3OFayBi9-MNIzwN3G (Kopie) | Datei | DERIVED |
| ONR_24005_2002_11_01_de.pdf | 1iY_YdPXawBBeVXifUmYW3Wpw3nBOgFfs | Datei | Norm (Gliederungsmuster) |
| 26_07_30_ONR-Regeln_Produktdatenblätter_Baudatenbank.at.md (2×) | 1H6S_0pmSE76nl9J_E6AYJw1EVZ5bKGpQ, 1bFLPT-Ls1tuXbwG5PzSjVr2T7O2AqCBU | Datei, **Dublette** | projektfremd |
| 26_07_31_Register_before_Deploy__THINK_befor_you_RUN__Search_before_generate.txt | 1rxlkg0Mk37guiDjAYP5hXWnhzUBlvKuv (3. Kopie im Drive) | Datei | Governance, projektfremd |
| Verknüpfungen (7, 10:27 UTC): Quellenbefund 18.09. · Deep-Parsing 18.09. · Chatprotokolle 18.09. · CLA-Analyse 18.09. · CODEX Inventar 04.07. · CODEX Knotenupdate 04.07. · QUELLEN-LISTE 11.09. | 1giK9wp9…, 1RbEhUAm…, 1yNZKAhF…, 1VKm6ur_…, 1pFbhZDD…, 1iJU7h__…, 125ktuIJ… | Shortcut | → §2 |
| **dieses Dokument** (Rev01) | 1Bztv0nNthbUdSHqvEizKqA1Rk4wEyWp8 | Datei | DERIVED |

Hinweis: Ordner `FT-TRAEGER-MATRIX` (1PMnJ_Mx6pEUglGLqa-R7awRurYg_x0Zi, Screenshot 11:34) gehört zu einem **anderen Projekt** (Fertigteilträger); RUNLOG.md dort ist nicht der Seilstatik-RUNLOG.

---

## 5 NEUERKENNTNIS-CHECK (Delta gegenüber Quellenbefund 18.09. / Chatprotokolle 22.09.)

| # | Erkenntnis | Quelle | Auswirkung | Status |
|---|---|---|---|---|
| N1 | **Variante A ist gerechnet** (RFEM 5.29, Th. III. O., Newton-Raphson, 5 Laststufen, 0 Meldungen, 307 s): max N RK1 gesamt 17,48 kN (S54) < F_Rd 27,9 kN → η 0,63; Bereich RL06–C21 11,58 kN (S18) → η 0,42; max u(LK100) 2,080 m (Kn 17); Tiefpunkt 1,74 m ≤ 2,50 m | Kurzbericht 23.09. §4 | Nachweise erfüllt, Reserve groß | VORLÄUFIG |
| N2 | **Neue Seillängen (vorläufig)**: S19 L(LK100) 4,925 m → Lsys ≈ 4,732 m · S22 9,576 m → Lsys ≈ 9,383 m (Beschlagabzug 0,193 ± 0,03 m empirisch); Bestandsseile ΔL ≤ 2,1 mm, ΔN ≤ +0,75 kN → rechnerisch wiederverwendbar | Kurzbericht §4, VORLAGE-002 §6 | Bestellgrundlage **nicht** freigegeben (F2, F7, 01-015) | OFFEN |
| N3 | **Ankerkräfte neue Fassadenanker** (RK1, |max| global): ex C06 5,24/4,60/1,07 kN · ex C07 5,75/2,36/0,46 kN; vorzeichenrichtig je LK in `VAR-A_ANKERKRAEFTE_JE_LK.csv` | Kurzbericht §4 | Übergabe an bauseitige Ankerprüfung (IEA) | READY (nach F2) |
| N4 | **CONFLICT Geometriebezug**: VAR-A nutzt 4-Anker-Fit (A05/A06/A13/A14, RMS 0,098 m, Bestandsanker fix); G3 06.09. nutzt 7-Punkt-Starrfit (RMSE 0,62–0,65 m, Anker mitverschoben) → S19/S22 ± 0,4–0,6 m (bei G3-XY: Sehnen ≈ 4,33 / 9,15 m, nicht gerechnet); transformationsfreie Streckenkontrolle stützt VAR-A (1–4 cm zu A05/A06) | VORLAGE-002 01-006, F2 | **Blocker Bestellung** | ENTSCHEIDUNG J. Zotter (Empfehlung A) |
| N5 | **LK220 = 1,35·LF10 + 1,50·LF43 (Erg. 2, 28.04.2015), max N 20,16 kN (η 0,72)** fehlt in 5e und VAR-A; LK214 (Schnee AGE 0,27) ist nicht der Bemessungsfall | 21.09.-Protokoll, VORLAGE-002 01-010 | bemessungsrelevant | F3 (Empfehlung A: beide Modelle ergänzen) |
| N6 | **Seilsteifigkeit**: Modell E 130 GPa (EA 4 940 kN) vs. Bericht Teil II EA 3 420 kN (90 000 × 38) | VORLAGE-002 01-005 | Einfluss auf Lsys → Sensitivität 120/140 GPa | F6 |
| N7 | **Endzustand A05/RL08/S17**: Rückbauplan 2022 nennt Ersatzpylon, Rückverankerung „Merkaden“, „S17 entfällt“; VAR-A setzt Bestand 2015 an | VORLAGE-002 01-011 | ggf. weitere Längen betroffen | F4 (AG-Bestätigung) |
| N8 | **Bestand reproduziert**: RFEM 5.29 ↔ Anh. 25: Δ < 0,02 mm / 0,001 kN im Bereich; einzige Abweichung S53 (schlaff, N ≈ 0, −66 mm) außerhalb Bereich; Anh. 27 (23/34 Seile ± 2 mm), Anh. 30 Pz 14/15 OK | Kurzbericht §5, 01-002 | Solver-Benchmark 2015→2026 geschlossen | ERLEDIGT |
| N9 | **Beschlagmaß-Kette** aus Bestand: Lsys = L(LK100) − 0,151 (Leuchte–Leuchte) / 0,193 (Leuchte–Anker) / 0,285 (Leuchte–Mast); Mastseile −46…67 mm (Kopfplatte) | Kurzbericht §5 | ersetzt frühere Annahme „Spannschloss 156 mm pauschal“ | vorläufig, PFEIFER bestätigt (F7) |
| N10 | **Sv (PFEIFER-Sollast) = N(LK100) des 2015-Modells** (S60 2, S61 3, S62 3, S63 5, S64 4, S81 5 kN), kein Vorspann-LF, kein 15 kN | CLA 18.09., 21.09.-Protokoll, BEFUND V01 24.09. | Initial-State = Knotengeometrie (Strategie S2 implizit) → Koordinaten-Update methodisch konsistent | KONSISTENT (3 unabhängige Quellen) |
| N11 | **Hash-Drift**: V01.rf5 am 07.09. 15:24 neu gespeichert; kein .rf5 trägt mehr den G3-Hash 7DB74920…; byteverschiedene Varianten V01.a / V02 (11.09.) | 21.09.-Protokoll, 01-001 | G3-Bezug formal offen; Rechenbasis ist ohnehin 5e (U6) → **Drift für VAR-A unerheblich**, für Registry zu dokumentieren | DOKU |
| N12 | Mapping **RFEM Member n ↔ Snn** (68 Seile 1–67 + 81) = HIGH_CONFIDENCE_PROVISIONAL; RSTAB-Crosswalk 2014 S01–S30 rekonstruiert (S13↔18, S19↔29, S22↔37 …); Member 35 seit 2015 ohne T/W/Eis-Lasten | 22.09. RUN 05B/05C | S19 = M19 (3006–9), S22 = M22 (10–3007), S63 = M63 (30–3021) bestätigt | HUM-Freigabe offen |
| N13 | **S81**: 2015 Linie 1,002 m, jetzt 1,678 m, weil A05 um 0,685 m verschoben → S81 neu zu fertigen (nicht „Beschlagdifferenz“) | CLA 18.09. | dritte neue Seillänge möglich | prüfen in VAR-A |
| N14 | **Geometerhöhe RL08 (Feb. 2026) ist kein Durchhang-Kontrollwert** (anderer Knoten, Zustand nach Rückbau) | VORLAGE-002 01-016, B2 | VORLAGE-001-Benchmark gestrichen | ERLEDIGT |
| N15 | **Übersehene Primärquellen**: Sprachmemo `26_03_26_Seilstatik.mp3` (167 MB, OneDrive, untranskribiert); historischer Ordner `20190322 - Böblingen` (Drive 1CocDUu542k635YaSMvHWj3F8ybMbeBKz: unterschriebene Prüfberichte, Kordina-Fundamentunterlagen) | 21.09. / 22.09. RUN 03 | Supporting Reference, keine Rechenbasis | OPEN |
| N16 | Vertrags-Scope bestätigt: Fassadenankerprüfung **bauseits**; geschuldet = 3D-Schnittstellenkräfte an 105/106/113/114/3006/3007/3021 | Angebot final 12 000 € | Kap. „Anker“ = nur Übergabe | KONSISTENT |

**Fazit**: Keine neuen Primärdaten seit 23.09.; die einzigen Neuerkenntnisse mit Bemessungsrelevanz sind N4 (XY-Bezug), N5 (LK220), N6 (EA) und N7 (S17). Alle vier sind Entscheidungen, keine Datenlücken.

---

## 6 SPERRLISTE — WIDERLEGTE AUSSAGEN (nicht mehr zitieren)

| Aussage | Widerlegt durch | Korrekt |
|---|---|---|
| „20 redundante/doppelte Cable-Stäbe 2000er↔3000er, vor Rechnung DELETE“ (DeepSeek 06.09., G3 §3, DIRECTORY-LISTINGS, DeepSeek-Checkliste) | U14 (Type 1), U15 §1.17, U17 (Stabtyp Balkenstab, Vouten linear, Gelenke 0/0) | M1001–M1021 = Kreuzstützen/Maste S235, 8,70 m |
| „Aktuelles Modell Z nach oben, Bestand nach unten“ | U15 + Anh. 25: beide „Z positiv nach unten“ | identisch |
| „15 kN Ablängkraft = Vorspannung / LF2“ | U9, N10 | 15 kN = Fertigungsparameter; Sv = N(LK100) |
| „F_Rd = 28,79 kN“ | Bestandsstatik §4.1.1 | F_Rk 46,1 / **F_Rd 27,9 kN** |
| „LF1 EG, LF2 Vorspannung, LF3 Eis 3 cm, LF4–7 Wind, LF8–10 Temp −25/+10/+45“ (ChatGPT 11.09., Rev00 §3, Perplexity) | U15 | LF10, LF20/21/22 (+10/+57/−34 K), LF30–33, LF40/41/43, LF50–53, LF60–63; 21 LK, EK1/EK2 |
| „2006/2007/2021 = reale Punkte mit Höhen 443,15/445,02/444,45“ | U8 | das sind 7004 (RL08), 7101/7102 (C06/C07), 7104 (C21) = 3000er-Anschlussknoten |
| `SURVEY_NODES_2026 = {3006: (5.12, 22.40, −7.10)}` (Codebeispiel 18.09.) | U14 | 3006 = (142,07; 58,49; −0,04) |
| „S17 = 8↔105, S18 = 8↔9“ | L-182-Plan + U14 | S17 = M17 (330–8), S18 = M18 (330–9), S81 = M81 (105–330) |
| „S81: 0,87 m Differenz durch Beschläge/Spannschloss, HOLD“ | CLA 18.09. | A05 um 0,685 m verschoben → S81 neu fertigen |
| „LK214 unterschreitet Prüfauflage 0,60 kN um 32,5 %“ | Erg. 2 | maßgebend LK220 (20,16 kN), nicht LK214 |
| „Transformation −9,1° (Mai)“ | Kurzbericht §5 | falsch; VAR-A-Trafo siehe U8e |
| „Benchmark LK100 = EG + Vorspannung; Durchhang RL08 2,10 m ↔ uz Kn 17 2,085 m (< 1 %)“ (VORLAGE-001) | B1, B2 | LK100 = EG + T+10 (Beiwerte 1,0); Vergleich unzulässig |
| „Solver-Differenz duz 50,4 mm / dN 0,25 kN“ (VORLAGE-001) | B3 | nur S53 außerhalb Bereich; im Bereich < 0,02 mm |
| „Seil-Formfindung“ (VORLAGE-001) | B7 | keine Formfindung; Anfangszustand = Knotengeometrie |
| „RUN 1B HOLD wegen fehlender Drive-File-IDs“ | CLA 18.09. | Dateien liegen lokal gehasht vor; Blocker = Auswahl CURRENT-Binary (→ gelöst: 5e) |
| „RFEM 6 / gRPC / MCP als Rechenpfad“ | CLA 18.09. | Projekt = RFEM 5 (Modell, COM, Lizenz) |
| „Vermessung Juni 2026“ (Deep-Parsing-Prompt) | U8, BöblingenMessung.docx | Messung 11./13.02.2026 |

---

## 7 KORREKTUREN ZU `UNTERLAGENVERZEICHNIS_ONR24005_Rev00` (24.09. 10:16 UTC) UND `BEFUND V01` (10:19 UTC)

| # | Rev00 / BEFUND | Befund | Korrektur (→ Rev01 dieses Dokument) |
|---|---|---|---|
| K1 | Rev00 U-13: „13bb_ausführungsstatik_1.rf5 (Bestandsmodell)“ | VORLAGE-002 01-001/01-002: Berichtsmodell = **5e** (`…150328_5e.rf5`, BD77CF83…) | U6 = 5e; 13bb_ausführungsstatik_1 = Vorläufer (U6a) |
| K2 | Rev00 U-20: „Vermesserdaten Blessing 05/2026“ | Messung 11./13.02.2026, Lieferung 20.04.2026, Bestätigung 21.05.2026 | Datum korrigiert (U8) |
| K3 | Rev00 §3 Lastmodell LF1–LF10 | BEFUND V01 selbst: „Abschnitt 3 Rev00 ist DAMIT ÜBERHOLT“ | LF10–LF63 lt. U15 (§6 Sperrliste) |
| K4 | Rev00 U-15: „Probebelastungsprotokolle Seile + Anker 03/2026“ | in keiner gelesenen Primärquelle belegt; bekannt sind Probebelastungen Mercaden 2014 (IEA) | Status → OPEN/unbelegt, bis Datei + Datum vorliegen |
| K5 | Rev00 U-30/U-31: V01.rf5 als „PRIMARY · Source-Freeze“, V02 als Arbeitskopie | 01-001: V01/V01.a = 5e + 20 Hilfsknoten + Knotenänderungen ohne Save-Protokoll → **nicht Rechenbasis**; Hash-Drift (N11) | V01 = Referenz/Archiv; Rechenbasis = U6 → U10/U11 (Sandbox 23.09.) |
| K6 | Rev00 fehlt gesamter `deepseek`-Stand 23.09. (VAR-A, VORLAGE-002, AP1, Kurzbericht) | letztgültige Rechenstände nicht erfasst | §1.5 U10–U12b ergänzt |
| K7 | Rev00 U-01 „Anfrage … OPEN“ | Anfrage liegt vor: U7a (06.03.2026, Drive 1tA7ObaeBu…) | geschlossen |
| K8 | BEFUND V01 §5: LASTEN+Kombi-EXCEL2RFEM.xlsx „DERIVED“ | bestätigt (eigene LF-Nummerierung, `#NAME?`) | übernommen |
| K9 | Rev00 P-01 „RFEM5 Build OPEN“ | Kurzbericht: **RFEM 5.29.01.161059** | geschlossen |

---

## 8 OFFENE ENTSCHEIDUNGEN + GAPS (Gate vor Bestellfreigabe)

Entscheidungen J. Zotter (VORLAGE-002 Anhang A, ★ = Empfehlung Prüfstand):

| F | Frage | Optionen | Empfehlung |
|---|---|---|---|
| F1 | Rolle des Berichts | A interner Vier-Augen-Kontrollbericht im werkraum-Format · B externer Prüfingenieur (AG beauftragt) · C nur prüffähige Doku | ★ A |
| F2 | Geometriebezug neue Anker (01-006) | A VAR-A (Bestandsanker fix) + Geometer bestätigt Strecken zu A05/A06 · B G3-XY beibehalten, neu rechnen · C beide rechnen | ★ A |
| F3 | LK220 aufnehmen (01-010) | A in Bestand + VAR-A · B nur VAR-A · C nicht (begründen) | ★ A |
| F4 | Endzustand A05/RL08/S17 (01-011) | A Bestand 2015 (AG bestätigt) · B Bauphase 2022 · C beide | ★ A |
| F5 | Format/Ablage | A .docx im Projektordner, Versionen _VORLAGE-00x · B Google Docs · C Claude Docs/SharePoint | ★ A |
| F6 | Seilsteifigkeit (01-005) | A E 130 GPa + Sensitivität 120/140 · B EA 3 420 kN · C PFEIFER bestätigen | ★ A |
| F7 | Beschlagmaß Lsys (01-009) | A empirisch 0,193 m, PFEIFER bestätigt · B Zeichnung abwarten · C Aufmaß vor Ort | ★ A |

Noch vorzulegen (VORLAGE-002 §7): Geometer-Bestätigung 7101/7102 = Lochmitte neue Anker + Strecken zu A05/A06 · Ankerplatten-/Gabelkopfdetail (PFEIFER-Beschlagmaß) · AG-Bestätigung Endzustand S17 · Leuchtendatenblatt + Geländehöhen (lichte Höhe ≥ 5,00 m Feuerwehr, 01-014) · Zustandsbefund Bestandsseile/Beschläge (01-015) · C21-Abweichung 0,60 m (01-008) · Kontrolle Rechenstände durch Wiederöffnen (01-017) · ETA-11/0160 aktuelle Rev · OCR Datenblatt PE.

Registry-Gaps (Quellenbefund §12, Stand nach 23.09.): geschlossen = OLD MODEL → OLD RESULTS (N8), NEW CALCULATION → CABLE FORCES (N1), → ANCHOR REACTIONS (N3); offen = LENGTH CONTRACT (F2/F7), QA (01-017), HUMAN RELEASE.

---

## 9 LESEUMFANG UND GRENZEN DIESES LAUFS

- **Vollständig gelesen (22)**: alle 10 Screenshots; VORLAGE-001, VORLAGE-002, Kurzbericht 23.09., G3-Entscheidung, Anfrage-PDF 06.03.2026, CLA-Analyse 18.09., CODEX-Inventar 04.07., Quellenverzeichnis 11.09. (docx), Deep-Parsing-Prompt 18.09., LASTEN-Excel, Unterlagenverzeichnis Rev00, BEFUND V01, Ordnerlistings (3), Metadaten aller 41 + 8 + 15 Objekte.
- **Nur strukturell/auszugsweise gelesen (5)**: Quellenbefund 18.09. (§1–3, 6, 8, 12, 13 Kern), Quellen-Liste 11.09. (Kopf + Gliederung), Chatprotokolle 21.09. (§1–3, Schluss) und 22.09. ×2 (alle TL;DR-Blöcke + Work-Order).
- **Nicht gelesen**: ZIP 22.09. (58,6 MB), Ausdruckprotokoll AP1 23.09. (PDF 2,7 MB), RFEM-Ausdruckprotokoll 07.09. (über BEFUND V01 abgedeckt), K15-PDF (über Quellenbefund §8 abgedeckt), Sovereign-PDFs, 003-AUSFÜHRUNGSSTATIK (265 KB, über CLA/ChatGPT-Bewertung abgedeckt), DeepSeek-RFEM-EVALUIERUNG (1,3 MB), Scan-PDF/JPG, ONR-PDF, Register_before_Deploy.
- **Kein Zugriff**: lokale Sandbox `SANDBOX_RFEM5_COM_20260923_1356` (U10–U12, Hashes nur wie in VORLAGE-002 zitiert), Dropbox/SharePoint/Gmail in diesem Lauf nicht abgefragt.
- Keine RFEM-Rechnung, keine Änderung an Drive-Dateien außer Upload dieses Dokuments.

`LOG: Repo julianzotter/julianzotter, Branch claude/seilstatik-doku-overview-rc0lpt, docs/ · Drive-Kopie in SEILNETZ-DOCU · RUNLOG-Zeile SEILNETZ ausstehend (kein Seilstatik-RUNLOG im Drive gefunden)`
