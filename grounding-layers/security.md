# Security & Safeguards

This file defines the threat model for the grounding stack and the mechanisms we use to prevent gaming, bias injection, or adversarial misuse.

## Threat Model

We assume an adversary may:
- Submit crafted claims designed to pass all tests while violating the substrate.
- Inject biases into the claim to skew the `cultural_lens`.
- Overfit the test suite by tailoring claims to the exact test patterns.
- Spoof the observer state (e.g., declaring "well‑rested" when not).
- Exploit the temporal layer by sending signals at odd sampling rates to cause aliasing.
- Use the `field_compass` to find the path of least friction and use it to spread misinformation.

## Mitigation Principles

1. **Claim Provenance** – Every claim must be tagged with a source identifier and a timestamp. Claims without provenance are rejected.
2. **Randomness Seeding** – All stochastic processes (e.g., noise in Lε) must use a fixed seed per session, to make results reproducible. The seed is derived from the claim hash + a secret salt.
3. **Test Isolation** – Each test run is in a fresh environment; no state leaks between claims.
4. **Rate Limiting** – To prevent brute‑force gaming, the system limits claim submissions per source per time window.
5. **Bias Injection Detection** – The `cultural_lens` is run twice: once on the claim alone, once on the claim with a "neutral" tag. A large discrepancy flags potential bias injection.
6. **Hard‑Stop Checks** – If a claim violates L0 or L1 at any point, it is immediately rejected without further processing (no second chance).
7. **Audit Trail** – Every claim, intermediate result, and final verdict is logged to an immutable ledger (hash‑chain) for external verification.

## Implementation

The safeguards are implemented in `safeguards.py` and are automatically invoked by `run_grounding_pipeline.py` and `playground.py`.

## Future Extensions

- Integration with external provenance systems (e.g., W3C PROV).
- Cryptographically signed claims to prevent tampering.
- Manual review queue for claims flagged by the safeguards.
