# DELTA-REFINEMENT LOOP 1 — Fremddatensatz „RFEM 6 ZIELDATEN – BEREINIGT – FALL B“ gegen EINGABEDATEN_RF6_v0.1 — Rev0

| Feld | Wert |
|---|---|
| Datum | 07.10.2026 · ID-03 |
| Prüfobjekt | eingefügter Fremddatensatz (12 Tabellen, „86 Knoten / 88 Stäbe / 14 Materialien / 13 QS / 43 Lager / 19 LF / 20 LK / 38 Sv / 41 PFEIFER“) |
| Referenz | `docs/00_Quellenlog/RF6/EINGABEDATEN_RF6_v0.1/` (U10-Export input_3.json SHA 394820eb…, model.db M5 SHA 773d7b65…, Patch E7 Rev0 SHA 115d7587…) |
| Methode | programmatischer Zeilen-Diff (Knoten, Stäbe, Materialien, QS, Lager, LF, LK, Lasten); Toleranz Koordinaten 0,5 mm |
| Ergebnis | **Fremddatensatz NICHT verwendbar als Eingabe.** 68 Seilstäbe und 79 Knoten stimmen; alles andere weicht ab oder verletzt den Kanon. Gültige Eingabe bleibt v0.1 (A_BESTAND + B_VARA). |

## 1 Trefferbild (Loop 1)

| Tabelle | Fremd | v0.1 (belegt) | Befund | Grad |
|---|---|---|---|---|
| 1 System | Formfindung „aktiv“, FE 0,5 m, Modellname 003_NACH_BP_FIX | keine Formfindung (P1–P3), FeMeshSubdivisions 3, Theorie III. O., Newton-Raphson, g 10,00 (E7) | Formfindung verboten; FE-Länge und Name unbelegt | **S** |
| 2 Knoten | 86 | 86 | 79 identisch; 7 abweichend (§2) | **S** |
| 3 Material | 14 | 6 | Mat 7–14 (Beton C30/37, Baustahl-Duplikate) existieren in U10 nicht; Mat 1 ν stillschweigend 8,0 → 0,30 (unbenutzt) | **S** |
| 4 Querschnitte | 13 | 13 | 12 von 13 falsch (A, Iy, Iz, Material; §3) | **S** |
| 5 Stäbe | 88 | 88 | 68 Seile korrekt (Knoten, Typ 9, QS 1); 20 Maste QS falsch (2→2 statt Voute) | **M** |
| 6 Lager | 43 | 27 Objekte / 35 Knoten | 3001–3005 sind Mastköpfe (z ≈ 0), keine Lager; Drehwinkel positionsverschoben (§4); Ankerfreiheitsgrade fehlen | **S** |
| 7 Lastfälle | 19 | 19 | Nummern und Namen stimmen; Typ „Schnee“ für Eis = K4 | ok |
| 8 Lastkombinationen | „20“ (21 gelistet) | 21 + LK220 fehlend | Faktoren fehlen vollständig; LK220 fehlt | **S** |
| 9 Knotenlasten | 6 Zeilen | 17 | LF10 14 × −0,80 kN widerlegt (30 × +1,000 kN); Vorzeichen falsch (Z nach unten positiv); LF41, LF50–53, LF60–63 fehlen; Knotenlisten vereinfacht | **S** |
| 10 Stablasten | 19 Zeilen | 18 | LF20 „ΔT = 0“ statt +10 K; Listen enthalten S35 (U10: 67 Seile ohne 35, E6); Wind LF30–33 0,014 statt 0,0048 kN/m; Kabel 0,00148 kN/m (LF10, 29 Seile) fehlt | **S** |
| 11 Seilvorspannung Sv | 38 Werte | — | Vorspannung ist kein Eingabewert (P1: Sv = N(LK100) Ergebnis); Werte unbelegt, Quelle fehlt; als Kalibrier-Vergleichswerte erst nach Quellennachweis | **S** |
| 12 PFEIFER-Längen | 41 Zeilen | — | Quelle U9 (K15.105) nicht beschafft; L_sys weicht systematisch von U10-Stablängen ab (§5); S18–S22 „Sv 15 kN“ unbelegt | **U** |

S = Sperre (nicht übernehmen), M = Mangel (korrigierbar), U = unbelegt.

## 2 Knoten: 7 Abweichungen

| Kn | U10 Bestand (x; y; z) | Fremd „VAR-A“ | Δmax m | Patch E7 Rev0 | Befund |
|---|---|---|---|---|---|
| 105 | 122,596; 57,411; −0,129 | 122,071816; 56,970598; −0,129 | 0,524 | = Bestand | Kanon: 105 bleibt Bestand 5e (nur 3006/3007 ändern). Fremdwert = G3-Siebenpunkt (E1-Konflikt) |
| 106 | 151,487; 37,125; 0,262 | 151,161724; 36,990289; 0,262 | 0,325 | = Bestand | wie 105 |
| 113 | 172,126; 36,292; −0,612 | 171,514489; 36,430740; −0,612 | 0,612 | = Bestand | wie 105 |
| 114 | 172,082; 11,240; −0,783 | 172,194131; 11,139194; −0,783 | 0,112 | = Bestand | wie 105 |
| 3006 | 141,809; 58,051; −0,038 | 142,074985; 58,490902; −0,038 | 0,440 | 142,648; 58,743; **0,452** | Fremd ≠ Patch (Δ 0,573 m), z nicht auf Ankerhöhe |
| 3007 | 160,376; 43,764; 0,186 | 161,455905; 44,182774; 0,186 | 1,080 | 161,883; 44,239; **0,452** | Fremd ≠ Patch (Δ 0,427 m) |
| 3021 | 192,946; 16,267; 0,937 | 192,948951; 15,945504; 0,937 | 0,322 | nicht im Patch | C21 = E3 offen (Fall A/B 0,60 m); Fremdwert entspricht keiner belegten Variante |

Zusätzlich: 2006/2007 „KEEP“ und Maste 1006/1007 vorhanden → widerspricht E2 (Maste entfallen, Kontrolle 84 Kn / 86 St). Ein „Fall B“ mit 86/88 ist in sich widersprüchlich.

## 3 Querschnitte: Werte aus U10 (cm², cm⁴) vs. Fremd

| QS | Bezeichnung U10 | Mat U10 | A U10 | Iy U10 | Iz U10 | Fremd A / Iy / Iz / Mat | Befund |
|---|---|---|---|---|---|---|---|
| 1 | Seil PE 5 Pfeifer | 5 | 0,380 | 0,0211 | 0,0211 | 0,38 / 0,04 / 0,02 / 5 | Iy falsch |
| 2 | KR 405/185/35/35/0 | 2 | 271,25 | 19 507,65 | 19 507,65 | 127,40 / 1 671,68 / 1 094,60 / 3 | alles falsch |
| 3 | KR 200/82/35/35/0 | 2 | 127,40 | 2 391,93 | 2 357,46 | 107,29 / 2 391,93 / 2 357,46 / 4 | A, Mat falsch |
| 4 | KR 405/185/35/35/0 | 6 | 271,25 | 19 507,65 | 19 507,65 | 127,40 / 1 671,68 / 1 094,60 / 5 | alles falsch (Mat 5 = Seil!) |
| 5 | KR 200/82/35/35/0 | 6 | 127,40 | 2 391,93 | 2 357,46 | 107,29 / … / 5 | A, Mat falsch (Mat 5 = Seil!) |
| 6 | KR 399.1/182/35/35/0 | 6 | 267,12 | 18 672,29 | 18 668,26 | 127,40 / 1 671,68 / 1 094,60 / 4 | alles falsch |
| 7 | **Rohr 247/36** | 2 | 238,64 | 13 666,95 | 13 666,95 | „Rohr 247/24“ 168,14 / 21 145,50 / 10 572,70 / 7 | Bezeichnung, alles falsch |
| 8 | Rohr 355.6/24 | 2 | 250,02 | 34 544,89 | 34 544,89 | 250,02 / 46 908,90 / 23 454,40 / 8 | Iy, Iz, Mat falsch |
| 9 | Rohr 247/24 | 2 | 168,14 | 10 572,73 | 10 572,73 | 168,14 / 21 145,50 / 10 572,70 / 9 | Iy (= 2·Iz) , Mat falsch |
| 10 | KR 399.1/182/35/35/0 | 2 | 267,12 | 18 672,29 | 18 668,26 | 127,40 / … / 10 | alles falsch |
| 11 | KR 202.1/83.1/35/35/0 | 6 | 128,87 | 2 466,63 | 2 431,80 | 128,87 / 513,28 / 2 466,63 / 6 | Iy, Iz falsch |
| 12 | KR 201.2/82.6/35/35/0 | 6 | 128,23 | 2 433,83 | 2 399,15 | 128,23 / 510,66 / 2 433,83 / 12 | Iy, Iz, Mat falsch |
| 13 | KR 200.3/82.1/35/35/0 | 6 | 127,61 | 2 402,41 | 2 367,89 | 127,40 / 1 671,68 / 1 094,60 / 13 | alles falsch |

Stab-QS-Paare (Voute) laut U10: 1001 3→10, 1003 11→4, 1021 12→4, 1017/1018 9→8, übrige 15 Maste 5→4. Fremd: 2→2 (1003: 3→3). Damit wären alle Maste mit A 127 cm² / Iy 1 672 cm⁴ statt 271 cm² / 19 508 cm⁴ am Fuß modelliert → Mastkopfsteifigkeit um Faktor ≈ 12 zu klein, Kalibrierung K1–K7 unmöglich.

## 4 Lager: Mechanik der Fremdfehler

U10: 27 Lagerobjekte. Anker 101–115: u_x u_y u_z fest, φ_x φ_y frei, φ_z fest (gelenkig um zwei Achsen). Mastfüße 2001–2021 (z ≈ 8,7 m, Z positiv nach unten): alle sechs Freiheitsgrade fest. Drehung φ_z des Bezugssystems:

| Lager-Knoten U10 | φ_z U10 | Fremd ordnet denselben Winkel zu |
|---|---|---|
| 101–106 | −45,00° | 101 0° (falsch); 102 45° |
| 109, 111 | +45,00° | 2009–2015 |
| 115 | 0° | 115 −55,47° |
| 2011, 2012, 2020 | 48,00° | 104 |
| 2021 | 4,00° | 105 |
| 2019 | 53,00° | 108 |
| 2002 | −55,47° | 115 |
| 2001 | −20,50° | 2001 (einziger Treffer) |
| 2018 | 90,00° | 2007 |
| 2017 | 110,00° | 2008 |
| 107, 108, 110, 112, 113, 114 | +45,00° | 2009–2015 |
| 2003 | −55,50° | 2016 |
| 2004 | −138,25° | 2017 |
| 2005 | 34,19° | 2018 |
| 2006 | −124,95° | 2019 |
| 2007 | 55,12° | 2020 |
| 2008 | 124,50° | 2021 |
| 2009 | 123,64° | 3001 |
| 2010 | 125,66° | 3002 |
| 2014 | 124,50° | 3003 |
| 2015 | −86,27° | 3004 |
| 2016 | 176,87° | 3005 |

Die Fremdliste enthält exakt die U10-Winkelfolge, aber um eine Position gegen eine fortlaufende Knotenliste verschoben (positioneller Join ohne Schlüssel). 3001–3005 (Mastköpfe auf Seilniveau) sind keine Lager. Für Modell B fehlen: Lager 2006/2007 entfernen, 3006/3007 gelenkig wie 105 (Patch E7).

## 5 PFEIFER-Längen (Tabelle 12) vs. U10-Systemlängen

L_sys (Fremd) liegt bei 38 von 43 Seilen 56–531 mm **unter** der U10-Stablänge, bei S36 +845, S66 +1 390, S46 −1 485, S53 −2 015 mm (Vorzeichen: U10 − Fremd). Interpretation ohne Quelle unzulässig (Beschlagmaß F7, Nulllage vs. Werkstattlänge). S19 3 565 / S22 7 685 mm (U10 3 832 / 8 003 mm) sind die zwei betroffenen Seile; neue Längen folgen aus Modell B, nicht aus dieser Tabelle. Quelle U9 (PFEIFER K15.105) beschaffen, dann Loop 2.

## 6 Lasten: Einzelbefunde

| # | Fremd | Belegt (model.db M5 / 07_, 08_, 09_) | Beleg |
|---|---|---|---|
| L1 | LF10: 14 Knoten × −0,80 kN „Ringleuchte RL01–14“ | 1 Knotenlast Fz = +1,000 kN auf Kn 1–30 (Σ 30,0 kN) | NodalLoad id LF10, Sperrliste Rev0 |
| L2 | Vorzeichen −0,80 | Z positiv nach unten → Gewicht positiv | Tabelle 1 Fremd selbst („nach unten positiv“) |
| L3 | LF10 Kabel fehlt | 0,00148 kN/m auf 29 Seilen (2, 4, 5, 9, 11, 12, 14, 20, 22, 23, 24, 27, 28, 29, 32, 34, 39, 40, 41, 44, 45, 49, 50, 54, 55, 59, 62, 63, 65) | 08_stablasten Zeile 1 |
| L4 | LF20 ΔT = 0 | ΔT = +10 K | 08_ Zeile 2 |
| L5 | dT-Listen „1-67,81“ | 67 Seile ohne 35 | E6 |
| L6 | LF30–33 Stab 0,014 kN/m | 0,0048 kN/m (0,014 ist der LF62/63-Wert) | 08_ Zeilen 5–8 |
| L7 | LF41, LF50–53, LF60–63 Knotenlasten fehlen | 0,029; ±0,0235/0,024; ±0,0106/0,011 kN | 07_ |
| L8 | Knotenlisten „1-30“ | LF30 31 Kn (+330), LF31 28 Kn + Doppellast Kn 1, LF32 29 Kn (+330, 3012), LF33 29 Kn, LF41 29 Kn, LF52 (+3002) | 07_; Bereinigung = K-Punkt 14_offen |
| L9 | LK-Faktoren fehlen | vollständig in 09_ (z. B. LK200 1,35·LF10 + 1,50·LF20 + 0,90·LF30; LK214 1,35·LF10 + 1,35·LF22 + 0,27·LF43) | LoadCombinationImplStatic_items |
| L10 | LK220 fehlt | 1,35·LF10 + 1,50·LF43 (Erg. 2) | BEFUND Rev0 K7 |
| L11 | Tabelle 11 Sv als Eingabe | keine Vorspannung im Modell | Kanon P1–P3 |

## 7 Refinement-Ergebnis: was aus dem Fremddatensatz bleibt

- Übernommen: nichts. Jede richtige Zeile (68 Seile, 79 Knoten, 19 LF-Namen) ist in v0.1 bereits aus der Primärquelle vorhanden.
- Hinweis-Wert: Tabelle 12 (PFEIFER) als Hypothese für U9; Tabelle 11 (Sv) als Hypothese für Bestands-Sv aus dem Ausdruck. Beide erst nach Quellenbeleg in das Quellenlog Ursprung.
- Neue Erkenntnis für Loop 2: die Mastfuß-Drehwinkel aus U10 sind beim Neuaufbau explizit je Lagerobjekt zu setzen (27 Objekte, keine Positionslisten).

## 8 Loop 2 (Vorgabe)

1. Modell A aus v0.1 bauen (Generator nach `api_write_check` = WRITE_API_PRESENT), Kontrolle 86/88/27 Lager/19 LF/21 LK.
2. Kalibrierung K1–K7 gegen U10 (u_Kn17 2,085 m, N_S54 17,47 kN) → erst dann Sv-Vergleich mit Tabelle 11.
3. Modell B = A + B_VARA (3006/3007 Patch, 1006/1007/2006/2007 löschen, Lager 3006/3007 wie 105), Kontrolle 84/86.
4. Delta-Matrix Blatt 6 (Vorlage Rev0), S19/S22 Längen aus Modell B, F_Rd 27,9 kN.
