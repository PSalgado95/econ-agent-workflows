---
name: econ-lfg
description: "Run a goal-backed autonomous economics workflow end to end. Use when the user explicitly wants one-prompt execution of a bounded empirical, model-computation, writing-from-evidence, or hybrid research task: plan with econ-plan, execute with econ-work, review with econ-review, revise findings, re-review, and deliver or pause only for user-level economics decisions."
---

<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources (skills/, .codex/agents/, references/) and run build_claude.py. -->

# Econ LFG

Run an autonomous economics workflow without losing the research object, evidence trail, or review discipline.

`econ-lfg` is not a replacement for `econ-plan`, `econ-work`, or `econ-review`. It orchestrates them under a goal-backed contract, then owns the review-resolution loop before final delivery.

Read `references/review_resolution_reference.md` before classifying review findings, deciding whether to fix directly, writing a Pedro-level decision memo, or choosing the targeted re-review surface.

## Direct invocation contract

Use this workflow only when the user explicitly asks for hands-off or one-prompt execution of a bounded economics or hybrid research task. Do not auto-route ordinary planning, work, review, or brainstorming requests here.

The required order is:

1. attach to a goal-backed run;
2. invoke `econ-plan`;
3. invoke `econ-work`;
4. invoke `econ-review`;
5. resolve review findings through a revision pass;
6. run targeted re-review;
7. deliver only when the result is resolved, consciously deferred, or genuinely blocked.

Do not skip the saved-plan gate. For non-trivial tasks, `econ-plan` must produce or refresh a saved plan before `econ-work` begins.

For Sequence-Jacobian / SSJ tasks, do not let the autonomous loop bypass the specialist map gate. The saved plan must either include an implementation-ready `econ-ssj-map` model map or make `econ-ssj-map` the next step before `econ-ssj-work` performs structural SSJ implementation or review-grade computation.

Route pure software work to the current Compound Engineering workflow instead of forcing it through economics skills.

## Input

<autonomous_task> #$ARGUMENTS </autonomous_task>

If the input is empty, ask one focused question:
"What bounded economics or hybrid research task should I run end to end?"

If the prompt is broad, ambiguous, or would require deciding the research question itself, ask for a narrower task or route to `econ-plan` first.

## Goal-backed run

Use the host platform's goal or persistence primitive when available. If the run is already inside a goal, continue under that goal. If no active goal exists and a goal primitive is available, create one whose objective names the requested research output and the required `econ-plan -> econ-work -> econ-review -> revision -> re-review` loop.

If no goal primitive is available, continue only when the host session itself can reasonably persist the loop. In the closeout, state that the run used session-local persistence rather than a goal-backed runtime. Do not pretend a goal was created.

Mark the goal complete only when the final deliverable is produced and review-resolution is handled. Mark it blocked only when the same user-level economics decision or external-access blocker prevents meaningful progress after repeated attempts.

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
- Record any material ambiguity that would block planning. Ask only if the missing answer changes baseline, estimand, sample boundary, benchmark treatment, output surface, note scope, destructive overwrite, or full rerun authority.

### Stage 1: Plan

Invoke `econ-plan` with the autonomous task.

After it returns:
- verify that a saved plan path exists, unless `econ-plan` stopped with a blocking question;
- if a blocking question was asked, pause the goal and return the question to the user;
- if the saved plan classifies the task as pure `software-handoff`, route away and stop the economics loop;
- capture the planned review route and artefacts `econ-work` must leave ready.

Do not perform implementation work until the saved-plan gate is satisfied.

### Stage 2: Work

Invoke `econ-work` on the saved plan.

After it returns:
- verify that work reached a valid closeout or named blocker;
- capture execution mode, code role, outputs refreshed versus inherited or inspected-only, interpretation or note-brief status, review-bundle status, and residual risks;
- if work paused for a user-level decision, pause the goal and return that decision;
- if work completed with a recommended `econ-review` route, continue.

Do not treat a script run, generated output, or partial closeout as enough to proceed.

### Stage 3: Review

Invoke `econ-review` using the review route from the plan or work closeout. Prefer `mode:headless` or `mode:autofix` only when the host workflow needs a non-interactive artifact; otherwise run the normal findings-first review.

Select the lightest review tier that protects the output:
- at least `tier:standard` for claim-bearing empirical or hybrid changes;
- `tier:promotion` before coauthor, supervisor, paper, appendix, replication, presentation, or public-facing promotion;
- `tier:quick` only for narrow hygiene surfaces with no realised empirical claims.

Capture:
- retained findings;
- fix classes;
- trust effects;
- affected labels;
- safe auto-fixes already applied;
- residual work;
- missing diagnostic surfaces; and
- whether the panel was degraded.

### Stage 4: Review-resolution pass

Do not deliver immediately after review. Use `references/review_resolution_reference.md` to classify each retained finding. Review findings are evidence for the loop, not orders to change the research object.

For every retained finding, inspect its finding ID, fix class, trust or promotion effect, issue origin, affected labels, evidence path, missing diagnostic surfaces, and authority source. Then assign exactly one route token:

- `fix-now`: safe automatic, mechanical, or agent-owned revision that should be handled before delivery;
- `revise-plan-choice`: review evidence shows an agent-owned planning default should change;
- `ask-user`: the fix would override a researcher-anchored choice or touch the Pedro-level trigger list;
- `defer-with-rationale`: legitimate follow-up outside the prompt or not needed for the requested output;
- `advisory-only`: useful note that does not affect trust, promotion, or the requested output.

Apply this policy:
- Fix `fix-now` findings through `econ-work` or a bounded local revision pass.
- Revise `revise-plan-choice` findings when the new path remains inside the initial prompt's intent.
- Pause for `ask-user` findings and write a decision memo when the decision is non-trivial.
- Record `defer-with-rationale` and `advisory-only` findings in the final closeout; do not hide them.

Claude Code may fix directly without asking Pedro for path repairs, stale cross-references, stale or missing metadata, stale or missing bundle manifests, package file-list checks already in scope, validators or checks named by the plan or review, output-consistency repairs that align wording with accepted evidence, missing diagnostics already required by the saved plan, and agent-owned choices such as diagnostic order, figure priority, note framing, implementation route, or review-bundle organisation.

Pedro must decide when a finding or proposed fix would change any of these:

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

When a non-trivial Pedro-level decision blocks progress, write an economist-facing HTML decision memo before asking. When the installed runtime provides them, prefer the `econ-html-memo` skill for the memo shape and validation, and the `econ-writing` skill for prose discipline. If those skills are unavailable in the runtime, use the fallback memo contract in `references/review_resolution_reference.md` rather than failing on a dangling dependency. The memo must say what decision arose, what the outputs or review findings show, what the agent recommends and why, what changes under each choice, what stays unchanged, and what the agent will do next after Pedro decides.

Write runtime decision memos to the active research workspace. If the saved plan names a memo, note, or output directory, use it. Otherwise write to `docs/decision-memos/<YYYY-MM-DD>-<slug>.html` under the current task workspace. Do not write runtime decision memos into this package/source repo unless the task is explicitly about this repo.

If revisions materially change the plan's assumptions, record that divergence in the work closeout or a follow-up plan recommendation. Do not rewrite the saved plan as a progress log.

### Stage 5: Targeted re-review

After `fix-now` or `revise-plan-choice` revisions, run targeted `econ-review` on changed or previously problematic surfaces. Cite the fixed finding IDs, changed surfaces, affected labels, and previous evidence paths.

Escalate to broader review only when revisions changed the baseline, sample, estimand, specification, inference, benchmark treatment, note argument, or primary output family.

Repeat the review-resolution pass until:
- no blocking or worth-fixing findings remain;
- remaining findings are consciously deferred with rationale;
- the run hits the same user-level decision blocker repeatedly; or
- external access or missing data prevents meaningful progress.

### Stage 6: Deliver

Deliver a compact final closeout with:
- original objective;
- saved plan path;
- execution mode and code role;
- outputs refreshed, inherited, inspected-only, or scaffolded;
- interpretation brief, note brief, note, figure, or bundle status;
- review tier, surface, and panel status;
- review findings fixed, with finding IDs and targeted re-review result;
- review findings deferred or advisory, with finding IDs and rationale;
- decision memo path, when one was written;
- blockers or user decisions, if any;
- verification performed;
- remaining risks;
- reusable lesson checkpoint; and
- recommended next command, if any.

If the autonomous run explicitly included compounding and produced a durable reusable lesson, invoke `econ-compound` after review-resolution. Otherwise keep the reusable lesson checkpoint in the closeout only.

## Hard stops

- Do not skip `econ-plan` for non-trivial tasks.
- Do not proceed from `econ-work` to delivery without `econ-review`, unless the saved plan or work closeout explicitly says no later review is needed.
- Do not deliver with unprocessed review findings.
- Do not silently override researcher-anchored choices.
- Do not make cross-language validation default-on.
- Do not auto-create GitHub issues unless the user requested issue creation or update.
- Do not add Compound Engineering PR, CI, browser-test, or deploy behavior to this workflow.
- Do not write durable learning notes unless the user explicitly asked for learning capture or the autonomous run explicitly includes compounding.

## Output

When complete, return the final closeout. When blocked, return:
- blocker type;
- decision or missing access needed;
- evidence path or review finding that caused the pause;
- options for the user;
- recommended conservative path; and
- exact command or prompt to resume the goal-backed run.
