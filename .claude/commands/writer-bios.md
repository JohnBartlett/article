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

1. Check `_bios/<slug>.md` for the writer's attribution line.
2. If the writer's attribution line is not "(none — byline only)", add it as the last paragraph in `.article-body`. Link the author's name to their `about.html` anchor:
```html
<p style="font-size: 15px; color: #888; font-style: italic;"><a href="../../../about.html#slug" style="color: #b51c20;">Author Name</a> is a ... attribution line.</p>
```

## Adding a new writer

1. Create `_bios/<slug>.md` with their info.
2. Add a `<div class="team-member" id="<slug>">` entry to the "Our Writers This Week" section of `about.html`.
3. If they have an articles popup (most recurring writers do), add it after the team-member div following the pattern used for David Sweet, Susan Aurinko, Jen Huang, etc.

## Updating an existing bio

Edit `_bios/<slug>.md` directly. If the bio text changes, also update the matching entry in `about.html`.

## Current writers

Run `ls _bios/` to see all writer bio files. Each filename is the slug; the `about.html` anchor is `#<slug>`.
