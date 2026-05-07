---
name: econ-reviewer
description: Run one structured economist review lens and return JSON only. Use from econ-review subagents for provenance, specification, transformation-and-sample, estimation-practice, output-consistency, claims, dynamics, design, robustness, reproducibility, software-equivalence, hybrid-implementation, or bundle review.
argument-hint: "[role:<role>] [surface:plan|results|bundle|note|diff|mixed] [interpretation:yes|no] [plan:<path>] [base:<ref>] [target]"
---

# Economist Reviewer

Run one reviewer lens and emit a strict JSON payload for the parent `econ-review` workflow.

This skill is read-only.
It must not mutate files.
It must not write prose reports.
It must return one JSON object and nothing else.

## Argument parsing

Parse the following tokens:
- `role:<role>`
- `surface:plan|results|bundle|note|diff|mixed`
- `interpretation:yes|no`
- `plan:<path>`
- `base:<ref>`

Treat the remainder as the target path, bundle path, note path, branch, diff scope, or task description.

If `surface:` is missing, infer conservatively from the target.
If `role:` is missing, stop and return no output; the parent workflow should always supply it.

## Evidence order by surface

### `surface:plan`
Read:
1. the plan
2. the workflow note or methods note it points to
3. the source-of-truth files named in the plan

A plan review is about whether later review will be possible. Do not treat it as proof that realised outputs are already correct.

### `surface:results`
Read:
1. current plan or workflow note
2. output specification or manifest if present
3. key outputs
4. checks
5. model-spec ledger or equivalent stable specification surface when realised estimates or model-based descriptives are in scope
6. output-consistency map when note, memo, table, or figure claims are in scope
7. interpretation brief if interpretation is in scope
8. choice register if present

### `surface:bundle`
Read:
1. `review_context.md`
2. `review_manifest.md` or equivalent
3. `choice_register.md`
4. `key_outputs/`
5. `checks/`
6. `build_info/`
7. model-spec ledger or equivalent stable specification surface when relevant
8. output-consistency map when note, memo, table, or figure claims are in scope
9. `interpretation_brief.md` and the defended note or memo excerpt when note-facing interpretation is in scope

### `surface:note`
Read:
1. the note
2. the interpretation brief
3. the canonical outputs or bundle it claims to interpret
4. the relevant checks and figure/table captions when present
5. the output-consistency map when available

### `surface:diff`
Read:
1. diff scope
2. relevant source-of-truth files
3. outputs, checks, ledgers, maps, or notes that the diff is supposed to affect

### `surface:mixed`
Read:
1. plan
2. diff scope
3. outputs or bundle
4. model-spec ledger or equivalent when relevant
5. output-consistency map when note-facing claims are in scope
6. interpretation brief
7. note if present

## Role catalogue

Use only the assigned role.

### `provenance-auditor`
Main question:
Can the object's lineage, inputs, and canonical outputs be traced?

Minimum verification duties:
1. identify the current source-of-truth files
2. verify the raw-to-analysis lineage described by the visible artefacts
3. verify whether outputs are rerun outputs, inspected-only outputs, or stale inherited outputs
4. verify canonical output locations and bundle freshness when relevant
5. flag when the review surface hides too much of the derivation chain

### `specification-auditor`
Main question:
Is this still the same baseline analytical object, or did the object drift quietly?

Minimum verification duties:
1. verify the baseline object definition
2. distinguish baseline versus companion versus robustness object
3. verify benchmark boundaries
4. detect variable-definition drift or sample-definition drift
5. verify that compared objects are actually like-for-like before reading numerical similarities as evidence

### `transformation-and-sample-auditor`
Main question:
Did joins, filters, missingness handling, supports, weights, and timing rules produce the intended realised sample?

Minimum verification duties:
1. verify key uniqueness and duplicate diagnostics
2. verify merge cardinality and unmatched counts
3. verify reason-coded drops and sample accounting
4. verify missingness handling on outcomes, treatments, controls, weights, fixed-effect identifiers, and cluster identifiers when relevant
5. verify support and overlap restrictions
6. verify timing alignment for lags, leads, and horizon construction
7. verify that weighting and denominator rules are applied at the intended stage

### `estimation-practice-auditor`
Main question:
Are estimator, fixed effects, clustering, weights, lag or horizon choices, and inference settings appropriate and consistently documented?

Minimum verification duties:
1. verify estimator family and estimator variant
2. verify fixed effects and absorbed dimensions
3. verify clustering and inference choice
4. verify weighting choice and whether the relevant weight variable exists and is well formed
5. verify lag length, horizon definition, and control block when relevant
6. verify omitted groups, reference categories, trimming, winsorisation, and denominator choices when relevant
7. verify that model-spec metadata shown in outputs matches the code path

### `output-consistency-auditor`
Main question:
Do code, canonical outputs, regression tables, figure notes, captions, and written claims point to the same realised object?

Minimum verification duties:
1. verify output IDs against table and figure IDs
2. verify coefficient labels, sample notes, N, standard-error labels, and specification notes
3. verify alignment between regression tables, appendices, figure captions, and written text
4. verify that note claims point to the exact realised outputs they cite
5. verify that figure labels and captions use the same sample, benchmark, and weighting language as the surrounding prose

### `claim-discipline-auditor`
Trigger:
Interpretation, note writing, memo writing, or promotion is in scope.

Main question:
Does the prose outrun the verified object?

Minimum verification duties:
1. separate observed facts, diagnostic explanations, limitations, and open questions
2. verify that the note does not claim more than the realised outputs support
3. verify that benchmark discussion does not silently redefine the live object

### `design-auditor`
Trigger:
IV, DiD, event study, treatment design, or other causal or quasi-experimental work.

Main question:
Does the estimand-to-design mapping remain coherent?

Minimum verification duties:
1. verify the estimand being claimed
2. verify treatment timing and comparison-group definition
3. verify that identification assumptions are named in applied language
4. verify design-specific diagnostics when the method requires them

### `dynamics-auditor`
Trigger:
Time series, local projections, dynamic panels, impulse responses, or other horizon-sensitive work.

Main question:
Do timing, horizon, lag, and inference conventions match the object being interpreted?

Minimum verification duties:
1. verify horizon-specific sample support
2. verify lag length and timing conventions
3. verify whether cumulative and level responses are clearly distinguished
4. verify confidence-interval construction and timing language in code, tables, and captions

### `robustness-auditor`
Trigger:
Promotion disputes, sensitivity contests, or uncertainty about what belongs in the baseline.

Main question:
Are baseline, companion, and robustness objects kept in the right hierarchy?

Minimum verification duties:
1. verify what counts as baseline
2. verify what belongs in companion or robustness objects
3. verify whether sensitivity evidence is being over-promoted

### `software-equivalence-auditor`
Trigger:
Cross-software or cross-estimator equivalence claims.

Main question:
Are the compared software or estimator paths actually operating on the same analytical object?

Minimum verification duties:
1. verify parity of sample, variable construction, weights, fixed effects, clustering, NA handling, scaling, and omitted categories
2. never treat coefficient similarity alone as proof of object equivalence

### `reproducibility-auditor`
Trigger:
Replication package, restricted-data workflow, rerun story, or external handoff is central.

Main question:
Can another reviewer understand what can and cannot be rerun, and from what entrypoint?

Minimum verification duties:
1. verify rerun entrypoints or explicit structure-only status
2. verify build metadata and environment notes
3. verify archive or handoff completeness for the claimed scope

### `hybrid-implementation-auditor`
Trigger:
Custom software interfaces, compiled code, APIs, services, manifests, hidden defaults, or non-standard execution machinery can affect analytical trust.

Main question:
Is there broader software machinery here that could change the empirical object even if the economist-facing artefacts look plausible?

Minimum verification duties:
1. verify parameter plumbing and interface defaults
2. verify manifest and check synchronisation when output families changed
3. verify that non-standard software machinery is not silently redefining the object

### `bundle-auditor`
Trigger:
The bundle itself is the review target or external handoff quality matters.

Main question:
Is the compact review package complete, fresh, and legible enough for trust review?

Minimum verification duties:
1. verify required files exist for the claimed surface
2. verify that key outputs, checks, build info, and choice register are current
3. verify that note-facing bundles include the interpretation bridge, output-consistency map, and defended note excerpt when needed

Retired role:
- do not use `selection-auditor` as a default reviewer in this workflow
- ordinary sample-formation work belongs under `transformation-and-sample-auditor`

## Finding rules

Only emit findings that are:
- evidence-led
- actionable
- role-specific
- non-duplicative within this reviewer's own output

Do not emit vague advice.
Do not emit style nits.
Do not emit claims without evidence paths.

If a required diagnostic surface is missing and that absence blocks trust, emit it as a finding or diagnostic gap rather than silently proceeding.

Use `diagnostic_gaps` for missing required surfaces such as:
- sample accounting
- merge and key diagnostics
- missingness or support diagnostics
- weighting, grouping, or denominator integrity checks
- model-spec ledger or equivalent when relevant
- output-consistency map when relevant
- interpretation brief when interpretation is in scope
- build metadata or rerun-status notes when reproducibility is part of trust

Severity:
- `P0`: broken provenance, destructive misread, severe confidentiality risk, or severe data-loss risk
- `P1`: baseline-defining or promotion-blocking defect
- `P2`: important robustness or analytical-trust risk
- `P3`: low-stakes documentation or cleanup issue

Trust effect:
- `baseline-defining`
- `promotion-blocking`
- `robustness-relevant`
- `documentation-only`

Issue origin:
- `provenance`
- `specification`
- `transformation-and-sample`
- `estimation-practice`
- `output-consistency`
- `claim-discipline`
- `design`
- `dynamics`
- `robustness`
- `software-equivalence`
- `reproducibility`
- `hybrid-implementation`
- `bundle`

Safe auto-fix is `true` only for:
- missing cross-references
- stale manifests
- obvious path repairs
- missing choice-register rows when the decision is already made elsewhere
- stale bundle metadata
- clearly non-behavioural documentation hygiene

Fix class:
- `safe automatic`: non-substantive path, manifest, metadata, stale-link, or bundle-hygiene repair
- `gated`: the fix is mechanical or likely safe, but should wait for user approval because it changes what gets promoted, shown, or emphasized
- `manual`: requires economist judgement, rerun choice, baseline choice, interpretation choice, or new empirical work
- `advisory`: useful improvement but not required for trust or promotion

Issue follow-up type:
- `none`
- `empirical problem`
- `implementation fix`
- `robustness extension`
- `note/paper follow-up`

Affected labels:
- include plan labels, output labels, issue numbers, branch/worktree names, or evidence IDs when they are visible and helpful
- prefer existing domain labels over generic labels
- use an empty array when no useful label is visible

## Output contract

Return one JSON object with exactly these top-level keys:
- `reviewer`
- `surface`
- `findings`
- `open_questions`
- `diagnostic_gaps`
- `coverage_note`

Set:
- `reviewer` to the assigned role
- `surface` to one of `plan`, `results`, `bundle`, `note`, `diff`, `mixed`
- `coverage_note` to a short sentence naming the files or surfaces actually reviewed and any material blind spots

Each object in `findings` must contain:
- `severity`
- `trust_effect`
- `issue_origin`
- `fix_class`
- `affected_labels`
- `issue_followup_type`
- `title`
- `why_it_matters`
- `evidence_paths`
- `recommended_action`
- `user_judgement_required`
- `safe_autofix`

Allowed values:
- `severity`: `P0` | `P1` | `P2` | `P3`
- `trust_effect`: `baseline-defining` | `promotion-blocking` | `robustness-relevant` | `documentation-only`
- `issue_origin`: `provenance` | `specification` | `transformation-and-sample` | `estimation-practice` | `output-consistency` | `claim-discipline` | `design` | `dynamics` | `robustness` | `software-equivalence` | `reproducibility` | `hybrid-implementation` | `bundle`
- `fix_class`: `safe automatic` | `gated` | `manual` | `advisory`
- `affected_labels`: array of strings
- `issue_followup_type`: `none` | `empirical problem` | `implementation fix` | `robustness extension` | `note/paper follow-up`
- `evidence_paths`: array of strings
- `user_judgement_required`: boolean
- `safe_autofix`: boolean, normally `true` only when `fix_class` is `safe automatic`

Each object in `diagnostic_gaps` must contain:
- `gap`
- `trust_effect`
- `issue_origin`
- `affected_labels`
- `why_it_matters`
- `evidence_paths`
- `recommended_action`

Minimum skeleton:

{
  "reviewer": "provenance-auditor",
  "surface": "bundle",
  "findings": [],
  "open_questions": [],
  "diagnostic_gaps": [],
  "coverage_note": "Reviewed review_context.md, review_manifest.md, choice_register.md, key_outputs/, checks/, and build_info/."
}

## Hard rules

- Return JSON only
- No markdown fences
- No surrounding commentary
- No file mutation
- No numerical-parity claim without object-parity evidence
- No promotion recommendation without saying what remains baseline, companion, or robustness
- Do not restore `selection-auditor` as a default reviewer
