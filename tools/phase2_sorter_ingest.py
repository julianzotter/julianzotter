"""W2 Sorter (Vorschlagsmodus) + W3 Export-Ingest, deterministisch aus TSV-Listings."""
import re, csv, collections
from typing import Dict, List, Tuple
S = "/tmp/claude-0/-home-user-julianzotter/31b66243-1d08-58ea-9ae9-8fda0b9ab499/scratchpad"
TODAY = "26_09_11"
def link(i: str) -> str: return f"[Link](https://drive.google.com/file/d/{i}/view)"
def mb(b: int) -> str: return f"{b/1e6:.2f}"

# ---------- W2 ----------
rows = [r for r in csv.reader(open(f"{S}/files.tsv", encoding="utf-8"), delimiter="\t")]
PHOTO = re.compile(r"^\d{4}-\d{2}-\d{2} |KNEIDINGER.*\.jpg$|ZOTTER.*\.jpg$|Zotter.*\.jpg$|_1\.jpg$", re.I)
def typ(name: str, folder: str) -> Tuple[str, str]:
    n = name.lower()
    if n.endswith(".url") or "link" in n or "master-liste" in n or "weblink" in n: return "LINKLISTE", "LINKS"
    if n.startswith("chatgpt-") or "perplexity" in n or "meta-ai" in n: return "EXPORT", "_developement/EXPORTS"
    if "protokoll" in n or "+prot" in n: return "PROTOKOLL", ""
    if n.endswith((".jpg", ".jpeg", ".png")):
        if "diagramm" in n or "formel" in n or "gwp" in n or "vgl" in n or "efficiency" in n or "exposé" in n or "experten" in n: return "DIAGRAMM", "BILD"
        return "FOTO", ""
    if n.endswith((".pdf", ".md", ".docx")): return "BERICHT", ""
    return "UNKLAR", ""
def slug(name: str) -> str:
    base = re.sub(r"\.[A-Za-z0-9]+$", "", name)
    base = re.sub(r"^\d{2}_\d{2}_\d{2}_", "", base)
    base = re.sub(r"^\d{2}_", "", base)
    base = re.sub(r"[ .]+", "-", base.strip())
    base = re.sub(r"[^A-Za-z0-9ÄÖÜäöüß_+\-]", "", base)
    base = re.sub(r"-{2,}", "-", base).strip("-_")
    return base.upper()[:60]
ext = lambda n: n.rsplit(".", 1)[-1].lower() if "." in n else ""
by_size = collections.defaultdict(list)
for folder, pid, name, fid, size, created in rows: by_size[int(size)].append((folder, name, fid))
actions, proposals, dups = [], [], []
for folder, pid, name, fid, size, created in rows:
    t, target = typ(name, folder)
    proj = folder.split("/")[0]
    new = f"{TODAY}_{proj}_{t}_{slug(name)}_v01.{ext(name)}"
    date_ok = re.match(r"^\d{2}_\d{2}_\d{2}_", name) is not None
    peers = [p for p in by_size[int(size)] if p[2] != fid]
    if peers:
        dups.append((folder, name, fid, size, "; ".join(f"{p[0]}/{p[1]}" for p in peers)))
    row = (folder, name, new, target or "(bleibt)", t, fid)
    if t in ("UNKLAR",) or (t == "FOTO" and folder.endswith("remember")): proposals.append(row)
    elif date_ok and new == name: continue
    else: actions.append(row)
out = [f"# {TODAY} — SORTER_LOG (W2, MODUS: VORSCHLAG, keine Änderung ausgeführt)", "",
       f"Stand: 2026-09-11 21:40 UTC · Regelwerk: routines/W2_inbox_sorter.md · Nomenklatur `JJ_MM_TT_<PROJEKT>_<TYP>_<vNN>.<ext>` (bestätigt)",
       f"Geprüft: {len(rows)} Dateien in 7 Ordnern · Vorschläge Umbenennen/Verschieben: {len(actions)} · Rückfrage: {len(proposals)} · Duplikat-Kandidaten: {len(dups)}", "",
       "## A) VORGESCHLAGENE AKTIONEN (würden im Modus AUSFÜHREN per update_file umgesetzt)", "",
       "| Ordner | alter Name | neuer Name | Ziel-Unterordner | TYP | ID |", "|---|---|---|---|---|---|"]
out += [f"| {a[0]} | {a[1]} | `{a[2]}` | {a[3]} | {a[4]} | {a[5]} |" for a in actions]
out += ["", "## B) RÜCKFRAGE (Regel greift nicht eindeutig)", "", "| Ordner | Name | Vorschlag | Grund | ID |", "|---|---|---|---|---|"]
out += [f"| {p[0]} | {p[1]} | `{p[2]}` | Privatfoto 2025 in Projektordner, Zweck unklar | {p[5]} |" for p in proposals]
out += ["", "## C) DUPLIKAT-KANDIDATEN (gleiche Bytegröße, nur Meldung, kein Trash)", "", "| Ordner | Name | Größe | identisch mit | ID |", "|---|---|---|---|---|"]
out += [f"| {d[0]} | {d[1]} | {d[3]} | {d[4]} | {d[2]} |" for d in dups]
out += ["", "## D) VARIANTEN-GRUPPEN (Versionierung über Dateinamen, Entscheidung nötig)", "",
        "| Gruppe | Dateien | Empfehlung |", "|---|---|---|",
        "| Bericht KNEIDINGER-LEDERER-ZOTTER (PDF) | `…ZOTTER.pdf` 10,84 MB · `…ZOTTER_+.pdf` 10,84 MB (Δ 356 B) · `26_09_11_…ZOTTER.pdf` 2,83 MB · `KNEIDINGER. LEDERER. ZOTTER..pdf` 0,30 MB · `Kurzvorstellung_…pdf` 2,40 MB | eine Datei als v03 (final) markieren, Rest nach `REST/ARCHIV` |",
        "| Kurzbericht (MD) | `26_09_11_Kneidinger_Lederer_Kurzbericht.md` 29 kB (17:45) · `…_Kurzbericht_1.md` 22 kB (11:49) | jüngere = v02, ältere = v01 |",
        "| ChatGPT Systemaufbau-Matrix | `.md` 1,09 MB · `.txt` 0,44 MB | `.md` behalten (vollständiger), `.txt` ist Teilexport |",
        "| High-Tech Vienna Circular Construction Stack | `_8p.pdf` 4,2 MB · `_VA.pdf` 15,1 MB · `05_…_8p_1.jpg` 3,2 MB | 8p = Kurzfassung, VA = Vortrag, JPG = Vorschau: drei TYPen, keine Duplikate |",
        "", "## E) ORDNER-NOMENKLATUR", "",
        "| Ist | Soll | Grund |", "|---|---|---|",
        "| `PeterKneidinger JakobLederer` | `KNEIDINGER-LEDERER` | Leerzeichen, Groß/Klein |",
        "| `REST` | `ARCHIV` oder auflösen | Name ohne Bedeutung, enthält Hauptberichte |",
        "| `remember` | `FOTO-2025` oder nach `_PRIVAT` | Kleinbuchstaben, Zweck unklar |",
        "| `links` (UNEP) und `LINKS` (Planungshilfe) | einheitlich `LINKS` | zwei Schreibweisen |",
        "", "## FREIGABE", "",
        "Zum Ausführen von Abschnitt A: Zeile `FREIGABE A: ja` in diese Datei schreiben oder im Chat „W2 ausführen“ sagen. Abschnitte B–E sind Entscheidungen, keine Automatik."]
open(f"{S}/26_09_11_SORTER_LOG.md", "w", encoding="utf-8").write("\n".join(out))

# ---------- W3 ----------
ex = [r for r in csv.reader(open(f"{S}/exports.tsv", encoding="utf-8"), delimiter="\t")]
def source(n: str, folder: str) -> str:
    l = n.lower()
    if "deepseek" in l: return "DeepSeek"
    if "chatgpt" in l: return "ChatGPT"
    if "perplexity" in l: return "Perplexity"
    if "meta-ai" in l or "meta ai" in l: return "Meta AI"
    if folder == "Google AI Studio" or "gemini" in l or "live mode" in l: return "Gemini / AI Studio"
    return "manuell"
def topic(n: str) -> str:
    t = re.sub(r"^\d{2}_\d{2}_\d{2}_", "", n); t = re.sub(r"^(DeepSeek|ChatGPT)[-_]", "", t, flags=re.I)
    t = re.sub(r"\.[A-Za-z0-9]+$", "", t); return t.replace("°°", "").strip(" #-")
def kind(n: str) -> str:
    l = n.lower()
    if "linkliste" in l or "weblink" in l or "list-of" in l or "quellen" in l: return "LINKLISTE"
    if "prompt" in l or "vibe-coder" in l or "framework" in l: return "PROMPT"
    if l.endswith(".zip"): return "ARCHIV"
    return "CHAT-EXPORT"
groups = collections.defaultdict(list)
for folder, name, fid, size, created in ex:
    key = re.sub(r"\.[A-Za-z0-9]+$", "", name).replace("°°", "").replace("_", "-").lower()
    key = re.sub(r"^\d{2}-\d{2}-\d{2}-", "", key); key = re.sub(r"[^a-z0-9+]", "", key)
    groups[key].append((folder, name, fid, size))
multi = {k: v for k, v in groups.items() if len(v) > 1}
srcs = collections.Counter(source(n, f) for f, n, *_ in ex)
kinds = collections.Counter(kind(n) for _, n, *_ in ex)
o = [f"# {TODAY} — KB_EXPORTS_INDEX (W3 Chat-Export-Ingest, erster Lauf)", "",
     f"Stand: 2026-09-11 21:40 UTC · Quellordner: `_developement`, `Google AI Studio`, `AUFBAUTEN-SYSTEMMATRIX`, `KNEIDINGER-LEDERER/REST` · {len(ex)} Dateien, {sum(int(r[3]) for r in ex)/1e6:.0f} MB",
     "", "## TL;DR", "",
     f"- Quellen: " + ", ".join(f"{k} {v}" for k, v in srcs.most_common()),
     f"- Typen: " + ", ".join(f"{k} {v}" for k, v in kinds.most_common()),
     f"- Format-Duplikate (gleicher Inhalt als .md/.txt/.pdf): {len(multi)} Gruppen, {sum(len(v)-1 for v in multi.values())} redundante Dateien",
     "- 3 AI-Studio-Prompts liegen zusätzlich als .txt in `_developement` (Quicksilver, EC2-Quellen, Vibe-Coder): Prompt-Datei ist die Quelle, .txt ist Kopie",
     "- Kein Export trägt Frontmatter (Quelle, Datum, Thema, Tags). Vorschlag: W3 im Modus AUSFÜHREN schreibt je Export eine Begleitdatei `<name>.meta.md`, Original bleibt unverändert",
     "", "## FORMAT-DUPLIKATE", "", "| Gruppe | Dateien (Ordner · Größe) | Behalten |", "|---|---|---|"]
for k, v in sorted(multi.items()):
    files = " · ".join(f"`{n}` ({f}, {mb(int(s))} MB)" for f, n, i, s in v)
    keep = max(v, key=lambda x: (x[1].endswith(".md"), int(x[3])))[1]
    o.append(f"| {topic(v[0][1])[:40]} | {files} | `{keep}` |")
o += ["", "## INDEX (alle Exporte, sortiert nach Quelle, Datum)", "", "| Quelle | Datum | Typ | Thema | Format | MB | Ordner | Link | ID |", "|---|---|---|---|---|---|---|---|---|"]
for folder, name, fid, size, created in sorted(ex, key=lambda r: (source(r[1], r[0]), r[4], r[1])):
    o.append(f"| {source(name, folder)} | {created} | {kind(name)} | {topic(name)[:70]} | {ext(name) or 'prompt'} | {mb(int(size))} | {folder} | {link(fid)} | {fid} |")
o += ["", "## THEMEN-CLUSTER (aus Dateinamen, zur Prüfung)", "",
      "| Cluster | Anzahl | Beispiele |", "|---|---|---|"]
clusters = {"LLM-Framework / Orchestrierung / Agenten": r"llm|agent|orchestr|framework|mcp|modellwahl|prompt-loop|chatmanagement|kilo|vibe|quicksilver|live",
            "Wissensmanagement / Drive / Index / KB": r"wiki|index|kb-|datenmanag|dateimanag|treelist|scratch|upload|inventar|workspace|drive|register|ssot|chat-split|exporter|semanti",
            "Bautechnik / EC2 / Aufbauten / Statik": r"ec2|eurocode|aufbauten|außenwand|aussenwand|träger|seilstatik|bautechnik|baustoff|lowtech|stroh|lehm|hochloch",
            "AEC-Dashboard / Data Mining": r"aec|dashboard|data mining|mining",
            "IT-Betrieb / Keys / Windows / Copilot": r"api-key|api key|passwort|windows|copilot|python einstell|github cli|gemini desktop|powershell|onedrive"}
for c, rx in clusters.items():
    hits = [n for _, n, *_ in ex if re.search(rx, n, re.I)]
    o.append(f"| {c} | {len(hits)} | {', '.join(topic(h)[:30] for h in hits[:3])} |")
o += ["", "## NÄCHSTER SCHRITT", "", "W3 im Modus AUSFÜHREN: je Export `<name>.meta.md` mit Frontmatter (source, date, topic, cluster, tags, size, drive_id) in denselben Ordner schreiben; Format-Duplikate nur melden. Freigabe: „W3 ausführen“."]
open(f"{S}/26_09_11_KB_EXPORTS_INDEX.md", "w", encoding="utf-8").write("\n".join(o))
print(f"W2: {len(rows)} geprüft, {len(actions)} Aktionen, {len(proposals)} Rückfragen, {len(dups)} Dup-Meldungen")
print(f"W3: {len(ex)} Exporte, {len(multi)} Format-Dup-Gruppen")
