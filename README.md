# Econ Agent Workflows

Research workflows for economists, inspired by
[Compound Engineering](https://github.com/EveryInc/compound-engineering-plugin).

It consists of a set of skills that structure the use of AI agents across the
full research process, from developing an idea and writing a plan to carrying
out the analysis, reviewing the evidence, and revising the work. Verified
lessons from completed projects are carried into later work, allowing
successful methods and solutions to accumulate across projects.

```text
brainstorm → plan → work → review → revise → compound
```

Most development so far has come from empirical applications, including data
construction, estimation, figures, tables, research notes, and replication.
The skills can also be used for computational and theory-based research,
although these applications have received less testing.

## The research workflow

The five core skills cover distinct parts of this process. They can be used
separately or combined as the research develops.

| Research task | Skill | What it does |
| --- | --- | --- |
| Explore a research idea | `econ-brainstorm` | Helps the researcher work out what they want to investigate |
| Plan the research | `econ-plan` | Turns an idea or concrete task into a sequence of research steps |
| Carry out the analysis | `econ-work` | Works through data, code, models, results, and their interpretation |
| Review the research | `econ-review` | Checks the design, evidence, results, and claims |
| Carry lessons into later work | `econ-compound` | Retains verified lessons from completed research for use in later projects |

Two additional skills support the core workflow. `econ-debug` investigates
unexpected empirical or computational results. `econ-lfg` coordinates the full
cycle for a defined research task, pausing when a decision would change the
research question, empirical design, interpretation, or scope.

An auxiliary skill, `gpt-pro-handoff`, prepares an external GPT Pro review
package when the researcher explicitly requests one.

## The review process

`econ-review` selects the checks that fit the research task and the available
evidence. Depending on the material, it examines:

- whether the data sources, transformations, and realised sample are clear;
- whether the specification answers the stated research question;
- whether estimation and inference are appropriate;
- whether dynamics and robustness support the interpretation;
- whether tables, figures, code, and written claims agree; and
- whether the analysis can be reproduced from the supplied material.

When useful and authorised, the work stage can prepare an independent
implementation of selected results in another programming language. The review
then inspects the supplied comparison of samples, variables, estimates, tables,
and figures. Reviewers do not create scripts or run new replications: they are
report-only. Cross-language work is a targeted diagnostic, not a default
requirement.

The researcher explicitly selects `econ-review`, or requests an end-to-end
`econ-lfg` run that includes it. Ordinary checking and debugging do not silently
activate the formal workflow. The coordinator retains the broader research task.

Review lenses describe coverage, not a roster of child agents. The coordinator
can cover them directly or delegate related checks together. The delegation
reference in `skills/econ-work/references/delegation_reference.md` governs both
work and review: Sol Low is a useful supporting default, Luna handles easy
searches with effort chosen for the task, and stronger independent judgment is
used selectively. Other hosts use available equivalents. Each run distinguishes
parent checks from independent checks and records worker settings and budgets.

Reports use `econ-review-report/v3`; v2 reports must not be silently reinterpreted
because their coverage does not distinguish parent and worker checks.

## Installation

The skills are model-agnostic. This repository currently provides installers
for Codex and Claude Code.

To install or update the Codex skills:

```text
python install.py --force
python install.py --check
```

To install or update the Claude Code skills:

```text
python install_claude.py --force
python install_claude.py --check
```

Restart the relevant application after installation so it reloads the skills.

## For contributors

### Source layout

```text
skills/                         # canonical skill source
  econ-brainstorm/
  econ-plan/
  econ-work/
  econ-review/
    references/
      personas/                 # internal specialist review perspectives
      *-schema.json             # review contracts
  econ-debug/
  econ-lfg/
  econ-compound/
  auxiliary/
    gpt-pro-handoff/
tests/                          # contract and installation tests
claude/
  skills/                       # generated Claude Code skills; do not edit
build_claude.py                 # builds and checks claude/
install.py                      # Codex installer and health check
install_claude.py               # Claude Code installer and health check
check_install.py                # shared read-only installation check
```

The repository is the source of truth. Installed skill directories are runtime
copies and do not update automatically when the repository changes.

Edit the source under `skills/`, regenerate the committed Claude output when
needed, run the tests, and then install from the exact checkout that should
become active. Do not edit generated files under `claude/` directly.

### Verification

Run the contract suite and verify the generated Claude package from the
repository root:

```text
python -m pip install jsonschema
python -m unittest discover -s tests -v
python build_claude.py --check
```
