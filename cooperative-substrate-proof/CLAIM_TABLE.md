# CLAIM_TABLE -- cooperative-substrate-proof

Ids are permanent and are never renumbered. `PRF_` is this folder's
prefix. These are claims about the BUILD -- what the code does, what it
refuses, and what was found by running it. They are not claims about
cooperation, competition, any published result, any organisation or any
person. The delivered order is `WORK_ORDER.md`, landed verbatim.

Status values: SUPPORTED / REFUTED / UNVERIFIED / CORRECTED.

---

## PRF_001 -- the named repository could not be created from here

**Status:** SUPPORTED.

The order says `repo: JinnZ2/cooperative-substrate-proof (create if
absent)`. Two attempts, both refused: `add_repo` returned *not found*,
and a create call returned *403 Resource not accessible by
integration*. GitHub access in this session is scoped to
`jinnz2/simulators` and `jinnz2/simulation`.

This is the `substrate-alternative/` `SA_018` precedent exactly, and the
same resolution is taken: the artifact lands as a self-contained folder
inside `Simulators`, carrying its own `LICENSE` and its own suite, and
importing nothing across its own boundary so it can be moved out whole.

**Falsifier:** an operator with repo-creation rights moves the folder to
its own repository; nothing in it has to change for that to work, which
is the property the no-cross-import rule buys.

---

## PRF_002 -- the coverage/values cut is structural, not promised

**Status:** SUPPORTED.

The framing says *coverage argument, not values argument* and *do not
strip the competition frame*. That is enforced in two places rather than
described:

1. `scope.py` has no return member meaning *the competitive frame is
   wrong* and none meaning some other frame is preferable. The three
   members are `WITHIN_COMPETITIVE_FRAME`, `OUTSIDE_FRAME_SCOPE` naming
   the condition that failed, and `UNDECLARED` naming the condition that
   was not coded. `OUTSIDE_FRAME_SCOPE` is a domain-of-validity
   statement: the frame does not cover this observation, which is not
   the observation being void.
2. `test_proof.py` walks the AST of every module for a declared ranking
   and values vocabulary and fails on a hit.

**Falsifier:** a module here returns a verdict ordering two frames, or
the scan stops firing on a plant.

---

## PRF_003 -- UNDECLARED outranks OUTSIDE_FRAME_SCOPE

**Status:** SUPPORTED.

C1-C4 are conjunctive (the order's word is *jointly*), so a failed
condition and an uncoded one both stop `WITHIN`. They are not the same
state and `code()` does not merge them: a coding with any condition
`None` returns `UNDECLARED` naming it, even when another condition is
already known to fail. Reading a silence as a failure would let an
uncoded corpus report that the competitive frame does not cover it,
which is a conclusion nobody measured.

This is the repo's absent-vs-known-negative repair on the field that
decides every part's scope line.

**Falsifier:** a coding with one `False` and one `None` returns
`OUTSIDE_FRAME_SCOPE`.

---

## PRF_004 -- the values scan fired on this folder's own code, and the repair was a better reading of the order

**Status:** CORRECTED.

P3's first corpus verdict was a majority rule over the pair readings,
and it carried a local variable named `best`. The AST values scan --
written to enforce `PRF_002` -- fired on it. The token is in the scan's
vocabulary because a ranking identifier is what a values argument gets
written with, and the scan was right: a corpus verdict taken as the
commonest pair reading is a vote among pairs.

The repair is `weakest_link`, and it is the order's own first sentence
for P3: *every link must transmit faithfully for information to reach a
model*. The corpus verdict is the weakest pair, not the commonest. A
majority rule would report `SHARED_TERMS` on a corpus holding one pair
that shares no terms at all.

So the scan changed a reading rather than a name. Recorded here rather
than silently fixed, because a guard that has only ever fired on a plant
is not known to fire on the thing it was written for.

**Falsifier:** the scan passes on a module that does carry a ranking
identifier.

---

## PRF_005 -- the token-rename null was a constant offset, and the cipher is the control

**Status:** CORRECTED.

P3's null was first built as a token rename: replace B's tokens with
fresh strings and re-measure the gain. That is not a null. Renaming
tokens to unseen strings destroys B's OWN compressibility, so
`C(rename(B))` is far larger than `C(B)`, the denominator moves, and the
control returns a near-constant offset -- measured at about `-0.025` for
every pair regardless of what the pair shared. `delta` was then
`gain + 0.025` and the ciphered fixture, which shares no terms with
anything by construction, read `SHARED_TERMS` at `delta 0.0553`.

A monoalphabetic substitution cipher is the control the measurement
needs: a fixed permutation of the alphabet leaves every repeat inside B
at the same length and the same distance, so `C(cipher(B))` is `C(B)` to
within a byte or two, while every substring B shared with A is gone.
Only the shared part moves.

Measured on the shipped fixtures after the repair: the shared-terms pair
drops `0.2350`, the ciphered control pair drops `-0.0052`. Separation of
about forty times the threshold, on the two sides of it.

**Falsifier:** a corpus where `C(cipher(B))` differs from `C(B)` by more
than a rounding, which would mean the permutation is doing something
other than relabelling.

---

## PRF_006 -- the ciphered fixture is the corpus's own null and it reads correctly

**Status:** SUPPORTED.

`fixtures/corpus/c_ciphered.txt` is `b_protocol.txt` put through the
module's own `encipher`. It is in the corpus deliberately: a
comprehension check whose corpus holds only agreeing documents cannot
show that it distinguishes anything.

The three pair readings: a-b `SHARED_TERMS` (gain 0.2507, delta 0.2350);
a-c `SHARED_FORM_ONLY` (gain 0.0174, delta -0.0052); b-c
`SHARED_FORM_ONLY` (gain 0.0205, delta -0.0066). The b-c pair is the
sharp one -- c IS b, letter for letter under a permutation, so every
structural property survives and every shared term is gone, and the
reading is exactly that: form yes, terms no.

Corpus verdict `SHARED_FORM_ONLY`, by `PRF_004`'s weakest-link rule.

**Falsifier:** the b-c pair reads `SHARED_TERMS`.

---

## PRF_007 -- `contest_limit` is the cut, and it was found by building the loop without it

**Status:** CORRECTED.

P4's first settler had `accepts` and `contests` and nothing else. With
every contest unbounded, the `corrective` chain -- one checking step
that objects, is answered, and moves on -- ran to the budget exactly as
the mutual-sabotage pair did, and both returned
`NO_ANSWER budget_exhausted`. The two outcomes the order asks to be
separated came back identical, which is the instrument reporting its own
absence of a distinction.

An unconditional `contests` edge is a mutual contest by another name.
The field added is `contest_limit`: an integer is a BOUNDED refusal (the
step objects a stated number of times and then takes what it is given),
absent or null is UNBOUNDED. It is DECLARED, never inferred -- nothing
reads the content of a step to decide whether its objection is the
correcting kind, because a word list doing that is the failure this
folder is about.

**Falsifier:** a chain whose only contest is bounded returns
`NO_ANSWER`.

---

## PRF_008 -- the turf-war chain has no answer for a structural reason, not for want of budget

**Status:** SUPPORTED.

`NO_ANSWER budget_exhausted` is a statement about the budget. The
shipped `turf_war` chain returns `NO_ANSWER` with reason `contest_loop`
and names both steps -- a cycle in the re-settle graph, where each
unbounded refusal's re-derivation triggers the other's. Detected on the
graph, so the verdict does not depend on how long the settler was
allowed to run.

`budget_exhausted` is kept as a backstop and labelled as what it is.
The order's sentence -- *not a worse answer, NO answer* -- is the
structural branch and not the backstop.

**Falsifier:** raising the budget multiplier changes the turf-war
verdict.

---

## PRF_009 -- P2's unverified share is a ceiling on verification, not a measurement of trust

**Status:** SUPPORTED.

A call site carries at least three clauses the caller cannot check: that
the callee returns what its name implies, in the shape the caller will
use, having left shared state as the caller left it. `LOCALLY_CHECKED`
is awarded in two narrow forms -- inside an `assert`, or an operand of a
comparison in a branch test -- and even then bounds ONE clause. A
checked return says nothing about what the callee did to shared state on
the way.

So `unverified_fraction` is an upper bound on how much of the call graph
could be locally verified, and the reported figure understates the
unverified surface rather than overstating it. On its own source: 100
call sites, 1 locally checked, `0.9900`. Below 1.0, so the metric is not
a constant; `None` on a file with no call sites, never `0.0`.

**Falsifier:** a file where the reported share exceeds the share a hand
count gives under the same two rules.

---

## PRF_010 -- the existence proof is the narrow checkable one

**Status:** SUPPORTED.

The order asks for *an existence proof checkable against itself*. The
claim made is the weak and checkable one: this output exists, producing
it required every contract in the two registers, the file analysed is
the file that produced the output, and its sha256 is printed beside the
reading. Scope stated in the module: this run, this machine, this
digest.

What is NOT claimed: that any of these layers is trustworthy, that code
in general depends on them in this proportion, or anything about a
system not analysed. The six layer contracts are listed with their
failure modes and each is marked uncheckable from inside the process --
that is the entry, not a gap in it.

**Falsifier:** the printed digest does not match the analysed file.

---

## PRF_011 -- P1's source rule is a refusal, and its limit is stated

**Status:** SUPPORTED.

`Requirement` raises `SourceMissing` at construction. The order is
unambiguous here (*Each entry needs a SOURCE*) and an
admitted-but-flagged entry is a record that can later be cited with the
flag dropped. `kind` is a closed five-member set and an entry outside it
raises rather than being filed under a nearest neighbour.

The limit is stated in the module rather than left to be discovered:
nothing checks whether the source SAYS what the entry says it says. That
is a reading, it is not performed here, and it is where P1 is weakest.
`absent_from_argument` is DECLARED per entry for the same reason.

**Falsifier:** a `Requirement` constructs with an empty source.

---

## PRF_012 -- the P1 pipeline is ABSENT and nothing stands in for it

**Status:** SUPPORTED.

The order names open-access methods sections as P1's pipeline. Egress
here is an allowlist and no publisher or preprint host answers, so no
methods section has been read. None is paraphrased from memory -- a
remembered methods section presented as a record is a fabricated source,
which is the one failure a folder about preconditions cannot commit.

`run_all.py` reports `P1*` as a separate ABSENT row rather than folding
it into P1's PASS, and the shipped record declares `CONSTRUCTED` in its
own provenance field. `unstated_fraction` on it is `0.8333`, which is a
property of a record written here and is not a measurement of any
published argument.

**Falsifier:** a methods-section host answers and the record is built
from one.

---

## PRF_013 -- an undeclared `t_visible` gives an undefined ratio, never a small one

**Status:** SUPPORTED.

`lag_ratio` returns `None` for an undeclared `t_visible`, for an absent
`t_scored`, and for a non-positive denominator, and `0.0` for a declared
immediate failure. The `0.0` and the `None`s are different statements
and the registered known-answer case pins them apart.

This is the whole of the antibiotic anchor. Scored per patient, per
course, the treatment read correct for fifty years -- not because the
resistance signal was measured and found absent, but because the
interval on which it becomes visible was not a variable anyone was
scored against. A ratio of zero would report the opposite: a failure
visible immediately.

All four verdicts occur on the shipped anchors (DECLARED_UNKNOWN 2,
NOT_EVALUABLE 1, TRACKED 1, UNDECLARED 1), so the classifier is neither
`CONSTANT_FIRES` nor `CONSTANT_SILENT`.

**Falsifier:** an undeclared `t_visible` returns a number.

---

## PRF_014 -- one operation is a COPY, and the drift cost is stated

**Status:** SUPPORTED.

The repo convention is import, never copy -- five stale copies of one
gate across three drops is what copying cost last time
(`measurement-fork` `MF_006`, `MF_011`). This folder imports nothing
across its own boundary, because `PRF_001` puts it here as a folder that
has to be able to leave whole.

The cost is one operation: `identifiers()` in `test_proof.py` is a copy
of `tools/authority_scan.py`'s AST walk. It is labelled a copy at its
definition. If the shared scanner gains a rule, this copy does not, and
nothing in the repo will say so -- which is exactly the `MF_019` shape,
accepted here with its reason rather than hidden.

**Falsifier:** the two implementations disagree on a file and nothing
reports it. That is the expected failure, not a surprise.

---

## PRF_015 -- two metrics carry known-answer cases

**Status:** SUPPORTED.

`p3_comprehension.gain_from_sizes` and `p5_lag.lag_ratio` are registered
in `tools/known_answer.py` and listed in `tests/test_known_answer_gate.py`'s
MANIFEST. Each case set carries more than one distinct expected value,
which is the registry's own rule against a case set that cannot detect a
constant metric. Both registrations sit inside `seed()`, so the
reachability check covers them.

The cases that matter are the absent ones: `gain_from_sizes` returns
`None` on an absent size and on a zero denominator, `0.0` when the
compressed sizes really are equal; `lag_ratio` the same shape one field
over. Reading either `None` as a zero is the failure the registry
exists to catch.

**Falsifier:** either metric drops out of `EXPECTED_METRICS` and the
completeness check stays COMPLETE.

---

## PRF_016 -- nothing here is a measurement of anything outside this folder

**Status:** UNVERIFIED, and it covers the folder.

Every record, chain, action, and document is CONSTRUCTED and says so.
No methods section was read, no corpus outside `fixtures/` was measured,
no model was run, and no published result, organisation or person is
named anywhere. The arithmetic is checkable by anyone with the clone;
the material it runs on was written here.

What the artifact establishes is that each part's check is runnable,
that its absent states are distinguishable from its measured ones, and
that its verdicts are reachable in more than one direction. Whether the
substrate argument holds of any real corpus, code base, chain of
reasoning, record or scoring regime is untouched in both directions.

**Falsifier:** any of the five parts is run on external material.
# CLAIM_TABLE — cooperative-substrate-proof

Ids are `CSF_`, permanent, never renumbered. Every number is printed by
`run_all.py` or `selftest.py` and pinned by `selftest.py`; the renders
are in `samples/`. Nothing here is a statement about any published
result, deployed model, trial or multi-agent run: the checks were built
to the dispatch and run on what this folder holds.

| id | claim | status | evidence | falsifier |
|---|---|---|---|---|
| CSF_001 | The dispatch's constraints hold, read from the files: every import is stdlib or this folder, every file parses under 3.9, every library module is under 300 lines and refuses `--selftest` with exit 2, no file names a network module, nothing imports across the folder boundary. | SUPPORTED | `selftest.py` folder section | a non-stdlib import, a 3.9 parse failure, a `--selftest` that exits 0 running nothing, a cross-folder import |
| CSF_002 | P3 measures cross-part vocabulary sharing and nothing else, because both arms are pseudo-word remaps of equal length and differ only in whether the map is shared. A shared-vocabulary corpus reads `CONVERGENT`; a corpus with no shared word type reads `INDISTINGUISHABLE_FROM_NULL` with the paired gap on zero. The first version compared the private arm to the raw corpus and read the disjoint corpus as `CONVERGENT`, since random letters compress less well than real words whatever the sharing; recorded in the module. | SUPPORTED | `selftest.py` P3 section: shared → CONVERGENT, disjoint → INDISTINGUISHABLE, `abs(gap/sd) < 3` | a corpus with no shared word type reading `CONVERGENT`, or a constructed shared-vocabulary corpus reading `INDISTINGUISHABLE` |
| CSF_003 | On this folder's own text the reading is `CONVERGENT` by a wide margin, and the number moves when this table is written, because the `--self` corpus includes the documents that quote it: the pinned sample was regenerated after `README.md` and this file landed, and anyone re-running reads them too. `UNI_010`'s loop, stated rather than closed. | SUPPORTED | `samples/run_all.sample.txt` P3 block; `selftest.py` "--self corpus -> CONVERGENT" | a `--self` run that is not `CONVERGENT`, or a render that does not print the part count beside the gap |
| CSF_004 | P3 establishes a necessary condition and not a sufficient one: compressibility is redundancy, a single sentence repeated across parts is maximally convergent, and the limit is printed on every render's last line rather than kept in a caveat. | SUPPORTED | the render's last line; the module docstring's WHAT THIS IS NOT | — (a stated limit; the check is that it is printed) |
| CSF_005 | P4's chain check separates a CORRECTION (contests an output AND produces a replacement WITH a reason; the chain terminates) from a CONTEST (contests, no replacement; the rejected output has no successor). Any contest returns `NO_ANSWER` with `final = None`; a replacement without a reason is a contest. The type has no quality axis, so "no answer, not a worse one" is what the type can express. | SUPPORTED | `selftest.py` P4 section | a chain carrying a contest with no replacement that returns a final output |
| CSF_006 | The turf war is exact: when sabotage is cheaper every agent sabotages, no goal advances, and completed is 0 at budget 50 and at budget 5000 alike; when it is not, all k complete at turn n. The goals are absolute, so sabotage never advances the saboteur and is chosen on cost alone, which is the dispatch's mechanism. This is a property of the construction; the dispatch's own turf-war case is carried and not read. | SUPPORTED | `render_turf()`; `selftest.py` "0 of 3", "3 of 3 at turn n", single agent completes | a cost row where sabotage is chosen and a goal completes |
| CSF_007 | P2 is an existence proof checkable against itself: on its own source it returns `SUBSTRATE_HOLDS` with every layer live, a second run reproduces the sha256 and every count, and the state is reachable in both directions — a planted non-IEEE `float_info` reads `VIOLATED`, one planted link in a three-link chain reads `NO_OUTPUT` where the faithful chain reads `OUTPUT 7`. | SUPPORTED | `selftest.py` P2 section | two runs on one source disagreeing on a count; a layer check that cannot return `VIOLATED` |
| CSF_008 | P2's contract count is a floor: `verified` is a syntactic proxy (`[CHOICE 8]`) that reads a try-wrapped call as verified while a try/except catches a raise and verifies nothing about a returned type. On its own source 10 of 95 call sites read verified and 85 are the unverified floor; the sum is asserted. | SUPPORTED | `p2.contracts()` on the three-call probe: total 3, verified 2, floor 1 | a proxy that reads the returned type at the call site |
| CSF_009 | Every P1 record carries a source that is checked by slicing: a record whose span does not slice out its own text is `UNSOURCED` and enters no count. On the CONSTRUCTED fixture 15 records are sourced across five classes, one is argued (`cores`), fourteen are not, ratio 14.0; `PRIOR_RESULT` is a visible zero. The pattern set is lexical both ways: recall is a floor and precision is a reading. | SUPPORTED | `selftest.py` P1 section; planted false span → `UNSOURCED` | a record with a false span that is counted; a fixture sentence in the pattern vocabulary not extracted |
| CSF_010 | The P1 pipeline (open-access methods sections) is a paste path here and not a fetch: no publisher host is reachable and none is transcribed from memory, so nothing in P1 is a statement about any published result. | UNVERIFIED | the fixture's first line; no network import in P1, asserted | a real methods section pasted in and the records hand-read |
| CSF_011 | P5 has three states, never two: `UNDECLARED` is an absent quantity (no `t_visible`, or a zero `t_scored`), not a small ratio, and never reads `TRACKED`. The dispatch's medicine sentences as numbers land at 1304.5 and 40.6 (`DECLARED_UNKNOWN`), the same-window action at 0.2 (`TRACKED`), the boundary at exactly 10.0. The gate declares and blocks nothing. | SUPPORTED | `selftest.py` P5 section | an action with no `t_visible` reading `TRACKED` or `DECLARED_UNKNOWN` |
| CSF_012 | C1-C4 are coded three-valued and `UNCODED` is not `ABSENT`: an uncoded case lands `UNDETERMINED`, never `OUT_OF_SCOPE`, and `ABSENT` beats `UNCODED`. C1 is the one condition with an instrument here (P5's clocks, `[CHOICE 1]`); C2-C4 are hand codes, and no study corpus is coded in this folder. | SUPPORTED | `selftest.py` scope section; P5 anchors code C1 `PRESENT PRESENT ABSENT UNCODED` | an uncoded case landing `OUT_OF_SCOPE`; a coded study corpus this folder does not hold |
| CSF_013 | The named repository could not be created from this session (`403 Resource not accessible by integration`, the `SA_018` outcome), so the artifact lands as a self-contained folder importing across no boundary, promotable as delivered. | SUPPORTED | the refusal recorded in `run_all.py`'s declaration; `CSF_001`'s no-cross-import check | the repository existing with this content while the folder imports from `../` |
| CSF_014 | UNVERIFIED: the framing claim's quantity — the cooperative substrate the competitive frame REQUIRES — is a coverage share, and no part measures a share. P2, P3, P4 establish necessary conditions (a faithful substrate, shared terms, an uncontested chain) on the system that ran them, which is an in-class self-report; P1 and P5 establish nothing beyond constructed inputs. The coverage argument is stated and its coverage number is not measured here. | UNVERIFIED | every render's declaration line | an instrument for the share, or a second party running the checks on a system they did not build |
| CSF_015 | The P3 self-read loop is measured, not only named: the part count and gap on the `--self` render are printed beside each other, the corpus grows by the documents that quote the result, and the pinned sample is the post-documents run. | SUPPORTED | `samples/run_all.sample.txt` | a `--self` render that omits the part count |
| CSF_016 | This is the third build of the subject in this repository (`../cooperative-substrate/` holds v1 and v2), rebuilt to a new dispatch without importing or reading the earlier modules while building. P5's three states came out the same shape as v2's — one builder converging with itself (`TP_003`), not two confirmations — and P3, P4 and P2 are different instruments from their v1 counterparts (compressibility vs cosine; chain check plus exact turf war vs random walk; live layer checks). | SUPPORTED | README "Relation" section; no import of `cooperative-substrate` anywhere, asserted by `CSF_001` | an import from the sibling, or a byte-identical module across the two folders |
