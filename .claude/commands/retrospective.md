# /retrospective

Run at the end of a session (or any time lessons need capturing) to memorialize what went
wrong, what went right, and apply those lessons to CLAUDE.md, skills, and memory files.

**Nothing is written until you approve the proposed changes.**

---

## Step 1 — Gather what happened

Ask the user:

> "What went wrong this session? What did we have to fix or redo? What went right that we
> should preserve? I'll draft all changes for your review before applying anything."

If the user gives a narrative, extract a list of discrete incidents — each with:
- **What happened** (the observable failure or success)
- **Root cause** (why it happened)
- **Category** (photo placement, nav, deployment, article structure, process, email, git, etc.)

If the user says "check the session" or similar, review:
- Recent git log: `git log --oneline -20`
- Recent memory files for the session
- Any hotfixes pushed (post-publish commits are a strong signal something went wrong)

---

## Step 2 — Audit existing documentation

For each incident, check whether it is already covered:

**CLAUDE.md mistakes list:**
```bash
grep -n "^\d\+\." /home/john/article/CLAUDE.md | tail -20
```

**Relevant skills:**
- `/prep-edition` — edition setup gaps
- `/new-edition` — article building, photo placement
- `/edition-checks` — pre-staging quality gate
- `/publish` — pre-publish checks
- `/stage` — promotion process

**Memory files:**
```bash
cat /home/john/.claude/projects/-home-john-article/memory/MEMORY.md
```

Note: if an incident is already documented accurately, skip it. Only document gaps or
corrections to existing documentation.

---

## Step 3 — Draft all proposed changes

Produce a single review document with every proposed change grouped by destination.
**Do not write anything yet.** Present this to the user first.

Format:

---
### CLAUDE.md — New mistakes
**#N — [Short title]**
[Full mistake text as it would appear in the numbered list]

### CLAUDE.md — Corrections to existing
**#N (current text):** [what it says now]
**Proposed change:** [what it should say]

### Skill: /skill-name — [section being changed]
**Current:** [relevant excerpt]
**Proposed:** [replacement text]

### Memory: [filename] — [new or updated]
**Type:** feedback / project / reference / user
**Content:** [full memory body]
---

Then ask:

> "Here are the proposed changes. Review each one and let me know:
> - Approve all → I'll apply everything
> - Approve some → tell me which to skip
> - Correct any → tell me what's wrong and I'll revise before applying"

---

## Step 4 — Apply approved changes

For each approved change, in order:

1. **CLAUDE.md** — add or correct mistakes in the numbered list; keep numbering sequential
2. **Skill files** — edit `.claude/commands/` files; only the specific sections that changed
3. **Memory files** — write new files or update existing ones in
   `/home/john/.claude/projects/-home-john-article/memory/`; update `MEMORY.md` index

Commit after all changes are applied:

```bash
git add CLAUDE.md .claude/commands/
git commit -m "Retrospective: memorialize [session date] lessons

[one line per major lesson added]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push origin dev2
```

Memory files do not need to be committed (they live outside the repo).

---

## Step 5 — Confirm

Report back:
- N mistakes added/updated in CLAUDE.md
- N skill sections updated (list which skills)
- N memory files written/updated
- Any incidents left undocumented and why (already covered, too specific to be reusable, etc.)

---

## Rules

- **Never apply changes without user review and approval** — Step 3 is mandatory; Step 4
  only runs after explicit approval.
- **Correct existing documentation, don't just append** — if a mistake is numbered wrong,
  an existing rule is incomplete, or a skill step is missing something, fix it rather than
  adding a new item that overlaps.
- **One lesson = one place** — don't duplicate the same rule across CLAUDE.md and a skill.
  CLAUDE.md gets the rule; the skill gets the operational step that enforces it.
- **Be specific** — "don't make mistakes" is not a rule. A rule names the exact action to
  take or avoid, the check to run, or the question to ask. Include the command or code snippet
  if the fix is a repeatable operation.
- **Flag corrections to wrong existing entries** — if a mistake is documented incorrectly
  (wrong root cause, wrong fix), propose a correction, don't just add a new one.
- **Memory vs. CLAUDE.md vs. skills:**
  - CLAUDE.md = the permanent rule or convention (what, never what happened)
  - Skills = the operational step that enforces the rule during a workflow
  - Memory = the context behind why a rule exists (the incident, the session, the decision)
