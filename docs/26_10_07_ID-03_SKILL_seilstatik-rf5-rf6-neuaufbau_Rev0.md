---
name: seilstatik-rf5-rf6-neuaufbau
description: Arbeitsauftrag Seilstatik Böblingen (GZ 26_001, Ergänzung 4). Bestandsstatik (RF5 + PDF-Doku) vollständig nach CSV extrahieren, neues RFEM-6-Modell aus den CSV über die API einspielen, dabei nur die zwei geänderten Haltepunkte (C06/C07 → Fassadenanker, RFEM 3006/3007) anpassen, alles andere unverändert lassen, dann RF5-Bestandsergebnis gegen RF6-Neuberechnung vergleichen. Use when the user says "Seilstatik", "RF5 → RF6", "Neuaufbau", "Ergänzung 4", "Böblingen", "Delta RF5/RF6", or asks to run, continue or audit this pipeline.
---

# SKILL — RF5-Bestand → CSV → RFEM 6 (zwei neue Haltepunkte) → Vergleich

## 0 Entscheidung (ID01, 07.10.2026) — verbindlich

1. Aus der Bestandsstatik (RF5-Modell + PDF-Ausdruck) werden **alle** Rechenmodelldaten in CSV extrahiert: Systemgeometrie, Material, Querschnitte, Knoten, Stäbe, Auflager, Lasten, Lastfälle/-kombinationen, Resultate.
2. Das neue Modell übernimmt diese Daten 1:1. Geändert werden **nur die zwei neuen Auflagerpunkte** (C06/C07 → Fassadenanker: Knoten 3006/3007, Maste 1006/1007 mit Füßen 2006/2007 entfallen). Alles andere bleibt: Knoten, Seile, übrige Maste, Lager, Lasten, Kombinationen, Rechenparameter.
3. Einspielen nach RFEM 6 über CSV-Tabellen + API (dlubal.api, gRPC).
4. Verglichen wird **nur** Ausgabe RF5-Bestandsberechnung gegen Ausgabe RF6-Neuberechnung. **Referenz = RF5-Gesamtmodell `13bb_ausführungsstatik_1.rf5`, Fassung 2015** (54 054 912 B, SHA-256 73242E1346AB6556…; mit P. Kneidinger vereinbart, ID01 07.10.2026). Die am 06.10.2026 gespeicherte Fassung (54 075 392 B, C88F7792…) ist verändert und kein Bestand. Befund 08.10. (COM-Vergleich): Geometrie/System 13bb ≡ 5e (nur Knoten 16↔17 anders nummeriert); Lasten/LK/RK sind in 13bb unvollständig und in 5e = Bestandsbericht. **Vorschlag D2a:** Geometrie aus 13bb = 5e, Lasten/LK/RK aus 5e → Modell A = Datensatz v0.1 (Bestätigung ID01).
5. Nichts anderes: keine Vorspannung als Eingabe, keine Formfindung, keine Laständerung, keine Siebenpunkt-Geometrie, keine Fremdskripte.
6. **Modellreduktion (ID01 07.10., Nachmittag):** gerechnet wird das Teilmodell um C06/C07 (§6) mit starren oder verschieblichen Randbedingungen an der Modellgrenze. Das Gesamtmodell bleibt Referenz für die Ergebnisse; das Teilmodell muss den Bestand an der Grenze reproduzieren (Gate T-G1), sonst Grenze erweitern.

## 1 Ablaufschema

```
 RF5 (COM, lokal)  ──┐                                  ┌─► RF6 Modell A (Bestand 1:1)  ─► Rechnen ─► Export A ─┐
 PDF-Ausdruck U1   ──┼─► [A] CSV-Extraktion (10 Tab.) ──┼                                                         ├─► [F] Vergleich RF5 ↔ RF6
 Geometer 7101/7102 ─┘        │                         └─► [C] Patch 3006/3007 ─► RF6 Modell B ─► Rechnen ─► Export B ┘        │
                              └─ [B] Readback-Kontrolle CSV ↔ RF6 (Zählwerte, Hashes)                                          └─► [G] Doku Ergänzung 4
```

Zwei Modelle, weil nur so belegt ist, dass der Unterschied RF5 → RF6 aus den zwei Haltepunkten kommt und nicht aus dem Programmwechsel: Modell A kalibriert RF6 gegen RF5, Modell B trägt die Änderung.

## 2 Schnittstellen und Anbindungen

| Kürzel | System | Zugang | Richtung | Werkzeug |
|---|---|---|---|---|
| RF5 | RFEM 5.28, Bestandsmodell `.rf5` | COM (Windows, lokal) | lesen → CSV | bestehender COM-Export (input_3.json-Schema, Quellenlog RF6 E3) |
| PDF | Bestandsstatik-Ausdruck (U1, RF5-Protokoll) | Datei (Drive) | lesen → CSV Resultate | manuell/OCR, Fundstelle je Zahl (Seite) |
| SV | Vermessung (Survey) Geometer 2026, Punkte 7101/7102 | Drive (V1 xlsx) | lesen → Patch | Transformation T1: x = X − 3 500 460,605; y = −(Y − 5 394 418,936); z = −(Z − 445,472) |
| RF6 | RFEM 6.13.0001 | gRPC 127.0.0.1:9000, `dlubal.api==2.13.1`, API-Key | schreiben (Modell) + lesen (Ergebnisse) | Bridge E5 (`…RFEM6_MCP_Bridge_Extended.py`), Skripte in `Skripte/` |
| API | Python-Skripte (Repo `tools/`) | lokal, PowerShell | CSV ↔ RF6 | `api_write_check`, Generator, `RF6-Ergebnis-Export`, `retour_rfem6_patch` |
| MCP | Google Drive (Quellen, Ablage), GitHub (Repo) | Claude-Session | lesen/schreiben Doku | Quellenlog, Befunde, Paket; keine Modelländerung über MCP |
| CSV | Austauschformat, `;`-getrennt, UTF-8, Einheiten m / kN / kN/m / K / cm² / cm⁴ | Datei | SSOT zwischen allen Systemen | `Daten/input/EINGABEDATEN_RF6_v0.1/` |

Regel: Jede Zahl im RF6-Modell stammt aus einer CSV-Zeile; jede CSV-Zeile aus einer Quelle mit Hash (MANIFEST). Keine Handwerte.

## 3 Schritte

### Schritt 1 — Quellen fixieren
- Eingabe: RF5-Gesamtmodell `13bb_ausführungsstatik_1.rf5` (Referenz lt. Vereinbarung mit P. Kneidinger; es existieren zwei Fassungen, 54 054 912 und 54 075 392 B → die mit Kneidinger abgestimmte Fassung benennen), PDF-Ausdruck der Bestandsberechnung, Geometer-Tabelle V1.
- Tun: SHA-256 jeder Datei bilden, in `00_Quellenlog/Ursprung` (U6a) bzw. `RF6 §1` eintragen; Fassung, Datum und Vereinbarungsvermerk notieren. 5e (BD77CF83…) bleibt als Querkontrolle, ist aber nicht die Referenz.
- Stand 08.10.: V1 (Fassung) und V2 (Hash) erledigt, siehe Quellenlog RF6 §6d; V3 (Datum der Vereinbarung) offen.
- Gate: ohne Hash und ohne Fassungsangabe kein Weiterarbeiten. Eingabedaten (Schritt 2) und Vergleichsergebnisse (Schritt 9) müssen aus derselben Datei stammen; nach D2a ist das 5e (Geometrie ≡ 13bb), die gespeicherten 5e-Ergebnisse 2015 sind die Vergleichswerte.

### Schritt 2 — Extraktion RF5 → CSV (Tabellen 01–10)
- Werkzeug: COM-Export RF5 (liefert input_3.json-Schema) → `make_eingabedaten.py` → `01_knoten … 09_lastfaelle_lastkombinationen`. Stand 08.10.: Diff 13bb ↔ 5e liegt vor (lokal `09_VERGLEICH_13bb_vs_5e_20261008\VERGLEICH_13bb_vs_5e.md`, Tabellen als JSON/XLSX); Geometrie identisch, Lasten aus 5e. **Damit gilt v0.1 (aus 5e-Export U10) als Modell-A-Datensatz; ein erneuter Export aus 13bb entfällt** (D2a). Die lokalen Vergleichsdateien nach `00_Quellenlog/RF6/` kopieren und hashen.
- Zusätzlich `10–12_resultate_rf5_*.csv`: aus dem lokalen 5e-Ergebnisexport (`ERGEBNISVERGLEICH_13bb_vs_5e.xlsx`, Roh-CSV `00_BESTAND_KOPIE\RFEM5_2015\5e\*.csv`) je Seil N_min/N_max je LK, Lagerkräfte je Lagerknoten, Verformungen u (LK100/101); PDF-Seite nur als Zweitbeleg. Kontrollwerte 5e: N_max GZT 17,50 kN (CO207), u_max LK100 2 079–2 080 mm.
- Kontrolle (Erwartung aus 5e): 86 Knoten, 88 Stäbe (68 Seile + 20 Maste), 6 Materialien, 13 QS, 27 Lagerobjekte, 19 LF, 21 LK (+ LK220 fehlt), LF10 = 30 × 1,000 kN. Weicht 13bb davon ab, gilt 13bb; Abweichung dokumentieren, nicht „bereinigen".
- Ausgabe: CSV + `MANIFEST.json` (SHA-256 aller Ein- und Ausgaben).

### Schritt 3 — Patch für die zwei Haltepunkte (Modell B)
- Eingabe: Geometer 7101 (C06) und 7102 (C07), Z = 445,020 m beide → z = +0,452 m; XY über T1.
- Tun: `B_VARA/10_patch_vara_rev0.json` verwenden: 3006/3007 neue Koordinaten; Stäbe 1006/1007 löschen; Knoten 2006/2007 und ihre Lager löschen; 3006/3007 Lager gelenkig wie Kn 105 (u fest, φx/φy frei, φz fest; Drehung analog Wandanker, Auflage ID01).
- Nicht tun: 105/106/113/114 verschieben (bleiben Bestand), 3021 ändern (E3 separat), Lasten anfassen.
- Kontrolle nach Patch: 84 Knoten, 68 Seile, 18 Maste, Lager 27 − 2 Objekte + 3006/3007.

### Schritt 4 — API-Schreibzugriff belegen
- `pip install --upgrade dlubal.api==2.13.1` (Server 6.13.0001), dann `python Skripte\26_10_06_ID-03_api_write_check.py > Logs\API_WRITE_CHECK_<stamp>.json`.
- Gate: Verdict `WRITE_API_PRESENT` und Feldnamen für Node/Member/NodalSupport/LoadCase/LoadCombination/NodalLoad protokolliert. Sonst Stopp.

### Schritt 5 — Modell A in RFEM 6 einspielen (Bestand 1:1)
- Neues leeres RF6-Modell `BOEB_MODELL_A_BESTAND.rf6`. Reihenfolge: Material → Querschnitte → Knoten → Stäbe (Seil Typ, Voute QS i→j) → Lager (Drehung φz je Objekt) → Lastfälle → Knotenlasten → Stablasten (Streckenlast, dT) → Lastkombinationen (Faktoren aus 09) → Rechenparameter (Th. III. O., Newton-Raphson, Inkremente aus 06).
- Readback: alle Objekte per `get_object_list` zurücklesen, gegen CSV zählen und je Feld vergleichen; Abweichungen = Stopp.
- Ausgabe: `.rf6` + SHA-256 + Readback-Protokoll in `Logs/`.

### Schritt 6 — Modell A rechnen und gegen RF5 kalibrieren
- Rechnen LK100 (+ alle LK), Export mit `Skripte\26_10_06_ID-03-RF6-Ergebnis-Export.py --run-id RUN-RF6-A01 --out Daten\results` → `01_Seilkraefte_N.csv`, `02_Lagerkraefte_global.csv`, `03_Knotenverformungen.csv`, `API_Log.json`.
- Vergleich mit `10_resultate_rf5.csv`: Kalibrierziel u_Kn17 = 2,085 m, N_S54 = 17,47 kN (LK100); alle Seilkräfte, Lagerkräfte, Σ Lagerkräfte = Σ Lasten (ΣV = 0).
- Gate: Toleranz E8 (ID01 legt fest; Vorschlag N ±2 %, u ±3 %). Bei Überschreitung: Ursache in Eingabedaten suchen (Richtungscodes Stablasten, Schubsteifigkeits-Flag E9, g 10,00 vs 9,81), nicht an Lasten oder Geometrie drehen.

### Schritt 7 — Modell B erzeugen
- Kopie von Modell A → `BOEB_MODELL_B_ERG4.rf6`; Patch aus Schritt 3 über `Skripte\26_10_06_ID-03_retour_rfem6_patch.py --patch … --gates Skripte\gates.json` (erst Dry-Run, dann `--apply`; Gates E1/E2 = FREIGEGEBEN durch ID01).
- Readback: 84 / 68 / 18, Lager 3006/3007 vorhanden, 2006/2007 weg, Lasten unverändert (LF10 Σ 30,0 kN).

### Schritt 8 — Modell B rechnen und exportieren
- Wie Schritt 6, `--run-id RUN-RF6-B01`. LK220 = 1,35·LF10 + 1,50·LF43 ergänzen, falls E4 freigegeben.

### Schritt 9 — Vergleich RF5-Bestand ↔ RF6-Neu (einzige Auswertung)
- Delta-Matrix nach Vorlage Blatt 6 (`Befunde/26_10_06_ID-03_DELTA-MATRIX_BLATT6_VORLAGE_Rev0.md`): je Seil N_RF5, N_RF6(A), N_RF6(B), ΔN; je Lager P_x/P_y/P_z; u an Kernknoten; η = N_Ed / F_Rd mit F_Rd = 46,1/(1,5·1,1) = 27,9 kN (DIN EN 1993-1-11); neue Seillängen S19/S22 aus der Nulllage von Modell B (Beschlagmaß F7 separat).
- Plausibilität: ΣV = 0, ΣM = 0 je Modell; Vorzeichen Z nach unten positiv; Einheiten kN/m.

### Schritt 10 — Dokumentation Ergänzung 4
- Blätter analog Bestandsstatik: Grundlagen (Quellen + Hashes), System (Modell B), Lasten (1:1 Bestand), Ergebnisse (Delta-Matrix), Nachweise (η, Anker 3006/3007 → Ankerbemessung), Anhang (CSV, Readback, API_Log, Run-Register).
- Jeder Lauf bekommt eine Zeile im Run-Register (Quellenlog RF6 §3): Modell-Hash, Skript-Hash, Zeit, Ergebnis-Hashes.

## 4 Fail-closed-Regeln (gelten in jedem Schritt)

- Keine Zahl ohne Fundstelle (CSV-Zeile oder PDF-Seite). FOUND ≠ VERIFIED.
- Keine Änderung außerhalb 3006/3007/1006/1007/2006/2007 (+ Lager dazu). Alles andere ist Abbruchgrund.
- Keine Formfindung, keine Vorspannung als Eingabe (Sv = N(LK100) ist Ergebnis), keine „Bereinigung" von Lasten.
- Original-Dateien nie überschreiben; nur Arbeitskopien; SHA-256 vor/nach.
- Fremdskripte aus Chats nur über die Sperrliste (`Befunde/…SPERRLISTE…`); nichts davon ausführen.
- Entscheidungen E1–E9/F7 trifft ID01 im eigenen Wortlaut in `Skripte/gates.json`.

## 5 Kontrollzahlen (Gesamtmodell)

| Größe | Modell A | Modell B |
|---|---|---|
| Knoten / Stäbe | 86 / 88 | 84 / 86 |
| Seile / Maste | 68 / 20 | 68 / 18 |
| Lagerobjekte | 27 | 25 (+ 3006/3007 im Lager-Objekt von Kn 105 oder eigene) |
| LF / LK | 19 / 21 (+ LK220) | gleich |
| LF10 Σ Leuchten | 30,0 kN | 30,0 kN |
| Kalibrierziel LK100 | u_Kn17 2,085 m · N_S54 17,47 kN | – |
| F_Rd Seil PE 5 | 27,9 kN | 27,9 kN |

| Teilmodell | A-T (Bestand) | B-T (Ergänzung 4) |
|---|---|---|
| Knoten / Stäbe | 16 / 15 | 14 / 13 |
| Seile / Maste | 12 / 3 (1006, 1007, 1021) | 12 / 1 (1021) |
| Lagerobjekte | 6 (105, 106, 113, 114, 2021, 2006, 2007) + Rand Kn 8 | 4 + Lager 3006/3007 + Rand Kn 8 |
| LF10 Σ Leuchten | 5 × 1,000 kN (Kn 8, 9, 10, 29, 30) | gleich |

## 6 Teilmodell T — Modellgrenze, Randbedingungen, Listen (heute zu rechnen)

Herleitung: Ring-Analyse der Netztopologie ab 3006/3007 (`tools/26_10_07_ID-03_make_teilmodell.py`). Alle Ränder sind echte Lager außer **einem** Schnittknoten 8, an dem das Netz über S16 (8–6) und S23 (8–11) weiterläuft. Annahme ID-03, da die Skizze im Upload nicht auffindbar war; Bestätigung durch ID01 im Begleitschreiben vermerken.

| Rolle | Knoten | Stäbe |
|---|---|---|
| Kern (Haltepunkte, ändern sich) | 3006, 3007 | S19 (3006–9), S22 (10–3007) |
| Netzknoten (bleiben, tragen Leuchten) | 9, 10, 29, 30, 330 | S18 (330–9), S20 (10–9), S21 (10–106), S61 (10–29), S62 (29–30), S81 (105–330), S60 (29–113), S64 (30–114), S17 (330–8), S63 (30–3021) |
| Echte Lager (unverändert) | 105, 106, 113, 114 (Wandanker, Obj 2/29/30), 2021 (Mastfuß, Obj 8) | Mast 1021 (3021–2021, QS 12→4) |
| Nur Modell A-T | 2006, 2007 (Mastfüße, Obj 36/37) | 1006, 1007 (QS 5→4) |
| **Schnittknoten (Modellgrenze)** | **8** | weggelassen: S16, S23 (außerhalb) |

Randbedingung am Schnittknoten 8 (Tabelle `T10_randbedingung_schnittknoten.csv`):
- **R1 starr (Standard heute):** u_x = u_y = u_z = 0, Verdrehungen frei. Konservativ für die Grenznähe (S17/S18 ziehen gegen eine feste Grenze); Leuchtenlast an Kn 8 geht direkt ins Lager.
- **R2 verschieblich:** Knoten-Zwangsverformung u_x/u_y/u_z aus dem RF5-Gesamtmodell je LK (RF6-Tabelle „Knoten-Zwangsverformungen“); dann reproduziert das Teilmodell den Bestand exakt an der Grenze. Werte aus `10_resultate_rf5_knoten.csv` (Kn 8), sobald vorhanden.

Gate T-G1 (Pflicht vor Modell B-T): Modell A-T mit R1 rechnen, N in S17, S18, S81, S60, S64, S63, S19, S22 (LK100) gegen RF5-Gesamtmodell vergleichen. Abweichung ≤ Toleranz E8 → Grenze ausreichend. Sonst Grenze um Ring 4 erweitern (Knoten 6, 11 + S16, S23; neue Schnittknoten 7, 12, 3003/3008) und T-G1 wiederholen.

Dateien: `Daten/input/EINGABEDATEN_RF6_TEILMODELL_v0.1/` (T01–T11, MANIFEST_TEILMODELL.json). Lasten, Materialien, QS, LF/LK sind 1:1 aus dem Gesamtmodell gefiltert, nichts geändert.

## 7 Maschinenprüfbare Änderungsgrenze (Begriff)

Bedeutung: Die erlaubten Änderungen stehen als Liste von Objekt-IDs in `T11_change_allowlist.csv` (8 Zeilen: 3006, 3007 Koordinaten; 1006, 1007, 2006, 2007 löschen; Lager 3006/3007 neu; Rand Kn 8). Ein Skript diffst Modell A gegen Modell B (CSV ↔ CSV und RF6-Readback ↔ CSV) und bricht ab, sobald eine Differenz außerhalb dieser Liste auftritt. „Maschinenprüfbar“ heißt: nicht der Mensch liest den Unterschied aus dem Plan ab, sondern der Diff beweist, dass genau diese und keine andere Änderung im Modell ist. Das ist derselbe Mechanismus wie Gate G3/G6 der Migrationsdateien vom 14:25.

## 8 Abgleich mit den Migrationsdateien `…1425_ID-03_RF5-CSV-RFEM6-SEILSTATIK_SKILL/WEGWEISER.md`

| Punkt | Migrationsdatei (14:25) | Dieser Skill | Ergebnis |
|---|---|---|---|
| Ziel, Scope, Zwei-Änderungen-Regel | G0–G10, Allowlist, Stop-Conditions | §0, §3, §7 | konsistent; G-Nummern werden als Querverweis geführt (G0 = Schritt 1, G1/G2 = Schritt 2, G3 = Schritt 3 + T11, G4 = Schritt 4, G5/G6 = Schritt 5 + Readback, G7/G8 = Schritte 6/8, G9 = Schritt 9, G10 = Schritt 10) |
| Konkrete Objekte, Koordinaten, Transformation, IDs | fehlen | vorhanden (T1, 3006/3007, 1006/1007, Lager) | Lücke der Migrationsdatei geschlossen |
| CSV-Vertrag | SI (N, m), Komma, abstrakte Spalten | kN/cm, Semikolon, vorhandene Dateien | **ein** Vertrag festgelegt: WEGWEISER §5 (bestehende Tabellen + Ergebnis-/Audit-Tabellen); Umrechnung in SI erfolgt im Generator beim API-Schreiben |
| Ergebnis-, Audit- und Vergleichstabellen | benannt, Spalten definiert | fehlten | übernommen in WEGWEISER §5 (10–12, `rf6_writeback_audit`, `rf5_rf6_comparison`) |
| Teilmodell | nicht vorgesehen | §6 | neu (Entscheidung Nachmittag) |
| Toleranzen, Kalibrierziele | „declared“ ohne Werte | u_Kn17 2,085 m, N_S54 17,47 kN, E8-Vorschlag | vorhanden |
| „Never infer missing data“ | ja | Fail-closed §4 | konsistent |
| Sprache | Englisch | Deutsch | Dieser Skill ist die verbindliche Fassung; die 14:25-Dateien bleiben als Vorlage im Ordner _SEILSTATIK_BOEBLINGEN |
