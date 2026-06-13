---
name: econ-compound
description: Capture durable economics research learnings after completed plan, work, review, note, source, data, model, or handoff tasks. Use when Codex should save or refresh a reusable lesson that future econ-plan, econ-work, or econ-review runs should consult; when deciding whether a lesson is durable or closeout-only; or when searching prior research-learning notes for relevant precedent.
---

# Economist Compound

Capture a reusable research lesson while the evidence is fresh. A learning note is precedent, not project state: it must not replace the current plan, source files, data, outputs, notes, review findings, or project backbone.

Keep this file as the workflow contract. Read `references/learning_schema.md` and `assets/learning_template.md` when writing or refreshing a learning note. Run `scripts/validate_learning_note.py` when a note is written or updated.

Do not auto-write learning notes from ordinary success language such as "that worked" or "good, remember this". Economics research lessons are contingent. Write or update a durable note only when the user explicitly asks for learning capture, or when an autonomous run explicitly includes compounding.

## Routing

Use `econ-compound` for economics research and hybrid analysis lessons, including empirical work, source work, data construction, theory or model exposition, paper-facing synthesis, reproducibility, and handoff practice.

Route elsewhere when appropriate:
- pure software-only lessons -> current Compound Engineering compound skill;
- writing-style preferences -> `econ-writing` preference capture;
- project-state updates -> current plan, issue, project backbone, note, or review finding, only with user approval;
- old memos, exploratory reports, GPT bundles, or project briefs -> use as leads only unless they were explicitly reviewed or accepted for a defined purpose;
- one-off closeout facts -> closeout only, not a durable learning note.

## Input modes

Classify the request before writing:
- `capture`: the user names a lesson, plan, closeout, review finding, output, note, source bundle, or task that just finished;
- `search`: the user asks for prior lessons or precedent;
- `refresh`: the user names an existing learning note that may be stale, duplicated, or superseded.

If the mode is unclear, inspect named files first. Ask one focused question only when the answer changes whether to write, update, or skip the durable note.

In `search` mode, do not write a note. Return relevant notes found, evidence paths, reuse boundaries, stale or conflict cautions, and whether any note should change the current plan, work, or review advice.

## Candidate gate

Write or update a durable note only when the lesson is reusable.

Good candidates:
- a source, access, or provenance trap that would change future collection plans;
- a data, linkage, denominator, measurement, or sample-construction rule;
- an estimand, baseline, inference, robustness, or software-equivalence rule;
- a theory, model, notation, or calibration exposition pattern worth reusing;
- a claim-budget or interpretation rule surfaced by work or review;
- a figure, note, memo, or paper-facing synthesis pattern;
- a reproducibility, manifest, review-package, or GPT Pro handoff lesson;
- a workflow practice that future plan/work/review runs should consult.

Bad candidates:
- a task-local status update;
- a trivial file move, typo, or one-off cleanup;
- a result that belongs in the paper, note, review finding, issue, or project backbone;
- a complaint with no evidence path;
- a preference about prose style that belongs in `econ-writing`;
- a broad maxim with no reuse boundary.

No named evidence path or source ID means no durable learning note. The evidence must be a repo-relative path or explicit source ID the agent has read, or one the user explicitly supplied. Use prefixes such as `source_id:`, `archive_id:`, `register_id:`, `dataset_id:`, or `doi:` for non-file evidence. If the lesson rests only on a broad chat impression, return `durability: closeout-only` or `durability: not-a-lesson`.

If the lesson is useful only for the current task, include it in closeout and return `durability: closeout-only`. Do not write a learning note.

## Categories

Use one category:
- `source-provenance`: source discovery, access restrictions, metadata traps, evidence categories, source logs.
- `data-measurement`: variable definitions, denominators, table reconstruction, exposure or treatment construction.
- `sample-linkage`: panels, joins, concordances, inclusion rules, support and missingness.
- `specification-estimation`: estimands, baselines, robustness, inference, model-output equivalence.
- `theory-models`: notation, model objects, derivation checks, calibration interpretation, mechanism exposition.
- `interpretation-claims`: what evidence can support, claim-budget rules, overclaiming risks.
- `writing-figures`: note structure, figure-text consistency, paper-facing claim discipline, and source/output-to-prose alignment.
- `reproducibility-handoff`: bundles, manifests, review packages, GPT Pro packages, rerun status.
- `workflow-practice`: useful planning/work/review patterns that do not fit a narrower category.

Do not use `writing-figures` for Pedro's prose-style preferences. Sentence rhythm, British English, caveat style, "AI-ish" phrasing, and preferred openings route to `econ-writing`. Use `writing-figures` only when the reusable lesson concerns evidence-to-claim discipline, figure-text consistency, or note structure.

## Evidence and stale-note rules

Every durable note must include:
- evidence paths, using repo-relative paths when inside a repo and explicit source-ID prefixes for non-file evidence;
- where the lesson applies;
- where it should not be applied;
- what live evidence overrides it;
- how future `econ-plan`, `econ-work`, or `econ-review` should use it.

Treat prior learning notes as precedent. If a note conflicts with live project files, current outputs, or current review findings, the live material wins. Mark the note as a refresh candidate rather than following it silently.

Use these statuses:
- `active`: usable precedent within its stated boundary;
- `provisional`: evidence is named and readable, but the basis is limited;
- `stale`: current evidence conflicts with the note, or the note should not guide work without refresh;
- `superseded`: a successor note or evidence path is named.

Use `scope: project` by default. Use `scope: repo` only when the lesson recurs across tasks in the repo. Use `scope: general` only with user confirmation or evidence from multiple projects.

When the evidence is an old memo, exploratory report, GPT bundle, or project brief, trace the lesson to the underlying source, data output, script, or review finding before making it durable. The old artifact can orient the search; it is not authority by itself unless it is the reviewed object.

## Storage

Prefer an existing repo convention for research-learning notes. Otherwise use:
- `docs/research-learnings/<category>/<slug>.md` inside a repo;
- `.codex/research-learnings/<category>/<slug>.md` when there is no repo but a durable local project folder exists.

Do not write substantive research lessons into `PROJECT_BRIEF.md`, `README.md`, or `AGENTS.md`.

Before creating a new note, search likely learning locations for overlap:
- `docs/research-learnings/`;
- `.codex/research-learnings/`;
- legacy `docs/solutions/` when present.

Use a bounded overlap search:
1. search filenames and frontmatter first;
2. read full bodies only for plausible candidates, capped at five notes unless the user asked for a broader refresh;
3. compare category, research object, durable lesson, evidence paths, applies-when, do-not-apply-when, and status;
4. update a high-overlap note rather than creating a duplicate;
5. mark a conflicting note `status: stale` with `refresh_reason` when no successor exists; and
6. use `status: superseded` only when `superseded_by` names the successor note or evidence path.

## Workflow

1. Read the named plan, closeout, review artifact, output, source bundle, note, or lesson text.
2. Decide `capture`, `search`, or `refresh`.
3. Apply the candidate gate: `durable`, `closeout-only`, or `not a lesson`.
4. If durable, choose category, scope, scope basis, status, evidence paths, applies-when, do-not-apply-when, refresh or supersession fields, and future workflow use.
5. Search for overlapping prior notes before writing.
6. Write or update exactly one learning note unless the user explicitly asks for a broader refresh.
7. Validate the note with `scripts/validate_learning_note.py`.
8. Return the saved path, category, durability decision, one-sentence lesson, reuse boundary, and where future workflows should consult it.

## Examples

Durable examples:
- Metadata-only search hits show that a public document existed and was hard to access, but cannot support claims about the document's content. Category: `source-provenance`.
- A measure should use the official eligible-population denominator for a specific exposure definition, with a boundary saying not to reuse it if the estimand becomes population-wide. Category: `data-measurement`.

Closeout-only examples:
- A rerun finished cleanly and all planned checks passed, with no changed definitions, samples, source rules, or claim rules.
- A task-specific note that one archive route was temporarily slow, with no broader access or provenance lesson.

Not-a-lesson examples:
- "Be careful with data" without a named evidence path or reuse boundary.
- A task status update that belongs in the closeout or issue comment.

Route-away examples:
- "Pedro prefers a less defensive opening" -> `econ-writing`.
- A pure implementation lesson about an app dependency or test harness -> current Compound Engineering compound skill.

## Output

For `capture` or `refresh`, return:
- `Durability`: durable|closeout-only|not-a-lesson;
- `Saved note`: path or none;
- `Category`: category or none;
- `Status`: active|provisional|stale|superseded|none;
- `Lesson`: one sentence;
- `Evidence`: evidence path or reason no durable note was written;
- `Reuse boundary`: when to apply and when not to apply;
- `Future workflow use`: how `econ-plan`, `econ-work`, or `econ-review` should consult it;
- `Validation`: validator result or reason not run.

For `search`, return:
- `Relevant notes`: paths or none;
- `How each note applies`: one line per note;
- `Stale or conflict cautions`: notes that current evidence should override or refresh;
- `Effect on current work`: whether the notes change the plan, work, or review advice.
