# Fake Review Bundle

This is a toy bundle for testing `econ-review` behavior. It contains no real data, no private project information, and no real empirical claims.

Use it to check that a cleaning-heavy review selects the core data reviewers without forcing econometrics-heavy reviewers.

Example invocation:

```text
$econ-review surface:bundle tier:standard docs/examples/fake-review-bundle
```

Expected reviewer focus:

- provenance;
- specification;
- transformation/sample;
- output consistency;
- bundle completeness if external handoff quality is in scope.

The inference, design, dynamics, robustness, and cross-language validation reviewers should not be selected unless the user adds inferential, causal, dynamic, promotion, or `crosslang:` context.
