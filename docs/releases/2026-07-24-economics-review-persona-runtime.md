# Economics review persona runtime migration

Date: 2026-07-24

## Summary

Economics review now has one public workflow, `econ-review`, with 15 internal,
skill-local review lenses selected automatically from the requested surface and
evidence. The migration removes both earlier generations of persona-bearing
reviewer registrations: 17 specialist agents and the later consolidated
reviewer.

This simplifies the public workflow without weakening review coverage. The
parent still composes the relevant lenses for provenance, specification,
sample construction, estimation, inference, outputs, claims, code, design,
dynamics, robustness, equivalence, reproducibility, and bundle quality. Users
do not choose among the lenses.

## Public package

The package contains seven core skills:

- `econ-brainstorm`
- `econ-plan`
- `econ-work`
- `econ-review`
- `econ-debug`
- `econ-lfg`
- `econ-compound`

`gpt-pro-handoff` remains an auxiliary skill. It activates only when the
current user turn explicitly names it or unambiguously requests an external GPT
Pro handoff package. No core workflow offers, recommends, prepares, or
automatically routes to a package.

## Review contracts

`econ-review` owns four versioned contracts:

- `econ-review-request/v1`
- `econ-reviewer-output/v1`
- `econ-domain-assessment/v1`
- `econ-review-report/v1`

Direct and nested calls normalize to the same request envelope. A generic child
returns one role-scoped reviewer output. Supplemental domain work enters as an
assessment, not as another reviewer. The parent alone assigns stable finding
IDs, synthesizes disagreements, derives immutable coverage, issues the verdict,
and decides the promotion gate.

Unknown request versions fail before selection or dispatch. An unknown child
version invalidates that lens only. An unknown domain-assessment version is
recorded as unsupported. A caller receiving an unknown final-report version
must preserve the raw payload, report `unsupported_report_version`, and stop.

## Preventive safety boundary

Review remains report-only. A child may run only when the host attests the
effective policy after configuration precedence and live overrides:

- a hard read-only workspace;
- no approval or elevation path;
- no side-effecting connector, browser, computer-control, messaging, or
  equivalent tool surface;
- no way for the child to broaden the policy.

Prompt instructions, declared configuration, child self-report, and a clean
post-run canary are not sufficient attestation. Without a proven boundary,
dispatch does not occur, coverage is `not-run`, the verdict is blocked, and
promotion cannot pass.

Coverage cannot be upgraded by a caller. Missing, invalid, failed, timed-out,
cancelled, or unavailable selected lenses degrade coverage. Promotion requires
full coverage, an unchanged state canary, accepted required assessments, and no
unresolved blocking finding.

## Skill-local installation

Personas, schemas, protocols, templates, and method guardrails now live inside
the skills that consume them. Installers copy complete skill trees recursively.
The former shared root review-contract directory is retired.

The generated Claude Code package contains directly invocable skills under
`claude/skills`. It contains:

- zero duplicate command wrappers;
- zero persona-bearing economics reviewer agents;
- zero root review contracts.

Claude output is generated only through `python build_claude.py`; it is never
edited by hand.

## Exact retired reviewer inventory

Forced installation removes exactly these 18 package-owned Codex filenames:

```text
econ-bundle-reviewer.toml
econ-claim-discipline-reviewer.toml
econ-code-quality-reviewer.toml
econ-cross-language-validation-reviewer.toml
econ-design-reviewer.toml
econ-dynamics-reviewer.toml
econ-estimation-practice-reviewer.toml
econ-hybrid-implementation-reviewer.toml
econ-inference-reviewer.toml
econ-output-consistency-reviewer.toml
econ-output-perception-reviewer.toml
econ-provenance-reviewer.toml
econ-reproducibility-reviewer.toml
econ-robustness-reviewer.toml
econ-software-equivalence-reviewer.toml
econ-specification-reviewer.toml
econ-transformation-sample-reviewer.toml
econ-reviewer.toml
```

Each retired Claude filename is derived deterministically as:

```text
Path(codex_filename).stem.replace("-", "_") + ".md"
```

The deletion inventory is literal. It is not a prefix, suffix, glob,
declared-name scan, or fuzzy ownership rule. Cleanup runs only under `--force`.
A non-force install deletes nothing.

The following are explicitly outside the retired reviewer inventory:

- `econ-review-readonly-transport.toml`;
- `econ_review_readonly_transport.md`;
- every `econ-ssj-*` or `econ_ssj_*` agent;
- every unknown or unrelated agent.

Those files are preserved byte-for-byte. Historical Claude wrappers, the old
`econ-reviewer` skill directory, and moved root contracts use separate exact
package-owned inventories. Unknown commands, references, and skills remain
untouched.

## Verification

Run from the repository root:

```text
python -m unittest discover -s tests -v
python build_claude.py --check
```

The test suite covers:

- catalogue resolution for exactly 15 personas;
- the 17-specialist responsibility crosswalk and folded roles;
- all four Draft 2020-12 schemas and representative payloads;
- deterministic roster ordering and queue semantics;
- wrapper salvage and invalid child outcomes;
- immutable coverage, verdict, and promotion rules;
- current-user-only handoff activation;
- complete skill-local reference resolution;
- generated-source parity;
- fresh, damaged, non-force, force, and repeated-force temporary installs;
- byte preservation for SSJ, optional transport, unknown agents, references,
  commands, and skills.

Temporary runtime checks may use:

```text
python install.py --codex-home <temporary-codex-home>
python install.py --codex-home <temporary-codex-home> --check

python install_claude.py --claude-home <temporary-claude-home>
python install_claude.py --claude-home <temporary-claude-home> --check
```

These commands do not touch a live installation.

The separate agent-native release smoke is:

```text
python tests/run_agent_native_smoke.py --host codex --checkout . --result-path <agent-native-release-proof.json>
```

It requires a trusted host adapter and validates four real runtime scenarios,
the installed personas and schemas, host-level safety attestation, and
byte-identical fixture state. An unavailable adapter returns `not-run`. This is
an optional maintainer test and does not block a normal local installation. See
[`docs/testing/agent-native-review-smoke.md`](../testing/agent-native-review-smoke.md)
for the adapter and receipt contract.

## Local installation

The proof-receipt installation gate was removed after review because it created
a circular local workflow: the new runtime could not be installed until it had
already been exercised. Install the reviewed package directly:

```text
python install.py --force
python install.py --check
```

The force path still removes only the exact package-owned retired files listed
by the installer. It does not use globs to delete unknown skills, agents, or
references. Restart Codex after installation so the skill registry refreshes.
