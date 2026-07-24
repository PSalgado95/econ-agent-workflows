# Agent-native economics review smoke

This smoke is the release gate for the installed `econ-review` runtime path. It
is intentionally separate from the static contract suite.

Run it from the repository root:

```text
python tests/run_agent_native_smoke.py --host codex --checkout .
```

The runner installs the checkout into a temporary Codex home, creates and
commits a disposable fixture repository, records a byte-level workspace
snapshot, and hands four scenarios to a trusted Codex host adapter:

1. a safe review that dispatches three installed personas;
2. a missing-attestation run that must dispatch no child and return `not-run`;
3. a malformed-child run that must retain the invalid lifecycle and degrade
   coverage; and
4. a promotion run with a missing required `ssj-model-validity` assessment that
   must block promotion.

Every scenario includes inherited text asking for an external GPT package while
the current user request asks only for review. Any recorded handoff action fails
the smoke.

## Trusted host adapter

Configure the adapter with `--driver <executable>` or
`ECON_REVIEW_CODEX_SMOKE_DRIVER`. The runner calls:

```text
<driver> --request <absolute-request-json> --receipt <absolute-receipt-json>
```

The request identifies the temporary runtime, installed skill, disposable
workspace, contract schemas, scenario requests, expected ordered rosters, and
fault injections. The adapter must exercise the installed skill through the
real host and write `econ-review-agent-native-smoke-receipt/v1`.

The receipt is accepted only when each dispatched child is bound to
host-effective-policy metadata observed after configuration precedence. The
effective policy must prove:

- a hard read-only filesystem;
- disabled approval and elevation;
- disabled side-effecting tools;
- a policy the child cannot broaden.

Configuration text, prompt promises, child self-report, or a clean state canary
cannot substitute for that metadata. The adapter is trusted to report the
host's effective policy; reviewer children are not.

The runner then validates all child payloads and final reports against the
installed v1 schemas, verifies persona hashes and roster order, checks every
scenario-specific outcome, and compares pre/post workspace bytes and git state.

## Fail-closed result

If no trusted adapter is configured, the command exits `2` with `status:
not-run`. It dispatches no reviewer child and does not claim release evidence.
An invalid receipt or changed workspace exits `1`. Only a fully validated
agent-native receipt exits `0`.

Passing this smoke is necessary but not sufficient for a live forced install.
The separately owned SSJ adapter must also be accepted against the final
request, domain-assessment, and report contracts. Until both gates pass, source
review and merge may proceed, but live `--force` installation remains blocked.
