---
name: econ-debug
description: "Diagnose an anomalous empirical or computational result — a sign flip, an observation-count cliff, an implausible magnitude, unexplained pre-trends, a failed check, a convergence failure — by tracing the full causal chain from cause to symptom before any fix. Use when the user says debug, my results look wrong, the coefficient flipped, N dropped, why is this number, this can't be right, or diagnose an estimate. Not for planning (econ-plan), not for review or trust verdicts (econ-review), and not for pure software debugging with no research object — route a broken build, failing unit test, or app bug with no estimate, sample, or output at stake to compound-engineering's ce-debug."
---

# Economist Debugging Workflow

Find why a research number is wrong, then fix it. The object under investigation is a research result — an estimate, a realised sample, a diagnostic, a computed model object — not application code. This file is the contract; it adapts the ce-debug diagnosis loop to research anomalies.

## Core principles

- **Investigate before fixing.** No fix until the full causal chain from cause to symptom is explained with no gaps (the iron rule below).
- **One change at a time.** Test one hypothesis and change one thing. Changing several things "to see what helps" hides which change mattered and is how a symptom patch masquerades as a cause.
- **Observed beats assumed.** Assumed values lie; a printed count, a `describe`, or a boundary check does not. Ground every hypothesis in something you actually observed.
- **When stuck, diagnose why.** After two or three exhausted hypotheses, stop and read the pattern — different subsystems implicated, contradictory evidence, an environment or vintage mismatch — rather than trying harder along the same line.

## Trigger

Invoke on an anomalous empirical or computational output: a sign flip against theory or a prior run, an observation-count cliff, an implausible magnitude, unexplained pre-trends, a broken identity or accounting residual, a convergence or feasibility failure, a failed object-defining check, or a plain "this number can't be right". If the request is a pure software fault with no estimate, sample, or output at stake, hand it to the Compound Engineering debug skill (`compound-engineering:ce-debug` when available) and stop.

## Iron rule

Investigate before fixing. Do not apply, propose, or commit any fix until the full causal chain from cause to symptom is explained with no gaps. "Somehow the merge inflates the coefficient" is a gap, not a chain. A fix that changes the number without a gap-free chain is a symptom patch: the real cause is still live, and the next run will surprise you again.

## Diagnose-then-fix gate

Once the root cause is confirmed, present the diagnosis before touching anything:

- the causal chain from cause to symptom, with the file, line, or output cell each step cites;
- the proposed fix and which files or specifications it changes;
- the minimal reproduction and the checks that will refresh after the fix;
- whether an existing check should have caught this, and why it did not.

Then ask (blocking) how to proceed. Offer, at minimum:

- **Fix it now** — proceed to the fix and the post-fix audit refresh below;
- **Diagnosis only** — stop after the written diagnosis; make no edit. This is a real end state, not a fallback: the researcher may want to own the fix;
- **Rethink the design** — when the root cause is a wrong baseline, estimand, sample rule, or benchmark rather than a slip, route to `econ-plan` (see Exits).

Default to no edit until the researcher chooses. In an autonomous parent run where no answer can be collected, stay diagnosis-only and return the recommended fix to the parent rather than applying it silently.

## Assumption audit

Before forming hypotheses, list every "this must be true" belief the surprising output rests on, and mark each **verified** (you read the code, checked the state, or ran it) or **assumed**. Most stuck debugging is a correct hypothesis tested against a wrong assumption. Cover at least:

- the **sample rule** — which rows the active filter actually keeps, and whether it matches the intended population;
- **merge cardinality** — one-to-one, one-to-many, or many-to-many, and whether a silent many-to-many inflated the panel;
- **weights** — which weight is applied, whether it is the intended one, and whether any step drops or renormalises it;
- **timing** — event, treatment, and reference dates; period alignment; lead/lag construction;
- **estimator settings** — fixed effects, clustering level, absorbed terms, reference category, optimiser tolerances, standardisation;
- **data vintage** — which extract, build, or version produced the inputs, and whether it is the one you think.

Verify cheapest-first: a one-line count or a `describe` before a full rerun.

## Hypotheses

Rank hypotheses by likelihood. Each must carry a concrete testable prediction — something in another slice of the data or code that must also hold if the hypothesis is right. For example: "if the merge duplicated firms, the raw panel row count exceeds the register firm count by roughly the number of duplicated keys"; or "if the sign flip is an omitted reference-category change, dropping the new control returns the old sign". A prediction that fails while the fix appears to work means you found a symptom. When the chain is obvious and gapless (a mis-typed variable, a filter with a flipped inequality), the chain explanation is itself the gate — no prediction ritual.

## Escalation by research subsystem

Localise the anomaly to the subsystem that produced it, then investigate there:

- **data construction** → transformation and sample diagnostics: recompute row counts before and after each merge and filter, missingness and support, key uniqueness, denominator and weight construction.
- **specification or estimation** → the model specification and estimator settings: fixed effects, clustering, absorbed terms, reference categories, standardisation, optimiser tolerances, and whether the realised specification matches the intended one.
- **software convention** → cross-package defaults: a default that differs between Stata, R, Python, or a solver (degrees-of-freedom corrections, small-sample adjustments, base levels, NA handling, integer vs float division). Reach for the `software-equivalence` lens — rebuild the disputed object in a second language and compare — when a convention gap is plausible.
- **genuine economics** → the number may be real and surprising. Do not fix it away: write a surprise memo and return the evidence boundary and next research decision to the user.

If two or three hypotheses point at different subsystems and none confirms, that divergence is itself a signal that the problem is a design choice, not a localised slip — route to `econ-plan` rather than forcing a fix.

## Reproduce minimally

Build a minimal script that reproduces the anomaly on the smallest input that still shows it — one merge, one estimator call, one slice — and keep it. Run it before the fix (it must reproduce) and after (it must be gone for the stated reason). After fixing, refresh every audit the change touches: sample counts, missingness, merge diagnostics, and any object-defining check on the affected output family. A fix that leaves stale audits behind is not closed.

## Questions

Asking a good blocking question is part of the job, not an interruption. Use the platform's blocking-question tool (`request_user_input`; the Claude build translates it), not plain chat text. Ask whenever the anomaly could be intended behaviour rather than a bug — a deliberate baseline choice, a sample restriction the researcher imposed on purpose, a benchmark defined a particular way. Ask one decision per question, with the context that makes it answerable: what the choice affects, the plausible readings with their consequences, and a recommended conservative default. Ask as many separate questions as the anomaly warrants; there is no question budget. Never present a genuine judgement call as a multiple-choice menu, and never bury it in a summary.

## Exits

- **Fix applied** → hand the changed surface to a targeted `econ-review` scoped to what changed (the edited script, the refreshed outputs, the affected audits), not a full re-review.
- **Design problem discovered** → the anomaly is a wrong baseline, estimand, sample definition, or benchmark, not a coding slip. Route back to `econ-plan`; a fix cannot repair a definition.
- **Genuine surprising finding** → the number is real. Route to the surprise-memo path in `econ-work`: write the memo (HTML via `econ-html-memo` when installed, plain standalone HTML under the same content discipline otherwise), state the minimal validation and open explanation, and ask only for the research decision or local check needed to continue.

## Hard stops

- Do not apply or propose a fix before the full causal chain from cause to symptom is explained with no gaps.
- Do not fix a number without first reproducing it minimally, and do not close without refreshing the sample counts, missingness, and merge diagnostics the change touched.
- Do not "fix away" a result that is actually a genuine, correctly computed finding — write the surprise memo and report it locally instead.
- Do not treat an intended baseline or a deliberate sample restriction as a bug — when in doubt, ask first.
- Do not change more than one thing at a time while hunting the cause; shotgun edits hide which change mattered.
- Do not route a pure software fault with no research object here; it belongs to `compound-engineering:ce-debug`.
