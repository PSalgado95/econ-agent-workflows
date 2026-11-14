<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources and run build_claude.py. -->

# Econ LFG Review Resolution Reference

Use this reference during `econ-lfg` Stages 3 to 5: to brief the single
reviewer, to judge which of its findings hold, and to route and record them.
Review findings are evidence for the loop; they are not orders to change the
research object.

## Reviewer brief

Send the reviewer this brief, filled in, as its whole prompt. It has no other
context, so every path is absolute and every settled choice is stated.

```md
mode: single-reviewer

You are the one independent reviewer of finished economics work. Read
<absolute path to econ-review/SKILL.md> and follow its "Single-reviewer mode"
section: stance, boundary, and return format.

- Research question:
- Deliverable and its reader:
- Settled choices (researcher-anchored or plan-backed). Do not reopen them as
  ordinary findings; challenge one only through a finding marked
  "Needs the researcher: yes":
- Evidence to read, with paths: saved plan; code entrypoints; realised outputs
  (tables, figures, logs); note or memo; execution record:
- Regenerated in this run versus only inspected:
- Re-review only: earlier findings, what was done about each, changed paths:

Read only. Start no other agents. Return only the review, in the stated format.
```

## Judging whether a finding holds

For every finding `R<n>`, inspect the decisive evidence yourself before acting:
the cited code, definitions, tables, figures, or outputs, with their context and
the settled decisions. A finding holds when that evidence supports it and it
changes the result or how it should be read. A finding without usable evidence
does not hold unless you can confirm it from the cited surface. Low reviewer
confidence calls for a closer check, not automatic rejection; high confidence
does not replace the check. When you reject a finding, record the evidence that
contradicts it.

For every "Not inspected" entry that could change the conclusion, treat the gap
like a finding: produce the evidence when the plan already requires it and the
inputs and authority are present, otherwise route it and keep it visible.

## Canonical Route Tokens

Use these route tokens exactly in the review-resolution record:

| Route token | Use when | Typical examples |
| --- | --- | --- |
| `fix-now` | The finding holds, the fix is mechanical or work the saved plan already requires, and it does not touch the researcher-level trigger list. | Coding error in a defined variable, path repair, stale cross-reference, mislabelled table, missing diagnostic already required by the plan, claim wording that overstates accepted evidence. |
| `revise-plan-choice` | The finding holds and shows an agent-owned plan or work default should change, and the better path remains inside the initial task intent. | Diagnostic order, figure priority, note framing, implementation route. |
| `ask-user` | The finding holds and its fix touches the researcher-level trigger list, overrides a researcher-anchored choice, or the reviewer marked it "Needs the researcher: yes" and you agree. | Baseline, sample, estimand, identification, benchmark treatment, output promotion, claim budget, substantive interpretation. |
| `defer-with-rationale` | The finding holds but is outside the prompt, not needed for trust in the requested output, or better handled as follow-up work. | Extension beyond the requested output, broader package audit. |
| `advisory-only` | The point is useful context but does not change the result or its reading. | Future wording improvement. |
| `rejected` | The finding does not hold on the evidence. | The cited line does not do what the finding says; the concern is already handled elsewhere. |

When the reviewer's "Needs the researcher" flag and the trigger list disagree,
take the more conservative route.

## What the Agent May Fix Without Asking

The agent may fix directly when the finding stays inside the saved plan, the initial prompt, and the current authority hierarchy:

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

Each direct fix must leave a compact trace: `R<n>` ID, the evidence you
checked, route token, fix performed, changed path, verification run, and
re-review surface.

## Researcher-Level Trigger List

Pause when the finding or proposed fix would make a new choice about, or override existing authority on, any of these:

- research question or decision problem;
- estimand or descriptive target;
- identification strategy;
- baseline specification;
- sample boundary, source universe, inclusion or exclusion rule, or variable definition;
- benchmark treatment or comparison target;
- estimator, inference, weighting, clustering, timing, horizon, or robustness hierarchy when it changes the research object;
- main output family or output promotion;
- note scope, claim budget, or substantive interpretation;
- destructive overwrite, expensive rerun, access-sensitive action, or release/sharing decision.

Restoring an explicitly agreed definition after an evidenced implementation error is not a new definition choice: it may be `fix-now` when the plan requires that correction, the necessary inputs and rerun authority are present, and the correction is verified and re-reviewed. A changed estimate alone does not settle an ambiguous intended definition. New or conflicting research choices remain decision blockers even when the review finding is persuasive. A review finding can justify presenting the decision clearly; it cannot itself decide the economics.

When pausing, return the finding ID, evidence path, affected labels, recommended conservative path, decision memo path when one was written, and exact resume prompt or command.

## Decision Memo Protocol

For an `ask-user` blocker that needs evidence synthesis, write an economist-facing decision memo before asking, using HTML unless the user requests another format. Reuse a suitable existing memo. For a single clear decision that can be explained with its evidence and consequences in a short question, ask directly; do not create a document just to obtain permission. A write-access failure must not prevent stating the decision and evidence in chat.

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
- why the finding is a researcher-level choice rather than an agent-owned cleanup;
- what the agent recommends as the conservative path and why;
- what changes under each plausible choice;
- what stays unchanged under each choice;
- what the agent will do next once the researcher decides;
- the exact prompt or command needed to resume the `econ-lfg` loop.

Output location:

- if the saved plan names a memo, note, or output directory, write the memo there;
- otherwise write to `docs/decision-memos/<YYYY-MM-DD>-<slug>.html` under the current task workspace;
- treat the repo containing `skills/econ-lfg/SKILL.md` as a package/source repo, not a runtime memo destination, unless the user's research task is explicitly about this package repo.

The need for a memo depends on the evidence synthesis and trade-offs, not only on the name of the decision. Default to a memo when the decision concerns identification, the estimand, or the sample definition and would change the headline result; ask directly when the choice is binary and its evidence fits in one paragraph. Researcher-owned choices still require an answer before the affected branch proceeds.

## Re-Review and Closeout

After `fix-now` or `revise-plan-choice`, start a new single reviewer on the
changed or previously problematic surfaces, with the re-review line of the brief
filled in: each earlier finding, what was done about it, and the changed paths.

Widen the re-review beyond the changed surfaces only when the revision changes
the baseline, sample, estimand, specification, inference, benchmark treatment,
note argument, primary output family, or another researcher-level boundary of
the research object.

Repeat review resolution until:

- no finding that holds and changes the result or its reading remains unaddressed;
- remaining findings are `defer-with-rationale`, `advisory-only`, or `rejected`;
- a researcher-level decision blocks the loop;
- external access or missing data prevents meaningful progress.

The final closeout lists every `R<n>` with its route and outcome (fixed,
deferred, advisory, rejected with reason, or awaiting the researcher), the
decision memo path if one was written, the re-review result, the verification
performed, whether the review ran independently, remaining risk, and the resume
route if blocked.
