# SEILSTATIK BÖBLINGEN — TO-DOS ZU DEN ZWEI KRITISCHEN UNSICHERHEITEN: VORSPANNUNG + KOORDINATENTRANSFORMATION v1.0

`STAND: 2026-09-29 · AGENT: Claude Code (ID03) · STATUS: DONE (nicht VERIFIED) · KLASSE: WORKFLOW + BEFUND`
`NEU GELESEN (Primärquellen): Statik 2015 Text-Fassung (1sufMK-2jmELfXvxDcXWVQW16ieRTiDJD, Zeilen 529–605, 1432–1434, 4982–4987, 5285–5305) · Seilkraftmessung_Pfeifer.pdf 16.06.2015 (1wA4Zm_EejjEXFDTx3V5qnwvYYbhIH85a) · Seilkraftmessung_Vergleich.pdf (1zuHrDvmNXjI3aYcQkeBdg-g3jZo9Og5w) · 05_geometer_points_mapping_zcheck.csv (1s1HH4s6Qbe0wBf7wlKMSYb5Y7kmpYtLG) · 02_AUSWERTUNG_LK100_VAR-A (13GMQ39TNrLwqoCluPu7a5C-D1OPRcb9A) · VORLAGE-005 + Stellungnahme 23.09. · 26_09_24_AUSWERTUNG_RFEM-ZUGRIFF · ETA-11/0160 (DIBt, Fassung 21.02.2025)`

## 0 TL;DR

- **Vorspannung ist geklärt, nicht offen.** Die Bestandsstatik sagt es dreimal selbst: „LF 10 – Vorspannung: Derzeit keine Vorspannung angesetzt" (Teil I, S. 18), „Ersatz der Vorspannungen aus der Vorstatik durch tatsächlich angesetzte Lasten" (Zusammenschau) und die Empfehlung, Geometrie „nicht über Vorspannen … sondern durch Konfektion der Seillängen bzw. der Nulllage" zu lösen. Die Seilkraft im Einbauzustand ist Ergebnis, nicht Eingabe. PFEIFER hat das 2015 gemessen: 18 Seile, Abweichung Messung zu Rechnung bei 22 °C zwischen 0 und −2,0 kN.
- **Deine Transformation ist im Kern schon verifiziert.** Für die vier unveränderten Fassadenanker A05/A06/A13/A14 passt die Starrkörper-Transformation (Translation + Rotation + Spiegelung) in XY auf 4–16 cm und in Z auf 0–3 cm. Die 0,5–0,7 m Abweichung entsteht nur dort, wo sich die Punkte **konstruktiv** geändert haben (C06/C07 sind neue Anker, keine Mastköpfe) oder wo die Zuordnung offen ist (C21). Die Verformung des Seilnetzes spielt dabei keine Rolle, weil der Geometer Lochmitten der Halterungen gemessen hat, keine Seilpunkte.
- **Reine Translation reicht nicht.** Der Fit braucht eine Spiegelung (Gauß-Krüger-Y gegen RFEM-Y) und eine kleine Rotation. Prüfbar in zehn Minuten über transformationsfreie Streckenvergleiche (To-Do G2).
- **RFEM 6 ist nicht nötig.** Am 24.09. lief RFEM 5.29 mit COM-Zugriff auf deinem Rechner (RFEM64.exe, 7 von 9 Workflow-Funktionen). Der RFEM-6-Pfad wäre ein Neuaufbau ohne Auftrag.
- Nachtrag zu Rev01: **VORLAGE-005** (Codex, 23.09.) ist die aktuelle Berichtsfassung, nicht mehr VORLAGE-002. Die Stellungnahme vom 23.09. schließt 01-005, 01-013, 01-017. Fragen sind jetzt F1–F10.

---

## 1 VORSPANNUNG — WAS DIE PRIMÄRQUELLEN SAGEN

| # | Aussage | Quelle (Locator) | Bedeutung für 2026 |
|---|---|---|---|
| P1 | „LF 10 – Vorspannung. Anm.: Derzeit keine Vorspannung angesetzt." | Statik 2015 Teil I, Lastfallliste S. 18 (TXT Z. 4982–4987) | Es gibt keinen Vorspann-Lastfall. Achtung: Im Text heißt LF 10 „Vorspannung", im RFEM-Modell ist LF10 das Eigengewicht. Nummerierung Text ≠ Modell. |
| P2 | „…der Ersatz der Vorspannungen aus der Vorstatik durch tatsächlich angesetzte Lasten ermöglichte, die ausgeschriebenen Dimensionen … zu halten." | Teil I, 4. Zusammenschau (TXT Z. 1432–1434); Vorstatik 18.08.2013 = Anhang 48 | Die Vorstatik 2013 hatte Vorspannkräfte. Die Ausführungsstatik 2015 hat sie bewusst abgeschafft. |
| P3 | „Es wird empfohlen, geometrische Anforderungen (Lage des Seilzuges im Endzustand) nicht über Vorspannen … zu lösen, sondern durch entsprechende Konfektion der Seillängen bzw. der Nulllage." | Abschnitt Standsicherheit/Hinweise (TXT Z. 5298–5305) | Das ist genau die PFEIFER-Längensystematik: Lsys unter Sollast Sv bei T = 10 °C. Die Länge wird konfektioniert, nicht nachgespannt. |
| P4 | Einbautemperatur T0 = 10 °C; ΔT(+) = 57 K, ΔT(−) = 34 K; „LK 100: 1,35·LF Eigengewicht + 1,35·LF Temperatur +10 °C" | Teil I (TXT Z. 529–605) | Text nennt 1,35; Modell und Ergänzung 2 (Pkt. 02-005) nennen 1,0. Der Modellwert gilt (01-003 CLOSED). |
| P5 | RFEM-Modell: Seilstäbe 1–67 + 81, Material E = 130 kN/mm², kein Vorspann-LF, keine Vordehnung; RF-Formfindung als Option gelistet, kein Formfindungs-LF | RFEM-Ausdruck 07.09. (U15), BEFUND V01 | Anfangszustand = Knotengeometrie, Seilkraft aus Eigengewicht + Geometrie nach Th. III. O. |
| P6 | **Seilkraftmessung PFEIFER 16.06.2015**, PIAB RTM 20 D Nr. 2169, 18 Seile (S01, S12, S13, S14, S16, S25, S26, S30, S36, S44, S48, S50, S51, S52, S53, S54, S55, S57) mit Sollkraft und gemessener Kraft | `EXPORT\00 Bestandstatik fragmentiert\PDF_Finale_Dokumente_Ausgang\13bb-statik-dokumentation\Seilkraftmessung_Pfeifer.pdf` | **Bisher in keinem Register.** Liefert Sv für 18 Seile, davon 8 aus dem Block S01–S30, der im K15-Blatt leer ist. |
| P7 | **Vergleich Messung ↔ Rechnung bei 22 °C**: Delta gemessen − nachträglich berechnet zwischen 0,0 und −2,0 kN; Beispiele S52 10,0 / 9,6 / 9,62 kN, S54 10,0 / 9,5 / 9,66 kN, S16 6,0 / 4,0 / 5,45 kN, S53 0 / 0 / 0,60 kN | `…\13bb-statik-dokumentation\Seilkraftmessung_Vergleich.pdf` | **Golden Case für den Anfangszustand.** Die geometriebasierte Methode wurde 2015 in situ bestätigt. Gemessen liegt systematisch unter Rechnung (Kriechen, Setzung, Beschlagspiel). |
| P8 | PFEIFER-Blatt K15.105 Ind. 1: Sv für S31–S67 und S81 ausgefüllt, S01–S30 leer; Sv(S53) = Sv(S56) = 0 | `03_pfeifer_seildaten.csv` (18.09.) | Sv = N(LK100) des 5e-Modells. S53/S56 = schlaffe Seile, im Modell N ≈ 0. |
| P9 | ETA-11/0160 = PFEIFER Wire Ropes (offene Spiralseile unlegiert + nichtrostend, mit Endverbindern), aktuelle Fassung 21.02.2025 (DIBt 8.06.02-289/24) | dibt.de, pfeifer.info | U9b geschlossen. Modell-Materialname „Z-14.7-411" ist die alte abZ, für Doku als historisch kennzeichnen. |

**Fazit Vorspannung**: Für die neue Berechnung gilt dieselbe Methode. Die Seilkraft im Einbauzustand ergibt sich aus LK100 mit der neuen Geometrie. Diese Kraft ist die Sollast Sv, die PFEIFER für die Konfektion der neuen Seile S19 und S22 braucht. VAR-A liefert bereits S19 4,62 kN und S22 3,83 kN. Die Bestandsmessung 2015 zeigt, dass die Realität 0 bis 2 kN darunter liegt. Das ist bei F_Rd 27,9 kN und η ≤ 0,42 unkritisch, muss aber im Bericht stehen.

### To-Dos Vorspannung

| ID | To-Do | Rolle | Input | Output | Abnahme |
|---|---|---|---|---|---|
| V1 | Seilkraftmessung 2015 als PRIMARY registrieren (2 PDFs, Hash, Drive-ID) und als GOLDEN_CASE-KO anlegen: Toleranz Δ ≤ 2,0 kN gemessen vs. Rechnung 22 °C | ID03 | P6, P7 | `ko/GC-BOEB-000002.json`, Zeile in SOURCE_REGISTRY | schemavalide; ID02 prüft 3 Werte gegen PDF |
| V2 | Sv-Register vervollständigen: K15-Blatt (S31–S67, S81) + Messblatt (18 Seile) + N(LK100) aus 5e-Export für alle 68 Seile in eine Tabelle; Differenzen ausweisen | ID03 | P6, P8, `RESULTS_BASIS-5e_gespeichert_2015.json` | `01_TABLES/sv_register_68.csv` (Sxx, Sv_K15, Sv_Messblatt, N_LK100_5e, N_gemessen, ΔT) | 68 Zeilen, keine leere N_LK100-Spalte; ID02 Stichprobe 10 % |
| V3 | Aussage für den Bericht formulieren, Kapitel „Anfangszustand": kein Vorspann-LF, Anfangszustand = Knotengeometrie, Sv = N(LK100), Zitat P1–P3 mit Seitenangabe, Messvergleich 2015 als Validierung | ID03 | P1–P7 | Absatz in Ergänzung 4 / V006 | ID01 liest gegen |
| V4 | RF-Formfindung-Flag in RFEM 5 am Modell 5e und VAR-A in der GUI prüfen (nicht über API lesbar); Screenshot als Beleg | ID01 | Modell offen | Screenshot + Zeile im RUN-KO | Flag dokumentiert AUS oder Wirkung erklärt |
| V5 | Sollast für PFEIFER aus VAR-A: S19 4,62 kN, S22 3,83 kN bei 10 °C; Sensitivität E = 120/140 GPa auf Sv und L(LK100) | ID03 | VAR-A Sandbox | Tabelle Sv/L für 3 E-Werte | ΔL ≤ 5 mm zwischen E-Varianten, sonst F6 eskalieren |
| V6 | Temperatur der Vermessung (11./13.02.2026) nur als Randnotiz: Anker unverformt, Leuchtenpunkt 7004 verformt und im Rückbauzustand → kein Kontrollwert (01-016). Optional: LK mit ΔT_Feb rechnen und RL08-Höhe vergleichen, nur als Plausibilität | ID03 | DWD-Tagesmittel Böblingen Feb 2026, VAR-A | Notiz + optional 1 Lauf | keine Freigaberelevanz |
| V7 | Widerspruch Text-LF-Nummerierung (LF 10 Vorspannung im Text, LF10 EG im Modell) im Bericht als Hinweis aufnehmen, damit der Prüfer nicht stolpert | ID03 | P1, U15 | Fußnote | – |
| V8 | Einbautemperatur für neue Seile: PFEIFER fertigt LA bei 20 °C, Statik bei 10 °C. Montagemonat 2026 festlegen und Temperaturkorrektur der Bestelllänge ausweisen (α = 1,6·10⁻⁵ /K, S22: 9,4 m × 10 K × 1,6·10⁻⁵ = 1,5 mm) | ID03 | K15 Legende | Zeile im Bestellblatt | ID02 rechnet nach |

---

## 2 KOORDINATENTRANSFORMATION — WAS SCHON BELEGT IST

| # | Befund | Quelle | Konsequenz |
|---|---|---|---|
| T1 | Gemessen wurden „Halterungen (Mitte Loch)" = Lochmitten der Anker- und Mastkopfhalterungen, plus zwei Leuchtenpunkte 7000/7004 (RL08). Messtage 11./13.02.2026 | Anfrage 06.03.2026 (U7a), BöblingenMessung.docx | **Anker verformen sich nicht.** Die Seilverformung (Dezimeter) betrifft nur 7000/7004. Diese beiden Punkte sind aus jedem Fit auszuschließen. |
| T2 | VAR-A-Transformation: x = X − 3 500 460,605; y = −(Y − 5 394 418,936); z = −(Z − 445,472). Fit auf A05/A06/A13/A14, Restabweichung XY 4–16 cm, RMS 0,098 m | Kurzbericht 23.09., 02_AUSWERTUNG | Starrkörper mit Spiegelung. Vier feste Fassadenanker stimmen auf Dezimeter-Bruchteile. |
| T3 | Z-Check: Höhendifferenz Vermessung minus RFEM-Höhendifferenz, jeweils relativ zu A05: A06 −0,009 m, A13 −0,013 m, A14 +0,026 m, C21 −0,084 m; C06/C07 −0,489 / −0,265 m → neue Anker liegen 0,45 m tiefer als die alten Mastköpfe | `05_geometer_points_mapping_zcheck.csv` | Z-Formel ist für Anker verifiziert. C06/C07 brauchen Z = +0,451 (in VAR-A umgesetzt, in V01/G3 nicht). |
| T4 | G3-Fit vom 06.09. (7 Punkte, RMSE 0,62–0,65 m) hat C06, C07 und C21 **mit in den Fit genommen**. C06/C07 sind konstruktiv neue Punkte (Fassadenanker statt Pylon). Ihr Residuum ist kein Messfehler, sondern die reale Verschiebung. | G3-Doku, Quellenbefund §6 | Der große RMSE ist ein Artefakt der Punktwahl. Fit nur auf unveränderte Punkte, dann neue Punkte transformieren. |
| T5 | C21 (7104 ↔ 3021): Abweichung 0,60 m; zu A13 bis 0,63 m; Mastneigung lt. Gemini-Auswertung 2,1° (8,7 m × sin 2,1° = 0,32 m) | 01-008, Gemini 07.09. | Kandidaten: Mastkopf-Auslenkung, Punktidentität, 2015-Aufmaß. Nicht durch Seilverformung erklärbar. Entscheidung offen. |
| T6 | Transformationsfreie Streckenkontrolle: Strecken 7101/7102 zu A05/A06 stimmen in VAR-A auf 1–4 cm; zu A13/A14 größere Residuen (Codex V005) | VORLAGE-002/005 01-006 | Methode ist die richtige, muss aber auf **alle** 6 Ankerstrecken ausgedehnt und tabelliert werden. |
| T7 | Zwei parallele Geometriestände: V01 in EXPORT (G3-XY, alte Z) und VAR-A in Sandbox (4-Anker-XY, Z +0,452); S19/S22 differieren um 0,4–0,6 m | AUSWERTUNG 24.09. A3 | F2 ist Entscheidung, keine Datenlücke. |

**Antwort auf deine Hypothese „nur Translation"**: Nein. Ohne Spiegelung geht es nicht (Rotation allein: RMSE 13,7 m, Pipeline Mai). Mit Spiegelung plus Rotation 0,23–0,58° und Translation liegt der Fit auf den vier Ankern bei 0,1 m. Ob man die Rotation weglassen kann, zeigt To-Do G2 in Zahlen.

### To-Dos Transformation

| ID | To-Do | Rolle | Input | Output | Abnahme |
|---|---|---|---|---|---|
| G1 | Referenzpunkte fixieren: Fit **nur** auf A05 (7100), A06 (7103), A13 (7107/7108 gemittelt), A14 (7105/7106 gemittelt). 7000/7004 (Leuchte), 7101/7102 (neu), 7104 (C21) sind Prüfpunkte, keine Fitpunkte | ID03 | U8, 05_geometer_points… | `transform_fit_v2.json` (Parameter, Residuen je Punkt) | RMS XY ≤ 0,15 m auf 4 Ankern; Z-Mismatch ≤ 0,03 m |
| G2 | Transformationsfreie Streckenmatrix: alle 21 Paarabstände der 7 Punkte (A05, A06, A13, A14, C06neu, C07neu, C21) aus Vermessung vs. RFEM-Modell (5e für Anker, VAR-A für C06/C07). Drei Spalten: d_survey, d_rfem, Δ | ID03, Nachrechnung ID02 | U8, DIAG-JSON | `01_TABLES/streckenmatrix_7pt.csv` | Ankerpaare Δ ≤ 0,05 m; C06/C07-Paare zeigen Δ zur VAR-A-Lage ≤ 0,05 m; C21-Paare weisen den Ausreißer aus |
| G3 | Translation-only-Test: G1 ohne Rotation wiederholen, Residuen vergleichen | ID03 | G1 | 2 Zeilen in transform_fit_v2.json | Wenn RMS(translation only) ≤ 0,15 m → Rotation vernachlässigbar, sonst Rotation bleibt |
| G4 | C21 klären: (a) Streckenmatrix G2, (b) Mastneigung aus Aufmaß-Foto/Scan, (c) Geometer fragen, ob 7104 Mastkopf-Lochmitte oder Fußpunkt ist | ID03 + ID01 (Mail) | T5 | Entscheidung: 3021 verschieben oder nicht, mit Begründung | Abweichung erklärt oder als Auflage im Bericht |
| G5 | Geometer-Bestätigung 7101/7102 = Lochmitte Ankerplatte neue Fassadenanker, Bolzenachse, Höhenbezug NHN; Anfrage inkl. Skizze | ID01 (Mail an Blessing) | 01-007 | schriftliche Bestätigung | Antwort registriert als PRIMARY |
| G6 | Ankerplattendetail 2024 (Kneidinger/IEA: M16 Innengewindeanker, Platte Ø 240 mm) anfordern; Versatz Lochmitte → Gabelkopfbolzen messen oder aus Zeichnung ableiten → ersetzt die empirische Annahme 0,193 m | ID01 (Mail an Kneidinger) | Mailkette 2024 | Zeichnung + Maß | Beschlagmaß aus Zeichnung, nicht aus Bestand |
| G7 | Variante B (G3-XY) als Sensitivität rechnen, nur Sandbox, Z = +0,451; S19/S22 beide Varianten nebeneinander | ID03 | V01-Geometrie | RUN-KO VAR-B | Differenz S19/S22 dokumentiert; F2 bekommt Zahlen |
| G8 | EXPORT-Bereich schreibschützen; die am 24.09. 05:27–05:35 ohne Protokoll gespeicherten Dateien (13bb, V01, WORKING_VALIDITY) als Vorfall dokumentieren; offene EXPORT-Modelle in RFEM ohne Speichern schließen | ID01 | AUSWERTUNG 24.09. Q1–Q4 | Vermerk + Schreibschutz | keine Saves mehr in EXPORT |

---

## 3 UMGANG MIT DER VERFORMTEN GEOMETRIE (deine Frage)

- Für die **Geometrie** irrelevant: gemessen sind Lochmitten fester Halterungen. Sie sind der unverformte Rand des Systems.
- Für den **Anfangszustand** irrelevant: Der Bestand definiert ihn über die Knotengeometrie der Anker plus konfektionierte Seillängen, nicht über gemessene Kräfte oder Durchhänge.
- Für die **Validierung** nutzbar, aber nur mit Zustand und Temperatur: 2015 hat PFEIFER bei 22 °C gemessen und die Statik hat nachgerechnet (P7). 2026 gibt es nur zwei Leuchtenpunkte im rückgebauten Zustand. Das reicht nicht für einen Vergleich. Wenn du einen willst: nach der Wiedermontage Seilkräfte messen lassen (PIAB oder Vergleichbares), wie 2015. Das wäre der saubere Abschluss der Kette und ein neuer Golden Case.
- Die Feuerwehr-Anforderung (lichte Höhe ≥ 5,00 m, Tiefpunkt ≤ 2,50 m unter Fixpunkt 8,50 m) wird im verformten Zustand LK100 geprüft. VAR-A: max. Tiefpunkt 1,74 m (RL06), RL09 1,07 m. Was fehlt, sind Geländehöhe und Leuchtenunterkante (01-014).

---

## 4 REIHENFOLGE (eine Woche)

1. ID01: Mails G5, G6 heute. Ohne Antworten bleibt F2/F7 offen.
2. ID03: V1, V2, G1, G2, G3 (alles aus vorhandenen Daten, ohne RFEM).
3. ID02: Nachrechnung G2 und Stichprobe V2 in eigener Session.
4. ID01: F2 auf Basis G2/G3-Zahlen entscheiden; F3 (LK220) und F4 (S17) gleich mit.
5. ID03: G7 und LK220-Ergänzung in Sandbox, danach V006 des Berichts.
