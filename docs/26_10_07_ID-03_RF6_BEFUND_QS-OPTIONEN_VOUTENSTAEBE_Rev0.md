# BEFUND RF6 — Plausibilitätsfehler Stab 1001 (Querschnittsoptionen Voutenstäbe) — Rev0

| Feld | Wert |
|---|---|
| Datum | 07.10.2026 03:5x (Screenshot RFEM 6.13.0001, `…_WORKING_CALC.rf6*`) |
| Fehlermeldung | Plausibilitätskontrolle: Objekt Stab Nr. 1001, Eingabefeld „Querschnitt – Am Stabende j“: „Inkompatible Berechnungsoptionen der Querschnitte. Alle Querschnitte in einem Stab müssen die gleichen Berechnungsoptionen haben.“ |
| Datenquelle | model.db der Arbeitskopie (.rf6bak SHA 903093dd…, read-only), Tabelle `SectionImplParametricThinWalled`; Stab-QS-Paare aus TEILABGLEICH members.csv |
| Status | CANDIDATE · Inhaltsprüfung ✔ · keine Änderung am Modell |

## 1 Ursache (belegt)

Voutenstäbe (Mast, QS Anfang ≠ QS Ende) mit unterschiedlichem Flag `shearStiffnessDeactivated` (Schubsteifigkeit deaktiviert):

| Stab | QS i → j | Flag QS i | Flag QS j | Konflikt |
|---|---|---|---|---|
| **1001** | 3 → 10 | 1 (aus) | 0 (ein) | **ja** (gemeldet) |
| **1003** | 11 → 4 | 0 (ein) | 1 (aus) | **ja** (folgt nach Fix 1001) |
| **1021** | 12 → 4 | 0 (ein) | 1 (aus) | **ja** (folgt) |
| 1002, 1004–1012, 1014–1016, 1019, 1020 (15 St.) | 5 → 4 | 1 | 1 | nein |
| 1017, 1018 | 9 → 8 | 0 | 0 | nein |

`warpingStiffnessDeactivated` = 1 bei allen 17 Querschnitten → kein Konflikt.

## 2 Behebung (RFEM 6, Arbeitskopie)

Querschnitte → QS 10, 11, 12 öffnen → Reiter Berechnungsoptionen → „Schubsteifigkeit berücksichtigen“ auf denselben Zustand wie QS 3/4/5 setzen (= deaktiviert, wie bei 17 von 20 Masten). Alternativ QS 3, 4, 5 aktivieren; dann sind alle 20 Maste mit Schubsteifigkeit. **Entscheidung E9 (ID01)**: einheitlich AUS (Mehrheit, RF5-Import) oder einheitlich EIN. Einfluss auf Seilkräfte: Maste KR 405/185 → 200/82 sind gegenüber den Seilen sehr steif; Schubverformung der Maste ist für N und u der Seile vernachlässigbar, für die Kalibrierung K1–K7 aber zu protokollieren.

## 3 Nächster erwarteter Fehler

Nach E9 meldet die Plausibilitätskontrolle voraussichtlich QS 14 (`bp-beleuchtung`, b = h = 0) an Stab 158/178/179–193 → P2 (löschen: 17 Stäbe, 20 Knoten inkl. 3095, 17 Linien, QS 14–17). Screenshot-Tabelle bestätigt: Zeilen 159–177 leer, 178–181 Balkenstab QS 14 noch vorhanden.

## 4 Korrekturen an den beiden eingefügten Anleitungen

| # | Aussage | Korrektur | Beleg |
|---|---|---|---|
| 1 | „Ersatzlast 1,000 kN an Knoten 1–30 in LF10 setzen (zuerst!)“ | **Nicht setzen.** Leuchtenlast 1,000 kN an Kn 1–30 ist in LF10 bereits vorhanden; QS-14-Stäbe tragen keine Lasten. Zusätzliche Last = doppelte Leuchtenlast. | BEFUND Rev0 §6 LF10; ADDENDUM B9 |
| 2 | Stäbe „158, 159, 179–193“ | 158, **178**, 179–193. 159 ist die Linie von Stab 178. | ADDENDUM K1; Screenshot (Zeile 159 leer, 178 vorhanden) |
| 3 | „Fehler 10134, Knoten 3025 frei in X, Steifigkeitsmatrix singulär“ | Der gezeigte Fehler ist die Plausibilitätskontrolle an Stab 1001 (§1), kein Solver-Fehler. Die Singularität der isolierten Cluster kommt erst nach E9 und ohne P2. | Screenshot |
| 4 | „Stab 64 zu Knoten 114/3062/3063 klären“ | Stab 64 = Seil S64 (A14 ↔ RL), keine Verbindung zu Hilfsknoten. 3062 trägt nur Stab 182, 3063 nur 183. | MODELL-DIFF §1/§2 |
| 5 | „Hängt an 3025–3072 ein Lager? Zuerst klären“ | Bereits belegt: kein Lager an Hilfsknoten, kein Lager an Kn 6. | ADDENDUM B7/B8; MODELL-DIFF §2 |
| 6 | „19 Knoten“ | 20 Knoten: zusätzlich 3095 (0/0/0, ohne Stab). | MODELL-DIFF §2 |
| 7 | „Deaktivieren statt löschen“ | Als reversibler Zwischenschritt zulässig. Die Plausibilitätskontrolle prüft QS 14 (h = 0) möglicherweise auch an inaktiven Stäben; dann bleibt nur Löschen (Kanon P2, Patch E7). Backup liegt vor (.rf6bak 903093dd…). | ADDENDUM K7 |
| 8 | „Modellierungsfehler aus dem Bestand“ | Nein: Hilfsgeometrie existiert nur in V01/RF6 (DXF-Import, z = 0,284), nicht in Bestand 5e (86 Kn / 88 Stäbe). | BEFUND Rev0 §5 |

## 5 Reihenfolge jetzt

1. E9: Schubsteifigkeits-Flag QS 10/11/12 angleichen (oder 3/4/5), Entscheidung notieren.
2. P2: QS-14-Cluster löschen (Liste MODELL-DIFF §1/§2), Kontrolle 86 Kn / 88 Stäbe.
3. Speichern, SHA-256 der .rf6 ins Quellenlog RF6 §1 (M5).
4. F5 → Results ✓ → E6a-Export → Phase 2.
