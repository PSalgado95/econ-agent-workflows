# Examples

Use these as compact pattern references. They are not templates to copy blindly.

## Example 1: lean review for an empirical research task

### User request

```text
Use $gpt-pro-handoff to prepare a package for GPT Pro. I want an economist-facing review of our local-projections result package, with emphasis on identification, mechanisms, and the strongest objections.
```

### Chosen mode and archetype

- Mode: lean
- Archetype: lean review / critique

### Likely include set

- active workflow note
- one config or design note
- one decisive result table or figure
- one short note on what changed most recently

### Likely prompt emphasis

- interpret the result
- assess identification logic
- separate mechanism from artefact
- recommend the next robustness checks

### Likely return contract

- short memo
- prioritised follow-up checks

## Example 2: staged writing / revision for a paper round

### User request

```text
Use $gpt-pro-handoff to prepare a GPT Pro package for revising our referee-response round. Include the referee letter, our current draft section, the latest response notes, and the style constraints for the paper.
```

### Chosen mode and archetype

- Mode: staged
- Archetype: staged writing / revision

### Recommended stage-workspace layout

```text
package/
  governing_direction.md
  return_contract.md
drafts/
  current_section_draft.md
evidence/
  referee_letter.md
  latest_response_notes.md
shared/
  paper_style_note.md
```

### Likely prompt emphasis

- keep the main voice economist-facing
- separate what is revised now from what remains open
- preserve scope on the targeted section rather than rewriting the whole paper

### Likely return contract

- summary note
- revised text
- change log
- unresolved issues note

## Example 3: staged hybrid research-implementation task

### User request

```text
Use $gpt-pro-handoff to prepare a GPT Pro package for deciding the right payment-measurement fix and turning it into a bounded implementation plan. The package should include the live code surface, the prior audit note, and the current issue direction.
```

### Chosen mode and archetype

- Mode: staged
- Archetype: staged hybrid research-implementation

### Recommended stage-workspace layout

```text
package/
  governing_direction.md
  repo_scan.md
  return_contract.md
evidence/
  prior_audit_note.md
code/
  live_measurement_file.do
  downstream_household_file.do
shared/
  variable_register.md
discussion/
  issue_state.md
```

### Likely prompt emphasis

- distinguish economic object first and variable names second
- keep the implementation bounded
- separate economist-facing reasoning from code-facing guidance

### Likely return contract

- short economist-facing memo
- technical annex
- code change guide
- revised file or diff
- optional diagnostics plan

## Example policy

These examples are deliberately compact and archetype-oriented.

Use them to answer:

- which mode should this task use;
- what role folders are justified;
- and how strong the return contract should be.

Do not use them to copy field names, repo-specific conventions, or historical package idiosyncrasies into unrelated tasks.
