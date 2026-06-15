---
title: Short descriptive title
date: YYYY-MM-DD
status: active
scope: project
scope_basis: current project evidence
category: workflow-practice
evidence_paths:
  - path/to/evidence
applies_when:
  - condition where this lesson is useful
do_not_apply_when:
  - condition where this lesson would mislead
last_checked: YYYY-MM-DD
supersedes: none
superseded_by: none
refresh_reason: none
---

<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources (skills/, .codex/agents/, references/) and run build_claude.py. -->

# Short descriptive title

## Situation

What happened, in economist-facing language. Name the research object, source set, data object, model object, output, note, or review surface involved.

## Durable Lesson

State the reusable rule or habit. Keep it narrow enough that a future agent can apply it without importing the whole old project.

## Evidence

Name the plan, output, source, review finding, note, bundle, or closeout that supports the lesson. Use repo-relative file paths for local evidence. For non-file evidence, use an explicit identifier such as `source_id:...`, `archive_id:...`, `register_id:...`, `dataset_id:...`, or `doi:...`.

If the lesson came from an old memo, exploratory report, GPT bundle, or project brief, name the underlying source, output, script, or review finding that makes the lesson credible. Do not treat the old artifact itself as authority unless it was the reviewed object.

## Reuse Boundary

State when to apply the lesson, when not to apply it, and what live evidence overrides it. If this note is stale, explain the conflict under `refresh_reason` in the frontmatter.

## Future Workflow Use

State how future `econ-plan`, `econ-work`, or `econ-review` runs should consult this note.
