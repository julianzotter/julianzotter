# WEGWEISER — wo liegen die Daten für den Skill `seilstatik-rf5-rf6-neuaufbau`

Lokal = `G:\Meine Ablage\_INDEX_LNK\BENCHMARK-SEILSTATIK\` (Drive für Desktop, synchron mit Drive-Ordner 1ZpE9ym5UVEJuiLml0YKXDQl8Qk878sZl). Repo = `julianzotter/julianzotter`, Branch `claude/seilstatik-doku-overview-rc0lpt`.

## 1 Eingaben je Schritt

| Schritt | Was | Wo (Drive-ID / Pfad) | Status |
|---|---|---|---|
| 1 | RF5 Berichtsmodell 5e `…150328_5e.rf5` (SHA BD77CF83…) | EXPORT\…\14_bb\statistik-unterlagen-150325\ (lokal, G:) | VERIFIED (Hash lt. VORLAGE-002) |
| 1 | RF5 Gesamtmodell „13bb" `13bb_ausführungsstatik_1.rf5` (zwei Fassungen 54 054 912 / 54 075 392 B) | EXPORT\…\04 Berechnung Gesamtsystem (lokal) | FOUND, Hash fehlt → Schritt 1 |
| 1 | PDF Bestandsstatik U1 (62 S.) + Ergänzung 2 (LK220) | EXPORT\00 Bestandstatik fragmentiert\…\13bb-statik-dokumentation\ (lokal) | FOUND, nicht im BENCHMARK-Ordner |
| 1 | RF5-Ausdruck V01 (20 S., Lager §1.7, QS §1.13, LF, LK) | Drive 1QAhMcR2hvvTk3Wt3rS7955cjfJhARaOK | gelesen (BEFUND Rev0) |
| 1 | RF6-Ausdruckprotokoll M1 (14,8 MB) | Drive 1flvOcGTPA3QKmNvGgfFwhMWzta90ZZU0 | nicht gelesen |
| 1 | Geometer V1 `7864Halterungen_mit_Lampenplan_Boardinghouse.xlsx` (7100–7108, Landeskoordinaten, Zuordnung RFEM) | Drive 1j-GHSEH7x_JsUppBplMaQYvcwje6EhKe | PRIMARY |
| 2 | RF5-COM-Export U10 (`input_3.json`, Knoten/Stäbe/Mat/QS/Lager/Parameter) + `lines.csv`, `members.csv` | Drive TEILABGLEICH.zip 1o_GYZlL59GwJtw6_RfSLPsusJGep5PwL (sources/) | gelesen, SHA 394820eb… |
| 2 | Lasten/LK aus RF6-Arbeitskopie `model.db` (M5, .rf6bak SHA 903093dd…) | Drive-Ordner 1opSMplUY91rtVnztdlam9ZbhVA3FgMOf | gelesen |
| 2 | Fertige CSV v0.1 (01–09, B_VARA 10–14, MANIFEST) | `Daten\input\EINGABEDATEN_RF6_v0.1\` · Drive 1ZPr8x8H81DXt6qQAHICKe8huZ1-nMmuO · Zip 1-0r03VNC5jV_xm8rALgGfDS40MFn9vs7 | CANDIDATE |
| 2 | Lesbare Tabellen `EINGABETABELLEN_RF6_v0.1.md` | Drive 13UTLAfnGGE1VP1iQt5iOnOaej6gSYFRz | CANDIDATE |
| 2 | `10_resultate_rf5.csv` (N, Lager, u aus PDF) | **fehlt** → aus U1/RF5-Ausdruck erzeugen | OFFEN |
| 3 | Patch zwei Haltepunkte `10_patch_vara_rev0.json` | `Daten\input\EINGABEDATEN_RF6_v0.1\B_VARA\` · Drive 1_4Xn1lhGCt5F0iU7HDKTFWTg-vC6d3jp | Rev0 |
| 3 | Zuordnung Geometer ↔ RFEM (V9) `…AEQUIVALENZ-KNOTEN…Rev0.csv` | Drive 1pnPWQTNqXODcQCdJ1NmOFOcybO_eil5G | DERIVED-KANON |
| 3 | Topologie-Gate C06/C07 (Plan + Höhenkontrolle) | `Befunde\26_10_07_ID-03_TOPOLOGIE-GATE_C06-C07_LAMPENPLAN_Rev0.md` · Drive 1Fx_VzssiwtKoq-kv9CDZ5R01m1IesfM5 | ERFÜLLT |
| 3 | Kurzbericht VAR-A 23.09.2026 (Transformation T1, 84/68/18) | Drive-Suche „KURZBERICHT_RFEM_VAR-A" | Quelle für T1 |
| 4 | `26_10_06_ID-03_api_write_check.py` | `Skripte\` · Drive 1YAyxwF66RVlC5ZNk0bWDQZ0OJxiCE9mk | CANDIDATE |
| 4 | Bridge E5 `26_10_06_ID-03-RFEM6_MCP_Bridge_Extended.py` (api_key_value, execute(), raw_results, snapshot) | lokal `Skripte\` (nicht im Repo) | belegt, SDK 2.12.8 → 2.13.1 nötig |
| 5 | Generator Modell A aus CSV | **fehlt** → nach Schritt 4 schreiben (Vorlage: `retour_rfem6_patch.py` need()-Muster, `make_eingabedaten.py` Tabellen) | OFFEN |
| 5–8 | `26_10_06_ID-03-RF6-Ergebnis-Export.py` (3 CSV + API_Log) | `Skripte\` · Drive 1gUwpP78z2UF8krSoqD9cl3xwJXwhbdlG | CANDIDATE |
| 6 | Kalibrierziele u_Kn17 2,085 m, N_S54 17,47 kN; Delta-Matrix Vorlage Blatt 6 | `Befunde\26_10_06_ID-03_DELTA-MATRIX_BLATT6_VORLAGE_Rev0.md` · Drive 1UrIB7cf3LTBdxXsle8ZWlw1DB0rL66LT | Rev0 |
| 7 | `26_10_06_ID-03_retour_rfem6_patch.py` + `gates.json.example` | `Skripte\` · Drive 1yG40SCCbz3vjF_nkr7gZDigdkupUfGGa | Dry-Run geprüft |
| 9 | `26_10_06_ID-03_anpassen_rf6.py` (Delta-Auswertung) | `Skripte\` · Drive 13KBaOIRlTxQu_BcOMl1LT1wqFjX0ELa7 | CANDIDATE |
| 9 | F_Rd 27,9 kN (F_Rk 46,1 kN, γ_R·γ_M = 1,5·1,1), ETA-11/0160 | Quellenlog Ursprung U9b | FOUND |
| 10 | Quellenlog Ursprung / Vermesser / RF6 (Run-Register §3, Pfade §6) | `00_Quellenlog\` · RF6 Rev1 Drive 1PqqND7dbDesZIgtBVmitxmsi9yXpNfiB | Rev0/Rev1 |

## 2 Beschaffung (ID01), blockiert Schritte 1/2/9

| Objekt | Wofür | Von wem |
|---|---|---|
| U1 PDF Bestandsstatik Teil I–III (62 S.) in den BENCHMARK-Ordner kopieren | Schritt 2 Resultate, Schritt 10 | lokal EXPORT-Ordner |
| 13bb.rf5 Hash + Entscheidung 5e vs 13bb als Referenz | Schritt 1 | ID01 |
| U9 PFEIFER K15.105 (Lsys, Beschläge) | Seillängen S19/S22, F7 | PFEIFER / Archiv |
| VF1 Lochmitte 7101/7102 (Bolzenachse) | Nulllage 3006/3007 | Geometer |
| Prüfberichte PB00–PB03 | Vergleichswerte Bestand | Prüfstatiker |

## 3 Entscheidungen, die in `Skripte\gates.json` stehen müssen

| Gate | Inhalt | Stand |
|---|---|---|
| E1 | Geometriebasis T1 (VAR-A, zwei Punkte) | durch Entscheidung 07.10. gesetzt: zwei Haltepunkte |
| E2 | Maste 1006/1007 entfallen, 3006/3007 gelenkig | durch Entscheidung 07.10. gesetzt |
| P2 | QS-14-Hilfsgeometrie nicht übernehmen | in Modell A ohnehin nicht enthalten |
| E3 | C21 (3021) unverändert lassen | Entscheidung „alles andere bleibt" → unverändert |
| E4 | LK220 ergänzen | offen |
| E8 | Kalibriertoleranz Schritt 6 | offen (Vorschlag N ±2 %, u ±3 %) |
| E9 | Schubsteifigkeits-Flag QS 10/11/12 | offen (nur Arbeitskopie M5; Modell A aus CSV hat RF5-Flags) |
| F7 | Beschlagmaß S19/S22 | offen (U9) |

## 4 Nicht verwenden

Fremdskripte `rf5_export.py`, `boeb_bereinigung.py`, `boeb_rf6_generator*.py`, `boeb_delta_matrix.py`, `boeb_pfeifer_mapping.py`, `boeb_full_pipeline.py`, `tabellen_generator.py`, `boeb_import.py`; Excel V02/V04; `transformed_nodes.csv` (G3-Siebenpunkt); Docx FERTIGSTELLUNG „Fall B". Begründung: `Befunde\…SPERRLISTE…`, Loop 1, Loop 2, Gegencheck-Antwort (alle im Ordner Befunde, Drive 1tSNvcVz-dGZEZXX5bH-qUNX7tzs5F6PA).
