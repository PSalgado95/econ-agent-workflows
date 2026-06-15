<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources (skills/, .codex/agents/, references/) and run build_claude.py. -->

# Econ Compound Learning Schema

Use this reference when writing or refreshing a durable economics research learning note.

## Purpose

A learning note records precedent for future economics research work. It is not live project state. Current plans, code, data, outputs, notes, source files, and review findings override old learning notes.

Old memos, exploratory reports, GPT handoff bundles, and project briefs are leads unless they were explicitly reviewed or accepted for a defined purpose. A learning note should cite the underlying evidence behind such artifacts, not the artifact alone, unless the artifact itself is the reviewed object.

## Storage

Prefer an existing repo convention. Otherwise use:

- `docs/research-learnings/<category>/<slug>.md` inside a repo;
- `.codex/research-learnings/<category>/<slug>.md` when there is no repo but a durable local project folder exists.

Do not write substantive research lessons into `PROJECT_BRIEF.md`, `README.md`, or `AGENTS.md`.

## Required Frontmatter

```yaml
---
title: Short descriptive title
date: YYYY-MM-DD
status: active|provisional|stale|superseded
scope: project|repo|general
scope_basis: current project evidence
category: source-provenance|data-measurement|sample-linkage|specification-estimation|theory-models|interpretation-claims|writing-figures|reproducibility-handoff|workflow-practice
evidence_paths:
  - path/to/plan-or-review-or-output
applies_when:
  - condition where this lesson is useful
do_not_apply_when:
  - condition where this lesson would mislead
last_checked: YYYY-MM-DD
supersedes: none
superseded_by: none
refresh_reason: none
---
```

## Field Rules

- `title`: plain descriptive title, no project-state claim.
- `date`: date the note was first written.
- `status`: use `active` for usable precedent, `provisional` when evidence is clear but limited, `stale` when current evidence conflicts with the note or the note cannot guide new work without refresh, and `superseded` only when a successor note is named.
- `scope`: use `project` by default; use `repo` for lessons that apply across several tasks in the same repo; use `general` only with user confirmation or evidence from multiple projects.
- `scope_basis`: one short reason the chosen scope is justified. For `general`, say either `user-confirmed general` or name the multi-project evidence basis.
- `category`: choose one category from the allowed list.
- `evidence_paths`: at least one path or source ID supporting the lesson. Use repo-relative paths inside a repo. For non-file evidence, use an explicit prefix such as `source_id:`, `archive_id:`, `register_id:`, `dataset_id:`, or `doi:`. A durable note needs a named evidence path or source ID that the agent has read or that the user explicitly supplied.
- `applies_when`: the positive reuse boundary.
- `do_not_apply_when`: the guard against stale or over-general use.
- `last_checked`: date the note was last checked against live evidence.
- `supersedes`: `none`, a repo-relative note path, or an explicit source ID. Separate multiple entries with semicolons if needed.
- `superseded_by`: `none` unless `status: superseded`, in which case it must name the successor note, evidence path, or explicit source ID.
- `refresh_reason`: `none` unless `status: stale`, in which case it must explain why the note should not currently guide work.

## Categories

- `source-provenance`: source discovery, access restrictions, metadata traps, evidence categories, source logs.
- `data-measurement`: variable definitions, denominators, table reconstruction, exposure or treatment construction.
- `sample-linkage`: panels, joins, concordances, inclusion rules, support and missingness.
- `specification-estimation`: estimands, baselines, robustness, inference, model-output equivalence.
- `theory-models`: notation, model objects, derivation checks, calibration interpretation, mechanism exposition.
- `interpretation-claims`: what evidence can support, claim-budget rules, overclaiming risks.
- `writing-figures`: note structure, figure-text consistency, paper-facing synthesis discipline.
- `reproducibility-handoff`: bundles, manifests, review packages, GPT Pro packages, rerun status.
- `workflow-practice`: useful planning/work/review patterns that do not fit a narrower category.

## Note Body

Use the template in `assets/learning_template.md`.

The note must include:
- Situation;
- Durable Lesson;
- Evidence;
- Reuse Boundary;
- Future Workflow Use.

Keep the note compact. If it needs a long narrative, a review note, methods memo, or project brief is probably the better home.
