# QUELLENLOG — URSPRUNG (Bestandsstatik 2015, Auftrag 2026, Normen)

| Feld | Wert |
|---|---|
| Datei | `00_Quellenlog/Ursprung/26_10_06_ID-03_Quellenlog_Ursprung.md` |
| Projekt | GZ 26_001_BOEBLINGEN · BV Boardinghouse Böblingen · Seilnetz Straßenbeleuchtung |
| Rolle | ID-03 (Claude) · Pflege: ID01 (J. Zotter) |
| Status | CANDIDATE Rev0 · FOUND ≠ VERIFIED · Hash nur wo belegt |
| Regel | Eine Zeile = ein Objekt. Pflichtfelder: Q-ID, Datei, Ort (Pfad oder Drive-ID), Datum, Autorität, Hash, Rolle, Status. Keine Zahl ohne Fundstelle. |
| Kanon | Quellenverzeichnis Rev01 + Errata (U1–U19), VORLAGE-005, BEFUND RF5/RF6/VAR-A Rev0 (06.10.) |

## 1 Primärquellen Bestand 2015 (Werkraum Wien / intermetric / PFEIFER)

| Q-ID | Datei | Ort | Datum | Autorität | SHA-256 | Rolle | Status |
|---|---|---|---|---|---|---|---|
| U1 | 01-statik_leuchtenabspannung-teil1bis3_150417.pdf (62 S.) | EXPORT\00 Bestandstatik fragmentiert\…\13bb-statik-dokumentation\ | 17.04.2015 | Werkraum Wien Ingenieure (Prüfber. PB00–PB03, GZ 8w4_14) | – | Bestandsstatik Teil I–III | FOUND, im BENCHMARK-Ordner **nicht** vorhanden (BEFUND Rev0 §1) |
| U2 | Ergänzung 2 (LK220 = 1,35·LF10 + 1,50·LF43) | dto. | 28.04.2015 | Werkraum Wien | – | Nachtrag Bemessung | FOUND |
| U6 | leuchtenabspannung_gesamt_nachaufmassgeometer_150328_5e.rf5 | EXPORT\…\14_bb\statistik-unterlagen-150325\ | 14.04.2015 | Rechenbasis Bestand (Anh. 25) | BD77CF83… | **Berichtsmodell 5e**: 86 Kn, 68 Seile, 20 Maste, 19 LF, 21 LK, 2 RK | VERIFIED (Hash lt. VORLAGE-002 §2) |
| U6a | 13bb_ausführungsstatik_1.rf5 | dto. / 04 Berechnung Gesamtsystem | 01.04.2015 | Vorläufer | – (54 054 912 / 54 075 392 B, zwei Fassungen) | Archiv, nicht Berichtsmodell | FOUND |
| U9 | PFEIFER K15.105.01.01.00-Ind.1 (Seilmasterblatt), K15.105.03/04.01.00 (Knotenbleche) | nicht im Ordner | 2015 | PFEIFER Seil- und Hebetechnik | – | Lsys, Ablängkraft 15 kN, Beschläge | **OFFEN – Beschaffung** |
| U9b | ETA-11/0160 PFEIFER Wire Ropes | extern (DIBt) | 21.02.2025 | DIBt | – | Seilzulassung (Modellname Z-14.7-411 = alte abZ) | FOUND |
| U18 | Seilkraftmessung_Pfeifer.pdf (PIAB RTM 20 D, 18 Seile) | Drive 1wA4Zm_EejjEXFDTx3V5qnwvYYbhIH85a | 16.06.2015 | PFEIFER | – | Messung vs. Rechnung @22 °C, Δ 0…−2,0 kN | FOUND |
| U19 | Seilkraftmessung_Vergleich.pdf | Drive 1zuHrDvmNXjI3aYcQkeBdg-g3jZo9Og5w | 2015 | Werkraum/PFEIFER | – | Vergleichstabelle | FOUND |
| U20 | Prüfberichte PB00–PB03 (DI Th. Eschbacher) | nicht im Ordner | 2014/15 | Prüfstatiker | – | Prüfstatik Bestand | **OFFEN – Beschaffung** (BEFUND Rev0 G11) |

## 2 Auftrag und Projektdaten 2026

| Q-ID | Datei | Ort | Datum | Autorität | Hash | Rolle | Status |
|---|---|---|---|---|---|---|---|
| A1 | Angebot/Beauftragung „Wiedermontage Seilnetz, Änderung Seillänge (2 Fassadenanker statt Pylone)“ | _SEILSTATIK_BOEBLINGEN (PDF) | 2026 | AG / Zotter Consult | – | Scope: S19, S22; 12 000 EUR netto; **Fassadenankerprüfung ausgeschlossen** | FOUND (IMPLEMENTATION-WORKFLOW §1) |
| A2 | Rückbauplan 2022 (Ersatzpylon, Rückverankerung „Merkaden“, S17 entfällt) | _SEILSTATIK_BOEBLINGEN | 2022 | AG | – | Endzustand (F4) | FOUND, AG-Bestätigung offen |
| A3 | 26_09_23_KURZBERICHT_RFEM_VAR-A_LK100 | Drive 1uopiu06LiU-JYfso6C7uEHx2M7ZL4s2t | 23.09.2026 | Zotter Consult (RFEM 5.29 COM) | – | VAR-A-Ergebnisse (vorläufig) | DERIVED-KANON |
| A4 | VORLAGE-005 + Stellungnahme 23.09. | Drive 1VKWJ3ZPgSInVpTSEOzWnQdEJ7FV7imSI / 16b-bVXpiWkaXY0DioDYiIfo3nhh2i1ZN | 23.09.2026 | ID03/Codex | – | Prüfbericht-Entwurf, F1–F10 | DERIVED-KANON |
| A5 | RECHENSTAND_HASHES_20260923_1437.json | Drive 15J_KURcseSrOuOb3gqQ_au5fi1tdyqNL | 23.09.2026 | Manifest | 5e: 317D78D7… · VAR-A: EAB6A5B1… | Hash-Referenz Sandbox | VERIFIED |

## 3 Normen (Projekt in DE → DIN EN + NA-DE)

| N-ID | Norm | Ausgabe (zu belegen) | Verwendung |
|---|---|---|---|
| N1 | DIN EN 1990 + NA | – | Kombinatorik (E4 offen: Bestandslogik 1,35·ΣQ vs. Gl. 6.10) |
| N2 | DIN EN 1991-1-1/-1-3/-1-4/-1-5 + NA | – | Eigengewicht, Schnee, Wind, Temperatur |
| N3 | EN ISO 12494 / DIN 1055-5 | – | Eislasten (LF40–63) |
| N4 | DIN EN 1993-1-11 + NA | – | Seiltragwerke, F_Rd = F_Rk/(γ_R·γ_M) = 46,1/(1,5·1,1) = 27,9 kN |
| N5 | ETA-11/0160 | 21.02.2025 | Seil PE5 1×19, d 8,1 mm, A 38 mm², E 130 ± 10 kN/mm² |
| N6 | EN 1992-4 / ETA-04/0095 (Würth W-VIZ) | – | nur Schnittstelle Ankerkräfte, Nachweis bauseits (A1) |

## 4 Pflegeregeln

1. Neue Zeile nur mit Ort + Datum; Hash nachtragen, sobald lokal gerechnet (`tools/01_scan_registry.py --hash`).
2. Statuswerte: FOUND · VERIFIED · DERIVED-KANON · OFFEN – Beschaffung · SPERRLISTE.
3. Änderungen am Kanon (U-Nummern) nur über Rev02 des Quellenverzeichnisses, hier nur verlinken.
