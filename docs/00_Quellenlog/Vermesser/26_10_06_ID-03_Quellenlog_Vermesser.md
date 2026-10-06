# QUELLENLOG — VERMESSER (Geometer-Aufmaß 2026, Transformation, Mapping)

| Feld | Wert |
|---|---|
| Datei | `00_Quellenlog/Vermesser/26_10_06_ID-03_Quellenlog_Vermesser.md` |
| Rolle | ID-03 (Claude) · Pflege: ID01 |
| Status | CANDIDATE Rev0 |
| Koordinaten | Geometer: Landeskoordinaten (X ≈ 3 500 4xx, Y ≈ 5 394 4xx, Z ≈ 445 m). RFEM lokal: Z positiv nach unten, [m] |
| Kanon | BEFUND RF5/RF6/VAR-A Rev0 §3 · AEQUIVALENZ-KNOTEN Rev0.csv · Rev01 U8d/U8e, N4 (F2) |

## 1 Vermesserquellen

| Q-ID | Datei | Ort | Datum | Autorität | Hash | Inhalt | Status |
|---|---|---|---|---|---|---|---|
| V1 | 7864Halterungen_mit_Lampenplan_Boardinghouse.xlsx (+ .dxf, .dwl2) | Drive 1j-GHSEH7x_JsUppBplMaQYvcwje6EhKe | Aufmaß 11./13.02.2026 | Geometer Blessing | – | 11 Messpunkte 7100–7108 (A13/A14 je 2 Punkte), Landeskoordinaten | PRIMARY |
| V2 | BöblingenMessung.pdf | _SEILSTATIK_BOEBLINGEN | 2026 | Geometer | – | Messprotokoll | FOUND, nicht gelesen |
| V3 | geometer_points.xlsx | Drive 1ad0_7D3tSltTplFcW8jzlcDQfotGdyOP | 2026 | Extrakt (intern) | – | Survey-Extrakt | DERIVED |
| V4 | rfem_reference_nodes.xlsx / Knotenkoordinaten_RFEM-Rechenfile.xlsx | Drive 1CmZqfw1qWzgLnqLG9lIzBXu-KNxTOgWT | 2026 | intern | – | RFEM-Bestandsknoten | DERIVED |
| V5 | 26_05_19_RFEM-GEOMETER-VGL(ALT-NEU-Halterung).xlsx/.pdf · 26_05_19_result.Verschiebung-Haltepunkte.pdf | _SEILSTATIK_BOEBLINGEN | 19.05.2026 | intern | – | Alt/Neu-Vergleich Haltepunkte | DERIVED |
| V6 | 26_05_20_MAPPING+TRANSFORMATION_GEOM-REFEM.pdf | Drive 1IsOdTG2P5m3nzH3U5Bdw064itS8g2Lpc | 20.05.2026 | intern (OCR teils unleserlich) | – | Mapping 7100→105, 7101/7102→3006/3007, 7104→3021; Parametersatz (−9,10°, 0,984) **obsolet** | DERIVED |
| V7 | 26_09_06_ZOTTER_BOEBLINGEN_G3_ENTSCHEIDUNG_FREIGABE__SEILSTATIK.docx | Drive 1ZAltNAK6WEU-IS59OlKGTyjrWpMK-Lmx (gdoc 1RtGAzRkPfHbKmZVKKfwx2jWoSWLoIZvazQoRFVUvRHg) | 06.09.2026 | ID01 Human Release | – | XY ACCEPT mit Auflagen, Z = MANUAL_ENGINEERING_Z, Hash-Bezug 7DB74920… (nicht mehr reproduziert) | PRIMARY (Entscheidung), **Revision E1 offen** |
| V8 | transformed_nodes.csv/.xlsx | Drive 189x35SBBe64Blk0J2uABwqRW5qob0W9d | 09/2026 | Pipeline G3 | – | Soll-Koordinaten G3 (7-Punkt-Starrfit) | DERIVED |
| V9 | 26_10_06_ID-03-AEQUIVALENZ-KNOTEN-GEOMETER-RFEM_Rev0.csv | Drive 1pnPWQTNqXODcQCdJ1NmOFOcybO_eil5G | 06.10.2026 | ID-03 | – | Geometer ↔ Label ↔ RFEM, drei Geometriestände | DERIVED-KANON |

## 2 Mapping Geometerpunkt → Label → RFEM-Knoten (aus V9)

| Geometer | Label | RFEM-Kn | Seil | Mast | ΔXY VAR-A − Bestand 5e [m] | ΔXY RF6(V01) − Bestand 5e [m] | Bemerkung |
|---|---|---|---|---|---|---|---|
| 7100 | A05 | 105 | S81 | – | 0,037 | 0,685 | Wandanker |
| 7101 | C06 → Fassadenanker | 3006 | S19 | 1006 (entfällt) | 1,087 (neu) | 0,514 | z VAR-A 0,452 ≠ RF6 −0,038 |
| 7102 | C07 → Fassadenanker | 3007 | S22 | 1007 (entfällt) | 1,580 (neu) | 1,158 | z VAR-A 0,452 ≠ RF6 0,186 |
| 7103 | A06 | 106 | S21 | – | 0,040 | 0,352 | Wandanker |
| 7104 | C21 | 3021 | S63 | 1021 bleibt | 0,600 | 0,322 | **E3: Fall A/B** |
| 7105 / 7106 | A14 (2 Punkte) | 114 | S64 | – | 0,255 / 0,057 | 0,151 | Lochmitte unbestätigt |
| 7107 / 7108 | A13 (2 Punkte) | 113 | S60 | – | 0,279 / 0,089 | 0,627 | Lochmitte unbestätigt |

## 3 Transformationen (zwei konkurrierende Workstreams, F2 / E1)

| T-ID | Workstream | Formel | Fit | Residuum | Quelle | Status |
|---|---|---|---|---|---|---|
| T1 | VAR-A (23.09.) | x = X − 3 500 460,605 · y = −(Y − 5 394 418,936) · z = −(Z − 445,472); Translation + Spiegelung | 4 Anker A05/A06/A13/A14 | RMS 0,098 m; Bestandsanker bleiben 0,04–0,09 m | Kurzbericht VAR-A §Grundlagen; Patch-JSON Rev0 | DERIVED-KANON (Empfehlung E1) |
| T2 | G3 / V01 / RF6 (06.09.) | Spiegelung + Rotation 0,23° + s = 1 + t = (115,0; 68,7) | 7 Punkte starr | RMSE 0,62–0,65 m; Bestandsanker verschoben 0,15–0,68 m (Artefakt) | WO9-OUT S-A1; ARBEITSPLAN-RAG | **CONFLICT** → G3-Revision |
| T3 | Prüfpaket 29.09. | Fit4 Drehung −0,0066° | 4 Anker | RMS 97,9 mm; C21 599,8 mm | IMPLEMENTATION-WORKFLOW (Ergebnis Koordinaten-Prüfpaket) | DIAGNOSE, UNRESOLVED |

## 4 Offene Vermesserfragen (Beschaffung ID01 → Geometer)

| # | Frage | Blockiert |
|---|---|---|
| VF1 | Sind 7101/7102 die Lochmitten der neuen Fassadenanker (Bolzenachse)? | Lsys S19/S22 (F2, TP-05) |
| VF2 | Höhenbezug Z (Landeshöhe → RFEM-Z): Einzelhöhen je Punkt, kein pauschaler Offset (z − 443,0 gesperrt, RMSE 1,366 m) | Z-Festlegung 3006/3007 (0,452) |
| VF3 | C21 (7104): reale Verschiebung 0,60 m oder Messtoleranz? | E3 Fall A/B, S63 |
| VF4 | A13/A14: welcher der zwei Punkte ist die Lochmitte? | Fit-Residuen 157/104 mm |
| VF5 | Unabhängige Streckenkontrolle A05↔C06, A06↔C07 (transformationsfrei) | F2-Absicherung |
