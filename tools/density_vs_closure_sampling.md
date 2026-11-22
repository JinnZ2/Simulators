# Density vs closure sampling: explore where the corpus is thin and the budgets still close

CC0. A reusable method, not a description of any person, body or field.

Status: PROPOSED. Method doc only. No code ships with this note; the
instrument is a separate order for the Simulators repository.

Index line: two readings per branch, CLOSURE (physics) and CROWDING
(corpus density), kept apart; explore thin branches that still close.

Tags: OBSERVED = stated in a source or seen in a run; DERIVED = follows
from what is stated here; PROPOSED = untested. [co-authored] = stated in
the work order of 2026-11-22 (Kavik + Claude), carried as stated.
[stated] = the owner said it directly; standing definitions, not findings.

## 0. Source and what is taken from it

Artiles et al., "The Alien Space of Science", arXiv:2603.01092 (v3,
2026-10-21). Cited, not copied. Statements about Artiles et al. come
from chat Claude's fetch of the arXiv abstract page (arXiv:2603.01092v3)
on 2026-11-22, relayed by the owner. Abstract only; the PDF was not read
by any party to this file. Atom extraction method, coherence-model
training, rater counts and stated limitations: NOT RECORDED. The four
welds are chat Claude's audit of the abstract (DERIVED).

[co-authored] Their move: score COHERENCE and AVAILABILITY separately,
then sample combinations that hold together but that no existing author
community is positioned to reach.

    their axis      their instrument              this note's axis   this note's instrument
    coherence       a model learned from past     CLOSURE            L0 budgets re-close on RETURN
                    papers (resemblance)                             (physics, not resemblance)
    availability    distance in the author        CROWDING           how dense the corpus default
                    network                                          is at the branch, with its basis

[DERIVED] The swap on the first row is the point. A learned coherence
model reads "looks like work that was accepted before". A budget reads
"mass in equals mass out". The first can only rate what resembles its
training set; the second has no training set.

## 1. Atoms are mechanisms, not topic labels

[co-authored] A branch is built from atoms. An atom is a mechanism that
carries across fields, never a field name or a topic.

    atom                 what it does (field-free)
    bottleneck           one narrow section sets the rate of the whole path
    buffer               a store that decouples inflow timing from outflow timing
    feedback loop        output returns as input; sign decides damp or amplify
    phase change         a state variable crosses a line and the rules change
    conservation leak    a budgeted quantity leaves by a path nobody is counting
    coupling             a change in one store forces a change in another
    threshold            no response below a level, response above it

[PROPOSED] Admission test for a new atom: it must be statable with no
field noun in the sentence, and it must be found in at least two fields
that do not share an instrument. A topic label ("hydrology",
"transformers") fails the first half by construction.

No coined terms. Where no English term fits a mechanism, the record
carries the literal string `term slot: void` and a one-line description
of the flow. A void slot is data; it is not filled with the nearest word.

## 2. Two readings, kept apart

[co-authored] Every branch gets two readings. They are never summed,
averaged, multiplied or folded into one number. A branch record with a
single combined score is malformed.

    CLOSURE    does the branch re-close the L0 budgets on RETURN
               (mass, energy, C, N, water)?

               pass                  every live budget closes inside its
                                     declared tolerance
               misclosure(value)     a budget does not close; the value
                                     and its unit are kept, per budget
               not checkable         no budget can be evaluated here
                                     (no conserved quantity is modelled,
                                     or RETURN was not run)

    CROWDING   how dense is the corpus default at this branch?

               dense | thin | absent | NOT RECORDED
               cut: see section 7 edge 3

               + crowding_basis: who ran the probe (Kavik / model /
                 both), which model, and how (search terms and corpus,
                 field experience, model recall with no search, ...)

[DERIVED] Three places a silence could pass as a value, each closed:

    not checkable   is not pass.     A branch nobody could test did not close.
    NOT RECORDED    is not absent.   Nobody looked is not "looked, found nothing".
    absent          needs a corpus.  "absent" with no stated corpus and
                                     terms is NOT RECORDED.

RETURN and anchor are used as in the anchor / branch / return loop of
`forest-model-ledger/CLAUDE.md` (METHOD BRIEF) in the Simulators
repository: a branch leaves an anchor state, and nothing counts as
explored until it is run back and diffed against that anchor. The L0
gate is the one in `relational-playground/` there: each budget LIVE or
VOID with a reason.

## 3. Selection rule

[co-authored] Flow of branches through the two gates:

    all branches from one anchor
            |
            v
      CLOSURE gate ---- misclosure(value) --> ledger, value kept, not explored further
            |      ---- not checkable -----> ledger, held; needs a budget before it can move
            | pass
            v
      CROWDING read
            |-- thin / absent ---> EXPLORE FIRST
            |-- dense -----------> ledger as REFERENCE, not deleted
            |-- NOT RECORDED ----> ledger; assess crowding before it is queued

[DERIVED] Order matters: CLOSURE first. A thin branch that leaks mass is
thin for a reason. The dense branches stay because they are the
reference the thin ones are diffed against; deleting them removes the
denominator.

[PROPOSED] This rule states an order of exploration only. It says
nothing about which branch is correct, and a dense branch that closes is
not demoted by it.

## 4. Holdout test (spec only, not run)

[co-authored]

    1. pick a cutoff date
    2. freeze every input dated before it (anchors, atoms, corpus view)
    3. run the explorer on the frozen inputs
    4. compare its branches against findings published after the cutoff
    5. record, per run:

         hits          explored branch matches a post-cutoff finding
         misses        post-cutoff finding the explorer did not reach
         false leads   explored branch (passed CLOSURE, thin) with no
                       post-cutoff counterpart
         denominator   total branches explored, and total post-cutoff
                       findings examined. REQUIRED. A hit count with no
                       denominator is not a result.

[DERIVED] A false lead is not a refuted branch. Inside the holdout
window it cannot be told apart from a branch nobody has reached yet
(section 6, weld 3). Record it under that name and leave it open.

## 5. Record fields, per branch

[co-authored]

    field            content
    anchor_id        the anchor this branch leaves from
    atoms[]          mechanisms from section 1; `term slot: void` allowed
    change           ONE change from the anchor. Two changes = two branches
    closure          pass | misclosure(value, per budget) | not checkable
    crowding         dense | thin | absent | NOT RECORDED
    crowding_basis   who (Kavik / model / both) and how. MANDATORY
    holdout_status   hit | miss | false lead | not run
    tag              OBSERVED | DERIVED | PROPOSED
    volume           volume = weight of evidence behind the tag: thin /
                     moderate / solid. [stated] by owner as a standing
                     tag; null until assessed.
    observer slots   null (reserved; nothing is written here by this method)

A record with `crowding` set and `crowding_basis` empty does not load.
`closure` and `crowding` are separate fields with separate vocabularies;
no field holds a function of both.

## 6. Welds to state

[co-authored] From chat Claude's audit of the arXiv abstract (DERIVED).
A weld here is a place where two different things travel under one word.

    1  corpus = one field       Their corpus is one field. An atom absent
                                from a corpus cannot be sampled from it.
                                "The space" is the space of that corpus.
    2  unavailable = network    "Unavailable" there is author-network
       distance                 distance. It is blind to people who hold
                                the combination and do not publish.
    3  holdout confirms only    A holdout can only confirm ideas someone
       the reached              later reached. It cannot score a branch
                                that is right and still unreached.
    4  same-family judging      An LLM judging LLM-proposed combinations
                                shares priors with the proposer; agreement
                                is not two readings.

[DERIVED] Inheritance into this method:

    weld 1   inherited by the atom list. Section 1's seven atoms are one
             session's list; a mechanism missing from it cannot be sampled.
    weld 2   inherited by CROWDING whenever a model assesses it. A model's
             "thin" is "thin in what was written down and trained on".
             This is why crowding_basis is mandatory: it is the only field
             that says whose view of density the tag is.
    weld 3   inherited by section 4 unchanged. Stated there.
    weld 4   NOT inherited by CLOSURE (a budget is not a judge). Inherited
             by CROWDING if the same model family proposes the branch and
             rates its crowding; crowding_basis must then say so.

## 7. Honest edges

1. [DERIVED] CLOSURE is necessary, not sufficient. A branch can conserve
   every budget and still be wrong about mechanism. `pass` means "not
   ruled out by conservation", nothing more.
2. [DERIVED] CLOSURE only reaches branches that model a conserved
   quantity. For the rest it reads `not checkable`, and the method then
   has no physics reading at all; it does not fall back to resemblance.
3. [PROPOSED] (co-authored) The crowding cut. NOT RECORDED stays as a
   fourth value.

       dense  = default reading appears on a cold first ask, unprompted
       thin   = appears only once the branch is named or primed
       absent = does not appear even when primed; corpus must be stated

   crowding_basis must name who ran the probe and which model.
4. [PROPOSED] Nothing here has been run. The selection rule, the atom
   admission test and the holdout spec are untested.

## Provenance

Co-authored, Kavik + Claude, work order of 2026-11-22. Sections tagged
[co-authored] carry the order as stated; DERIVED and PROPOSED lines were
added in this render and are marked. Statements about Artiles et al.
come from chat Claude's fetch of the arXiv abstract page
(arXiv:2603.01092v3) on 2026-11-22, relayed by the owner. Abstract only;
the PDF was not read by any party to this file. Atom extraction method,
coherence-model training, rater counts and stated limitations: NOT
RECORDED. The four welds are chat Claude's audit of the abstract
(DERIVED). No instrument, corpus or run accompanies this note. Mirrored
byte-identical in the Simulators repository at
`tools/density_vs_closure_sampling.md`.
