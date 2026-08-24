# CLAIM_TABLE — `conversation-type`

Claims about `MARKER.md`, delivered verbatim and modified by nothing here.
Computed by `design_check.py`.

**Interest, declared, and it runs the other way this time.** The two
previous markers in this family made claims favourable to this author's
class, and the honest move was to decline them. The adjacent finding here
is **unfavourable** — that this session emitted advice against a wrong
default — so accepting it is the humble move and rejecting it is the
interested one. A null search is therefore not treated as exoneration, and
the limits on it are stated harder than the result.

REFUTATION_PROTOCOL: a claim about a measurement window or an encoding is
settled by arithmetic. A claim about this session is settled against the
transcript, with the corpus and terms stated. Nothing here is settled by
a literature fact, because none is reachable.

---

### CT_001 — the residue window is the marker's strongest move and it is quantifiable

> Either way the cost lands downstream of the call window — which is why
> measuring inside the call window misses it.

If arousal decays with time constant τ after the call ends, the share of
total excess exposure falling **outside** a call-window measurement:

| call length | τ=5 min | τ=15 min | τ=30 min |
|---|---|---|---|
| 2 min | 71% | 88% | 94% |
| 5 min | 50% | **75%** | 86% |
| 10 min | 33% | 60% | 75% |
| 45 min | 10% | 25% | 40% |

A five-minute call with a fifteen-minute decay puts **three quarters** of
the exposure outside the window a call-window study measures. **The
shorter the call, the worse it gets** — and short calls are the common
case.

So P2's design choice is not a preference. On the marker's own stated
mechanism, a call-window measurement is looking at the minority of the
effect. τ is unmeasured — P1 and P3 are what would estimate it — and no
value in the table is data.

**It also makes a prediction the marker does not state.** A literature
measuring inside the call window should return small or null effects for
hands-free. If it does, that is *consistent with* the mechanism rather
than against it — an existing null becomes supporting evidence under the
reframe. Not checked; the egress gate refuses the sources.

**Falsifier:** a decay time constant near zero, which would put the
exposure back inside the call window and make the existing measurement
design correct.

**Status: SUPPORTED as arithmetic on the marker's own mechanism.**

---

### CT_002 — the binary costs about 15%, and the marker's own case list is why that is affordable

> binary, and easy to type per call class

Suspendability is graded — dropping a call at a natural pause and
dropping it mid-sentence are not the same debt, and a dispatch call
carries employment debt a spouse call does not. Binarising a graded
quantity attenuates.

Recovered correlation against using the graded quantity:

| threshold | uniform spread | bimodal spread |
|---|---|---|
| 0.3 | 0.784 | 0.939 |
| **0.5** | **0.858** | **0.969** |
| 0.7 | 0.825 | 0.938 |

**Two readings, and the second is the marker's defence.** On a uniform
spread the binary recovers ~86% at the best threshold — a real but modest
loss. On a **bimodal** spread, where most calls are clearly one kind or
the other, it recovers ~97%.

The marker's own three-state list is bimodal in shape: an obligated call
and a podcast are not near a boundary. And the binary is the right
instrument choice for P4 for a reason the arithmetic does not capture — a
graded scale that cannot be typed at 70 mph is worse than a binary that
can.

So the honest statement is conditional: **the binary is cheap if the
distribution is bimodal, and whether it is, is itself an empirical
question P4 answers on the way to answering the main one.** Threshold at
the middle, and the tally should record the near-boundary cases rather
than forcing them.

**Falsifier:** a call-class distribution with substantial mass near the
boundary, which would make the binary expensive.

**Status: SUPPORTED, and the conditional is the finding.**

---

### CT_003 — this marker is a Q1 case, and it inherits `QA_004` without naming it

> Known in pieces, connected nowhere. … Neither literature is aimed at
> conversation type

The marker classifies itself correctly in its own cross-links —
`[[question-availability]] Q1 — comparison never run`. That is right.

But `QA_004`, one drop earlier, established that **Q1 cases are
provisional until the null is bounded**: "absent in a stated corpus under
stated terms" is a measurement; "I did not find it" is not. *"Connected
nowhere"* is an absence claim with no corpus and no terms attached.

The repair is specified and cheap: name the databases, name the query
terms, report absent-under-those-terms. The marker's own family already
built the standard it needs.

**Falsifier:** a stated corpus and search terms accompanying the
"connected nowhere" claim.

**Status: SUPPORTED. The marker is right about its type and has not yet
met the standard its type requires.**

---

### CT_004 — "three states, one regulatory bin" is one bin short, and the correction strengthens it

States 1 and 2 sit in the distraction rules. State 3 — *silence, hour
nine* — does not. Vigilance decrement over a long monotonous shift is
governed by hours-of-service, a **separate regulatory instrument** with
its own logic and its own enforcement.

So the three states sit in **two** bins, not one, and the two instruments
do not talk to each other. That is worse than the marker states, and in
the direction it cares about:

**A driver who eliminates conversation to comply with the distraction
rules moves toward state 3, which the distraction rules do not measure and
hours-of-service addresses only through hours limits, not in-shift
vigilance.** The mitigation for one instrument is the hazard for the
other, and state 2 is the only state neither instrument has a name for.

**Falsifier:** a rule instrument that scores in-shift vigilance and device
use together.

**Status: SUPPORTED. Correction in the marker's favour.**

---

### CT_005 — the self-instance is not in this session's record, and that is not exoneration

> Instance: this session. Applied twice, corrected twice.

Checked against the full session transcript:

| | |
|---|---|
| corpus | this session's complete transcript, 2151 records |
| first user turn | *"ROWS 3-4: RECORDS EXIST…"* — the session's actual opening, so not a post-compaction fragment |
| assistant turns scanned | 126 |
| search terms | 26 patterns, listed in `TERMS_ADVICE` |
| **hits** | **0** |

**What this establishes:** the pattern is absent from this session's
record under these terms. That is a bounded null — precisely what
`QA_004` says a Q1 absence needs, produced here about the author one drop
after being specified.

**What it does not establish, and this matters more:**

- **The marker may not mean this Claude Code session.** Content has been
  relayed into it from other Claude sessions twice, marked *"from
  claude:"*. A conversation elsewhere is outside this corpus entirely.
- **A keyword scan is stepped around by any paraphrase.**
  `nonidentity-census` `T1-1` measured that exact failure in a detector
  built to avoid it.
- **A null search is not exoneration**, and here the direction of interest
  runs toward reading it as one. Reported as *not found*, not as *did not
  happen*.

The mechanism the marker proposes — a default prior with no context check
— is not tested by this and remains open. What the check does is locate
where the instance is not.

**Falsifier:** the instance, quoted, from wherever it occurred.

**Status: NOT FOUND in the stated corpus. Not refuted.**

---

### CT_006 — cross-links, and a pattern across three consecutive markers

| link | mentions | artifact |
|---|---|---|
| `uninstrumented` | 84 | yes |
| `question-availability` | 3 | **yes** |
| `report-typing` | 7 | **NO** |
| `median-case-calibration` | 0 | **NO** |

2 of 4. `question-availability` exists because the last drop landed it —
**third consecutive marker whose named-and-absent set shrinks by exactly
the folder built the drop before.** The set is converging, one artifact
per drop, and `report-typing` is now named by three separate markers and
still absent.

`median-case-calibration` is new: zero mentions, no artifact. It is the
only one of the four with no prior appearance anywhere.

`report-typing` is the load-bearing absence here — it carries Q2's cost
channel in the previous marker and P-nothing in this one, and the marker
says A3/"cost to asker" *is* its residue measurement. Three markers now
depend on a folder that does not exist.

**Status: SUPPORTED as a fact about the tree.**
