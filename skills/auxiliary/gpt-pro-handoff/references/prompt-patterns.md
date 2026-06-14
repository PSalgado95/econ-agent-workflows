# Prompt patterns

Use a short, explicit prompt that tells GPT Pro:

- what the package is for;
- what success means;
- how to read it;
- what evidence rules govern the answer;
- what not to do;
- when to stop;
- and what to return.

For handoff prompts, the most useful structure is usually clear blocks plus a clean output contract, not a long pseudo-workflow. Describe the destination and constraints; only prescribe the path when the path is part of the task.

## Current prompt principles

Use these principles when writing handoff prompts:

- Lead with the outcome and success criteria.
- Use step-by-step process instructions only when exact order matters.
- Treat `must`, `always`, `never`, and `only` as hard-rule language for true invariants.
- Define what counts as enough evidence and what to do when evidence is missing.
- Keep stable structure early and dynamic task-specific detail later.
- Add validation expectations for code-facing, visual, or implementation-planning tasks.
- Add stop rules so the task does not keep expanding after the core ask can be answered.

## Core prompt shape

Use this structure by default.

```text
You are reviewing a curated handoff package prepared by Codex.

## Goal
[one clear statement of the task]

## Success criteria
- [what must be true before the final answer]
- [what evidence or contract must be satisfied]

## Package mode
- Mode: [lean | staged]
- Archetype: [lean review | lean plan | staged synthesis | staged revision | staged hybrid patch]

## How to use the package
1. Read `handoff_brief.md` first.
2. Read `package_manifest.md` second.
3. If present, read `source/package/governing_direction.md`.
4. If present, treat `source/package/return_contract.md` or `.yaml` as binding for filenames and bundle structure.
5. Use the files in `source/` as the primary evidence.

## Scope
- [what is in scope]
- [what is explicitly out of scope]

## Evidence rules
- Use the files in `source/` as primary evidence.
- Distinguish source-backed claims from inference or assumptions.
- Call out missing evidence before relying on it.

## Deliverables
Return exactly [N] deliverables:
1. ...
2. ...

## Working rules
- [high-value rule]
- [high-value rule]

## Stop rules
- Stop once the success criteria can be met from the package and allowed external research.
- If a blocking input is missing, name the smallest missing input rather than broadening the task.
- If the requested output cannot be supported by the package, return the closest useful bounded answer and list the blocker.
```

## When to keep the prompt minimal

Keep the prompt itself compact when the task is lean.

A lean prompt usually needs only:

- goal;
- success criteria;
- how to use the package;
- one short scope block;
- explicit deliverables;
- a few working rules;
- and stop rules.

Do not add `Context`, `Questions to answer`, and several extra blocks unless they genuinely do different jobs.

## When to extend the prompt

Add extra blocks when staged structure needs them.

Useful staged additions:

- `## Audience and style`
- `## Non-goals`
- `## Folder guide`
- `## Diagnostic minimum`
- `## External research`
- `## Verification expectations`

Use them only when they remove recurring ambiguity.

## Separate the human ask from the machine contract

This is the most important prompt change.

### Put in the prompt

- the purpose of the task;
- success criteria;
- audience and tone;
- scope, non-goals, and evidence rules;
- the plain-language deliverables;
- and the most important working rules.

### Put in `source/package/return_contract.*`

- exact filenames;
- file-by-file section requirements;
- revised-file expectations;
- diff requirements;
- machine-readable appendix schema;
- and no-change rules.

That keeps the prompt readable without making the output contract vague.

## Lean prompt template

```text
You are reviewing a curated handoff package prepared by Codex.

## Goal
Assess whether the empirical design is credible and identify the strongest fixes.

## Success criteria
- The final memo distinguishes identification threats from presentation weaknesses.
- The revision brief names the highest-leverage fixes first.
- Claims are grounded in the packaged evidence or clearly labeled as assumptions.

## Package mode
- Mode: lean
- Archetype: lean review

## How to use the package
1. Read `handoff_brief.md` first.
2. Read `package_manifest.md` second.
3. Use the files in `source/` as the primary evidence.

## Deliverables
Return exactly 2 deliverables:
1. a short assessment memo for an economist-facing reader;
2. a prioritised revision brief.

## Evidence rules
- Use the files in `source/` as the primary evidence.
- Distinguish source-backed claims from inference.
- Call out missing evidence or ambiguities before leaning on them.

## Working rules
- Distinguish core identification problems from presentation weaknesses.
- Be concrete about what should change first.

## Stop rules
- Stop once the two requested deliverables can be written from the available evidence.
- If the evidence cannot support a credibility judgment, say exactly what is missing and give the most useful bounded assessment.
```

## Staged prompt template

```text
You are reviewing a curated handoff package prepared by Codex.

## Goal
Move from evidence review to a bounded implementation-ready recommendation.

## Success criteria
- The recommendation is traceable to the governing files and decisive evidence.
- Economist-facing and implementation-facing outputs remain separate.
- Any proposed implementation work stays within the stated live surface.

## Package mode
- Mode: staged
- Archetype: staged hybrid patch

## How to use the package
1. Read `handoff_brief.md` first.
2. Read `package_manifest.md` second.
3. Read `source/package/governing_direction.md`.
4. Read `source/package/return_contract.md`.
5. Use `source/evidence/` for the prior analysis and `source/code/` for the live implementation surface.

## Scope
- Focus on the live post-2010 measurement path.
- Do not redesign the broader pipeline.

## Deliverables
Follow the binding contract in `source/package/return_contract.md`.

## Evidence rules
- Use `source/evidence/` for prior analysis and `source/code/` for the live implementation surface.
- Verify governing notes against the evidence rather than inheriting them automatically.
- Mark unsupported claims, missing files, or uncertain owner assumptions explicitly.

## Working rules
- Keep the implementation bounded.
- Call out missing evidence or ambiguities before leaning on them.

## Stop rules
- Stop once the binding return contract can be satisfied.
- If a requested patch or recommendation is not supported by the package, keep it out of the main recommendation and list it as a blocker or deferred follow-up.
```

## Deliverable wording patterns

### Simple memo

Use:

- `Return exactly 1 deliverable: a structured memo ...`

### Human memo plus machine appendix

Use:

- `Return exactly 2 deliverables: (1) a short memo for [audience]; (2) a compact machine-facing appendix in YAML or JSON ...`

### Artefact bundle

Use:

- `Follow the binding contract in source/package/return_contract.md.`

That is cleaner than pasting a long filename list into the prompt body.

## Reading-order patterns

### Lean

The prompt can usually carry the reading order directly.

### Staged

Prefer progressive disclosure:

1. root control files
2. `source/package/`
3. then role folders in the intended order

Do not say "read everything" when some files govern the interpretation of others.

## Working-rule patterns that travel well

Use these when they fit:

- `Call out missing evidence or ambiguities before leaning on them.`
- `Treat distilled owner priors as things to verify, not assumptions to inherit automatically.`
- `Keep scope bounded to the stated task; do not turn this into a full redesign unless the evidence forces that conclusion.`
- `Separate the main recommendation from deferred follow-up work.`
- `Be concrete about what to add, tighten, remove, or rebalance.`

## Good habits

- Say `Return exactly N deliverables` when there are multiple outputs.
- Use exact audience language when tone matters.
- Keep non-goals explicit when the evidence invites sprawl.
- Prefer one short external-research instruction over several scattered reminders.
- Keep filenames and section ordering in the return-contract file when possible.
- Use examples only when they resolve a recurring ambiguity.
- Include stop rules for evidence gathering, scope expansion, and unsupported outputs.

## Avoid

- one huge undifferentiated context blob;
- long filename inventories in the prompt when the manifest or return contract can carry them;
- forcing the handoff through a pseudo-chain-of-thought procedure;
- making every preference a hard rule;
- repeating the manifest in the prompt;
- and overloading lean tasks with staged-package machinery.
