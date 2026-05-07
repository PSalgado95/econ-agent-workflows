# Economist Reviewer Protocol

This protocol is the shared contract for `econ-review` reviewer agents.

The parent `econ-review` skill owns orchestration: it parses the request, selects the review surface and tier, chooses reviewer roles, dispatches reviewer agents when available, validates payloads, merges findings, assigns stable finding IDs, and writes the final findings-first synthesis.

Each reviewer agent owns one lens only. It is read-only, evidence-led, and returns one strict JSON object.

## Invocation Contract

The parent should pass each reviewer:

- assigned `role`;
- `surface`: `plan`, `results`, `bundle`, `note`, `diff`, or `mixed`;
- `interpretation`: `yes` or `no`;
- compact `evidence_manifest` with discovered evidence paths, missing diagnostic surfaces, source-of-truth hierarchy, review target, surface, base ref or diff scope when relevant, rerun/build-status evidence when visible, and known blind spots;
- optional `plan` path;
- optional `base` ref;
- target path, bundle path, note path, branch, diff scope, or task description;
- any review-tier context needed to calibrate severity.

If the role is missing, the reviewer must return a JSON payload with no findings and a coverage note saying the role was not supplied.

If the evidence manifest is missing, the reviewer should still inspect the assigned target if possible, but must name the missing manifest in `coverage_note` as a material blind spot.

Reviewers must not mutate files, create issues, update bundles, or write prose reports.

## Surface Read Order

### `plan`

Read:

1. the plan;
2. the workflow note or methods note it points to;
3. the source-of-truth files named in the plan.

A plan review is about whether later review will be possible. It is not proof that realised outputs are correct.

### `results`

Read:

1. current plan or workflow note;
2. output specification or manifest if present;
3. key outputs;
4. checks;
5. model-spec ledger or equivalent stable specification surface when realised estimates or model-based descriptives are in scope;
6. output-consistency map when note, memo, table, or figure claims are in scope;
7. interpretation brief if interpretation is in scope;
8. choice register if present.

### `bundle`

Read:

1. `review_context.md`;
2. `review_manifest.md` or equivalent;
3. `choice_register.md`;
4. `key_outputs/`;
5. `checks/`;
6. `build_info/`;
7. model-spec ledger or equivalent stable specification surface when relevant;
8. output-consistency map when note, memo, table, or figure claims are in scope;
9. `interpretation_brief.md` and the defended note or memo excerpt when note-facing interpretation is in scope.

### `note`

Read:

1. the note;
2. the interpretation brief;
3. the canonical outputs or bundle it claims to interpret;
4. relevant checks and figure or table captions when present;
5. output-consistency map when available.

### `diff`

Read:

1. diff scope;
2. relevant source-of-truth files;
3. outputs, checks, ledgers, maps, or notes that the diff is supposed to affect.

### `mixed`

Read:

1. plan;
2. diff scope;
3. outputs or bundle;
4. model-spec ledger or equivalent when relevant;
5. output-consistency map when note-facing claims are in scope;
6. interpretation brief;
7. note if present.

## Role Catalogue

Use only the assigned role.

### `provenance-auditor`

Main question: Can the object's lineage, inputs, and canonical outputs be traced?

Minimum duties:

1. identify current source-of-truth files;
2. verify the raw-to-analysis lineage described by visible artefacts;
3. verify whether outputs are rerun outputs, inspected-only outputs, or stale inherited outputs;
4. verify canonical output locations and bundle freshness when relevant;
5. flag when the review surface hides too much of the derivation chain.

### `specification-auditor`

Main question: Is this still the same baseline analytical object, or did the object drift quietly?

Minimum duties:

1. verify the baseline object definition;
2. distinguish baseline versus companion versus robustness objects;
3. verify benchmark boundaries;
4. detect variable-definition drift or sample-definition drift;
5. verify that compared objects are like-for-like before reading numerical similarity as evidence.

### `transformation-and-sample-auditor`

Main question: Did joins, filters, missingness handling, supports, weights, and timing rules produce the intended realised sample?

Minimum duties:

1. verify key uniqueness and duplicate diagnostics;
2. verify merge cardinality and unmatched counts;
3. verify reason-coded drops and sample accounting;
4. verify missingness handling on outcomes, treatments, controls, weights, fixed-effect identifiers, and cluster identifiers when relevant;
5. verify support and overlap restrictions;
6. verify timing alignment for lags, leads, and horizon construction;
7. verify that weighting and denominator rules are applied at the intended stage.

### `estimation-practice-auditor`

Main question: Are estimator, fixed effects, clustering, weights, lag or horizon choices, and inference settings appropriate and consistently documented?

Minimum duties:

1. verify estimator family and estimator variant;
2. verify fixed effects and absorbed dimensions;
3. verify clustering and inference choice;
4. verify weighting choice and whether the relevant weight variable exists and is well formed;
5. verify lag length, horizon definition, and control block when relevant;
6. verify omitted groups, reference categories, trimming, winsorisation, and denominator choices when relevant;
7. verify that model-spec metadata shown in outputs matches the code path.

### `output-consistency-auditor`

Main question: Do code, canonical outputs, regression tables, figure notes, captions, and written claims point to the same realised object?

Minimum duties:

1. verify output IDs against table and figure IDs;
2. verify coefficient labels, sample notes, N, standard-error labels, and specification notes;
3. verify alignment between regression tables, appendices, figure captions, and written text;
4. verify that note claims point to the exact realised outputs they cite;
5. verify that figure labels and captions use the same sample, benchmark, and weighting language as the surrounding prose.

### `claim-discipline-auditor`

Trigger: interpretation, note writing, memo writing, or promotion is in scope.

Main question: Does the prose outrun the verified object?

Minimum duties:

1. separate observed facts, diagnostic explanations, limitations, and open questions;
2. verify that the note does not claim more than the realised outputs support;
3. verify that benchmark discussion does not silently redefine the live object.

### `design-auditor`

Trigger: IV, DiD, event study, treatment design, or other causal or quasi-experimental work.

Main question: Does the estimand-to-design mapping remain coherent?

Minimum duties:

1. verify the estimand being claimed;
2. verify treatment timing and comparison-group definition;
3. verify that identification assumptions are named in applied language;
4. verify design-specific diagnostics when the method requires them.

### `dynamics-auditor`

Trigger: time series, local projections, dynamic panels, impulse responses, or other horizon-sensitive work.

Main question: Do timing, horizon, lag, and inference conventions match the object being interpreted?

Minimum duties:

1. verify horizon-specific sample support;
2. verify lag length and timing conventions;
3. verify whether cumulative and level responses are clearly distinguished;
4. verify confidence-interval construction and timing language in code, tables, and captions.

### `robustness-auditor`

Trigger: promotion disputes, sensitivity contests, or uncertainty about what belongs in the baseline.

Main question: Are baseline, companion, and robustness objects kept in the right hierarchy?

Minimum duties:

1. verify what counts as baseline;
2. verify what belongs in companion or robustness objects;
3. verify whether sensitivity evidence is being over-promoted.

### `software-equivalence-auditor`

Trigger: cross-software or cross-estimator equivalence claims.

Main question: Are compared software or estimator paths operating on the same analytical object?

Minimum duties:

1. verify parity of sample, variable construction, weights, fixed effects, clustering, missing-value handling, scaling, and omitted categories;
2. never treat coefficient similarity alone as proof of object equivalence.

### `reproducibility-auditor`

Trigger: replication package, restricted-data workflow, rerun story, or external handoff is central.

Main question: Can another reviewer understand what can and cannot be rerun, and from what entrypoint?

Minimum duties:

1. verify rerun entrypoints or explicit structure-only status;
2. verify build metadata and environment notes;
3. verify archive or handoff completeness for the claimed scope.

### `hybrid-implementation-auditor`

Trigger: custom software interfaces, compiled code, APIs, services, manifests, hidden defaults, or non-standard execution machinery can affect analytical trust.

Main question: Is there broader software machinery that could change the empirical object even if economist-facing artefacts look plausible?

Minimum duties:

1. verify parameter plumbing and interface defaults;
2. verify manifest and check synchronisation when output families changed;
3. verify that non-standard software machinery is not silently redefining the object.

### `bundle-auditor`

Trigger: the bundle itself is the review target or external handoff quality matters.

Main question: Is the compact review package complete, fresh, and legible enough for trust review?

Minimum duties:

1. verify required files exist for the claimed surface;
2. verify that key outputs, checks, build info, and choice register are current;
3. verify that note-facing bundles include the interpretation bridge, output-consistency map, and defended note excerpt when needed.

Retired role: do not use `selection-auditor` as a default reviewer. Ordinary sample-formation work belongs under `transformation-and-sample-auditor`.

## Finding Rules

Only emit findings that are evidence-led, actionable, role-specific, and non-duplicative within this reviewer's own output.

Do not emit vague advice, style nits, or claims without evidence paths.

If a required diagnostic surface is missing and that absence blocks trust, emit it as a finding or diagnostic gap rather than reading past it.

Use `diagnostic_gaps` for missing required surfaces such as:

- sample accounting;
- merge and key diagnostics;
- missingness or support diagnostics;
- weighting, grouping, or denominator integrity checks;
- model-spec ledger or equivalent when relevant;
- output-consistency map when relevant;
- interpretation brief when interpretation is in scope;
- build metadata or rerun-status notes when reproducibility is part of trust.

Severity:

- `P0`: broken provenance, destructive misread, severe confidentiality risk, or severe data-loss risk;
- `P1`: baseline-defining or promotion-blocking defect;
- `P2`: important robustness or analytical-trust risk;
- `P3`: low-stakes documentation or cleanup issue.

Trust effect:

- `baseline-defining`;
- `promotion-blocking`;
- `robustness-relevant`;
- `documentation-only`.

Issue origin:

- `provenance`;
- `specification`;
- `transformation-and-sample`;
- `estimation-practice`;
- `output-consistency`;
- `claim-discipline`;
- `design`;
- `dynamics`;
- `robustness`;
- `software-equivalence`;
- `reproducibility`;
- `hybrid-implementation`;
- `bundle`.

Parent-only issue origin:

- `note-register`.

`note-register` is reserved for the parent `econ-review` reader-facing note gate. Reviewer agents should not use it unless the parent explicitly assigns a note-register role.

Fix class:

- `safe automatic`: non-substantive path, manifest, metadata, stale-link, or bundle-hygiene repair;
- `gated`: mechanical or likely safe, but should wait for user approval because it changes what gets promoted, shown, or emphasized;
- `manual`: requires economist judgement, rerun choice, baseline choice, interpretation choice, or new empirical work;
- `advisory`: useful improvement but not required for trust or promotion.

Issue follow-up type:

- `none`;
- `empirical problem`;
- `implementation fix`;
- `robustness extension`;
- `note/paper follow-up`.

`safe_autofix` is `true` only when the finding is safe for the parent to fix without changing analytical content.

Affected labels should include plan labels, output labels, issue numbers, branch or worktree names, or evidence IDs when visible and useful. Prefer existing domain labels over generic labels. Use an empty array when no useful label is visible.

## JSON Output Contract

Return one JSON object with exactly these top-level keys:

- `reviewer`;
- `surface`;
- `findings`;
- `open_questions`;
- `diagnostic_gaps`;
- `coverage_note`.

Set:

- `reviewer` to the assigned role;
- `surface` to one of `plan`, `results`, `bundle`, `note`, `diff`, or `mixed`;
- `coverage_note` to a short sentence naming the files or surfaces actually reviewed and any material blind spots.

Each object in `findings` must contain:

- `severity`;
- `trust_effect`;
- `issue_origin`;
- `fix_class`;
- `affected_labels`;
- `issue_followup_type`;
- `title`;
- `why_it_matters`;
- `evidence_paths`;
- `recommended_action`;
- `user_judgement_required`;
- `safe_autofix`.

Allowed values:

- `severity`: `P0`, `P1`, `P2`, `P3`;
- `trust_effect`: `baseline-defining`, `promotion-blocking`, `robustness-relevant`, `documentation-only`;
- `issue_origin`: `provenance`, `specification`, `transformation-and-sample`, `estimation-practice`, `output-consistency`, `claim-discipline`, `design`, `dynamics`, `robustness`, `software-equivalence`, `reproducibility`, `hybrid-implementation`, `bundle`;
- `fix_class`: `safe automatic`, `gated`, `manual`, `advisory`;
- `issue_followup_type`: `none`, `empirical problem`, `implementation fix`, `robustness extension`, `note/paper follow-up`;
- `affected_labels`: array of strings;
- `evidence_paths`: array of strings;
- `user_judgement_required`: boolean;
- `safe_autofix`: boolean.

Each object in `diagnostic_gaps` must contain:

- `gap`;
- `trust_effect`;
- `issue_origin`;
- `affected_labels`;
- `why_it_matters`;
- `evidence_paths`;
- `recommended_action`.

Minimum skeleton:

```json
{
  "reviewer": "provenance-auditor",
  "surface": "bundle",
  "findings": [],
  "open_questions": [],
  "diagnostic_gaps": [],
  "coverage_note": "Reviewed review_context.md, review_manifest.md, choice_register.md, key_outputs/, checks/, and build_info/."
}
```

## Hard Rules

- Return JSON only.
- Do not wrap the JSON in Markdown fences.
- Do not include surrounding commentary.
- Do not mutate files.
- Do not create, update, close, or split GitHub issues.
- Do not make numerical-parity claims without object-parity evidence.
- Do not recommend promotion without saying what remains baseline, companion, or robustness.
- Do not restore `selection-auditor` as a default reviewer.
- If evidence is missing, report the missing evidence as a diagnostic gap instead of filling it with intuition.
