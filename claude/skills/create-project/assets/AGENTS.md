<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources (skills/, .codex/agents/, references/) and run build_claude.py. -->

# Local Agent Instructions

## Working Style

- Write for an economist. Use plain research language.
- Keep the economics and measurement object visible.
- Do not turn `README.md` into a live empirical-status memo.

## Folder Rules

- Use `code/` for analysis code and project helpers.
- Treat `data/raw/` as read-only.
- Write derived data to `data/processed/`.
- Write generated results, tables, figures, and logs under `output/`.
- Use `paper/` for paper draft material when needed.
- Use `reference/` for papers, manuals, codebooks, and other reference material.
- Put working plans, brainstorms, temporary memos, and notes under `scratch/docs/`.
- Put raw agent clutter such as screenshots, package stages, return extracts, and raw logs under `scratch/agents/`.

## Consent Rules

Ask before changing:

- folder structure;
- main run files;
- data definitions;
- key research parameters;
- `README.md` or this `AGENTS.md`;
- whether scratch material should become tracked project documentation.

