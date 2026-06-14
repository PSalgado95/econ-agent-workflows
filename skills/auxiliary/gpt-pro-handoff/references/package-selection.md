# Package selection and staging heuristics

Use these rules to keep the handoff package useful without overwhelming GPT Pro.

## 1. Decide mode first

Before selecting files, decide whether the task is `lean` or `staged`.

- Lean mode is for a narrow question with a small decisive evidence set.
- Staged mode is for mixed artefact classes, stronger scope control, or binding implementation-style outputs.

Do not solve a staging problem by making the prompt longer.

## 2. Curate by role

Think in roles, not only in paths.

### Governing context

Include first:

- short workflow notes;
- README or project overview;
- scope note;
- distilled direction;
- one note that explains what the artefacts are.

### Core evidence

Include:

- the one or two strongest tables, figures, or memos;
- the decisive draft or results note;
- the minimal code or workflow files needed to interpret the issue;
- and compact extracted notes when the raw source is bulky.

### Minimal traceability

Include:

- one manifest;
- one brief;
- one config or metadata file when it materially clarifies provenance;
- and a return-contract file only when the output shape actually matters.

## 3. Lean-package guidance

### Typical size discipline

Use lean mode when you can usually stay around:

- about 6 to 12 decisive source files;
- a compact readable brief and manifest;
- and one prompt that can fit on one screen without becoming a wall of text.

### What lean packages do well

- critique;
- comparison;
- plan review;
- empirical interpretation;
- bounded design questions.

### What to avoid in lean packages

- raw issue-thread dumps;
- code folders plus draft folders plus discussion folders all at once;
- long binding filename contracts;
- and broad background material that is not directly decision-relevant.

## 4. Staged-package guidance

Use staged mode when different materials play genuinely different jobs.

### Stage-workspace pattern

Create a temporary stage workspace with role folders at the workspace root:

```text
<stage_workspace>/
  package/
  evidence/
  code/
  shared/
  discussion/
  drafts/
  examples/
```

The current packaging script will then copy them into final:

```text
source/package/
source/evidence/
source/code/
...
```

Do not create a nested local `source/` folder in the stage workspace unless you intentionally want `source/source/...` later.

### When staged structure pays off

- GPT Pro must move from diagnosis to implementation;
- the live code surface should not be confused with earlier discussion;
- the package contains both prior returns and current source files;
- or the user wants both economist-facing and implementation-facing outputs.

### Staged-package discipline

Even staged packages must stay curated.

Use role folders to separate material, not to justify shipping everything.

## 5. Folder handling

If the user points to a folder:

- treat it as a candidate pool, not an instruction to copy the whole folder;
- pull the strongest files from inside it;
- prefer summary files over raw subfolders;
- and mention omitted siblings in the manifest when they are relevant.

For staged packages, only include a full role folder when the whole curated role folder is itself the point.

## 6. Condense instead of copy

When many files say nearly the same thing:

- keep one representative file;
- summarise the rest in `handoff_brief.md`;
- and note the omitted set in `package_manifest.md`.

When the raw material is too bulky but still important:

- extract the decisive pages, sections, or tables;
- render chart-heavy notes to PDF when visuals matter;
- export decisive tables from large workbooks;
- and include a short note that explains provenance or sampling.

## 7. Code and workflow files

For hybrid tasks:

- include only the live execution surface;
- include helper files only when they materially affect the object under review;
- prefer a small `repo_scan.md` in `source/package/` over a large code dump;
- and separate current live code from deferred or historical code.

## 8. Examples

Examples are useful only when they clarify the archetype.

Include compact examples when:

- the user is asking for redesign of a reusable workflow;
- the package needs a lean-versus-staged contrast;
- or the return-contract pattern is non-obvious.

Do not default to shipping full historical bespoke packages. Abstract the pattern unless the old package itself is under review.

## 9. Soft limits

Treat these as judgement guides rather than laws.

### Lean

- usually about 6 to 12 source files
- strongly prefer concise prompts and a flat package

### Staged

- usually about 12 to 30 curated source files across roles
- strong role separation is more important than raw file count
- still prefer smaller rendered or extracted files over giant raw folders

If the package keeps expanding beyond that, the question is usually not "can GPT Pro handle more?", but "have we stopped curating?"

## 10. Omission language

Use simple reasons in the manifest:

- omitted to keep the package lean
- omitted because it duplicated stronger included evidence
- omitted because it exceeded the file-size guardrail
- omitted because it was likely irrelevant to the stated task
- omitted because the staged role was already represented by a stronger file
- missing from the requested path

## 11. Final check

Before packaging, ask:

1. does each included file play a distinct role?
2. is the package mode correct?
3. could a shorter reading order achieve the same result?
4. are the human ask and machine return contract separated cleanly?
5. would a future reader understand why each file is here?

If not, recurate before zipping.
