"""Shared trust roots and version identifiers for live-install evidence."""

from __future__ import annotations


# The empty initial allowlist is intentional. Add a digest only after an
# independent review of the real host adapter; never add a fixture or test
# driver. Both the smoke runner and installers consume this one trust root.
TRUSTED_SMOKE_ADAPTER_SHA256: dict[str, frozenset[str]] = {
    "codex": frozenset(),
}

RELEASE_GATE_VERSION = "econ-agent-workflows-release-gate/v1"
AGENT_NATIVE_PROOF_VERSION = "econ-review-agent-native-release-proof/v1"
SSJ_ACCEPTANCE_VERSION = "econ-ssj-adapter-acceptance/v1"
RELEASE_SCENARIOS = (
    "safe-dispatch",
    "missing-attestation",
    "invalid-child",
    "missing-ssj-assessment",
)
