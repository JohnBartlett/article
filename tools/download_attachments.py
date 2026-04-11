#!/usr/bin/env python3
"""Download all attachments from Gmail messages using gcloud credentials."""

import os
import sys
import json
import base64
import email
import requests

GMAIL_MCP_CREDS = os.path.expanduser("~/.gmail-mcp/credentials.json")
GMAIL_MCP_KEYS = os.path.expanduser("~/.gmail-mcp/gcp-oauth.keys.json")

def get_access_token():
    with open(GMAIL_MCP_CREDS) as f:
        creds = json.load(f)
    with open(GMAIL_MCP_KEYS) as f:
        keys = json.load(f)
    web = keys.get("web") or keys.get("installed") or {}
    client_id = web.get("client_id")
    client_secret = web.get("client_secret")
    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": creds["refresh_token"],
        "grant_type": "refresh_token",
    })
    resp.raise_for_status()
    return resp.json()["access_token"]

def download_attachments(message_id, output_dir, token):
    os.makedirs(output_dir, exist_ok=True)
    url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}?format=raw"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    raw = base64.urlsafe_b64decode(resp.json()["raw"])
    msg = email.message_from_bytes(raw)
    saved = []
    for part in msg.walk():
        fname = part.get_filename()
        if not fname:
            continue
        data = part.get_payload(decode=True)
        if not data:
            continue
        out_path = os.path.join(output_dir, fname)
        with open(out_path, "wb") as f:
            f.write(data)
        saved.append(fname)
        print(f"  Saved: {fname} ({len(data):,} bytes)")
    return saved

if __name__ == "__main__":
    token = get_access_token()
    print("Access token obtained.\n")

    jobs = [
        ("19d7d9a7a80d533e", "/tmp/fpm_haunted2"),
    ]
    for msg_id, out_dir in jobs:
        print(f"Downloading from message {msg_id} → {out_dir}")
        files = download_attachments(msg_id, out_dir, token)
        print(f"  {len(files)} file(s) saved.\n")
