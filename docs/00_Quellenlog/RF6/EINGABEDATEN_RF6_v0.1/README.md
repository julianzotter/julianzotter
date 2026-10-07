# EINGABEDATEN RF6-NEUAUFBAU v0.1 — Seilstatik Böblingen (07.10.2026, ID-03, CANDIDATE)

Erzeugt mit `tools/26_10_07_ID-03_make_eingabedaten.py` aus: RF5-COM-Export U10 (`input_3.json`, BESTAND-5e_NEUBERECHNET 23.09.), `lines.csv` (Teilabgleich), `model.db` der Arbeitskopie M5 (nur Lasten/LK), Patch E7 Rev0. Hashes aller Quellen und Ausgaben in `MANIFEST.json`. Einheiten: m, kN, kN/m, K, cm², cm⁴.

## A_BESTAND (Modell A = Bestand 5e, Kalibrierziel u_Kn17 2,085 m / N_S54 17,47 kN)

| Datei | Zeilen | Inhalt |
|---|---|---|
| 01_knoten.csv | 86 | Koordinaten RFEM lokal (Z positiv nach unten) |
| 02_staebe.csv | 88 | 68 Seile (Typ 9, QS 1) + 20 Maste (Voute QS i→j), Linie, Knoten i/j, Länge |
| 03_materialien.csv | 6 | E, G, ν, γ, α_T, γ_M; Mat 1 „rundlitze“ unbenutzt und fehlerhaft (ν 8,0) |
| 04_querschnitte.csv | 13 | A, Ay, Az, It, Iy, Iz aus RF5 (QS 1: A 0,38 cm²) |
| 05_lager.csv | 27 | Knotenlisten, Festhaltungen, Drehung Bezugssystem (Anker 101–115 gelenkig, Mastfüße eingespannt) |
| 06_rechenparameter.csv | 28 | Iterationen, Inkremente, Schubsteifigkeit, Solver; Theorie III. O. (E7 g offen) |
| 07_knotenlasten.csv | 17 | je LF: Komponenten kN, Knotenliste (LF10 = 30 × 1,000 kN) |
| 08_stablasten.csv | 18 | Streckenlasten kN/m (Kabel 0,00148; Wind 0,0048; Eis 0,009/0,0045; Wind auf Eis 0,0303/0,01395) und dT = +10/+57/−34 K auf 67 Seilen (ohne S35, E6) |
| 09_lastfaelle_lastkombinationen.csv | 41 | 19 LF, 21 LK mit Faktoren, LK220 als fehlend |

## B_VARA (Modell B = Modell A + Patch, Kontrolle 84 Kn / 68 Seile / 18 Maste)

| Datei | Inhalt |
|---|---|
| 11_knoten_patch.csv | 3006/3007 → Fassadenanker (Geometer 7101/7102, VAR-A-Trafo, z 0,452); 105/106/113/114 = Bestand |
| 12_loeschen.csv | Stäbe 1006, 1007; Knoten 2006, 2007 |
| 13_lager_patch.csv | 3006/3007 gelenkig wie Kn 105; Lager 2006/2007 entfernen |
| 14_offen.csv | C21/E3, LF-Listen, EK1/LK220 (E4), Seil 35 (E6) |
| 10_patch_vara_rev0.json | Patch-Quelle |

Regeln: keine Vorspannung, keine Formfindung, keine Laständerung. Die QS-14-Hilfsgeometrie ist in Modell A nicht enthalten (Bestand kennt sie nicht). Richtungscode in 08 ist der RF6-interne Code; die Richtung ergibt sich aus dem LF-Namen und ist beim Neuaufbau gegen den RF5-Ausdruck zu prüfen.
