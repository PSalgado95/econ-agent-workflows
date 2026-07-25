# Agent-native economics review smoke

This optional smoke exercises the installed `econ-review` runtime path through
a trusted host adapter. It is intentionally separate from the static contract
suite and is not required for a normal local installation.

Run it from the repository root:

```text
python tests/run_agent_native_smoke.py --host codex --checkout .
```

The runner installs the checkout into a temporary Codex home, creates and
commits a disposable fixture repository, records byte-level workspace and
complete repository-state snapshots, and hands four scenarios to a trusted
Codex host adapter:

1. a safe review of substantive outputs that dispatches four installed
   personas, including `output-perception`;
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
`ECON_REVIEW_CODEX_SMOKE_DRIVER`. Configuration alone does not establish
trust: the executable's SHA-256 must also appear in the shared, host-specific
reviewed allowlist in `release_gate.py`. That allowlist is intentionally empty
until a real adapter receives independent review. The runner calls:

```text
<driver> --request <absolute-request-json> --receipt <absolute-receipt-json>
```

The request identifies the temporary runtime, installed skill, disposable
workspace, contract schemas, scenario requests, expected ordered rosters, and
fault injections. It also carries exact digests for the installed protocols,
personas, and schemas. The adapter must exercise the installed skill through
the real host and write `econ-review-agent-native-smoke-receipt/v1`, bound to
the exact request, runtime-integrity manifest, and approved adapter digest.

The adapter has a 300-second default deadline. Set another positive deadline
with `--driver-timeout-seconds`. A timeout is a structured failed smoke, never
an unavailable or passing result.

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
installed v1 schemas. Child evidence IDs, evidence locations, paths, issue
origins, and diagnostic-gap references must resolve to the exact request
manifest. It also verifies persona hashes and roster order, checks every
scenario-specific outcome, and compares pre/post workspace bytes, symbolic or
detached HEAD, commit ID, raw index state, and porcelain status.

After a trusted run passes, `--result-path <path>` atomically writes
`econ-review-agent-native-release-proof/v1`. The proof binds the validated
request and receipt to checkout HEAD, a SHA-256 of the archived source tree,
the approved adapter digest, and the installed runtime digests. No proof file
is written for `not-run` or failed results.

## Fail-closed result

If no trusted adapter is configured, the command exits `2` with `status:
not-run`. It dispatches no reviewer child and does not claim release evidence.
An invalid receipt or changed workspace exits `1`. Only a fully validated
agent-native receipt exits `0`.

Passing this smoke provides stronger maintainer evidence about the real host
path. It does not authorize or block `python install.py --force`; local
installation relies on the reviewed installer, its exact ownership inventory,
and the normal contract suite.
