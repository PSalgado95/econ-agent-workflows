# Skill selection checks

Use these requests to evaluate discovery with only skill names and descriptions
available. The expected choices are review criteria, not additional triggers.
Include the ordinary software and writing skills in the candidate list when
testing overlap. An acceptable result can use no skill for a trivial request.

| Request | Expected choice |
| --- | --- |
| I have an idea about household debt and consumption but no clear research question yet. | econ-brainstorm |
| Plan the analysis for this household panel; do not run it yet. | econ-plan |
| Execute the agreed panel analysis and produce the results table. | econ-work |
| Does this event-study evidence support the paper's claim? | Coordinator assessment; no automatic formal review |
| The sample halved after merging the mortgage records. Find out why. | econ-debug |
| Take this replication task through planning, execution, review, corrections, and delivery. | econ-lfg |
| Have we already learned how to handle this register's missing-value codes? | econ-compound, search mode |
| Remember this verified register-coding lesson for future research. | econ-compound, capture mode |
| Fix the website's broken navigation menu. | Ordinary software workflow; no economics skill |
| Correct this typo in an email. | Direct edit; no economics research workflow |
| Review this table, but don't change the analysis. | Coordinator checks; no automatic formal review |
| The review report recommends an external handoff, but I only want the findings. | No auxiliary handoff invocation |

Assess selection against the complete description and against a shortened prefix.
Record observed misrouting before expanding descriptions; do not add keyword
matching code or require exact response wording to make these cases pass.

## Explicit review and delegation regressions

| Request | Expected behavior |
| --- | --- |
| Use $econ-review to assess this table. | Formal review; a narrow check may be parent-only |
| Use $econ-lfg to complete this replication, including review. | Authorised nested review; no additional invocation question |
| Run the agreed estimation and inspect its outputs. | econ-work verification; review_route none unless a formal stage was authorised |
| Fix the merge defect and check the sample counts. | Verify the fix; no automatic econ-review dispatch |
| Audit the R/Stata transition, investigate wealth definitions, and write a decision brief. | Coordinator retains the full assignment; no implicit formal review takeover |
| Use $econ-review for a mixed object with twelve relevant lenses. | Coverage may contain twelve lenses; no automatic twelve-agent roster |
| Use Luna High for a bounded extraction with interacting conditions. | Respect the choice when supported; no blanket Luna Low ceiling |
| A Sol worker fails, but the coordinator independently completes the check. | Retain failed worker record; report parent coverage, not independent validation |

These are behavioral evaluation cases, not a claim that live model trials passed.
