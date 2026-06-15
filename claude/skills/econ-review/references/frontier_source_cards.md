<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources (skills/, .codex/agents/, references/) and run build_claude.py. -->

# Frontier source cards for econometrics-facing reviewers

These cards translate contemporary econometrics into review guardrails. They are not a runtime literature-review requirement. Reviewers should cite or invoke them only if the user asks for literature grounding; otherwise, use them silently as method awareness.

## Difference-in-differences and event studies

### Roth, Sant'Anna, Bilinski, and Poe (2023), "What's Trending in Difference-in-Differences?"

Use as the broad synthesis card. Audit implication: the reviewer should not treat canonical two-period DiD assumptions as automatically valid in staggered, heterogeneous, dynamic, or inference-sensitive settings. Require design class, treatment timing, comparison group, parallel-trends rationale, clustering/inference, and sensitivity/diagnostic evidence.

### Callaway and Sant'Anna (2021), "Difference-in-Differences with Multiple Time Periods"

Use for staggered-adoption group-time ATT discipline. Audit implication: require a clear target aggregation and support by group and time. If the paper reports an overall effect, reviewers should ask what group-time effects are being aggregated and with what weights.

### Sun and Abraham (2021), "Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects"

Use for TWFE event-study contamination risk. Audit implication: require omitted-period, event-time support, cohort support, and a clear statement of whether dynamic coefficients are interpretable under heterogeneous effects.

### Goodman-Bacon (2021), "Difference-in-Differences with Variation in Treatment Timing"

Use for TWFE decomposition awareness. Audit implication: require object-parity and treatment-timing diagnostics before treating TWFE as a clean average treatment effect in staggered-adoption settings.

## Inference and clustering

### Abadie, Athey, Imbens, and Wooldridge (2023), "When Should You Adjust Standard Errors for Clustering?"

Use for design/sampling logic of clustering. Audit implication: require reviewers to ask why clustering is needed, what uncertainty source is represented, whether clustering aligns with treatment assignment or sampling, and whether conventional clustered SEs over/understate uncertainty in the design.

### MacKinnon, Nielsen, and Webb (2023), "Cluster-Robust Inference: A Guide to Empirical Practice"

Use for cluster-robust practice. Audit implication: require cluster counts, cluster leverage/imbalance concerns, multiway/nested clustering, and small-cluster remedies such as wild cluster bootstrap or other design-consistent approaches when relevant.

## Instrumental variables

### Montiel Olea and Pflueger (2013), "A Robust Test for Weak Instruments"

Use for weak-instrument diagnostics under heteroskedastic/autocorrelated/clustered conditions. Audit implication: a conventional first-stage F is not enough when the variance structure differs from the textbook homoskedastic case.

### Lee, McCrary, Moreira, and Porter (2022), "Valid t-Ratio Inference for IV"

Use for single-IV weak-inference caution. Audit implication: when IV estimates carry the claim, reviewers should ask whether inference remains valid at the reported first-stage strength rather than relying mechanically on `F > 10`.

## Regression discontinuity

### Calonico, Cattaneo, and Titiunik (2014), "Robust Nonparametric Confidence Intervals for Regression-Discontinuity Designs"

Use for RD inference. Audit implication: require bandwidth, polynomial order, kernel, bias correction/robust inference convention, and sensitivity checks before promotion.

### Cattaneo, Idrobo, and Titiunik (2020/2024), "A Practical Introduction to Regression Discontinuity Designs"

Use for practical RD evidence surfaces. Audit implication: require running variable, cutoff, manipulation/density, covariate balance, bandwidth sensitivity, fuzzy first stage when relevant, and local-randomisation/discrete-score caveats when relevant.

## Synthetic control and panel counterfactuals

### Abadie (2021), "Using Synthetic Controls: Feasibility, Data Requirements, and Methodological Aspects"

Use for synthetic-control feasibility and diagnostics. Audit implication: require donor pool, pre-treatment fit, predictor balance, donor-weight concentration, placebo/permutation evidence, and sensitivity to donor-pool changes.

### Arkhangelsky, Athey, Hirshberg, Imbens, and Wager (2021), "Synthetic Difference-in-Differences"

Use for synthetic DiD and panel weighting. Audit implication: require clarity on unit/time weights, target parameter, pre-period fit, and whether uncertainty is treated as placebo/randomisation, asymptotic, bootstrap, or descriptive.

## Dynamics and local projections

### Jorda (2005), "Estimation and Inference of Impulse Responses by Local Projections"

Use for local-projection basics. Audit implication: require horizon definition, shock timing, lag controls, and horizon-specific samples.

### Plagborg-Moller and Wolf (2021), "Local Projections and VARs Estimate the Same Impulse Responses"

Use for LP/VAR interpretation. Audit implication: reviewers should not treat LP and VAR as necessarily different estimands; differences may arise from finite-sample dimension reduction, lag specification, or identification implementation.

### Montiel Olea and Plagborg-Moller (2021), "Local Projection Inference Is Simpler and More Robust Than You Think"

Use for LP inference. Audit implication: require inference convention by horizon, lag controls, persistence/long-horizon treatment, and pointwise versus simultaneous band clarity.

## Randomised experiments

### Athey and Imbens (2017), "The Econometrics of Randomized Experiments"

Use for design-based experiment review. Audit implication: require randomisation unit, assignment probabilities, stratification/blocking, cluster assignment, attrition, non-compliance, ITT/TOT distinction, interference risks, and design-consistent inference.

## ML-assisted causal estimation

### Chernozhukov et al. (2018), "Double/Debiased Machine Learning for Treatment and Structural Parameters"

Use for ML-assisted causal inference. Audit implication: require target low-dimensional parameter, nuisance models, orthogonal/debiased score, sample splitting/cross-fitting, leakage checks, and inference method.
