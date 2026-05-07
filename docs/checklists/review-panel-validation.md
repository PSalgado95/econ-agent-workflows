# Review Panel Validation Checklist

Use this checklist after changing `econ-review`, the reviewer protocol, or custom reviewer agents.

## Package Shape

- `skills/econ-review/SKILL.md` says direct invocation tries to run the subagent review panel.
- `references/reviewer-protocol.md` contains the shared role catalogue, evidence rules, finding taxonomy, and JSON schema.
- `.codex/agents/` contains one custom TOML agent per reviewer role.
- `README.md` installs `econ-plan`, `econ-work`, and `econ-review`, but not a user-facing `econ-reviewer` skill.

## Agent Files

- Every `.codex/agents/*.toml` file defines `name`, `description`, and `developer_instructions`.
- Reviewer agents are read-only.
- Reviewer agents say to return JSON only.
- Reviewer agent names match the role-to-agent mapping in `skills/econ-review/references/review_reference.md`.
- Reviewer agents prefer the parent-supplied protocol excerpt and evidence manifest before looking for local protocol files.

## Review Behavior

- `surface:plan` uses a smaller panel and reports reviewability only.
- `surface:results` uses the default empirical trust panel.
- `surface:note`, `surface:mixed`, and note-facing bundles include claim discipline and the reader-facing note gate.
- Parent `econ-review` builds and passes a compact evidence manifest to every reviewer prompt.
- Missing diagnostic surfaces become diagnostic gaps rather than soft caveats.
- Malformed reviewer JSON is discarded or quarantined by the parent.

## Degraded Mode

- Quick degraded reviews are labelled.
- Standard degraded reviews include an explicit warning and missing-role list.
- Promotion degraded reviews stop or require explicit user acceptance.
- Headless promotion degraded reviews return a degraded verdict rather than certifying readiness.

## Packaging Audit

- No local absolute paths appear in package text.
- No private project names appear in examples.
- No license file is added without an explicit license decision.
- README explains both user-level and project-scoped reviewer-agent installation.
- README makes clear that first-time installs use `econ-review`, not a separate `econ-reviewer` skill.
- The original local Codex skill folders outside this repository were not edited.
