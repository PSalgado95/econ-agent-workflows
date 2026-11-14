---
name: econ-lfg
description: "Run an agreed economics research task end to end without stopping: plan, work, one independent review, revision and delivery. Use only when the researcher explicitly asks for autonomous, hands-off or one-prompt execution. Not for open ideas (econ-brainstorm), a single stage (econ-plan, econ-work or econ-review) or pure software work (ce-work)."
---

<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources and run build_claude.py. -->

# Econ LFG

Run an autonomous economics workflow without losing the research object, evidence trail, or review discipline.

`econ-lfg` is not a replacement for `econ-plan`, `econ-work`, or `econ-review`. It orchestrates them under a goal-backed contract, has the finished work reviewed by one fresh-context reviewer that follows `econ-review`, then owns the review-resolution loop before final delivery.

Read `references/review_resolution_reference.md` before briefing the reviewer, judging which findings hold, deciding whether to fix directly, writing a researcher-level decision memo, or choosing the re-review surface.

## Direct invocation contract

Use this workflow only when the user explicitly asks for hands-off or one-prompt execution of a bounded economics or hybrid research task. Do not auto-route ordinary planning, work, review, or brainstorming requests here.

The required order is:

1. attach to a goal-backed run;
2. invoke `econ-plan`;
3. invoke `econ-work`;
4. review the finished work with one fresh-context reviewer subagent that follows `econ-review` (see "Reviewer subagent");
5. resolve the findings that hold through a revision pass;
6. run a targeted re-review when revisions or new evidence require it;
7. deliver only when the result is resolved, consciously deferred, or genuinely blocked.

Do not skip the saved-plan gate. For non-trivial tasks, `econ-plan` must produce or refresh a saved plan before `econ-work` begins.

Route pure software work to the current Compound Engineering workflow instead of forcing it through economics skills.

## Input

Treat the arguments passed with this invocation, or the user's current request, as the autonomous task to run end to end. Inspect any named files and the available project context before asking questions. Use the request, prior decisions, and that evidence to define the bounded task. Ask only for an unresolved choice that materially changes the economics, authority, or feasible deliverable. State reversible assumptions and proceed; do not repeat an intake interview when the user has already supplied the task. If the prompt would require deciding the research question itself, use `econ-brainstorm` or `econ-plan` to build the task first.

Once the bounded task is agreed and the run begins, work autonomously. Return with a question only when newly discovered evidence would materially change the agreed task, a researcher-level decision is required, required access is missing, or new external or destructive authority is needed.

## Goal-backed run

Claude Code has no goal primitive. Persist the loop with the built-in task list: one task per stage (plan, work, review, revise, re-review, deliver), with statuses kept current as the run advances. The session is the persistence boundary; if it ends, the loop does not survive on its own. Record session-local persistence in the execution record; mention it to the user when it limits completion or resumption. Do not claim a goal was created or promise work after the session ends.

Treat the run as complete only when the final deliverable is produced and review-resolution is handled. Treat the affected branch as blocked when an unresolved economics decision or access limit prevents progress. Continue independent authorised work; do not repeat failed actions or questions without new evidence.

## Reviewer subagent

The review stage starts exactly one reviewer with the `Agent` tool:

- fresh context: leave `subagent_type` at the general-purpose default and never use `fork`, which would inherit this conversation; the prompt is the filled-in brief from `references/review_resolution_reference.md` ("Reviewer brief");
- `model`: pass the alias of the coordinator's own model explicitly (for example `opus` under an Opus coordinator). Never a smaller model and never `haiku`; omitting `model` may fall back to a smaller configured default. Set effort to the coordinator's where the tool exposes an effort setting; otherwise it is inherited. Do not pass `reasoning_effort`;
- a leaf assignment: the reviewer starts no other agents and changes nothing, so no `isolation` is needed;
- wait for its return before Stage 4. If it runs in the background, do not begin Stage 4 until its result has arrived.

If the tool rejects the settings or the start fails, retry once. If the reviewer still cannot run, or its return does not follow the format in the brief after one `SendMessage` follow-up, carry out the same review yourself by following the single-reviewer section of `econ-review`, and record in the closeout that the review was not independent.

## Authority hierarchy

Keep these decision sources separate:

1. **Researcher-anchored choices**: constraints stated in the initial prompt, such as baseline, estimand, sample boundary, benchmark treatment, target output, note scope, or fixed comparison. Do not override these silently.
2. **Plan-backed choices**: decisions written into the saved `econ-plan`. These govern execution unless review or realised outputs show the plan's own assumptions need revision.
3. **Agent-owned choices**: defaults the agent inferred during planning or work, such as diagnostic order, figure priority, note framing, or an implementation route. These may be revised by best judgment when review evidence supports a better path.
4. **Execution-discovered facts**: realised outputs, missing inputs, failed checks, stale artefacts, or unexpected findings. These can force revision or a pause.

When a review finding conflicts with a researcher-anchored choice, pause and ask. When it challenges an agent-owned choice, revise without asking if the better path remains inside the initial prompt's intent.

## Pipeline

### Stage 0: Intake and routing

- Restate the task compactly.
- Classify whether it belongs in the economics workflow:
  - empirical or hybrid economics research: continue;
  - source collection, data construction, model computation, analysis, writing from defended evidence: continue;
  - pure app, API, UI, infrastructure, general tooling, or non-research refactor/debug task: route away.
- Identify likely researcher-anchored choices from the initial prompt.
- Before beginning the autonomous loop, resolve material ambiguity about the objective, baseline, estimand, sample boundary, benchmark treatment, output surface, note scope, destructive overwrite, or rerun authority. During the loop, stop only under the autonomous boundary above.

### Stage 1: Plan

Invoke `econ-plan` with the autonomous task.

After it returns:
- verify that a saved plan path exists, unless `econ-plan` stopped with a blocking question;
- if a blocking question was asked, pause the goal and return the question to the user;
- if the saved plan classifies the task as pure `software-handoff`, route away and stop the economics loop;
- capture the planned review route and artefacts `econ-work` must leave ready.

Do not perform implementation work until the saved-plan gate is satisfied.

### Stage 2: Work

Invoke `econ-work` on the saved plan with the private `caller_contract: econ-lfg/v1` return contract.

After it returns:
- validate that the response uses `econ-work-for-caller/v1` and contains every required field; retry a malformed or wrong-version child response once, then stop with the child-contract failure rather than guessing;
- verify that work reached a valid closeout or named blocker;
- capture what was inspected, changed, run, and regenerated; code role; outputs refreshed versus inherited or inspected-only; interpretation or note-brief status; review-bundle status; and residual risks;
- if work paused for a user-level decision, pause the goal and return that decision;
- if work reached a valid closeout, continue to the review stage.

Do not treat a script run, generated output, or partial closeout as enough to proceed.

### Stage 3: Review

Start the reviewer described in "Reviewer subagent" once the work stage has reached a valid closeout. Fill the reviewer brief from the saved plan and the work closeout: the research question, the deliverable, the settled choices the reviewer must not reopen as findings (researcher-anchored and plan-backed), and the evidence to read: plan, code, realised outputs, notes, and the execution record. Point the reviewer at the single-reviewer section of `econ-review`; resolve `../econ-review/SKILL.md` relative to this skill's directory and pass the absolute path. This explicitly requested end-to-end workflow authorises its review stage.

The reviewer returns a short verdict, findings `R1`, `R2`, ... ranked by consequence, each with its evidence, consequence, fix, and whether it needs the researcher, and a list of what it could not inspect. Record the reviewer's model and effort, whether it ran independently, and its return in the execution record.

### Stage 4: Review-resolution pass

Do not deliver immediately after review. Review findings are evidence for the loop, not orders to change the research object. Use `references/review_resolution_reference.md` for every finding:

1. **Check whether it holds.** Inspect the decisive evidence yourself: the code, definitions, tables, or outputs it cites, with their context and the settled decisions. A finding holds when that evidence supports it and it changes the result or its reading. Disagree on evidence, not on authority; the reviewer's confidence is an input, not a verdict.
2. **Route it.** Give every finding exactly one route token: `fix-now`, `revise-plan-choice`, `ask-user`, `defer-with-rationale`, `advisory-only`, or `rejected` (does not hold, with the reason).
3. **Act.** Fix `fix-now` findings through `econ-work` (with `caller_contract: econ-lfg/v1`, consuming `econ-work-for-caller/v1`) or a bounded local revision pass. Revise `revise-plan-choice` findings when the new path stays inside the initial prompt's intent. Pause on `ask-user` findings and write a decision memo when the decision is non-trivial.
4. **Record which you took.** Keep one line per finding in the execution record: ID, holds or not, route, what was done, changed paths, and the verification run. Report `defer-with-rationale`, `advisory-only`, and `rejected` findings in the final closeout; do not hide them. Deferred findings that affect trust must also land on a durable residual sink before delivery — the review bundle's residual section, a GitHub issue (as the repository's instructions direct, or with approval when it has none), or a dated `docs/residual-findings/<slug>.md` — with their `R<n>` IDs preserved. Never deliver with trust-affecting residuals recorded only in chat.

A "Not inspected" entry that could change the conclusion is a gap: produce the missing evidence when the plan already requires it and the inputs and authority are present (`fix-now`); otherwise route it like a finding.

The direct-fix boundary, the researcher-level trigger list, and the decision-memo contract are defined in `references/review_resolution_reference.md`; apply them exactly.

When a researcher-level decision needs evidence synthesis, write an economist-facing decision memo before asking, using HTML unless another format was requested. A clear single decision can be asked directly with its evidence and consequences; follow the proportional memo contract in the reference. When the installed runtime provides them, prefer the `econ-html-memo` skill for the memo shape and validation, and the `econ-writing` skill for prose discipline. If those skills are unavailable in the runtime, use the fallback memo contract in `references/review_resolution_reference.md` rather than failing on a dangling dependency. The memo must say what decision arose, what the outputs or review findings show, what the agent recommends and why, what changes under each choice, what stays unchanged, and what the agent will do next after the researcher decides.

Write runtime decision memos to the active research workspace. If the saved plan names a memo, note, or output directory, use it. Otherwise write to `docs/decision-memos/<YYYY-MM-DD>-<slug>.html` under the current task workspace. Do not write runtime decision memos into this package/source repo unless the task is explicitly about this repo.

If revisions materially change the plan's assumptions, record that divergence in the work closeout or a follow-up plan recommendation. Do not rewrite the saved plan as a progress log.

### Stage 5: Targeted re-review

If no finding was fixed or revised and no new evidence arrived, proceed to delivery. Do not manufacture a revision or repeat an unchanged review.

After `fix-now` or `revise-plan-choice` revisions, start a new reviewer the same way on the changed or previously problematic surfaces. Its brief adds the earlier findings with what was done about each and the changed paths; it checks whether the fixes hold and whether they introduced new problems, and it may raise anything new on those surfaces. Earlier outcomes never stop it from reporting new evidence.

Widen the re-review beyond the changed surfaces only when revisions changed the baseline, sample, estimand, specification, inference, benchmark treatment, note argument, or primary output family.

Repeat the review-resolution pass until:
- no finding that holds and changes the result or its reading remains unaddressed;
- remaining findings are consciously deferred with rationale or rejected with a reason;
- a researcher-level decision prevents further meaningful work on the affected branch; or
- external access or missing data prevents meaningful progress.

### Stage 6: Deliver

Lead the final closeout with the research outcome and usable deliverable. Explain what the evidence supports, what changed, and the limitations that matter for interpretation or reuse. Then give the saved plan and main output paths, what was actually regenerated versus only inspected, the validation result, and the review conclusion. Translate internal terms when explaining them to the researcher; do not lead with schemas, stages, or agent status.

Keep detailed stage and code-role bookkeeping in the execution record, including the reviewer's model and effort, whether the review ran independently, and any delegated worker's model, effort, and reason. Preserve `R<n>` IDs with the route taken for each, their re-review outcomes, and durable residual paths. Disclose a review that did not run independently, and anything the reviewer could not inspect, plainly; neither can be hidden by a shorter closeout. Include a decision memo or resume instruction only when one is needed. Do not create a follow-up merely to fill a final field.

If the autonomous run explicitly included compounding and produced a durable reusable lesson, invoke `econ-compound` after review-resolution. If compounding was in scope but no durable lesson emerged, report `Reusable lesson: none` and write nothing. When compounding was not in scope, keep any candidate in the closeout without interrupting the run or writing a learning note.

## Hard stops

- Do not skip `econ-plan` for non-trivial tasks.
- Do not proceed from `econ-work` to delivery without the review stage, unless the saved plan or work closeout explicitly says no later review is needed.
- Do not review with a model smaller than the coordinator's, or with a panel of reviewers in place of the single reviewer.
- Do not deliver with unprocessed review findings.
- Do not present a review the coordinator carried out itself as independent.
- Follow the repository's own instructions for Git and issues (branching, committing, pushing, issue and pull-request comments). Only when the repository has none, ask before committing, pushing, or posting.
- Do not silently override researcher-anchored choices.
- Do not make cross-language validation default-on.
- Do not import Compound Engineering PR, CI, browser-test, or deploy steps into this workflow; Git and pull-request actions follow the rule above.
- Do not write durable learning notes unless the user explicitly asked for learning capture or the autonomous run explicitly includes compounding.

## Output

When complete, return the final closeout. When blocked, return:
- blocker type;
- decision or missing access needed;
- evidence path or review finding that caused the pause;
- options for the user;
- recommended conservative path; and
- exact command or prompt to resume the goal-backed run.
