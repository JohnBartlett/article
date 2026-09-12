# Attachment staging

This directory is populated automatically, hourly, by `.github/workflows/fetch-email-attachments.yml`
running `tools/fetch_pending_attachments.py`. It exists to solve one specific gap: the hourly
Claude cloud check-emails routine can read contributor email text via the Gmail MCP connector,
but that connector cannot download attachments in its cloud sandbox — only a local session with
real Gmail API credentials (`tools/gmail_api.py`) could do that before this existed.

## Structure

Each processed Tier-1 contributor email with image/PDF/docx attachments gets its own folder,
named by Gmail message ID, containing the attachments with their **original filenames preserved**
(never renamed — see CLAUDE.md's file-naming rules) plus a `meta.json` with sender/subject/date.

```
_attachment-staging/
  1a08bc49f7b39acb/
    meta.json
    COVER - Puget Sound.jpeg
    1 Lawn Airplane.jpeg
    ...
```

## How to consume this (cloud routine or local session)

When you identify an email that has photos/PDF/docx you need for an article:

1. Check `_attachment-staging/<message-id>/` first — it may already be fetched.
2. If present, copy (don't move via rename) the files into the correct `editions/YYYY-MM-DD/<slug>/`
   folder, preserving filenames exactly.
3. Delete the now-consumed `_attachment-staging/<message-id>/` folder and commit that deletion
   along with the article update, so staging doesn't grow unbounded.
4. If the folder isn't there yet, it means the fetch workflow hasn't run since the email arrived
   (it runs hourly, offset :15) — note it as pending in STATUS.md like normal, it should appear
   within the hour.

This directory is intentionally outside `editions/` so `edition_checks.py`'s folder-scanning
(which treats every folder under `editions/` as a potential article) never picks it up.
