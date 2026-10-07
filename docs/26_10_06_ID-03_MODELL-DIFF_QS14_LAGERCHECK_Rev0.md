# MODELL-DIFF RF6 — QS 14 (bp-beleuchtung) mit Lagercheck — Rev0

| Feld | Wert |
|---|---|
| Projekt | GZ 26_001_BOEBLINGEN · Seilnetz · Auftrag 3 (Claude, 06.10.2026) |
| Modell | `26_10_06_SEILSTATIK-MODELL-001.rf6` (Drive 119Unwcdhj5MEfUiOmmlR59FlIh2-PaYt, SHA-256 1286822edbe6c738933e401619b5cd2df0df032b1c62f3306be19c28573db3cd, 2 309 460 B) |
| Datenquelle | `26_10_06_ID-03_SEILSTATIK_RF5_RF6_TEILABGLEICH.zip` (1o_GYZlL59GwJtw6_RfSLPsusJGep5PwL): nodes.csv (106), lines.csv (105), members.csv (105), summary.json; Lagerinfo aus RF5-Ausdruck V01_WORKING (1QAhMcR2hvvTk3Wt3rS7955cjfJhARaOK) §1.7 via BEFUND Rev0 §5 |
| Status | CANDIDATE · Metadaten ✔ · Inhaltsprüfung ✔ (CSV) · RF6-Lagertabelle **nicht** im Teilabgleich enthalten → Lagercheck = Abgleich gegen RF5-Lagerliste, in RF6 zu bestätigen (§5) |
| Ebenen | keine Berechnung · keine Freigabe · keine Änderung am Original |

## 0 TL;DR

- 17 Stäbe mit QS 14 (`bp-beleuchtung`, A = 1,0 cm², I = 1,0 cm⁴, b = h = 0 → RF6-Fehler QS 14) liegen alle auf z = 0,284 m. Keiner existiert in Bestand 5e (nodes.csv: alle Endknoten `ADDED`).
- Drei Cluster: **C2** = 15 Stäbe (179–193) als zusammenhängender Balkenbaum, einziger Anschluss an das Tragwerk über **Stab 193 an Seilknoten 6** (dort Seile 12/13/16). **C1a** Stab 158 und **C1b** Stab 178 sind isolierte Einzelbalken.
- **Lagercheck:** keiner der 19 Hilfsknoten (3025–3028, 3057–3072 ohne 3059) und Knoten 6 trägt ein Lager (RF5-Lagerliste nur 101–115 gelenkig, 2001–2021 eingespannt). C1a/C1b sind kinematisch (frei schwebend), C2 hängt nur an Kn 6 → Singularität + Zusatzmasse.
- Knoten 3095 (0/0/0) hat keinen Stab. Querschnitte 15–17 sind definiert, aber unbenutzt.
- **Aktion (Vorschlag, Freigabe ID01):** 17 Stäbe + 20 Knoten (3025–3028, 3057–3072 ohne 3059, 3095) + QS 14–17 in der Arbeitskopie `…_WORKING_CALC.rf6` löschen. Kontrollwerte danach: 86 Kn / 88 Stäbe (= Bestand 5e) vor VAR-A-Patch; 84 Kn / 86 Stäbe nach Patch (Maste 1006/1007 entfallen).

## 1 Stabtabelle QS 14 (17 Stäbe)

| Stab | Linie | Knoten i → j | L [m] | z_i / z_j [m] | Cluster | weitere Stäbe an i | weitere Stäbe an j | Lager i / j | Bestand 5e | Aktion |
|---|---|---|---|---|---|---|---|---|---|---|
| 158 | 158 | 3026 → 3025 | 0.911 | 0.284 / 0.284 | C1a isoliert | – | – | kein / kein | nein (ADDED) | löschen |
| 178 | 159 | 3028 → 3027 | 0.720 | 0.284 / 0.284 | C1b isoliert | – | – | kein / kein | nein (ADDED) | löschen |
| 179 | 179 | 3058 → 3057 | 19.414 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | [180, 181] | [182, 183] | kein / kein | nein (ADDED) | löschen |
| 180 | 180 | 3060 → 3058 | 19.090 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | [188, 189, 190] | [179, 181] | kein / kein | nein (ADDED) | löschen |
| 181 | 181 | 3061 → 3058 | 2.904 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | – | [179, 180] | kein / kein | nein (ADDED) | löschen |
| 182 | 182 | 3062 → 3057 | 12.064 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | – | [179, 183] | kein / kein | nein (ADDED) | löschen |
| 183 | 183 | 3057 → 3063 | 10.768 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | [179, 182] | – | kein / kein | nein (ADDED) | löschen |
| 184 | 184 | 3065 → 3064 | 2.156 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | [192] | – | kein / kein | nein (ADDED) | löschen |
| 185 | 185 | 3067 → 3066 | 1.006 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | – | [187, 191] | kein / kein | nein (ADDED) | löschen |
| 186 | 186 | 3069 → 3068 | 3.701 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | – | [187, 190] | kein / kein | nein (ADDED) | löschen |
| 187 | 187 | 3068 → 3066 | 15.927 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | [186, 190] | [185, 191] | kein / kein | nein (ADDED) | löschen |
| 188 | 188 | 3070 → 3060 | 7.491 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | – | [180, 189, 190] | kein / kein | nein (ADDED) | löschen |
| 189 | 189 | 3071 → 3060 | 3.799 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | – | [180, 188, 190] | kein / kein | nein (ADDED) | löschen |
| 190 | 190 | 3060 → 3068 | 20.499 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | [180, 188, 189] | [186, 187] | kein / kein | nein (ADDED) | löschen |
| 191 | 191 | 3066 → 3072 | 11.699 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | [185, 187] | [192, 193] | kein / kein | nein (ADDED) | löschen |
| 192 | 192 | 3065 → 3072 | 16.528 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | [184] | [191, 193] | kein / kein | nein (ADDED) | löschen |
| 193 | 193 | 6 → 3072 | 23.685 | 0.284 / 0.284 | C2 Balkenbaum an Kn 6 | [12, 13, 16] | [191, 192] | kein / kein | nein (ADDED) | löschen |

ΣL = 172.362 m · Eigengewicht bei A = 1,0 cm², γ = 78,5 kN/m³: G = 1.353 kN (davon C2 170,731 m → 1,340 kN; wirkt vollständig auf Kn 6).

## 2 Knotentabelle Hilfsgeometrie (20 Knoten + Kn 6)

| Knoten | x [m] | y [m] | z [m] | Stäbe | Lager (RF5-Liste) | Bestand 5e | Lage ≈ | Aktion |
|---|---|---|---|---|---|---|---|---|
| 6 | 93.933 | 61.204 | 0.284 | [12, 13, 16, 193] | kein (nicht in 101–115 / 2001–2021) | MATCH_NUMERICAL | – | **behalten** (Seilknoten RL06, Stab 193 lösen) |
| 3025 | 143.471 | 59.342 | 0.284 | [158] | kein (nicht in 101–115 / 2001–2021) | ADDED | – | löschen |
| 3026 | 142.929 | 58.610 | 0.284 | [158] | kein (nicht in 101–115 / 2001–2021) | ADDED | – | löschen |
| 3027 | 162.620 | 44.755 | 0.284 | [178] | kein (nicht in 101–115 / 2001–2021) | ADDED | – | löschen |
| 3028 | 162.193 | 44.175 | 0.284 | [178] | kein (nicht in 101–115 / 2001–2021) | ADDED | – | löschen |
| 3057 | 181.328 | 16.984 | 0.284 | [179, 182, 183] | kein (nicht in 101–115 / 2001–2021) | ADDED | – | löschen |
| 3058 | 170.967 | 33.402 | 0.284 | [179, 180, 181] | kein (nicht in 101–115 / 2001–2021) | ADDED | – | löschen |
| 3060 | 153.191 | 40.360 | 0.284 | [180, 188, 189, 190] | kein (nicht in 101–115 / 2001–2021) | ADDED | – | löschen |
| 3061 | 172.272 | 35.996 | 0.284 | [181] | kein (nicht in 101–115 / 2001–2021) | ADDED | ≈ A13 | löschen |
| 3062 | 193.306 | 15.550 | 0.284 | [182] | kein (nicht in 101–115 / 2001–2021) | ADDED | ≈ C21 | löschen |
| 3063 | 172.478 | 10.850 | 0.284 | [183] | kein (nicht in 101–115 / 2001–2021) | ADDED | ≈ A14 | löschen |
| 3064 | 120.506 | 85.008 | 0.284 | [184] | kein (nicht in 101–115 / 2001–2021) | ADDED | – | löschen |
| 3065 | 121.780 | 83.268 | 0.284 | [184, 192] | kein (nicht in 101–115 / 2001–2021) | ADDED | – | löschen |
| 3066 | 123.428 | 57.908 | 0.284 | [185, 187, 191] | kein (nicht in 101–115 / 2001–2021) | ADDED | ≈ A05 | löschen |
| 3067 | 122.772 | 57.145 | 0.284 | [185] | kein (nicht in 101–115 / 2001–2021) | ADDED | ≈ A05 | löschen |
| 3068 | 139.137 | 55.284 | 0.284 | [186, 187, 190] | kein (nicht in 101–115 / 2001–2021) | ADDED | – | löschen |
| 3069 | 141.891 | 57.755 | 0.284 | [186] | kein (nicht in 101–115 / 2001–2021) | ADDED | ≈ C06 | löschen |
| 3070 | 160.072 | 43.321 | 0.284 | [188] | kein (nicht in 101–115 / 2001–2021) | ADDED | ≈ C07 | löschen |
| 3071 | 151.665 | 36.881 | 0.284 | [189] | kein (nicht in 101–115 / 2001–2021) | ADDED | ≈ A06 | löschen |
| 3072 | 116.760 | 67.521 | 0.284 | [191, 192, 193] | kein (nicht in 101–115 / 2001–2021) | ADDED | – | löschen |
| 3095 | 0.000 | 0.000 | 0.000 | – (kein Stab) | kein (nicht in 101–115 / 2001–2021) | ADDED | – | löschen |

## 3 Clusterbefund

| Cluster | Stäbe | ΣL [m] | G [kN] | Kopplung ans Tragwerk | Lager | Kinematik | Folge |
|---|---|---|---|---|---|---|---|
| C1a | 158 | 0,911 | 0,007 | keine | keines | frei (6 Starrkörperfreiheitsgrade) | Singularität |
| C1b | 178 | 0,720 | 0,006 | keine | keines | frei | Singularität |
| C2 | 179–193 (15) | 170,731 | 1,340 | nur Stab 193 → Kn 6 (RL06) | keines | Pendel um Kn 6 | Singularität + 1,34 kN Zusatzlast auf Seilknoten 6 (> Leuchte 1,0 kN) |

## 4 Querschnitte / Materialien (RF6, summary.json: 17 QS, 14 Mat)

| QS | Verwendung | Befund | Aktion |
|---|---|---|---|
| 1 | 68 Seilstäbe (Typ 9, Seil) | A = 0,38 cm² in RF5, RF6 und Bestand (BEFUND Rev0 G1) | prüfen, ob RF6-Import A korrekt übernommen hat (ANWEIDUNG.docx behauptet 0,02 cm² → **Widerspruch zu BEFUND G1**, per `rfem_read_objects sections` klären) |
| 3→10, 5→4, 9→8, 11→4, 12→4 | 20 Maste (Voute) | unverändert | behalten (1006/1007 nach VAR-A-Patch entfallen) |
| 14 | 17 Hilfsstäbe | b = h = 0 → RF6-Fehler | löschen |
| 15, 16, 17 | 0 Stäbe | unbenutzt | löschen |

## 5 Grenzen und offene Prüfungen

1. RF6-Lager/Gelenke sind im Teilabgleich nicht exportiert (summary.json `not_checked`: „supports and hinges equivalence“). Lagercheck beruht auf RF5-Lagerliste (101–115 gelenkig, 2001–2021 eingespannt). Bestätigung: `python 26_10_06_ID-03-RFEM6_MCP_Bridge_Extended.py` → `rfem_read_objects(kind="nodal_supports")`.
2. Knoten 17 trägt Kommentar „Gelagert“, hat aber kein Lager (BEFUND Rev0 §5) → Kommentar in Arbeitskopie korrigieren.
3. Lage ≈ (Spalte 8) ist Sichtprüfung aus BEFUND Rev0 §5, keine Vermessung.
4. Keine Aussage zu Lasten auf QS-14-Stäben; falls LF-Listen (LF31/32/33/41/52) Hilfsknoten enthalten, vor Löschen bereinigen.

