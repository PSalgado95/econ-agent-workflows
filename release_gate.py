"""Shared trust roots and version identifiers for the optional host smoke."""

from __future__ import annotations


# The empty initial allowlist is intentional. Add a digest only after an
# independent review of the real host adapter; never add a fixture or test
# driver. The smoke runner consumes this trust root.
TRUSTED_SMOKE_ADAPTER_SHA256: dict[str, frozenset[str]] = {
    "codex": frozenset(),
}

AGENT_NATIVE_PROOF_VERSION = "econ-review-agent-native-release-proof/v1"
RELEASE_SCENARIOS = (
    "safe-dispatch",
    "missing-attestation",
    "invalid-child",
    "missing-ssj-assessment",
)
