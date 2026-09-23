# CLAIM_TABLE — unowned-join

Ids are permanent and are never renumbered. `UJ_*` are claims about THIS
build and its reading of the delivered order; they are distinct from the
order's own numbered faces and steps. Every claim below is checked by
`test_unowned.py` unless its status says otherwise.

---

**UJ_001 — SUPPORTED.** The seven faces are parsed out of the delivered
order at call time and never retyped in the modules.
*Support:* `faces()` returns seven numbered entries, each occurring verbatim
in `WORK_ORDER.md` whitespace-flattened; an AST walk over both modules'
string literals finds no face text retyped; a document with no
`## Faces identified` section raises `OrderUnparsed` rather than returning
an empty list, since an empty face list would read as a census.
*Falsifier:* a face text present as a literal in either module, or a parse
returning fewer than the order's seven.

**UJ_002 — SUPPORTED.** The order's step 1 succeeds and what it returns is
smaller than it looks. A1–A4 can be stated, and once they are written down
the conclusion — that no check confined to a single scope decides the join —
follows in one line. The difficulty is not the inference. It is that A4 is
checkable only when every component's scope `S(k)` has been declared, and
nothing in the failures the order lists declares `S(k)` anywhere. The
formalisation relocates the work from the theorem to the declaration step.
*Support:* `verdict()` decides A1–A4 mechanically on any declared structure;
A1, A3 and the basis requirement are enforced at construction;
`NOT_EVALUABLE` is returned rather than a verdict whenever a scope is
undeclared.
*Falsifier:* a declared structure satisfying A1–A4 on which a check confined
to one `S(k)` decides the join.

**UJ_003 — SUPPORTED.** Two unowned states are kept apart, and merging them
would lose the distinction the order's own face 3 turns on.
`UNOWNED_BY_UNION` is a join the union of scopes covers and no single scope
does — every part visible to somebody, the relation to nobody.
`UNOWNED` is a join carrying an observable in no scope at all. The repairs
differ: the first wants an owner for an aggregation that exists, the second
wants an observable nobody holds.
*Support:* `[CHOICE 1]`; both verdicts reached by controls; face 3 returns
the first and faces 1, 2, 4, 5 and 7 the second.
*Falsifier:* a case where the two call for the same repair.

**UJ_004 — SUPPORTED.** Face 6, the frog, is the one face the order marks
UNRESOLVED and the one face the invariant returns `NOT_EVALUABLE` on — and
for the same reason. Declared per `[CHOICE 7]` on the order's own sentence
(*"You cannot list in advance which binaries will turn out false, because
that is precisely what the environment supplies"*), the environment's scope
is undeclarable in advance, so A4 is not checkable.
*Support:* face 6 is the only `NOT_EVALUABLE` row in the fit table; the
declaration is a single `UNDECLARED` scope and the verdict falls out of it
rather than being stipulated.
*Falsifier:* a declarable scope for the environment, stated in advance,
which would move face 6 to a verdict and refute the order's own reason with
it.

**UJ_005 — REFUTED (the order's strong claim), with the scope stated.** The
order: *"Because there is no good word, NO PROCEDURES CAN BE MADE AROUND IT
AND NO CODE CAN BE MADE AROUND IT,"* restated in its scope limits as *"No
term is coined, so this instrument cannot yet be implemented."* This folder
implements it: a checkable predicate over the structure, five reachable
verdicts, no term coined anywhere. The refutation is bounded to one
structure and one folder and does not establish that every unnamed structure
is codeable. **What survives is the order's own mechanism, two sections on:**
with a term a claim is a REPORT and status is inherited; without one the
same content is rebuilt across several sentences and reads as a PROPOSAL.
Code needs a predicate; transmission needs a name. The order merges the two
requirements and only the second is load-bearing.
*Support:* `code_without_a_term()` reports the predicate, the verdict
reachability, `term_coined: False`, and the scope sentence; both of the
order's lines are checked present in the delivered text.
*Falsifier:* an operation the invariant cannot express without a name for
the structure.

**UJ_006 — SUPPORTED.** No term is coined and the instruction is structural
rather than described. `coin()` raises `TermCoinageRefused`. The order's
step 3 is `NOT_RUN`: the cross-language status is `UNSEARCHED`, zero
languages are scored, and no vocabulary is scored from memory — the sources
are not reachable from this environment. `UNSEARCHED` is not *no term
exists*, and the order's own expected status is `named_elsewhere`
(`[CHOICE 8]`).
*Falsifier:* a term for the structure adopted or coined in this folder, or a
language scored without a search.

**UJ_007 — SUPPORTED, and it bounds every number in the folder.** Six of
seven faces hold the shape, and that is close to a tautology: the invariant
was abstracted from those same seven faces. The evidence test is the order's
step 2 — an eighth face supplied by someone who did not write the seven —
and it is `NOT_RUN`, because this session is the same party that holds them.
A face produced here would be one hand widening its own set.
*Support:* `STEP2["run"] is False` with the reason stated; the render
carries the warning above the counts, asserted by position.
*Falsifier:* step 2 run by a second party, in either direction — faces
arriving strengthens substrate-independence, faces stopping is the boundary,
and both are results.

**UJ_008 — SUPPORTED, and it is the weakest fit in the set.** Face 5, the
air gap, reads as an unowned join only because there is no component for the
unconsidered channel. That is not an evasion: it is why the overclaim goes
unchecked, and the structure records it as a join observable
(`channel_b_state`) lying in no declared scope.
*Falsifier:* a declared component for the second channel, which would move
face 5 to `OWNED` or `UNOWNED_BY_UNION` and make it a different face.

**UJ_009 — SUPPORTED.** The instrument is not `CONSTANT_FIRES`. Three of the
five controls do not hold the shape, including a structure whose join is
covered by a single scope (`OWNED`) and one whose component is declared not
locally correct (`LOCAL_FAULT`). The coverage figure keeps a measurement and
a silence apart: a declared join no declared scope reaches is `0.0`, while an
empty join and a scope set carrying an `UNDECLARED` member are `None`
(`[CHOICE 2]`). Reading an undeclared scope as an empty one would report the
shape from a silence, which is the failure the order is about.
*Support:* `join_coverage` is registered in `tools/known_answer.py` with six
cases; the `0.0` against the two `None`s is the pin.
*Falsifier:* a verdict returned on a structure carrying an undeclared scope.

**UJ_010 — SUPPORTED.** Three faces carry an arrow to a companion order and
all three resolve in this tree by folder path plus a content marker
(`[CHOICE 6]`): WO-1 to `chain-position/`, WO-2 to `quiet-aggregation/`,
WO-3 to `terminal-crossing/`. Faces 2, 5, 6 and 7 carry no companion, which
is a count and not a claim that they need one.
*Falsifier:* a companion resolving on a name occurring in prose with no
folder behind it.

**UJ_011 — UNVERIFIED, and it covers the folder.** Nothing here is a
measurement. Every structure is a declared reading written in this session;
the face-to-structure mapping is this audit's (`[CHOICE 5]`); no container,
rule, report, accounting boundary, channel, organism or institution was
observed. Whether the invariant separates the shape from its neighbours in
the field is untouched in both directions, and the order's own steps 2, 3
and 4 are the work that would touch it.
