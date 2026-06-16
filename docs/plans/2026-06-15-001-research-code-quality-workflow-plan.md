# Integrate Research-Code Quality into Econ Agent Workflows

- **Date:** 2026-06-15
- **Type:** workflow-skill design / implementation plan
- **Status:** implemented 2026-06-15
- **Owner:** Pedro

## 1. Summary

Implement a minimal research-code-quality layer across the economics workflow. `econ-plan` should classify research code and model-computation work correctly, `econ-work` should enforce a cheap first-pass code-quality floor when it writes research code, and `econ-review` should add one targeted reviewer lens when code is part of the review surface. Pure software remains routed to Compound Engineering, framework-specific model-computation guidance stays deferred, and external coding-guide materials remain evidence rather than committed repo content.

## 2. Problem Frame

The current skills are strong for empirical planning, execution, and review, but the taxonomy is still too empirical-rerun-shaped for research code whose main object is a model solver, simulation, calibration routine, numerical method, or reusable research tool. At the same time, adding generic software standards would push the skills outside their economics role and risk producing style-heavy reviews rather than research-useful feedback.

The GPT Pro response recommends a smaller integration: add a shared research-code-quality standard, add one review lens, add a general research-computing category, and calibrate expectations by the role code plays in the research workflow. This plan turns that recommendation into repo-local implementation steps.

## 3. Requirements

- **R1. Keep the change additive and reversible.** Prefer one shared reference, one reviewer lens, and narrow skill edits over a broad rewrite of the empirical workflow.
- **R2. Treat research code as economics workflow only when code correctness affects a research object.** Pure app, API, UI, infrastructure, general tooling, refactor, or debugging work remains a route-away case for Compound Engineering.
- **R3. Add a general research-computing lane.** Model solving, simulation, numerical methods, calibration routines, estimation machinery, and reusable economics research tooling need a home without making the core taxonomy framework-specific.
- **R4. Calibrate code expectations by code role.** Exploratory code, analysis pipelines, collaborator-facing code, replication-facing code, and library/tool code should not all get the same test/documentation burden.
- **R5. Make code-quality review research-facing.** The new reviewer should catch code structure that blocks reading, checking, rerunning, or safely modifying research work. It should suppress style nits and avoid duplicating substantive empirical reviewers.
- **R6. Keep performance guidance gated.** Performance advice should appear only when scale, profiling, runtime, memory, or model-computation bottlenecks make it relevant.
- **R7. Do not vendor Matt's coding-guide materials.** Distill the relevant principles into this package's own standards. Public attribution to Matthew Rognlie's materials is fine in an appropriate acknowledgements or influences section, but operational skill rules should stand on their own.
- **R8. Keep Codex source authoritative.** Edit the repo's Codex sources only in this plan; do not hand-edit generated Claude files or redesign Claude build tooling in this round.

## 4. Scope Boundaries

### In Scope

- Add a shared research-code-quality reference at `references/research-code-quality.md`.
- Add one Codex reviewer agent at `.codex/agents/econ-code-quality-reviewer.toml`.
- Update `econ-plan`, `econ-work`, and `econ-review` source skill text and their relevant references.
- Update `references/reviewer-protocol.md` so the new reviewer has a clear contract and JSON taxonomy support.
- Update `install.py` so Codex installation copies all root shared references, not only the reviewer protocol.
- Update `README.md` only where needed to keep install and review-panel descriptions accurate.

### Deferred to Follow-Up Work

- Framework-specific model-computation skill, reviewer, and reference guidance.
- Dedicated performance reviewer.
- Generated Claude package refresh and any Claude build-script policy changes.
- Any durable `econ-compound` learning note about this design.

### Out of Scope

- Committing external coding-guide or fast-code materials.
- Threading personal/source-specific attribution through operational reviewer prompts, issue taxonomy, or execution rules.
- Changing Compound Engineering workflows.
- Adding Python/R/Stata/Julia language preferences.
- Making cross-language validation default-on.
- Rewriting the empirical reviewer system from scratch.

## 5. Key Technical Decisions

### Decision 1: Shared Reference, Not New Top-Level Skill

Add `references/research-code-quality.md` as a sibling of `references/reviewer-protocol.md`. Code quality is a standard used by planning, work, and review; it is not a separate user workflow like `econ-plan` or `econ-review`.

### Decision 2: One New Reviewer Lens

Add `code-quality-auditor` with custom agent name `econ_code_quality_reviewer`. The lens should be selected when code, notebooks, scripts, diffs, computational routines, helper functions, tests, or code-generated outputs are part of the review surface. It should not run for pure note-only or output-only reviews where code is not in scope.

### Decision 3: `model_computation` Plus `code_role`

Add `task_family: model_computation` for model solvers, simulations, numerical methods, calibration, estimation machinery, and research tooling. Add `code_role` to calibrate the maturity expected of the code:

- `none`
- `exploratory`
- `analysis-pipeline`
- `shared-collaborator`
- `replication-facing`
- `library-tool`

Do not add a new `domain_mode` now. Keep `domain_mode: hybrid` for economics research-computing work where implementation integrity and research-object integrity both matter.

### Decision 4: `software-handoff` Becomes an Exit Marker

Revise `software-handoff` language so it no longer says direct invocations should always continue to an `econ-plan` execution artifact. For pure software work, the skill should identify the route-away and point to the current software workflow rather than pretending `econ-work` is the right executor.

### Decision 5: Cheap Always-On Code Floor

Whenever `econ-work` writes or changes research code, require the cheap floor from the first pass: descriptive names, visible entrypoints, named parameters/constants, no stale debug/test fragments in production functions, clear separation between analytical logic and formatting, and assertions for object-defining facts.

### Decision 6: Tests and Performance Scale with Code Role

Inline assertions are enough for local invariants. Named tests become expected for reusable helpers, replication-facing code, library/tool code, or bugs that should not recur. Performance advice is off by default unless the task is explicitly performance-sensitive or bottleneck evidence exists.

### Decision 7: Attribution Belongs in Reader-Facing Context

It is appropriate to acknowledge Matthew Rognlie's coding and fast-code materials in the README or in a short attribution note in the shared reference. Do not make those names part of the skill's operational logic. Reviewer prompts, issue origins, execution checklists, and routing rules should say the research-code-quality standard directly, without requiring the agent or reader to know the external source.

## 6. Implementation Units

### U1. Add Shared Research-Code-Quality Standard

**Files**

- `references/research-code-quality.md`

**Plan**

Write a concise shared standard covering:

- the purpose of research-code quality in economics workflows;
- the `code_role` ladder;
- the cheap always-on first-pass floor;
- assertion and test expectations;
- data and sample-transformation transparency;
- notebook-to-script boundaries;
- `model_computation` checks;
- gated performance guidance;
- explicit guardrails against style nits, over-refactoring, hidden transformations, language preferences, premature framework-specific design, and pure-software capture.

**Test Scenarios**

- A reader can tell when the standard applies to empirical scripts, model-computation code, notebooks, and pure software.
- The standard does not name external coding-guide material as committed authority or include large quoted/vendor content.
- Any public attribution, if added, is isolated to a short acknowledgements or influences note rather than repeated through operational rules.
- The standard does not include framework-specific categories, reviewer roles, or rules.
- The standard does not prefer a programming language.

### U2. Update Planning Taxonomy and Plan Template

**Files**

- `skills/econ-plan/SKILL.md`
- `skills/econ-plan/references/plan_template.md`

**Plan**

Extend classification rules so `econ-plan` captures:

- `task_family: model_computation`;
- `code_role`;
- research-computing work under `domain_mode: hybrid`;
- pure-software work under `domain_mode: software-handoff` as a route-away;
- expected execution route: `structure-only`, `full empirical rerun`, or `full computational run`;
- a research-code-quality contract block when code is in scope.

Revise stale language that currently says direct invocations should never stop at `software-handoff`.

**Test Scenarios**

- A data-cleaning plan can still classify as `task_family: data_construction` without forced model-computation fields beyond `code_role` when relevant.
- A model solver or simulation task classifies as `task_family: model_computation` and receives computational verification expectations.
- A pure API/UI/infrastructure request is marked as `software-handoff` and routed away instead of becoming an econ execution plan.
- `SKILL.md` and `plan_template.md` list the same `task_family` and `code_role` values.

### U3. Update Work-Time Execution Rules

**Files**

- `skills/econ-work/SKILL.md`
- `skills/econ-work/references/execution_reference.md`

**Plan**

Add work-time rules for research code:

- state `code_role` in the execution outline or closeout when code is in scope;
- add `full computational run` beside `structure-only` and `full empirical rerun`;
- require object-defining assertions;
- move reusable checks into named tests when the code role warrants it;
- delete scratch debug prints, temporary plots, commented-out test fragments, and stale exploratory code from production paths;
- keep notebooks from being the only durable record when code will be reused, reviewed, or promoted;
- use model-computation checks such as dimensions, convergence, residuals, mass conservation, market clearing, deterministic simulation checks, or small-grid benchmarks.

**Test Scenarios**

- A simple note-only task can remain `structure-only` without forced code-quality overhead.
- A script edit that changes sample construction requires assertions for keys, merge cardinality, row counts, denominators, or support as relevant.
- A model-computation task can close as `full computational run` without mislabeling the work as an empirical rerun.
- The closeout template names code-quality checks without turning every task into a full software test-suite requirement.

### U4. Add Code-Quality Review Lens

**Files**

- `.codex/agents/econ-code-quality-reviewer.toml`
- `references/reviewer-protocol.md`
- `skills/econ-review/SKILL.md`
- `skills/econ-review/references/review_reference.md`

**Plan**

Add a read-only reviewer lens with:

- role alias `code-quality-auditor`;
- custom agent name `econ_code_quality_reviewer`;
- `issue_origin: code-quality`;
- a protocol section defining what the lens owns and what it must leave to provenance, transformation/sample, specification, inference, robustness, reproducibility, software-equivalence, cross-language validation, hybrid-implementation, and bundle review;
- parent selection rules for code-bearing review surfaces;
- evidence-manifest fields for code paths, entrypoints, tests/asserts, computational checks, notebooks, and performance scope;
- prompt payload language so the parent passes the relevant excerpt of `references/research-code-quality.md` or the distilled contract.

**Test Scenarios**

- A code-bearing diff selects `code-quality-auditor` in addition to the relevant empirical reviewers.
- A pure note review does not select `code-quality-auditor` only because there is prose interpretation.
- A cross-language validation audit still uses the existing cross-language and software-equivalence roles; code-quality only comments on inspectability, tests, hidden debug code, or hard-to-rerun comparison scripts.
- The new TOML follows the same shape and read-only policy as existing reviewer agents.
- `issue_origin: code-quality` is accepted wherever issue origins are enumerated.

### U5. Update Installation and Public Docs

**Files**

- `install.py`
- `README.md`

**Plan**

Change Codex installation from copying one named shared protocol file to copying all root `references/*.md` files into the installed shared-reference directory. Update user-facing wording so the repo describes shared references rather than only a single protocol file.

Keep README edits restrained. It should explain that code-quality review applies when code is part of the review surface, not introduce a long internal taxonomy.

**Test Scenarios**

- A temp Codex install contains both `reviewer-protocol.md` and `research-code-quality.md`.
- `install.py --force` still refuses unsafe replacement outside the target Codex home.
- README install instructions no longer tell users to copy only `reviewer-protocol.md`.
- README does not claim the generated Claude package has been refreshed by this plan.

### U6. Final Consistency and Validation Pass

**Files**

- All changed files from U1-U5.

**Plan**

Run consistency checks across skill text, reviewer taxonomy, installer behavior, and stale wording. Do not stage or commit until the diff is reviewed.

**Test Scenarios**

- No generated Claude files are modified.
- No `build_claude.py` or `install_claude.py` edits appear in the diff.
- The new `code-quality` origin appears in the shared protocol and review reference.
- The new role appears in the reviewer role matrix and custom-agent mapping.
- The `task_family` and `code_role` enums match between plan skill and template.
- `software-handoff` is no longer described as something that must still become an econ execution plan.

## 7. Validation Checklist

No persistent test files are planned in this change. The repo currently validates these workflow skills through script checks, TOML parsing, install smoke tests, and targeted text searches. If implementation uncovers an existing repo-local fixture convention, use it; otherwise keep validation command-based.

Run after implementation:

```powershell
git diff --check
python -m py_compile install.py
```

Validate reviewer TOML shape:

```powershell
@'
from pathlib import Path
import tomllib

for p in sorted(Path(".codex/agents").glob("econ-*-reviewer.toml")):
    data = tomllib.loads(p.read_text())
    for key in ["name", "description", "model_reasoning_effort", "sandbox_mode", "developer_instructions"]:
        assert key in data, f"{p}: missing {key}"
    assert data["sandbox_mode"] == "read-only", f"{p}: reviewer must be read-only"
print("TOML reviewer agents OK")
'@ | python -
```

Validate Codex install copies shared references:

```powershell
$tmp = Join-Path $env:TEMP ("econ-agent-workflows-install-" + [guid]::NewGuid())
python install.py --codex-home $tmp --force
Get-ChildItem (Join-Path $tmp "references\econ-agent-workflows") -Filter *.md | Select-Object -ExpandProperty Name | Sort-Object
Test-Path (Join-Path $tmp "references\econ-agent-workflows\reviewer-protocol.md")
Test-Path (Join-Path $tmp "references\econ-agent-workflows\research-code-quality.md")
```

Validate reviewer-protocol consistency:

```powershell
@'
from pathlib import Path

protocol = Path("references/reviewer-protocol.md").read_text()
review_ref = Path("skills/econ-review/references/review_reference.md").read_text()

required = {
    "provenance", "specification", "transformation-and-sample",
    "estimation-practice", "inference", "output-consistency",
    "claim-discipline", "output-perception", "code-quality",
    "design", "dynamics", "robustness", "software-equivalence",
    "cross-language-validation", "reproducibility",
    "hybrid-implementation", "bundle"
}

for origin in required:
    assert origin in protocol, f"protocol missing {origin}"
    assert origin in review_ref, f"review_reference missing {origin}"

allowed_line = next(line for line in protocol.splitlines() if line.startswith("- `issue_origin`:"))
for origin in required:
    assert f"`{origin}`" in allowed_line, f"allowed values missing {origin}"

assert "`code-quality-auditor`" in protocol
assert "`code-quality-auditor`" in review_ref
assert "econ_code_quality_reviewer" in review_ref
print("Reviewer protocol enum consistency OK")
'@ | python -
```

Validate skill frontmatter:

```powershell
@'
from pathlib import Path

for p in sorted(Path("skills").glob("*/SKILL.md")) + sorted(Path("skills/auxiliary").glob("*/SKILL.md")):
    text = p.read_text()
    assert text.startswith("---\n"), f"{p}: missing opening frontmatter"
    end = text.find("\n---", 4)
    assert end != -1, f"{p}: missing closing frontmatter"
    front = text[4:end]
    assert "name:" in front, f"{p}: missing name"
    assert "description:" in front, f"{p}: missing description"
print("Skill frontmatter shape OK")
'@ | python -
```

Targeted searches:

```powershell
rg -n "never stop at `software-handoff`|never stop at software-handoff" skills README.md references
rg -n "reviewer-protocol.md.*only|shared protocol$" README.md install.py skills references
rg -n "code-quality|code_quality|code-quality-auditor|econ_code_quality_reviewer" references skills .codex/agents README.md
rg -n "code_role|model_computation|full computational run" skills references README.md
rg -n "performance-auditor|econ_performance_reviewer" skills references .codex/agents README.md
```

Expected result: the first, second, and performance-reviewer searches should be empty or contain only intentional deferred-scope wording. The code-quality, code-role, model-computation, and full-computational-run searches should show the intended new references.

## 8. Implementation Order

1. Add `references/research-code-quality.md`.
2. Update `econ-plan` and `plan_template.md` so the taxonomy has a place to reference the new standard.
3. Update `econ-work` and `execution_reference.md` so execution behavior matches the new taxonomy.
4. Add the new reviewer TOML and update `econ-review`, `review_reference.md`, and `reviewer-protocol.md`.
5. Update `install.py` and README shared-reference wording.
6. Run validation.
7. Review the diff manually for scope creep, especially generated Claude files, build scripts, external guide material, source-specific attribution inside operational rules, framework-specific model-computation text, and performance-reviewer drift.

## 9. Risks and Guardrails

- **Risk: style-nit reviews.** Guardrail: code-quality findings must name a readability, rerun, modification, or research-trust consequence.
- **Risk: over-refactoring empirical code.** Guardrail: prefer the smallest change that makes the research object easier to read, test, rerun, or review.
- **Risk: abstractions hide sample rules.** Guardrail: for data and construction code, hidden filters, merges, denominators, weights, and sample restrictions are code-quality defects.
- **Risk: pure software leaks into econ skills.** Guardrail: keep `software-handoff` as an exit marker.
- **Risk: performance advice becomes default.** Guardrail: require performance-sensitive scope or bottleneck evidence.
- **Risk: Claude package parity silently drifts.** Guardrail: do not hand-edit generated Claude files in this plan; track Claude refresh as a separate source-sync task after Codex-source changes are accepted.

## 10. Handoff

This plan is ready for `ce-work` or ordinary implementation. The executor should keep the diff focused on the files named above, validate before committing, and report any needed Claude-package follow-up separately instead of expanding this change midstream.
