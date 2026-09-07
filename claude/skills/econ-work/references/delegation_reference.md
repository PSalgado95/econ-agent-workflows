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

Where these models are available, use these defaults as a starting point:

| Assignment | Starting choice | Adjustment |
| --- | --- | --- |
| Supporting investigation, code tracing, ordinary implementation and checks | GPT-5.6 Sol Low | Medium or High when interacting logic or unresolved failures justify it |
| Easy searches, locating definitions, extracting specified information | GPT-5.6 Luna | Choose Low, Medium, High, or another supported effort based on the task; higher effort is reasonable for demanding but bounded checks |
| Independent challenge to a consequential economic argument | GPT-6 Astra Low, selectively | Medium when difficult ambiguity warrants it |
| Coordination and final research judgment | The user's selected model and effort | Do not silently change the coordinator |

On other hosts, choose available models with comparable roles rather than
requesting unsupported names. A small model is not restricted to trivial
reasoning, and a review label does not automatically justify an expensive one.
Assess cost per completed assignment, including retries and parent repairs;
do not assume that matching model families shares a cache or guarantees savings.

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

Read the host's current spawn-tool contract before setting model, effort, or
context inheritance. Pass both `model` and reasoning effort explicitly in each spawn request when
supported. For the collaboration tool, these are `model` and `reasoning_effort`;
use `fork_turns: "none"` or a bounded history when needed to permit overrides.
If full-history inheritance prevents overrides, use a self-contained assignment
with the necessary context instead. Verify the returned settings where exposed;
do not assume inheritance is a quality requirement. User-configured defaults
are not a reason to block review. Inspect their effect and override only within
the user's preferences. A different model or lower effort does not itself
mean degraded coverage. No child may weaken the parent's permission boundary.

Keep separate user-owned tasks distinct from subagents. Create a task only when
the user requests one; a worker assignment normally uses child-agent tools.

## Sources and maintenance

Guidance checked 2026-09-07. The model examples should evolve with observed
completion quality and usage; they are not comparative benchmark results.

- [OpenAI subagent guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents): model and effort selection, context isolation, and delegation overhead.
- [OpenAI model selection](https://developers.openai.com/api/docs/guides/model-selection): establish acceptable accuracy, then evaluate cheaper configurations.
- [Practical multi-agent orchestration](https://x.com/pvncher/status/2080707291603407077): focused assignments, variable effort, and leaf-worker boundaries.
