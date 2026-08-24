# AUDIT_NOTES — `conversation-type`

`MARKER.md` is delivered verbatim and heads this folder. Audit content is
here, in `CLAIM_TABLE.md`, and in `design_check.py`.

```
python3 design_check.py            # full report
python3 design_check.py --selftest # every falsifier as an assertion
```

Six claims `CT_001`–`CT_006`.

## Interest, declared, and it runs the other way this time

The two previous markers in this family made claims **favourable** to this
author's class, and the honest move was to decline them — an interested
party should not ratify a claim in its own favour.

The adjacent finding here is **unfavourable**: that this session emitted
advice against a wrong default, twice. So the directions invert.
**Accepting it is the humble move; rejecting it is the interested one.**

Which is why `CT_005` reports a null search as *not found* rather than as
*did not happen*, and states the limits harder than the result.

## What the arithmetic says

**`CT_001` — the residue window is the strongest thing in the marker, and
it is quantifiable without any driving data.** If arousal decays with time
constant τ after a call, the share of exposure falling outside a
call-window measurement:

| call length | τ=5 | τ=15 | τ=30 |
|---|---|---|---|
| 2 min | 71% | 88% | 94% |
| 5 min | 50% | **75%** | 86% |
| 45 min | 10% | 25% | 40% |

A five-minute call with a fifteen-minute decay puts **three quarters** of
the exposure outside the window, and **the shorter the call the worse it
gets** — short calls being the common case. P2's design choice is not a
preference; on the marker's own mechanism a call-window study is looking
at the minority of the effect.

It also makes a prediction the marker does not state: **a literature
measuring inside the call window should return small or null effects for
hands-free**, and finding that would be *consistent with* the mechanism
rather than against it. An existing null becomes supporting evidence under
the reframe. Not checked — the egress gate refuses the sources.

**`CT_002` — the binary costs about 15%, and the marker's own case list is
why that is affordable.** Suspendability is graded: a natural pause and a
mid-sentence drop are different debts, and a dispatch call carries
employment debt a spouse call does not. Binarising attenuates — to ~86% of
the graded signal on a uniform spread, ~97% on a bimodal one.

The marker's three-state list is bimodal in shape; an obligated call and a
podcast are not near a boundary. And the binary is right for P4 for a
reason the arithmetic misses: a graded scale that cannot be typed at 70
mph is worse than a binary that can.

So the statement is conditional and the conditional is the finding — **the
binary is cheap if the distribution is bimodal, and whether it is, is an
empirical question P4 answers on the way to the main one.** Threshold at
the middle; record the near-boundary cases rather than forcing them.

## Two corrections, both in the marker's favour

**`CT_004` — "three states, one regulatory bin" is one bin short.** States
1 and 2 are in the distraction rules; state 3 is not. Vigilance decrement
is governed by hours-of-service, a separate instrument with its own logic.

So there are **two** bins and they do not talk to each other, which is
worse than stated and in the direction the marker cares about: **a driver
who eliminates conversation to comply with the distraction rules moves
toward state 3**, which those rules do not measure and hours-of-service
addresses only through hours limits, not in-shift vigilance. The
mitigation for one instrument is the hazard for the other, and state 2 is
the state neither has a name for.

**`CT_003` — the marker is a Q1 case and inherits `QA_004` without naming
it.** It classifies itself correctly (`Q1 — comparison never run`). But
`QA_004`, one drop earlier, established that Q1 cases stay provisional
until the null is bounded: *"absent in a stated corpus under stated
terms"* is a measurement, *"I did not find it"* is not. *"Connected
nowhere"* is an absence claim with no corpus and no terms. The standard it
needs was built in its own family last drop.

## The self-instance

**`CT_005`.** Checked against the session transcript — 2151 records,
first user turn is the session's actual opening so this is not a
post-compaction fragment, 126 assistant turns, 26 search patterns,
**0 hits**.

That is a bounded null, and producing one about the author one drop after
specifying the standard is the point. But three things it does not
establish, and they matter more than the result:

- **The marker may not mean this Claude Code session.** Content has been
  relayed in from other Claude sessions twice, marked *"from claude:"*.
- **A keyword scan is stepped around by any paraphrase** —
  `nonidentity-census` `T1-1` measured that failure in a detector built to
  avoid it.
- **A null search is not exoneration**, and the interest here runs toward
  reading it as one.

The proposed mechanism — a default prior with no context check — is not
tested by this and stays open. The check locates where the instance is
not.

## Cross-links, and a pattern

2 of 4 artifacts present. `question-availability` exists because the last
drop landed it — **third consecutive marker whose named-and-absent set
shrinks by exactly the folder built the drop before.** The set converges
one artifact per drop.

`report-typing` is now named by three separate markers, carries Q2's cost
channel in one and A3's residue measurement in another, and does not
exist. It is the load-bearing absence in this family.
`median-case-calibration` is new: zero mentions anywhere.

## Where it sits

`uninstrumented/` is the parent — the marker's own framing is a quantity
the instrument cannot admit, and the instrument here is a rule written on
channel rather than on the variable. `question-availability/` supplies
`CT_003`'s standard. `sim-span/` is the closest methodological sibling:
both find that the measurement window, not the mechanism, is what decides
whether an effect is visible.

Every claim about arousal, vigilance and motor carrier rulemaking is
carried from the marker and unchecked — the egress gate refuses the
sources, `MS_004` status. **Nothing above rests on one**; the two
computations are arithmetic on the marker's own stated mechanism, and the
transcript check is on a local file.

CC0. Stdlib only. Parses under Python 3.9.
