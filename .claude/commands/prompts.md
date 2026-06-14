# /prompts

Quick reference for phrasing common requests on Classic Chicago Magazine. The point is to say what you want in plain terms — I'll figure out the mechanism. These are example phrasings that have worked well; deviations are fine.

When the user runs `/prompts`, display this reference grouped by task type. Use it as a cheat sheet, not a script.

---

## Photos & captions

| What you want | Try saying |
|---|---|
| Fix a single caption | "In the [article] article, change photo N's caption to '...'" |
| Match captions to filenames | "The captions are supposed to be: [list]. Match them to photos by filename." |
| Swap two captions | "Swap the captions on photos 4 and 5 in [article]." |
| Add a caption to an uncaptioned photo | "Add the caption '...' to photo N in [article]." |
| Remove a caption | "Remove the caption from photo N in [article]." |

## Photo size & position

When an image looks wrong, just describe the result you want — I'll pick between CSS and an actual file crop.

| What you want | Try saying |
|---|---|
| Smaller inline photo | "Make photo N in [article] half size." (or "two-thirds", "small", "thumbnail-sized") |
| Crop higher in a hero/card | "Shift the focus up on the [article] hero so her face isn't cut off." |
| Crop lower | "Move the crop down on the [article] homepage card — show more of the foreground." |
| Re-center a crop | "Center the crop horizontally on the [article] cover." |
| Replace the cover photo with a different one | "Use photo N as the cover for [article] instead." |
| Re-order photos | "Move photo 3 to be the second photo in [article]." |

Two mechanisms behind the scenes:
- **Cropped containers** (homepage cards, hero) — adjusted via `object-position` (no file change)
- **Inline figures** (article body) — full image shown; resize via `max-width` on the `<figure>`, or actually re-crop the file

You don't need to know which case applies — just describe the result.

## Article text

| What you want | Try saying |
|---|---|
| Fix a typo or wording | "In [article], change '...' to '...'" |
| Add an author link | "Link the byline in [article] to the author bio in About." |
| Update the byline | "Change the byline on [article] to 'By Jane Doe'." |
| Insert a paragraph | "After the paragraph that begins '...', add: '...'" |
| Italicize a title | "Italicize 'Another Earth' wherever it appears in [article]." |

## Homepage & navigation

| What you want | Try saying |
|---|---|
| Reorder articles | "Make [article] the hero this week; move [other] to position 3." |
| Update a card's image | "Use [filename] as the homepage card image for [article]." |
| Update a card's teaser | "Change the homepage teaser for [article] to: '...'" |
| Fix article-to-article nav | "Run /layout nav" (or "fix the next/previous links across this edition") |

## Editions & deployment

| What you want | Try saying |
|---|---|
| Prep a new edition skeleton | "Prep the [date] edition from Judy's article list" → runs `/prep-edition` |
| Fill in articles as content arrives | "Build [article] from the email Judy sent" → runs `/new-edition` |
| Lay out a single article | "Build [article] from the email Judy sent on [date]" |
| Deploy a dev2 preview | "Deploy a fresh preview." |
| Promote dev2 → dev | "/stage" |
| Push to production | "/publish" |
| Verify edition state | "Verify the [date] edition" → runs `tools/verify_edition.py` |

## Editorial review

| What you want | Try saying |
|---|---|
| Check Judy's emails | "/check-emails" (process new instructions and FormSubmit votes) |
| Refresh the editors pages | "/update-editors" |
| Draft Judy's weekly update | "/send-update" |
| Layout audit | "/layout audit" (report only) or "/layout fix" (apply) |

## When in doubt

A vague description plus the article name is usually enough:
- "Something looks off on the [article] hero — the subject's eyes are cut off."
- "The third photo in [article] looks too big next to the text."
- "Can you check the captions on [article]? Two of them look swapped."

If I'm not sure what you mean, I'll ask one clarifying question before editing.
