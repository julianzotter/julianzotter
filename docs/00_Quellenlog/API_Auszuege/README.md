# API_AUSZUEGE — Ablagevertrag für RF6-API-Exporte

Jeder Export = ein Unterordner `RF6_EXPORT_<YYMMDD_HHMMSS>_<RUN-ID>/` mit genau diesen Dateien:

| Datei | Inhalt | Pflichtspalten / Felder |
|---|---|---|
| `01_Seilkraefte_N.csv` | Stabschnittgrößen (SDK `STATIC_ANALYSIS_MEMBERS_INTERNAL_FORCES`), alle gespeicherten Loadings | member_no, loading (LC/CO + Nr.), location/x, n [N], (v_y, v_z, m_t, m_y, m_z) |
| `02_Lagerkraefte_global.csv` | Lagerkräfte global XYZ (`…_NODES_SUPPORT_FORCES`) | node_no, loading, p_x, p_y, p_z [N], m_x, m_y, m_z [N·m] |
| `03_Knotenverformungen.csv` | Knotenverformungen (`…_NODES_DEFORMATIONS`) | node_no, loading, u_x, u_y, u_z [m], |u| |
| `API_Log.json` | Protokoll | run_id, model_guid, model_name, model_sha256 (falls Datei bekannt), rfem_version, sdk_version, read_at_utc, loadings_found, rows_per_file, sha256_per_file, warnings, status (ok / partial / no_results) |

Regeln:
1. Einheiten = RFEM-API-SI (m, N, N·m). Umrechnung in kN erst in der Delta-Matrix, nie in der Rohdatei.
2. Rohdateien werden nicht editiert. Auswertung in `…/Auswertung/` daneben.
3. Ohne `API_Log.json` gilt der Export als nicht existent (fail-closed).
4. Dateiname des Modells und Hash in `API_Log.json` müssen mit `00_Quellenlog/RF6` §1 übereinstimmen.
5. Alternativer Vollexport: `python 26_10_06_ID-03-RFEM6_MCP_Bridge_Extended.py --export <DIR>` (alle ResultsType-Kategorien + INPUT_MODELL.txt + MANIFEST.json). Dann MANIFEST.json statt API_Log.json referenzieren.
