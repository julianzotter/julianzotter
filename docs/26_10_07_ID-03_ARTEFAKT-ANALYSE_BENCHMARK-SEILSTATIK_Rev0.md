# ARTEFAKT-ANALYSE Drive-Ordner BENCHMARK-SEILSTATIK — Anweisungen, Datensätze, Konflikte — Rev0

| Feld | Wert |
|---|---|
| Stand | 07.10.2026 13:30 UTC · ID-03 · vollständige Root-Liste (5 Seiten) + Unterordner SKILL, Befunde, Daten, 00_Quellenlog |
| Zweck | Welche Skill-/Wegweiser-/Begleitschreiben-Dokumente existieren, von wem, mit welchem Stand, wo sie sich widersprechen, was verbindlich ist |
| Ergebnis | 7 Anweisungs-Familien, 4 davon zum Teilmodell. Drei unabhängige Teilmodell-Herleitungen stimmen überein (Schnittknoten 8, 16/15 → 14/13); eine weicht ab (Schnitt 6/11/30). Verbindlich: Ordner SKILL (Repo-Skill), ergänzt um drei Übernahmen (§5). |

## 1 Anweisungsdokumente (Skill / Wegweiser / Begleitschreiben / Runbook)

| # | Datei (Drive-ID) | Zeit UTC | Label | Kern | Status |
|---|---|---|---|---|---|
| A1 | SKILL/`26_10_07_ID-03_SKILL_seilstatik-rf5-rf6-neuaufbau_Rev0.md` (1nqE8i4r…) + WEGWEISER (1hf9bJaV…) + Befunde/`…BEGLEITSCHREIBEN-NOTIZEN_ERG4_Rev0.md` (1ErcDZhi…) | 12:51–12:53 | ID-03 (diese Session, Repo `.claude/skills/…`, aktiv) | Entscheidung ID01, 10 Schritte, Schnittstellen, Teilmodell T §6 (T01–T11), CSV-Vertrag §5, Allowlist, Abgleich mit A2 | **verbindlich**, CANDIDATE bis Rechenlauf |
| A2 | `26_10_07_1425_ID-03_RF5-CSV-RFEM6-SEILSTATIK_SKILL.md` / `_WEGWEISER.md` (1pIi5f7O…, 1oSuh5XO…; Kopien in _SEILSTATIK_BOEBLINGEN) | 12:30 | „ID-03", englisch, Fremdassistent | G0–G10, Allowlist, Stop-Conditions, SI/Komma-CSV | in A1 §8 abgeglichen; Vorlage |
| A3 | `26_10_07_ID-Deep_SKILL-RF6-CABLE-TEILMODELL-001b.md` (1UV5e_a5…), `…WEGWEISER-…-001b.md` (1mM57dYa…), `…BEGLEITSCHREIBEN-001b.md` (1B2hSHCJ…), Sammeldatei `…RF6-Seilstatik Teilmodell-Migration.md` (1NA7uzOD…), Vorfassung `…-001.md` (1pCMlVrI…) | 13:14–13:22 | ID-Deep (NEXUS-RF6-CABLE) | übernimmt Teilmodell aus A1 1:1 (16/15, 14/13, Kn 8, S16/S23 weg, A1/A2-Annahmen), ergänzt V1–V8 Vorbedingungen, Gates T-G0…GATE-6, Toleranzvertrag, T00–T16, Run-Envelope, Begleitschreiben-Formular | konsistent mit A1; eigene Regel „V1–V5 offen → BLOCK" trifft derzeit zu |
| A4 | `26_10_07_125238_UTC_ID-03_TEILMODELL_V1.1_SKILL.md` (1sVSnHJW…) / `_WEGWEISER.md` (1S-PTUTC…) | 12:52 | „ID-03", Fremdassistent | **anderer Schnitt:** 14 Knoten / 13 Seile ohne Mast 1021, Schnittknoten 6/11/30, S16/S23 drin, S63 weg; 6-DOF je Schnittknoten einzeln freizugeben; „handschriftliches Z = +0,451 m"; neue Quell-Links (Bestandsdruck 1e5FMUicX…, Halterungsdoku 18cy-J7Qf…, Gesamtstatik 1K-efzJMN…) | abweichend, siehe §2 |
| A5 | `26_10_07_1107_ID-03_CHECKLISTE_RFEM6-SEILSTATIK-BOEBLINGEN_V1.0.md` (1BG244f0…) | 09:08 | „ID-03", Fremdassistent | G0–G7 für Rechenlauf am Gesamtmodell M1 (106/105, GUID e0726678…, RFEM 6.12.0008) | gültig als Prüf-Checkliste, bezieht sich auf M1 nicht auf Teilmodell |
| A6 | `26_10_07_ID-03_RF6-BASELINE_RUNBOOK_Rev1.md` (gdoc 1Vt1_N4G…) + `26_10_06_ID-03_RF6-BASELINE-LAUF_Rev1.py` (1baiCQb5…) | 01:45 | ID-03 (frühere Session) | Option D: V01 unverändert rechnen, Export + RUNLOG; Signaturen gegen dlubal.api **2.16.1** geprüft; Rev2/Rev3-Rückschreibskripte SUPERSEDED | gültig für Baseline-Lauf; API-Version klären (§4) |
| A7 | `26_10_06_233714_ID-03_ARBEITSANWEISUNG_CLAUDE_RFEM6_API.md` (1CDTxQe4…) | 06.10. 21:37 | ID-03 | 12 Schritte Arbeitskopie → Readback → Rechnung → Bericht | gültig, generisch |
| A8 | `26_10_06_ID-03_WO_CLAUDE_SEILSTATIK_BOEBLINGEN.md`, `…Skill-Work-Order-GPT/-Gemini.md`, `…SYSTEMPROMPT-SEILSTATIK-VORABZUG.md` | 06.10. 15:05–15:44 | ID-03 | Rollen, Work-Orders | historisch, Rollenregister |
| A9 | NEXUS-RF6-CABLE CONCEPT / ADDON (gdocs 1bNSPT-l…, 1Tu8e8a9…) | 11:55–12:20 | ID01-Draft | Architektur (Planes, Gates, Run-Envelope, Ablage) | Rahmen, keine Lauf-Anweisung |

## 2 Teilmodell-Definitionen im Vergleich

| Quelle | Knoten | Stäbe | Schnitt | Mast 1021 | Rand Kn 8 |
|---|---|---|---|---|---|
| A1 (ID-03, T01–T11) | A-T 16 / B-T 14 | 15 / 13 | 8 (S16, S23 weg) | drin (3021, 2021) | R1: u fest, φ frei; R2: Zwangsverformung |
| `26_10_07_ID-03-RF6_TEILMODELL_C06-C07-C21_Rev0.json` (1T932WHT…, 07:55) | 14 (B) | 13 | 8 „ERSATZ_GELENKIG" (u fest, φ frei) | drin | wie A1 R1 |
| A3 ID-Deep | 16 / 14 | 15 / 13 | 8 | drin | R1 „6 DOF gesperrt" |
| `TELLER_SCHNITT_C06_C07_TOPOLOGIE_QA_Rev0.zip` (1fCbCRpv…, 13:04) | 16 / 14 (CSV beigelegt, aus v0.1) | 15 / 13 | 8 | drin („3021 statt 115") | R1 „nicht bewiesen" → Kalibrierung gegen 13bb |
| A4 V1.1 | 14 | 13 | **6, 11, 30** | **weg** (S63 abgeschnitten) | 6-DOF je Schnittknoten einzeln |

Befund: Vier Herleitungen (drei davon unabhängig von A1) treffen denselben Schnitt. A4 schneidet S63 am Mastkopf ab und erzeugt drei Schnittknoten statt einem; das vergrößert die Randunsicherheit, ohne Objekte zu sparen (14/13 in beiden Fällen). Empfehlung bleibt A1. Z der neuen Anker: A4 liest „+0,451 m handschriftlich", T1 ergibt 0,452 m (445,472 − 445,020); 1 mm, kein Konflikt. Die TELLER-QA korrigiert eine Fremdparaphrase „V1.4" (115 statt 3021, 7 Lager, LF10 10 × −0,8), nicht die A1-Dateien; ihre Korrekturen entsprechen A1.

## 3 Datensätze im Ordner (Eingabekandidaten)

| Datensatz | Ort | Inhalt | Verhältnis zu A1 |
|---|---|---|---|
| EINGABEDATEN_RF6_v0.1 (+ Zip 1-0r03VN…) und TEILMODELL_v0.1 | Daten/input/ | 01–09, B_VARA 10–14, T01–T11, Hashes | Basis von A1 |
| `26_10_07_RF6_VAR-A_Rev0_CANDIDATE` (gsheet 1oJjVmR9…, 08:07) + Ordner `…ID-03-RF6_EINGABE_VAR-A_Rev0` (10Cp0Cdh…) | Root | 12 Blätter SI (Pa, N), 84/86/86, LK 71 Faktorzeilen, EK1/EK2, Solver (fe 0,5 m, Teilungen 10, Tc 0 °C, g 10, RFEM 6.12.0008/API 2.12.8), Richtungen + Bezugslänge je Stablast (LF30 WAHR, sonst PROJIZIERT) | gleicher Inhalt wie v0.1 in SI; **löst die offenen Richtungscodes aus 08_stablasten** → übernehmen |
| `26_10_07_RF6_86-88_CANDIDATE` (gsheet 1DRoUiK8…, xlsx 1_IBxPm2…, Manifest 1Qr0unap…) + Ordner `…FULL_INPUT_86-88_Rev1` (1OTRzBxe…) | Root | Modell A 86/88 in SI, 13_PFEIFER_AUDIT (Lsys = L + 156, LB = LAG2 − 127 arithmetisch) | Modell A, konsistent |
| `26_10_07_RF6_VAR-A_84-86_Rev1.zip` (1vULivds…), `…MODELL_A_B_DELTA_Rev1.csv` (1TUe02Ci…), `…A_B_DELTA_REFINEMENT.md` (1ifIozFd…) | Root | A/B-Diff, 7 Koordinaten, Lager 36/37 vs 44, 69 vs 71 LK-Zeilen | konsistent mit Patch E7 |
| Fall-B-Prüfung: `…FALL_B_PRUEFVERMERK.md` (1BBDMBrt…), `…USERDATEN_VALIDIERUNG.csv` (1zT1100l…), `…FALL_B_DOKUMENTPRUEFUNG.md` (120KHIEx…), `…QUELLENWEGWEISER_UND_TOPOLOGIE_ADDENDUM.md` (1EeyMOi-…) | Root 08:39–08:56 | unabhängige Prüfung des Fremddatensatzes; **neue Primärquelle:** Schreiben LR Grundstücksgesellschaft 06.03.2026 „Fassadenanker statt zweier Pylone" (1pRgq2rC…) | deckt Loop 1/2; Schreiben in Quellenlog Ursprung aufnehmen |
| `…RF6_86-88_REVIEW_UND_GEMINI_AUFTRAG_Rev0–2.md`, `rf5_rf6_node_delta.py`, `…RF5_RF6_KNOTEN_DELTA_CANDIDATE.csv`, `…RF5_AUSDRUCK_KNOTEN_106_PDF_EXTRAKT.csv`, `boeb_import.py` (Inspektor), `rf5_export_probe.py`, `boeb_full_pipeline_safe.py`, `pfeifer_mapping_formula_audit.csv`, `26_10_07_preflight_report.json` | Root 08:16–08:25 | 106 PDF-Knoten ↔ 86 Kandidat ≤ 1,5 mm; Fremdskripte als „nicht ausführungsreif" beurteilt; Routen A/B/C für Gemini | deckt Sperrliste; `boeb_import.py` hier = read-only-Inspektor, nicht das gesperrte Chatskript gleichen Namens |
| RF6-Tabellenexport-Index `26_10_07_ID-03-Stäbe+Stabendgelenke-json.txt` (14gCnIvx…) | Root 12:06 | Liste der lokal exportierten RF6-Tabellen (CSV + JSON) | Readback-Format für Schritt 5/7 |

## 4 Konflikte und Entscheidungen

| # | Punkt | Stände | Entscheidung / Empfehlung |
|---|---|---|---|
| K1 | Modellgrenze | A1/JSON/Deep/TELLER: Kn 8 · A4: 6/11/30 | A1 (ein Schnittknoten, alle anderen Ränder echte Lager); Gate T-G1 entscheidet, ob Ring 4 nötig |
| K2 | Randbedingung Kn 8 | A1: u fest, φ frei · Deep: 6 DOF · A4: je DOF belegen · TELLER: „nicht bewiesen" | Seilknoten überträgt keine Momente → φ frei (A1); R1 nur mit T-G1-Kalibrierung, sonst R2 |
| K3 | CSV-Vertrag | A1: `;`, Punkt, BOM, kN/cm · Deep: `;`, Komma, ohne BOM · A2/A4: `,`, Punkt, SI | A1 bleibt (Dateien existieren, Hashes); SI-Umrechnung im Generator (×1e7, ×1e-4, ×1e3) |
| K4 | Tabellennamen | A1: T01–T11 · Deep: T00–T16 · A4: 01_CSV/*.csv | A1-Namen; Deep-Ergänzungen als T12–T16 übernehmen (Readback A, Results B, Comparison, Readback B, Verify) |
| K5 | Toleranzen | Deep: N ±0,5 kN/±2 %, u ±3 mm, L ±10 mm, xyz ±1 mm · A4: „keine erfundenen Toleranzen" | Deep-Werte als **Vorschlag E8**, Festlegung ID01 |
| K6 | Referenzmodell | ID01: 13bb (Kneidinger) · Review Rev2: WORKING-Kopie statt „Legacy 13bb" · Checkliste: M1 | 13bb laut Entscheidung; Fassung/Hash offen |
| K7 | API-/RFEM-Version | 6.12.0008 + api 2.12.8 (Bridge, Sheets) · 6.13.0001 → 2.13.1 (Quellenlog) · 2.16.1 (Runbook 01:45) | `api_write_check.py` liefert die installierten Versionen; Eintrag in Quellenlog RF6 §1 |
| K8 | Label „ID-03" | A2, A4, A5 tragen ID-03, stammen nicht aus dieser Session | Rollenregister: Fremdfassungen künftig mit eigener ID (ID-Deep ist korrekt gelabelt) |
| K9 | LF10 | alle Drive-Prüfungen: 30 × +1,000 kN | abgeschlossen |

## 5 Übernahmen in den verbindlichen Satz (A1)

1. Richtung + Bezugslänge der Stablasten aus dem VAR-A/86-88-Sheet (RF5-Ausdruck): LF10 Kabel Z projiziert; dT „wahr"; LF30 X wahr, LF31–33/50–53/60–63 projiziert; Eis Z projiziert. Ersetzt die RF6-internen Richtungscodes in 08_/T08.
2. Vorbedingungen V1–V5 und Gate-Tabelle aus A3 (T-G0…GATE-6) als Prüfliste; Begleitschreiben-Formular A3 §1–§11 als Vorlage für das heutige Schreiben, gefüllt mit A1-Inhalten.
3. Primärquelle Schreiben 06.03.2026 (1pRgq2rC…) in Quellenlog Ursprung als U0 (Auftrag) aufnehmen; A4-Links (Bestandsdruck, Halterungsdoku, Gesamtstatik) prüfen und als U1-Fundorte eintragen.

## 6 Nur im Chat vorhanden (nicht als Drive-Anweisung)

Entscheidungen ID01 (13bb mit Kneidinger; Modellreduktion; „heute versenden"), Höhenkontrolle T1 (445,020 → 0,452), Ring-Analyse, Begleitschreiben-Punkte 1–10. Alles davon steht in Quellenlog RF6 §6a–§6c, Topologie-Gate und Begleitschreiben-Notizen (Befunde). Keine weitere Chat-Information ist für den Lauf erforderlich.
