# Routinen — Anlage über die claude.ai-Routinen-UI

Aus einer Claude-Code-Session heraus können in dieser Organisation keine Connector-Rechte
(Google_Drive, Claude_Code_Remote) an Routinen weitergegeben werden. Routinen mit
Drive-Zugriff müssen daher in der claude.ai-Routinen-UI angelegt werden:

1. claude.ai → Code → Routinen → „Neue Routine“
2. Name, Zeitplan (UTC) und Prompt aus der jeweiligen Datei übernehmen
3. Connectoren aktivieren: siehe Tabelle
4. Neue Session je Lauf: ja · Benachrichtigung: Push

| Datei | Name | Cron (UTC) | Connectoren |
|---|---|---|---|
| W1_drive_indexer.md | W1 DRIVE-INDEXER | `0 4 * * *` | Google_Drive |
| W4_dev_log.md | W4 DEV-LOG | `0 20 * * *` | Google_Drive, Claude_Code_Remote, GitHub |
| W2_inbox_sorter.md | W2 INBOX-SORTER | `30 4 * * *` | Google_Drive (erst nach Nomenklatur-Freigabe) |

Der Prompt-Block beginnt in jeder Datei nach der Zeile `---PROMPT---` und wird 1:1 eingefügt.
