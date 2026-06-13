---
name: econ-review
description: "Review empirical economics or hybrid analysis-engineering work. Use for plan reviewability, results review, bundle review, note-facing review, GitHub issue-ready follow-up drafting, mixed code-output-note diffs, or explicit cross-language validation planning/audit. Audit supporting artefacts rather than recreating the whole workflow, assign stable trust-impact findings, classify fix routes, and run a reader-facing note gate when notes are in scope."
---

# Economist Review Workflow

Review the current research object before trusting it, promoting it, or handing it to a co-author.

## Direct invocation contract

Direct invocation of `econ-review` is an explicit request to try the subagent review panel. The default path is:

1. parse the review target, surface, tier, mode, interpretation scope, and optional cross-language validation trigger;
2. gather empirical evidence and build one compact evidence manifest;
3. select the economist reviewer roles;
4. spawn the selected reviewer agents in parallel when subagent tools and reviewer agents are available;
5. validate their JSON payloads;
6. merge, deduplicate, and assign stable finding IDs; and
7. return a findings-first synthesis.

Do not silently downgrade a panel review into a single-agent review. If subagents or configured reviewer agents are unavailable, use the fallback rules below and label the result as degraded.

The object under review is:

1. what is being estimated or described;
2. what estimand or descriptive target is being claimed;
3. how the realised sample was formed;
4. what estimator, design, fixed effects, weights, inference, and dynamic conventions generated the object;
5. what the canonical outputs actually show; and
6. what the note or memo claims those outputs mean.

Route pure software reviews to the current software-engineering review workflow when available. Keep `econ-review` focused on research trust, hybrid empirical/software handoff, and economist-facing reproducibility.

Keep this file as the parent review contract. Read `references/review_reference.md` when you need the detailed surface read order, reviewer-role matrix, custom-agent mapping, fallback rules, finding taxonomy, cross-language validation trigger, issue-ready templates, or headless output envelope. Reviewer agents use the shared protocol in `references/reviewer-protocol.md` from this package repository or the installed copy at `~/.codex/references/econ-agent-workflows/reviewer-protocol.md` when available. If the protocol is unavailable and the parent cannot pass the relevant protocol excerpt, treat the panel as degraded before dispatch.

## Input parsing

Parse these tokens when present:

- `mode:report-only`;
- `mode:autofix`;
- `mode:headless`;
- `tier:quick|standard|promotion`;
- `surface:plan|results|bundle|note|diff|mixed`;
- `interpretation:yes|no`;
- `issues:yes|no`;
- `crosslang:no|yes|plan|audit`;
- `plan:<path>`; and
- `base:<ref>`.

Treat the remainder as the plan path, bundle path, note path, branch, diff scope, validation manifest, or review target.

Conflicting mode flags are an error. Stop rather than guessing.

`crosslang:` defaults to `no`. Natural-language requests such as "prepare a cross-language validation", "replicate this in Stata/R/Python", "compare R and Stata", "R = Stata check", or "cross-software validation" count as `crosslang:yes` unless the user explicitly says not to do it. Do not infer cross-language validation merely because the repository contains more than one language.

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
- changing inference settings;
- changing cross-language validation status;
- changing substantive interpretation; or
- rewriting the note's argument or opening.

## Review tiers

If `tier:` is omitted, infer the lightest tier that protects the decision:

`quick`
- use for small hygiene checks, narrow plan reviewability checks, or documentation/bundle cleanup;
- do not run a full reviewer panel unless the target unexpectedly touches realised empirical claims.

`standard`
- default for empirical outputs, review bundles, and hybrid code-output changes;
- cover provenance, specification/estimand, sample/transformation, output consistency, and claim discipline when interpretation is live.

`promotion`
- use before sending to a coauthor, supervisor, paper appendix, replication package, presentation, or public-facing surface;
- require stricter treatment of missing diagnostics, rerun status, note claims, inference, design support, output automation, and portability claims.

Escalation triggers:

- any claim-bearing empirical change is at least `tier:standard`;
- coauthor, supervisor, paper, appendix, replication package, presentation, or public-facing promotion is `tier:promotion`;
- changed sample construction, estimand, specification, weighting, clustering, inference, treatment timing, inclusion/exclusion rules, dynamic horizon, or headline table/figure cannot remain `tier:quick`;
- if the tier is uncertain, choose the stricter tier when the result may be promoted.

## Fix classes

For each finding, classify the recommended fix:

- `safe automatic`: non-substantive path, manifest, metadata, stale-link, or bundle-hygiene repair;
- `gated`: the fix is mechanical but should wait for user approval because it changes what gets promoted, shown, or emphasized;
- `manual`: requires economist judgement, rerun choice, baseline choice, interpretation choice, validation choice, or new empirical work;
- `advisory`: useful improvement but not required for trust or promotion.

## Review surfaces

If `surface:` is omitted, infer it conservatively from the target.

Surface meanings:

- `plan` -> review whether the plan makes later empirical review possible;
- `results` -> default trust surface for realised empirical work;
- `note` -> never review the note in isolation from its evidence;
- `bundle` -> standard external-handoff surface;
- `diff` -> never stop at the diff;
- `mixed` -> use when note, outputs, and code changed together.

Use the surface-specific read order in `references/review_reference.md`.

## Core diagnostic minimum

Whenever the surface touches realised empirical outputs, try to locate and test these artefacts when relevant:

- sample accounting;
- merge and key diagnostics;
- missingness and support diagnostics;
- weighting, grouping, and denominator integrity checks;
- a model-spec ledger or equivalent stable specification surface for realised estimates or model-based descriptives;
- an estimand statement or econometric evidence contract for realised estimates, causal claims, dynamic responses, or inferential claims;
- inference metadata: standard-error/test type, cluster level, cluster counts, finite-sample correction, special inference method, confidence-band convention, and multiplicity treatment when relevant;
- a horizon ledger for local projections, event studies, dynamic panels, cumulative responses, or other horizon-sensitive work;
- an output-consistency map when note, memo, table, or figure claims are in scope;
- output-automation status for promoted tables, figures, and in-text statistics;
- an interpretation brief when interpretation is in scope;
- a note brief when reporting is in scope;
- rerun or build metadata showing whether outputs are `rerun`, `inspected-only`, `inherited`, `structure-only`, or `unknown`; and
- a cross-language validation manifest only when explicitly requested or directly targeted.

If one of these surfaces is relevant and missing, surface that absence as a diagnostic gap rather than reading past it.

## Optional cross-language validation

Cross-language validation is useful but expensive. It is not a default review requirement.

Use `references/cross_language_validation_workflow.md` when the user explicitly requests cross-language validation.

Rules:

- `crosslang:no`: default; do not run or plan cross-language validation.
- `crosslang:plan`: prepare a separate validation handoff; do not pretend validation has been run.
- `crosslang:yes`: if a cross-language validation manifest or comparison outputs already exist, audit them; otherwise prepare a validation handoff.
- `crosslang:audit`: audit an existing validation manifest or comparison outputs; if absent, report the missing manifest and provide the handoff.

Cross-language validation scripts, if later created by a separate workflow, must not modify author code. `econ-review` can audit the manifest and comparison outputs, but reviewer agents must not create those scripts.

## Workflow

### Stage 0: Determine scope and route

Decide:

- domain mode (`empirical`, `hybrid`, or `software-handoff`);
- review tier;
- review surface;
- whether GitHub issue drafting or creation was requested;
- whether interpretation is in scope;
- whether a reader-facing note is in scope;
- whether cross-language validation is explicitly requested or directly targeted; and
- the current authority hierarchy.

In that hierarchy, old memos, exploratory reports, GPT bundles, and project briefs are leads unless they were explicitly reviewed or accepted for a defined purpose. Treat live project evidence and current review findings as stronger than old learning notes or intermediate writeups.

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
- sample-flow, merge, key, missingness, support, overlap, denominator, and weight diagnostics;
- the model-spec ledger when relevant;
- estimand/design/inference/horizon metadata when relevant;
- the output-consistency map when note-facing claims are in scope;
- output-automation status when outputs or in-text statistics are promoted;
- the interpretation brief when interpretation is in scope;
- the note brief when reporting is in scope;
- build info or rerun-status notes;
- the review bundle when present; and
- cross-language validation manifest/comparison outputs only when explicitly requested or directly targeted.

If a required diagnostic surface is missing, treat that absence as review evidence.

Before dispatch, build a compact evidence manifest for reviewers. Include:

- review target and surface;
- review tier;
- interpretation flag;
- cross-language validation state;
- current authority hierarchy;
- discovered plan, workflow note, bundle, outputs, checks, ledgers, briefs, maps, note paths, build metadata, and validation manifests;
- missing diagnostic surfaces;
- base ref or diff scope when relevant;
- rerun or build-status evidence when visible;
- known blind spots or unavailable files; and
- a `data_construction_evidence` block when the review touches raw-to-analysis construction, joins, filters, missingness, sample restrictions, supports, denominators, weights, or timing rules; and
- an `econometric_evidence` block when relevant.

The `data_construction_evidence` block should include known values and paths for source lineage, unit and keys, joins and merges, filters and drops, missingness, support and overlap, denominators and weights, timing alignment, intermediate outputs, manual steps, and rerun status. This block is the core evidence surface for cleaning-heavy work, even when no regression or inferential output exists.

The `econometric_evidence` block should include known values and paths for estimand, identification, sample, estimator, fixed effects, weights, inference, dynamics, robustness hierarchy, output automation, and cross-language validation. Do not invent values; unknown fields should remain missing or `unknown`.

Pass this evidence manifest to every reviewer prompt so child reviewers start from the same source map the parent found.

### Stage 2: Select the review panel

Always include:

- `provenance-auditor`; and
- `specification-auditor`.

For any surface other than `plan`, default the economist core to:

- `transformation-and-sample-auditor`; and
- `output-consistency-auditor`.

Add `claim-discipline-auditor` whenever interpretation is in scope. For `surface:note`, note-facing bundle review, and interpretation-bearing `surface:mixed`, it is compulsory.

Use the role matrix in `references/review_reference.md` for additional conditional reviewers such as estimation-practice, inference, output-perception, dynamics, design, robustness, reproducibility, software-equivalence, cross-language-validation, hybrid-implementation, or bundle review.

Special cross-language rule:

- If `crosslang:plan` is active and no validation manifest exists, the parent may prepare a cross-language validation handoff without spawning a large equivalence panel.
- If `crosslang:audit` is active or a cross-language validation manifest exists, include `cross-language-validation-auditor`; include `software-equivalence-auditor` when equivalence is being claimed.

Do not duplicate roles that are asking the same question.

Before dispatch, announce the selected reviewer roles, the review tier, and the cross-language validation state. This makes it visible whether the run is a compact plan review, a standard results review, a promotion-grade panel, or an opt-in validation audit.

### Stage 3: Spawn reviewer subagents

Spawn one custom reviewer agent per selected role in parallel and wait for all available reviewer agents before synthesis. Use the role-to-agent mapping in `references/review_reference.md`.

For each reviewer prompt, include:

- assigned role;
- review surface;
- interpretation flag;
- review tier;
- cross-language validation state;
- plan path, base ref, and target when present;
- evidence manifest from Stage 1;
- the relevant surface read order;
- the relevant method guardrails from the shared reviewer protocol when a method is visible;
- the JSON output contract from the shared reviewer protocol; and
- the instruction to return JSON only, with evidence-led findings, no raw logs, no file mutation, no artifact writes, no validation-script creation, and no issue updates.

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
- `Diagnostic gaps`;
- `Reader-facing note register` when relevant;
- `Cross-language validation handoff` when explicitly requested but not yet run; and
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

Run artefacts under `.context/econ-review/<run-id>/` are transient review records, not analytical evidence and not project memory. Durable review evidence belongs in the project plan, outputs, checks, review bundle, interpretation brief, note brief, approved project-backbone update, or explicit cross-language validation manifest.

Suggested artefacts:

- `findings.md`;
- `findings.json`;
- `applied_fixes.md`;
- `residual_work.md`; and
- `cross_language_validation_handoff.md` only when explicitly requested and not yet run.

### Stage 6: Reader-facing note gate

Whenever the target includes a note, note-facing bundle, or interpretation-bearing mixed surface, run this gate directly.

Check that:

1. the first paragraph tells the reader what the note studies, what the main answer is, and why the note exists;
2. the research object, sample boundary when empirical, estimand when relevant, and main comparison are defined before decompositions, benchmark bridges, or implementation details;
3. the main text can be understood without repo knowledge;
4. internal workflow nouns do not carry the main narrative;
5. figures appear in a sensible order, with the headline figure first;
6. benchmark material and heavy diagnostics are bounded rather than crowding the lead;
7. variable names, file paths, and wave IDs are not overused when ordinary economic language would do;
8. limitations are stated explicitly; and
9. causal, mechanism, policy, or extrapolative language does not outrun the verified object.

A note that reads like an execution log or opens from workflow machinery is at least a meaningful note-register problem even when the underlying results are sound.

### Stage 7: Optional cross-language validation handoff

When `crosslang:plan` is active, or `crosslang:yes` is active but no usable validation manifest exists, prepare a separate handoff using `references/cross_language_validation_workflow.md`.

The handoff should include:

- status: planned, not yet run;
- validation target outputs/tables/figures;
- baseline specification IDs and estimands;
- primary software and proposed comparison software;
- source data/input version;
- object parity checks;
- numeric comparison checks;
- tolerance and discrepancy classification rules;
- independence boundary: validation scripts do not modify author code;
- minimum expected output: `cross_language_validation_manifest.md` plus comparison tables.

Do not claim cross-language validation passed unless a manifest and comparison outputs were audited.

### Stage 8: Synthesize for the user

Always lead with findings.

Default output shape:

1. `Blocking before trust`;
2. `Worth checking before promotion`;
3. `Diagnostic gaps`;
4. `Reader-facing note register` when relevant;
5. `Cross-language validation handoff` when explicitly requested and not yet run;
6. `Documentation / cleanup`;
7. `Reusable review lesson` when relevant;
8. `Open questions`; and
9. `Artefact summary`.

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

Add `Reusable review lesson: none|closeout-only|econ-compound candidate` when the review reveals a possible economics research lesson. Use `none` as the compact default. Use `closeout-only` when the lesson is task-local and should stay in the review finding or residual summary. Good `econ-compound candidate` examples include repeated overclaiming from weak sources, a sample-accounting diagnostic that should become standard, a model-output equivalence rule, a manifest or handoff practice, or a note-facing claim-discipline rule. If the lesson is a candidate, provide the one-sentence lesson and evidence path so a later `econ-compound` run can write the durable note. Do not write durable learning notes from `econ-review` unless the user explicitly asked for learning capture.

If `issues:yes` was supplied or the user explicitly asked to file/draft GitHub issues:

- produce issue-ready follow-ups for retained findings whose fix class is `gated` or `manual`, or whose trust effect is `baseline-defining` or `promotion-blocking`;
- keep one issue per coherent empirical problem or implementation lane, not one issue per reviewer sentence;
- distinguish empirical problem, implementation fix, robustness extension, and note/paper follow-up;
- include objective, evidence surface, proposed done-when condition, and links to finding IDs;
- include affected labels when they help tie the issue to a plan decision, output, branch, or existing issue;
- create or update GitHub issues only after explicit approval, unless the user already directly asked for creation in the current request.

### Stage 9: Headless output envelope

In `mode:headless`, use the structured envelope in `references/review_reference.md`.

## When to ask the user

Ask rather than guessing when the live question is:

- whether to promote a result;
- whether to change the baseline;
- whether a divergence is decisive or merely descriptive;
- whether interpretation is in scope;
- whether a substantive note or memo should be rewritten;
- whether cross-language validation should be run rather than merely planned; or
- which comparison software should be used when the user requested cross-language validation but did not specify one.

If `request_user_input` is unavailable, ask concise numbered choices in chat, name the recommended conservative default, and wait for the user's answer when the decision changes trust, promotion, baseline, interpretation, or validation scope.

Do not ask for documentation-only cleanups, path repairs, missing manifest rows, or clearly safe bundle-hygiene fixes.

## Hard stops

- Do not mutate analytical content in safe auto-fix.
- Do not create or update GitHub issues unless the user requested or approved it.
- Do not treat GitHub issue text as analytical evidence without checking the actual plan, outputs, code, or bundle.
- Do not review a note in isolation from its evidence.
- Do not let reader-facing note failures disappear into generic copy-editing language.
- Do not treat numerical similarity alone as proof that two paths estimate the same analytical object.
- Do not silently turn ordinary review into cross-language validation.
- Do not let documentation-only gaps masquerade as baseline failures.
- Do not treat missing required diagnostic surfaces as harmless omissions.
