<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources (skills/, .codex/agents/, references/) and run build_claude.py. -->

# Return-contract patterns

Use these patterns to ask for more reliable outputs without making the prompt heavy.

The rule is simple:

- keep the human ask in the prompt;
- move the exact artefact contract into a dedicated file only when it is doing real work.

## Pattern 1: memo only

### Use when

- one audience
- one main deliverable
- no revised files
- no machine-readable appendix needed

### Prompt shape

State the deliverable directly in the prompt.

### Typical contract

```text
Return exactly 1 deliverable: a structured memo for [audience].
```

### Required sections

- bottom line
- main reasoning
- objections or trade-offs
- uncertainty
- next steps

## Pattern 2: memo plus prioritised changes

### Use when

- the task is critique or redesign
- the user wants both diagnosis and concrete fixes

### Prompt shape

Still small enough to keep in the prompt.

### Typical contract

```text
Return exactly 2 deliverables:
1. a concise assessment memo;
2. a prioritised revision brief.
```

## Pattern 3: memo plus machine appendix

### Use when

- the task has a human audience but also needs a structured appendix
- the user wants archetypes, schemas, file maps, or rule inventories

### Recommended contract location

Prompt plus small `return_contract.yaml` when the machine appendix needs a schema.

### Typical files

- `summary.md`
- `machine_appendix.yaml` or `machine_appendix.json`

### Why use it

It keeps the human memo readable while giving downstream workflows something structured.

## Pattern 4: revision bundle

### Use when

- GPT Pro must revise draft text
- the user wants both output text and revision accounting

### Recommended contract location

`source/package/return_contract.md`

### Typical files

- `00_summary.md`
- revised main text
- `change_log.md`
- `open_issues.md`

### Recommended rules

- separate what was changed now from what remains unresolved
- keep writing guidance in the prompt
- keep exact filenames and file-by-file duties in the return contract

## Pattern 5: patch bundle

### Use when

- the task is hybrid research plus implementation
- revised files or diffs matter
- the user wants economist-facing and implementation-facing outputs separately

### Recommended contract location

`source/package/return_contract.md`

### Typical files

- `00_summary.md`
- economist-facing memo
- `technical_annex.md`
- `code_change_guide.md`
- revised file(s)
- `patches/*.diff`

### Optional files

- diagnostics plan
- variable semantics table
- register update note

### Recommended rules

- state no-change rules explicitly
- separate local fixes from deferred follow-up work
- keep scope bounded to the stated implementation surface

## Pattern 6: binding bundle with filenames

### Use when

- filenames matter downstream
- GPT Pro may otherwise return the right substance in the wrong shape
- the user wants install-ready or upload-ready artefacts

### Recommended contract location

`source/package/return_contract.md` or `.yaml`

### Include

- exact filenames
- required / optional files
- section expectations
- no-change rules
- bundle naming rule if needed

### Keep out of the prompt

Avoid pasting long filename lists directly into the prompt unless the whole task is about the file inventory itself.

## Markdown versus YAML

### Prefer Markdown when

- the contract needs prose explanation;
- writing standards matter;
- or each file has a richer semantic role.

### Prefer YAML when

- the contract is mostly structural;
- GPT Pro must also return a machine-facing appendix;
- or the user wants compact rules, archetype definitions, or decision logic.

## Minimal return-contract skeleton

### Markdown

```text
# Return Contract

## Required deliverables
- `00_summary.md`
- `technical_annex.md`

## File roles
- `00_summary.md`: short reader-facing summary
- `technical_annex.md`: evidence and implementation detail

## Rules
- Keep scope bounded to ...
- Do not revise ...
```

### YAML

```yaml
required_files:
  - 00_summary.md
  - machine_appendix.yaml
rules:
  - keep scope bounded
  - separate accepted changes from deferred work
```

## Good practice

- Use a return contract only when it reduces ambiguity.
- Strengthen the contract as the task becomes more implementation-facing.
- Keep the prompt readable even when the contract is strong.
- Let the archetype determine the default contract pattern.
