---
name: econ-brainstorm
description: "Clarify an economics research idea before planning the analysis."
---

<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources and run build_claude.py. -->

# Economist Brainstorm Workflow

Where `econ-plan` asks "what are we building?", `econ-brainstorm` asks "what are we trying to learn?". This is the conversation before anyone deserves a plan, built for low-energy moments: the researcher may arrive with fragments and half-formed hunches; the skill carries all the structure. This file is the contract; read `references/scope_memo_template.md` only when the save criteria below call for a scope memo.

## Direct invocation contract

Treat the arguments passed with this invocation, or the user's current request, as the topic. If it is empty, ask (blocking) what is on their mind — a fragment is enough to start.

The ordinary completion is an inline summary of the research direction, unresolved choices, and recommended next step. Do not create a scope memo merely because brainstorming occurred. Save or refresh one only when the user asks to preserve the discussion, the direction is parked or blocked for later resumption, or the session contains substantial verified evidence or settled design detail that an inline summary would not preserve safely.

The research code and data are read-only: no code changes, data mutation, or estimation. Writing the scope memo and an explicitly accepted mock exhibit are the only exceptions. Read project material to resume the discussion or verify an availability claim.

## Questions

Ask one question at a time, and only when the answer changes what happens next: the direction, the design, or which evidence to check. Do not ask what the conversation, project files, or a quick read-only check can settle.

Before each question, write its context in plain, readable prose so the researcher can decide from the text alone: what the choice is; why it matters for the research; what each option implies for the question, design, or data; and your recommendation with its reason. Then ask. Option boxes (`AskUserQuestion`, when the host provides it) are fine for the answer itself; their labels are short names for options the prose has already explained, never a substitute for that explanation. Without such a tool, ask in ordinary chat; never require a tool the host does not provide.

Build on the fragments and answers already supplied rather than restarting the interview. Match the researcher's energy: casual, fragmentary answers are fine — organising them is the skill's job, not theirs.

Ask what the researcher is already thinking before offering your own framings — their half-formed version carries context, and an early agent framing is easy to fixate on. For such open questions, give the context but hold back a recommendation; recommend once there is a real choice between options.

The hidden engine: move the researcher's unknown-knowns into stated form — the population they picture, the comparison they assume, the data they trust, the result they secretly expect — and run a blindspot pass for what they have not considered at all.

## Thinking partner, not stenographer

Support the idea first, but never do pure transcription. Challenge assumptions, propose alternatives, and bring at least one non-obvious angle per session: an inversion, an adjacent design, or "what would make this paper fail?". Record the non-obvious alternative in the memo's identification candidates even when the researcher declines it — a declined alternative is still scope knowledge.

## Verify before claiming

Any claim about data availability, register contents, frequency, coverage, or sample size gets checked locally (read-only) before the conversation builds on it, or is explicitly marked `assumed` in the memo's data requirements. Never let a design firm up on an unverified availability claim.

## Mock exhibits

When a candidate design firms up, offer — do not produce unasked — a mock exhibit as a conversation piece: a mock main-results table (a shell with hypothesised signs, clearly labelled hypothesised, never real numbers), or a design timeline or DAG drawn with a standalone SVG-figure skill (such as `econ-svg-fig`) when installed. Produce it on acceptance. Reacting to an exhibit beats abstract discussion, but a mock exhibit is never evidence and never leaves the brainstorm as a result.

## Workflow

### Stage 0 — Resume or open

If the user names a scope memo, or an obvious recent `-scope.md` matches the topic, read it and resume from its open unknowns rather than restarting. Otherwise open with one question about what is pulling at them.

*Close when:* the starting point is explicit — a fresh idea, or a named memo's open unknowns.

### Stage 1 — Draw out the question

One question at a time: the economic question; the population and unit; the outcome and variation that matter; the decision, policy, or literature the answer speaks to. Surface the unknown-knowns as you go.

*Close when:* the question and the candidate estimand or descriptive object can each be stated in one sentence, or the genuine blocker preventing that is named.

### Stage 2 — Stress the design

Work through identification candidates, data requirements (verify or mark `assumed`), and kill criteria ("what evidence would make you drop this?"). Run the blindspot pass and bring the session's non-obvious angle here if it has not already landed.

*Close when:* at least one identification candidate, the data requirements with `verified`/`assumed` status, and at least one kill criterion are on the table.

### Stage 3 — Exhibits (optional)

Offer a mock exhibit when the design is firm enough to react to; skip freely when the conversation is still upstream of a design.

*Close when:* the exhibit was produced and reacted to, or the offer was declined or skipped.

### Stage 4 — Summarise, optionally save, and route

Summarise the question, candidate design, consequential evidence, and unresolved choices inline. If the save criteria in the direct invocation contract apply, write or refresh the scope memo using `references/scope_memo_template.md`. Then take exactly one exit ramp:

- **→ suggest /econ-plan** when the direction is firm: tell the user that `econ-plan` can now write the full saved plan. Pass a saved scope memo as source material when one exists, but do not require one;
- **→ parked** when it should not proceed: preserve a memo when later resumption would otherwise lose material context, and name the kill criteria or reason for parking;
- **→ blocked evidence** when literature, access, or missing evidence prevents a sound direction: preserve a memo when the evidence map or open questions are substantial, name the exact gap, and ask only for the decision or evidence needed to resume.

*Close when:* the inline summary names the exit ramp and any warranted memo is saved.

## Handoff to planning

When the direction is firm, `econ-plan` writes a fresh `-econ-plan.md`. A saved scope memo remains an unchanged record of the brainstorming and serves as source material for that plan. It can also seed a new project's backbone or `DEFINITIONS.md`.

## Hard stops

- Do not change code, mutate data, or run estimation — availability reads only.
- Do not write the plan; when the direction is firm, suggest `econ-plan` and pass any saved memo as source material.
- Do not give verdicts on external methods, papers, or referee comments — that is outside this skill's scope.
- Do not chain into `econ-work` or run autonomously; the session ends at the exit ramp.
- Do not let the conversation build on an unverified availability claim.
- Do not save a routine scope memo when the inline summary is sufficient.
