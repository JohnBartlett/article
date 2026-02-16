# Branch Strategy

This repository uses three branches:

## `master` — Production
The production branch. Code on `master` is live and deployed to the production site. Only merge into `master` from `dev` after changes have been staged and verified.

## `dev` — Staging
The staging branch. Changes are collected and reviewed here before being promoted to `master`. Use `dev` to verify that content and code changes work correctly before deploying to production.

## `dev2` — Experimental
The experimental branch for spitballing ideas and trying things out. Work here is informal and may or may not be promoted to `dev`. Use `dev2` for drafts, experiments, and exploratory changes without affecting staging or production.

## Workflow

```
dev2 (experiment) --> dev (stage & verify) --> master (production)
```

1. Try out new ideas on `dev2`.
2. When changes are ready for review, merge or cherry-pick them into `dev`.
3. After verifying on `dev`, merge into `master` for production deployment.
