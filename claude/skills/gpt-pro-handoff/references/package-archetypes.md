<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources (skills/, .codex/agents/, references/) and run build_claude.py. -->

# Package archetypes

Use these archetypes to decide how much structure the package should have.

The aim is not to create many templates. The aim is to recognise when the task has crossed a threshold where stronger package structure is useful.

## Default rule

- Start from the leanest package that can carry the task cleanly.
- Escalate to a staged package when the package needs role separation, a stronger reading order, or a binding return contract.
- Allow explicit user override, but otherwise choose automatically.

## Decision rule

### Choose lean when all are true

- one central question;
- one main audience;
- the answer is mainly analysis, critique, interpretation, or bounded planning;
- no revised-file bundle or patch set is required;
- the decisive source set is small and easy to inspect.

### Choose staged when any two are true

- multiple deliverables or audiences;
- revised files, diffs, or named artefacts are required;
- materials span code, discussion, drafts, data, and references;
- prior rounds or issue history materially govern the task;
- reading order matters;
- scope boundaries need reinforcement;
- the cost of a wrong action is high.

## Archetype 1: lean review / critique

### Best for

- skill review
- empirical design critique
- bounded interpretation
- comparison of two outputs, plans, or prompts

### Default package shape

```text
handoff_brief.md
handoff_prompt.txt
package_manifest.md
source/
  [small decisive file set]
```

### Typical return

- short memo
- prioritised objections or changes

### Signs you should escalate

- the prompt starts carrying implementation rules
- you need several audiences
- the package begins to mix raw discussion, code, and prior returns

## Archetype 2: lean plan / design

### Best for

- workflow redesign
- prompt redesign
- package design
- prioritisation notes
- design choice comparison

### Default package shape

Same as lean review, but often with one more explicit planning artefact or comparison note.

### Typical return

- assessment memo
- revision brief
- prioritised design changes

### Special note

Keep the planning ask human-readable. Use a machine appendix only if the user explicitly wants schemas, inventories, or structured rules.

## Archetype 3: staged evidence synthesis

### Best for

- research synthesis across several evidence types
- literature positioning with repo-specific material
- empirical framing that mixes notes, tables, methods, and external references

### Default stage-workspace shape

```text
package/
  governing_direction.md
  reading_order.md
  return_contract.yaml
evidence/
shared/
examples/
```

### Final uploaded shape

```text
source/package/
source/evidence/
source/shared/
source/examples/
```

### Typical return

- human-facing memo
- machine-facing appendix
- evidence table or issue map

### Why staged helps

The package should not leave GPT Pro to infer which evidence is authoritative or what bundle shape is required.

## Archetype 4: staged writing / revision

### Best for

- paper revision
- referee response
- rewrite of a draft plus issue table
- revision rounds where evidence and style constraints matter separately

### Default stage-workspace shape

```text
package/
drafts/
evidence/
shared/
examples/
```

### Typical return

- revised text
- summary memo
- change log
- unresolved issues note

### Why staged helps

Drafts, evidence, and style constraints play different roles and should not compete in one flat folder.

## Archetype 5: staged hybrid research-implementation

### Best for

- measurement fixes
- code-path adjudication
- patch design
- empirical-analysis-plus-implementation tasks
- situations where both economist-facing and implementation-facing outputs matter

### Default stage-workspace shape

```text
package/
  governing_direction.md
  repo_scan.md
  return_contract.md
code/
evidence/
discussion/
shared/
```

### Typical return

- economist-facing memo
- technical annex
- code change guide
- revised file(s) or diffs
- diagnostics plan when useful

### Why staged helps

The package needs explicit separation between:

- what the issue currently is;
- what prior analysis already established;
- and where the live implementation surface actually sits.

## Reading-order rule by archetype

### Lean review / lean plan

The prompt can carry the reading order directly.

### Staged synthesis / staged revision / staged hybrid

Prefer:

1. `handoff_brief.md`
2. `package_manifest.md`
3. `source/package/`
4. then role folders in the intended order

## Return-contract strength by archetype

| Archetype | Return-contract strength |
|---|---|
| Lean review | light |
| Lean plan | light to medium |
| Staged synthesis | medium |
| Staged revision | medium to strong |
| Staged hybrid patch | strong |

Use stronger contracts only when the output shape must be reproducible.

## Examples policy

Keep examples at pattern level.

Recommended example set inside the reusable skill:

- one lean review example;
- one staged synthesis or revision example;
- one staged hybrid implementation example.

Do not embed full historical bespoke packages as defaults. Their job is to teach threshold recognition, not to become hidden templates.
