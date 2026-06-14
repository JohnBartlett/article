# /writer-bios

Manage the writer bio library at `_bios/`. Use this skill to look up, add, or update a writer's bio for use in articles and `about.html`.

## Bio file format

Each writer has a file at `_bios/<slug>.md`:

```markdown
---
name: Full Name
slug: about-html-anchor-id
role: Their role/column
about_url: about.html#anchor (or "not yet in about.html")
email: optional
website: optional
---

One or two sentence bio for about.html.

**Article attribution line:**
The italic line that appears at the end of their articles.
```

## When building an article

1. Look up the writer's `slug` and `about_url` in `_bios/<slug>.md`.
2. Add an "About the Author" link as the last element inside `.article-body`, before the feedback widget:
```html
<p style="margin-top: 32px;"><a href="../../../about.html#slug" style="font-family: 'Lato', sans-serif; font-size: 14px; font-weight: 700; color: #b51c20; text-decoration: none; text-transform: uppercase; letter-spacing: 0.08em;">About the Author: Author Name &rarr;</a></p>
```

**Do not include bio text in the article body.** The attribution line in the bio file is for `about.html` only — never paste it into an article.

## Adding a new writer

1. Create `_bios/<slug>.md` with their info.
2. Add a `<div class="team-member" id="<slug>">` entry to the **More Contributors** section of `about.html` (permanent bio card, persists across editions).
3. If they have an articles popup (most recurring writers do), add it after the team-member div following the pattern used for David Sweet, Susan Aurinko, Jen Huang, etc.
4. The "Our Writers This Week" section is updated each edition (via `/edition-checks`) — it is not updated here.

## Updating an existing bio

Edit `_bios/<slug>.md` directly. If the bio text changes, also update the matching entry in `about.html`.

## Current writers

Run `ls _bios/` to see all writer bio files. Each filename is the slug; the `about.html` anchor is `#<slug>`.
