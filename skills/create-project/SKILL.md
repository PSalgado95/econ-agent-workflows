---
name: create-project
description: "Create a sparse economics research project in the current folder, with local scaffold folders, minimal starter control files, and a private GitHub repository. Use when starting a new research repo or when the user asks to initialise a clean economics project workspace."
---

# Create Research Project

Use this skill to initialise a new economics research project in the current working directory. The skill is an execution workflow: it may create files, create local folders, initialise git, and create a private GitHub repository after safety checks pass.

Do not use this skill to retrofit a mature project, reorganise an existing repo, or import a full external template. If the folder already contains material, stop and ask before mutating anything.

## Core Principles

1. **Current folder is the project root** - Treat the current working directory as the intended project root unless the user explicitly says otherwise.
2. **Sparse tracked state** - Track only starter control files by default: `README.md`, `AGENTS.md`, and `.gitignore`.
3. **No stale project-state docs** - Do not create a tracked `docs/` folder. Do not persist the research idea, one-line purpose, or current empirical status in tracked files or GitHub issues unless the user explicitly asks.
4. **Scratch is organised but non-authoritative** - Put working plans, brainstorms, temporary memos, and notes under `scratch/docs/`. Put raw agent clutter under `scratch/agents/`.
5. **Raw data is protected** - Treat `data/raw/` as read-only. Derived data belongs in `data/processed/`. Generated tables, figures, logs, and results belong under `output/`.
6. **Private GitHub by default** - Create a private GitHub repository from the local folder name after showing the intended name and preflight summary.
7. **Ask before structural change** - If the user asks to alter the folder grammar, starter docs, data policy, or durable project-state handling, explain the consequence and ask before proceeding.

## Required Safety Checks

Before creating or changing files:

1. Resolve the current working directory and show it to the user.
2. Inspect top-level contents, including hidden entries.
3. If the folder is not empty, stop and show the top-level contents. Ask whether to proceed, adapt, or abort. Do not auto-continue.
4. If `.git/` already exists, stop and ask before reusing the repo.
5. If a git remote already exists, stop and ask before adding or changing a remote.
6. Check whether `gh` is available and authenticated before attempting private repo creation. If it is missing or unauthenticated, report the exact blocker and leave remote creation undone.
7. Before any GitHub command, show a concise preflight summary:
   - project root;
   - intended repository name;
   - privacy: private;
   - selected data-tracking policy;
   - tracked starter files;
   - local-only scaffold folders.

## Light Kickoff Questions

Ask only what is needed to create the scaffold safely:

1. **Project display name** - default to the current folder name.
2. **One-line purpose** - optional and transient. Use it only to orient the current session; do not write it into tracked files or GitHub issues by default.
3. **Data tracking policy** - ask the user to choose:
   - `ignore all data` - ignore both `data/raw/` and `data/processed/`;
   - `ignore raw only` - ignore `data/raw/` while allowing selected processed files to be tracked later.
4. **Folder deviations** - ask only if the user already indicated a deviation. Otherwise use the default scaffold.

If the user asks for a project-management issue, project brief, manuscript template, language-specific runner, or Zotero/citation setup, treat that as an explicit extension and ask before adding it.

## Default Local Scaffold

Create these folders locally:

```text
code/
data/raw/
data/processed/
output/logs/
output/figures/
output/tables/
output/results/
paper/
reference/
scratch/docs/plans/
scratch/docs/brainstorms/
scratch/docs/memos/
scratch/docs/notes/
scratch/agents/
```

Do not add placeholder files solely to make empty folders appear on GitHub. Empty folders can remain local until real project files exist.

## Starter Files

Use the assets in this skill as the starting point:

- `assets/README.md` -> `README.md`
- `assets/AGENTS.md` -> `AGENTS.md`
- `assets/gitignore-all-data.txt` or `assets/gitignore-raw-only.txt` -> `.gitignore`

Before writing, replace `<PROJECT_NAME>` with the project display name. Do not add the transient project purpose unless the user explicitly asks.

### README Role

`README.md` is a minimal index. It should map where things belong, not claim to describe the live empirical state.

### AGENTS Role

`AGENTS.md` is a brief behaviour contract. It should tell future agents how to avoid clutter and protect the research object. It is not a project brief.

## Git and GitHub Flow

After writing starter files and local folders:

1. Initialise git if no `.git/` exists and the user has approved the safety summary.
2. Stage only `README.md`, `AGENTS.md`, and `.gitignore` for the first commit.
3. Make an initial commit with a concise message such as `chore: initialise research project`.
4. Create a private GitHub repository with the folder name as the repository name.
5. Use GitHub CLI as the primary route when available. The intended shape is a private repository created from the existing local source and pushed after local commit.
6. If GitHub creation fails, report the exact failure and the local state. Do not claim that a remote exists.

Do not create GitHub issues, project boards, labels, or wiki pages by default.

## Closeout

End with:

- project root;
- GitHub repository URL, if created;
- data policy selected;
- starter files created;
- note that empty scaffold folders are local-only until real files exist;
- any blocker, if remote creation or git setup did not complete.

If the skill changed source files in the `econ-agent-workflows` package itself, remember that installed runtime copies are not updated until `python install.py --force` is run from the source checkout and Codex is restarted.
