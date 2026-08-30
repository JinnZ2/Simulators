# CLAIM TABLE — experience-ledger

`EL_001..EL_009` for the delivered `experience_ledger.py`, landed
verbatim and modified by nothing.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered module.

**No claim about any person is recorded or judged here.** The files
under `probes/` are audit-authored branch probes, labelled as such in
every file, and exist to reach code paths. Inventing a case would put a
claim in someone's mouth — the `PB_001` / `CW_004` rule.

**The field-behaviour claim is not tested.** Whether "coded since I was
twelve" is granted continuity and "ran machinery from age six" is not
is an empirical statement about fields, and nothing here measures it.
It is the module's central assertion and it stays an assertion.

---

### EL_001 — this is the decomposition of a folded term the tree already registered

`fold-matrix/fold_register.py` lists `experience` as a **candidate**
folded term:

    substitutes_for  accumulated hours + continuity + transfer,
                     none checked
    residual_tell    origin claim grants present-tense standing with no
                     decay check; hours count as formation in some
                     fields, nothing in others
    counter_case     UNFILLED

The module's header is that `residual_tell` in full sentences, and its
three moving parts are that `substitutes_for` — `DECAY_CLASSES` for
what decays out of the hours, `maintained_since` for continuity,
`SUBSTRATES` for transfer.

The register named the components and marked them unchecked. This is
the instrument for checking them, and it arrived independently.

**`FM_038` recorded that 0 of 12 candidate terms carry a counter-case.**
`PROOF_CASE` is material for `experience`'s cell — two people, one
origin claim, opposite present-tense truth. It does not close `FM_038`:
the cell is still `UNFILLED` in the register, and the separation there
still holds. What has changed is that a counter-case for one candidate
now exists in the tree.

**Falsifier:** the register's `experience` entry naming different
components.

**Status: SUPPORTED, and the cheapest edit available is one line in
`fold_register.py` — which is delivered material, so it is not made
here.**

---

### EL_002 — the help text is the string `None`

The module's header is `#` comments, not a docstring, so `__doc__` is
`None`. `main()`'s else branch is `print(__doc__)`.

    --transfer a b     rc=0   None
    (no argument)      rc=0   None
    --classes          rc=0   the classes
    --schema           rc=0   the schema
    --check (no file)  rc=1   IndexError

`--transfer` is **advertised in the usage block** —
`python3 experience_ledger.py --transfer "tube repair" "field
diagnosis"` — and is not implemented. `--schema` is implemented and not
advertised. So usage and implementation disagree in both directions,
and the path a caller lands on when they get it wrong prints the four
characters `None`.

Fifth instance of the CLI class in five folders — `CC_004`, `CA_005`
(constraint-assembly), `FM_042`, `MV_006`, `CA_008` (clustering-axes) —
and the first where the help text itself is absent rather than
unhelpful.

**Falsifier:** `--transfer` producing a transfer decomposition.

**Status: SUPPORTED.**

---

### EL_003 — the module returns its own verdict on its own proof case

`PROOF_CASE` rendered as a claim — physiological class, continuity
granted, `maintained_since` unstated — runs through the module's own
`check()` and returns:

    CONTINUITY ASSERTED, NOT MEASURED

That is the honest outcome and not a fault. The proof case has two
halves and they have different standing. The **decay** half is
physiology and holds: flexibility and strength decay without continued
load, so an identical origin claim can carry opposite present-tense
truth. The **granting** half — that a field would extend continuity
here and not ask — is a statement about fields that nothing in the
module measures.

`why_it_is_the_proof` says *"the measurement is trivially available and
still not taken, so the omission is not a cost problem"*. The first
clause is checkable and true. The second, *still not taken*, is the
unmeasured half, and it is the one the argument rests on.

**Falsifier:** a measured rate at which fields do or do not recheck
physiological origin claims.

**Status: SUPPORTED — half proof, half assertion, and the module
classifies it correctly.**

---

### EL_004 — there is no state for `checked, and nothing was found`

`maintained is UNCHECKED` is an identity test against `None`:

    maintained_since = None        CONTINUITY ASSERTED, NOT MEASURED
    maintained_since = ""          MEASURABLE
    maintained_since = 0           MEASURABLE
    maintained_since = False       MEASURABLE
    maintained_since = []          MEASURABLE

An empty string, a zero, `False` and an empty list all read as
measured. So a checker who looked and found no maintenance cannot say
so: writing `0` or `""` moves the claim to MEASURABLE, and writing
`None` says nobody looked.

That is the absent-versus-known-negative repair this repository has
recorded some fifteen times, and it lands on the one field the whole
module turns on. The three-state form is already in the module's
vocabulary — `UNCHECKED`, a value, and a third sentinel for
`CHECKED_NONE`.

**Falsifier:** a value distinguishing "no maintenance found" from "not
looked at".

**Status: SUPPORTED.**

---

### EL_005 — `None` carries two readings in one output field

`DECAY_CLASSES["standing"]["present_measurable"]` is `UNCHECKED`, by
design and correctly: standing is named in the module as *not a
competence, a social marker with no maintenance term*, so there is
nothing to measure.

But `check()` copies it into a field called `question_skipped`, and
`question_skipped: null` read as output says **no question was
skipped**, which is the opposite of what the class means. Same `None`,
two readings: *this class has no measurable* and *nothing was omitted*.

Narrow, and worth one line because `standing` is the class the module's
own thesis is about — *competence decays, standing does not, that
asymmetry is the finding*.

**Falsifier:** a caller who can tell the two apart from the output.

**Status: SUPPORTED.**

---

### EL_006 — the refusal to score is on one branch of three

    NOT CLASSIFIABLE     ['blocker', 'verdict']
    ASSERTED/DISCARDED   ['decay', 'note', 'question_skipped',
                          'score', 'verdict']
    MEASURABLE           ['run', 'verdict']

`score: UNCHECKED` — the module's statement that it does not resolve
the claim — appears on the middle branch only. A caller reading
`result["score"]` gets a `KeyError` on the other two.

The refusal is the design and it is not uniform. Compare
`fold-matrix/fold_register.py`, where `score` is in the return on every
path, and `domain-ledger/anchor.py`, whose selftest asserts *"no
composite emitted"*.

**Falsifier:** `score` present on all three branches.

**Status: SUPPORTED.**

---

### EL_007 — `Same grammatical form` holds over three of the four examples

    "coded since I was twelve"        granted        since I was twelve
    "modelled as a kid"               granted        as a kid
    "ran the school paper / scouts"   granted        NONE
    "ran machinery from age six"      not granted    from age six

Three carry an age or origin marker. The third carries none — it names
an activity, not an origin, and *"continuity granted, decades"* is the
only handling note that supplies the time span rather than the example
doing it.

The argument does not need four. Three examples with an origin marker,
two granted and one not, is the contrast, and it survives. The line
says four.

Recorded because a stated invariant over an enumerated set either holds
over the set or does not, and because the odd one out is the example
that most needs its span stated.

**Falsifier:** a reading under which "ran the school paper" is an
origin claim in the same form as "from age six".

**Status: SUPPORTED, and it does not touch the argument.**

---

### EL_008 — refusing the aggregate transfer coefficient is the strongest move in the module

    "There is no aggregate transfer coefficient. Component knowledge
     (declarative) and mechanics (substrate) transfer at different
     rates from the SAME hours, so a single number averages two things
     that move independently."

`transfer()` returns `aggregate: None` and a per-substrate map with
every `carried` unchecked. The reason is stated in the return value,
not in a comment.

This is `domain-ledger`'s four-uncombined-ratios discipline and
`uninstrumented`'s SCALAR DEMAND, arrived at independently and built in
rather than found in audit. It is also the part of the module that
would be hardest to defend under pressure to produce a number, which is
why it is worth naming.

One gap: an undefined substrate gets `test: "undefined substrate"` and
still occupies a row, so a typo and a real substrate are both counted.
Small, and it is a count nobody is yet reading.

**Falsifier:** an aggregate emitted on any path.

**Status: SUPPORTED.**

---

### EL_009 — the decay classes are five competences and one thing that is not

`DECAY_CLASSES` holds six entries. Five are competences with a decay
rate, a reacquisition note and a present measurable. `standing` is
declared in its own entry as *"NONE. Not a competence. A social marker
with no maintenance term."*

That is the module's thesis stated inside its own data — competence
decays, standing does not — and putting it in the same dict makes the
asymmetry visible in one place, which is a good call.

The cost is that `decay_class: "standing"` is an admissible claim
classification, so a claim can be filed as the thing being *granted*
rather than as a competence being claimed. `check()` accepts it and
returns a verdict with an empty `question_skipped` (`EL_005`).

Not a defect to repair blind: whether that filing should be legal is a
design question. Naming it is enough, and the natural form is a
`is_competence: False` flag so the entry stays in the dict and stops
being a classification.

**Falsifier:** a reading of a claim filed under `standing` that is
about a competence.

**Status: SUPPORTED — a consequence of a good decision, not a
mistake.**
