# STATUSBERICHT Seilstatik Böblingen — Ergänzung 4 (RF5 → CSV → RFEM 6, Teilmodell) — Rev0

| Feld | Wert |
|---|---|
| Stand | 08.10.2026 00:xx UTC (Arbeitsstand Ende 07.10.) · Ersteller ID-03 · für ID01 / P. Kneidinger / Prüfstatik |
| Projekt | GZ 26_001_BOEBLINGEN, BV Boardinghouse, Seilnetz Straßenbeleuchtung, Ergänzung 4 zur Bestandsstatik 2015 |
| Auftrag | Zwei Pylone C06/C07 durch Fassadenanker ersetzt → neue Seillängen S19/S22; Nachweis analog Bestandsstatik |
| Gesamtstatus | **Eingabe- und Teilmodelldaten vollständig und gehasht; RFEM-6-Rechenlauf lokal noch nicht ausgeführt.** Lieferfähig heute: Teilmodell-Tabellen, Skill/Wegweiser, Begleitschreiben-Notizen. Nicht lieferfähig: Ergebnisse, Delta-Matrix, Nachweise. |

## 1 Wo wird dokumentiert (drei Orte, ein Inhalt)

| Ort | Was | Zugang |
|---|---|---|
| **GitHub** `julianzotter/julianzotter`, Branch `claude/seilstatik-doku-overview-rc0lpt` (Stand Commit 0e893cb) | Verträge und Code: `.claude/skills/seilstatik-rf5-rf6-neuaufbau/` (SKILL, WEGWEISER), `tools/` (6 Skripte + Quarantäne), `docs/` (alle Befunde, Loops, Quellenlog, Eingabedaten v0.1 + Teilmodell v0.1, Pakete als ZIP) | versioniert, jede Datei mit Commit |
| **Google Drive** `_INDEX_LNK/BENCHMARK-SEILSTATIK/` (Ordner-ID 1ZpE9ym5UVEJuiLml0YKXDQl8Qk878sZl) = lokal `G:\Meine Ablage\_INDEX_LNK\BENCHMARK-SEILSTATIK\` | Spiegel des Pakets: `SKILL/`, `Skripte/`, `Daten/input/EINGABEDATEN_RF6_v0.1/` und `…TEILMODELL_v0.1/`, `Befunde/`, `Logs/`, `Daten/results/`, `00_Quellenlog/` (Ursprung, Vermesser, RF6, API_Auszuege), `README_PAKET.md`, `MANIFEST_PAKET.json` | Drive für Desktop synchronisiert nach G:\ |
| **Quellenlog RF6** `00_Quellenlog/RF6/26_10_06_ID-03_Quellenlog_RF6_Rev1.md` (Drive 1NVDntJwuR3d4aupLzMvi-MqnsA92wIYV) | Register: Modelle + Hashes §1, Exporte §2, Run-Register §3 (noch leer), Entscheidungen §4/§6c, Pfade + Drive-IDs §6/§6a, Skill §6b | Pflege ID01/ID-03; jede neue Datei bekommt hier eine Zeile |

Regel: Chat-Entscheidungen werden sofort in das Quellenlog übernommen (zuletzt §6c Referenzmodell 13bb). Ohne Zeile im Quellenlog gilt eine Datei als nicht vorhanden.

## 2 Entscheidungen ID01 (07.10.2026)

| Nr | Entscheidung | Dokumentiert in |
|---|---|---|
| D1 | Extraktion aller Rechenmodelldaten aus RF5 + PDF nach CSV; nur die zwei Haltepunkte 3006/3007 ändern; Import über CSV + API; Vergleich nur RF5-Bestand ↔ RF6-neu | SKILL §0 |
| D2 | Referenzmodell = RF5-Gesamtmodell `13bb_ausführungsstatik_1.rf5` (mit P. Kneidinger vereinbart); 5e nur Querkontrolle | SKILL Schritt 1, Quellenlog RF6 §6c |
| D3 | Modellreduktion: Teilmodell um C06/C07 mit Randbedingungen an der Modellgrenze | SKILL §6, TEILMODELL_v0.1 |
| D4 | Fremdskripte (rf5_export, boeb_*) gesperrt; nur Repo-Skripte | Sperrliste Rev0, Gegencheck-Antwort |

## 3 Geliefert (prüffähig, mit SHA-256)

| Lieferung | Inhalt | Ort |
|---|---|---|
| EINGABEDATEN_RF6_v0.1 | Modell A (Bestand, aus 5e-Export): 86 Kn, 88 St, 6 Mat, 13 QS, 27 Lager, 28 Parameter, 17 Knotenlasten, 18 Stablasten, 19 LF + 21 LK; Modell B Patch E7 (3006/3007, Löschungen, Lager) | Daten/input/EINGABEDATEN_RF6_v0.1 · Repo docs/00_Quellenlog/RF6/ |
| EINGABEDATEN_RF6_TEILMODELL_v0.1 | T01–T11: A-T 16 Kn / 15 St, B-T 14 / 13; Schnittknoten 8; Randbedingung R1/R2; Allowlist 8 Zeilen; Manifest | Daten/input/EINGABEDATEN_RF6_TEILMODELL_v0.1 (Drive 1dohnA_rFa-7NS3ygHX4fxzS8bOQ5BcTo) |
| Skill + Wegweiser | Arbeitsauftrag 10 Schritte, Schnittstellen RF5/PDF/SV/RF6/API/MCP/CSV, CSV-Verträge, minimaler Datensatz, Gates | SKILL/ (Drive 1F1xbTixsIAZ4qnTuUuPW0PIdNmvsDu1_), Repo `.claude/skills/` |
| Topologie-Gate C06/C07 | Lampenplan V1: 7101 → C06 → 3006/2006, 7102 → C07 → 3007/2007; beide Z = 445,020 m → z = 0,452 m; Wandanker reproduzieren Bestandshöhe auf 1–25 mm | Befunde/…TOPOLOGIE-GATE… |
| Begleitschreiben-Notizen | 10 Punkte (Referenz 13bb, Annahme Modellgrenze, Ankergeometrie vorläufig, Lasten 1:1, F_Rd 27,9 kN, offene Punkte) | Befunde/…BEGLEITSCHREIBEN-NOTIZEN… |
| Prüfberichte | Loop 1 (Fremddaten „Fall B"), Loop 2 (Docx Fertigstellung), Gegencheck-Antwort, Sperrliste, Artefakt-Analyse (07.10. 13:30) | Befunde/ |
| Skripte | api_write_check, Ergebnis-Export (E6a), anpassen_rf6, retour_rfem6_patch (Dry-Run), make_eingabedaten, render_eingabetabellen_md, make_teilmodell | Skripte/ · Repo tools/ |
| Pakete | `SEILSTATIK_BOEBLINGEN_ERG4_BENCHMARK-SEILSTATIK_v0.1.zip` (50 Dateien), `26_10_07_ID-03_RECHENLAUF_HEUTE_TEILMODELL_v0.1.zip` | Repo docs/00_Quellenlog/RF6/, Dateiversand Session |

## 4 Offen (blockiert den Rechenlauf oder den Versand als „geprüft")

| # | Punkt | Wer | Wirkung |
|---|---|---|---|
| O1 | 13bb: Fassung (54 054 912 oder 54 075 392 Byte), SHA-256, Datum der Vereinbarung; Datei nach `Daten\input\` | ID01 | Skill Schritt 1 (Gate) |
| O2 | COM-Export aus 13bb → EINGABEDATEN_RF6_v0.2_13bb (v0.1 stammt aus 5e) + Diff 5e ↔ 13bb | ID01/Codex lokal | Schritt 2 |
| O3 | RF5-Vergleichswerte LK100 aus 13bb: N S17/S18/S19/S22/S60/S63/S64/S81, Lager 105/106/113/114/2021, u Kn 8/9/10/29/30 (`10–12_resultate_rf5`) | ID01 lokal | Gate T-G1, Randbedingung R2 |
| O4 | `api_write_check.py` ausführen (dlubal.api 2.13.1 zu Server 6.13.0001) → WRITE_API_PRESENT | ID01/Codex | Schritte 4–8 |
| O5 | Generator Modell A-T aus CSV (wird nach O4 geschrieben) | ID-03 | Schritt 5 |
| O6 | Skizze Modellgrenze nachreichen → Annahme A1 (Schnitt bei Kn 8) bestätigen oder Ring 4 | ID01 | Begleitschreiben |
| O7 | Entscheidungen E3 (C21), E4 (LK220), E8 (Toleranz; Vorschlag N ±0,5 kN/±2 %, u ±3 mm), E9 (Schubsteifigkeit), F7 (Beschlagmaß) in `Skripte\gates.json` | ID01 | Modell B, Blatt 6 |
| O8 | Beschaffung: U1 PDF Bestandsstatik in den Ordner, U9 PFEIFER K15.105, VF1 Lochmitte 7101/7102 (Geometer), Prüfberichte PB00–PB03; Schreiben LR 06.03.2026 (Drive 1pRgq2rCnX7mgKkSgUN6GbwvogNWpbBpa) ins Quellenlog Ursprung | ID01 | Nachweise, Seillängen |

## 5 Nächste Schritte (Reihenfolge)

1. O1 + O4 lokal (30 min): Hash 13bb, `api_write_check.py`, Ergebnis-JSON nach `Logs\` und Quellenlog RF6 §1/§3.
2. O2/O3: COM-Export 13bb und LK100-Vergleichswerte → `Daten\input\EINGABEDATEN_RF6_v0.2_13bb\`.
3. ID-03: Generator Modell A-T → Readback → Rechenlauf A-T → Gate T-G1 gegen O3.
4. Modell B-T (Patch, Allowlist) → Rechenlauf → Export → Delta-Matrix Blatt 6 → Begleitschreiben finalisieren.
5. Run-Register Quellenlog RF6 §3 je Lauf (Modell-Hash, Skript-Hash, Ergebnis-Hashes).

## 6 Bekannte Abweichungen zwischen parallelen Fremdfassungen (siehe Artefakt-Analyse §4)

Modellgrenze Kn 8 (vier Quellen) gegen 6/11/30 (eine Quelle); Randbedingung u fest/φ frei gegen 6 DOF; drei CSV-Konventionen; RFEM/API-Versionen 6.12/2.12.8 · 6.13/2.13.1 · 2.16.1. Verbindlich: Ordner SKILL; Abweichungen sind entschieden oder mit Gate versehen.
