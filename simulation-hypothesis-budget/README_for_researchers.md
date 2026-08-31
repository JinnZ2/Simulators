# Simulation Hypothesis Budget — Research Toolkit

## What This Folder Is

This folder contains a **complete, runnable, self‑auditing argument** about the simulation hypothesis. It is not a simulation. It is a **budget** — a cost‑accounting of what the hypothesis would require.

You can run it on any machine with Python (including a phone). It will pass all its internal checks. It will also show you one claim that it **refuted** — because the audit system caught a mistake in its own argument.

## What This Folder Is Not

- Not a simulation
- Not a measurement of any real system
- Not a proof that we live (or do not live) in a simulation

It is a **test harness for a specific argument** — and it is designed to be extended, challenged, and improved by anyone who reads it.

## How to Run It

```bash
# Run the full audit
python3 budget.py --selftest

# Check the scaling classes
python3 scaling_classes.py --selftest

# Inspect the consequence frame
python3 consequence_frame.py --selftest

All output will be in plain text. No external libraries required.

The Most Important Claim to Read

SHB‑013 was a claim about what terms are needed before assigning a cost to simulation. It included a falsifier. The falsifier fired. The claim was refuted by the repository's own audit.

This is not a failure. It is the strongest evidence that the audit system works.

Read CLAIM_TABLE.md to see how the refutation was recorded (the claim's status was changed to REFUTED, not hidden or corrected).

Where to Start Exploring

If you are new to this material, start with these three gaps:

1. The lazy‑consistency cost — no one knows how to bound it. Can you?
2. Area‑law vs. volume‑law entanglement — what fraction of matter is in each state?
3. The SHB‑013 falsifier repair — the falsifier was too narrow. Can you write a better one?

See STUDY_PATHS.md for a full list of research projects, each scoped to a semester or a summer.

How to Contribute

1. Fork the repository
2. Pick a gap from STUDY_PATHS.md
3. Explore it, measure it, or write a new falsifier
4. Submit a pull request with your findings
5. Update the claim table — your new result becomes part of the argument

License

This folder is CC0 / public domain. Use it, break it, improve it, teach with it.

```
