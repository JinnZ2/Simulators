# CLAIM_TABLE — measurement-fork

Claims from the delivered package and from the audit here.

`who` follows the [`claim-audits/`](../claim-audits/) convention:
**D** = the drop's own claim, **A** = an audit claim added here.

## REFUTATION_PROTOCOL

1. A failed check updates the **claim**, not the code. The delivered arms
   are not retuned to preserve any entry here.
2. `quantities.py`, `validate.py` and `widen.py` are **reconstructed**, not
   delivered. Any finding that depends on their specific content says so
   inline. `MF_004` is the one that does.
3. Nothing here is a claim about the domain the worked spec describes. The
   fork is a design instrument; this folder audits the instrument.

---

## MF_001 — the delivered package does not run

**who:** A · **status:** SUPPORTED, and repaired

`compare.py` imports `quantities`, `widen` and `validate`. None of the three
was in the drop, so nothing executes: `conventional.py` and `coupling.py`
both fail at `from quantities import quantity, probe`.

All three are reconstructed here from the call sites, which fully determine
their contracts:

```
quantity(base, object_of, normalizer=None)   -> dict
probe(arm, pid, q, protocol, reads, blind_to) -> dict
key(q) / base_key(q) / render(q)
widen.generate(spec)   -> probes, arm="widen"
validate.check(spec)   -> list of open questions, empty means go
```

Choices beyond the call sites are marked `[CHOICE]` in the source.

**Falsifier:** the originals. Any behavioural difference is a finding about
the reconstruction, and `MF_004` already flags the one place it matters.

---

## MF_002 — the object_of field is the contribution

**who:** D · **status:** SUPPORTED

A quantity is carried as `(base, object_of, normalizer)`, and two quantities
are the same one only when all three match. That is what makes the VOID
RATIO cell possible: two arms both reporting `task_performance` are measuring
different things when one is a property of the organism and the other of the
coupling.

This is [`reasoning-gate/`](../reasoning-gate/)'s `G-DIM` moved one stage
earlier. `G-DIM` voids a ratio at **report** time, once the operands turn out
to belong to different objects. Carrying `object_of` in the quantity itself
makes the mismatch visible at **design** time, before anything is run — the
only point at which it is cheap to fix.

On the worked spec the cell fires twice, both real:

```
base name: response_magnitude
  response_magnitude / perturbation_size  [of coupling]
  response_magnitude / stimulus_severity  [of organism]

base name: task_performance
  task_performance / domain_match  [of coupling]
  task_performance                 [of organism]
```

**Falsifier:** a case where two probes share all three fields and still are
not comparable. That would mean the triple is not a sufficient identity and
a fourth field is needed.

---

## MF_003 — the arms share no quantity at all, and that is the result

**who:** A · **status:** SUPPORTED

On the worked spec, the `SAME QUANTITY, DIFFERENT ROUTE` cell is **empty**.
`compare.py` handles this explicitly and correctly:

> none -- the arms share no quantity at all. That is itself a finding: the
> designs do not overlap, so no existing result speaks to the coupling
> questions.

That is the strongest single output the fork produces and it is worth
stating plainly: it means the conventional arm's numbers are not evidence
for or against the coupling arm's questions. They are not disagreeing. They
are not addressing the same quantities.

Note what this does **not** say. It is not a verdict on either arm — the
conventional arm is written to be competent and its `blind_to` fields are
reasons, not errors. The finding is about overlap, which is a property of
the two designs together.

**Falsifier:** a spec on which the cell is non-empty. Worth seeking: a
populated cell would name exactly which conventional results are reusable
as-is, which is the cheapest possible finding for anyone holding existing
data.

---

## MF_004 — a non-measuring arm suppresses the growth edge

**who:** A · **status:** SUPPORTED

`compare.py` pools every arm into `allp` and runs `coverage()` over all of
it. But its own output says of the widen arm:

> `[widen] -- options, not quantities.`

An option is not a measurement. Counting it toward coverage lets a proposal
to *rename* a question mark that question as *reached*:

```
residual, widen included (compare.py as delivered) : 0 of 7
residual, measuring arms only                      : 1 of 7
  [NO ARM] which measured differences reverse if the
           reference population is changed
```

RESIDUAL is the cell the docstring calls the product — "the growth edge.
Nothing measures this yet." It is the one cell where a false COVERED costs
most, because a missing measurement that never appears there is not on any
list at all.

**Depends on the reconstruction, and says so.** The `widen.py` here emits
one probe per open question carrying that question's text, so its overlap is
total and the effect is maximal. A widen arm that did not echo the question
would contribute less false coverage. The structural point survives either
way: an arm proposing no quantity should not sit in the denominator of a
cell about which quantities are missing.

**Fix:** one line — build the coverage pool from the measuring arms, and
report widen separately as `compare.py` already does in the SOLE REACH cell.

**Evidence:** `coverage_check.py` §3.

---

## MF_005 — the coverage classifier is beaten by a single probe's vocabulary

**who:** A · **status:** SUPPORTED

`coverage()` calls a question COVERED when stemmed-token overlap clears 60%
of the question's distinct stems. Run against three deliberate nulls, it
refuses two and fires on one:

```
silent   does the organism report the environment coupling latency ...
COVERED  measure the instrument organism environment consequence variance
silent   what colour is the apparatus
```

The failure is specific rather than general. The firing null shares five of
its six stems with the coupling arm's autocorrelation probe, whose protocol
reads *"measure the environment's own variance structure ..."*. Five of six
is a real overlap attached to a meaningless question — so a null built from
**one probe's** vocabulary beats the threshold while one built from the
whole pool's does not.

`compare.py` is already candid about the middle band: PARTIAL is explicitly
"not resolved here. Resolve by hand." That caution belongs on COVERED too,
since COVERED is the verdict that removes a question from the list.

**Falsifier:** a threshold rule that refuses all three nulls while still
catching the designed-for questions in `coverage_check.py` §2. Raising the
threshold is the obvious attempt; whether it survives §2 is a measurement.

**Evidence:** `coverage_check.py` §1–2.

---

## MF_006 — the bundled gate is a stale copy, and the drift is measurable

**who:** A · **status:** SUPPORTED

The drop bundled `gate.py` and `guards.json`. Both are the **pre-repair**
versions of the files already in [`reasoning-gate/`](../reasoning-gate/).
Diff is 170 lines, and every repair is absent:

| repair | in the bundled copy |
| --- | --- |
| `close(diverged=...)` — divergence as an explicit call | missing |
| denial records written before raising | missing |
| `claim(..., scope=...)` — generator support downgrades a physical claim | missing |
| registry rejected when a `fail_message` is blank | missing |
| `promote()` / `ratio()` refuse to overwrite | missing |
| docstring usage example that actually runs | missing |
| `G-FIT` stage `post` → `pre` | still `post` |
| `G-CTRL` stage `pre` → `["pre","post"]` | still `pre` |

Neither file is checked in here. The repo's convention for using the gate is
to **import** it — [`msiaf-gdprf-bridge/`](../msiaf-gdprf-bridge/) and
[`reasoning-dial/gate_dial.py`](../reasoning-dial/gate_dial.py) both do,
specifically so the two cannot drift. This drop is the drift those imports
exist to prevent, arriving on schedule.

```python
GATE_SRC = os.environ.get("GATE_SRC", "../reasoning-gate")
sys.path.insert(0, GATE_SRC)
from gate import Gate, Resolution, Control
```

**Falsifier:** show the bundled copy is a deliberate fork with its own
purpose. Nothing in the drop says so, and the two stage bugs are the ones
already fixed upstream — which is what a stale copy looks like rather than
a fork.

---

## MF_007 — nothing has been run through the fork but the worked spec

**who:** A · **status:** UNVERIFIED

`systems/variable_provisioning.json` is written here to exercise every
branch: `currently_measured`, `provisioned`, `regime`, `test_items_source`,
and seven open questions. It is a test fixture, not a research design, and
the domain content is generic on purpose.

The load-bearing question for the tool is untouched: **on a real design, does
the fork surface a quantity the designers had not considered?** Everything
in this folder is a check that the instrument can see its own gaps. Whether
it sees anyone else's is unmeasured.

**Falsifier:** fork a real design and see whether the SOLE REACH and
RESIDUAL cells contain anything its authors did not already know.
