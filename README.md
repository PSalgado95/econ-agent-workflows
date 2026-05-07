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
- `econ-review`: reviews empirical plans, results, bundles, notes, diffs, or mixed work surfaces. It focuses on trust, promotion risk, missing diagnostics, and reader-facing claim discipline.
- `econ-reviewer`: runs one structured reviewer lens for `econ-review` and returns machine-readable findings.

## Folder Structure

```text
skills/
  econ-plan/
  econ-work/
  econ-review/
  econ-reviewer/
README.md
```

## Installation

Copy the skill folders into your local Codex skills directory.

On Windows, this is typically:

```powershell
Copy-Item -Recurse .\skills\econ-plan $env:USERPROFILE\.codex\skills\econ-plan
Copy-Item -Recurse .\skills\econ-work $env:USERPROFILE\.codex\skills\econ-work
Copy-Item -Recurse .\skills\econ-review $env:USERPROFILE\.codex\skills\econ-review
Copy-Item -Recurse .\skills\econ-reviewer $env:USERPROFILE\.codex\skills\econ-reviewer
```

On macOS or Linux, this is typically:

```bash
cp -R skills/econ-plan ~/.codex/skills/econ-plan
cp -R skills/econ-work ~/.codex/skills/econ-work
cp -R skills/econ-review ~/.codex/skills/econ-review
cp -R skills/econ-reviewer ~/.codex/skills/econ-reviewer
```

Restart Codex after copying the folders so the skills are loaded.

## Notes

No license file is included yet. Add one only after deciding how collaborators should be allowed to use, modify, and redistribute the package.

Before sharing outside a trusted collaborator group, re-audit the skill text for project-specific assumptions, confidential paths, or private workflow references.
