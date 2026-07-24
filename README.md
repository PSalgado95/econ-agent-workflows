# Econ Agent Workflows

Agentic workflows for economists, inspired by
[Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin).

The package adapts a plan → work → review → revise → compound loop to economic
research. It helps an agent preserve the research object, realised sample,
evidence trail, interpretation boundary, and reader-facing deliverable while
moving from an idea to reviewed work.

This is a beta. The workflows are strongest for empirical research—data
construction, estimation, tables, figures, notes, review bundles, and
reproducibility—but the same boundaries also apply to computational and
theory-facing work.

## Public workflow

The seven core skills are:

- **`econ-brainstorm`** turns a vague research idea into a bounded scope memo.
- **`econ-plan`** turns a clear task into a staged, reviewable research plan.
- **`econ-work`** executes a plan or concrete request while separating code
  changes, realised-output inspection, interpretation, reporting, and closeout.
- **`econ-review`** performs one report-only review over plans, implementation,
  empirical results, replication material, or a mixed evidence surface.
- **`econ-debug`** diagnoses anomalous empirical or computational results
  without silently changing the research object.
- **`econ-lfg`** runs the bounded plan → work → review → revise loop and pauses
  for researcher-level decisions.
- **`econ-compound`** records a durable research lesson only when bounded
  evidence supports it.

The package also contains one auxiliary skill, **`gpt-pro-handoff`**. It
activates only when the current user turn explicitly names the skill or
unambiguously requests an external GPT Pro handoff package. Core workflows do
not offer, recommend, prepare, or automatically route to a package. Reports,
blockers, prior turns, imported packages, and generated next steps cannot
activate it.

## One economics review, internal lenses

Users invoke `econ-review`; they do not choose or dispatch reviewers.

The skill contains 15 compact, skill-local review lenses:

1. provenance;
2. specification;
3. transformation and sample;
4. estimation practice;
5. inference;
6. output consistency;
7. claim discipline;
8. output perception;
9. code quality;
10. design;
11. dynamics;
12. robustness;
13. software equivalence;
14. reproducibility;
15. bundle quality.

`econ-review` selects the applicable lenses automatically from the requested
surface, depth, visible evidence, and promotion status. The list is a catalogue
of internal perspectives, not 15 commands or user-facing products. Necessary
lenses compose, and six is a cost target rather than a cap.

Cross-language and custom-implementation checks are folds across these lenses,
not separate reviewers. Cross-language work establishes object parity before
numeric parity and selects software equivalence plus the sample and
reproducibility lenses when those surfaces are material.

The review contracts live with the skill:

- `econ-review-request/v1` normalizes direct and nested requests;
- `econ-reviewer-output/v1` constrains one lens contribution;
- `econ-domain-assessment/v1` accepts supplemental domain evidence without
  treating it as another reviewer;
- `econ-review-report/v1` is the parent-owned final report.

The parent owns roster selection, child validation, stable finding IDs,
synthesis, coverage, verdict, and the promotion gate. Coverage is immutable
report evidence: missing, invalid, unavailable, failed, or timed-out required
lenses degrade the report rather than being relabelled away. Promotion passes
only with full coverage, an unchanged state canary, accepted required
assessments, and no unresolved blocking finding.

## Report-only and fail-closed

`econ-review` never edits reviewed files, applies fixes, changes repository
state, creates issues, or initiates another workflow.

Reviewer children run only when the host attests the effective child policy
after configuration precedence and live overrides:

- the workspace is hard read-only;
- approval or elevation cannot be granted;
- side-effecting connector, browser, computer-control, messaging, and similar
  tools are unavailable;
- the child cannot broaden the policy.

A prompt promise, configuration declaration, child self-report, or clean
post-run canary is not attestation. If the host cannot prove the preventive
boundary, the review fails closed: no child is dispatched, selected lenses are
unavailable, coverage is `not-run`, and promotion is blocked.

## Source layout

```text
skills/                         # canonical skill source
  econ-brainstorm/
  econ-plan/
  econ-work/
  econ-review/
    references/
      personas/                 # 15 internal review lenses
      *-schema.json             # four versioned contracts
  econ-debug/
  econ-lfg/
  econ-compound/
  auxiliary/
    gpt-pro-handoff/
tests/                          # contract and migration tests
claude/
  skills/                       # generated Claude Code skills; do not edit
build_claude.py                 # builds and checks claude/
install.py                      # Codex installer and health check
install_claude.py               # Claude Code installer and health check
check_install.py                # shared read-only install checker
```

Complete skill trees are the install unit. Personas, schemas, templates,
scripts, and skill-local references move together. There is no shared root
review-contract directory.

Claude Code discovers the generated skills directly under `claude/skills`.
The generated package has no duplicate command wrappers, no persona-bearing
reviewer agents, and no root review contracts.

## Verification

From the repository root:

```text
python -m unittest discover -s tests -v
python build_claude.py --check
```

Temporary-home install checks are safe and do not affect a live runtime:

```text
python install.py --codex-home <temporary-codex-home>
python install.py --codex-home <temporary-codex-home> --check

python install_claude.py --claude-home <temporary-claude-home>
python install_claude.py --claude-home <temporary-claude-home> --check
```

Maintainers regenerate Claude output only from canonical source:

```text
python build_claude.py
python build_claude.py --check
```

Never hand-edit `claude/`.

## Live-install gate

The source can be reviewed and merged now. A live `--force` installation of
this migration is blocked until the separately owned SSJ adapter:

1. emits `ssj-model-validity` through `econ-domain-assessment/v1`;
2. no longer requests a retired reviewer identity; and
3. passes the core request/report integration checks.

This gate matters because a forced migration removes the retired core reviewer
registrations while existing SSJ workflows may still depend on one. Do not run
a live forced install from this version before the adapter prerequisite passes.

After that prerequisite is accepted, install from the exact reviewed checkout:

```text
python install.py --force
python install.py --check
```

or, for Claude Code:

```text
python install_claude.py --force
python install_claude.py --check
```

Restart the relevant runtime after installation so its skill registry refreshes.
Repository edits do not update installed copies automatically.

## Migration boundary

Forced installation removes exactly 18 retired package-owned reviewer
identities: the 17 former specialist registrations and the later consolidated
registration. The Claude filenames are derived deterministically from that
literal list. Cleanup runs only under `--force`.

The migration does not use prefixes, globs, declared-name scans, or fuzzy
ownership rules. Every SSJ agent, unknown file, unrelated skill, and optional
persona-free read-only transport is outside the stale inventory and is
preserved. Historical Claude command wrappers and moved root contracts have
their own exact package-owned inventories.

See
[the 2026-07-24 persona-runtime migration note](docs/releases/2026-07-24-economics-review-persona-runtime.md)
for the exact retired identities and upgrade details.

## Source versus installed runtime

This repository is the source of truth. Installed copies under
`$CODEX_HOME/skills` or `~/.codex/skills`, and under
`$CLAUDE_CONFIG_DIR/skills` or `~/.claude/skills`, are runtime copies.

Edit repository source first, regenerate committed Claude output when needed,
run the contract suite, and use the installer only from the exact checkout that
should become active. Prefer explicit copy installation over symlinks so an
uncommitted source edit does not silently change runtime behaviour.
