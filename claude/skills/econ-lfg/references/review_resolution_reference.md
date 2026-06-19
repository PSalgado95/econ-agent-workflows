<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources (skills/, .codex/agents/, references/) and run build_claude.py. -->

# Econ LFG Review Resolution Reference

Use this reference during `econ-lfg` Stage 4 after `econ-review` returns retained findings. Review findings are evidence for the loop; they are not orders to change the research object.

## Classification Inputs

For every retained finding, inspect these fields before choosing a route:

- finding ID;
- fix class: `safe automatic`, `gated`, `manual`, or `advisory`;
- trust effect or promotion effect;
- issue origin;
- affected labels, such as plan labels, output IDs, bundle IDs, branch/worktree names, or evidence IDs;
- evidence path and whether the evidence path is strong enough to act on;
- missing diagnostic surfaces, if any;
- whether the finding conflicts with a researcher-anchored, plan-backed, agent-owned, or execution-discovered choice.

If a finding has no evidence path, do not act on it unless the issue is a visible bundle-metadata gap. Treat unsupported findings as degraded or advisory and record that limitation in the closeout.

## Canonical Route Tokens

Use these route tokens exactly in the review-resolution closeout:

| Route token | Use when | Typical examples |
| --- | --- | --- |
| `fix-now` | The fix is mechanical, safe automatic, or missing work already required by the saved plan, and it does not touch the Pedro-level trigger list. | Path repair, stale cross-reference, missing metadata, stale bundle manifest, validator rerun, missing diagnostic already required by the plan. |
| `revise-plan-choice` | Review evidence shows an agent-owned plan or work default should change, and the better path remains inside the initial task intent. | Diagnostic order, figure priority, note framing, implementation route, wording that narrows a claim to accepted evidence. |
| `ask-user` | The fix touches the Pedro-level trigger list or would override a researcher-anchored choice. | Baseline, sample, estimand, identification, benchmark treatment, output promotion, claim budget, substantive interpretation. |
| `defer-with-rationale` | The finding is legitimate but outside the prompt, not needed for trust in the requested output, or better handled as follow-up work. | Optional robustness extension, future package audit, non-blocking broader cleanup. |
| `advisory-only` | The finding is useful context but does not affect trust, promotion, or the requested output. | FYI note, non-blocking ergonomics suggestion, future wording improvement. |

## Mapping From econ-review Fix Classes

- `safe automatic` usually maps to `fix-now`, unless the authority test shows the edit would change a Pedro-level choice.
- `gated` maps to `ask-user` when it changes what gets promoted, shown, emphasized, or treated as the main output. If it is outside the requested output, map it to `defer-with-rationale`.
- `manual` usually maps to `ask-user`. It may map to `fix-now` only when the missing work is already required by the saved plan, the needed inputs and rerun authority are present, and no Pedro-level trigger is touched.
- `advisory` maps to `advisory-only` or `defer-with-rationale`.

Choose the more conservative route when fix class, trust effect, and authority source disagree.

## What Claude Code May Fix Without Asking Pedro

Claude Code may fix directly when the finding stays inside the saved plan, the initial prompt, and the current authority hierarchy:

- path repairs;
- stale cross-references;
- stale or missing metadata;
- stale or missing bundle manifests;
- missing choice-register rows when the decision is explicit elsewhere;
- package file-list or zip membership checks when already in scope;
- validators, tests, or checks named by the plan, work closeout, or review finding;
- output-consistency repairs that align labels, wording, manifests, or citations with already accepted evidence without changing the claim budget;
- missing diagnostic surfaces already required by the saved plan, when the inputs and rerun authority are present;
- agent-owned planning or work defaults, such as diagnostic order, figure priority, note framing, implementation route, or review-bundle organisation.

Each direct fix must leave a compact trace: finding ID, evidence path, route token, fix performed, verification run, and targeted re-review surface.

## Pedro-Level Trigger List

Pause for Pedro when the finding or proposed fix would change any of these:

- research question or decision problem;
- estimand or descriptive target;
- identification strategy;
- baseline specification;
- sample boundary, source universe, inclusion or exclusion rule, or variable definition;
- benchmark treatment or comparison target;
- estimator, inference, weighting, clustering, timing, horizon, or robustness hierarchy when it changes the research object;
- main output family or output promotion;
- note scope, claim budget, or substantive interpretation;
- destructive overwrite, expensive rerun, access-sensitive action, or external handoff decision.

These are decision blockers even when the review finding is persuasive. A review finding can justify presenting the decision clearly; it cannot itself decide the economics.

When pausing, return the finding ID, evidence path, affected labels, recommended conservative path, decision memo path when one was written, and exact resume prompt or command.

## Decision Memo Protocol

For any non-trivial `ask-user` blocker, write an economist-facing HTML decision memo before asking Pedro to decide.

When the installed runtime provides them, prefer these skills:

- `econ-html-memo` for restrained HTML memo structure, source/output traceability, document-shaped layout, and validation;
- `econ-writing` for economist-facing prose discipline.

If those skills are unavailable, use this fallback contract instead of failing:

- write a restrained HTML document, not a dashboard;
- open with the economic decision, not with process;
- separate what the review/output evidence shows from what each choice would mean;
- avoid software-developer jargon, PR/CI/deploy language, and agent-process narration;
- include compact tables only when they clarify the alternatives;
- keep claims within the evidence.

The memo must say:

- what decision arose;
- which review findings, outputs, diagnostics, or evidence paths created the decision;
- why the finding is a Pedro-level choice rather than an agent-owned cleanup;
- what the agent recommends as the conservative path and why;
- what changes under each plausible choice;
- what stays unchanged under each choice;
- what the agent will do next once Pedro decides;
- the exact prompt or command needed to resume the `econ-lfg` loop.

Output location:

- if the saved plan names a memo, note, or output directory, write the memo there;
- otherwise write to `docs/decision-memos/<YYYY-MM-DD>-<slug>.html` under the current task workspace;
- treat the repo containing `skills/econ-lfg/SKILL.md` as a package/source repo, not a runtime memo destination, unless the user's research task is explicitly about this package repo.

For trivial one-question blockers with no evidence synthesis needed, the agent may ask directly. Do not use that exception for baseline, sample, estimand, identification, benchmark, promotion, claim-budget, or interpretation decisions.

## Re-Review and Closeout

After `fix-now` or `revise-plan-choice`, run targeted `econ-review` on the changed or previously problematic surface. Cite the fixed finding IDs, changed paths, changed output or bundle labels, and prior evidence paths.

Escalate from targeted to broader review only when the revision changes the baseline, sample, estimand, specification, inference, benchmark treatment, note argument, primary output family, or another Pedro-level research-object boundary.

Repeat review resolution until:

- no blocking or worth-fixing findings remain;
- remaining findings are `defer-with-rationale` or `advisory-only`;
- a Pedro-level decision blocks the loop;
- external access or missing data prevents meaningful progress.

The final closeout must list fixed finding IDs, deferred/advisory finding IDs, decision memo path if one was written, targeted re-review result, verification performed, remaining risk, and resume route if blocked.
