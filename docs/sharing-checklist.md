# Sharing Checklist

Use this before making the repository public or sending it to new collaborators.

## Required Before Public Release

- Confirm `LICENSE` matches the intended reuse terms.
- Decide whether the repository should remain private, become public, or stay private with selected collaborators.
- Re-run the private-context scan for local paths, private project names, server names, restricted-data references, and personal workflow details.
- Confirm that examples are generic and economist-native.
- Confirm the README says the package is Codex-first and portable in principle, not a fully packaged Claude Code release.

## Strongly Recommended

- Add one small example review bundle that contains no real project data.
- Add a short `CONTRIBUTING.md` if outside collaborators will propose changes.
- Add a version tag or release note once the first shared version feels stable.
- Add an install script only after the manual install instructions have been tested by another person.
- Keep `econ-compound` out of the default package until it is ready.

## Current Attribution

This workflow package is inspired by Compound Engineering, but it is not affiliated with Every and does not replace the original project:

https://github.com/EveryInc/compound-engineering-plugin

The adaptation here is empirical-economics-specific: planning, execution, review, traceability, data-construction checks, econometric review, and reproducibility handoff.
