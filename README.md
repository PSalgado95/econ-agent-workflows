# Econ Agent Workflows

Small Codex workflows for economists, inspired by [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin).

## Status

Working beta. Shared for early feedback; expect rough edges.

The goal was to take the plan/work/review discipline that Compound Engineering makes natural for software projects and adapt it to how economists work. This is not a replacement for Compound Engineering, and it is not affiliated with Every. If you want the general engineering workflow, use Compound Engineering directly. This repo is a small economics-specific adaptation.

At this stage, the package is most developed for empirical projects: data cleaning, sample construction, estimation, tables, figures, notes, review bundles, and reproducibility handoffs. Some pieces may also be useful for structural work, model-building, calibration, simulation, or other economics workflows, but those paths are less tested.

The package is organized around a simple research workflow:

1. plan the empirical task;
2. execute the code, checks, outputs, and interpretation work;
3. review the plan, outputs, bundle, or note before trusting or promoting results;
4. capture reusable research-learning notes only when they have bounded evidence; and
5. keep empirical traceability explicit throughout.

The skills are meant for economists working with data, estimation, tables, figures, notes, replication material, and hybrid analysis-engineering projects.

The package is currently designed for Codex skills and Codex custom agents. The architecture is intentionally portable: the same division between a parent review workflow, role-specific reviewers, and a shared reviewer protocol can be adapted for Claude Code or other agent runtimes, but those adapters are not packaged here yet.

## Skills

- `econ-plan`: turns an empirical or hybrid research task into a staged plan. It makes the reader, reporting class, bottleneck, evidence surface, execution stages, and review route explicit.
- `econ-work`: executes empirical or hybrid work from a saved plan or clear request. It separates code execution, output inspection, interpretation, note preparation, and closeout.
- `econ-review`: reviews empirical plans, results, bundles, notes, diffs, or mixed work surfaces. Direct invocation means "try to run the economist review panel" using the included Codex custom reviewer agents.
- `econ-compound`: captures durable economics research lessons as bounded precedent, not live project state. It validates learning notes against evidence paths, scope, status, and stale/supersession rules.

Reviewer lenses live as custom agents under `.codex/agents/`, with shared rules in `references/reviewer-protocol.md`.

The review panel is evidence-triggered. Data cleaning, sample construction, and provenance reviews use the core data reviewers by default. Econometrics-heavy reviewers such as inference, design, dynamics, robustness, and cross-language validation are added only when the review surface calls for them.

## Folder Structure

```text
.codex/
  agents/
    econ-*-reviewer.toml
references/
  reviewer-protocol.md
skills/
  econ-plan/
  econ-work/
  econ-review/
  econ-compound/
install.py
LICENSE
README.md
```

## Installation

This is a workflow package, not just a set of skills. `econ-review` needs the reviewer agents and shared protocol too.

Simplest path: ask Codex to install the full package from this repo.

```text
Install the full econ-agent-workflows package from https://github.com/PSalgado95/econ-agent-workflows.

Clone or download the repo, run `python install.py --force` from the repo root, and confirm that it installs:
- the four skills under skills/
- the reviewer agents under .codex/agents/
- the shared reviewer protocol under references/

Do not stop after installing only the skills; econ-review's panel needs the reviewer agents.
```

Restart Codex after installation so the skills and reviewer agents are loaded.

Manual installation is the same three pieces: copy `skills/econ-plan`, `skills/econ-work`, `skills/econ-review`, and `skills/econ-compound` into your Codex skills folder; copy `.codex/agents/*.toml` into your Codex agents folder; and copy `references/reviewer-protocol.md` into a stable Codex reference location such as `~/.codex/references/econ-agent-workflows/reviewer-protocol.md`.

### User-Level vs Project-Scoped Agents

For a small collaborator group, user-level installation is usually simplest: copy `.codex/agents/*.toml` into your personal Codex agents directory as shown above. Those reviewer agents will then be available across repositories.

For a specific empirical project, you can instead keep the reviewer agents project-scoped by copying `.codex/agents/*.toml` into that project's `.codex/agents/` directory. This keeps the panel tied to one project. The shared protocol should still be installed at `~/.codex/references/econ-agent-workflows/reviewer-protocol.md`, or passed by the parent `econ-review` prompt.

## Review Panel Behavior

Use `econ-review` directly for review work. It selects reviewer roles, tries to spawn the configured custom agents, merges their JSON findings, and presents a findings-first review.

For cleaning-heavy work, the default panel stays focused on provenance, specification, transformation/sample, and output consistency. If the target includes estimates, standard errors, causal claims, dynamic responses, table/figure interpretation, or cross-language validation, `econ-review` adds the relevant optional reviewers.

Cross-language validation is opt-in. Use `crosslang:plan` to prepare a validation handoff, or `crosslang:audit` to audit an existing validation manifest.

If the custom agents are not installed or subagent tools are unavailable, `econ-review` should say that the panel did not fully run. Quick or standard reviews may continue in a degraded mode with a warning. Promotion-grade reviews should not silently downgrade; they should stop or ask whether a degraded review is acceptable.

## Notes

This project is released under the MIT License. See `LICENSE`.

Before sharing outside a trusted collaborator group, re-audit the skill text for project-specific assumptions, confidential paths, or private workflow references.
