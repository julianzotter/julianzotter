# QUELLENLOG — RF6 (Modell 001, Migration RF5 → RF6, Exporte, Läufe)

| Feld | Wert |
|---|---|
| Datei | `00_Quellenlog/RF6/26_10_06_ID-03_Quellenlog_RF6.md` |
| Rolle | ID-03 (Claude) · Pflege: ID01 / Codex (lokal) |
| Status | CANDIDATE Rev1 (06.10. 21:10 UTC) · **kein RF6-Rechenlauf registriert** · Rev1 = Einarbeitung ADDENDUM Rev0 + Uploads WORKING_CALC.rf6bak / TABLE-EXPORT.xml |
| Software | Modellformat RFEM 6.12.0008 · **Server beim Export 6.13.0001** (ADDENDUM §3) · Client dlubal.api 2.12.8 (Server verlangt 2.13.1) · API-II gRPC 127.0.0.1:9000 |
| Kanon | BEFUND RF5/RF6/VAR-A Rev0 §2 · TEILABGLEICH summary.json · MODELL-DIFF QS14 Rev0 |

## 1 Modelle und Hashes

| M-ID | Datei | Ort | Datum | SHA-256 | Inhalt | Rolle | Status |
|---|---|---|---|---|---|---|---|
| M1 | 26_10_06_SEILSTATIK-MODELL-001.rf6 (2 309 460 B) | Drive 119Unwcdhj5MEfUiOmmlR59FlIh2-PaYt · lokal BENCHMARK-SEILSTATIK | 06.10.2026 10:40 | 1286822edbe6c738933e401619b5cd2df0df032b1c62f3306be19c28573db3cd | 106 Kn, 105 Linien, 105 Stäbe, 17 QS, 14 Mat, 19 LF, 21 LK; = V01 topologisch 1:1 | **Original RF6, nicht ändern** | VERIFIED (Hash lt. summary.json) |
| M1b | 26_10_06_SEILSTATIK-MODELL-001.rf6bak (2 309 257 B) | Drive 19mrwOyWN0hMNLaR3SiWS4JwZVUQMAtcH | 06.10.2026 | – | RFEM-Backup | Archiv | FOUND |
| M2 | 01-Gesamtmodell-Seilabspannung_V01.rf5 (11 567 104 B) | EXPORT\…\02 RFEM-Modelle\RFEM-MODELL-Gesamt\ | 04.07./07.09.2026 | 47751311e24e993450e891bcd61feba2c3dff12d26cdc6d2f919a0e23b14db36 (≠ Freeze 7DB74920…) | Importquelle für M1 | Importbasis, nicht Rechenbasis | CONFLICT (Hash-Drift N11) |
| M3 | BOEB_BESTAND-5e_NEUBERECHNET_RFEM529_20260923_1437.rf5 | SANDBOX\05_RECHENSTAND | 23.09.2026 | 317D78D7AF7837F402928221C504F06B48AF6153BF1B60C53DE440A109FE4E12 | 86 Kn / 88 Stäbe / 19 LF / 21 LK | **Kalibrierreferenz** (u_Kn17 2,085 m, N_S54 17,47 kN) | VERIFIED 23.09.; mtime 30.09. → Hash neu prüfen |
| M4 | BOEB_VAR-A_…_VORLAEUFIG_20260923_1437.rf5 | SANDBOX\05_RECHENSTAND | 23.09.2026 | EAB6A5B1A31D4C14746ECBDA27480D8D514FD8F10F30B208AE4E4C80E42EC970 | 84 Kn / 86 Stäbe | VAR-A Zielgeometrie | VERIFIED 23.09. |
| M4b | …_1437.1.rf5 (48 619 520 B) | SANDBOX\05_RECHENSTAND | 30.09.2026 | – | unbekannt | Konfliktkopie | **SPERRLISTE bis Hash + Wiederöffnung** |
| M5 | 26_10_06_SEILSTATIK-MODELL-001_WORKING_CALC.rf6 (.rf6bak-Upload 2 360 116 B) | lokal BENCHMARK-SEILSTATIK; Upload Chat 06.10. | gespeichert 06.10. (format.txt: RFEM6 6.13.0001, ts 1791320603) | .rf6bak: 903093dd0274826f3316cd21f9178cc78553369f500cfe06cd8eb230c278e327 (.rf6 selbst nicht hochgeladen) | model.db read-only: **106 Kn / 105 Linien / 105 Stäbe / 17 QS / 14 Mat / 19 LF / 21 LK / 2 RK / 27 NodalSupport an 35 Knoten**; QS-14-Stäbe 158, 178, 179–193 **noch vorhanden**; keine Ergebnisse (results.xml leer) | Arbeitskopie = 1:1-Kopie von M1 | P1 erledigt · **P2 (QS-14 löschen) offen** · A = 0,38 cm² lt. ADDENDUM B3 |

## 2 Exporte, Protokolle, Skripte

| E-ID | Datei | Drive-ID | Datum | Inhalt | Status |
|---|---|---|---|---|---|
| E1 | 26_10_06_RF6-AUSDRUCKPROTOKOLL-001.pdf (14,8 MB) | 1flvOcGTPA3QKmNvGgfFwhMWzta90ZZU0 | 06.10. 10:42 | RF6-Ausdruck M1 | nicht gelesen |
| E2 | 26_10_06_RF5-AUSDRUCKPROTOKOLL_Gesamtmodell-V1-WORKING(mit-angepasster-Geometrie).pdf | 1QAhMcR2hvvTk3Wt3rS7955cjfJhARaOK | 06.10. 11:20 | RF5-Ausdruck V01 (20 S.): Lager §1.7, QS §1.13, LF, LK | gelesen (BEFUND Rev0) |
| E3 | 26_10_06_ID-03_SEILSTATIK_RF5_RF6_TEILABGLEICH.zip | 1o_GYZlL59GwJtw6_RfSLPsusJGep5PwL | 06.10. 11:24 | nodes/lines/members.csv, summary.json, compare_models.py, sources/* | gelesen |
| E4 | 26_10_06_ID-03-rf6_model_export.py | 1Yefs-aU3ElvuKy_mWQiUyFCcyuAE1dKq | 06.10. 16:35 | read-only Export model.db → CSV + manifest.json (kein API-Lauf) | getestet mit Testmodell |
| E5 | 26_10_06_ID-03-RFEM6_MCP_Bridge_Extended.py v1.0.0 | 10briGfFIdYYBesyAK3m2mT5sZQXXtFYD | 06.10. 11:00 | API-II-Bridge: `--check`, `--export DIR` (INPUT_MODELL.txt + RESULTATE/*.csv + MANIFEST.json), MCP-Tools read-only | lokal zu testen |
| E6a | 26_10_06_ID-03-RF6-Ergebnis-Export.py (Claude) | 1-c68iAHk3KY3_ANZihVM1AL_z0Td_Zf0 (5 375 B) | 06.10. 17:45 UTC | Wrapper um E5 `execute(raw_results)`, Enum per Teilstring, Ausgaben `01_…csv` + API_Log.json | CANDIDATE, ungetestet |
| E6b | 26_10_06_ID-03-RF6-Ergebnis-Export.py (**lokal gelaufene Fassung**) | lokal G:\…\BENCHMARK-SEILSTATIK, nicht in Drive | Lauf 06.10. 18:12–18:13 UTC | lt. ADDENDUM §3/K3/K6: ruft dlubal.api direkt, Enum `STATIC_ANALYSIS_NODES_DEFORMATIONS_TABLE` (existiert nicht), Ausgabenamen `26.01.006_b_rf6_…` → **Namenskollision mit E6a, anderes Skript** | Lauf: API OK, GUID 798c4012-d8c4-4a7e-a712-68bc4f9121e5, „No results available“, keine CSV |
| E9 | 26_10_06_ID-03-RFEM6-TABLE-EXPORT.xml (1 094 322 B) | Upload Chat 06.10. | 06.10. | RFEM-Tabellenexport von WORKING_CALC: nur Modell (775 Items), **keine Ergebnisse**, kein Stab deaktiviert; SHA 412c4088daf320c18dda83aa538250353fd0e8e9636b0f072d4f50e575ff6c9f | FOUND |
| E10 | 26_10_06_ID-03_ADDENDUM_RF6_BASELINE_BEFUND_Rev0.md | Upload Chat 06.10. (Ablage BENCHMARK-SEILSTATIK lt. LOG) | 06.10. | Befunde B1–B12 aus M1-model.db, Korrekturen K1–K8, Aktionen P1–P6 | DERIVED-KANON für RF6-Stand |
| E11 | 26_10_06_WhatsApp-Chat.zip (Meta-AI-Dialog, 614 KB) | Upload Chat 06.10. | 06.10. | NEXUS-Staging-Dialog; Seilstatik-Zahlen darin (SEIL_01.json L 7,8 m, q 17,9, EA 15 000, „Vorspann 10“, „H = 92 kN“, „LK220 103 kN“) sind frei generiert, ohne Quelle | **SPERRLISTE (S0)** |
| E7 | 26_10_06_ID-03-RF6_GEOMETRIE_PATCH_VARA_Rev0.json | 1TdRcnL3SEARibNJRcGZKOXBhzXmLa-zB | 06.10. 16:35 | Patch-Vorschlag für M5 (6 Knoten, Stäbe/Knoten löschen, Lager 3006/3007) | VORSCHLAG, nicht angewendet |
| E8 | Screenshots RF6 (LF31/43/50/60, QS-14-Fehler, Dateiname, Ausdruck) | 1APAuBvcVwyGJ…, 1ggnX3KWyF6X4…, u. a. | 06.10. | Sichtbelege Import | FOUND |

## 3 Run-Register RF6 (fail-closed: ohne Zeile kein Ergebnis)

| RUN-ID | Modell (Hash) | Datum | Solver | Loadings | Ergebnisdateien (SHA-256) | Kalibrierung Δ | Status |
|---|---|---|---|---|---|---|---|
| RUN-RF6-000 | M1 1286822e… / M5 | Exportversuch 06.10. 18:12 UTC (E6b) | – (nicht gerechnet) | 21 LK abgefragt | keine (No results available) | – | **NICHT ERFÜLLT** · M1 wegen QS-14-Fehler nicht rechenbar (ADDENDUM K7) |
| RUN-RF6-001 | M5 (–) | – | Th. III. O., Newton-Raphson, g = 10,00 m/s² (E7 offen) | LK100, RK1, LK220 | – | Soll: u_Kn17 2,085 m, N_S54 17,47 kN (Toleranz E8 offen) | geplant |

## 3a Korrekturen aus ADDENDUM Rev0 (übernommen)

| K | Korrektur | Wirkung hier |
|---|---|---|
| K1 | Hilfsstäbe = 158, **178**, 179–193 (nicht 159; 159 = Linie von Stab 178) | MODELL-DIFF Rev0 §1 war bereits korrekt (Stab 178, Linie 159) |
| K2 | Server 6.13.0001, Format 6.12.0008; Speichern in 6.13 ändert Hash | M5 trägt format.txt „RFEM6 6.13.0001“ → M1-Hash gilt nicht für M5 |
| K3/K6 | gelaufenes Skript ≠ Wrapper, Ausgabenamen abweichend | als E6b getrennt geführt; vor nächstem Lauf Datei auf G: mit Drive-Fassung E6a vergleichen (Hash) |
| K4 | A = 0,38 cm² in M1 belegt (B3) | Behauptung 0,02 cm² (ANWEIDUNG.docx) widerlegt; Delta-Matrix Spalte „A = ?“ → 0,38 |
| K5 | RK1/RK2 im Export fehlen | E6a exportiert je Kategorie alle Loadings der Tabelle; ob RK enthalten, erst nach erstem erfolgreichen Lauf belegt |
| K7 | Baseline = M1 + QS-14-Bereinigung ohne VAR-A-Patch | RUN-RF6-000 neu definiert: Modell = M5 nach P2, Geometrie V01 |
| K8 | Bezugstemperatur: Material 20 °C, dT +10/+57/−34 K | E5 präzisieren: Frage ist dT-Basis (T_Montage) vs. PFEIFER T₀ 10 °C, nicht „0 °C“ |

## 4 Offene Entscheidungen mit RF6-Wirkung (aus BEFUND Rev0 §8)

E1 Geometriebasis VAR-A statt G3 · E2 Maste 1006/1007 entfallen, 3006/3007 gelenkig · E3 C21 Fall A/B · E4 Kombinatorik EN 1990 vs. Bestand · E5 Bezugstemperatur 0 °C vs. T₀ 10 °C · E6 Seil 35 Stablasten · E7 g 10,00 → 9,81 · E8 Kalibriertoleranz.

## 5 Nächste Schritte RF6 (Stand 06.10. 21:10 UTC)

1. P2 in M5 ausführen (17 Stäbe, 20 Knoten, QS 14–17 löschen; Kontrolle 86 Kn / 88 Stäbe), speichern, SHA-256 der .rf6 notieren.
2. `pip install --upgrade dlubal.api==2.13.1` (Server 6.13.0001), dann `--check`.
3. Enum-Liste ausgeben: `python -c "from dlubal.api import rfem; print([k for k in rfem.results.ResultsType.keys() if 'NODES' in k])"` → Verformungs-Kategorie belegen.
4. Rechenlauf LK100/RK1 in M5 (Th. III. O.), danach E6a ausführen; API_Log.json + CSV-Hashes in §3 eintragen.
5. Kalibrierung K1–K7 der Delta-Matrix nur gegen ein Modell mit Bestand-5e-Geometrie (O1); M5 trägt V01-Geometrie → zusätzliche Arbeitskopie `…_BESTAND5E_CALC.rf6` oder Entscheidung E1 vorziehen.

## 6 Pfadreferenzen (ID01, 07.10.2026) und Ablage der Loop-Dokumente

| Ref | Ort | Drive-ID / Pfad | Regel |
|---|---|---|---|
| P1 | Hauptordner Projekt | `_SEILSTATIK_BOEBLINGEN` · 13EeKXWMpoN-FrH1oPFcOsPuK_9BqfmA3 | Projektquellen (Bestandsstatik, Vermesser, Prüfberichte) |
| P2 | Projekt-Arbeitsverzeichnis Adaptierung | `26-03-18_Boeb_Adaptierung` · 1tA6hbxW3SqxyGLPY8EP1J0ESmsVuMYi5 | Arbeitsstand Ergänzung 4 |
| P3 | Benchmark-Ordner (Drive) | `_INDEX_LNK/BENCHMARK-SEILSTATIK` · 1ZpE9ym5UVEJuiLml0YKXDQl8Qk878sZl | enthält 00_Quellenlog (1kbe5F856ZwxMRybU8ouCpgefjK-Eyck2) |
| P4 | Lokal (Drive für Desktop) | `G:\Meine Ablage\_INDEX_LNK\BENCHMARK-SEILSTATIK\` | Arbeitskopien, nie M1 beschreiben |
| P5 | Skripte lokal | `…\BENCHMARK-SEILSTATIK\Skripte\` | nur Skripte aus Repo `tools/` (Hash im Quellenlog); Sperrliste Rev0 gilt |
| P6 | Ergebnis-/Exportverzeichnis lokal | `…\BENCHMARK-SEILSTATIK\Daten\results\` | E6a-Exporte → zusätzlich `00_Quellenlog/API_Auszuege/RF6_EXPORT_<stamp>_<RUN-ID>/`; schreibgeschützt nach Lauf |

Loop-Dokumente (07.10.): Loop 1 Fremddaten „Fall B“ Drive 16nR2N7F5OWlQpJ4vP6H8aDbXkLxbm2Rj · Loop 2 Docx FERTIGSTELLUNG + Eingabetabellen Drive 1QZJxf7BR8e9Jud-O0SrBJko2Pw8bq4Bt (Repo `docs/26_10_07_ID-03_DELTA-REFINEMENT_LOOP2_FERTIGSTELLUNG-DOCX_Rev0.md`) · Eingabedaten v0.1 Zip 1-0r03VNC5jV_xm8rALgGfDS40MFn9vs7.

### 6a Drive-Ordnerstruktur BENCHMARK-SEILSTATIK (angelegt 07.10. 09:04–09:07 UTC, spiegelt Paket v0.1 Stand cdc6acf)

| Pfad (Drive = G:\Meine Ablage\_INDEX_LNK\BENCHMARK-SEILSTATIK\) | Drive-ID |
|---|---|
| README_PAKET.md | 1ZljCyNMIWZqwUMvNj5jTy0BR8UMmqojp |
| Skripte/ | 1iZNO0RFjfYXLS6clwA0vNYyWKuHkvpCF |
| Skripte/_GESPERRT_FREMDSKRIPTE_CHATFASSUNG/ | 1ewcBd4x-NQ1mTVsVv8ebeh90R9swpbzx |
| Daten/ | 1ncwXXd0sqislDw8BHWB8e2P3_wMpL5jd |
| Daten/input/ | 1jvEhVlmHp8zZzjNuhDqPZBveV8ZzCnn7 |
| Daten/input/EINGABEDATEN_RF6_v0.1/ | 1ZPr8x8H81DXt6qQAHICKe8huZ1-nMmuO |
| Daten/input/EINGABEDATEN_RF6_v0.1/A_BESTAND/ | 1wsZYY6q54b7bhLuxcCzQrWPUEgV5hVPo |
| Daten/input/EINGABEDATEN_RF6_v0.1/B_VARA/ | 1c9Av0mZ4gqeb4ApPBaoPM1MFZkBVAMIK |
| Daten/results/ | 1x2ACcb2u4fQ1-B9mUCwkFRyohF39Rkt6 |
| Logs/ | 1jwh1tfHHnEEiaEKgtU7Zrjfbcz7Q3k6n |
| Befunde/ | 1tSNvcVz-dGZEZXX5bH-qUNX7tzs5F6PA |
| 00_Quellenlog/ (bestehend) | 1kbe5F856ZwxMRybU8ouCpgefjK-Eyck2 |

Weitere Dateien 07.10.: Gegencheck-Antwort 1qRkkAnHRBxzBbpCpNE2Aw-NTKY9RGKeE (RF6-Ordner) · Topologie-Gate C06/C07 (Befunde/) · ZIP `SEILSTATIK_BOEBLINGEN_ERG4_BENCHMARK-SEILSTATIK_v0.1.zip` (50 Dateien, SHA-256 98f39df608a97b4c…) nur im Repo und als Session-Dateiversand; Drive-Connector lädt keine Binärdateien dieser Größe. Die Ordnerstruktur auf Drive ersetzt das ZIP für die lokale Synchronisation.

### 6b Skill-Arbeitsauftrag (07.10. 12:25 UTC, Entscheidung ID01 „RF5 → CSV → RF6, zwei Haltepunkte, Vergleich“)

| Datei | Repo | Drive (BENCHMARK-SEILSTATIK/SKILL, Ordner 1F1xbTixsIAZ4qnTuUuPW0PIdNmvsDu1_) |
|---|---|---|
| SKILL.md (aktiv als `seilstatik-rf5-rf6-neuaufbau`) | `.claude/skills/seilstatik-rf5-rf6-neuaufbau/SKILL.md`, Kopie `docs/26_10_07_ID-03_SKILL_…_Rev0.md` | Ordner SKILL (jeweils aktuelle Datei gleichen Namens) |
| WEGWEISER.md | `.claude/skills/seilstatik-rf5-rf6-neuaufbau/WEGWEISER.md`, Kopie `docs/26_10_07_ID-03_WEGWEISER_…_Rev0.md` | Ordner SKILL (jeweils aktuelle Datei gleichen Namens) |

### 6c Entscheidung Referenzmodell (ID01, 07.10.2026)

Das RF5-Gesamtmodell `13bb_ausführungsstatik_1.rf5` (U6a) ist als Grundlage mit P. Kneidinger vereinbart und damit Referenz für Eingabedaten (CSV v0.2) und Vergleichsergebnisse. Berichtsmodell 5e (U6, BD77CF83…) nur Querkontrolle. Offen: welche der zwei Fassungen (54 054 912 / 54 075 392 B), SHA-256, Datum der Vereinbarung. Skill Rev0 Schritt 1/2 angepasst (Drive-Kopien ersetzt).

### 6d Befund 13bb vs. 5e (lokale Session RFEM 5.29.01/COM, 08.10.2026, nur lesend) — Konsequenz für Referenzmodell

| Modell | Pfad (lokal) | Datum | Bytes | SHA-256 | Status |
|---|---|---|---|---|---|
| 13bb 2015 (**Referenz**) | `00_BESTAND_KOPIE\RFEM5_2015\13bb_ausführungsstatik_1.rf5` | 01.04.2015 | 54 054 912 | 73242E1346AB6556… | = Original EXPORT\…\statistik-unterlagen-150325 · VERIFIED |
| 13bb (verändert) | `EXPORT\…\04 Berechnung Gesamtsystem\13bb_ausführungsstatik_1.rf5` | 06.10.2026 19:39 | 54 075 392 | C88F779233B26ED4… | **nicht Bestand**, nicht verwenden |
| 5e | `00_BESTAND_KOPIE\RFEM5_2015\leuchtenabspannung_gesamt_nachaufmassgeometer_150328_5e.rf5` | 14.04.2015 | 69 345 280 | BD77CF839C98210E… | = Original (U6) · VERIFIED |

Eingabevergleich (alle COM-Tabellen): Materialien/QS/Stäbe/Lager 6/13/88/27 identisch; Knoten 86 / Linien 88 identisch bis auf vertauschte Nummern 16↔17 (Linien 44, 46–49 entsprechend); Rechenparameter identisch. Lasten: 13bb unvollständig (Kabel 2,0 statt 1,48 N/m; Leuchten-Wind/Eis/Schnee fehlen; LF33 −0,8 kN Fehler); 13bb nur 16 LK (CO100–213), 1 RK; 5e 21 LK, 2 RK = Bestandsbericht 17.04.2015. Ergebnisse 2015: 5e max N GZT 17,50 kN (CO207) = Bericht (< 20,45 kN); u_max LK100 2 079/2 080 mm; 13bb Anker 111 / Stab 56 lokal unterschätzt, LF43 = 0.

**Konsequenz (Vorschlag D2a, Bestätigung ID01):** Geometrie/System 13bb ≡ 5e → Vereinbarung Kneidinger ist mit 5e-Geometrie erfüllt; Lasten, LK, RK aus 5e (= Bericht). Damit ist `EINGABEDATEN_RF6_v0.1` (aus 5e-Export U10, geprüft gegen diesen Befund: 86/88/6/13/27, 19 LF, 21 LK, Kabel 0,00148 kN/m, Leuchtenlasten 0,021/0,065/0,029/1,5/0,0235/0,0106 kN) der gültige Modell-A-Datensatz; ein COM-Export aus 13bb ist für die Geometrie nicht mehr nötig. Gates V1/V2 erledigt, V3 (Vereinbarungsdatum) offen. Knotennummern 16/17: v0.1 folgt 5e (Kn 16 = 205,154/113,761/−0,400; Kn 17 = 203,032/130,830/−0,600); Teilmodell enthält 16/17 nicht. Lokale Befunddateien (`09_VERGLEICH_13bb_vs_5e_20261008\`, `00_BESTAND_KOPIE\RFEM5_2015\<modell>\*.csv`, `04_SKRIPTE_REPRO\*.py`) nach `BENCHMARK-SEILSTATIK\00_Quellenlog\RF6\` bzw. `Daten\input\` kopieren und hier mit Hash eintragen.
