# PAKET SEILSTATIK BÖBLINGEN — Ergänzung 4 — BENCHMARK-SEILSTATIK v0.1 (ID-03, 07.10.2026)

Entpacken nach `G:\Meine Ablage\_INDEX_LNK\` (ergibt `…\BENCHMARK-SEILSTATIK\`). Vorhandene Dateien gleichen Namens vorher sichern. Inhalt = Stand Repo `julianzotter/julianzotter`, Branch `claude/seilstatik-doku-overview-rc0lpt`; Hashes aller Dateien in `MANIFEST_PAKET.json`.

## Inhalt

| Ordner | Inhalt | Status |
|---|---|---|
| `Daten/input/EINGABEDATEN_RF6_v0.1/` | A_BESTAND 01–09 (86 Kn, 88 St, 6 Mat, 13 QS, 27 Lager, 28 Parameter, 17 Knotenlasten, 18 Stablasten, 19 LF + 21 LK), B_VARA 10–14 (Patch E7 Rev0), `EINGABETABELLEN_RF6_v0.1.md` (alle Tabellen lesbar, Modell B Varianten B-2/B-7), MANIFEST mit SHA-256 | CANDIDATE, Inhalt belegt (U10, M5, E7) |
| `Skripte/` | `make_eingabedaten.py` (CSV-Erzeugung), `render_eingabetabellen_md.py` (Markdown), `api_write_check.py` (SDK-Introspektion, zuerst ausführen), `RF6-Ergebnis-Export.py` (E6a, 3 CSV + API_Log), `anpassen_rf6.py` (Phase 2 Delta), `retour_rfem6_patch.py` (Phase 3A, Dry-Run, Gates), `gates.json.example` | CANDIDATE; Schreibzugriffe erst nach WRITE_API_PRESENT und Freigabe ID01 |
| `00_Quellenlog/` | Ursprung, Vermesser, RF6 (inkl. LF/LK- und Knotenlasten-CSV aus model.db), API_Auszuege | Rev0/Rev1 |
| `Befunde/` | Loop 1 (Fremddaten „Fall B“), Loop 2 (Docx FERTIGSTELLUNG), Sperrliste Fremdskripte, Befund QS-Optionen (Stab 1001), Modell-Diff QS-14, Delta-Matrix Blatt 6 Vorlage | Rev0 |
| `Daten/results/`, `Logs/` | leer (werden durch E6a / Retour gefüllt) | – |

## Nicht enthalten (bewusst)

`rf5_export.py`, `tabellen_generator.py`, `boeb_rf6_generator*.py`, `boeb_full_pipeline.py`, `boeb_import.py`, `003_NACH_BP_FIX_BEREINIGT_FALL_B_V04.xlsx`, `LF10_14x08.csv`, `seilvorspannung_38.csv`, `pfeifer_41.csv`, `transformed_nodes.csv` als Eingabe. Gründe mit Beleg: `Befunde/…SPERRLISTE…`, Loop 1 §1–§6, Loop 2 D1–D12 (Kurzfassung: LF10 = 30 × 1,000 kN; 6 Materialien / 27 Lager / 21 LK; keine Formfindung, keine Vorspannung als Eingabe; Geometriebasis T1 statt G3-Siebenpunkt; C06/C07 entfallen; η gegen F_Rd 27,9 kN; Quelle 5e/U10 statt 13bb). Die RF5-Rohdaten liegen bereits als `input_3.json` (U10-Export 23.09.) vor; ein erneuter COM-Export ist nicht nötig.

## Ausführung (lokal, PowerShell), in dieser Reihenfolge

```powershell
cd "G:\Meine Ablage\_INDEX_LNK\BENCHMARK-SEILSTATIK"
# 0  SDK an Server 6.13.0001 angleichen, dann Schreib-API belegen (keine Verbindung nötig)
python -m pip install --upgrade "dlubal.api==2.13.1"
python Skripte\26_10_06_ID-03_api_write_check.py > Logs\API_WRITE_CHECK_$(Get-Date -Format yyMMdd_HHmm).json
# 1  Arbeitskopie WORKING_CALC: E9 (Schubsteifigkeit QS 10/11/12 angleichen), P2 (QS-14-Cluster löschen, Kontrolle 86/88), speichern, SHA-256 ins Quellenlog RF6 §1
# 2  Rechenlauf Th. III. O. (LK100, RK1) in RFEM 6, Results ✓
# 3  Ergebnis-Export E6a (RFEM 6 läuft, gRPC 127.0.0.1:9000, Bridge E5 im selben Ordner)
python Skripte\26_10_06_ID-03-RF6-Ergebnis-Export.py --run-id RUN-RF6-000 --out Daten\results
# 4  Delta (Phase 2) gegen Kalibrierziel U10 (u_Kn17 2,085 m, N_S54 17,47 kN)
python Skripte\26_10_06_ID-03_anpassen_rf6.py --export Daten\results\RF6_EXPORT_<stamp>_RUN-RF6-000 --model Daten\results\out_rf6 --mapping 00_Quellenlog\Vermesser\26_10_06_ID-03-AEQUIVALENZ-KNOTEN-GEOMETER-RFEM_Rev0.csv
#    out_rf6 = Modellexport E4 (26_10_06_ID-03-rf6_model_export.py); Mapping V9 von Drive 1pnPWQTNqXODcQCdJ1NmOFOcybO_eil5G nach 00_Quellenlog\Vermesser\ kopieren
# 5  Modell B: Entscheidungen E1/E2/E3/E4 in Skripte\gates.json auf FREIGEGEBEN setzen (ID01), erst Dry-Run, dann --apply
python Skripte\26_10_06_ID-03_retour_rfem6_patch.py --patch Daten\input\EINGABEDATEN_RF6_v0.1\B_VARA\10_patch_vara_rev0.json --gates Skripte\gates.json
```

Erwartungswerte sind erst nach Schritt 2 belegt; „LK100 287,41 kN“, „4 Iterationen“, „C07 52,21 mm“ aus Fremdvorlagen sind ohne Rechenlauf unbelegt und werden nicht als Soll geführt. Soll-Werte Kalibrierung: Blatt 6 Vorlage Rev0 (K1–K7).
