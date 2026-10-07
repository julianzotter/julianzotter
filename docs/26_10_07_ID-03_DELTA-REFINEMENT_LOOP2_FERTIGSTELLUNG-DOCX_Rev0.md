# DELTA-REFINEMENT LOOP 2 — Docx „26_10_07_SEILSTATIK-FERTIGSTELLUNG“ gegen Originalaufgabe (Ergänzung 4) und EINGABEDATEN_RF6_v0.1 — Rev0

| Feld | Wert |
|---|---|
| Datum | 07.10.2026 · ID-03 |
| Prüfobjekt | Drive 1uMx6_npKkPO_M-qDDikKOuMN0-Fw6Wxh, `26_10_07_SEILSTATIK-FERTIGSTELLUNG.docx` (20 166 B, erstellt 07.10. 08:45 UTC), Fremdassistent; Inhalt: „Klärung Bestandsmessung“, „Entscheidung Fall B“, `BOEBLINGEN_FALL_B_DECISION.md`, XLSX-Struktur V02, Ausführungsreihenfolge, Erwartungswerte |
| Originalaufgabe | GZ 26_001: Ergänzung 4 zur Bestandsstatik 2015 — Maste C06/C07 entfallen, Ersatz durch Fassadenanker, neue Seillängen S19/S22; Nachweis DIN EN 1990/1991/1993-1-11 + NA-DE; prüffähig, analog Bestandsstatik |
| Referenzen | Quellenlog Vermesser Rev0 (V1–V9, T1–T3, VF1–VF5), Patch E7 Rev0, Loop 1 (Fremddaten „Fall B“), Sperrliste Rev0, EINGABEDATEN_RF6_v0.1 (Hashes im MANIFEST) |
| Ergebnis | **Docx nicht freigabefähig.** Es ersetzt die Aufgabe (Fassadenanker) durch „geneigte Maste C06/C07“, nutzt den G3-Siebenpunkt (T2, CONFLICT) als Randbedingung, fordert Formfindung und LF10 = 11,2 kN und wiederholt den gesperrten Skriptpfad. Entscheidungen E1/E2/E3 bleiben bei ID01. Die fertigen RFEM-6-Eingabetabellen liegen im Anhang (Modell A vollständig, Modell B in zwei Varianten). |

## 1 Befunde D1–D12 (Docx-Aussage → Beleg → Grad)

| # | Docx | Belegte Lage | Grad |
|---|---|---|---|
| D1 | „7 gemessene Positionen = verbindliche BCs“ (105, 106, 113, 114, 3006, 3007, 3021 mit G3-Koordinaten) | Dieselben Zahlen wie Loop 1 „Fall B“ = transformed_nodes.csv (V8) = Transformation T2 (7-Punkt-Starrfit, RMSE 0,62–0,65 m), Status **CONFLICT**; T1 (VAR-A, 4 Anker, RMS 0,098 m) ist Kanon-Empfehlung. E1 offen, Freigabeblock im Docx leer. | S |
| D2 | „Mastkopf C06/C07, Maste M1006/M1007 bleiben geneigt (3,4° / 7,6°)“ | Ergänzung 4: C06/C07 **entfallen**, 7101/7102 = Fassadenanker (V9-Mapping, Patch E7: Stäbe 1006/1007 löschen, Lager 2006/2007 entfernen, 3006/3007 gelenkig, z 0,452). Eine Mastneigung existiert für entfallene Maste nicht. Docx-Z −0,038/0,186 = Bestandsmastkopf, nicht Ankerhöhe (VF2). | **S, Aufgabenwidrig** |
| D3 | „Wandanker 105 sitzt 68 cm anders als im Bestandsplan“ (ΔXY 0,685/0,352/…) | Unter T1 weichen dieselben Anker 0,037/0,040/0,089/0,057 m ab (V9 §2). Die 0,15–0,68 m sind T2-Artefakt (Rotation 0,23°, Translation). Physisch unveränderte Anker dürfen nicht verschoben werden. | S |
| D4 | ΔXY-Tabelle: 113 0,132 · 3006 0,339 · 3007 0,200 | Nachgerechnet aus den Docx-eigenen Koordinaten: 113 **0,627**, 3006 **0,514**, 3007 **1,158** (√(ΔX²+ΔY²)); 105/106/114/3021 stimmen. Docx-Neigungstabelle nennt selbst 0,514/1,158/0,322 → interner Widerspruch. | M |
| D5 | Neigung 3,4° / 7,6° / 2,1°, Mastlängen 8,715 / 8,777 / 8,706 m | Rechnerisch korrekt für G3-Kopf gegen Bestandsfuß 2006/2007/2021 (Höhe 8,700 m): 3,38° / 7,58° / 2,12°. Gilt nur, wenn die Maste bleiben (D2) — für 1021 (C21) relevant = E3 Fall A/B. | ok (bedingt) |
| D6 | „Randbedingungen für die Formfindung“, „Theorie III. O. + Formfindung“ | Kanon P1–P3: keine Formfindung, keine Vorspannung; Geometrie = Nulllage, Sv = N(LK100) ist Ergebnis. | S |
| D7 | „LF10-Fix 11,2 kN statt 30 kN (14 × 0,80 kN)“ | model.db M5: LF10 = 1 Knotenlast Fz +1,000 kN auf Kn 1–30 (Σ 30,0 kN). Laständerung ohne AG/Prüfstatiker unzulässig (Sperrliste Rev0). | S |
| D8 | XLSX V02: 14 Material / 43 Lager / 20 LK; „Erwartet 14/43/20“ | Loop 1: U10 hat 6 Materialien, 27 Lagerobjekte (35 Knoten, keine Lager an 3001–3005), 21 LK (+ LK220 fehlend). Docx-Erwartungswerte prüfen gegen falsche Sollwerte. | S |
| D9 | Pipeline rf5_export → boeb_bereinigung → boeb_rf6_generator → delta_matrix; Quelle `13bb_ausfuehrungsstatik_1.rf5`; RFEM 6.11, dlubal.api 2.11 | Sperrliste Rev0 (alle vier Skripte). Quelle = U6a (Vorläufer), nicht 5e/U10. Installiert: RFEM 6.13.0001, Server verlangt Client 2.13.1 (Quellenlog RF6 E5). | S |
| D10 | PFEIFER_MAPPING η S31 0,064 · S32 0,085 · S33 0,128 · S81 0,106 „OK“ | η = Sv/47 kN (Z_Bk). Zulässig ist F_Rd = 46,1/(1,5·1,1) = 27,9 kN → 0,108 / 0,143 / 0,215 / 0,179. Sv-Werte selbst unbelegt (Loop 1 §1 Tab. 11). Konstanten „127 mm / 156 mm / Ek 0,00035“ ohne Quelle (U9 nicht beschafft, F7). | S |
| D11 | „P0: C07 (3007) u_res 52,21 mm > 50 mm Gabelspannschloss“ | Unbelegt (kein Rechenlauf existiert, M5 ohne Ergebnisse). In Modell B ist 3007 Lagerknoten (u = 0). Bestand LK100: u_Kn17 = 2,085 m → 50-mm-Schwelle für Netzknoten sinnlos; Stellweg ist Montagemaß, kein Verformungskriterium. | S |
| D12 | „Alle anderen Knoten (…, 3021) bleiben aus dem Bestandsmodell“ + 3021 in der 7er-Liste; „Konvergenz 4–5 Iterationen“, „Δ ≤ 0,01 %“, „1 Arbeitstag“, „Thomas Blessing“ | Interner Widerspruch 3021. Konvergenz/Gleichgewichtswerte sind Erwartungen ohne Lauf. Geometer: V1 nennt „Blessing“, 11./13.02.2026 ✓; Vorname nicht belegt. | M/U |

Grad: S = Sperre, M = Mangel (korrigierbar), U = unbelegt.

## 2 Fokus Originalaufgabe: was Ergänzung 4 tatsächlich braucht

| Baustein | Stand | Quelle |
|---|---|---|
| Modell A (Bestand 5e, Kalibrierziel u_Kn17 2,085 m, N_S54 17,47 kN) | Eingabetabellen vollständig (Anhang A1–A9) | U10, M5 |
| Modell B (Ergänzung 4) | Patch E7 Rev0 = Variante B-2 (Anhang B1/B2): nur 3006/3007 neu (Fassadenanker, z 0,452), Maste 1006/1007 + Fuß 2006/2007 entfallen, Lager 3006/3007 gelenkig wie 105 | Kurzbericht VAR-A 23.09., V9 |
| Nachweisgrößen | N_max je Seil (η gegen F_Rd 27,9 kN), Ankerkräfte 3006/3007 (→ Ankerbemessung), u (LK100/101), neue Längen S19/S22 aus Modell-B-Geometrie (Nulllage) + Beschlagmaß F7 | DIN EN 1993-1-11 §6.2, Blatt 6 Vorlage Rev0 |
| Lasten | 1:1 Bestand (A7–A9), LK220 ergänzen (E4) | M5, BEFUND Rev0 K7 |
| Offen (ID01) | E1 Geometriebasis T1 vs T2 · E2 Maste entfallen (Aufgabenprämisse, Docx widerspricht) · E3 C21 0,60 m · E4 EK1/LK220 · E6 S35 · E7 g · E9 Schubsteifigkeit QS 10/11/12 · F7 Beschlagmaß · VF1–VF5 an Geometer | Quellenlog RF6/Vermesser |

Entscheidungsvorlage E1/E2 (eine Zeile je Option, Empfehlung zuerst):

| Option | Geometrie Modell B | Maste C06/C07 | Konsequenz |
|---|---|---|---|
| **B-2 (empfohlen)** | T1: 3006/3007 aus 7101/7102, Anker 105/106/113/114 = Bestand | entfallen | entspricht Auftrag; 84 Kn / 86 St; Delta-Matrix Blatt 6 direkt vergleichbar mit Bestand |
| B-7 (Docx) | T2: 7 Knoten verschoben | bleiben geneigt | widerspricht Auftrag; Ankerverschiebung ist Artefakt; neue Geometer-Freigabe (V7-Revision) nötig; Mastnachweis 1006/1007 zusätzlich |
| B-2 + E3 Fall B | wie B-2, zusätzlich 3021 (C21) auf 7104 (0,60 m, Mast 1021 bleibt, 2,1°) | entfallen | nur wenn VF3 bestätigt (reale Verschiebung, nicht Messtoleranz) |

## 3 Loop-Ergebnis

- Übernommen aus dem Docx: nichts. Rechnerisch bestätigt: Neigungswinkel/Längen (D5) als Kennwerte für E3 (C21).
- Korrigiert: drei ΔXY-Werte (D4), η-Bezug (D10).
- Neu geliefert: Anhang mit allen RFEM-6-Eingabetabellen (Modell A vollständig; Modell B Varianten B-2 und B-7 nebeneinander), erzeugt aus den gehashten CSV (`tools/26_10_07_ID-03_render_eingabetabellen_md.py`).
- Loop 3 (nach E1/E2 durch ID01): Generator Modell A → Kalibrierung K1–K7 → Modell B → Blatt 6. Vorher lokal: `api_write_check.py`, E9, P2 in WORKING_CALC.

---

# ANHANG — FERTIGE RFEM-6-EINGABETABELLEN (EINGABEDATEN_RF6_v0.1)


Quellen (SHA-256): input_3.json 394820ebeada…; lines.csv 14b77cef4301…; model.db 773d7b65de5a…; patch_vara_rev0.json 115d7587f0e2…

Regeln: keine Vorspannung (Sv = N(LK100) ist Ergebnis), keine Formfindung, Bestandslasten 1:1. Einheiten m, kN, kN/m, K, cm², cm⁴.

## A Modell A — Bestand 5e (Quelle U10 RF5-COM-Export; Lasten model.db M5)

### A1 Knoten (86) — RFEM lokal, Z positiv nach unten [m]

| Kn | X [m] | Y [m] | Z [m] |
|---|---|---|---|
| 1 | 16.361 | 1.928 | 0.537 |
| 2 | 24.174 | 18.489 | 0.237 |
| 3 | 44.155 | 22.100 | 0.274 |
| 4 | 56.034 | 37.552 | 0.145 |
| 5 | 76.823 | 44.657 | 0.450 |
| 6 | 93.933 | 61.204 | 0.284 |
| 7 | 103.560 | 79.605 | 0.405 |
| 8 | 116.629 | 67.891 | 0.350 |
| 9 | 138.936 | 55.525 | 0.177 |
| 10 | 153.008 | 40.669 | 0.616 |
| 11 | 121.677 | 83.646 | -0.103 |
| 12 | 141.682 | 88.099 | -0.475 |
| 13 | 151.366 | 102.000 | -0.272 |
| 14 | 168.308 | 107.836 | -0.565 |
| 15 | 181.416 | 123.367 | -0.600 |
| 16 | 205.154 | 113.761 | -0.400 |
| 17 | 203.032 | 130.830 | -0.600 |
| 18 | 219.184 | 149.059 | -1.000 |
| 19 | 241.683 | 157.884 | -1.200 |
| 20 | 255.873 | 175.720 | -1.650 |
| 21 | 277.366 | 182.392 | -1.600 |
| 22 | 284.004 | 193.779 | -2.200 |
| 23 | 297.358 | 189.952 | -1.900 |
| 24 | 309.259 | 193.681 | -2.500 |
| 25 | 308.535 | 209.204 | -3.150 |
| 26 | 298.467 | 209.615 | -3.000 |
| 27 | 220.448 | 97.652 | 0.050 |
| 28 | 238.003 | 89.312 | -0.300 |
| 29 | 170.654 | 33.408 | 0.400 |
| 30 | 181.204 | 17.175 | 1.290 |
| 101 | 18.540 | -4.834 | 0.122 |
| 102 | 47.989 | 18.036 | 0.033 |
| 103 | 55.065 | 41.060 | -0.194 |
| 104 | 80.581 | 40.388 | -0.128 |
| 105 | 122.596 | 57.411 | -0.129 |
| 106 | 151.487 | 37.125 | 0.262 |
| 107 | 141.563 | 82.660 | -1.251 |
| 108 | 182.304 | 110.361 | -0.890 |
| 109 | 254.304 | 182.149 | -2.073 |
| 110 | 275.525 | 193.698 | -2.403 |
| 111 | 294.001 | 209.147 | -3.153 |
| 112 | 217.051 | 152.155 | -1.433 |
| 113 | 172.126 | 36.292 | -0.612 |
| 114 | 172.082 | 11.240 | -0.783 |
| 115 | 249.524 | 55.359 | -0.883 |
| 330 | 123.243 | 58.165 | -0.000 |
| 2001 | -0.000 | 0.000 | 8.700 |
| 2002 | 23.002 | 20.153 | 8.618 |
| 2003 | 80.004 | 55.046 | 8.529 |
| 2004 | 93.408 | 79.242 | 8.372 |
| 2005 | 106.465 | 81.548 | 8.280 |
| 2006 | 141.809 | 58.051 | 8.662 |
| 2007 | 160.376 | 43.764 | 8.886 |
| 2008 | 120.222 | 85.326 | 8.232 |
| 2009 | 148.945 | 105.034 | 7.950 |
| 2010 | 175.577 | 123.721 | 7.803 |
| 2011 | 201.958 | 110.490 | 7.747 |
| 2012 | 220.962 | 113.241 | 7.807 |
| 2014 | 243.467 | 155.695 | 7.157 |
| 2015 | 277.617 | 178.265 | 6.743 |
| 2016 | 288.414 | 186.772 | 6.476 |
| 2017 | 314.556 | 188.983 | 5.747 |
| 2018 | 308.210 | 221.137 | 4.836 |
| 2019 | 218.305 | 94.756 | 8.057 |
| 2020 | 240.947 | 92.467 | 8.197 |
| 2021 | 192.946 | 16.267 | 9.637 |
| 3001 | -0.000 | -0.000 | 0.000 |
| 3002 | 23.002 | 20.153 | -0.082 |
| 3003 | 80.004 | 55.046 | -0.171 |
| 3004 | 93.408 | 79.242 | -0.328 |
| 3005 | 106.465 | 81.548 | -0.420 |
| 3006 | 141.809 | 58.051 | -0.038 |
| 3007 | 160.376 | 43.764 | 0.186 |
| 3008 | 120.222 | 85.326 | -0.468 |
| 3009 | 148.945 | 105.034 | -0.750 |
| 3010 | 175.577 | 123.721 | -0.897 |
| 3011 | 201.958 | 110.490 | -0.953 |
| 3012 | 220.962 | 113.241 | -0.893 |
| 3014 | 243.467 | 155.695 | -1.543 |
| 3015 | 277.617 | 178.265 | -1.957 |
| 3016 | 288.414 | 186.772 | -2.224 |
| 3017 | 314.556 | 188.983 | -2.753 |
| 3018 | 308.210 | 221.137 | -3.664 |
| 3019 | 218.305 | 94.756 | -0.643 |
| 3020 | 240.947 | 92.467 | -0.503 |
| 3021 | 192.946 | 16.267 | 0.937 |

### A2 Stäbe (88) — Typ 9 = Seil (nur Zug), Typ 1 = Balken; QS i → j = Voute

| Stab | Typ | Kn i | Kn j | QS i | QS j | L [m] | Linie RF5 |
|---|---|---|---|---|---|---|---|
| 1 | Seil | 101 | 1 | 1 | 1 | 7.117 | 3 |
| 2 | Seil | 3001 | 1 | 1 | 1 | 16.483 | 2 |
| 3 | Seil | 2 | 1 | 1 | 1 | 18.314 | 4 |
| 4 | Seil | 3002 | 2 | 1 | 1 | 2.060 | 6 |
| 5 | Seil | 3 | 2 | 1 | 1 | 20.305 | 7 |
| 6 | Seil | 3 | 102 | 1 | 1 | 5.592 | 8 |
| 7 | Seil | 4 | 3 | 1 | 1 | 19.491 | 9 |
| 8 | Seil | 4 | 103 | 1 | 1 | 3.655 | 10 |
| 9 | Seil | 5 | 4 | 1 | 1 | 21.972 | 11 |
| 10 | Seil | 104 | 5 | 1 | 1 | 5.717 | 12 |
| 11 | Seil | 5 | 3003 | 1 | 1 | 10.883 | 13 |
| 12 | Seil | 6 | 3003 | 1 | 1 | 15.236 | 15 |
| 13 | Seil | 6 | 7 | 1 | 1 | 20.768 | 18 |
| 14 | Seil | 3005 | 7 | 1 | 1 | 3.591 | 19 |
| 15 | Seil | 3004 | 7 | 1 | 1 | 10.185 | 17 |
| 16 | Seil | 8 | 6 | 1 | 1 | 23.661 | 20 |
| 17 | Seil | 330 | 8 | 1 | 1 | 11.768 | 23 |
| 18 | Seil | 330 | 9 | 1 | 1 | 15.914 | 27 |
| 19 | Seil | 3006 | 9 | 1 | 1 | 3.832 | 29 |
| 20 | Seil | 10 | 9 | 1 | 1 | 20.467 | 32 |
| 21 | Seil | 10 | 106 | 1 | 1 | 3.873 | 36 |
| 22 | Seil | 10 | 3007 | 1 | 1 | 8.003 | 37 |
| 23 | Seil | 11 | 8 | 1 | 1 | 16.550 | 25 |
| 24 | Seil | 11 | 3008 | 1 | 1 | 2.252 | 26 |
| 25 | Seil | 11 | 12 | 1 | 1 | 20.498 | 28 |
| 26 | Seil | 12 | 107 | 1 | 1 | 5.495 | 82 |
| 27 | Seil | 13 | 12 | 1 | 1 | 16.943 | 33 |
| 28 | Seil | 13 | 3009 | 1 | 1 | 3.911 | 35 |
| 29 | Seil | 13 | 14 | 1 | 1 | 17.921 | 38 |
| 30 | Seil | 14 | 108 | 1 | 1 | 14.226 | 101 |
| 31 | Seil | 15 | 14 | 1 | 1 | 20.323 | 41 |
| 32 | Seil | 15 | 3010 | 1 | 1 | 5.857 | 43 |
| 33 | Seil | 15 | 17 | 1 | 1 | 22.868 | 44 |
| 34 | Seil | 17 | 16 | 1 | 1 | 17.202 | 47 |
| 35 | Seil | 3011 | 16 | 1 | 1 | 4.606 | 46 |
| 36 | Seil | 3012 | 16 | 1 | 1 | 15.824 | 49 |
| 37 | Seil | 17 | 18 | 1 | 1 | 24.358 | 48 |
| 38 | Seil | 112 | 18 | 1 | 1 | 3.784 | 51 |
| 39 | Seil | 19 | 18 | 1 | 1 | 24.169 | 53 |
| 40 | Seil | 19 | 3014 | 1 | 1 | 2.845 | 54 |
| 41 | Seil | 19 | 20 | 1 | 1 | 22.797 | 56 |
| 42 | Seil | 20 | 109 | 1 | 1 | 6.631 | 57 |
| 43 | Seil | 20 | 21 | 1 | 1 | 22.505 | 58 |
| 44 | Seil | 3015 | 21 | 1 | 1 | 4.150 | 59 |
| 45 | Seil | 21 | 22 | 1 | 1 | 13.194 | 62 |
| 46 | Seil | 22 | 110 | 1 | 1 | 8.482 | 65 |
| 47 | Seil | 23 | 22 | 1 | 1 | 13.895 | 87 |
| 48 | Seil | 23 | 3016 | 1 | 1 | 9.498 | 66 |
| 49 | Seil | 24 | 23 | 1 | 1 | 12.486 | 68 |
| 50 | Seil | 24 | 3017 | 1 | 1 | 7.085 | 75 |
| 51 | Seil | 23 | 3017 | 1 | 1 | 17.246 | 71 |
| 52 | Seil | 26 | 22 | 1 | 1 | 21.462 | 85 |
| 53 | Seil | 26 | 111 | 1 | 1 | 4.493 | 67 |
| 54 | Seil | 26 | 3018 | 1 | 1 | 15.104 | 22 |
| 55 | Seil | 25 | 3018 | 1 | 1 | 11.948 | 73 |
| 56 | Seil | 25 | 26 | 1 | 1 | 10.078 | 69 |
| 57 | Seil | 24 | 25 | 1 | 1 | 15.553 | 72 |
| 58 | Seil | 3012 | 27 | 1 | 1 | 15.626 | 89 |
| 59 | Seil | 27 | 28 | 1 | 1 | 19.439 | 91 |
| 60 | Seil | 29 | 113 | 1 | 1 | 3.392 | 95 |
| 61 | Seil | 10 | 29 | 1 | 1 | 19.083 | 94 |
| 62 | Seil | 29 | 30 | 1 | 1 | 19.381 | 96 |
| 63 | Seil | 30 | 3021 | 1 | 1 | 11.782 | 98 |
| 64 | Seil | 30 | 114 | 1 | 1 | 11.079 | 97 |
| 65 | Seil | 27 | 3019 | 1 | 1 | 3.669 | 90 |
| 66 | Seil | 28 | 115 | 1 | 1 | 35.859 | 93 |
| 67 | Seil | 28 | 3020 | 1 | 1 | 4.320 | 92 |
| 81 | Seil | 105 | 330 | 1 | 1 | 1.002 | 81 |
| 1001 | Balken | 3001 | 2001 | 3 | 10 | 8.700 | 135 |
| 1002 | Balken | 3002 | 2002 | 5 | 4 | 8.700 | 136 |
| 1003 | Balken | 3003 | 2003 | 11 | 4 | 8.700 | 1 |
| 1004 | Balken | 3004 | 2004 | 5 | 4 | 8.700 | 138 |
| 1005 | Balken | 3005 | 2005 | 5 | 4 | 8.700 | 139 |
| 1006 | Balken | 3006 | 2006 | 5 | 4 | 8.700 | 142 |
| 1007 | Balken | 3007 | 2007 | 5 | 4 | 8.700 | 143 |
| 1008 | Balken | 3008 | 2008 | 5 | 4 | 8.700 | 141 |
| 1009 | Balken | 3009 | 2009 | 5 | 4 | 8.700 | 145 |
| 1010 | Balken | 3010 | 2010 | 5 | 4 | 8.700 | 146 |
| 1011 | Balken | 3011 | 2011 | 5 | 4 | 8.700 | 148 |
| 1012 | Balken | 3012 | 2012 | 5 | 4 | 8.700 | 149 |
| 1014 | Balken | 3014 | 2014 | 5 | 4 | 8.700 | 152 |
| 1015 | Balken | 3015 | 2015 | 5 | 4 | 8.700 | 153 |
| 1016 | Balken | 3016 | 2016 | 5 | 4 | 8.700 | 154 |
| 1017 | Balken | 3017 | 2017 | 9 | 8 | 8.500 | 76 |
| 1018 | Balken | 3018 | 2018 | 9 | 8 | 8.500 | 78 |
| 1019 | Balken | 3019 | 2019 | 5 | 4 | 8.700 | 150 |
| 1020 | Balken | 3020 | 2020 | 5 | 4 | 8.700 | 151 |
| 1021 | Balken | 3021 | 2021 | 12 | 4 | 8.700 | 5 |

### A3 Materialien (6) — E, G in kN/cm²

| Mat | Bezeichnung | E | G | ν | γ [kN/m³] | α_T [1/K] | γ_M | Hinweis |
|---|---|---|---|---|---|---|---|---|
| 1 | rundlitze | Z-14.7-411 | 90000.0 | 5000.0 | 8.0 | 80.0 | 1.6e-05 | 1.1 | nicht verwendet, nu = 8,0 und E = 900 GPa sind Bestandsfehler |
| 2 | Baustahl S 235 JR | DIN EN 10025-2:2004-11 | 21000.0 | 8076.923 | 0.3 | 78.5 | 1.2e-05 | 1.0 |  |
| 3 | Baustahl S 235 | DIN 18800:1990-11 | 21000.0 | 8100.0 | 0.2963 | 78.5 | 1.2e-05 | 1.1 |  |
| 4 | S 235 J2 G3 | 21000.0 | 8100.0 | 0.2963 | 78.5 | 1.2e-05 | 1.1 |  |
| 5 | Seil PE (Pfeifer) | Z-14.7-411 | 13000.0 | 5000.0 | 0.3 | 80.0 | 1.6e-05 | 1.1 |  |
| 6 | S 235 J2 G3 | 21000.0 | 8100.0 | 0.2963 | 78.5 | 1.2e-05 | 1.1 |  |

### A4 Querschnitte (13) — cm², cm⁴

| QS | Bezeichnung | Mat | A | Ay | Az | It | Iy | Iz | Verwendung |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Seil PE 5 | Pfeifer | 5 | 0.38 | 0.3192 | 0.3192 | 0.0423 | 0.0211 | 0.0211 | Seile |
| 2 | KR 405/185/35/35/0 | 2 | 271.25 | 0.0 | 0.0 | 1094.6034 | 19507.651 | 19507.651 | Maste (Voute) |
| 3 | KR 200/82/35/35/0 | 2 | 127.4 | 0.0 | 0.0 | 507.2904 | 2391.9292 | 2357.4612 | Maste (Voute) |
| 4 | KR 405/185/35/35/0 | 6 | 271.25 | 0.0 | 0.0 | 1094.6034 | 19507.651 | 19507.651 | Maste (Voute) |
| 5 | KR 200/82/35/35/0 | 6 | 127.4 | 0.0 | 0.0 | 507.2904 | 2391.9292 | 2357.4612 | Maste (Voute) |
| 6 | KR 399.1/182/35/35/0 | 6 | 267.1162 | 118.3502 | 118.3583 | 1077.7238 | 18672.2871 | 18668.2558 | Maste (Voute) |
| 7 | Rohr 247/36 | 2 | 238.6354 | 120.6344 | 120.6344 | 27333.8944 | 13666.9472 | 13666.9472 | Maste (Voute) |
| 8 | Rohr 355.6/24 | 2 | 250.0205 | 124.3831 | 124.3831 | 69089.7749 | 34544.8875 | 34544.8875 | Maste (Voute) |
| 9 | Rohr 247/24 | 2 | 168.1381 | 84.0049 | 84.0049 | 21145.462 | 10572.731 | 10572.731 | Maste (Voute) |
| 10 | KR 399.1/182/35/35/0 | 2 | 267.1162 | 118.3502 | 118.3583 | 1077.7238 | 18672.2871 | 18668.2558 | Maste (Voute) |
| 11 | KR 202.1/83.1/35/35/0 | 6 | 128.8674 | 62.2892 | 62.5265 | 513.2791 | 2466.6329 | 2431.8023 | Maste (Voute) |
| 12 | KR 201.2/82.6/35/35/0 | 6 | 128.2267 | 62.0361 | 62.274 | 510.6643 | 2433.8255 | 2399.1533 | Maste (Voute) |
| 13 | KR 200.3/82.1/35/35/0 | 6 | 127.6077 | 61.7917 | 62.0302 | 508.138 | 2402.4108 | 2367.8875 | Maste (Voute) |

### A5 Lager (27 Objekte, 35 Knoten) — fest/frei, Drehung des Lager-Bezugssystems um Z

| Lager | Knoten | u_x | u_y | u_z | φ_x | φ_y | φ_z | Drehung Z [°] |
|---|---|---|---|---|---|---|---|---|
| 2 | 101-106 | fest | fest | fest | frei | frei | fest | -45.00 |
| 5 | 109,111 | fest | fest | fest | frei | frei | fest | 45.00 |
| 6 | 115 | fest | fest | fest | frei | frei | fest | 0.00 |
| 7 | 2011,2012,2020 | fest | fest | fest | fest | fest | fest | 48.00 |
| 8 | 2021 | fest | fest | fest | fest | fest | fest | 4.00 |
| 11 | 2019 | fest | fest | fest | fest | fest | fest | 53.00 |
| 18 | 2002 | fest | fest | fest | fest | fest | fest | -55.47 |
| 19 | 2001 | fest | fest | fest | fest | fest | fest | -20.50 |
| 25 | 2018 | fest | fest | fest | fest | fest | fest | 90.00 |
| 26 | 2017 | fest | fest | fest | fest | fest | fest | 110.00 |
| 27 | 110 | fest | fest | fest | frei | frei | fest | 45.00 |
| 28 | 112 | fest | fest | fest | frei | frei | fest | 45.00 |
| 29 | 114 | fest | fest | fest | frei | frei | fest | 45.00 |
| 30 | 113 | fest | fest | fest | frei | frei | fest | 45.00 |
| 31 | 107 | fest | fest | fest | frei | frei | fest | 45.00 |
| 32 | 108 | fest | fest | fest | frei | frei | fest | 45.00 |
| 33 | 2003 | fest | fest | fest | fest | fest | fest | -55.50 |
| 34 | 2004 | fest | fest | fest | fest | fest | fest | -138.25 |
| 35 | 2005 | fest | fest | fest | fest | fest | fest | 34.19 |
| 36 | 2006 | fest | fest | fest | fest | fest | fest | -124.95 |
| 37 | 2007 | fest | fest | fest | fest | fest | fest | 55.12 |
| 38 | 2008 | fest | fest | fest | fest | fest | fest | 124.50 |
| 39 | 2009 | fest | fest | fest | fest | fest | fest | 123.64 |
| 40 | 2010 | fest | fest | fest | fest | fest | fest | 125.66 |
| 41 | 2014 | fest | fest | fest | fest | fest | fest | 124.50 |
| 42 | 2015 | fest | fest | fest | fest | fest | fest | -86.27 |
| 43 | 2016 | fest | fest | fest | fest | fest | fest | 176.87 |

### A6 Rechenparameter (RF5-Einstellungen U10)

| Parameter | Wert | Hinweis |
|---|---|---|
| MaxIterations | 100 |  |
| LoadCaseIncrements | 5 |  |
| LoadCombinationIncrements | 5 |  |
| MaximumIncreasingLoading | 1000 |  |
| MemberDivisionsForResultDiagram | 10 |  |
| SpecialMemberDivisions | 10 |  |
| MemberDivisionsForMaxMin | 10 |  |
| FeMeshSubdivisions | 3 |  |
| NewtonRaphsonPickard | 5 |  |
| DivisionForMembersWithNodes | False |  |
| ShearStiffness | True |  |
| LargeDeformationDivisions | False |  |
| ModifyStiffness | True |  |
| ConsiderExtraOptions | True |  |
| IgnoreRotationDegreesOfFreedom | False |  |
| CheckForcesAndMoments | True |  |
| StressOnBeams | False |  |
| NonsymmetricDirectSolver | False |  |
| ChangeStandardSettings | False |  |
| ConvergencePrecision | 0.0 |  |
| InstabilityDetection | 0.0 |  |
| DynamicRelaxationTimeStep | 0.0 |  |
| IterativeCalculationRobustness | 0.0 |  |
| MinimumInitialStrain | 0.0 |  |
| AlwaysUseMinimumStrain | False |  |
| solver_code | 1 |  |
| theory_code | 1 |  |
| theorie | III. Ordnung, Newton-Raphson, g = 10,00 m/s² | RF5-Ausdruck via BEFUND Rev0 §6 (E7 offen) |

### A7 Knotenlasten (17) — kN, RFEM lokal (Z nach unten positiv)

| LF | Nr | F_x | F_y | F_z | n | Knoten |
|---|---|---|---|---|---|---|
| 10 | 1 | 0.0 | 0.0 | 1.0 | 30 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30 |
| 30 | 1 | 0.021 | 0.0 | 0.0 | 31 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,330 |
| 31 | 1 | -0.021 | 0.0 | 0.0 | 28 | 1,2,3,4,5,6,7,8,9,10,11,13,14,16,17,18,19,20,21,22,23,24,25,26,27,28,30,113 |
| 31 | 2 | -0.021 | 0.0 | 0.0 | 1 | 1 |
| 32 | 1 | 0.021 | 0.0 | 0.0 | 29 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,25,26,27,28,330,3012 |
| 33 | 1 | 0.0 | -0.021 | 0.0 | 29 | 1,2,3,4,5,6,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,330 |
| 40 | 1 | 0.0 | 0.0 | 0.065 | 30 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30 |
| 41 | 1 | 0.0 | 0.0 | 0.029 | 29 | 1,2,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30 |
| 43 | 1 | 0.0 | 0.0 | 1.5 | 30 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30 |
| 50 | 1 | 0.0235 | 0.0 | 0.0 | 30 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30 |
| 51 | 1 | -0.024 | 0.0 | 0.0 | 30 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30 |
| 52 | 1 | 0.0 | 0.024 | 0.0 | 30 | 1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,3002 |
| 53 | 1 | 0.0 | -0.024 | 0.0 | 30 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30 |
| 60 | 1 | 0.010599999 | 0.0 | 0.0 | 30 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30 |
| 61 | 1 | -0.011 | 0.0 | 0.0 | 30 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30 |
| 62 | 1 | 0.0 | 0.011 | 0.0 | 30 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30 |
| 63 | 1 | 0.0 | -0.011 | 0.0 | 30 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30 |

### A8 Stablasten (18) — kN/m bzw. ΔT [K]; Richtungscode RF6-intern (gegen RF5-Ausdruck prüfen)

| LF | LF-Name | Nr | Art | Wert | Richtung | n | Stäbe |
|---|---|---|---|---|---|---|---|
| 10 | Eigengewicht Ausbauzustand | 1 | Streckenlast_kN_m | 0.00148 | 16 | 29 | 2,4,5,9,11,12,14,20,22,23,24,27,28,29,32,34,39,40,41,44,45,49,50,54,55,59,62,63,65 |
| 20 | Temperatur +10 | 1 | Temperatur_dT_K | 10.0 | 2 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 21 | temperatur + 57 | 1 | Temperatur_dT_K | 57.0 | 2 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 22 | temperatur -34 | 1 | Temperatur_dT_K | -34.0 | 2 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 30 | wind x | 1 | Streckenlast_kN_m | 0.0048 | 11 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 31 | wind -x | 1 | Streckenlast_kN_m | -0.0048 | 14 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 32 | wind y | 1 | Streckenlast_kN_m | 0.0048 | 15 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 33 | wind -y | 1 | Streckenlast_kN_m | -0.0048 | 15 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 40 | raueis rd2 | 1 | Streckenlast_kN_m | 0.009 | 16 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 41 | raueis rd2 wind leitend | 1 | Streckenlast_kN_m | 0.0045 | 16 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 50 | wind auf eis x | 1 | Streckenlast_kN_m | 0.0303 | 14 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 51 | wind auf eis -x | 1 | Streckenlast_kN_m | -0.0303 | 14 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 52 | wind auf eis y | 1 | Streckenlast_kN_m | 0.0303 | 15 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 53 | wind auf eis -y | 1 | Streckenlast_kN_m | -0.03 | 15 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 60 | wind auf eis x rd2 leitend | 1 | Streckenlast_kN_m | 0.01395 | 14 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 61 | wind auf eis -x rd2 leitend | 1 | Streckenlast_kN_m | -0.01395 | 14 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 62 | wind auf eis y rd2 leitend | 1 | Streckenlast_kN_m | 0.014 | 15 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |
| 63 | wind auf eis -y rd2 leitend | 1 | Streckenlast_kN_m | -0.014 | 15 | 67 | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,81 |

### A9 Lastfälle (19) und Lastkombinationen (21 + LK220 fehlend)

| Typ | Nr | Name | Kategorie-ID | Definition / Faktoren | Quelle |
|---|---|---|---|---|---|
| LF | 10 | Eigengewicht Ausbauzustand | 11 | Eigengewicht automatisch + Leuchte 1,000 kN Kn 1-30 + Kabel 0,001 kN/m (RF5-Ausdruck) | model.db M5 (LoadCase) + BEFUND Rev0 §6 |
| LF | 20 | Temperatur +10 | 71 | dT = +10 K | model.db M5 |
| LF | 21 | temperatur + 57 | 71 | dT = +57 K | model.db M5 |
| LF | 22 | temperatur -34 | 71 | dT = -34 K | model.db M5 |
| LF | 30 | wind x | 61 |  | model.db M5 |
| LF | 31 | wind -x | 61 |  | model.db M5 |
| LF | 32 | wind y | 61 |  | model.db M5 |
| LF | 33 | wind -y | 61 |  | model.db M5 |
| LF | 40 | raueis rd2 | 54 | Eis als Schnee-Kategorie (K4 pruefen) | model.db M5 |
| LF | 41 | raueis rd2 wind leitend | 54 |  | model.db M5 |
| LF | 43 | Schnee auf Leuchten | 54 | 1,500 kN/Knoten | model.db M5 |
| LF | 50 | wind auf eis x | 61 |  | model.db M5 |
| LF | 51 | wind auf eis -x | 61 |  | model.db M5 |
| LF | 52 | wind auf eis y | 61 |  | model.db M5 |
| LF | 53 | wind auf eis -y | 61 |  | model.db M5 |
| LF | 60 | wind auf eis x rd2 leitend | 61 |  | model.db M5 |
| LF | 61 | wind auf eis -x rd2 leitend | 61 |  | model.db M5 |
| LF | 62 | wind auf eis y rd2 leitend | 61 |  | model.db M5 |
| LF | 63 | wind auf eis -y rd2 leitend | 61 |  | model.db M5 |
| LK | 100 | Verformungsnachweis |  | 1.00*LF10 + 1.00*LF20 | model.db M5 (LoadCombinationImplStatic_items) |
| LK | 101 | verformung unter eislast |  | 1.00*LF10 + 1.00*LF22 + 1.00*LF40 | model.db M5 |
| LK | 200 | temperatur 10 wind auf seil x |  | 1.35*LF10 + 1.50*LF20 + 0.90*LF30 | model.db M5 |
| LK | 201 | temperatur 10 wind auf seil - x |  | 1.35*LF10 + 1.35*LF20 + 0.90*LF31 | model.db M5 |
| LK | 202 | temperatur 10 wind auf seil y |  | 1.35*LF10 + 1.35*LF20 + 0.90*LF32 | model.db M5 |
| LK | 203 | temperatur 10 wind auf seil -y |  | 1.35*LF10 + 1.35*LF20 + 0.90*LF33 | model.db M5 |
| LK | 204 | temp +57 |  | 1.35*LF10 + 1.50*LF21 | model.db M5 |
| LK | 205 | temp -34 eis |  | 1.35*LF10 + 1.35*LF22 + 1.35*LF40 | model.db M5 |
| LK | 206 | temp -34 rd2 leitend wind x |  | 1.35*LF10 + 1.35*LF22 + 1.35*LF40 + 0.75*LF60 | model.db M5 |
| LK | 207 | temp -34 rd2 leitend wind -x |  | 1.35*LF10 + 1.35*LF22 + 1.35*LF40 + 0.75*LF61 | model.db M5 |
| LK | 208 | temp -34 rd2 leitend wind y |  | 1.35*LF10 + 1.35*LF22 + 1.35*LF40 + 0.75*LF62 | model.db M5 |
| LK | 209 | temp -34 rd2 leitend wind -y |  | 1.35*LF10 + 1.35*LF22 + 1.35*LF40 + 0.75*LF63 | model.db M5 |
| LK | 210 | temp -34 wind x leitend rd2 |  | 1.35*LF10 + 1.35*LF22 + 0.75*LF41 + 1.35*LF60 | model.db M5 |
| LK | 211 | temp -34 wind -x leitend rd2 |  | 1.35*LF10 + 1.35*LF22 + 0.75*LF41 + 1.35*LF61 | model.db M5 |
| LK | 212 | temp -34 wind y leitend rd2 |  | 1.35*LF10 + 1.35*LF22 + 0.68*LF41 + 1.35*LF62 | model.db M5 |
| LK | 213 | temp -34 wind -y leitend rd2 |  | 1.35*LF10 + 1.35*LF22 + 0.68*LF41 + 1.35*LF63 | model.db M5 |
| LK | 214 | GZT (EQU) - Aussergewoehnlich - psi-1,1 |  | 1.35*LF10 + 1.35*LF22 + 0.27*LF43 | model.db M5 |
| LK | 215 | GZT (EQU) - Staendig / voruebergehend |  | 1.10*LF10 + 1.35*LF20 + 1.35*LF30 | model.db M5 |
| LK | 216 | GZT (EQU) - Staendig / voruebergehend |  | 1.10*LF10 + 1.35*LF20 + 1.50*LF31 | model.db M5 |
| LK | 217 | GZT (EQU) - Staendig / voruebergehend |  | 1.10*LF10 + 1.35*LF20 + 1.35*LF32 | model.db M5 |
| LK | 218 | GZT (EQU) - Staendig / voruebergehend |  | 1.10*LF10 + 1.35*LF20 + 1.35*LF33 | model.db M5 |
| LK | 220 | Erg. 2 (28.04.2015) - FEHLT im Modell |  | 1.35*LF10 + 1.50*LF43 (max N 20,16 kN lt. Kurzbericht) | BEFUND Rev0 K7, Rev01 N5 |

## B Modell B — Ergänzung 4 (Modell A + Patch)

### B1 Variante B-2 (Kanon, Patch E7 Rev0, Transformation T1 VAR-A, RMS 0,098 m): Knoten setzen

| Kn | Label | X [m] | Y [m] | Z [m] | ΔXY zu 5e [m] | Basis |
|---|---|---|---|---|---|---|
| 105 | A05 | 122.596 | 57.411 | -0.129 | 0.000 | Bestand 5e (VAR-A: Anker unverändert, Abw. Geometer 0.037 m) |
| 106 | A06 | 151.487 | 37.125 | 0.262 | 0.000 | Bestand 5e (Abw. Geometer 0.040 m) |
| 113 | A13 | 172.126 | 36.292 | -0.612 | 0.000 | Bestand 5e (Abw. Geometer 7108: 0.089 m) |
| 114 | A14 | 172.082 | 11.240 | -0.783 | 0.000 | Bestand 5e (Abw. Geometer 7106: 0.057 m) |
| 3006 | C06 -> Fassadenanker | 142.648 | 58.743 | 0.452 | 1.088 | Geometer 7101, VAR-A-Trafo |
| 3007 | C07 -> Fassadenanker | 161.883 | 44.239 | 0.452 | 1.580 | Geometer 7102, VAR-A-Trafo |

### B2 Variante B-2: Löschen / Lager

| Objekt | Nr | Aktion / Grund |
|---|---|---|
| Stab | 1006 | Mast entfällt (C06/C07 → Fassadenanker) |
| Stab | 1007 | Mast entfällt (C06/C07 → Fassadenanker) |
| Knoten | 2006 | Mastfuß entfällt, Lager entfernen |
| Knoten | 2007 | Mastfuß entfällt, Lager entfernen |
| Lager neu | 3006 | gelenkig wie Kn 105 (u fest, φ_x φ_y frei, φ_z fest); Drehung analog Wandanker (Auflage ID01) |
| Lager neu | 3007 | gelenkig wie Kn 105 (u fest, φ_x φ_y frei, φ_z fest); Drehung analog Wandanker (Auflage ID01) |

Kontrolle nach Patch: 84 Knoten / 68 Seile / 18 Maste / 25 Lagerobjekte (27 − 2 + Erweiterung Lager 105 um 3006/3007). Lasten unverändert (LF10 30 × 1,000 kN; Kabel; Wind; Eis; ΔT). LK220 = 1,35·LF10 + 1,50·LF43 ergänzen (E4).

### B3 Variante B-7 (Docx 07.10., G3-Siebenpunkt, Transformation T2, RMSE 0,62 m) — NUR VERGLEICH, nicht freigegeben (E1/E2)

| Kn | X [m] | Y [m] | Z [m] | ΔXY zu 5e [m] | Befund |
|---|---|---|---|---|---|
| 105 | 122.071816 | 56.970598 | -0.129 | 0.685 | Wandanker: physisch unverändert, Δ = Transformationsartefakt T2 |
| 106 | 151.161724 | 36.990289 | 0.262 | 0.352 | Wandanker: physisch unverändert, Δ = Transformationsartefakt T2 |
| 113 | 171.514489 | 36.430740 | -0.612 | 0.627 | Wandanker: physisch unverändert, Δ = Transformationsartefakt T2 |
| 114 | 172.194131 | 11.139194 | -0.783 | 0.151 | Wandanker: physisch unverändert, Δ = Transformationsartefakt T2 |
| 3006 | 142.074985 | 58.490902 | -0.038 | 0.514 | C06/C07: als Mastkopf behandelt, Z = Bestand; widerspricht Ergänzung 4 (Fassadenanker, z 0,452) |
| 3007 | 161.455905 | 44.182774 | 0.186 | 1.158 | C06/C07: als Mastkopf behandelt, Z = Bestand; widerspricht Ergänzung 4 (Fassadenanker, z 0,452) |
| 3021 | 192.948951 | 15.945504 | 0.937 | 0.322 | C21: E3 Fall A/B |
