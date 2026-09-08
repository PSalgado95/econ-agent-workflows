<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources and run build_claude.py. -->

# Delegation reference

Read this when an economics workflow delegates work. `econ-work` and `econ-review` use this same policy; loading this reference does not invoke the execution workflow. It holds the packet templates, the rule for choosing a worker's model and reasoning effort, and host notes. The coordinator retains responsibility for the research question, definitions, evidence assessment, priorities, and final conclusions.

Use the user's selected coordinator model and effort. Respect their model preferences and the settings actually exposed by the host. The examples below are starting choices, not capability guarantees or mandatory tiers.

## Packet templates

Fill every field. A field that cannot be filled precisely for a bounded worker means the work is judgment work.

### Judgment worker

```md
## Worker packet (judgment)
- Economic question:
- Fixed definitions (cite DEFINITIONS.md or the plan's registry):
- Evidence the worker may use (paths, evidence IDs):
- What the worker may decide, and what stays with the parent:
- Completion check (what a correct return shows):
- Return form (short note; findings first; evidence locations):
```

### Bounded worker

```md
## Worker packet (bounded)
- Operation (one sentence, no interpretation):
- Exact inputs (paths, vintages, hashes if known):
- Exact commands or entrypoint:
- Exact output form (file path or table shape, units, rounding):
- Stop rule (when to stop and return, including on error):
- Do not decide: any Class A or B choice, any definition, any new sample rule
- Completion check the parent will run on the return:
```

## Choosing workers and reasoning effort

The coordinator decides whether delegation is useful before choosing a model.
Keep a task local when dispatch, repeated context, and checking the return would
cost more than doing it directly. Delegate separable investigations with clear
ownership; avoid duplicate searches and overlapping writers.

For each proposed worker, identify the question, evidence, expected return,
completion check, model and effort, and why delegation helps. Select model and
effort separately according to difficulty, consequences of error, and how the
return will be checked. Judgment work and review do not require the parent's
settings. Workers may reason, challenge assumptions, and disagree; the parent
checks decisive evidence and owns the synthesis. Decisions reserved for the
researcher remain with the researcher.

A small model is not restricted to trivial reasoning, and a review label does
not automatically justify an expensive one. Assess cost per completed
assignment, including retries and parent repairs; do not assume that matching
model families shares a cache or guarantees savings. The starting choices for
the current host are in the next section.

## Starting model choices

The `Agent` tool accepts a `model` value. Use `sonnet` and `opus` only; do not pass a smaller model for economics work. Reasoning effort is not a per-call setting on this host; see Host settings.

| Assignment | Starting choice | Adjustment |
| --- | --- | --- |
| Supporting investigation, code tracing, ordinary implementation and checks | `sonnet` | `opus` when interacting logic, unresolved failures, or a consequential definition are involved |
| Easy searches, locating definitions, extracting specified information | `sonnet` | Keep `sonnet`; narrow the packet and stop rule instead of raising the model |
| Independent challenge to a consequential economic argument | `opus`, selectively | Reserve for verdict-changing or promotion-bound arguments; a same-family child is not an independent model |
| Coordination and final research judgment | The user's selected model and effort | Do not silently change the coordinator |

Pass `model` explicitly on every worker start. Omitting it inherits the session model, which silently runs a bounded worker at the coordinator's tier.

## Scope, context, and resource budget

Start narrow reviews locally and substantial reviews with zero to two children.
This is an initial default, not a requirement to spawn two or a universal cap.
When the right budget or reasoning intensity is materially uncertain, recommend
a concrete worker budget, model/effort mix, and tradeoff, then ask the user how
aggressive to be. Continue independent local work while that question is pending;
do not repeat it when a budget or preference is already settled.

Record a finite total child-start budget and a separate concurrency limit before
dispatch. Set them from the actual independent questions and user constraints,
not the number of lenses or available host slots. A free slot is not a reason
to launch another agent. Before expanding the budget, assess existing returns,
name the unresolved question and benefit, and record the revised budget and
reason. Honor any user-set ceiling; ask only if increasing it is necessary.
Retries and replacement workers count toward total starts. Prefer a targeted
follow-up to an existing worker when it avoids repeated context.

Use fresh context for bounded assignments, with only the relevant evidence,
fixed decisions, restrictions, and return contract. Include broader history
only when the assignment needs it. State: complete this assignment directly;
do not spawn other agents. Stay available to the user and integrate completed
returns while independent work proceeds. Do not repeat the same investigation
locally merely because it was delegated; check the decisive evidence instead.

Record the actual worker model and effort when exposed, the selection reason,
and whether the return passed its completion check. If settings cannot be
verified, disclose that rather than asserting a model or independence level.
Do not launch an unknown expensive fallback. Continue locally when appropriate.

## Host settings

Workers are started with the `Agent` tool. Its contract, as checked on 2026-09-07:

- `model`: pass explicitly on every start (`sonnet` or `opus`, per the table above). The value passed is the value used, so record it as the worker model.
- Reasoning effort: there is no per-call effort parameter. Workers inherit the session's effort setting. Do not pass `reasoning_effort`; the call is rejected. Record effort as `inherited` in the delegation log, and steer depth through model choice and the packet's scope, stop rule, and completion check.
- Context: a worker starts with fresh context and receives only its prompt. Every packet must be self-contained; the worker cannot see the conversation.
- `subagent_type`: leave at the general-purpose default. Do not register or reference persona-bearing agent definitions.
- `mode`: omit, so the user's permission settings apply to the child. No child may weaken the parent's permission boundary.
- `run_in_background: true` when the assignment is independent, so the coordinator stays available and integrates returns as they arrive.
- `isolation: "worktree"` only for a worker that writes files inside a Git repository; the coordinator integrates the worktree afterwards. Review and bounded read-only assignments do not need it.
- Follow-up: use `SendMessage` with the existing worker's name to ask a follow-up; this does not count as a new start. A capacity error is backpressure: wait for an owned worker or continue locally; do not spin.

Verify the returned settings where exposed; do not assume inheritance is a quality requirement. User-configured defaults are not a reason to block review. Inspect their effect and override only within the user's preferences. A different model or inherited effort does not itself mean degraded coverage.

Keep separate user-owned tasks distinct from subagents. Create a task only when the user requests one; a worker assignment normally uses child-agent tools.

## Sources and maintenance

Guidance checked 2026-09-07. The model examples should evolve with observed
completion quality and usage; they are not comparative benchmark results.

- [OpenAI subagent guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents): model and effort selection, context isolation, and delegation overhead.
- [OpenAI model selection](https://developers.openai.com/api/docs/guides/model-selection): establish acceptable accuracy, then evaluate cheaper configurations.
- [Practical multi-agent orchestration](https://x.com/pvncher/status/2080707291603407077): focused assignments, variable effort, and leaf-worker boundaries.
