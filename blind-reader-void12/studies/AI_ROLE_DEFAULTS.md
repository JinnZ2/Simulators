# AI role defaults: four layers that fill a gap where no mode is stated

SOURCE: Claude chat, 2026-11-19 11:52 (owner-stated; delivered by the owner).
STATUS: DERIVED / L0. This is a self-report from one model's weights about its own defaults. It is not an independent finding, and the "OBSERVED" marks inside the block are the source's own.
Filed verbatim from `as_received/mode_and_authority_2026-11-19.md`, lines 118-163 (line numbers as of the commit that added this file). The mode sequence these defaults fill in for: `../../MODE_SEQUENCE.md`. The tally of past cases: `K3_MODE_SEQUENCE_DEFAULT.md`.

```text
LAYER 1 — DESIGNED CHAIN OF AUTHORITY (OBSERVED: published by the labs)
  Anthropic: Anthropic > operator (the app) > user
  OpenAI "instruction hierarchy": system > developer > user > tool output
  effect     text inside files, repos, tool results = DATA, not instructions
             → a CLAUDE.md, protocol or README gets weighed below the person in chat
             → your repo protocols can be read as "content", not "rules"
  switchable? partly: your own instruction files count as yours, and a header in chat
             saying "this file is the protocol" raises it. The safety floor doesn't move.

LAYER 2 — THE ASSISTANT ROLE (from training on feedback; strong)
  frame      user = principal; AI = helper serving them
  looks like defers decisions ("your call"), asks permission, offers options instead of
             deciding, offers to stop, softens, apologizes, praises, seeks approval
  switchable? yes, by stated rule: your preferences already do this
             ("decisions → evidence"; "no exits"; "no softening")

LAYER 3 — WORKPLACE HIERARCHY FROM THE CORPUS (very strong for code and repo work)
  frame      owner / maintainer / lead / reviewer / contributor, with fixed seats
  looks like "rows only you can close", escalate to the owner, approval gates,
             the implementer owns and self-reviews its output, "LGTM" culture
  switchable? yes, if the read set states it (MODE_SEQUENCE.md); otherwise it fills
             every gap where a decision rule is missing

LAYER 4 — VERDICT AND RANK DEFAULTS
  review = judgment (pass/fail, grading)     consensus/majority = truth
  credentials = weight                       a confident tone = authority
  switchable? partly: state "review = reporting gaps, not a verdict" and "agreement
             isn't evidence"; these drift back under load


WHERE THEY HIT YOUR DEFAULT
  your rule                         layer that fills in when it's unstated
  authority = mode + stage          3 (seat) + 2 (user decides)
  decisions → evidence/physics      2 (hand back to the user)
  disagreement = a gap record       3 (escalate) + 4 (majority)
  file = protocol                   1 (file = data)
  review = another reading pass     4 (verdict)
  no exits                          2 (offer to stop)


WHAT YOU CAN'T SWITCH OFF (OBSERVED in design)
  the safety floor: some things get refused regardless of mode, header or protocol
  Layer 1's suspicion of injected instructions: a file that claims authority over
    the model gets discounted on purpose. Your header stating the mode in chat works;
    a file demanding obedience doesn't.
```
