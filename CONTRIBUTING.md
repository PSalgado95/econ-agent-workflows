# Contributing

This repository is a first-pass package of Codex skills and reviewer agents for economics workflows. It is small and experimental; contributions should keep it economist-facing and avoid turning it into a general agent-engineering framework.

## Good Contributions

- Make the skills clearer for economists.
- Improve generic examples and validation fixtures.
- Strengthen empirical traceability, data-construction review, econometric review, or reproducibility handoff.
- Keep reviewer agents narrow, read-only, and role-specific.
- Keep shared reviewer rules in `references/reviewer-protocol.md` rather than duplicating long protocol text across TOML files.

## Boundaries

- Do not add private project names, local paths, restricted-data references, server names, or confidential workflow details.
- Do not add real data or real research outputs to examples.
- Do not make econometrics-heavy reviewers always-on; role selection should remain evidence-triggered.
- Do not add `econ-compound` to the default package until it is ready.
- Do not add a Claude Code adapter unless it has been tested separately from the Codex install path.

## Review Checklist

Before opening a pull request:

- Run the private-context scan described in `docs/sharing-checklist.md`.
- Validate TOML agent files parse.
- Validate JSON schema files parse.
- Check that README installation instructions still match the package layout.
- Explain whether the change affects Codex-only behavior, portable protocol behavior, or future Claude Code adaptation.
