# 26_09_11 — Bestandsaufnahme Google-Drive-Workflows + Systemcheck

Stand: 2026-09-11 20:25 UTC · Quelle: Drive-Connector (list_recent_files, get_file_metadata), Claude_Code_Remote (get_session, list_triggers), git ls-remote · Modus: READ_ONLY

## TL;DR
- Heute 08:53–19:29 UTC: ~70 Dateiänderungen in 8 Ordnern, davon ~80 % manuelle Ablage-, Umbenennungs- und Indexarbeit.
- 5 wiederkehrende manuelle Muster erkannt (M1–M5). 4 davon sind vollständig autonomisierbar (W1–W5 unten), nur Lösch-/Kanonik-/Freigabe-Entscheidungen bleiben manuell.
- 3 Systemblocker: (1) Repo ohne Default-Branch, (2) Routine „Office Management Agent" hängt seit 12:35 UTC in einer Freigabe, (3) Voice-Modus in Claude Code nicht vorhanden.

## 1. Drive-Aktivität 11.09.2026 (Fakten)

| Zeit (UTC) | Ordner | Vorgang | Art |
|---|---|---|---|
| 08:53–08:58 | BUILDING-MATERIALS+CLIMATE(UNEP+GlobalABC) → `links` | Ordner angelegt, UNEP-.url abgelegt | manuell |
| 10:39 | PeterKneidinger JakobLederer | Ordner + Kurzbericht.md (29 kB, bis 17:45 editiert) | manuell/LLM |
| 11:51–11:56 | AUFBAUTEN-SYSTEMMATRIX | Ordner + bericht+prot.pdf | manuell |
| 16:23–17:54 | AI Studio (Prompts) | 3 Prompt-Kopien (Vibe-Coder, EC2-Quellen, Quicksilver Live) | manuell |
| 17:43–17:59 | `_developement` | 4 TXT-Exporte derselben Prompts + ChatGPT-Export als .md (1,09 MB) UND .txt (0,44 MB) | manuell, doppelt |
| 17:16–17:19 | AUFBAUTEN-SYSTEMMATRIX/BILD, MathiasStandfestKnowledgeGraph | 5 JPG-Diagramme abgelegt | manuell |
| 17:24–18:38 | PeterKneidinger JakobLederer + `REST` | 12 PDF/PNG/JPG, Fotos mit Präfix 01_…05_ umbenannt, 4 Namensvarianten desselben Berichts-PDF | manuell |
| 18:01 | `remember` | 8 Fotos aus 04–05/2025 abgelegt, 5 davon byte-identisch mit BILD-Diagrammen | Duplikate |
| 18:36 | PeterKneidinger JakobLederer | KAMGARNHOF PDF 26,7 MB + 2,0 MB + JPG | manuell |
| 19:05–19:29 | Planungshilfe-mehrgeschossiger-Wohnungsbau → `LINKS` | TREE.txt/LIST.txt (Windows `tree`/`dir` auf G:), DRIVE-LINK-LISTE.txt (15 Links ohne Titel), .url verschoben, 2 geclusterte Web-Linklisten (Perplexity, Meta AI) | manuell |

## 2. Erkannte manuelle Muster (Kostentreiber)

| ID | Muster | Problem |
|---|---|---|
| M1 | Index per Windows `dir`/`tree` → TREE.txt/LIST.txt | keine Drive-IDs, keine Links, nur am Windows-PC möglich, veraltet sofort |
| M2 | Link-Sammlung als nackte `drive_copy`-URLs und einzelne `.url`-Dateien | ohne Titel/Kontext nicht durchsuchbar |
| M3 | Chat-/Prompt-Exporte händisch als .md + .txt | Doppelung, keine Metadaten (Quelle, Datum, Thema) |
| M4 | Versionierung über Dateinamen (`_+`, `_1`, `01_`, `26_09_11_`) | 4 Varianten eines PDF, 5 identische JPG in 2 Ordnern |
| M5 | Ordner-Nomenklatur `links` / `LINKS` / `REST` / `remember` | inkonsistent, keine Regel für Routinen ableitbar |

## 3. Systemcheck

| Komponente | Status | Befund / Maßnahme |
|---|---|---|
| Session | OK | claude-fable-5-1, effort high, permission auto, origin Android |
| Repo `julianzotter/julianzotter` | **BLOCKER** | origin hat nur 3 `claude/*`-Branches, kein `main`/`master`. Session-Quelle `refs/heads/main` existiert nicht → leerer Workspace. Fix: dieser Branch wird gepusht; danach auf GitHub Default-Branch setzen (Settings → Branches). |
| Routine „Office Management Agent" (12:30 UTC Mo–Fr) | **BLOCKIERT** | Lauf 12:35 steht in `REQUIRES_ACTION`: wartet auf Freigabe „Artifact publish“. Modell leer (→ Sonnet). Inhaltlich Doppelung zum „Morning Brief 05:00“. Empfehlung: löschen oder Ausgabe auf Drive-Datei statt Artifact umstellen. |
| Routines BOOKKEEPER-EVAL (17:00 tägl.), Wochenstatus (Mo 05:00), Morning Brief (Mo–Fr 05:00) | OK | letzte Läufe SUCCEEDED |
| Drive-Connector | OK, mit Grenzen | kann: suchen, lesen, erstellen, **umbenennen, verschieben**, trash, share, permissions. Kann nicht: rekursiv listen (je Ebene ein Call), Binärdateien >~10 MB zuverlässig lesen. |
| Container-Toolchain | OK | python 3.11, node 22, uv 0.8; kein rclone/gdrive-CLI; Proxy aktiv; 30 GB frei |
| Voice-Modus | **nicht verfügbar** | Claude Code (Web/Android) hat keinen Voice-Modus; Voice gibt es nur im Claude-App-Chat. Diktat über Tastatur erzeugt Transkriptionsfehler. Empfehlung: Vorgaben per Voice im Claude-App-Chat ausformulieren lassen → fertigen Prompt hier als Routine einsetzen. Alternative mit Live-Audio: Gemini Live API (Prototyp „Quicksilver AEC Live Engine“ liegt bereits in `_developement`). |

## 4. Autonomisierbare Workflows (Vorgabe definieren → läuft)

| ID | Workflow | Trigger | Vorgabe (Input) | Output | Autonomie | ersetzt |
|---|---|---|---|---|---|---|
| W1 | DRIVE-INDEXER | täglich 04:00 UTC | Liste Ordner-IDs + Tiefe | `INDEX_<Ordner>.md` in `_INDEX`: Tree mit Name, ID, Link, Größe, mtime; Diff zum Vortag | 100 % | M1, M2 |
| W2 | INBOX-SORTER | täglich 04:30 UTC | Regelwerk Muster → Zielordner, Namensschema `JJ_MM_TT_<Projekt>_<Typ>` | verschiebt/umbenennt; Duplikate (Name+Größe) → Vorschlagsliste | 90 % (Trash nur nach Freigabe) | M4, M5 |
| W3 | CHAT-EXPORT-INGEST | täglich 05:00 UTC | Quellordner `_developement`, AI-Studio-Ordner | dedupliziert .md/.txt, Frontmatter (Quelle, Datum, Thema, Tags), Eintrag in KB-Index | 90 % | M3 |
| W4 | DEV-LOG | täglich 20:00 UTC | – | `JJ_MM_TT_DEVLOG.md` in `_INDEX`: Drive-Änderungen, Routine-Läufe, Git-Commits | 100 % | manuelles Protokoll |
| W5 | LINK-CLUSTER | bei neuer URL-Liste (W1 erkennt) | Klassen (Norm, Hersteller, Paper, Tool) | titelt jede URL, klassifiziert, schreibt `.url` + Quellen-Tabelle | 80 % (Klassen prüfen) | M2 |

Nicht autonomisierbar (bleibt Freigabe): endgültiges Löschen, Kanonik-Entscheidung, Freigaben/Sharing, E-Mail-Versand.

Fertige Routine-Prompts: `routines/W1_drive_indexer.md`, `routines/W2_inbox_sorter.md`, `routines/W4_dev_log.md`. Aktivierung: „Routine W1 anlegen“ genügt.

## 5. Sofortmaßnahmen (Reihenfolge)
1. GitHub: Default-Branch setzen (sonst bleibt jede neue Session leer).
2. Routine „Office Management Agent": Freigabe erteilen oder löschen.
3. W1 + W4 aktivieren (kein Risiko, nur Lesen + eine Datei schreiben).
4. Nomenklatur festlegen (Vorschlag: `JJ_MM_TT_<PROJEKT>_<TYP>_<vNN>.<ext>`, Ordner GROSS, keine Leerzeichen) → dann W2 aktivieren.
5. Duplikate `remember` ↔ `BILD` (5 JPG) und PDF-Varianten `REST` entscheiden.

## Referenz-IDs
- `_INDEX` 1okgsbzTD2QuHZqPGYTrzmf_NESmkkaqD · `_ENGINEERING-WORKBENCH` 1-69SduAduBTdEnS9hfXyNlUmUHyGB3fU · `_developement` 1OIyJI6rljIi8zNsT-iwg47NsuguoZqTB
- Planungshilfe-mehrgeschossiger-Wohnungsbau 1Hyvc-4TD7buFS8TdyBX9Cd3QDVMSf-I7 · AUFBAUTEN-SYSTEMMATRIX 1AvRcFHlZnJZKUZOub_kKwkxksoNOiXlR · PeterKneidinger JakobLederer 1AL88iCG9AotGf2LlMy0ZbSu3MEJkXKC5

## Quellen
- Claude Code on the web (Umgebung, Routinen): https://code.claude.com/docs/en/claude-code-on-the-web
- Google Drive API Files (update = rename/move): https://developers.google.com/workspace/drive/api/reference/rest/v3/files/update
