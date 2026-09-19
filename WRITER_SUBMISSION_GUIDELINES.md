# Writer Submission Guidelines (Internal Reference)

**Internal doc — dev2 only, not shown to writers directly.** This is what a complete,
build-ready submission from a contributor should include. Use it as a checklist when
content comes in, and adapt relevant parts into an email to a specific contributor if a
submission is missing something on this list. Every item traces back to a real mistake
already made on a published article — see the referenced CLAUDE.md mistake number for the
full incident.

Originated 2026-09-13, out of the Jill Lowe "Chitchat" PDF-fidelity fix session — most of
these items are things that either went wrong for her specific submission, or that Sig
Zetouni's and Ana Baca's submissions got right and other contributors haven't consistently
matched.

## The ideal submission format (layout mechanics)

- **Article text pasted directly into the email body, not a PDF or Word doc attachment.**
  Plain email text preserves paragraph breaks exactly as written. A PDF or Word doc
  requires an extraction step that silently discards paragraph breaks and all
  italics/bold — this is what happened to Jill Lowe's Chitchat article. (Mistake #43)
- **If a PDF/Word doc is unavoidable**, build using `pdftotext -layout` (not PyPDF2 — see
  mistake #43 for why) and do a page-by-page visual comparison (`pdftoppm -png`) against
  the built HTML before marking the article Ready. (Mistake #43, #46)
- **One photo per email, one caption per photo.** Never send multiple photos bundled into
  a single message or document with a shared caption block. Sig Zetouni's Chef
  submission — nine separate emails, each with exactly one attachment and one caption — is
  the model: it removes any possibility of a photo/caption mismatch, because there's never
  more than one candidate for either. A bundled document (PDF, Word doc with embedded
  images) forces us to infer both photo identity and placement at once from position
  alone, which is exactly what swapped two of Jill Lowe's photos. (Mistake #46)
- **Captions must be specific and complete**: full description *and* full credit line
  (photographer, museum, institution), not just a description. A specific caption also
  lets placement be inferred confidently by matching its keywords against the article
  prose — Sig's captions naming "Marcel Proust," "the Paperole," "NYB Hamantaschen" each
  matched exactly one paragraph. (Mistake #2)
- **State placement explicitly when possible** — "Photo 3 goes after the paragraph about
  X" — rather than relying on caption-to-prose keyword matching alone. Even a good
  caption still requires an inference step; explicit placement removes it entirely. Ana
  Baca's Puget Sound submission did this consistently and was noted at the time as "the
  cleanest placement instructions received all edition, no ambiguity."

## Everything else a complete submission needs

1. **Final title** — not a working title left to be confirmed later.
2. **Byline name spelled exactly as they want it published** — confirmed from their
   signature or a prior published byline, never inferred from an email address (e.g.
   "sigalina@aol.com" does not mean the person's name is "Sigalina"). (Mistake #4)
3. **Column/category name, if known** (e.g. "Facts and Froth," "My Silk Roads," "About the
   Town") — the small-caps label at the top of the article.
4. **Cover/homepage-card photo preference, if they have one** — distinct from the inline
   body photos; a photo with "COVER" in its filename is treated as the homepage card image
   and normally excluded from the article body unless it also has a caption and the
   contributor explicitly says to include it. (Mistake #27)
5. **Any format request, stated up front** — interview/Q&A vs. straight prose, a boxed
   quote treatment (like Laurel Baer's framed member-quotes), or anything else non-default.
   If it's a Q&A, the number of questions in the source must match exactly in the built
   HTML — a dropped question leaves no visible gap. (Mistake #6)
6. **Explicit inline links, if any**, with exact destination URL and anchor text. Link
   count must be checked against the source before publishing — an entire 39-link roundup
   article once shipped with every link silently dropped, reading coherently as plain text
   with no visible gap. (Mistake #42)
7. **If part of a multi-part series, explicit confirmation of the run schedule.** One part
   per edition, across consecutive weeks, never bundled into a single edition — confirmed
   directly from the current agreement, not inherited from an old citation. (Mistake #38)
8. **If someone other than the writer is sending the piece (a coordinator, spouse,
   assistant), state whose byline it runs under.** Don't assume the sender is the author —
   check whether they're a known production-assistant/coordinator role for someone else
   first (e.g. Emma Muhleman sends other writers' finished pieces as well as her own).
   When it's ambiguous, confirm explicitly rather than guessing either way. (Mistake #56)
9. **For a returning columnist, match their established category/style, don't default to
   generic.** Before publishing, check the author's own prior CCM bylines for the category
   label they've actually been running under (e.g. Bob Glaze's column runs under "Weekend
   Road Trips," not the template's generic default) — grep their name across `editions/`
   rather than leaving a placeholder category in place. (Mistake #55)

## Checking whether text has actually arrived

Before logging an email as "no article text" or "photos only," fetch it in full-content
format and check the actual attachment/MIME part list — not just the rendered body. A
`.docx` or other attachment can be present with zero mention of it in the visible text,
and a body-only read will miss it entirely. This caused Adrian Naves's Hawthorne Works
article (a real `.docx` attachment) to be logged as missing when it had, in fact, already
arrived. (Mistake #54)

## Why this exists

Every item above either caused a real published error once, or is a documented example of
a contributor getting it right that the rest of this list generalizes from. See CLAUDE.md's
"Common Mistakes to Avoid" section for the full incident behind each numbered reference.
