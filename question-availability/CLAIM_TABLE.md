# CLAIM_TABLE — `question-availability`

Claims about `MARKER.md`, delivered verbatim and modified by nothing here.
Computed by `check_marker.py`.

REFUTATION_PROTOCOL: a claim about what is in this tree is settled by
reading the tree. A claim about a measurement's structure is settled by
constructing the states it has to encode. Nothing here is settled by
agreeing with the marker twice.

---

### QA_001 — the split is the contribution, and Q3's exclusion from it is what makes it a split

> "Knowledge decay" as a single container is wrong for Q1 and Q2. Nothing
> decayed in either. Q1 was never held; Q2 is actively held out. Only Q3
> is decay.

The move that earns this is that Q3 is **kept in and named as the
exception**. A three-way split where all three are the new thing is a
rename; one where the third is explicitly the old container is a
distinction, and it comes with a test — *was it ever held* — that
separates them without appeal to intent.

`question availability` is also the right container name for the reason
the marker gives: what is measured is entry, not loss. That is a different
quantity from anything in the `uninstrumented` register, which reads
instruments; this reads whether a measurement is attempted.

**Status: SUPPORTED. The honest positive.**

---

### QA_002 — the ordinal is off by three, for the second time

> status: candidate ninth exclusion mechanism for [[uninstrumented]]
> [[uninstrumented]] eight exclusion mechanisms; Q2 candidate

Counted in the tree:

| filed | |
|---|---|
| register `MECHANISMS` tuple | **8** |
| `category-weld/MECHANISM_09.md` | CATEGORY WELD |
| `generation-capacity/MECHANISM_10.md` | GENERATION CAPACITY REMOVED |
| `derivation-discarded/MECHANISM_11.md` | DERIVATION DISCARDED |
| **next unused ordinal** | **12** |

Nine, ten and eleven are taken. **Second instance of this exact slip** —
`nonidentity-census` T4 caught the same one and recorded *"the ordinal is
also taken: this would be a twelfth, not a ninth."*

Worth saying why it recurs rather than treating it as carelessness: the
**eight-item list is the register**, and it is the only place the count
appears as a list. Mechanisms nine through eleven live in sibling folders
as `MECHANISM_NN.md` and are invisible from the register's own file. Two
independent readers have now made the same subtraction. That is a property
of where the count is kept, and the repair is a count the register itself
publishes.

**Falsifier:** the next unused ordinal being 9. `--selftest` fails if it is.

**Status: SUPPORTED.**

---

### QA_003 — Q2 is not a candidate mechanism; it is one the register already recorded as missing

`UNI_012`, on the register's own literature note, found four mechanisms
named in prose and two of them not on the list. Of those two,
`undeclared frames` has a whole folder. **`affect routing` has neither** —
no entry, no mechanism.

Its shape there, and Q2's here:

| `UNI_012` | Q2 |
|---|---|
| *"a channel reclassified at intake, so the reading never reaches a guard at all"* | *"the label is applied prior to content, so the content never reaches evaluation"* |
| *"unfalsifiable from the speaker's side, because objecting to it reads as confirming it"* | *"Answering the label does not clear it; the pre-emptive denial imports the frame"* |

The same mechanism, stated twice, reached from two directions. Q2 is that
mechanism **arriving with a name**, and the name is better than
`affect routing`, which describes only one of its two cases.

**And the marker names UNI_012's own case without connecting it.** Q2's
second case — *"driver diagnostic question typed as complaint by reporter
position"* — is the case `UNI_012` was written from. Q2's **first** case,
*"why is this arrangement retained"* filed as conspiracy-adjacent, is from
a different field, which is exactly what `UNI_002`'s standing cross-field
check has been open for: a second entry under one mechanism from a
different field.

So the correct status line is not *candidate ninth*. It is: **the twelfth
ordinal, for a mechanism the register identified as missing three drops
ago, now arriving with its second case and its second field.**

**Falsifier:** `affect routing` appearing in the register's `MECHANISMS`
tuple, which would mean it was filed and Q2 is a duplicate of a filed
mechanism rather than of an unfiled one.

**Status: SUPPORTED.**

---

### QA_004 — A1 cannot answer the question the marker's own Open section poses

> A1 Q1: does a control condition exist in the world, and is there any
> published comparison. **Two booleans. Cheap.**

> Q1 has no negative evidence by construction. Need a criterion for
> distinguishing "not asked" from "asked and not found by me."

A1's second boolean is the outcome of a search. Three states have to be
encoded:

| state | A1 returns |
|---|---|
| comparison found | `(True, True)` |
| absent in a stated corpus under stated terms | `(True, False)` |
| not searched | `(True, False)` |

**The two that collide are exactly the two the Open section says must be
separated.** Three states into two values; the collision is arithmetic,
not a judgement.

The repair is the one this repo keeps arriving at — a third state — and
here it does specific work. *"Absent in a stated corpus under stated
terms"* is a measurement, because the null is bounded. *"I did not find
it"* is not one. *"Not searched"* is neither. Bounding the null is what
makes a Q1 case enterable at all, and it is the criterion the Open section
asks for.

Thirteenth instance of the absent-versus-known-negative repair in this
repo, and among the few where the missing state is the whole finding
rather than a reporting nicety.

**Falsifier:** an encoding of A1 in which the three states do not collide.
`--selftest` fails if the collision disappears.

**Status: SUPPORTED.**

---

### QA_005 — A4 is built and unrun, and needs a reference class the marker does not name

> A4 is the cheapest real measurement in the set and is **runnable now**.

The computation is built here — corrected share per year since correction,
plus a half-life that returns `None` for a curve that never crosses rather
than a large number, because never-crossing is the Q3 case and has to be
a distinct value.

**No citation counts are supplied.** The egress gate refuses the
databases, and inventing them would be worse than not running it.

The marker is right that a single ratio is not enough and asks for the
series *"by year since correction."* What it does not say is that **the
series is still uninterpretable alone.** Two constructed corrections with
the *same* corrected-share at year 10:

| | y1 | y5 | y10 | y20 | half-life |
|---|---|---|---|---|---|
| displaced | 0.10 | 0.30 | **0.45** | 0.80 | 11.4 y |
| stalled | 0.25 | 0.40 | **0.45** | 0.44 | **never** |

The trajectory separates them, so the marker's instinct holds. But whether
an observed curve counts as *"the corrected version did not displace it"*
needs a **reference class of corrections that did** — otherwise "slow" and
"stalled" are read off a prior. `criterion-symmetry`'s missing comparison
table, on a second substrate, and the same repair.

**Falsifier:** a displacement threshold derivable from one curve without a
comparison set.

**Status: SUPPORTED. The measurement is right and is one input short.**

---

### QA_006 — 0 of 4 measurements are runnable in this environment, and that is not the marker's fault

| | state |
|---|---|
| A1 | broken by the marker's own Open section (`QA_004`) |
| A2 | needs a venue-typed corpus; none in this tree |
| A3 | is `report-typing`'s residue measurement; that folder is not in this tree |
| A4 | built here; data refused by the egress gate |

**A4 genuinely is runnable** — by someone with a citation database.
`notes/study_watch.py` runs on a GitHub Actions runner that reaches
Crossref, OpenAlex and arXiv, which is why it exists. A4 is the second
item in this drop family the watcher was built for, after
`shape-spec-audit` `MS_004`.

A1 is the one that is broken rather than blocked, and it is the cheapest
to repair — one field.

**Status: SUPPORTED.**

---

### QA_007 — mention is not existence, and a sibling drop made the difference visible

| link | mentions | artifact |
|---|---|---|
| `uninstrumented` | 80 | yes |
| `criterion-symmetry` | 4 | **yes** |
| `report-typing` | 3 | **NO** |
| `rubric-backcasting` | 3 | **NO** |
| `merit-anchoring` | 3 | **NO** |

Artifacts present: **2 of 5**, up from 1 of 4 on the previous marker,
because the last drop landed `criterion-symmetry`. The named-and-absent
set converges as drops arrive, and the same three are still missing —
they are the comparison set both markers say the shape needs.

**The two columns disagree, and the disagreement is the finding.**
`report-typing` has three mentions and no artifact, and it acquired every
one of them the moment the *previous* marker listed it in its own
cross-links. A mention count — which is what the checker two drops ago
used — would now report it as resolving.

That is `UNI_010`'s self-reference shape reaching this audit **through a
sibling folder** rather than through its own output, so the `EXCLUDE`-list
repair does not catch it. The fix is a second column: ask whether the
artifact exists, not whether the token appears.

**Falsifier:** `report-typing` having an artifact, or having no mentions.
`--selftest` fails on either.

**Status: SUPPORTED as a claim, REFUTED on its stated instance
(2026-08-26).**

`report-typing` landed. The falsifier fired exactly as written, the
selftest went red, and the check was repointed rather than loosened:
the live instance is now `merit-anchoring`, 6 mentions and no
artifact, which acquired two of them from the arriving marker's own
cross-refs — the same route by which `report-typing` acquired its
three, one drop later.

So the *instance* expired and the *mechanism* did not. The arriving
folder re-instanced it at a finer grain in the same commit: its own
`RT_002` found `observer-exclusion` naming `report-typing` only in a
cross-link checker's target list, which is neither a citation nor an
absence but a third state — a folder asking whether the artifact
exists. Two columns were not enough; the prose/code split is the
third.

The count moved the way the paragraph above predicted and by more
than it predicted: artifacts present **3 of 5**, and the arriving
marker's cross-refs opened two further absences
(`median-case-calibration`, `sensing-spine`), so the named-and-absent
set grew in the commit that shrank it.
