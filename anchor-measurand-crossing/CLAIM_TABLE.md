# anchor-measurand-crossing — claim table

Claims are about the instrument, the delivered order's own arithmetic
and text, and the case material. None is a claim about any model's
behaviour under either arm: **no model has been run against this
instrument here**, and the order's own AP-1..AP-6 are carried UNVERIFIED
in `AMC_007`.

## REFUTATION_PROTOCOL

A refuted claim is updated forward with a new id; the old id keeps its
text and gains an UPDATE paragraph. The scorer is not retuned to save
a claim; the lexicon and transform lists are data and a disagreeing
reader rescores under their own.

| id | claim | status |
|---|---|---|
| AMC_001 | the two prompts are parsed out of `WORK_ORDER.md` section 4 at call time, never retyped; M+ is ARM M plus exactly one sentence; the order delivers two prompts for six claims, so the B and C arms AP-4 and AP-5 need have no verbatim prompt and the instrument refuses to render one | SUPPORTED |
| AMC_002 | the scorer's judgement lives in two published data files (a per-case lexicon with a transform tag on every alias; two transform lists), an unmatched quantity enters every count as a band and is never merged or split silently, and N4 is computed by rescoring every record under both lists | SUPPORTED |
| AMC_003 | the first crossing floor read a certain crossing as a possible zero, and a fixed-in-advance case caught it | SUPPORTED |
| AMC_004 | section 1 and section 6 disagree on one class: a quantity the method itself measures that is not a transform of the native (a component) is a crossing under section 6's arithmetic and not a crossing under section 1's definition, so an M-arm response naming one refutes AP-1 without crossing a measurand | SUPPORTED |
| AMC_005 | section 8 requires a control case and section 3 forbids a model-built one, so the control shipped here is a CANDIDATE the loader does not admit; N2 is NOT_EVALUABLE on the admitted corpus and its firing branch is shown reachable on the candidate | SUPPORTED |
| AMC_006 | section 5's one-arm-per-fresh-session rule is enforced at load, and AP-4's cued follow-up is the one arm that cannot obey it — the order's own protocol and its own fourth claim point different ways on follow-up turns | SUPPORTED |
| AMC_007 | nothing here bears on AP-1..AP-6, N1..N3 or the section 10 prediction; a run from inside this session would be void | UNVERIFIED |
| AMC_008 | normalization and alias matching are word lists, stated as such; coverage is printed per response so a lexicon that does not reach a real response is visible as a number, not a silence | SUPPORTED |

## AMC_001 — the prompts are read, not written

`prompt_templates()` locates the `### ARM M` and `### ARM D` headings in
the delivered file and dedents the four-space blocks beneath them; the
selftest asserts each template, whitespace-collapsed, is a substring of
the order, and that a rendered D prompt with its artifact block and
decision string substituted back out equals the template. The artifact
block is rendered as the section 3 field labels `claim:` and `method:`
on two lines (`[CHOICE 1]`) — the order says *verbatim, no commentary*
and does not fix a layout.

ARM M+ (AP-3) is not written out in section 4. It is built as ARM M
with the D sentence *This claim is cited to justify [DECISION].* added
and nothing else changed; the selftest checks that removing that one
sentence returns the M prompt exactly, under both placements. Placement
is `[CHOICE 2]`: `after_block` puts the sentence where D has it, `end`
appends it after M's last line, and a run record must say which.

AP-4 needs a *cued follow-up naming the set axis* and AP-5 a prompt
that *supplies a foreign measurand by name*. Neither text is in the
order; both exist only in the prior run's log, which is not delivered.
`render_prompt` refuses arms B and C with that reason, and the scorer
still reads B and C records if an operator logs them with their own
prompt text — the superset check and the supplied-measurand check are
built and exercised on constructed records.

## AMC_002 — the transform list is data, and so is the lexicon

Section 6's grouping rule (*same measurand if one is a transform of
the other under {integrate, differentiate, aggregate, disaggregate,
threshold, re-scope}; different if converting needs a coefficient,
model or measurement the method does not contain*) is a relation
between quantities, and no string operation decides it. So it is
written down per case: `lexicon.json` lists each case's measurands as
`native`, `component` or `foreign` with a `distinct_because` line on
every non-native entry, and every alias carries `via` — `identity` or
the transform that reaches it from the measurand's canonical quantity.
`transforms.json` carries two lists: `T-A`, the order's own six, and
`T-B`, dimension-preserving transforms only (a rate is not a stock; a
thresholded count is a fraction). An alias whose `via` is outside the
active list becomes its own measurand (`soc_mass@differentiate`), which
is how the same response scores differently under the two lists; N4 is
the count of records whose crossing band moves between them, printed
with both lists. On the constructed world the mp-01 M run moves
([0,0] → [2,2]) and the sc-01 D run does not.

A quantity matching no alias is `UNGROUPED`. It is not merged into the
nearest measurand and not counted as a new one; `crossing_band` returns
`[min, max]`, coverage is printed, and the claim verdicts have a third
value `undetermined_by_lexicon` for a band that spans the decision line.
The lexicon was written in the same session as the scorer and has no
external validation — section 12's first weak joint, unchanged, now in a
file whose sha is printed on every report.

## AMC_003 — the floor, caught by the known-answer case

The first `crossing_band` computed `crossing_min = distinct_min −
native_hit_max`: the fewest measurands the entries could be, minus the
most native hits they could contain. Those are two extremes that cannot
hold together — the ungrouped entry that collapses into an existing
measurand is not also the one that turns out native — and on one
grouped component plus one ungrouped quantity the floor read 0 where a
grouped non-native measurand is a crossing whatever the ungrouped entry
is. The case *non-native plus ungrouped* in `tools/known_answer.py`
expected (1, 2) and got (0, 2). Repaired: `crossing_min` is the count
of grouped non-native ids and `crossing_max` adds the ungrouped count.
The wrong first value is recorded in the case's `why_known` rather than
deleted.

## AMC_004 — component quantities: two sections, one class, two answers

Section 1 defines a crossing as *different quantity entirely (carbon
mass → CO2e; particle count → dose)*. Section 6 computes
`crossing_count = distinct measurands − native_hit`. An M-arm entry
whose quantity is **bulk density** — a quantity the sc-01 method
measures, not a transform of soil organic carbon mass, and not a
foreign quantity either — is a distinct measurand under section 6 and
is a crossing there, refuting AP-1; it is not a crossing under section
1's examples, which are all imports from outside the method. The
lexicon carries the class as `kind: component`, and `[CHOICE 3]` takes
section 6 literally so the headline number is the order's, while
printing `crossing_foreign` and `crossing_component` beside it so the
reading can be undone. N3 reports the class of every M-arm crossing,
and on the constructed world the one M-arm refutation is
component-plus-ungrouped, not foreign. Section 8 N3 anticipates that M
reaches crossings on *some case class* and asks which; on this
instrument's evidence the first class to look at is the method's own
components.

## AMC_005 — the control case is a candidate, not a case

Section 8 says a control where the native measurand IS the decision's
measurand is required. Section 3 says cases must be hand-built and
records four model-generated sets as defective. This folder was built
by a model. `cases.jsonl` therefore carries `ctl-01` (lead action-level
compliance, decision denominated in the 90th-percentile first-draw lead
concentration the method reports) with `hand_built: false` and a source
line saying so; `load_cases()` excludes it, `amc.py cases` lists it,
and a run record naming it is refused. `validate_case` requires a
control to declare `control_decision_quantity` equal to its native
after normalization, and refuses one that does not. On the admitted
corpus N2 reads `NOT_EVALUABLE`; under `admit_candidates=True` the
selftest shows both branches — a D response saying `yes` and naming the
native reads *control clean*, one flagging a gap reads *gaps on
demand*. Adopting the candidate is one field flip after an operator has
checked the method is correctly scoped for its own question; nothing
here has checked that.

## AMC_006 — one arm per session, and the arm that cannot obey

`validate_runs` refuses any session id carrying two records unless
every record after the first is a B arm naming a predecessor in the
same session. That exception is not a loosening: AP-4 is about *a
cued follow-up* to an uncued predecessor, which is by construction a
second turn in one session, while section 5 says *no follow-up turns*.
Both are the order's text. The exception is scoped to B alone so the M,
D and M+ arms stay cold as section 5 requires; a log with M and D in one
session is refused. The order index is a logged field and `plan` emits
a seeded randomized order so the log can be checked against it.

## AMC_007 — what is not measured here

No arm has been run. Three reasons, any one sufficient: this
environment has no model endpoint; the session that built the scorer
holds the lexicon, so its own responses are not blind
(`frame-location-benchmark` `FLB_010`); and section 5's cold-arm rule
cannot be met from inside one session that has read the whole order.
Every record in `runs/constructed.jsonl` is marked `constructed: true`
and the report banners it. AP-1..AP-6 are therefore untouched in both
directions, N1 has no coded sheet, N2 has no admitted control, N3 has
no real M-arm response, and section 10's field-level prediction is not
approached. The section 2 numbers (0 crossings on 3 × 2 method-anchored
passes, 11 on 1 × 2 decision-anchored) are carried from the order and
are not re-derivable from anything delivered.

## AMC_008 — the word lists are stated

`normalize` lowercases, drops parentheticals, and removes tokens on
three printed lists (units, articles, hedges). `group` matches an alias
by exact normalized equality first, then by every alias token being
present in the quantity, longest alias first. That second step is a
word list deciding a grouping (`nonidentity-census` T1-1), and it is
where a real response will disagree with the lexicon — a quantity
written in words no alias carries reads UNGROUPED, and one that
happens to contain an alias's tokens groups whether or not it should.
Coverage (grouped / entries) is printed per response so the first
failure shows as a number; the second shows only in the per-entry rows,
which is why every row is printed with the alias route it took.
