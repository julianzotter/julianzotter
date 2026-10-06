# BLATT 6 — DELTA-MATRIX RF5 ↔ RF6 ↔ VAR-A (Vorlage Rev0, Auftrag 4)

| Feld | Wert |
|---|---|
| Status | VORLAGE · Spalten RF6 leer bis Baseline-Export (Auftrag 1, RUN-RF6-000) und Rechenlauf (RUN-RF6-001) vorliegen |
| Referenzwerte | Spalte „Bestand 5e“ und „VAR-A“ = Kurzbericht VAR-A 23.09. [2] (RF 5.29.01, vorläufig); Einheiten kN, m |
| Toleranz | **E8 offen** – Vorschlag: Verformung ±2 mm, Seilkraft ±0,05 kN, Lagerkraft ±0,05 kN (Kalibrierung Bestand); für VAR-A-Vergleich erst nach E1–E3 |
| Vorzeichen | RFEM-Z positiv nach unten; API-SI (N, m) → kN, m umrechnen |

## 1 Kalibrierung Bestandsgeometrie (RF6 mit Bestand-5e-Geometrie gegen RF5)

| # | Größe | Loading | Bestand 5e (RF5) | RF6 Baseline (M1, A = ?) | RF6 WORKING_CALC (A = 0,38) | Δ RF6−RF5 | Toleranz | Gate |
|---|---|---|---|---|---|---|---|---|
| K1 | max u (Kn 17, Stab 34) [m] | LK100 | 2,085 | | | | ±0,002 | |
| K2 | max N gesamt (S54) [kN] | RK1 | 17,47 | | | | ±0,05 | |
| K3 | max N Bereich RL06–C21 (S18) [kN] | RK1 | 10,53 | | | | ±0,05 | |
| K4 | Tiefpunkt RL06 unter Fixpunkt [m] | LK100 | 1,79 | | | | ±0,01 | |
| K5 | L(LK100) S19 / S22 [m] | LK100 | 3,835 / 8,009 | | | | ±0,002 | |
| K6 | Lagerkraft A05 (105) P_x/P_y/P_z [kN] | RK1 | aus RF5-Export eintragen | | | | ±0,05 | |
| K7 | Σ P_z aller Lager − Σ Eigengewicht [kN] | LK100 | 0 (ΣV = 0) | | | | ±0,01 | Gleichgewicht |

## 2 Variante A (nach Patch E7, Geometrie T1)

| # | Größe | Loading | VAR-A (RF5, [2]) | RF6 VAR-A | Δ | Toleranz | Gate |
|---|---|---|---|---|---|---|---|
| V1 | max u (Kn 17) [m] | LK100 | 2,080 | | | | |
| V2 | max N gesamt (S54) [kN] | RK1 | 17,48 | | | | |
| V3 | max N RL06–C21 (S18) [kN] | RK1 | 11,58 | | | | |
| V4 | L(LK100) S19 / S22 [m] | LK100 | 4,925 / 9,576 | | | | |
| V5 | Lsys S19 / S22 [m] (− Beschlag 0,193, F7) | – | ≈ 4,732 / ≈ 9,383 | | | | |
| V6 | Ankerkraft ex-C06 (3006) x/y/z [kN] | RK1 | 5,24 / 4,60 / 1,07 | | | | |
| V7 | Ankerkraft ex-C07 (3007) x/y/z [kN] | RK1 | 5,75 / 2,36 / 0,46 | | | | |
| V8 | Tiefpunkt RL09 unter Fixpunkt [m] | LK100 | 1,07 | | | | |
| V9 | übrige Seile ΔL / ΔN | LK100/RK1 | ≤ 2,1 mm / ≤ 0,75 kN | | | | |
| V10 | **LK220** max N (1,35·LF10 + 1,50·LF43) [kN] | LK220 | 20,16 (Erg. 2) · η = 0,72 | | | | neu in RF6 |

## 3 Beiblatt Rev2 (Struktur, an P. Kneidinger)

1. Modell-ID + Hash (M1 / M5), RFEM-Version, Run-ID, Datum.
2. Geometriebasis (E1) und Patch-Protokoll (E7 angewendet ja/nein, Kontrollwerte 84 Kn / 68 Seile / 18 Maste).
3. Delta-Matrix §1 (Kalibrierung PASS/FAIL je Zeile) und §2.
4. Offene Entscheidungen E1–E8, Status.
5. Freigabestatus: VORLÄUFIG · FREIGABE NEIN · BESTELLREIF NEIN.
