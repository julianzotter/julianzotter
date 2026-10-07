# SPERRLISTE — Fremdskripte „RF5-Export / RF6-Neuaufbau / Bereinigung / Delta-Matrix“ (06./07.10.2026) — Rev0

| Feld | Wert |
|---|---|
| Status | SPERRLISTE (S0) · nicht ausführen · nicht in BENCHMARK-SEILSTATIK\Skripte ablegen |
| Geprüft gegen | model.db M5 (NodalLoad, Section, LoadCombination), TEILABGLEICH members/lines/nodes.csv, input_3.json (RF5-COM-Export U10), Bridge E5 (belegte SDK-Oberfläche), BEFUND Rev0, ADDENDUM Rev0 |
| Prüfer | ID-03 · Freigabe der Sperre: ID01 |

## 1 Gesperrte Skripte und Hauptgründe

| Skript | Sperrgrund (je ein Beleg) |
|---|---|
| rf5_export.py / boeb_rf5_export.py | Quellmodell `13bb_ausführungsstatik_1.rf5` = Vorläufer U6a (Rev01 K1). COM-Aufrufe `GetObjectCount(1,0)`, `GetNode(i)`, `GetLoadCaseCount()` in keinem vorhandenen Export belegt. Keine Lasten, keine LK-Faktoren. Funktionierender Export von U10 existiert (input_3.json, 23.09.). |
| boeb_rf6_generator.py | SDK-Methoden/Klassen unbelegt (`create_model`, `delete_all_objects`, `CrossSection`, `api_key_name`, `save_model(path)`, `rfem.results.STATIC_…`). E-Modul ×100 statt Pa. G3-Siebenpunkt statt VAR-A-Zweipunkt (E1). LF10 „11,2 kN“. Keine Querschnittsparameter, Lager-DOF, Analyse-Einstellungen, Stab-/Temperaturlasten, RK1/RK2. |
| boeb_full_pipeline.py | kettet gesperrte Skripte ohne Hash-Gates. |
| boeb_bereinigung.py | **LF10-„Fix“ 30 × 1,000 kN → 14 × 0,80 kN**: widerlegt. model.db M5: LF10 = 1 Knotenlast, Fz = 1 000 N, Knoten 1–30, Σ 30,0 kN (Knotenlasten-CSV 07.10.). Lastannahmenänderung gegenüber geprüfter Bestandsstatik ohne AG/Prüfstatiker. „EN 1990 5.1.3“ als Regel für „Bereinigung ≠ Modelländerung“ existiert nicht. Zählung „105 − 19 = 86“ falsch (106 − 20). Löschlisten selbst sind korrekt (158, 178–193; 3025–3028, 3057–3072 ohne 3059, 3095; QS 14–17). |
| boeb_delta_matrix.py | Vergleicht Koordinaten aus der Verformungstabelle (dort stehen u, keine Koordinaten). η gegen Z_Bk 47 kN statt F_Rd 27,9 kN (DIN EN 1993-1-11, γ_R·γ_M = 1,5·1,1). Schwelle „u_res > 50 mm = P0“ ist für ein Seilnetz mit u ≈ 2,08 m unsinnig. Keine RF5-Referenzwerte trotz Docstring. Soll-Werte Blatt 6 (u_Kn17 2,085 m, N_S54 17,47 kN) fehlen. |

## 2 Unbelegte Zahlen aus denselben Quellen (Meta AI / Folgeantworten)

14 Ringleuchten · 0,80 kN · 11,2 kN · 24 kN · „168 % Überlast“ · „L = inf“ · „Fehler 10134“ · „±50 mm Toleranz Gabelspannschlösser“ · „1 Arbeitstag“ · „EN 1990 5.1.3“.

## 3 Was aus den Vorlagen übernommen werden darf

- Löschlisten (identisch mit MODELL-DIFF Rev0 §1/§2 und Patch E7).
- Idee Neuaufbau aus Tabellendaten (validiert am 07.10., siehe Antwort „Zwei-Modell-Workflow“).
- Blattstruktur Delta-Matrix nur in der Fassung `26_10_06_ID-03_DELTA-MATRIX_BLATT6_VORLAGE_Rev0.md`.

## 4 Gültiger Pfad (unverändert)

1. `api_write_check.py` lokal → Feldnamen belegt.
2. E9 (Schubsteifigkeit QS 10/11/12), P2 (QS-14-Cluster), F5 in WORKING_CALC.
3. Lasten aus model.db M5 (Knotenlasten liegen vor; Stab-/Temperaturlasten folgen) + Geometrie/Lager/Rechenparameter aus input_3.json → Datenbasis Modell A.
4. Generator Modell A → Kalibrierung gegen U10 → Modell B (Patch E7) → Delta-Matrix Blatt 6.
