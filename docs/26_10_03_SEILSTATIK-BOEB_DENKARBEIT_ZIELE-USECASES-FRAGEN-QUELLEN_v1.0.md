# SEILSTATIK BÖBLINGEN — DENKARBEIT SCHRITTE 1–6: ZIELE, USE CASES, RETRIEVAL-FRAGEN, INFORMATIONSBEDARF, QUELLENANFORDERUNGEN, GOLDEN SLICE v1.0

`STAND: 2026-10-03 · AGENT: Claude Code (ID03, Entwurf für ID05/ID01) · STATUS: CANDIDATE · KLASSE: DERIVED`
`ANLASS: Self-Refinement Iteration 01 hat festgestellt, dass die Schritte 1–5 der 20-Schritt-Liste in keinem Artefakt standen (0 Treffer „Retrieval Question" in docs/). Dieses Dokument schließt die Lücke.`
`QUELLEN FÜR DIE ANTWORTEN: U1–U19 lt. Quellenverzeichnis Rev01 + Errata; VORLAGE-005; TODOS_VORSPANNUNG+TRANSFORMATION v1.0`

## 1 MAIN GOALS (Schritt 1)

| ID | Ziel | Entscheidung, die es stützt | Qualitätsanforderung | Status |
|---|---|---|---|---|
| MG1 | Bestellfähige Systemlängen Lsys und Sollast Sv für S19, S22 (ggf. S81) an PFEIFER | Bestellfreigabe durch ID01 | Lsys ± 5 mm nach Bestätigung Beschlagmaß; Sv aus LK100; Temperaturbezug 10 °C ausgewiesen | VAR-A vorläufig, F2/F7 offen |
| MG2 | Nachweis ULS/SLS des Seilnetzes im Bereich RL06/RL11–A14/C21 mit neuer Geometrie | Freigabe Wiedermontage | η = N_Ed/F_Rd ≤ 1 je Seil und Kombination inkl. LK220; Tiefpunkt ≤ 2,50 m unter Fixpunkt; lichte Höhe ≥ 5,00 m | η ≤ 0,42 im Bereich; LK220 fehlt; lichte Höhe offen |
| MG3 | 3D-Schnittstellenkräfte an 105/106/113/114/3006/3007/3021 je Lastkombination für die bauseitige Ankerprüfung | Übergabe an IEA/AG | vorzeichenrichtig, global und lokal, charakteristisch und Bemessungswert | VAR-A liefert RK1; Vorzeichen je LK in CSV |
| MG4 | Prüffähige Dokumentation analog Bestandsstatik 2015 („Ergänzung 4") | externe Prüfung durch AG-Prüfstatiker | Gliederung Teil I–III + Anhänge; jede Zahl mit Quelle; Normenstand 2026 ausgewiesen | VORLAGE-005, V006 ausstehend |
| MG5 | Wiederverwendbarkeit der Bestandsseile belegen oder verneinen | Bestellumfang | ΔL, ΔN je Seil; Zustandsbefund | rechnerisch ΔL ≤ 2,1 mm; Befund fehlt |

## 2 USE CASES (Schritt 2) — 14 repräsentative Fälle

| UC | Anwendungsfall | Ziel | Rolle |
|---|---|---|---|
| UC01 | Seillänge eines neuen Seils aus RFEM-Ergebnis und PFEIFER-Längenkette ableiten | MG1 | ID03 |
| UC02 | Sollast Sv eines Seils bestimmen und gegen Bestand (K15, Messung 2015) prüfen | MG1 | ID03/ID02 |
| UC03 | Vermesserpunkt einem RFEM-Knoten zuordnen und transformieren | MG1, MG2 | ID03 |
| UC04 | Transformation ohne Transformation prüfen (Streckenmatrix) | MG1 | ID02 |
| UC05 | Lastfall oder Kombination aus Bestand nachschlagen (Definition, Beiwerte, Quelle) | MG2 | alle |
| UC06 | Fehlende Kombination (LK220) identifizieren und ergänzen | MG2 | ID03 |
| UC07 | Normstand einer Norm für Bauort DE und Datum prüfen (CURRENT / HISTORICAL / MISSING) | MG4 | ID05 |
| UC08 | Herstellerkennwert mit Zulassung belegen (E, Z_Bk, F_Rd, ETA-Fassung) | MG2 | ID03 |
| UC09 | Prüfauflage aus Prüfbericht 2015 finden und auf 2026 anwenden | MG2, MG4 | ID02 |
| UC10 | Ankerkraft je Kombination für einen Knoten ausgeben | MG3 | ID03 |
| UC11 | Entscheidung F1–F10 mit Optionen, Begründung und Beleg dokumentieren | MG4 | ID01 |
| UC12 | Widerlegte Aussage erkennen und sperren (Sperrliste) | alle | ID02 |
| UC13 | Rechenstand reproduzieren (Hash, Wiederöffnung, Δ = 0) | MG4 | ID02 |
| UC14 | Bestandsseil auf Wiederverwendung prüfen (ΔL, ΔN, Befund) | MG5 | ID03 |

## 3 RETRIEVAL QUESTIONS (Schritt 3) — je Use Case die Fragen, die das System zuverlässig beantworten muss

| UC | Frage | Erwartete Antwortform | Quelle, die sie beantworten muss |
|---|---|---|---|
| UC01 | Wie lang ist L(LK100) für S19 in VAR-A, und welches Beschlagmaß gilt Leuchte–Anker? | Zahl m + Locator | RUN VAR-A 23.09.; Ankerzeichnung (offen) |
| UC01 | Wie lautet die PFEIFER-Längenkette Lsys → L → LA → LAG2 → LB → Lo2k mit allen Abzügen? | Formel + Parameter | K15.105 Legende (U9) |
| UC02 | Welche Seilkraft hat Seil Sxx in LK100 im Bestand und in VAR-A? | Zahl kN je Seil | RESULTS_BASIS-5e, RESULTS_VAR-A |
| UC02 | Wie groß war 2015 die Abweichung Messung zu Rechnung bei 22 °C je Seil? | Tabelle 18 Zeilen | U18, U19 |
| UC02 | Gibt es im Bestand einen Vorspann-Lastfall? | Ja/Nein + Zitat | U1 S. 18, Zusammenschau, Hinweise |
| UC03 | Welche Vermesserpunkte entsprechen A05, A06, A13, A14, C06neu, C07neu, C21? | Mapping-Tabelle | U8, 05_geometer_points_mapping_zcheck.csv |
| UC03 | Welche Transformation wurde in VAR-A verwendet, und auf welche Punkte wurde gefittet? | Formel + Residuen | Kurzbericht 23.09., 02_AUSWERTUNG |
| UC04 | Wie groß sind die 21 Paarabstände der 7 Punkte in Vermessung und RFEM? | Matrix | U8 + DIAG-JSON (zu erzeugen) |
| UC05 | Wie ist LK100 definiert, mit welchen Beiwerten, und was sagt Ergänzung 2 dazu? | Formel + Zitat | U15, U2 Pkt. 02-005 |
| UC05 | Welche Lastfälle gibt es im Bestandsmodell mit Nummer und Inhalt? | Tabelle LF10–LF63 | U15 |
| UC06 | Welche Kombinationen der Bestandsstatik fehlen im RFEM-Modell? | Liste + Quelle | U2 (LK220), U15 |
| UC07 | Welche Ausgabe von DIN EN 1991-1-4 mit NA ist in BW am Stichtag verbindlich? | Ausgabe + Rechtsquelle | VwV TB BW (extern, offen) |
| UC08 | Welche Kennwerte gelten für PE5 1×19 d 8,1 mm, und aus welcher ETA-Fassung? | Tabelle + Fassung | U9, ETA-11/0160 21.02.2025 |
| UC09 | Welche Prüfauflagen stellten PB00–PB03, und welche betreffen die Wiedermontage? | Liste mit Seite | U5 |
| UC10 | Welche Kraft wirkt am neuen Anker ex C06 in LK208, global und lokal? | Vektor kN | VAR-A_ANKERKRAEFTE_JE_LK.csv |
| UC11 | Welche Optionen hat F2 und was empfiehlt der Prüfstand? | Tabelle | VORLAGE-005 Anhang A |
| UC12 | Ist „15 kN Vorspannung" eine gültige Aussage? | Nein + Widerlegung | Sperrliste Rev01 §6, U9 |
| UC13 | Welcher Hash gehört zum Rechenstand VAR-A, und wurde er wiedergeöffnet? | Hash + Δ | MANIFEST, REOPEN_CHECK_RESULT.json |
| UC14 | Um wie viel ändert sich L(LK100) von S18 und S20 zwischen Bestand und VAR-A? | mm | 02_AUSWERTUNG (2,122 / 2,058 mm) |

## 4 REQUIRED INFORMATION (Schritt 4) — abgeleitet aus den Fragen, ohne Dateisuche

| Informationsklasse | Elemente | Für UC |
|---|---|---|
| Geometrie | Knotenkoordinaten RFEM (5e, VAR-A), Vermesserpunkte (X, Y, H), Mapping, Transformationsparameter, Residuen | 01, 03, 04 |
| Topologie | Member ↔ Start-/Endknoten ↔ Sxx, Stabtyp, Querschnitt | 01, 02, 10 |
| Material/Produkt | d, A, E, Z_Bk, F_Rd, α_T, E_k, Beschlagabzüge, Spannschloss, ETA-Fassung | 01, 08 |
| Lastmodell | LF-Definitionen, LK-Beiwerte, EK/RK, fehlende LK | 05, 06 |
| Ergebnisse | N je Seil je LK, u je Knoten, Lagerkräfte je LK, L(LK100) | 01, 02, 10, 14 |
| Messungen | Seilkräfte 2015 (Soll, gemessen, nachgerechnet), Vermessung 2026 | 02, 03 |
| Normen/Recht | Normausgabe, NA, Rechtsverbindlichkeit BW, Prüfauflagen | 07, 09 |
| Entscheidungen | F1–F10 mit Optionen, Status, Datum, Beleg | 11 |
| Provenienz | Pfad, Drive-ID, Hash, Datum, Autorität, Klasse | alle |
| Sperrliste | widerlegte Aussage, Beleg, korrekte Aussage | 12 |

## 5 SOURCE REQUIREMENTS (Schritt 5) — welche Quelle autoritativ sein muss

| Informationsklasse | Autoritative Quelle | Autorität | Ersatz nur wenn |
|---|---|---|---|
| Geometrie Bestand | U6 5e.rf5 (BD77CF83) | A1 | nie |
| Geometrie neu | U8 Vermessung 11./13.02.2026 + Geometerbestätigung (offen) | A1 | nie |
| Topologie | U14 DIAG-JSON + U15 Ausdruck | A1 | nie |
| Material/Produkt | U9 K15.105 + ETA-11/0160 (21.02.2025) | A0/A1 | nie |
| Lastmodell | U15 (Modell), U1/U2 (Begründung) | A1 | Konflikt → Erg. 2 entscheidet |
| Ergebnisse | RUN-KO mit Hash, Sandbox 23.09. | A3 | neuer RUN mit Hash |
| Messungen | U18/U19 (2015), U8 (2026) | A1 | nie |
| Normen | DIN EN + NA-DE Originaldatei, VwV TB BW | A0 | ÖNORM-B nur als HISTORICAL-Hinweis, nie als DE-Nachweis |
| Entscheidungen | VORLAGE-005 Anhang A mit Datum/Kürzel ID01 | A1 | nie |
| KI-Berichte | keine Autorität; nur Zeiger auf Primärquelle | A5 | – |

## 6 GOLDEN SLICE (Schritt 6)

End-to-End-Fall, an dem das System zuerst gebaut und getestet wird: **UC01 + UC02 + UC04 für Seil S19.**

- Input: U6, U8, U9, U14, U15, RUN VAR-A, U18/U19.
- Erwarteter Output: Lsys(S19) als Zahl mit Band, Sv(S19) = N(LK100), Streckenmatrix-Zeilen für 7101, Begründung Anfangszustand mit drei Zitaten.
- Referenz für das Residuum: Kurzbericht 23.09. (L(LK100) 4,925 m, Sv 4,62 kN), unabhängige Sehnenrechnung aus U8 + Mapping, Seilkraftmessung 2015 als Methodenbeleg.
- Toleranz: ΔL ≤ 5 mm gegen Sehnenrechnung, ΔN ≤ 0,05 kN gegen RUN, Zitate mit Seite.
- Bestanden, wenn ID02 alle UC-Fragen zu S19 nur aus Registry und Artefakten beantworten kann, ohne diesen Chat.

## 7 OFFENE PUNKTE DIESES DOKUMENTS

- ID05 hat die Use Cases und Fragen nicht gegengelesen. Status bleibt CANDIDATE.
- UC07 kann derzeit niemand beantworten: keine DIN-NA-Datei im Bestand, VwV TB BW nicht registriert.
- UC04 braucht die Streckenmatrix, die noch nicht erzeugt ist.
