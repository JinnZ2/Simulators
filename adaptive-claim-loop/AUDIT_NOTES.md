# AUDIT_NOTES — adaptive-claim-loop

Two things in this folder. [`adaptive_loop.py`](adaptive_loop.py) is the
module; [`delivered/`](delivered) holds an uploaded adaptive simulation
framework and its two provenance logs, verbatim and unmodified, and
[`replay_delivered.py`](replay_delivered.py) reads them.

    python3 adaptive_loop.py --selftest
    python3 adaptive_loop.py
    python3 replay_delivered.py

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
| `adaptive_loop.py` | added — the module, selftest 39/39 |
| `replay_delivered.py` | added — the delivered moves through the gate |
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
