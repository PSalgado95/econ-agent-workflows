---
name: econ-review
description: "Review empirical economics or hybrid analysis-engineering work. Use for plan reviewability, results review, bundle review, note-facing review, GitHub issue-ready follow-up drafting, or mixed code-output-note diffs. Audit supporting artefacts rather than recreating the whole workflow, assign stable trust-impact findings, classify fix routes, and run a dedicated reader-facing note gate when notes are in scope."
---

# Economist Review Workflow

Review the current empirical object before trusting it, promoting it, or handing it to a co-author.

## Direct invocation contract

Direct invocation of `econ-review` is an explicit request to try the subagent review panel. The default path is:

1. parse the review target, surface, tier, and mode;
2. select the economist reviewer roles;
3. spawn the selected reviewer agents in parallel when subagent tools and reviewer agents are available;
4. validate their JSON payloads;
5. merge, deduplicate, and assign stable finding IDs; and
6. return a findings-first synthesis.

Do not silently downgrade a panel review into a single-agent review. If subagents or configured reviewer agents are unavailable, use the fallback rules below and label the result as degraded.

The object under review is:
1. what is being estimated or described;
2. how the realised sample was formed;
3. what the canonical outputs actually show; and
4. what the note or memo claims those outputs mean.

Route pure software reviews to the current software-engineering review workflow when available.

Keep this file as the parent review contract. Read `references/review_reference.md` when you need the detailed surface read order, reviewer-role matrix, custom-agent mapping, fallback rules, finding taxonomy, issue-ready templates, or headless output envelope. Reviewer agents use the shared protocol in `references/reviewer-protocol.md` from this package repository or the installed copy at `~/.codex/references/econ-agent-workflows/reviewer-protocol.md` when available. If the protocol is unavailable and the parent cannot pass the relevant protocol excerpt, treat the panel as degraded before dispatch.

## Input parsing

Parse these tokens when present:
- `mode:report-only`;
- `mode:autofix`;
- `mode:headless`;
- `tier:quick|standard|promotion`;
- `surface:plan|results|bundle|note|diff|mixed`;
- `interpretation:yes|no`;
- `issues:yes|no`;
- `plan:<path>`; and
- `base:<ref>`.

Treat the remainder as the plan path, bundle path, note path, branch, diff scope, or review target.

Conflicting mode flags are an error. Stop rather than guessing.

## Modes

Interactive (default)
- run the review;
- apply safe auto-fixes silently when they are truly non-substantive; and
- present a findings-first synthesis.

`mode:report-only`
- read-only review;
- no file mutation;
- good for parallel audit or early critique.

`mode:autofix`
- no interactive questions unless a baseline-defining user decision blocks the whole review;
- apply only safe documentation and bundle-hygiene fixes;
- write a run artefact under `.context/econ-review/<run-id>/`; and
- report residual work and stop.

`mode:headless`
- same mutation boundary as autofix;
- no interactive questions;
- write a run artefact under `.context/econ-review/<run-id>/`; and
- return the structured envelope in `references/review_reference.md`.

## Safe auto-fix boundary

Safe auto-fix includes:
- path repairs;
- stale cross-references;
- stale or missing bundle manifests;
- missing metadata fields; and
- missing choice-register rows when the decision is already explicit elsewhere.

Safe auto-fix does not include:
- changing the baseline;
- changing canonical software;
- changing variable definitions or sample rules;
- changing estimator settings;
- changing substantive interpretation; or
- rewriting the note's argument or opening.

## Review tiers

If `tier:` is omitted, infer the lightest tier that protects the decision:

`quick`
- use for small hygiene checks, narrow plan reviewability checks, or documentation/bundle cleanup;
- do not run a full reviewer panel unless the target unexpectedly touches realised empirical claims.

`standard`
- default for empirical outputs, review bundles, and hybrid code-output changes;
- cover provenance, specification, sample/transformation, output consistency, and claim discipline when interpretation is live.

`promotion`
- use before sending to a coauthor, supervisor, paper appendix, replication package, or public-facing surface;
- require stricter treatment of missing diagnostics, rerun status, note claims, and portability.

Escalation triggers:
- any claim-bearing empirical change is at least `tier:standard`;
- coauthor, supervisor, paper, appendix, replication package, presentation, or public-facing promotion is `tier:promotion`;
- changed sample construction, estimand, specification, weighting, clustering, inference, treatment timing, inclusion/exclusion rules, or headline table/figure cannot remain `tier:quick`;
- if the tier is uncertain, choose the stricter tier when the result may be promoted.

## Fix classes

For each finding, classify the recommended fix:
- `safe automatic`: non-substantive path, manifest, metadata, stale-link, or bundle-hygiene repair;
- `gated`: the fix is mechanical but should wait for user approval because it changes what gets promoted, shown, or emphasized;
- `manual`: requires economist judgement, rerun choice, baseline choice, interpretation choice, or new empirical work;
- `advisory`: useful improvement but not required for trust or promotion.

## Review surfaces

If `surface:` is omitted, infer it conservatively from the target.

Surface meanings:
- `plan` -> review whether the plan makes later empirical review possible;
- `results` -> default trust surface for realised empirical work;
- `note` -> never review the note in isolation from its evidence;
- `bundle` -> standard external-handoff surface;
- `diff` -> never stop at the diff; and
- `mixed` -> use when note, outputs, and code changed together.

Use the surface-specific read order in `references/review_reference.md`.

## Core diagnostic minimum

Whenever the surface touches realised empirical outputs, try to locate and test these artefacts when relevant:
- sample accounting;
- merge and key diagnostics;
- missingness and support diagnostics;
- weighting, grouping, and denominator integrity checks;
- a model-spec ledger or equivalent stable specification surface for realised estimates or model-based descriptives;
- an output-consistency map when note, memo, table, or figure claims are in scope;
- an interpretation brief when interpretation is in scope;
- a note brief when reporting is in scope; and
- rerun or build metadata showing whether outputs are rerun, inspected-only, or inherited.

If one of these surfaces is relevant and missing, surface that absence as a diagnostic gap rather than reading past it.

## Workflow

### Stage 0: Determine scope and route

Decide:
- domain mode (`empirical`, `hybrid`, or `software-handoff`);
- review tier;
- review surface;
- whether GitHub issue drafting or creation was requested;
- whether interpretation is in scope;
- whether a reader-facing note is in scope; and
- the source-of-truth hierarchy.

If the target is actually pure software, route to the current software-engineering review workflow and stop. If no such workflow is available, state the route mismatch and stop rather than forcing pure software review through the empirical panel.

If a GitHub issue is named, treat it as coordination context only. Use the plan, outputs, checks, bundle, and note surfaces as the analytical record.

### Stage 1: Gather evidence

Read the evidence in the correct order for the review surface using `references/review_reference.md`.

Always try to locate:
- the current plan or workflow note;
- the current choice register;
- output specification or manifest when outputs changed materially;
- canonical outputs;
- checks and audit artefacts;
- the model-spec ledger when relevant;
- the output-consistency map when note-facing claims are in scope;
- the interpretation brief when interpretation is in scope;
- the note brief when reporting is in scope;
- build info or rerun-status notes; and
- the review bundle when present.

If a required diagnostic surface is missing, treat that absence as review evidence.

Before dispatch, build a compact evidence manifest for reviewers. Include:
- review target and surface;
- source-of-truth hierarchy;
- discovered plan, workflow note, bundle, outputs, checks, ledgers, briefs, maps, and note paths;
- missing diagnostic surfaces;
- base ref or diff scope when relevant;
- rerun or build-status evidence when visible; and
- any known blind spots or unavailable files.

Pass this evidence manifest to every reviewer prompt so child reviewers start from the same source map the parent found.

### Stage 2: Select the review panel

Always include:
- `provenance-auditor`; and
- `specification-auditor`.

For any surface other than `plan`, default the economist core to:
- `transformation-and-sample-auditor`; and
- `output-consistency-auditor`.

Add `claim-discipline-auditor` whenever interpretation is in scope. For `surface:note`, note-facing bundle review, and interpretation-bearing `surface:mixed`, it is compulsory.

Use the role matrix in `references/review_reference.md` for additional conditional reviewers such as estimation-practice, dynamics, design, robustness, reproducibility, software-equivalence, hybrid-implementation, or bundle review.

Do not duplicate roles that are asking the same question.

Before dispatch, announce the selected reviewer roles and the review tier. This makes it visible whether the run is a compact plan review, a standard results review, or a promotion-grade panel.

### Stage 3: Spawn reviewer subagents

Spawn one custom reviewer agent per selected role in parallel and wait for all available reviewer agents before synthesis. Use the role-to-agent mapping in `references/review_reference.md`.

For each reviewer prompt, include:
- assigned role;
- review surface;
- interpretation flag;
- review tier;
- plan path, base ref, and target when present;
- evidence manifest from Stage 1;
- the relevant surface read order;
- the JSON output contract from the shared reviewer protocol; and
- the instruction to return JSON only, with evidence-led findings, no raw logs, no file mutation, no artifact writes, and no issue updates.

If a selected reviewer agent is not configured, treat that as a degraded panel and record the missing role in the artefact summary.

Fallback rules:
- `tier:quick`: a degraded single-thread review may proceed if the final output clearly says the panel did not run.
- `tier:standard`: a degraded review may proceed only with an explicit warning and a list of missing roles.
- `tier:promotion`: do not silently proceed in degraded mode. Ask the user whether to accept a degraded review, install/configure the missing agents, or stop. In `mode:headless`, stop with a degraded verdict rather than promoting the result.

Subagent failure handling:
- If a reviewer returns malformed JSON, discard or quarantine that payload and report the role as degraded.
- If a reviewer returns findings without evidence paths, suppress those findings unless the issue is a visible bundle-metadata gap.
- If all reviewer agents fail or are unavailable, do not call the result a panel review.

### Stage 4: Merge and deduplicate

Merge reviewer payloads conservatively:
- discard malformed payloads;
- suppress findings with no evidence path unless the issue is a bundle-metadata gap visible in the bundle itself;
- deduplicate by title plus overlapping evidence path plus issue origin;
- keep the higher severity on duplicates; and
- keep the more conservative trust effect on disagreement.

Build these queues:
- `Blocking before trust`;
- `Worth checking before promotion`;
- `Diagnostic gaps`; and
- `Documentation / cleanup`.

Assign stable finding IDs after deduplication:
- use existing IDs if reviewing a prior findings file or residual summary;
- otherwise assign `F1`, `F2`, ... in severity order;
- keep IDs stable in residual summaries and issue drafts.

Classify every retained finding with a fix class: `safe automatic`, `gated`, `manual`, or `advisory`.

Carry affected labels forward when reviewer payloads provide them. These may include plan labels, output IDs, issue numbers, branch/worktree names, or evidence IDs.

### Stage 5: Optional safe auto-fix

In interactive mode, apply safe auto-fixes silently and then present findings.

In `mode:autofix` or `mode:headless`, apply only safe auto-fixes once, write a run artefact, and stop after reporting residual work.

Run artefacts under `.context/econ-review/<run-id>/` are transient review records, not analytical evidence and not project memory. Durable review evidence belongs in the project plan, outputs, checks, review bundle, interpretation brief, note brief, or approved project-backbone update.

Suggested artefacts:
- `findings.md`;
- `findings.json`;
- `applied_fixes.md`; and
- `residual_work.md`.

### Stage 6: Reader-facing note gate

Whenever the target includes a note, note-facing bundle, or interpretation-bearing mixed surface, run this gate directly.

Check that:
1. the first paragraph tells the reader what the note studies, what the main answer is, and why the note exists;
2. the empirical object, sample boundary, and main comparison are defined before decompositions, benchmark bridges, or implementation details;
3. the main text can be understood without repo knowledge;
4. internal workflow nouns do not carry the main narrative;
5. figures appear in a sensible order, with the headline figure first;
6. benchmark material and heavy diagnostics are bounded rather than crowding the lead;
7. variable names, file paths, and wave IDs are not overused when ordinary economic language would do; and
8. limitations are stated explicitly.

A note that reads like an execution log or opens from workflow machinery is at least a meaningful note-register problem even when the underlying results are sound.

### Stage 7: Synthesize for the user

Always lead with findings.

Default output shape:
1. `Blocking before trust`;
2. `Worth checking before promotion`;
3. `Diagnostic gaps`;
4. `Documentation / cleanup`;
5. `Reader-facing note register` when relevant;
6. `Open questions`; and
7. `Artefact summary`.

For each finding include:
- finding ID;
- severity;
- trust effect;
- issue origin;
- fix class;
- affected labels, if any;
- short title;
- why it matters;
- evidence path(s);
- recommended action; and
- whether user judgement is required.

For `surface:plan`, make clear that the verdict is about reviewability, not realised-output certification.

If `issues:yes` was supplied or the user explicitly asked to file/draft GitHub issues:
- produce issue-ready follow-ups for retained findings whose fix class is `gated` or `manual`, or whose trust effect is `baseline-defining` or `promotion-blocking`;
- keep one issue per coherent empirical problem or implementation lane, not one issue per reviewer sentence;
- distinguish empirical problem, implementation fix, robustness extension, and note/paper follow-up;
- include objective, evidence surface, proposed done-when condition, and links to finding IDs;
- include affected labels when they help tie the issue to a plan decision, output, branch, or existing issue;
- create or update GitHub issues only after explicit approval, unless the user already directly asked for creation in the current request.

### Stage 8: Headless output envelope

In `mode:headless`, use the structured envelope in `references/review_reference.md`.

## When to ask the user

Ask rather than guessing when the live question is:
- whether to promote a result;
- whether to change the baseline;
- whether a divergence is decisive or merely descriptive;
- whether interpretation is in scope; or
- whether a substantive note or memo should be rewritten.

If `request_user_input` is unavailable, ask concise numbered choices in chat, name the recommended conservative default, and wait for the user's answer when the decision changes trust, promotion, baseline, or interpretation.

Do not ask for documentation-only cleanups, path repairs, missing manifest rows, or clearly safe bundle-hygiene fixes.

## Hard stops

- Do not mutate analytical content in safe auto-fix.
- Do not create or update GitHub issues unless the user requested or approved it.
- Do not treat GitHub issue text as analytical evidence without checking the actual plan, outputs, code, or bundle.
- Do not review a note in isolation from its evidence.
- Do not let reader-facing note failures disappear into generic copy-editing language.
- Do not treat numerical similarity alone as proof that two paths estimate the same analytical object.
- Do not let documentation-only gaps masquerade as baseline failures.
- Do not treat missing required diagnostic surfaces as harmless omissions.
