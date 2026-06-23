# Econ Agent Workflows

Agentic workflows for economists, inspired by [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin).

These skills adapt a plan -> work -> review -> revise -> compound loop to economic research. They help a coding agent turn a research task into a staged plan, run code and checks, inspect and interpret outputs, review the resulting evidence, revise in response to review findings, and save lessons that should carry into future projects.

This is still a beta. Most of the development so far has come from empirical work: data cleaning, sample construction, estimation, tables, figures, notes, review bundles, and reproducibility handoffs. The same loop should also adapt to more theory-based settings, including structural and theory-based work, calibration, simulation, etc.

The skills were built and tested for Codex, but the loop is conceptually portable to Claude Code or any agent runtime that supports skills and subagents. The Codex-specific pieces are the install paths, local skill layout, and reviewer-agent configuration.

## The Loop

1. **Plan** the research task: who reads the output, what is being estimated or built, what evidence will exist, and how it will be reviewed.
2. **Work** through it: run code, inspect outputs, interpret results, prepare notes, and close out while keeping those steps distinct.
3. **Review** the result before trusting or promoting it: a plan, a set of outputs, a bundle, a note, a diff, or a mix.
4. **Revise** fixable or agent-owned review findings before delivery, while pausing before overriding researcher-anchored choices.
5. **Compound** a reusable lesson, but only when there is bounded evidence for it.

## Core Skills

- **`econ-plan`** turns a research or analysis-engineering task into a staged plan. It surfaces the material planning decisions, classifies the task family, and hands a four-stage execution path to `econ-work`.
- **`econ-work`** executes from a saved plan or a clear request. It keeps code changes, output inspection, interpretation, note preparation, review-bundle preparation, and closeout separate.
- **`econ-review`** reviews plans, outputs, bundles, notes, diffs, or mixed evidence surfaces. It audits the evidence and runs an economist review panel using the included reviewer agents.
- **`econ-lfg`** runs the autonomous loop for bounded tasks: plan, work, review, revise fixable or agent-owned findings, write decision memos for researcher-level choices, targeted re-review, then deliver or pause.
- **`econ-compound`** saves durable research lessons as bounded precedent, validating each note against its evidence paths, scope, status, and rules for staleness and supersession.
- **`create-project`** starts a sparse economics research project in the current folder. It creates a local scaffold, brief starter control files, and a private GitHub repository while routing working notes and agent clutter to `scratch/`.

## Review Panel

`econ-review` is built around research-audit lenses. The review checks the main places where research workflows can go wrong: data provenance, sample and variable construction, specification choice, inference, robustness, output consistency, reproducibility, and research-code quality when code is part of the review surface. Different reviewer agents specialise in these questions, and the parent review skill assigns the relevant ones for the task. A data-cleaning review focuses on provenance, transformations, sample rules, and output consistency. A results review adds specification, estimation, inference, robustness, or dynamics checks when the estimates require them.

The review panel also includes a code-quality evaluator for research code. It checks whether scripts, notebooks, model code, and helper functions are clear, testable, rerunnable, and appropriate for the role they play in the project. The standard is intentionally different for exploratory code, analysis pipelines, replication-facing code, and reusable research tools. It also covers performance and numerical-code concerns when they matter for the task. This part of the workflow draws in part on Matthew Rognlie's coding guide and his [fast-code-macro](https://github.com/mrognlie/fast-code-macro) materials.

Reviewer lenses live as custom agents under `.codex/agents/`, with shared rules in [references/reviewer-protocol.md](references/reviewer-protocol.md) and [references/research-code-quality.md](references/research-code-quality.md). If the agents are not installed or subagent tools are unavailable, `econ-review` reports that the panel did not fully run. Promotion-grade reviews stop or ask before continuing in a degraded mode.

### Cross-Language Validation

The skills also support cross-language validation as a way to catch coding mistakes. The idea is to rebuild selected outputs independently in another language, most naturally R or Python, and sometimes Stata. Because the agent has to express the same sample, variables, transformations, fixed effects, and inference rules in a different software environment, it is less likely to repeat exactly the same coding error. The validation then compares coefficients, standard errors, diagnostics, and output files, classifying any discrepancy as an object mismatch, a software-convention difference, a tolerance-level numerical difference, or an unresolved problem.

Use `crosslang:plan` to prepare the validation handoff or `crosslang:audit` to check an existing validation against its manifest. It is off by default and is never triggered just because a repo contains more than one language.

## Folder Structure

```text
.codex/
  agents/
    econ-*-reviewer.toml      # Codex reviewer agents (source of truth)
references/
  reviewer-protocol.md        # shared reviewer protocol (source of truth)
  research-code-quality.md    # shared research-code-quality standard
skills/                       # skills (source of truth)
  econ-plan/
  econ-work/
  econ-review/
  econ-lfg/
  econ-compound/
  create-project/
  auxiliary/
    gpt-pro-handoff/
claude/                       # generated Claude Code package (do not hand-edit)
  skills/  commands/  agents/  references/
install.py                    # Codex installer
build_claude.py               # regenerates claude/ from the Codex sources
install_claude.py             # installs the generated claude/ package
LICENSE
README.md
```

## Installation

`econ-review` depends on three pieces: the skill text, the reviewer agents, and the shared references. Installing only the skills leaves the review panel incomplete.

**Simplest path**: ask Codex to install the package from this repo.

```text
Clone or download https://github.com/PSalgado95/econ-agent-workflows, then run:

python install.py --force

from the repo root. Confirm it installs the core skills, auxiliary helper skills, reviewer agents, and shared references.
```

Restart Codex afterward so the skills and reviewer agents load.

**Manual install**: copy the core skill folders and auxiliary skill folders into your Codex skills folder, copy `.codex/agents/*.toml` into your Codex agents folder, and copy `references/*.md` into a stable reference location such as `~/.codex/references/econ-agent-workflows/`.

### Claude Code

The skills are authored for Codex, and a ready-to-install Claude Code package is generated under `claude/`. Install it from the repo root:

```text
python install_claude.py --force
```

This installs into `~/.claude`: the skills, `/econ-plan` / `/econ-work` / `/econ-review` / `/econ-lfg` / `/econ-compound` / `/create-project` / `/gpt-pro-handoff` slash commands, the reviewer subagents, and the shared references. Restart Claude Code afterward. To update, pull the repo and re-run the same command.

On Claude Code the reviewer lenses run as subagents dispatched through the Task tool, and they default to the Sonnet model (promote a review to Opus manually when the task is critical).

### Editing the skills (maintainers)

**Codex is the single source of truth.** Edit the Codex sources (`skills/`, `.codex/agents/`, `references/`), then regenerate the Claude Code package and commit it:

```text
python build_claude.py
```

Never hand-edit anything under `claude/`; every generated file says so in a banner and will be overwritten on the next build.
