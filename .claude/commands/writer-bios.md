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
2. Do **not** add an "About the Author" link in the article — author links belong on `about.html`, not in articles.
3. If the writer's attribution line is not "(none — byline only)", add it as the last paragraph in `.article-body`:
```html
<p style="font-size: 15px; color: #888; font-style: italic;">Attribution line here.</p>
```

## Adding a new writer

1. Create `_bios/<slug>.md` with their info.
2. Add a `<div class="team-member" id="<slug>">` entry to the "Our Writers This Week" section of `about.html`.
3. If they have an articles popup (most recurring writers do), add it after the team-member div following the pattern used for David Sweet, Lee Hamilton, etc.

## Updating an existing bio

Edit `_bios/<slug>.md` directly. If the bio text changes, also update the matching entry in `about.html`.

## Current writers

| File | Name | about.html anchor |
|------|------|-------------------|
| `adrian-naves.md` | Adrian Naves | `#adrian-naves` |
| `david-sweet.md` | David A. F. Sweet | `#david-sweet` |
| `elizabeth-dunlop-richter.md` | Elizabeth Dunlop Richter | `#elizabeth-dunlop-richter` |
| `jen-huang.md` | Jen Huang | `#jen-huang` |
| `judy-carmack-bross.md` | Judy Carmack Bross | `#judy-carmack-bross` |
| `lee-hamilton.md` | Lee Hamilton | `#lee-hamilton` |
| `sophie-bross.md` | Sophie Bross | `#sophie-bross` |
| `susan-aurinko.md` | Susan Aurinko | `#susan-aurinko` |
| `sydney-armstrong.md` | Sydney Armstrong | not yet in about.html |
