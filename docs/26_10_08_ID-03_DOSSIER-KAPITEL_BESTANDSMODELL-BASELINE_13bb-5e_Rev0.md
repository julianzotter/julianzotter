# Dossier-Kapitel: Bestandsmodell-Erfassung und Baseline-Entscheidung 13bb versus 5e — Rev0

| Feld | Wert |
|---|---|
| Stand | 08.10.2026 · ID-03 · Grundlage: Befund der lokalen COM-Session (RFEM 5.29.01, nur lesend) vom 08.10.2026, Quellenlog RF6 §6d |
| Status | vorläufig, nicht freigegeben; eigene Prüfung der RF5-Dateien, vollständigen Hashes und Berichtsseiten durch ID-03 nicht erfolgt |
| Verwendung | Kapitel für das technische Dossier (`26_10_08_TECHNISCHES DOSSIER RFEM-MCP-API-CSV-SKILL`), Ergänzung 4 Blatt „Grundlagen" |

## 1 Verbindliche Zuordnung

| Gegenstand | Zuordnung | Behandlung |
|---|---|---|
| Historische Bestandsfassung | `13bb_ausführungsstatik_1.rf5`, Fassung 2015, 54 054 912 B, SHA-256 73242E13… (vollständiger Wert aus dem lokalen Manifest zu übernehmen) | unveränderbare Referenz für Modellidentität; vereinbarte Ausgangsfassung (P. Kneidinger) |
| Veränderte 13bb-Datei | Stand 06.10.2026, 54 075 392 B, C88F7792… | vom Bestandsquellenpfad ausgeschlossen |
| Berichtskonforme Lastgrundlage | `…150328_5e.rf5`, BD77CF83… | Quelle für Lasten, Kombinationen (21 LK, 2 RK) und gespeicherte Vergleichsergebnisse 2015 |
| **Abgeleitete Arbeitsbaseline** (= D2a) | Geometrie/System 13bb ≡ 5e; Last- und Kombinationsstand aus 5e | eigener Modellstand mit Herkunftsnachweis; nicht als unveränderter Bestand bezeichnen. Datensatz: `EINGABEDATEN_RF6_v0.1` (5e-Export U10), geprüft gegen den Befund |
| Variante A (23.09.) | auf 5e aufgebaut | bestehende Arbeitsgrundlage; Dateiidentität im Register ergänzen |
| Sicherungskopien `RFEM5_2015 - Kopie\` | identisch | nicht als Arbeitsmodelle öffnen |

Kurzhashes dienen der Lesbarkeit; in `MANIFEST`/Quellenlog gehören die vollständigen SHA-256-Werte (offen: O2, Kopie der lokalen Vergleichsdateien).

## 2 Drei getrennte Änderungsarten (Auditspur)

1. **Historischer Modellvergleich** 13bb ↔ 5e: dokumentieren, nichts verändern (liegt vor: `09_VERGLEICH_13bb_vs_5e_20261008\`).
2. **Baseline-Konsolidierung**: 5e-Lasten/LK/RK ausdrücklich der Arbeitsbaseline zuordnen; Übertragungsplan aus den Vergleichsdaten, kein freier Entwurf. Einzeln zu erfassen: Kabel-Stablast LF10 (1,48 N/m), Leuchten-Wind LF30–33 inkl. Korrektur LF33, Raueis LF40/41, Schnee LF43, Wind auf vereiste Leuchte LF50–53 und LF60–63, CO214–218, RK1-Änderung und RK2 (EQU). In v0.1 bereits enthalten (Nachweis: Konsistenzprüfung 08.10., Quellenlog §6d).
3. **Neue Projektänderung** (Ergänzung 4): C06/C07 → Fassadenanker 3006/3007 als eigener Patch (`T11_change_allowlist.csv`), erst nach 1 und 2.

## 3 Objektidentität statt Nummerngleichheit

- RF5-Objektnummer und kanonische Objektidentität getrennt führen; Mapping 13bb ↔ 5e speichern (Knoten 16↔17, Linien 44, 46–49).
- v0.1 und Teilmodell folgen der 5e-Nummerierung. Das Teilmodell (A-T 16 / B-T 14 Knoten) enthält 16/17 nicht.
- Physikalische Gleichheit nur über Koordinaten- und Konnektivitätsvergleich, nicht über Nummern.

## 4 Gespeicherte Ergebnisse 2015: Klassifizierung

- Historische RF5-Ergebnisreferenzen (5e), keine Ergebnisse eines aktuellen Laufs. Verwendung lastfall-, kombinations- und objektbezogen (Vertrag Tabellen 10–12).
- Globale Maxima liegen nahe beieinander (5e 17,50 kN CO207 vs. 13bb 17,42 kN CO203), lokal weichen 13bb-Werte stark ab (Anker 111, Stab 56, LF43 = 0). Ein Vergleich nur der maximalen Seilkraft reicht für die Abnahme nicht.
- **Prüfstatus P-01:** Einzelwert 94 kN bei LF62/Stab 53 (13bb) gegenüber 3,8 kN (5e). Weder entfernen noch als RF6-Referenz übernehmen; Ursache klären (Lastobjekt LF62 in 13bb), im Vergleich getrennt ausweisen.

## 5 Arbeitsstand nach Befund

| Punkt | Status | Behandlung |
|---|---|---|
| V1 Fassung 13bb | erledigt | Pfad + Identität registriert (§6d) |
| V2 SHA-256 | erledigt (Kurzform) | vollständige Hashes nach O2 |
| Eingabevergleich, Ergebnisreferenzen (Phase 1.3) | erledigt lokal | JSON/XLSX/CSV nach `00_Quellenlog/RF6/` kopieren; Tabellen 10–12 ableiten |
| V3 Vereinbarungsdatum | offen | Governance-Angabe ID01 |
| D2a Bestätigung | offen | ID01 |
| Kombinationsregeln Bericht Teil I S. 24–26 | nicht gegengeprüft | vor Freigabe der LK-Übernahme prüfen (E4) |
| Auflagerbeschreibung Teil I S. 5 (Seile gelenkig an Fassadenankern und Masten) | auszuwerten | Grundlage für Lager 3006/3007 (gelenkig, Drehung analog Wandanker) |
| Ankerunterlagen Teil II S. 40–43 (Würth W-VIZ M16, IEA) | auszuwerten | Schnittstelle Ankerbemessung (P. Kneidinger), außerhalb Auftrag |
| RFEM-6-Mapping, Readback, Roundtrip | nicht nachgewiesen | Skill Schritte 4–8 |

## 6 Dossiertext (Übernahme)

Die Bestandsmodell-Erfassung vom 08.10.2026 unterscheidet zwischen der vereinbarten historischen Modellfassung 13bb aus 2015 und dem späteren Modellstand 5e nach Geometer-Aufmaß. Die Erfassung erfolgte über RFEM 5.29.01 mittels COM-Zugriff ausschließlich lesend; Modelle wurden weder verändert noch berechnet oder gespeichert. Der Befund ist vorläufig und nicht freigegeben.

Als maßgebende Bestandsdatei wird die unveränderte 13bb-Fassung (54 054 912 Byte, SHA-256 73242E13…) geführt. Eine am 06.10.2026 gespeicherte, abweichende 13bb-Datei ist nicht als Bestandsquelle zu verwenden.

Der Eingabevergleich weist Tragwerksgeometrie und Systemeigenschaften von 13bb und 5e als physikalisch gleichwertig aus; abweichende Nummerierungen einzelner Knoten und Linien werden durch ein explizites Objekt-Mapping berücksichtigt. Unterschiede bestehen bei Leuchtenlasten sowie Last- und Ergebniskombinationen; der Laststand von 5e entspricht dem Bestandsbericht vom 17.04.2015.

Für die Neuberechnung wird eine abgeleitete Arbeitsbaseline geführt: Geometrie-/Systemreferenz 13bb, Last- und Kombinationsstand 5e. Herkunft, Übertragung und Prüfentscheidungen werden getrennt protokolliert. Die Arbeitsbaseline gilt weder als unveränderte 13bb-Datei noch allein durch globale Ergebnisähnlichkeit als freigegeben. Die RF5-Ergebnisse 2015 dienen als historische Vergleichsgrößen, lastfall-, kombinations- und objektbezogen, mit gesonderter Kennzeichnung auffälliger Einzelwerte. Eine fachliche Freigabe setzt die Prüfung des übertragenen Modells, der Kombinationsregeln und der neu berechneten Ergebnisse voraus.
