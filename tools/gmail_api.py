#!/usr/bin/env python3
"""Shared Gmail API helpers used by Claude Code skills."""

import os, json, base64, email as emaillib, requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

GMAIL_MCP_CREDS = os.environ.get("GMAIL_CREDENTIALS_PATH", os.path.expanduser("~/.gmail-mcp/credentials.json"))
GMAIL_MCP_KEYS  = os.environ.get("GMAIL_OAUTH_KEYS_PATH",  os.path.expanduser("~/.gmail-mcp/gcp-oauth.keys.json"))

def get_access_token():
    with open(GMAIL_MCP_CREDS) as f: creds = json.load(f)
    with open(GMAIL_MCP_KEYS)  as f: keys  = json.load(f)
    web = keys.get("web") or keys.get("installed") or {}
    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": web["client_id"], "client_secret": web["client_secret"],
        "refresh_token": creds["refresh_token"], "grant_type": "refresh_token",
    })
    resp.raise_for_status()
    return resp.json()["access_token"]

def search_messages(token, query, max_results=20):
    r = requests.get("https://gmail.googleapis.com/gmail/v1/users/me/messages",
        headers={"Authorization": f"Bearer {token}"},
        params={"q": query, "maxResults": max_results})
    r.raise_for_status()
    return r.json().get("messages", [])

def get_metadata(token, msg_id):
    r = requests.get(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}",
        headers={"Authorization": f"Bearer {token}"},
        params={"format": "metadata", "metadataHeaders": ["From", "Subject", "Date"]})
    r.raise_for_status()
    msg = r.json()
    headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
    return {"id": msg_id, "snippet": msg.get("snippet", ""), **headers}

def get_body(token, msg_id):
    r = requests.get(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}",
        headers={"Authorization": f"Bearer {token}"}, params={"format": "raw"})
    r.raise_for_status()
    raw = base64.urlsafe_b64decode(r.json()["raw"] + "==")
    msg = emaillib.message_from_bytes(raw)
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            payload = part.get_payload(decode=True)
            if payload:
                return payload.decode(part.get_content_charset() or "utf-8", errors="replace")
    return ""

def list_attachments(token, msg_id):
    r = requests.get(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}",
        headers={"Authorization": f"Bearer {token}"}, params={"format": "full"})
    r.raise_for_status()
    results = []
    def walk(payload):
        fn = payload.get("filename", "")
        att_id = payload.get("body", {}).get("attachmentId", "")
        if fn and att_id:
            results.append({"filename": fn, "attachmentId": att_id})
        for part in payload.get("parts", []):
            walk(part)
    walk(r.json()["payload"])
    return results

def download_attachment(token, msg_id, att_id, dest_path):
    r = requests.get(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}/attachments/{att_id}",
        headers={"Authorization": f"Bearer {token}"})
    r.raise_for_status()
    data = base64.urlsafe_b64decode(r.json()["data"] + "==")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(data)

def send_email(token, to, subject, body, cc=None):
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    if cc:
        msg["Cc"] = cc
    msg.attach(MIMEText(body, "plain"))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    r = requests.post("https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        headers={"Authorization": f"Bearer {token}"}, json={"raw": raw})
    r.raise_for_status()
    return r.json()

def get_html_body(token, msg_id):
    r = requests.get(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}",
        headers={"Authorization": f"Bearer {token}"}, params={"format": "full"})
    r.raise_for_status()
    def extract_html(payload):
        if payload.get("mimeType") == "text/html":
            data = payload.get("body", {}).get("data", "")
            if data:
                return base64.urlsafe_b64decode(data + "==").decode('utf-8', errors='replace')
        for part in payload.get("parts", []):
            result = extract_html(part)
            if result:
                return result
        return ""
    return extract_html(r.json()["payload"])

def parse_formsubmit(html):
    import re
    pattern = r'<strong>([^:]+):\s*</strong>\s*<br>\s*<pre[^>]*>([^<]*)</pre>'
    matches = re.findall(pattern, html)
    return {key.strip(): value.strip() for key, value in matches}
