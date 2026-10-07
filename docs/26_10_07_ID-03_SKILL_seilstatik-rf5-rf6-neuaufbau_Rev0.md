---
name: seilstatik-rf5-rf6-neuaufbau
description: Arbeitsauftrag Seilstatik Böblingen (GZ 26_001, Ergänzung 4). Bestandsstatik (RF5 + PDF-Doku) vollständig nach CSV extrahieren, neues RFEM-6-Modell aus den CSV über die API einspielen, dabei nur die zwei geänderten Haltepunkte (C06/C07 → Fassadenanker, RFEM 3006/3007) anpassen, alles andere unverändert lassen, dann RF5-Bestandsergebnis gegen RF6-Neuberechnung vergleichen. Use when the user says "Seilstatik", "RF5 → RF6", "Neuaufbau", "Ergänzung 4", "Böblingen", "Delta RF5/RF6", or asks to run, continue or audit this pipeline.
---

# SKILL — RF5-Bestand → CSV → RFEM 6 (zwei neue Haltepunkte) → Vergleich

## 0 Entscheidung (ID01, 07.10.2026) — verbindlich

1. Aus der Bestandsstatik (RF5-Modell + PDF-Ausdruck) werden **alle** Rechenmodelldaten in CSV extrahiert: Systemgeometrie, Material, Querschnitte, Knoten, Stäbe, Auflager, Lasten, Lastfälle/-kombinationen, Resultate.
2. Das neue Modell übernimmt diese Daten 1:1. Geändert werden **nur die zwei neuen Auflagerpunkte** (C06/C07 → Fassadenanker: Knoten 3006/3007, Maste 1006/1007 mit Füßen 2006/2007 entfallen). Alles andere bleibt: Knoten, Seile, übrige Maste, Lager, Lasten, Kombinationen, Rechenparameter.
3. Einspielen nach RFEM 6 über CSV-Tabellen + API (dlubal.api, gRPC).
4. Verglichen wird **nur** Ausgabe RF5-Bestandsberechnung gegen Ausgabe RF6-Neuberechnung. **Referenz = RF5-Gesamtmodell `13bb_ausführungsstatik_1.rf5`** (mit P. Kneidinger vereinbart, ID01 07.10.2026). Das Berichtsmodell 5e dient nur als Querkontrolle.
5. Nichts anderes: keine Vorspannung als Eingabe, keine Formfindung, keine Laständerung, keine Siebenpunkt-Geometrie, keine Fremdskripte.

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
- Gate: ohne Hash und ohne Fassungsangabe kein Weiterarbeiten. Eingabedaten (Schritt 2) und Vergleichsergebnisse (Schritt 9) müssen aus derselben Datei stammen.

### Schritt 2 — Extraktion RF5 → CSV (Tabellen 01–10)
- Werkzeug: COM-Export RF5 (liefert input_3.json-Schema) → `make_eingabedaten.py` → `01_knoten … 09_lastfaelle_lastkombinationen`. **Pflicht: Export aus 13bb** → Ordner `EINGABEDATEN_RF6_v0.2_13bb/`. Die vorhandenen Tabellen v0.1 stammen aus 5e (U10) und gelten nur als Vorlage/Querkontrolle; Unterschiede 13bb ↔ 5e zeilenweise diffen und dokumentieren (gleicher Diff wie Loop 1).
- Zusätzlich `10_resultate_rf5.csv` aus dem PDF-Ausdruck: je Seil N_min/N_max (LK), Lagerkräfte je Lagerknoten, Verformungen u (LK100/101), mit Seitenangabe.
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

## 5 Kontrollzahlen

| Größe | Modell A | Modell B |
|---|---|---|
| Knoten / Stäbe | 86 / 88 | 84 / 86 |
| Seile / Maste | 68 / 20 | 68 / 18 |
| Lagerobjekte | 27 | 25 (+ 3006/3007 im Lager-Objekt von Kn 105 oder eigene) |
| LF / LK | 19 / 21 (+ LK220) | gleich |
| LF10 Σ Leuchten | 30,0 kN | 30,0 kN |
| Kalibrierziel LK100 | u_Kn17 2,085 m · N_S54 17,47 kN | – |
| F_Rd Seil PE 5 | 27,9 kN | 27,9 kN |
