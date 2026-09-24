<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources and run build_claude.py. -->

# Delegation reference

Read this when an economics workflow delegates work. `econ-plan`, `econ-work`, and `econ-review` use this same policy; loading this reference does not invoke the execution workflow. It holds the packet templates, the rule for choosing a worker's model and reasoning effort, and host notes. The coordinator retains responsibility for the research question, definitions, evidence assessment, priorities, and final conclusions.

Use the user's selected coordinator model and effort. Explicit user worker-model and effort overrides take precedence over these defaults. Respect the settings actually exposed by the host. The examples below are starting choices, not capability guarantees or mandatory tiers.

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

## GPT worker selection

GPT model IDs are not accepted by Claude-native worker tools. Use the Claude worker selection policy below. Only use an external GPT worker when explicitly authorised and supported by that tool.

## Claude worker selection

For an Anthropic worker, use Claude Opus 5.5 (`claude-opus-5-5`) when Opus is
selected for implementation or independent judgment. This is the latest Opus
verified in the official documentation on 2026-09-24; it is not a mandate to
send every lightweight search to Opus. Keep small searches local or use an
explicitly authorised available lightweight model. Do not pass GPT IDs to
Claude-native tools or substitute a different Anthropic family automatically.

Claude Code requires version 2.1.280 or later for Opus 5.5. Check `claude --version`, the current tool contract, provider, and account availability before
dispatch. Prefer the full ID where accepted; an `opus` alias is acceptable only
when its resolved model is verified as the requested version. Older CLIs can
accept a model-name argument without supporting that model. Report an upgrade
requirement instead of launching an older Opus under the alias.

Opus 5.5 supports `low`, `medium`, `high`, `xhigh`, and `max`. Choose effort for
the assignment, starting with Medium for ordinary bounded work and High when
harder judgment warrants it. Use only effort controls the installed tool
actually exposes (for example subagent `effort` or CLI `--effort` on supported
versions); do not pass `reasoning_effort` to a Claude tool that lacks it. If a
child tool only accepts aliases or cannot set effort independently, verify
alias resolution and inherited effort before dispatch, or disclose the limit
and continue locally. Do not change the coordinator to configure a worker.

## Unavailable models and overrides

Never silently substitute GPT-5.6 models, an older Opus, an inherited model, or
an expensive fallback when the selected worker model is unavailable. Honor an
explicit user override, including an older model if deliberately requested.
Otherwise report the unavailable model and continue locally where possible;
ask for an alternative only if independent work is necessary to complete the
assignment. Do not enable automatic fallback options. If the provider changes
the actual model, disclose it and do not count that return as the requested
independent check without resolving the mismatch.

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

Read the installed `Agent` tool contract before dispatch. Pass the selected model explicitly using a supported full ID or a verified alias. Do not assume the alias is the model that actually ran. Check the returned model and effort where exposed; disclose any unverified setting. Follow the version and availability checks above.

Use an independent effort setting only where exposed by the installed tool. Otherwise verify and record inherited effort; never send `reasoning_effort` to an unsupported parameter. Do not change the coordinator's model or effort to configure a child.

Give each worker a self-contained evidence packet and use the general-purpose worker rather than registering persona agents. Preserve the user's permission boundary. Use background execution for independent assignments when supported, and isolate writers only when their file ownership requires it. Follow up with an existing worker when possible; on capacity errors, wait for owned work or continue locally. Create a separate user-owned task only when requested.

## Sources and maintenance

Guidance checked 2026-09-24 against the live GPT spawn-tool contract and local model catalogue, plus the official Anthropic documentation below. The model examples should evolve with observed
completion quality and usage; they are not comparative benchmark results.

- [OpenAI subagent guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents): model and effort selection, context isolation, and delegation overhead.
- [OpenAI model selection](https://developers.openai.com/api/docs/guides/model-selection): establish acceptable accuracy, then evaluate cheaper configurations.
- [Practical multi-agent orchestration](https://x.com/pvncher/status/2080707291603407077): focused assignments, variable effort, and leaf-worker boundaries.

- [Anthropic model catalogue](https://platform.claude.com/docs/en/models/overview): current Opus designation and full model ID.
- [Claude Code model configuration](https://code.claude.com/docs/en/model-config): version requirements, provider aliases, effort controls, and fallback behavior.
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents): supported child model and effort settings; verify the installed version's contract.
