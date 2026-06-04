#!/usr/bin/env python3
"""Extract photos for June 7 edition from specific Gmail message IDs."""

import os
import sys
import json
import base64
import email
import requests
from pathlib import Path

GMAIL_MCP_CREDS = os.path.expanduser("~/.gmail-mcp/credentials.json")
GMAIL_MCP_KEYS = os.path.expanduser("~/.gmail-mcp/gcp-oauth.keys.json")

def get_access_token():
    with open(GMAIL_MCP_CREDS) as f:
        creds = json.load(f)
    with open(GMAIL_MCP_KEYS) as f:
        keys = json.load(f)
    web = keys.get("web") or keys.get("installed") or {}
    resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": web["client_id"],
            "client_secret": web["client_secret"],
            "refresh_token": creds["refresh_token"],
            "grant_type": "refresh_token",
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]

def extract_attachments(message_id, token):
    url = f"https://www.googleapis.com/gmail/v1/users/me/messages/{message_id}?format=raw"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, timeout=60)
    resp.raise_for_status()
    raw = base64.urlsafe_b64decode(resp.json()["raw"] + "==")
    msg = email.message_from_bytes(raw)
    attachments = []
    for part in msg.walk():
        cd = part.get("Content-Disposition", "")
        if "attachment" in cd or part.get_filename():
            filename = part.get_filename()
            if filename:
                payload = part.get_payload(decode=True)
                if payload:
                    attachments.append((filename, payload))
    return attachments

# message_id -> output_dir (relative to /home/john/article)
EXTRACTIONS = {
    # Court Tennis: 3 photos
    "19e8cc7d1d17aebc": "editions/2026-06-07/court-tennis",
    # Scott Holleran: docx + 2 photos
    "19e82b9ae37f18c3": "editions/2026-06-07/scott-holleran",
    # Scott Holleran cover photo (separate email)
    "19e923f0a7217f77": "editions/2026-06-07/scott-holleran",
    # Jill Lowe article PDF
    "19e8d3e3aaca2dc1": "editions/2026-06-07/jill-lowe-magic",
    # Jill Lowe photos (14 images)
    "19e8d407de6fe087": "editions/2026-06-07/jill-lowe-magic",
    # Heritage ad new PNG
    "19e8d42e4ca1bee7": "ads",
    # Ryan Licht Sang cover
    "19e92222c5e01352": "editions/2026-06-07/ryan-licht-sang",
    # Minds Matter cover
    "19e92219948b1797": "editions/2026-06-07/minds-matter",
}

base = Path("/home/john/article")

def main():
    print("Getting access token...")
    token = get_access_token()
    print("Token obtained.")

    for msg_id, rel_dir in EXTRACTIONS.items():
        out_dir = base / rel_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"\nExtracting from {msg_id} -> {rel_dir}")
        try:
            attachments = extract_attachments(msg_id, token)
            for filename, data in attachments:
                dest = out_dir / filename
                dest.write_bytes(data)
                print(f"  Saved: {filename} ({len(data)} bytes)")
            if not attachments:
                print("  No attachments found.")
        except Exception as e:
            print(f"  ERROR: {e}")

if __name__ == "__main__":
    main()
