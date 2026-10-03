#!/usr/bin/env python3
"""drive_inventory.py — rekursives Google-Drive-Inventar über die Drive API v3 (JSONL).

Liefert je Datei: id, name, mimeType, size, modifiedTime, md5Checksum (von Drive, ohne
Download), parents, path (aufgelöst), webViewLink, shortcut_target. Der Drive-MCP-Connector
kann nicht rekursiv listen; dieses Skript kann es.

Vorbereitung (einmalig):
  pip install google-api-python-client google-auth-oauthlib
  OAuth-Client (Desktop) in der Google Cloud Console anlegen -> credentials.json daneben legen.
Aufruf:
  python tools/drive_inventory.py --folder 13EeKXWMpoN-FrH1oPFcOsPuK_9BqfmA3 \
      --folder 1tA6hbxW3SqxyGLPY8EP1J0ESmsVuMYi5 --out INVENTORY_RAW.jsonl
Scope: drive.metadata.readonly (nur Metadaten, kein Inhalt).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import deque
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
FIELDS = ("nextPageToken, files(id, name, mimeType, size, modifiedTime, md5Checksum, "
          "parents, webViewLink, shortcutDetails)")
FOLDER = "application/vnd.google-apps.folder"
SHORTCUT = "application/vnd.google-apps.shortcut"


def get_service():
    """OAuth-Flow mit token.json-Cache; Import erst hier, damit --help ohne Libs geht."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES).run_local_server(port=0)
        Path("token.json").write_text(creds.to_json(), encoding="utf-8")
    return build("drive", "v3", credentials=creds)


def list_children(service, folder_id: str) -> list[dict]:
    """Alle direkten Kinder eines Ordners (paginiert)."""
    items: list[dict] = []
    token = None
    while True:
        resp = service.files().list(q=f"'{folder_id}' in parents and trashed = false",
                                    fields=FIELDS, pageSize=1000, pageToken=token).execute()
        items.extend(resp.get("files", []))
        token = resp.get("nextPageToken")
        if not token:
            return items


def walk(service, root_id: str, root_name: str) -> list[dict]:
    """Breitensuche ab root_id; Pfad wird mitgeführt, Shortcuts werden nicht verfolgt."""
    out: list[dict] = []
    queue = deque([(root_id, root_name)])
    while queue:
        fid, fpath = queue.popleft()
        for f in list_children(service, fid):
            rec = {k: f.get(k) for k in ("id", "name", "mimeType", "size", "modifiedTime",
                                          "md5Checksum", "parents", "webViewLink")}
            rec["path"] = f"{fpath}/{f['name']}"
            rec["root"] = root_name
            rec["status"] = "FOUND"
            if f["mimeType"] == SHORTCUT:
                rec["shortcut_target"] = f.get("shortcutDetails", {}).get("targetId")
            out.append(rec)
            if f["mimeType"] == FOLDER:
                queue.append((f["id"], rec["path"]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--folder", action="append", required=True, help="Drive-Ordner-ID (mehrfach)")
    ap.add_argument("--out", default="INVENTORY_RAW.jsonl")
    args = ap.parse_args()

    service = get_service()
    records: list[dict] = []
    for fid in args.folder:
        meta = service.files().get(fileId=fid, fields="id, name").execute()
        recs = walk(service, fid, meta["name"])
        print(f"{meta['name']} ({fid}): {len(recs)} Objekte")
        records.extend(recs)
    tmp = Path(args.out + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, args.out)
    folders = sum(1 for r in records if r["mimeType"] == FOLDER)
    print(f"out={args.out} total={len(records)} folders={folders} files={len(records) - folders}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
