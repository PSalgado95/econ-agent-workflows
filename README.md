# Econ Agent Workflows

Codex skills for empirical economics workflows.

This package is organized around a simple research workflow:

1. plan the empirical task;
2. execute the code, checks, outputs, and interpretation work;
3. review the plan, outputs, bundle, or note before trusting or promoting results;
4. keep empirical traceability explicit throughout.

The skills are meant for economists working with data, estimation, tables, figures, notes, replication material, and hybrid analysis-engineering projects.

## Skills

- `econ-plan`: turns an empirical or hybrid research task into a staged plan. It makes the reader, reporting class, bottleneck, evidence surface, execution stages, and review route explicit.
- `econ-work`: executes empirical or hybrid work from a saved plan or clear request. It separates code execution, output inspection, interpretation, note preparation, and closeout.
- `econ-review`: reviews empirical plans, results, bundles, notes, diffs, or mixed work surfaces. Direct invocation means "try to run the economist review panel" using the included Codex custom reviewer agents.

This package does not install `econ-reviewer` as a separate user-facing skill. Reviewer lenses live as custom agents under `.codex/agents/`, with shared rules in `references/reviewer-protocol.md`.

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
docs/
  examples/
  plans/
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

### Note on `econ-reviewer`

This first shared version does not install `econ-reviewer` as a separate skill. Use `econ-review`; the reviewer lenses are packaged as custom agents.

## Review Panel Behavior

Use `econ-review` directly for review work. It selects reviewer roles, tries to spawn the configured custom agents, merges their JSON findings, and presents a findings-first review.

If the custom agents are not installed or subagent tools are unavailable, `econ-review` should say that the panel did not fully run. Quick or standard reviews may continue in a degraded mode with a warning. Promotion-grade reviews should not silently downgrade; they should stop or ask whether a degraded review is acceptable.

## Notes

No license file is included yet. Add one only after deciding how collaborators should be allowed to use, modify, and redistribute the package.

Before sharing outside a trusted collaborator group, re-audit the skill text for project-specific assumptions, confidential paths, or private workflow references.
