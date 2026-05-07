# Econ Agent Workflows

Small Codex workflows for economists, inspired by [Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin).

The goal was to take the plan/work/review discipline that Compound Engineering makes natural for software projects and adapt it to how economists work. This is not a replacement for Compound Engineering, and it is not affiliated with Every. If you want the general engineering workflow, use Compound Engineering directly. This repo is a small economics-specific adaptation.

At this stage, the package is most developed for empirical projects: data cleaning, sample construction, estimation, tables, figures, notes, review bundles, and reproducibility handoffs. Some pieces may also be useful for structural work, model-building, calibration, simulation, or other economics workflows, but those paths are less tested.

The package is organized around a simple research workflow:

1. plan the empirical task;
2. execute the code, checks, outputs, and interpretation work;
3. review the plan, outputs, bundle, or note before trusting or promoting results;
4. keep empirical traceability explicit throughout.

The skills are meant for economists working with data, estimation, tables, figures, notes, replication material, and hybrid analysis-engineering projects.

The package is currently designed for Codex skills and Codex custom agents. The architecture is intentionally portable: the same division between a parent review workflow, role-specific reviewers, and a shared reviewer protocol can be adapted for Claude Code or other agent runtimes, but those adapters are not packaged here yet.

## Skills

- `econ-plan`: turns an empirical or hybrid research task into a staged plan. It makes the reader, reporting class, bottleneck, evidence surface, execution stages, and review route explicit.
- `econ-work`: executes empirical or hybrid work from a saved plan or clear request. It separates code execution, output inspection, interpretation, note preparation, and closeout.
- `econ-review`: reviews empirical plans, results, bundles, notes, diffs, or mixed work surfaces. Direct invocation means "try to run the economist review panel" using the included Codex custom reviewer agents.

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
LICENSE
README.md
```

## Installation

Copy the skill folders into your local Codex skills directory, copy the reviewer agents into Codex's agent configuration, and copy the shared reviewer protocol into a stable Codex reference location.

On Windows, this is typically:

```powershell
New-Item -ItemType Directory -Force $env:USERPROFILE\.codex\skills | Out-Null
New-Item -ItemType Directory -Force $env:USERPROFILE\.codex\agents | Out-Null
New-Item -ItemType Directory -Force $env:USERPROFILE\.codex\references\econ-agent-workflows | Out-Null

Copy-Item -Recurse .\skills\econ-plan $env:USERPROFILE\.codex\skills\econ-plan
Copy-Item -Recurse .\skills\econ-work $env:USERPROFILE\.codex\skills\econ-work
Copy-Item -Recurse .\skills\econ-review $env:USERPROFILE\.codex\skills\econ-review

Copy-Item .\.codex\agents\*.toml $env:USERPROFILE\.codex\agents\
Copy-Item .\references\reviewer-protocol.md $env:USERPROFILE\.codex\references\econ-agent-workflows\reviewer-protocol.md
```

On macOS or Linux, this is typically:

```bash
mkdir -p ~/.codex/skills ~/.codex/agents ~/.codex/references/econ-agent-workflows

cp -R skills/econ-plan ~/.codex/skills/econ-plan
cp -R skills/econ-work ~/.codex/skills/econ-work
cp -R skills/econ-review ~/.codex/skills/econ-review

cp .codex/agents/*.toml ~/.codex/agents/
cp references/reviewer-protocol.md ~/.codex/references/econ-agent-workflows/reviewer-protocol.md
```

Restart Codex after copying the folders so the skills and custom agents are loaded.

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
