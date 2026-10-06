# QUELLENLOG — RF6 (Modell 001, Migration RF5 → RF6, Exporte, Läufe)

| Feld | Wert |
|---|---|
| Datei | `00_Quellenlog/RF6/26_10_06_ID-03_Quellenlog_RF6.md` |
| Rolle | ID-03 (Claude) · Pflege: ID01 / Codex (lokal) |
| Status | CANDIDATE Rev0 · **kein RF6-Rechenlauf registriert** |
| Software | RFEM 6.12.0008 (SDK dlubal.api 2.12.8), API-II gRPC 127.0.0.1:9000 |
| Kanon | BEFUND RF5/RF6/VAR-A Rev0 §2 · TEILABGLEICH summary.json · MODELL-DIFF QS14 Rev0 |

## 1 Modelle und Hashes

| M-ID | Datei | Ort | Datum | SHA-256 | Inhalt | Rolle | Status |
|---|---|---|---|---|---|---|---|
| M1 | 26_10_06_SEILSTATIK-MODELL-001.rf6 (2 309 460 B) | Drive 119Unwcdhj5MEfUiOmmlR59FlIh2-PaYt · lokal BENCHMARK-SEILSTATIK | 06.10.2026 10:40 | 1286822edbe6c738933e401619b5cd2df0df032b1c62f3306be19c28573db3cd | 106 Kn, 105 Linien, 105 Stäbe, 17 QS, 14 Mat, 19 LF, 21 LK; = V01 topologisch 1:1 | **Original RF6, nicht ändern** | VERIFIED (Hash lt. summary.json) |
| M1b | 26_10_06_SEILSTATIK-MODELL-001.rf6bak (2 309 257 B) | Drive 19mrwOyWN0hMNLaR3SiWS4JwZVUQMAtcH | 06.10.2026 | – | RFEM-Backup | Archiv | FOUND |
| M2 | 01-Gesamtmodell-Seilabspannung_V01.rf5 (11 567 104 B) | EXPORT\…\02 RFEM-Modelle\RFEM-MODELL-Gesamt\ | 04.07./07.09.2026 | 47751311e24e993450e891bcd61feba2c3dff12d26cdc6d2f919a0e23b14db36 (≠ Freeze 7DB74920…) | Importquelle für M1 | Importbasis, nicht Rechenbasis | CONFLICT (Hash-Drift N11) |
| M3 | BOEB_BESTAND-5e_NEUBERECHNET_RFEM529_20260923_1437.rf5 | SANDBOX\05_RECHENSTAND | 23.09.2026 | 317D78D7AF7837F402928221C504F06B48AF6153BF1B60C53DE440A109FE4E12 | 86 Kn / 88 Stäbe / 19 LF / 21 LK | **Kalibrierreferenz** (u_Kn17 2,085 m, N_S54 17,47 kN) | VERIFIED 23.09.; mtime 30.09. → Hash neu prüfen |
| M4 | BOEB_VAR-A_…_VORLAEUFIG_20260923_1437.rf5 | SANDBOX\05_RECHENSTAND | 23.09.2026 | EAB6A5B1A31D4C14746ECBDA27480D8D514FD8F10F30B208AE4E4C80E42EC970 | 84 Kn / 86 Stäbe | VAR-A Zielgeometrie | VERIFIED 23.09. |
| M4b | …_1437.1.rf5 (48 619 520 B) | SANDBOX\05_RECHENSTAND | 30.09.2026 | – | unbekannt | Konfliktkopie | **SPERRLISTE bis Hash + Wiederöffnung** |
| M5 | 26_10_06_SEILSTATIK-MODELL-001_WORKING_CALC.rf6 | – | geplant | – | M1 + Patch (A = 0,38 cm² prüfen, QS 14 löschen, VAR-A-Geometrie) | Arbeitskopie | **existiert noch nicht** |

## 2 Exporte, Protokolle, Skripte

| E-ID | Datei | Drive-ID | Datum | Inhalt | Status |
|---|---|---|---|---|---|
| E1 | 26_10_06_RF6-AUSDRUCKPROTOKOLL-001.pdf (14,8 MB) | 1flvOcGTPA3QKmNvGgfFwhMWzta90ZZU0 | 06.10. 10:42 | RF6-Ausdruck M1 | nicht gelesen |
| E2 | 26_10_06_RF5-AUSDRUCKPROTOKOLL_Gesamtmodell-V1-WORKING(mit-angepasster-Geometrie).pdf | 1QAhMcR2hvvTk3Wt3rS7955cjfJhARaOK | 06.10. 11:20 | RF5-Ausdruck V01 (20 S.): Lager §1.7, QS §1.13, LF, LK | gelesen (BEFUND Rev0) |
| E3 | 26_10_06_ID-03_SEILSTATIK_RF5_RF6_TEILABGLEICH.zip | 1o_GYZlL59GwJtw6_RfSLPsusJGep5PwL | 06.10. 11:24 | nodes/lines/members.csv, summary.json, compare_models.py, sources/* | gelesen |
| E4 | 26_10_06_ID-03-rf6_model_export.py | 1Yefs-aU3ElvuKy_mWQiUyFCcyuAE1dKq | 06.10. 16:35 | read-only Export model.db → CSV + manifest.json (kein API-Lauf) | getestet mit Testmodell |
| E5 | 26_10_06_ID-03-RFEM6_MCP_Bridge_Extended.py v1.0.0 | 10briGfFIdYYBesyAK3m2mT5sZQXXtFYD | 06.10. 11:00 | API-II-Bridge: `--check`, `--export DIR` (INPUT_MODELL.txt + RESULTATE/*.csv + MANIFEST.json), MCP-Tools read-only | lokal zu testen |
| E6 | 26_10_06_ID-03-RF6-Ergebnis-Export.py | **in Drive nicht vorhanden** (Stand 06.10. 20:00) | – | lt. Auftrag 1: 3 CSV + API_Log.json | **CANDIDATE** siehe `tools/` im Repo |
| E7 | 26_10_06_ID-03-RF6_GEOMETRIE_PATCH_VARA_Rev0.json | 1TdRcnL3SEARibNJRcGZKOXBhzXmLa-zB | 06.10. 16:35 | Patch-Vorschlag für M5 (6 Knoten, Stäbe/Knoten löschen, Lager 3006/3007) | VORSCHLAG, nicht angewendet |
| E8 | Screenshots RF6 (LF31/43/50/60, QS-14-Fehler, Dateiname, Ausdruck) | 1APAuBvcVwyGJ…, 1ggnX3KWyF6X4…, u. a. | 06.10. | Sichtbelege Import | FOUND |

## 3 Run-Register RF6 (fail-closed: ohne Zeile kein Ergebnis)

| RUN-ID | Modell (Hash) | Datum | Solver | Loadings | Ergebnisdateien (SHA-256) | Kalibrierung Δ | Status |
|---|---|---|---|---|---|---|---|
| RUN-RF6-000 | M1 1286822e… | – | – | – | Baseline-Export Auftrag 1 (ausstehend) | – | **ausstehend** |
| RUN-RF6-001 | M5 (–) | – | Th. III. O., Newton-Raphson, g = 10,00 m/s² (E7 offen) | LK100, RK1, LK220 | – | Soll: u_Kn17 2,085 m, N_S54 17,47 kN (Toleranz E8 offen) | geplant |

## 4 Offene Entscheidungen mit RF6-Wirkung (aus BEFUND Rev0 §8)

E1 Geometriebasis VAR-A statt G3 · E2 Maste 1006/1007 entfallen, 3006/3007 gelenkig · E3 C21 Fall A/B · E4 Kombinatorik EN 1990 vs. Bestand · E5 Bezugstemperatur 0 °C vs. T₀ 10 °C · E6 Seil 35 Stablasten · E7 g 10,00 → 9,81 · E8 Kalibriertoleranz.
