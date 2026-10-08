# WEGWEISER — wo liegen die Daten für den Skill `seilstatik-rf5-rf6-neuaufbau`

Lokal = `G:\Meine Ablage\_INDEX_LNK\BENCHMARK-SEILSTATIK\` (Drive für Desktop, synchron mit Drive-Ordner 1ZpE9ym5UVEJuiLml0YKXDQl8Qk878sZl). Repo = `julianzotter/julianzotter`, Branch `claude/seilstatik-doku-overview-rc0lpt`.

## 1 Eingaben je Schritt

| Schritt | Was | Wo (Drive-ID / Pfad) | Status |
|---|---|---|---|
| 1 | **Referenz: RF5 Gesamtmodell `13bb_ausführungsstatik_1.rf5` Fassung 2015** (54 054 912 B, SHA-256 73242E1346AB6556…; vereinbart mit P. Kneidinger, ID01 07.10.) | lokal `00_BESTAND_KOPIE\RFEM5_2015\` (= EXPORT\…\statistik-unterlagen-150325) | VERIFIED 08.10.; Fassung 54 075 392 B (EXPORT\…\04 Berechnung Gesamtsystem, geändert 06.10.2026, C88F7792…) **nicht verwenden** |
| 1 | RF5 Berichtsmodell 5e `…150328_5e.rf5` (SHA BD77CF83…) | EXPORT\…\14_bb\statistik-unterlagen-150325\ (lokal, G:) | VERIFIED, nur Querkontrolle |
| 1 | PDF Bestandsstatik U1 (62 S.) + Ergänzung 2 (LK220) | EXPORT\00 Bestandstatik fragmentiert\…\13bb-statik-dokumentation\ (lokal) | FOUND, nicht im BENCHMARK-Ordner |
| 1 | RF5-Ausdruck V01 (20 S., Lager §1.7, QS §1.13, LF, LK) | Drive 1QAhMcR2hvvTk3Wt3rS7955cjfJhARaOK | gelesen (BEFUND Rev0) |
| 1 | RF6-Ausdruckprotokoll M1 (14,8 MB) | Drive 1flvOcGTPA3QKmNvGgfFwhMWzta90ZZU0 | nicht gelesen |
| 1 | Geometer V1 `7864Halterungen_mit_Lampenplan_Boardinghouse.xlsx` (7100–7108, Landeskoordinaten, Zuordnung RFEM) | Drive 1j-GHSEH7x_JsUppBplMaQYvcwje6EhKe | PRIMARY |
| 2 | RF5-COM-Export U10 (`input_3.json`, Knoten/Stäbe/Mat/QS/Lager/Parameter) + `lines.csv`, `members.csv` | Drive TEILABGLEICH.zip 1o_GYZlL59GwJtw6_RfSLPsusJGep5PwL (sources/) | gelesen, SHA 394820eb… |
| 2 | Lasten/LK aus RF6-Arbeitskopie `model.db` (M5, .rf6bak SHA 903093dd…) | Drive-Ordner 1opSMplUY91rtVnztdlam9ZbhVA3FgMOf | gelesen |
| 2 | CSV v0.1 aus 5e (01–09, B_VARA 10–14, MANIFEST) | `Daten\input\EINGABEDATEN_RF6_v0.1\` · Drive 1ZPr8x8H81DXt6qQAHICKe8huZ1-nMmuO · Zip 1-0r03VNC5jV_xm8rALgGfDS40MFn9vs7 | **gültiger Modell-A-Datensatz** nach D2a (Geometrie 13bb ≡ 5e, Lasten 5e = Bericht); Export v0.2 aus 13bb entfällt |
| 2 | Vergleich 13bb ↔ 5e (Eingaben Feld für Feld, Ergebnisse je LK/Stab/Anker, RFEM-CSV-Export 21 Blätter je Modell, Skripte) | lokal `09_VERGLEICH_13bb_vs_5e_20261008\`, `00_BESTAND_KOPIE\RFEM5_2015\<modell>\*.csv`, `04_SKRIPTE_REPRO\` → nach `00_Quellenlog\RF6\` kopieren | vorhanden lokal 08.10., Drive-Kopie + Hash offen |
| 2 | Lesbare Tabellen `EINGABETABELLEN_RF6_v0.1.md` | Drive 13UTLAfnGGE1VP1iQt5iOnOaej6gSYFRz | CANDIDATE |
| 2 | `10–12_resultate_rf5_*.csv` (N, Lager, u je LK) | aus lokalem 5e-Ergebnisexport (`ERGEBNISVERGLEICH_13bb_vs_5e.xlsx`, Roh-CSV 5e) nach Vertrag §5 ableiten | Quelle vorhanden, Tabelle noch zu erzeugen |
| 3 | Patch zwei Haltepunkte `10_patch_vara_rev0.json` | `Daten\input\EINGABEDATEN_RF6_v0.1\B_VARA\` · Drive 1_4Xn1lhGCt5F0iU7HDKTFWTg-vC6d3jp | Rev0 |
| 3 | Zuordnung Geometer ↔ RFEM (V9) `…AEQUIVALENZ-KNOTEN…Rev0.csv` | Drive 1pnPWQTNqXODcQCdJ1NmOFOcybO_eil5G | DERIVED-KANON |
| 3 | Topologie-Gate C06/C07 (Plan + Höhenkontrolle) | `Befunde\26_10_07_ID-03_TOPOLOGIE-GATE_C06-C07_LAMPENPLAN_Rev0.md` · Drive 1Fx_VzssiwtKoq-kv9CDZ5R01m1IesfM5 | ERFÜLLT |
| 3 | Kurzbericht VAR-A 23.09.2026 (Transformation T1, 84/68/18) | Drive-Suche „KURZBERICHT_RFEM_VAR-A" | Quelle für T1 |
| 4 | `26_10_06_ID-03_api_write_check.py` | `Skripte\` · Drive 1YAyxwF66RVlC5ZNk0bWDQZ0OJxiCE9mk | CANDIDATE |
| 4 | Bridge E5 `26_10_06_ID-03-RFEM6_MCP_Bridge_Extended.py` (api_key_value, execute(), raw_results, snapshot) | lokal `Skripte\` (nicht im Repo) | belegt, SDK 2.12.8 → 2.13.1 nötig |
| 5 | Generator Modell A aus CSV | **fehlt** → nach Schritt 4 schreiben (Vorlage: `retour_rfem6_patch.py` need()-Muster, `make_eingabedaten.py` Tabellen) | OFFEN |
| 5–8 | `26_10_06_ID-03-RF6-Ergebnis-Export.py` (3 CSV + API_Log) | `Skripte\` · Drive 1gUwpP78z2UF8krSoqD9cl3xwJXwhbdlG | CANDIDATE |
| 6 | Kalibrierziele u_Kn17 2,085 m, N_S54 17,47 kN; Delta-Matrix Vorlage Blatt 6 | `Befunde\26_10_06_ID-03_DELTA-MATRIX_BLATT6_VORLAGE_Rev0.md` · Drive 1UrIB7cf3LTBdxXsle8ZWlw1DB0rL66LT | Rev0 |
| 7 | `26_10_06_ID-03_retour_rfem6_patch.py` + `gates.json.example` | `Skripte\` · Drive 1yG40SCCbz3vjF_nkr7gZDigdkupUfGGa | Dry-Run geprüft |
| 9 | `26_10_06_ID-03_anpassen_rf6.py` (Delta-Auswertung) | `Skripte\` · Drive 13KBaOIRlTxQu_BcOMl1LT1wqFjX0ELa7 | CANDIDATE |
| 9 | F_Rd 27,9 kN (F_Rk 46,1 kN, γ_R·γ_M = 1,5·1,1), ETA-11/0160 | Quellenlog Ursprung U9b | FOUND |
| 10 | Quellenlog Ursprung / Vermesser / RF6 (Run-Register §3, Pfade §6) | `00_Quellenlog\` · Drive-Ordner RF6 1UllYfuGwqUM5khZyAH4cUyMc60Lo6TrV (aktuelle Datei `…Quellenlog_RF6_Rev1.md`) | Rev0/Rev1 |

## 2 Beschaffung (ID01), blockiert Schritte 1/2/9

| Objekt | Wofür | Von wem |
|---|---|---|
| U1 PDF Bestandsstatik Teil I–III (62 S.) in den BENCHMARK-Ordner kopieren | Schritt 2 Resultate, Schritt 10 | lokal EXPORT-Ordner |
| 13bb: Datum der Vereinbarung mit P. Kneidinger (V3); Bestätigung D2a (Geometrie 13bb = 5e, Lasten 5e) | Schritt 1 | ID01 |
| U9 PFEIFER K15.105 (Lsys, Beschläge) | Seillängen S19/S22, F7 | PFEIFER / Archiv |
| VF1 Lochmitte 7101/7102 (Bolzenachse) | Nulllage 3006/3007 | Geometer |
| Prüfberichte PB00–PB03 | Vergleichswerte Bestand | Prüfstatiker |

## 3 Entscheidungen, die in `Skripte\gates.json` stehen müssen

| Gate | Inhalt | Stand |
|---|---|---|
| E1 | Geometriebasis T1 (VAR-A, zwei Punkte) | durch Entscheidung 07.10. gesetzt: zwei Haltepunkte |
| E2 | Maste 1006/1007 entfallen, 3006/3007 gelenkig | durch Entscheidung 07.10. gesetzt |
| P2 | QS-14-Hilfsgeometrie nicht übernehmen | in Modell A ohnehin nicht enthalten |
| E3 | C21 (3021) unverändert lassen | Entscheidung „alles andere bleibt" → unverändert |
| E4 | LK220 ergänzen | offen |
| E8 | Kalibriertoleranz Schritt 6 | offen (Vorschlag N ±2 %, u ±3 %) |
| E9 | Schubsteifigkeits-Flag QS 10/11/12 | offen (nur Arbeitskopie M5; Modell A aus CSV hat RF5-Flags) |
| F7 | Beschlagmaß S19/S22 | offen (U9) |

## 4 Nicht verwenden

Fremdskripte `rf5_export.py`, `boeb_bereinigung.py`, `boeb_rf6_generator*.py`, `boeb_delta_matrix.py`, `boeb_pfeifer_mapping.py`, `boeb_full_pipeline.py`, `tabellen_generator.py`, `boeb_import.py`; Excel V02/V04; `transformed_nodes.csv` (G3-Siebenpunkt); Docx FERTIGSTELLUNG „Fall B". Begründung: `Befunde\…SPERRLISTE…`, Loop 1, Loop 2, Gegencheck-Antwort (alle im Ordner Befunde, Drive 1tSNvcVz-dGZEZXX5bH-qUNX7tzs5F6PA).

## 5 CSV-Verträge (verbindlich; UTF-8 mit BOM, Trennzeichen `;`, Dezimalpunkt, Einheiten im Spaltennamen, erste Zeile Kopf, keine Formeln)

| Datei | Spalten | Schlüssel | Einheit |
|---|---|---|---|
| 01_knoten | no; x_m; y_m; z_m; quelle | no | m, RFEM lokal, Z nach unten + |
| 02_staebe | no; linie; knoten_i; knoten_j; typ_rf5 (9 Seil / 1 Balken); typ_text; qs_start; qs_ende; laenge_m; quelle | no | m |
| 03_materialien | no; bezeichnung; E_kN_cm2; G_kN_cm2; nu; gamma_kN_m3; alpha_T_1_K; gamma_M; hinweis | no | kN/cm² (API: ×1e7 → Pa) |
| 04_querschnitte | no; bezeichnung; material; A_cm2; Ay_cm2; Az_cm2; It_cm4; Iy_cm4; Iz_cm4; verwendung | no | cm², cm⁴ (API: ×1e-4 / ×1e-8 → m², m⁴) |
| 05_lager | no; knoten (Liste); ux; uy; uz; phix; phiy; phiz (fest/frei/Federwert); drehung_z_rad; hinweis | no | rad |
| 06_rechenparameter | parameter; wert; hinweis | parameter | – |
| 07_knotenlasten | LF; nr; Fx_kN; Fy_kN; Fz_kN; anzahl; knoten (Liste) | LF+nr | kN (API: ×1e3 → N) |
| 08_stablasten | LF; lf_name; nr; art (Streckenlast_kN_m / Temperatur_dT_K); wert; richtung_code_rf6; anzahl; staebe (Liste) | LF+nr | kN/m, K |
| 09_lastfaelle_lastkombinationen | typ (LF/LK); nr; name; actionCategoryId; definition (Faktor*LF + …); quelle | typ+nr | – |
| 10_resultate_rf5_staebe (**neu, aus 13bb/PDF**) | LK; stab; N_min_kN; N_max_kN; x_m; seite_pdf; quelle | LK+stab | kN |
| 11_resultate_rf5_lager (**neu**) | LK; knoten; Px_kN; Py_kN; Pz_kN; seite_pdf; quelle | LK+knoten | kN |
| 12_resultate_rf5_knoten (**neu**) | LK; knoten; ux_m; uy_m; uz_m; seite_pdf; quelle | LK+knoten | m (liefert auch R2 für Kn 8) |
| T01–T09 (Teilmodell) | wie 01–09, zusätzlich T01: x_m_B; y_m_B; z_m_B; rolle; in_modell_A_T; in_modell_B_T · T02: in_modell_B_T; weggelassen_am_schnitt · T05: knoten_im_teilmodell; in_modell_B_T | wie oben | wie oben |
| T10_randbedingung_schnittknoten | knoten; LK; option_R1; option_R2_ux_m; option_R2_uy_m; option_R2_uz_m; quelle_R2 | knoten+LK | m |
| T11_change_allowlist | objekt; id; aktion; alt; neu; grund; freigabe | objekt+id | – |
| rf6_writeback_audit (Schritt 5/7) | gruppe; objekt_id; feld; csv_wert; rf6_wert; status (OK/ABWEICHUNG) | gruppe+objekt_id+feld | SI wie API |
| 01_Seilkraefte_N / 02_Lagerkraefte_global / 03_Knotenverformungen (Export E6a) | wie vom Export-Skript geliefert (API-Felder), plus run_id | LK+objekt | N, m (API) |
| rf5_rf6_comparison (Schritt 9) | LK; objekt_typ (Seil/Lager/Knoten); id; groesse; RF5; RF6_A; RF6_B; delta_B_minus_RF5; delta_rel; status (APPROVED_CHANGE / SOFTWARE_MAPPING / ROUNDING / UNAPPROVED) | LK+objekt_typ+id+groesse | kN, m |

Vergleichsschlüssel: Seil = LK + Stab-Nr; Lager = LK + Knoten; Knoten = LK + Knoten-Nr. Vorzeichen: Z nach unten positiv, Zug positiv. Nullschwelle für δ: |RF5| < 0,1 kN bzw. 1 mm → nur Δ absolut.

## 6 Minimaler Datensatz für den heutigen Rechenlauf (Teilmodell, so wenig wie möglich)

| Nr | Datei | Zeilen | Status |
|---|---|---|---|
| 1 | T01_knoten (16, davon 2 nur A-T) | 16 | vorhanden |
| 2 | T02_staebe (15 + 2 weggelassen dokumentiert) | 17 | vorhanden |
| 3 | T03_materialien (Mat 5 Seil, Mat 6 S 235 J2 G3) | 2 | vorhanden |
| 4 | T04_querschnitte (QS 1, 4, 5, 12) | 4 | vorhanden |
| 5 | T05_lager (6 Objekte + NEU-B + RAND-8) | 8 | vorhanden; Drehung 3006/3007 = Auflage ID01 |
| 6 | T06_rechenparameter | 28 | vorhanden |
| 7 | T07_knotenlasten (gefiltert) | 16 | vorhanden |
| 8 | T08_stablasten (gefiltert, 12 Seile) | 18 | vorhanden; Richtungscodes gegen RF5-Ausdruck prüfen |
| 9 | T09 LF/LK | 41 | vorhanden; LK220 Entscheidung E4 |
| 10 | T10 Randbedingung Kn 8 | 22 (je LK) | R1 sofort; R2 braucht 12_resultate_rf5_knoten |
| 11 | T11 change_allowlist | 8 | vorhanden |
| 12 | 10/11/12_resultate_rf5 (Vergleichswerte, T-G1) | – | **fehlt** → heute aus RF5 13bb (COM oder Ausdruck) für LK100 mindestens: N S17, S18, S19, S22, S60, S63, S64, S81; Lager 105, 106, 113, 114, 2021; u Kn 8, 9, 10, 29, 30 |

Alles andere (Gesamtmodell 86/88, übrige LF-Knotenlisten, Hilfsgeometrie, Fremddaten) ist für den heutigen Lauf nicht erforderlich.

Ablage: `Daten\input\EINGABEDATEN_RF6_TEILMODELL_v0.1\` (lokal/Drive) · Generator `Skripte\26_10_07_ID-03_make_teilmodell.py` · RF6-Tabellenexport als Readback-Format: lokaler Ordner `…\BENCHMARK-SEILSTATIK\` (Index `26_10_07_ID-03-Stäbe+Stabendgelenke-json.txt`, Drive 14gCnIvxV8PtLj7Jm7rj6aMxsBcAHp4_m; enthält u. a. `Knoten-Zwangsverformungen.csv` für R2 und `Stabnichtlinearitäten.csv` für Seil = nur Zug).
