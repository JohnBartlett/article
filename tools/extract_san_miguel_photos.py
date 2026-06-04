#!/usr/bin/env python3
"""Extract San Miguel photos via Gmail API using attachment IDs."""
import json, base64, requests
from pathlib import Path

GMAIL_MCP_CREDS = '/root/.gmail-mcp/credentials.json'
GMAIL_MCP_KEYS = '/root/.gmail-mcp/gcp-oauth.keys.json'

import os
GMAIL_MCP_CREDS = os.path.expanduser('~/.gmail-mcp/credentials.json')
GMAIL_MCP_KEYS = os.path.expanduser('~/.gmail-mcp/gcp-oauth.keys.json')

CACHE = '/home/john/.claude/projects/-home-john-article/cf4324b5-2431-4329-8a3f-c268951a2a8b/tool-results/mcp-claude_ai_Gmail-get_thread-1780571919192.txt'
MSG_ID = '19e79ecd652408bf'
OUT = Path('/home/john/article/editions/2026-06-07/san-miguel')
OUT.mkdir(parents=True, exist_ok=True)

def get_token():
    with open(GMAIL_MCP_CREDS) as f:
        creds = json.load(f)
    with open(GMAIL_MCP_KEYS) as f:
        keys = json.load(f)
    web = keys.get('web') or keys.get('installed') or {}
    resp = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': web['client_id'], 'client_secret': web['client_secret'],
        'refresh_token': creds['refresh_token'], 'grant_type': 'refresh_token',
    }, timeout=10)
    resp.raise_for_status()
    return resp.json()['access_token']

with open(CACHE) as f:
    data = json.load(f)

token = get_token()
msg = data['messages'][0]  # Annie's original

for att in msg['attachments']:
    fname = att['filename']
    att_id = att['id']
    url = f'https://www.googleapis.com/gmail/v1/users/me/messages/{MSG_ID}/attachments/{att_id}'
    resp = requests.get(url, headers={'Authorization': f'Bearer {token}'}, timeout=30)
    resp.raise_for_status()
    raw = resp.json()['data']
    data_bytes = base64.urlsafe_b64decode(raw + '==')
    dest = OUT / fname
    dest.write_bytes(data_bytes)
    print(f'Saved: {fname} ({len(data_bytes)} bytes)')
