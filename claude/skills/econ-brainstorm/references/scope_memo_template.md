<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources and run build_claude.py. -->

# Scope Memo Template

The scope memo is the brainstorm's session state and its only durable output. Save it at `docs/plans/YYYY-MM-DD-<slug>-scope.md` (or the repo's plan convention). Brainstorms resume by reading it; `econ-plan` graduates it by upgrading the same document in place to a full plan, keyed on `readiness: scoping-only`.

Keep entries short — one line each is normal. An honest `unknown` beats an invented answer.

```markdown
---
readiness: scoping-only
date: YYYY-MM-DD
slug: <short-topic-slug>
---

# <Working title> — scope memo

## Question
<The economic question in one sentence, as currently understood.>

## Candidate estimand or descriptive object
<What would be estimated or described if this proceeded; `unknown` is fine.>

## Population and unit
<Who or what the answer is about, and the unit of observation.>

## Identification candidates
<One line per candidate design, including the non-obvious alternative raised
in the session — record it even when declined, marked `(declined)`.>

## Data requirements
<One line per requirement: source — what is needed — `verified` (how) or `assumed`.>

## Kill criteria
<What evidence or discovery would make the researcher drop this direction.>

## Out of scope
<What this direction deliberately does not cover.>

## Open unknowns
<The questions the next session should pick up first.>
```

## Field rules

- `readiness: scoping-only` stays until `econ-plan` upgrades the document; the brainstorm never changes it.
- **Data requirements** carry a `verified`/`assumed` tag on every line; `verified` names how (the file, register, or listing read). No untagged requirement.
- **Identification candidates** keep the session's non-obvious alternative on record, marked `(declined)` when the researcher set it aside.
- **Kill criteria** must be concrete enough to check later — "no register coverage before 2005" rather than "data problems".
- Refresh in place across sessions; do not create a second memo for the same direction.
