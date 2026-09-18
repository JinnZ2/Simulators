# CLAIM TABLE -- substrate-alternative

Ids are permanent.  `SA_` = substrate-alternative.  Status is one
of SUPPORTED / REFUTED / UNVERIFIED.  Every SUPPORTED claim is a
property of the two modules or of their measured output, and is
recomputable by anyone with the folder:
`python3 test_substrate.py` (126 checks).

---

## frame_audit.py

**SA_001 -- LOCATE ONLY is enforced, not promised.  SUPPORTED.**
`frame_audit.py` carries no field in which a replacement could be
written.  An AST walk over every identifier, argument, attribute,
function name and dict key finds none of
`suggest / suggestion / replace / replacement / instead /
alternative / rewrite / recommend / recommendation / improve /
fix / better / prefer / should`, and `Hit._fields` intersects that
vocabulary at zero.  The scan is null-tested: a planted module
containing `def suggestion` fires it.  *Falsifier:* an identifier
from that vocabulary appearing in the module, or a returned field
carrying a proposal.

**SA_002 -- every declared frame is reachable and every absence is
a visible zero.  SUPPORTED.**  One constructed sentence per frame
puts all five above zero.  `zero_counts()` returns an ordered dict
carrying all five keys, so a frame with no hits reads `0` rather
than being absent -- a caller cannot otherwise tell a frame that
did not fire from one nobody examined.  The negative is reachable:
a three-sentence text about a flood returns `hits_n 0` with three
sentences counted, so the module is not `CONSTANT_FIRES`.

**SA_003 -- sense-ambiguity is a third state, counted apart.
SUPPORTED.**  Of 165 registry entries, 32 carry a live non-money
sense (`value` = absolute value; `property` = a property of a
system; `cost` = a cost function; `budget` = an energy budget;
`competition` = a measured ecological interaction; `efficiency` =
a measured ratio; and so on), each with a stated reason.  Three
counts are returned and never collapsed -- total, unambiguous,
ambiguous -- and `total == unambiguous + ambiguous` holds per
frame.  A single collapsed count would silently include the
physics senses or silently drop them, and the module locates, it
does not adjudicate which sense is live.

**SA_004 -- matching is by word boundary, never substring.
SUPPORTED.**  `The supermarket is downtown and well known.`
returns zero hits; `The market is open.` returns one.  The failure
this avoids is the one recorded elsewhere as a `lean` matching
inside `clean`.

**SA_005 -- THE LIMIT: a word list, and a paraphrase steps around
it.  SUPPORTED, and measured rather than asserted.**
`You have to pay for it.` returns one hit.
`It takes something from you before you may have it.` returns
zero, and carries the same frame.  Inflections are not generated
either: `compete` is registered and fires, `competing` is not and
does not.  So a zero from this module is a property of THE
REGISTRY and never evidence that a text is frame-free.  The
registry's coverage is the measurement; the text is the sample.
This is stated at the TOP of `frame_audit.py`, not the bottom.

**SA_006 -- a surface form carries exactly one frame, and a
collision raises at load.  SUPPORTED.**  `[CHOICE 5]`.  Longest
match wins at a position `[CHOICE 1]`, so `cost-effective` is one
VALUE_AS_PRICE hit rather than a PRICE hit plus a loose word, and
`supply and demand` is one SCARCITY_AS_GIVEN hit.  The alternative
-- counting both -- double-counts one utterance.

---

## pilot_loop.py

**SA_007 -- THE ICS FINDING: the substrate's own vocabulary
carries the thing being removed, and that is what fires the
screen.  SUPPORTED.**  The screen over `pilot_loop.py` returns
**0 unexempted hits and 5 exempted**, and the five reduce to four
distinct entries: `finance`, `procurement`, `compensation`,
`cost`.  Every one is a name ICS itself gives a part of its
structure -- the **Finance/Administration** section of the General
Staff, and three of its four units (**Procurement**,
**Compensation**/Claims, **Cost**).  One of four General Staff
sections, and three of its four units, are the part of the
structure this loop has no channel for.  A pilot that borrows ICS
as a substrate has dropped or repurposed a quarter of what it
borrowed, and the doctrine says so before any of ours does.
Recorded, not smoothed.  *Falsifier:* a reading of the doctrine
showing Finance/Administration is not a General Staff section, or
that its units are not the four named.

**SA_008 -- the anticipated second exemption turned out to be
unnecessary, and is recorded rather than kept empty.  REFUTED (as
a prediction), SUPPORTED (as a record).**  A region was reserved
for the module docstring on the reasoning that a module cannot say
which signal it removed without naming it, use-mention being
invisible to a word screen.  The docstring was then written
without the vocabulary, the anticipated hits did not occur, and
the region was deleted.  An unfired exemption left in place reads
as a hit that was forgiven.

**SA_009 -- the matching rule is OURS, not ICS's.  SUPPORTED.**
ICS specifies a request channel (ICS-213RR) and an assignment
authority.  It does not specify who wins when two requests meet
one pallet.  Earliest horizon first, ties by node id `[CHOICE 2]`;
within a need, nearest eligible capacity first, ties by node id
`[CHOICE 3]`.  Both are printed by `--choices` and cited at the
line where they take effect.  `[CHOICE 3]` carries its own
counter-rule: drawing from the largest holder first, to keep small
holders in reserve, is defensible and gives a different log.

**SA_010 -- UNMET is a first-class return type and all four
reasons are reachable.  SUPPORTED.**  `UNMET(node, resource,
quantity, reason)` is a namedtuple, not an exception (asserted
both ways), and `resource` is `[CHOICE 1]` on top of the three
fields asked for, because a node may need two resources and a bare
quantity would not say which went unfilled.  Four constructed
scenarios reach `NO_CAPACITY_DECLARED`, `CAPACITY_EXHAUSTED`,
`UNREACHABLE` and `ARRIVES_AFTER_HORIZON` respectively, and the
suite asserts no declared reason is unreachable -- a reason nobody
has seen fire is not known to fire.  The negative is reachable
too: a scenario with nothing unmet returns `[]`.  A partial fill
returns BOTH an allocation for what moved and an UNMET for the
remainder.

**SA_011 -- absence and zero are kept apart at four sites.
SUPPORTED.**  An undeclared route returns `None` from `travel()`
`[CHOICE 4]`, never a large number and never zero -- both would
put an undeclared route on the same scale as a declared one.  A
node that received nothing has `max_lag None` and `lags []`, never
`0`, which would read as instant delivery.  `needed` is carried
even where nothing moved.  And the four UNMET reasons split what a
single "not filled" would merge.

**SA_012 -- no composite per node, and no ranking anywhere.
SUPPORTED.**  `[CHOICE 7]`.  A per-node cell carries
`needed / met / unfilled / lags / max_lag / min_lag` and no
seventh number; nothing is summed across nodes and the run returns
no total.  An AST scan finds no identifier from
`rank / score / best / top / winner / leaderboard / priority /
weight / merit / standing`, and is null-tested with a plant.  One
number per node would be a standing for the node, which is a
second allocation signal arriving through the readout.

---

## What this does not establish

**SA_013 -- THE BLIND SPOT.  SUPPORTED, and it is the sharpest
thing in the folder.**  Removing the price signal and keeping ICS
substitutes an allocation rule for one signal AND a command
authority for another.  ICS coordinates a response under a
declared incident with a declared commander.  `frame_audit`
screens for one vocabulary and the authority assumption is not in
it, so the screen returns clean on a module that made a second
substitution it cannot see.  **The screen has a blind spot exactly
the shape of the substrate chosen to fill the hole it screens
for.**  *Falsifier:* a frame label for delegated authority, with a
registry, that fires on `pilot_loop.py`.  None is built here,
because inventing one in the same session that wrote the module
would score the module against a list written to let it pass.

**SA_014 -- the result is smaller than it sounds.  SUPPORTED by
construction.**  A matching rule that hands limited capacity to
several needs IS a distribution decision.  A number attached to a
unit of food is one such rule.  Removing it does not remove the
decision; it makes the rule explicit, logged, and arguable.  That
is the whole of what `pilot_loop.py` does.

**SA_015 -- every ICS fact is CARRIED and unverified.
UNVERIFIED.**  The General Staff sections, the Finance/Admin
units, ICS-213RR / 211 / 204 / 215, the resource-status
vocabulary, span of control 3-7 and the Planning P are all
transcribed from memory.  This environment's network is an
allowlist and the doctrine hosts are not on it, so nobody here
opened a source.  `SA_007` rests on this and says so.

**SA_016 -- nothing here is a statement about any food system.
UNVERIFIED.**  Every scenario in the folder is constructed and
declares itself so.  No distribution has been run, no capacity
declared by anyone, and no need declared by anyone.  What is
established is that the loop returns what its specification says
it must.

**SA_017 -- the AST scan is a copy, and a copy drifts.
SUPPORTED.**  The identifier scan in `test_substrate.py` exists
elsewhere as a shared tool.  It is reimplemented here because this
folder is meant to stand as its own repository, and importing
across the repository boundary would make it unpromotable.  The
discipline it breaks is the one recorded as "import rather than
copy"; the cost is a second copy that can drift from the first
without either noticing.  Stated rather than hidden.

**SA_018 -- the folder did not land in the repository it was
addressed to.  SUPPORTED.**  `JinnZ2/substrate-alternative` does
not exist and could not be created from this session: the GitHub
integration answers `403 Resource not accessible by integration`
to a repository-create call, and `add_repo` answers `not found`.
The folder is therefore self-contained and promotable -- stdlib
only, no imports across its boundary, its own LICENSE and its own
suite -- and a `git subtree`/`git filter-repo` split moves it
without editing a line.

**SA_019 -- a count in the prose disagreed with the registry, and
was found by running rather than by reading.  SUPPORTED.**  The
README and this table first stated that 23 entries carry a second
live sense.  The registry holds **32**.  A transposition, in a
folder whose whole subject is a number standing in for a thing.
Nothing in the modules moved; what was false was the description.
Both counts are now asserted in the suite against the loaded
registry, and the suite additionally requires the figure to appear
in both documents, so a change to the registry that is not carried
into the prose turns a check red rather than leaving two numbers
disagreeing in different files.
