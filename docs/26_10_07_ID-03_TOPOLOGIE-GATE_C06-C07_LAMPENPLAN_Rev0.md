# TOPOLOGIE-GATE „zwei Fassadenanker statt Pylone“ — Nachweis der RFEM-Objekte aus dem Lampenplan — Rev0

| Feld | Wert |
|---|---|
| Datum | 07.10.2026 · ID-03 |
| Quelle | V1 `7864Halterungen_mit_Lampenplan_Boardinghouse.xlsx` (Drive 1j-GHSEH7x_JsUppBplMaQYvcwje6EhKe), Blatt „Tabelle1“ Spalten Geometer Knoten / Bezeichnung / RFEM Knoten; Messpunkte 7000–7108 in Landeskoordinaten | 
| Zweck | Gate aus Gegencheck 2: betroffene RFEM-IDs für „C06/C07 → Fassadenanker“ anhand der Pläne belegen, bevor Modell B gebaut wird |

## 1 Zuordnung laut Plan (V1, Tabelle1, 1:1 übernommen)

| Geometer | Bezeichnung | RFEM-Knoten lt. Plan | Objekt im Bestand 5e | Folge in Modell B (B-2) |
|---|---|---|---|---|
| 7100 | A05 | 105 | Wandanker, Seil S81 | bleibt |
| 7101 | **C06** | **3006 / 2006** | Mastkopf 3006, Mastfuß 2006, Mast 1006, Seil S19 | 3006 = Fassadenanker (Lager gelenkig), 1006 + 2006 entfallen |
| 7102 | **C07** | **3007 / 2007** | Mastkopf 3007, Mastfuß 2007, Mast 1007, Seil S22 | 3007 = Fassadenanker (Lager gelenkig), 1007 + 2007 entfallen |
| 7103 | A06 | 106 | Wandanker, S21 | bleibt |
| 7104 | C21 | 3021 / 2021 | Mastkopf 3021, Mast 1021, S63 | E3 (Fall A/B 0,60 m) |
| 7105, 7106 | A14 | 114 | Wandanker, S64 | bleibt (VF4 Lochmitte) |
| 7107, 7108 | A13 | 113 | Wandanker, S60 | bleibt (VF4) |
| 7000, 7004 | RL08 | 8 | Ringleuchte Kn 8 | Kontrollpunkt |

Damit sind die zwei zu ersetzenden Pylone eindeutig **1006 (C06)** und **1007 (C07)**; die Seilenden sind 3006 (S19) und 3007 (S22). Das entspricht Patch E7 Rev0 (Variante B-2) und dem Kurzbericht VAR-A (84 Kn / 68 Seile / 18 Maste).

## 2 Höhenkontrolle (neuer Beleg gegen „Mastkopf bleibt“)

Transformation T1: z = −(Z − 445,472).

| Punkt | Z Geometer [m] | z T1 [m] | z Bestand 5e [m] | Δ [m] | Befund |
|---|---|---|---|---|---|
| 7100 → 105 | 445,600 | −0,128 | −0,129 | +0,001 | Anker unverändert |
| 7103 → 106 | 445,200 | +0,272 | +0,262 | +0,010 | Anker unverändert |
| 7107/7108 → 113 | 446,070 | −0,598 | −0,612 | +0,014 | Anker unverändert |
| 7105/7106 → 114 | 446,280 | −0,808 | −0,783 | −0,025 | Anker unverändert |
| **7101 → 3006** | **445,020** | **+0,452** | −0,038 | +0,490 | neuer Punkt, 0,49 m unter altem Mastkopf |
| **7102 → 3007** | **445,020** | **+0,452** | +0,186 | +0,266 | neuer Punkt, 0,27 m unter altem Mastkopf |
| 7104 → 3021 | 444,450 | +1,022 | +0,937 | +0,085 | C21: E3 |

7101 und 7102 liegen auf exakt derselben Höhe 445,020 m, 0,27–0,49 m unter den alten Mastköpfen, obwohl beide Maste unterschiedliche Kopfhöhen hatten. Das ist das Bild zweier auf gleicher Höhe gesetzter Fassadenanker, nicht zweier (geneigter) Mastköpfe. Die Docx-Annahme „Mastkopf, Z = Bestand, ΔZ = 0“ widerspricht der Messung. Die vier Wandanker reproduzieren mit T1 ihre Bestandshöhe auf 1–25 mm; T1 ist damit auch in Z konsistent (VF2 teilweise beantwortet: Einzelhöhen je Punkt, kein pauschaler Offset).

## 3 Gate-Entscheidung

| Gate | Status |
|---|---|
| Betroffene Pylone belegt (1006, 1007; Füße 2006, 2007; Köpfe 3006, 3007) | **ERFÜLLT** (V1 Tabelle1) |
| Fassadenanker-Höhe belegt (z = 0,452 beide) | **ERFÜLLT** (V1 Z-Werte, T1) |
| Variante B-7 („Maste bleiben geneigt“) | widerspricht V1-Höhen und Auftrag → nur mit ausdrücklicher Begründung ID01 |
| Offen | VF1 Lochmitte/Bolzenachse 7101/7102 (Beschlagmaß F7), VF3 C21, VF4 A13/A14 |
