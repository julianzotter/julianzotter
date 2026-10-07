# ANTWORT AUF „GEGENCHECK – STATUS DER CLAUDE-AKTIVITÄT“ (07.10.2026) — Rev0

| Feld | Wert |
|---|---|
| Prüfobjekt | eingefügter Gegencheck (Fremdassistent), 8 Abschnitte |
| Referenz | Paket `SEILSTATIK_BOEBLINGEN_ERG4_BENCHMARK-SEILSTATIK_v0.1.zip`, Sperrliste Rev0, Loop 1, Loop 2, Quellenlog RF6 §6 |

## 1 Faktenkorrekturen zum Gegencheck

| # | Gegencheck | Ist | Beleg |
|---|---|---|---|
| G1 | „ZIP hochgeladen, Drive-ID 1QZJxf7BR…, 34 KB, Ordner BENCHMARK-SEILSTATIK“ | 1QZJxf7BR8e9Jud-O0SrBJko2Pw8bq4Bt ist das **Loop-2-Dokument** (34 118 B) im Ordner 00_Quellenlog/RF6. Das ZIP (85 704 B, SHA-256 71236222…) liegt im Repo `docs/00_Quellenlog/RF6/` und wurde als Datei in der Session gesendet; Drive-Connector nimmt Binärdateien nur inline, Upload abgebrochen. Im Ordner BENCHMARK-SEILSTATIK liegt das Paket-README (16QBelwJuVZqoba3ug3K4eeBSQfWtycMA). | Quellenlog RF6 §6 |
| G2 | „Das Foto zeigt Modell 13bb“ | In dieser Session liegt kein Foto vor. Die genannten Bestandskoordinaten (105: 122,596 / 57,411 / −0,129) sind U10 = Bestand 5e, identisch in 13bb (U6a) nur für unveränderte Knoten; die Modellzuordnung ist aus Koordinaten allein nicht belegbar. | A_BESTAND/01_knoten.csv |
| G3 | „Ohne die 5 Skripte ist das Paket nicht ausführbar“ | Das Paket ist in der vorgesehenen Reihenfolge ausführbar (README Schritte 0–5: api_write_check → E9/P2 → Rechenlauf → E6a-Export → anpassen_rf6 → retour_rfem6_patch). Die fünf Fremdskripte sind kein Bestandteil dieses Pfads. | README_PAKET |
| G4 | „Sperre, weil Fall B noch nicht entschieden war“ | Nein. Die Sperre ist **technisch** und entscheidungsunabhängig (§2). Eine Fall-B-Entscheidung hebt keinen der Sperrgründe auf. | Sperrliste Rev0 |
| G5 | „boeb_bereinigung.py: Bereinigung EN 1990“ | EN 1990 enthält keine Regel „5.1.3“ zur Modellbereinigung; das Skript ändert LF10 von 30 × 1,000 kN auf 14 × 0,80 kN = Lastannahmenänderung gegenüber der geprüften Bestandsstatik. | model.db M5, Sperrliste |
| G6 | Soll-Paket mit `13bb_ausfuehrungsstatik_1.rf5`, `26.01.006_a_Daten_V02.xlsx`, `BOEBLINGEN_FALL_B_DECISION.md` | 13bb = Vorläufer U6a, nicht Bestand 5e; V02-Excel = Loop-1-Datensatz (12 von 13 QS falsch, 43 Lager, LF10 11,2 kN); DECISION.md = Loop 2 D1–D12, Freigabeblock leer. | Rev01 K1, Loop 1, Loop 2 |

## 2 Warum die fünf Skripte gesperrt bleiben (je ein harter Grund)

| Skript | Sperrgrund, unabhängig von Fall A/B |
|---|---|
| rf5_export.py | exportiert U6a (13bb) statt 5e/U10; COM-Aufrufe unbelegt; Export von U10 existiert (input_3.json) |
| boeb_bereinigung.py | LF10 → 11,2 kN (Laständerung), Zählung 105 − 19 falsch |
| boeb_rf6_generator.py | E-Modul ×100 statt Pa; SDK-Klassen/Methoden unbelegt; 14 Materialien, 43 Lager (inkl. Mastköpfe 3001–3005), Maste ohne Voute, QS-Werte falsch |
| boeb_delta_matrix.py | vergleicht Verschiebungen als Koordinaten; η gegen Z_Bk 47 statt F_Rd 27,9 kN; Schwelle 50 mm bei u ≈ 2 m |
| boeb_pfeifer_mapping.py | Quelle U9 (K15.105) nicht beschafft; Konstanten 127/156 mm, Ek 0,00035 unbelegt; Sv als Eingabe (P1) |

Jedes dieser Skripte erzeugt ein Modell oder einen Nachweis, der von der geprüften Bestandsstatik abweicht, ohne dass dies dokumentiert oder freigegeben wäre. Das ist der Gegenteil von prüffähig.

## 3 Was die Fall-B-Entscheidung tatsächlich ändert — und was dafür im Paket liegt

- Fall B im Sinne des Docx = zwei Entscheidungen: **E1** Geometriebasis T2 (G3-Siebenpunkt) statt T1 (VAR-A) und **E2** Maste 1006/1007 bleiben (geneigt). E2 widerspricht der Auftragsprämisse Ergänzung 4 (C06/C07 → Fassadenanker, neue Längen S19/S22). Beides ist eine Entscheidung von ID01 im eigenen Wortlaut, nicht durch Weiterleitung eines Fremdtexts.
- Damit der Pfad nach einer solchen Entscheidung sofort ausführbar ist, enthält das Paket jetzt zusätzlich `B_VARA/10b_patch_fallB_G3_rev0.json` (Variante B-7): 7 Knoten auf G3, keine Mastlöschung, Lager unverändert, Kontrolle 86/88/27. Der Retour-Scaffold verarbeitet ihn (Dry-Run geprüft: 8 Schritte, alle GESPERRT bis gates.json FREIGEGEBEN).
- Variante B-2 (Patch E7 Rev0, Kanon) bleibt die Vorzugslösung; beide Varianten stehen in `EINGABETABELLEN_RF6_v0.1.md` §B nebeneinander.

## 4 Konsequenz

Paket v0.1 bleibt wie geliefert, ergänzt um den B-7-Patch. Aufnahme der Fremdskripte: abgelehnt, mit Belegen in §2. Nächster Schritt lokal: README Schritt 0 (`api_write_check.py`), danach Entscheidung E1/E2 durch ID01 in `Skripte/gates.json`.
