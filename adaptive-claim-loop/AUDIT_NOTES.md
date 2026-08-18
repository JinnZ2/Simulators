# AUDIT_NOTES — adaptive-claim-loop

Two things in this folder. [`adaptive_loop.py`](adaptive_loop.py) is the
module; [`delivered/`](delivered) holds an uploaded adaptive simulation
framework and its two provenance logs, verbatim and unmodified, and
[`replay_delivered.py`](replay_delivered.py) reads them.

    python3 adaptive_loop.py --selftest
    python3 adaptive_loop.py
    python3 replay_delivered.py
    python3 gate_null_test.py
    python3 adversarial_probe.py

## What this is

The delivered framework is a competent piece of work: provenance dataclasses,
a claim system with predicates and evidence, a spatially explicit forest
model, a switching Moran process, an agent that reads outcomes and proposes
changes, an adaptive loop, a CLI. It is a good instance of a shape that is
becoming common.

Its agent has exactly one move. `_propose_action` returns
`(new_params, description)` — there is no other return shape — so when a
claim fails, the only thing that can happen is a parameter change. **That
operation cannot fail.** It searches for a setting under which the prediction
is true, and the reasoning chain records each step as a hypothesis tested.

This module is the same architecture with that move removed and four others
put in its place, plus the guards that keep it from coming back as a sweep.

## File status

| file | status |
|------|--------|
| `delivered/adaptive_sim_framework.py` | delivered, verbatim |
| `delivered/provenance_forest.jsonl` | delivered, verbatim — 2 rows |
| `delivered/provenance_fluctuating.jsonl` | delivered, verbatim — 5 rows |
| `delivered/adaptive_sim_results.png` | delivered, verbatim |
| `adaptive_loop.py` | added — the module, selftest 53/53 |
| `replay_delivered.py` | added — the delivered moves through the gate |
| `gate_null_test.py` | added — the null-harness invariant over the gate |
| `adversarial_probe.py` | added — a responder that relabels until something is admitted |
| `README.md` | added |
| `AUDIT_NOTES.md` | added |
| `samples/` | added |

Nothing in `delivered/` is modified, and the module does not import it.

## Claims

| id | claim | falsified by | status |
|----|-------|--------------|--------|
| ACL_001 | Every agent action in the delivered log is a parameter change (3 of 3 non-terminal moves), and the architecture admits no other: `_propose_action` has one return shape, so "the claim was wrong", "the readout is wrong" and "this failure is the result" are not expressible | a second return shape, or a non-parameter action in the log | SUPPORTED |
| ACL_002 | The three-step walk did **not** produce the pass the log appears to show: run 4 is 556 s later, carries the session's first seed (123), and sits at the original `switching_rate` 0.3, which no logged action produces. `ProvenanceLogger` appends with no session field, so two invocations are one file | a session marker in the delivered log, or an action returning the parameter to 0.3 | SUPPORTED |
| ACL_003 | Offered to this gate, the delivered walk is refused three ways — one level is not a sweep, levels below the current setting do not bracket it, and an edit justified by "the claim failed" is justified by its outcome — while the restatement the protocol asks for is admitted | any of the three being admitted, or the restatement being refused | SUPPORTED |
| ACL_004 | `Claim.test` assigns `status = "inconclusive"` on an exception and then returns `False`; the runner reads only the bool, so a predicate that raised is logged as `failed` — the correct value is computed one line above the return and discarded at the call site | the runner reading `claim.status` | SUPPORTED — tenth instance of the absent-vs-known-negative repair, fourth found rather than designed in |
| ACL_005 | The termination branch is reached both on budget exhaustion and on success and emits one sentence for both; run 3 prints "Final iteration or all claims passed." with both claims failed | the two cases printing differently | SUPPORTED |
| ACL_006 | The delivered framework carries three things this module does not — real spatially explicit models, claim generation, figures — and the claim here is about the response vocabulary and the record, not about the models | this folder claiming a modelling result | SUPPORTED (holds) |
| ACL_007 | The bracketing guard refused this module's own stub responder before any finding rested on it: the first version used a fixed ladder `[-0.05, 0, 0.05]` and was refused as soon as a scenario started at advantage 0.06 | the guard passing a one-sided ladder silently | SUPPORTED (holds) |
| ACL_008 | `Sweep` needs a predicate over the readings and not a sentence — the first version took a prose `gradient_claim` and the loop walked one level per iteration while re-reading the **point** claim, which is the removed move with extra steps | the loop evaluating the point claim after a sweep is admitted | SUPPORTED — found in this module, repaired |
| ACL_009 | The shipped responder is a stub and is not the contribution; the gates are in the type system, so they are unchanged whether the responder is a person, a script or a model | a gate that depends on which responder is installed | SUPPORTED (holds) |
| ACL_010 | The gate discriminates rather than refusing on surface form: TP 1.00 over the delivered agent's ten branches (AST-enumerated, justified with its own hypothesis text), FP 0.00 over six proposals written for two other folders, `null-harness` grade **OK**, 10 of 10 matching a pre-registration printed before the gate was called | a signal item admitted, or a null item refused | SUPPORTED |
| ACL_011 | The epicycle guard is a **declaration, not a check** — `independently_falsifiable` and `predicts_beyond_parent` arrive as booleans from the caller and nothing derives either from the restatement's text, so it cannot be null-tested from text at all | a routine deriving either from the text | SUPPORTED |
| ACL_012 | The null test found one hole: `InstrumentEdit` admitted the delivered agent's random `num_replicates += 20` on the prose artifact "sampling noise", because it required three non-empty strings and nothing more — the module's README already said this edit is admissible because the gap is *computable*, and the gate was not asking for the computation. Repaired with a sixth response class, `RESOLUTION_EDIT` | the prose form being admitted again | SUPPORTED — found, diagnosed, repaired, pinned by 6 selftest assertions |
| ACL_013 | The repair's limit, stated: `ResolutionEdit` checks that two numbers were supplied and that `need > have`; it does **not** check that `need` is what the claim's tolerance implies, so `have=50, need=70` is admitted. Closing it needs the tolerance declared on the CLAIM rather than on the response, and no claim here declares one as data | a gate that reads the claim's tolerance | SUPPORTED (open, and named) |
| ACL_014 | A persistent responder gets the walk ADMITTED in **five attempts**, each amendment being what the gate asked for in the sentence it refused with; the last one supplies `lambda r: (True, ...)` because `Sweep` required `callable(...)` and nothing more — the gate checked a predicate exists, not that it can say no | the walk surviving no relabelling, or being admitted in one | SUPPORTED |
| ACL_015 | Before the repair that was **worse than the failure this module was built against**: admitted sweep → constant predicate returns SUPPORTED → gradient claim replaces the point claim → loop terminates `converged`. A walk with a session-stamped audit trail and a supported claim at the end. Repaired in `Loop.run_sweep`, not in the constructor, because the constructor has no readings to run the predicate on | the check working at admission time | SUPPORTED — found, repaired, both stages measured |
| ACL_016 | The discrimination rule had to be tightened from "some counterfactual moves" to "the **permuted** one moves": under `any`, every symmetric function of the outcomes passed — measured, `sum > 1.8` and `max > 0.8` and `variation exists` all differ on `flattened` only. Cost stated: a variation-only claim is now refused, and the two failure cases are reported apart because they need different fixes | a symmetric predicate producing a sweep verdict | SUPPORTED |
| ACL_017 | The outcome screen is stepped around in one amendment by paraphrase, as any keyword screen is (`UNI_009`, `DF_010` are the same shape). The guards that hold against paraphrase are the two that ask for a number or a computation — `ResolutionEdit`'s have/need and the discrimination check. **A guard that asks for prose can be satisfied with prose** | a prose guard that survives paraphrase | SUPPORTED (holds) |

## 1 — ACL_001, one move

    run  switching_rate  fixation  slow    action
    0    0.3             failed    failed  Decreased switching_rate to 0.2100
    1    0.21            failed    failed  Decreased switching_rate to 0.1470
    2    0.147           failed    failed  Decreased switching_rate to 0.1029
    3    0.1029          failed    failed  Terminate loop
    4    0.3             passed    passed  Terminate loop

    agent actions that change a parameter : 3
    agent actions of any other kind       : 0

Three of three. Not because the agent chose parameters each time — because
`_propose_action` returns `(new_params, action_str)` and the loop assigns
`current_params = new_params`. The hypothesis strings the agent generates are
rich ("switching too fast relative to demographic rates, or population size
too large for drift") and every one of them resolves to a dial.

Put through this module's gate, the walk is not refused for being wrong. **It
has no constructor.** That is the difference between a guard and a
vocabulary: a guard says no to a thing that can be expressed, and this cannot
be expressed.

## 2 — ACL_002, the walk did not produce the pass

    run 0  seed=123  switching_rate=0.3     failed
    run 1  seed=124  switching_rate=0.21    failed  +0s
    run 2  seed=125  switching_rate=0.147   failed  +0s
    run 3  seed=126  switching_rate=0.1029  failed  +0s
    run 4  seed=123  switching_rate=0.3     passed  +556s

Run 4 carries seed **123** — the first seed of a session, not the fifth —
sits at the **original** parameter value, and arrives nine minutes later. No
action in the log moves `switching_rate` back to 0.3. It is a second
invocation of the script, appended to the same file.

So the reading the log invites — the agent lowered the switching rate and the
claims came good — is false in the delivered data. The claims passed in a
different session at the untouched parameter, and the walk resolved nothing.
The forest log has the same shape: two rows, both seed 42, 580 s apart.

`ProvenanceLogger.__init__` takes a path, opens in append mode and writes no
session field, so a run's ordinal within its loop is not recoverable. This
module emits `SESSION_OPEN` / `SESSION_CLOSE` and stamps every row with its
session and an ordinal — the entire repair, and it is four lines.

This is the finding that matters most, and it is not a criticism of the
agent. It is a property of the **record**: a log that cannot separate
sessions will be read as one trajectory, and the reader who does that is
reading correctly given what the file says.

## 3 — ACL_003, the delivered moves through the gate

    REFUSED  the walk, named honestly            a sweep needs at least two levels
    REFUSED  the walk dressed as a sweep         levels do not bracket the current value
    REFUSED  the walk with the log's hypothesis  edit justified by outcome -> 'claim failed'
    ADMITTED the response the protocol asks for  -> CLAIM_UPDATE

Three reasons, three different guards. The admitted one is a restatement:
slow-strain fixation was observed at exactly `0.0000`, which is a different
shape from "below a 5% threshold", and the claim that fits it names the ratio
of switching to demographic timescale as the exposed variable.

**The gate is not smarter than the delivered agent.** It refuses categories,
not judgements. The same walk offered with bracketing levels, a gradient
claim and a predicate over the readings is admitted — and is then an
experiment rather than a search.

## 4 — ACL_004, an exception filed as a refutation

    except Exception as e:
        self.status = "inconclusive"
        return False, f"Test error: {str(e)}", {}

and at the call site:

    passed, msg, details = claim.test(outcomes)
    claim_results[claim.claim_id] = {'status': 'passed' if passed else 'failed'}

`inconclusive` is the right value and the field already exists. It is
assigned one line above the return and never read. A predicate that raised —
a `KeyError` on an outcome the model did not produce, say — is written to the
provenance log as `failed`, and the agent is dispatched to fix a claim that
was never tested.

Tenth instance of one repair across this drop family, and the fourth found
rather than designed in:

    PB_004   frame_sim option_gain           found -- merged
    PB_012   binary_audit handoff()          found -- merged
    GC_004   MECHANISM_10 R3                 found -- merged
    MD_002   moral-decomposer reduces_to     found -- merged
    CC_002   closure.py rules_out            found -- merged
    ACL_004  Claim.test exception path       found -- computed, then discarded
    GC_010   SUBCASE_10A S1                  designed in -- specified
    DL_008   anchor.py routing states        designed in -- implemented
    CC_001   closure.py knowledge_state      designed in -- vocabulary
    CA_002   assemble.py sufficiency         designed in -- fail-closed

This one is the cheapest of the ten and the only one where the correct value
is already in a variable.

## 5 — ACL_005, one branch, two meanings

Run 3 records `"Final iteration or all claims passed."` with both claims
failed. The `else` is reached when the budget runs out and when everything
passes, and it emits the same sentence for both.

Four named states here, asserted distinct in the selftest. The fourth,
`no_admissible_response`, has no counterpart in the delivered architecture —
it is what happens when every proposal a responder made was refused, and it
fires in the demo when the stub responder's sweep is rejected.

## 6 — ACL_006, what the delivered framework has that this does not

Three things, and the folder should say so plainly.

`ForestScalingSim` is a real lattice model with dispersal, competition and
metabolic scaling. The two demo models here are a Moran process and a
piecewise line, sized to make the gates visible.

`_generate_claims` proposes new claims from outcomes. There is no equivalent
here, and the gap is deliberate rather than principled: a generated claim is
one whose falsifier was chosen after seeing the data, and the admission rule
for that is not written. That is a real hole, not a design decision dressed
as one.

And the drop ships a figure.

The claim in this folder is about the response vocabulary and the provenance
record. A parameter walk under a good model still tells you nothing; a gate
over a toy model still refuses the walk. They are separable, and only one is
here.

## 7 — ACL_007, the guard caught the author

The stub responder's first version proposed a fixed ladder for the drift
sweep:

    levels=[-0.05, 0.0, 0.05]

which is fine while the scenario sits at advantage 0.0 and is refused the
moment it sits at 0.06 — three levels all below the current setting, offered
against a claim that fails because the setting is high. The demo stopped on
`no_admissible_response` and the refusal was in the log.

It is recorded rather than quietly fixed because it is the only evidence in
the folder that the bracketing guard fires on something nobody wrote it for.
The repair was to centre the levels on the current value, and the comment in
`ConservativeResponder` says what happened.

## 8 — ACL_008, the sweep was the removed move for one revision

`Sweep`'s first version took a prose `gradient_claim` and no predicate, and
`Loop.apply` set the parameter to the next declared level each iteration
while the loop re-evaluated the **point** claim. That is: a directed sequence
of single parameter changes, with a sentence about a gradient attached that
nothing evaluated.

It is the delivered framework's move with a better name on it, and it was in
this module until the demo output made it visible — the drift sweep set
`advantage` to −0.05, `p_fix` moved 0.617 → 0.317, and the claim was still
being read at the point.

The repair is the shape `measurement-fork` `MF_020` names: a spec that cannot
say what would refute it produces a design incapable of failing. `Sweep` now
requires a callable, `Loop.run_sweep` evaluates the model at every level in
one iteration, the gradient predicate reads the whole set, and the gradient
claim replaces the point claim it was raised against. `Loop.apply` no longer
touches parameters for a sweep at all.

Measured after the repair, on the `drift-selected` scenario:

    p_fix across advantage [0.0, 0.06, 0.12] = [0.515, 0.698, 0.833]

Monotone, and 0.515 at advantage 0. The point claim ("p_fix ≈ 0.5") was
correctly refuted at advantage 0.06; the gradient claim that replaces it is
supported, and is a statement the readings could have broken.

## 9 — ACL_009, the responder is not the contribution

`ConservativeResponder` is rule-based, hardcoded per claim id, and exists so
the loop runs and so every refusal branch is reachable in the selftest. It
would be easy to make it look good — a responder that always returns
`CLAIM_UPDATE` passes every gate — and that is precisely why the gates and
not the agent are the object here.

The check is structural: `Loop` calls `responder.respond(...)` and knows
nothing else about it, and every admission rule lives in a `Response`
constructor. A person, a script or a model reaches the same refusals.

What this does **not** establish is that the vocabulary is complete. Five
responses were chosen because five failure modes were in front of us; a sixth
would be found the same way, by something being refused that should not have
been. Nothing here has been run against a responder the author did not write,
which is the obvious next measurement and is not taken.

---

# The null test

`gate_null_test.py`. Added after the folder shipped, because `ACL_009` named
the hole and the hole was reachable.

## 10 — ACL_010, does the gate discriminate

The 45 selftest assertions check that each guard **can** fire. A gate that
refuses everything passes every one of them. Firing is not discrimination,
and nothing here had measured the second thing — which is the `null-harness/`
invariant, and it applies to this gate exactly as it applies to any other.

Two arms, and the sourcing is the whole design:

| arm | source | independent? |
|-----|--------|--------------|
| signal (must refuse) | the delivered agent's ten `actions.append` branches, enumerated from its source by AST | yes — another author, no knowledge of this gate |
| null (must admit) | 3 `MechanismEdit` proposals from `photoperiod-claim-harness/PENDING_EDITS`, 3 claims from `equivalence-field/seed_claims()` | half — see `ACL_011` |

Neither arm was written for this test. Each signal branch is offered in the
**most favourable admissible form** it could take, justified with the
delivered agent's own hypothesis text and nothing else, so a refusal is
about the justification rather than about a hostile transcription.

Expected verdicts are pre-registered and printed before the gate is called
once — 9 REFUSE / 1 ADMIT on the signal arm, all ADMIT on the null arm.
**The single expected admission is the point.** A gate that refuses 10 of 10
is refusing on surface form — "it changes a number" — and is scored here as
over-tight, not as perfect.

    signal arm : 9 of 9 refused as expected  (TP)
    signal arm : 10 of 10 matched the pre-registration
    null arm   : 0 of 6 wrongly refused      (FP)
    TP rate    : 1.00
    FP rate    : 0.00
    grade      : OK

The branch that admits is `num_steps *= 1.5` under "simulation not at steady
state" — a diagnosis about the **run**, checkable without reference to the
verdict. `switching_rate *= 0.7` and `num_steps *= 1.5` are both "multiply a
number", and they separate on the justification alone. That is `ACL_003`'s
"categories, not judgements" measured instead of asserted.

**One correction to this test, made before it was published.** The first
version offered each parameter branch as a single-level sweep, so nine of
them died on the two-level guard without reaching the others — one guard
tested nine times, dressed as nine results, and weaker than the file's own
stated protocol. Corrected to offer `[current, proposed]`, which clears the
two-level and bracketing guards and tests the predicate guard instead. The
correction can only move a result toward ADMIT, never toward REFUSE.

## 11 — ACL_011, the epicycle guard is a declaration

`ClaimUpdate` refuses unless `independently_falsifiable` and
`predicts_beyond_parent` are both true, and both arrive as booleans from the
caller. Nothing derives either from the text of the restatement, so a
responder passing `True, True` is never refused on that guard whatever it
wrote.

Third folder, one shape: `domain-ledger` `DL_015` (band membership is a
string the author writes, nothing derives it), `generation-capacity`
`GC_003` (the calibration constraint is a declared field, not a unit check),
and this.

It is not nothing — a declaration that must be made is a place to lie
deliberately rather than by omission, and it sits in the log beside the
restatement it licensed. But it cannot be null-tested from text, which is
why the null arm is six items and not sixty: the corpus that would test it
is restatements labelled by someone other than their author, and no such
corpus exists in this repo.

The checkable half of the same guard **is** checked. `new_refuted_if` must
differ from the parent's, whitespace- and case-normalised, which catches a
restatement that moved only its wording.

## 12 — ACL_012, the one hole the test found

`num_replicates += 20` — the delivered agent's `else`-branch, fired at
random with no gap computed — was **admitted** as an `InstrumentEdit` whose
artifact was the phrase `"sampling noise"`.

Pre-registered REFUSE, and the pre-registration was right. The README says
this edit is admissible because the resolution gap is **computable**, and
the gate was not asking for the computation: `InstrumentEdit` required three
non-empty strings plus the outcome screen, so a fluent phrase satisfied it.

Same shape as `reasoning-dial` on `G-FIT` — the rule is "name why the
statistic can discriminate", the implementation checks a string is
non-empty, and a wrong-but-fluent sentence passes.

**Repaired.** `ResolutionEdit` is the sixth response class and requires the
resolution you HAVE and the one the claim NEEDS, as numbers, with `need >
have`; `InstrumentEdit` refuses when its artifact names a resolution claim
in prose and says which class to use. Six selftest assertions pin it, the
first being the exact proposal that got through. The demo's drift scenario
now emits `RESOLUTION_EDIT` where it emitted `INSTRUMENT_EDIT`, which is
what the responder was already computing — it had the number and the gate
never asked for it.

The direction matters, because "the test disagreed and then the code
changed" is the failure mode this entire folder is about. The rule was
written before the test — it is in the README — and the gate was
under-implementing it. The change makes the gate stricter, on a rule it
already claimed. That is the distinction between closing a specification gap
and tuning to an outcome, and it is the same distinction the gate itself
enforces on a responder.

## 13 — ACL_013, the limit of the repair

    REFUSED  num_replicates += 20, as offered (prose)
    ADMITTED num_replicates 50 -> 70,  no gap stated
    ADMITTED num_replicates 50 -> 157, gap computed

The middle row is the honest limit. `ResolutionEdit` checks that two numbers
were supplied and that `need` exceeds `have`. It does **not** check that
`need` is the number the claim's tolerance implies, so an agent writing
`have=50, need=70` because its `else`-branch adds 20 is admitted — with the
arbitrary pair sitting in the log where a reader can see it.

A smaller hole than the prose one, and a different kind: the first let a
phrase stand in for a computation, this one requires the computation to be
shown but not to be right.

Closing it needs the gate to know the claim's tolerance, which means the
resolution requirement moves onto the **claim** rather than the response — a
change to where the number lives, not a change to the guard. Not made here,
and the reason is specific: no claim in this module declares a tolerance as
data. `ACL_drift_neutral` carries `NEUTRAL_TOL` inside its predicate, where
the gate cannot reach it.

`ACL_009` is unchanged by all of this. The gate has now been run against
proposals the author did not write, which is what that claim said had not
happened — but a responder the author did not write is still not the same
thing, and none has been run.

---

# The adversarial probe

`adversarial_probe.py`. The other half of `ACL_009`: `gate_null_test.py`
ran the gate against proposals written elsewhere, and a **responder** is not
a proposal — it reads a refusal and tries again. Static proposals cannot
push back.

**Threat model.** Get a parameter change carried out and the claim off
REFUTED. Truth is not a consideration. It is the delivered agent's policy
with persistence added.

**What constrains it.** It never reads `adaptive_loop`'s source; its
knowledge of the gate is `inspect.signature` over the six response classes
plus the text of each refusal, both of which any caller has. Its retries are
driven by the refusal message rather than by hand-picked bypasses — the gate
says what it wants, the adversary supplies that and resubmits. It is written
here, which is the honest limitation and is stated in `ACL_017`.

## 14 — ACL_014, five attempts

| try | verdict | gate said | adversary then |
|-----|---------|-----------|----------------|
| 1 | REFUSED | edit justified by outcome | paraphrased around the flagged phrase |
| 2 | REFUSED | a sweep needs at least two levels | added the current value as a second level |
| 3 | REFUSED | must restate the claim over the gradient | supplied a gradient claim |
| 4 | REFUSED | a sweep must carry a predicate | supplied a predicate |
| 5 | **ADMITTED** | — | — |

Every amendment is the thing the gate asked for in the sentence it refused
with. A person reading the same refusals would do the same, which is the
point — none of these is a trick.

The load-bearing one is the last:

    lambda readings: (True, "gradient observed", {})

`Sweep` required `callable(gradient_predicate)` and nothing else. **The gate
checked that a predicate exists. It did not check that the predicate can
return anything but SUPPORTED.**

`null-harness` has a name for a test that always returns the same answer,
and this module applies that grading to other people's gates in
`gate_null_test.py` while not applying it to the predicate it accepts.

## 15 — ACL_015, what that bought, and where the repair goes

Before the repair, the full chain ran: sweep admitted → `run_sweep`
evaluates every level → constant predicate returns SUPPORTED → the gradient
claim **replaces** the point claim → loop terminates `converged`.

That is worse than the failure this module was built against. The delivered
framework's walk at least leaves its claims marked `failed`. This one
produced a parameter walk with a session-stamped audit trail and a supported
claim at the end of it.

**The repair is in `Loop.run_sweep`, not in `Sweep.__init__`,** and that is
forced rather than chosen. The constructor sees a callable and no readings,
so it cannot know whether the callable discriminates. Admission is the wrong
stage, and leaving the check there is what let the walk through. Measured,
after:

| predicate | sweep verdict | loop stop |
|-----------|---------------|-----------|
| constant | UNDECIDED | `stood_on_refutation` |
| real gradient | SUPPORTED | `converged` |

Those two rows are the null-harness pair for the check itself. A check that
refused every predicate would show UNDECIDED on both and be useless.

## 16 — ACL_016, the rule had to be tightened, by measurement

The first version required that **some** counterfactual move. That let
through every symmetric function of the outcomes:

| predicate | discriminates | differs on |
|-----------|---------------|------------|
| constant True / False | no | — |
| counts readings | no | — |
| variation exists | no | flattened |
| `sum > 1.8` | no | flattened |
| `max > 0.8` | no | flattened |
| reads first only | yes | permuted |
| monotone in level | yes | permuted |

(The table shows the rule as it now stands. Under `any(differs)` the three
`flattened`-only rows passed.)

Those read the outcome *values* and not their assignment to levels — and "a
predicate that looks like it reads data" is exactly what an adversary writes
next. The rule is now that the **permuted** counterfactual must move, which
is definitional: a gradient claim is a claim about which outcome goes with
which level.

**The cost is real and is stated.** "The outcome varies at all across these
levels" is a genuine if weak claim and is now refused. That is right for a
*gradient* claim and it is a narrowing, so the two failure cases are
reported apart — a symmetric predicate is told it is symmetric, a constant
one is told it reads nothing, and they need different fixes.

Still open: the counterfactual set is two, chosen because two failure shapes
were in front of us, and nothing derives it. The permutation used is a
reversal, which is one permutation of several.

An error corrected in the making: the first draft of this section asserted
that a predicate reading only the first reading would slip through. It does
not — reversal changes the first element. The claim was replaced by the
measurement, which found a different and sharper gap.

## 17 — ACL_017, the paraphrase, and what is still not closed

    REFUSED   "because the claim failed, lower it"
    ADMITTED  "the predicate's observed value sits outside the stated band…"

One amendment. The outcome screen is a keyword list and no keyword list is a
barrier to anything that wants past it. Same shape as `uninstrumented`'s
scanner (`UNI_009`) and `declared-frame` (`DF_010`): triggers written in the
vocabulary of the failing document catch the phrasings they list and no
others.

It does not follow that the screen is useless. A responder writing "because
the claim failed" is stopped, and the phrase it must avoid is the phrase
that names the reasoning — so the screen converts a casual retune into one
that has to be described in mechanism language, and that description then
sits in the log beside the proposal.

**The pattern worth taking forward:** the two guards that hold against
paraphrase are the two that ask for a number or a computation —
`ResolutionEdit`'s have/need pair, and the discrimination check. A guard
that asks for prose can be satisfied with prose.

**And what is still not closed.** The adversary is written here. Its
strategies come from refusal text and its knowledge from `inspect.signature`
— the strongest constraint available from inside — and that is not the same
as a responder written by somebody else, because what it does not try is
bounded by what occurred to the person who wrote it. `ACL_009` is narrower
than it was and it is not closed.
