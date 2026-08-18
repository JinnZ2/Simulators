#!/usr/bin/env python3
"""
ADAPTIVE CLAIM LOOP
Same architecture as an adaptive simulation framework -- provenance log,
claim system, an agent that reads results and proposes a change, a loop
that iterates -- with one move removed. Stdlib only, deterministic.

THE MOVE THAT IS REMOVED. In the ordinary shape of this architecture, a
failed claim hands the agent a parameter dial and the agent turns it until
the claim passes. That is a search over the parameter space for a setting
under which the prediction is true, reported as a chain of reasoning. It
cannot fail, it learns nothing about the system, and the provenance log
that records it reads as diligence.

This module has no vocabulary for it. A failure admits exactly five
responses, each with its own admission requirements:

  CLAIM_UPDATE     the claim was wrong. Restate it. Requires a new break
                   condition that is not the old one, and the epicycle
                   guard: the restatement must predict something beyond
                   rescuing its parent.

  MECHANISM_EDIT   the sim is missing a process. Requires a basis that is
                   independent of this run, and a prediction registered
                   BEFORE the edited sim is run.

  INSTRUMENT_EDIT  the number is being read in the wrong place -- sampling
                   phase, statistic, integration step. Requires the artifact
                   removed and a quantity that is unchanged by the change.
                   Takes no prediction: it is not a claim about the world.

  SWEEP            a parameter is varied across levels declared before the
                   run, and the claim is restated as a statement about the
                   gradient. The levels must bracket the current value, or
                   the responder must say why a one-sided sweep is the
                   right instrument here.

  STAND            the failure is the result. Nothing is proposed. Logged.

A bare parameter move aimed at the failing claim is not on that list and
cannot be constructed. The refusal is in the type system, not in a warning.

WHAT THIS MODULE DOES NOT SUPPLY. A good agent. `ConservativeResponder` is
a rule-based stub that exists so the loop runs and so the selftest can
exercise every refusal branch. The claim here is about the admission rules,
which are the same whether the responder is a person, a script, or a model.

Usage:
  adaptive_loop.py                     run the demo loop
  adaptive_loop.py --scenario drift    one scenario
  adaptive_loop.py --log FILE          write provenance
  adaptive_loop.py --selftest
"""

import hashlib
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# outcome-reason screening
#
# Every free-text field a responder supplies is screened, not just the one
# labelled "reason". The fields that ask for justification -- basis,
# prediction, rationale -- are where outcome reasoning goes when it is going
# anywhere, so screening `reason` alone screens the field least likely to
# carry it.
# ---------------------------------------------------------------------------

FORBIDDEN_REASONS = (
    "so the claim passes",
    "so that the claim passes",
    "to make the claim pass",
    "to make it pass",
    "so it passes",
    "because the claim failed",
    "claim failed",
    "to fix the failure",
    "to get a pass",
    "until it passes",
    "match the prediction",
    "to match the expected",
    "recover the expected result",
)


class Refused(Exception):
    """A proposal that does not meet its admission requirements."""


class EpicycleRejected(Refused):
    """A restatement that only rescues its parent."""


def screen(**fields):
    """Refuse any proposal whose justification is the outcome it produces."""
    low = " ".join(str(v) for v in fields.values() if v is not None).lower()
    for bad in FORBIDDEN_REASONS:
        if bad in low:
            raise Refused(
                "edit justified by outcome, not by mechanism -> %r\n"
                "The protocol updates the claim; it does not retune the sim."
                % bad)


# ---------------------------------------------------------------------------
# verdicts
#
# Three, not two. UNDECIDED is reachable and is what an empty evaluation set
# returns -- a predicate computed over nothing is not a pass. The delivered
# shape of this architecture returns passed/failed only, and routes a
# predicate that raised into `failed`, where it is indistinguishable from a
# prediction that was tested and broke.
# ---------------------------------------------------------------------------

SUPPORTED = "SUPPORTED"
REFUTED = "REFUTED"
UNDECIDED = "UNDECIDED"
NOT_EVALUATED = "NOT_EVALUATED"
VERDICTS = (SUPPORTED, REFUTED, UNDECIDED, NOT_EVALUATED)


class Undecidable(Exception):
    """Raised by a predicate that cannot be computed on these outcomes."""


def require(cond, why):
    """Use inside a predicate for a precondition the outcomes must meet."""
    if not cond:
        raise Undecidable(why)


class Claim(object):
    """
    A falsifiable claim. `refuted_if` is stated in words and is what a
    later restatement has to differ from -- the predicate is how the loop
    evaluates it, the sentence is what a reader argues with.
    """

    def __init__(self, cid, statement, predicate, refuted_if,
                 parent=None, exposed=None):
        self.cid = cid
        self.statement = statement
        self.predicate = predicate
        self.refuted_if = refuted_if
        self.parent = parent
        self.exposed = exposed
        self.history = []

    def evaluate(self, outcomes):
        """-> (verdict, note, detail). Never raises."""
        try:
            ok, note, detail = self.predicate(outcomes)
        except Undecidable as e:
            v = (UNDECIDED, "precondition not met: %s" % e, {})
        except Exception as e:                      # noqa: BLE001
            # A predicate that raised is a broken instrument, not a refuted
            # claim. Keeping it apart is the whole reason UNDECIDED exists.
            v = (UNDECIDED, "predicate error: %s: %s"
                 % (type(e).__name__, e), {})
        else:
            v = (SUPPORTED if ok else REFUTED, note, detail)
        self.history.append(v)
        return v


# ---------------------------------------------------------------------------
# responses
#
# Five constructors. Each raises Refused rather than returning a flag, so an
# inadmissible proposal cannot reach the log at all.
# ---------------------------------------------------------------------------

class Response(object):
    kind = None

    def record(self):
        d = {k: v for k, v in self.__dict__.items() if not callable(v)}
        d["kind"] = self.kind
        return d


class ClaimUpdate(Response):
    """
    The default response. The claim was wrong; restate it.

    Epicycle guard, from equivalence-field/claim_lineage.py: the restatement
    is admitted only if it is independently falsifiable AND predicts beyond
    rescuing the parent. A child that says only "the parent holds except
    here" adds a term and no reach.
    """
    kind = "CLAIM_UPDATE"

    def __init__(self, claim_id, new_statement, new_refuted_if, exposed,
                 independently_falsifiable, predicts_beyond_parent,
                 old_refuted_if, rationale=""):
        screen(new_statement=new_statement, new_refuted_if=new_refuted_if,
               exposed=exposed, rationale=rationale)
        if not str(new_refuted_if).strip():
            raise Refused("a restatement needs a break condition")
        if _same(new_refuted_if, old_refuted_if):
            raise Refused(
                "the new break condition is the old one; the claim did not "
                "move, only its wording")
        if not (independently_falsifiable and predicts_beyond_parent):
            raise EpicycleRejected(
                "%r: independently_falsifiable=%s predicts_beyond_parent=%s "
                "-> epicycle, not admitted"
                % (exposed, independently_falsifiable, predicts_beyond_parent))
        self.claim_id = claim_id
        self.new_statement = new_statement
        self.new_refuted_if = new_refuted_if
        self.exposed = exposed
        self.rationale = rationale


class MechanismEdit(Response):
    """
    The sim is missing a process. `basis` must be independent of this run;
    `prediction` is registered before the edited sim is run and is settled
    afterward with an explicit bool.
    """
    kind = "MECHANISM_EDIT"

    def __init__(self, mechanism, basis, prediction, affects, rationale=""):
        screen(mechanism=mechanism, basis=basis, prediction=prediction,
               rationale=rationale)
        for name, val in (("mechanism", mechanism), ("basis", basis),
                          ("prediction", prediction)):
            if not str(val).strip():
                raise Refused("a mechanism edit needs a %s" % name)
        if not affects:
            raise Refused("a mechanism edit must name the claims it could move")
        self.mechanism = mechanism
        self.basis = basis
        self.prediction = prediction
        self.affects = list(affects)
        self.rationale = rationale
        self.held = None

    def settle(self, observed, held):
        if not isinstance(held, bool):
            raise Refused(
                "settle(observed, held) requires held=True|False. A "
                "registered prediction that is never adjudicated is not a "
                "registered prediction.")
        self.held = held
        self.observed = observed
        return self


class InstrumentEdit(Response):
    """
    A change to where a number is read. Names the artifact removed and a
    quantity unchanged by the change. Takes no prediction: it is not a
    claim about the world. If it moves a verdict, that is a finding about
    the old readout.
    """
    kind = "INSTRUMENT_EDIT"

    def __init__(self, readout, artifact, unchanged, rationale=""):
        screen(readout=readout, artifact=artifact, unchanged=unchanged,
               rationale=rationale)
        for name, val in (("readout", readout), ("artifact", artifact),
                          ("unchanged", unchanged)):
            if not str(val).strip():
                raise Refused("an instrument edit needs a %s" % name)
        self.readout = readout
        self.artifact = artifact
        self.unchanged = unchanged
        self.rationale = rationale


class Sweep(Response):
    """
    The one response that moves a parameter, and the guards are what keep it
    from being the removed move under another name.

      levels declared before the run, at least two
      the claim restated as a statement about the GRADIENT, not the endpoint
      the levels bracket the current value, or `one_sided_because` says why

    A one-sided sweep whose levels all run toward the setting that would
    make the claim pass is the parameter walk. It is admissible only with
    the reason stated, so it is legible in the log as a choice.
    """
    kind = "SWEEP"

    def __init__(self, parameter, current, levels, gradient_claim,
                 gradient_predicate, one_sided_because=None, rationale=""):
        screen(parameter=parameter, gradient_claim=gradient_claim,
               one_sided_because=one_sided_because, rationale=rationale)
        levels = list(levels)
        if len(levels) < 2:
            raise Refused(
                "a sweep needs at least two levels; one level is a parameter "
                "move with a sweep's name on it")
        if len(set(levels)) != len(levels):
            raise Refused("sweep levels must be distinct")
        if not str(gradient_claim).strip():
            raise Refused(
                "a sweep must restate the claim over the gradient. A sweep "
                "read at its endpoint is the endpoint, not a gradient.")
        if not callable(gradient_predicate):
            raise Refused(
                "a sweep must carry a predicate over the readings. A gradient "
                "claim stated in prose with nothing that can evaluate it is a "
                "design that cannot fail its own falsifier.")
        brackets = min(levels) <= current <= max(levels)
        if not brackets and not str(one_sided_because or "").strip():
            raise Refused(
                "levels %s do not bracket the current value %s. A one-sided "
                "sweep is admissible, with the reason stated."
                % (levels, current))
        self.parameter = parameter
        self.current = current
        self.levels = levels
        self.gradient_claim = gradient_claim
        self.gradient_predicate = gradient_predicate
        self.brackets_current = brackets
        self.one_sided_because = one_sided_because
        self.rationale = rationale


class Stand(Response):
    """
    The failure is the result. The architecture this module copies has no
    way to say this: its loop terminates on success or on budget, and a
    refutation is a thing to be worked around.
    """
    kind = "STAND"

    def __init__(self, claim_id, note):
        screen(note=note)
        if not str(note).strip():
            raise Refused("standing on a refutation is a decision; state it")
        self.claim_id = claim_id
        self.note = note


def _settled(verdict, note, detail):
    """Freeze a sweep verdict as the claim's predicate for later iterations."""
    def p(_outcomes, _v=verdict, _n=note, _d=detail):
        if _v == UNDECIDED:
            raise Undecidable(_n)
        return _v == SUPPORTED, "swept: " + _n, _d
    return p


def _same(a, b):
    return " ".join(str(a).lower().split()) == " ".join(str(b).lower().split())


# ---------------------------------------------------------------------------
# provenance
# ---------------------------------------------------------------------------

class Provenance(object):
    """
    Append-only JSONL with a session boundary.

    The boundary is not decoration. An append-mode log with no session field
    cannot distinguish iteration N of one loop from iteration 0 of a later
    invocation, and a reader following the parameter column across that seam
    reads a search that never happened.
    """

    def __init__(self, path=None, session_tag="s"):
        self.path = path
        self.rows = []
        self.session = session_tag
        self.ordinal = 0
        self._emit({"kind": "SESSION_OPEN", "session": self.session})

    def _emit(self, row):
        row = dict(row)
        row.setdefault("session", self.session)
        self.rows.append(row)
        if self.path:
            with open(self.path, "a") as f:
                f.write(json.dumps(row, sort_keys=True, default=str) + "\n")
        return row

    def run(self, model, params, seed, outcomes, verdicts):
        self.ordinal += 1
        return self._emit({
            "kind": "RUN",
            "ordinal": self.ordinal,
            "model": model,
            "params": dict(params),
            "seed": seed,
            "outcomes": outcomes,
            "verdicts": verdicts,
            "params_digest": digest(params),
        })

    def response(self, claim_id, resp):
        return self._emit({
            "kind": "RESPONSE",
            "ordinal": self.ordinal,
            "claim_id": claim_id,
            "response": resp.record(),
        })

    def refusal(self, claim_id, proposed_kind, why):
        """A refused proposal is logged. The trail is what was tried."""
        return self._emit({
            "kind": "REFUSED",
            "ordinal": self.ordinal,
            "claim_id": claim_id,
            "proposed": proposed_kind,
            "why": str(why).splitlines()[0],
        })

    def close(self, reason):
        return self._emit({"kind": "SESSION_CLOSE", "reason": reason,
                           "runs": self.ordinal})


def digest(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:12]


# ---------------------------------------------------------------------------
# the loop
# ---------------------------------------------------------------------------

CONVERGED = "converged"
BUDGET = "budget_exhausted"
STOOD = "stood_on_refutation"
NOTHING_ADMITTED = "no_admissible_response"


class Loop(object):
    """
    Runs a model, evaluates claims, asks a responder what to do about each
    refutation, and admits only what passes the gates.

    Termination is one of four named states. The architecture this copies
    prints "Final iteration or all claims passed" on a branch reached in
    both cases, so its log says a loop converged when it ran out of budget
    with every claim still failing.
    """

    def __init__(self, model, claims, responder, prov=None):
        self.model = model
        self.claims = list(claims)
        self.responder = responder
        self.prov = prov or Provenance()

    def run(self, params, iterations=4, seed=1):
        params = dict(params)
        history = []
        stop = BUDGET
        for it in range(iterations):
            outcomes = self.model.run(params, seed + it)
            verdicts = {}
            for c in self.claims:
                v, note, detail = c.evaluate(outcomes)
                verdicts[c.cid] = {"verdict": v, "note": note}
            self.prov.run(self.model.name, params, seed + it,
                          outcomes, verdicts)
            history.append({"iteration": it, "params": dict(params),
                            "outcomes": outcomes, "verdicts": verdicts})

            # UNDECIDED is answerable too, and the answer is different in
            # kind: a refutation asks what the claim got wrong, an undecided
            # asks what the instrument could not resolve. Collecting only
            # refutations leaves the second silently unaddressed.
            open_ = [c for c in self.claims
                     if verdicts[c.cid]["verdict"] in (REFUTED, UNDECIDED)]
            if not open_:
                stop = CONVERGED
                break

            admitted = []
            for c in open_:
                try:
                    resp = self.responder.respond(c, outcomes, params,
                                                  self.model,
                                                  verdicts[c.cid]["verdict"])
                except Refused as e:
                    self.prov.refusal(c.cid, getattr(e, "kind", "?"), e)
                    continue
                if resp is None:
                    continue
                self.prov.response(c.cid, resp)
                if resp.kind == "SWEEP":
                    self.run_sweep(c, resp, params, seed + it)
                admitted.append((c, resp))

            if not admitted:
                stop = NOTHING_ADMITTED
                break
            if all(r.kind == "STAND" for _, r in admitted):
                stop = STOOD
                break
            params = self.apply(params, admitted)

        self.prov.close(stop)
        return {"stop": stop, "iterations": len(history), "history": history,
                "final_params": params}

    def run_sweep(self, claim, resp, params, seed):
        """
        A sweep is run, not walked. The model is evaluated at every declared
        level and the gradient predicate reads the whole set, so the claim
        that replaces the point claim is a statement the readings can refute.
        Walking one level per iteration and re-reading the POINT claim is the
        removed move with extra steps.
        """
        readings = []
        for lvl in resp.levels:
            q = dict(params)
            q[resp.parameter] = lvl
            readings.append((lvl, self.model.run(q, seed)))
        try:
            ok, note, detail = resp.gradient_predicate(readings)
            verdict = SUPPORTED if ok else REFUTED
        except Undecidable as e:
            verdict, note, detail = UNDECIDED, str(e), {}
        except Exception as e:                       # noqa: BLE001
            verdict, note, detail = (UNDECIDED, "predicate error: %s: %s"
                                     % (type(e).__name__, e), {})
        self.prov._emit({
            "kind": "SWEEP_RESULT", "ordinal": self.prov.ordinal,
            "claim_id": claim.cid, "parameter": resp.parameter,
            "levels": resp.levels, "verdict": verdict, "note": note,
            "detail": detail,
            "readings": [{"level": l, "outcomes": o} for l, o in readings],
        })
        # the gradient claim replaces the point claim it was raised against
        claim.statement = resp.gradient_claim
        claim.refuted_if = "the gradient predicate fails over the declared levels"
        claim.predicate = _settled(verdict, note, detail)
        return verdict

    def apply(self, params, admitted):
        """
        Only a SWEEP touches params, and it sets the parameter to each
        declared level in turn -- it does not move it toward anything. A
        CLAIM_UPDATE rewrites the claim in place; the other kinds change
        nothing here and are carried out by a person.
        """
        out = dict(params)
        for claim, resp in admitted:
            if resp.kind == "SWEEP":
                # the sweep already ran at every level; params do not move.
                pass
            elif resp.kind == "INSTRUMENT_EDIT":
                need = getattr(self.responder, "raise_to", None)
                if need and "replicates" in getattr(self.model,
                                                    "parameters", ()):
                    out["replicates"] = need
            elif resp.kind == "CLAIM_UPDATE":
                claim.statement = resp.new_statement
                claim.refuted_if = resp.new_refuted_if
                claim.parent = claim.cid
                claim.exposed = resp.exposed
        return out


# ---------------------------------------------------------------------------
# demo models -- stdlib, seeded, deterministic
# ---------------------------------------------------------------------------

class DriftFixation(object):
    """
    Two variants in a finite population under neutral-to-weak selection.
    A Moran-style birth-death step on integers, no libraries. `advantage`
    is the per-step edge of variant A; `n` is the population.
    """
    name = "drift"
    parameters = ("n", "advantage", "replicates", "max_steps")

    def run(self, params, seed):
        n = int(params.get("n", 40))
        adv = float(params.get("advantage", 0.0))
        reps = int(params.get("replicates", 200))
        cap = int(params.get("max_steps", 20000))
        rng = random.Random(seed)
        fixed_a = 0
        unresolved = 0
        times = []
        for _ in range(reps):
            a = n // 2
            for t in range(cap):
                if a == 0 or a == n:
                    break
                wa = a * (1.0 + adv)
                wb = n - a
                born_a = rng.random() < wa / (wa + wb)
                dies_a = rng.random() < a / float(n)
                a += (1 if born_a else 0) - (1 if dies_a else 0)
                a = max(0, min(n, a))
            if a == n:
                fixed_a += 1
                times.append(t)
            elif a == 0:
                times.append(t)
            else:
                unresolved += 1
        resolved = reps - unresolved
        return {
            "replicates": reps,
            "resolved": resolved,
            "unresolved": unresolved,
            "p_fix_a": (fixed_a / float(resolved)) if resolved else None,
            "mean_time": (sum(times) / float(len(times))) if times else None,
        }


class ThresholdYield(object):
    """
    A deterministic response with a threshold in it. Below `tip` the output
    is linear in load; above it the output collapses. Exists so a claim can
    be refuted for a reason that is structural rather than stochastic.
    """
    name = "threshold"
    parameters = ("load", "tip", "slope")

    def run(self, params, seed):
        load = float(params.get("load", 0.4))
        tip = float(params.get("tip", 0.6))
        slope = float(params.get("slope", 1.0))
        if load < tip:
            y = 1.0 - slope * load
        else:
            y = max(0.0, (1.0 - slope * tip) * (1.0 - 4.0 * (load - tip)))
        return {"load": load, "yield": round(y, 6),
                "linear_prediction": round(1.0 - slope * load, 6)}


MODELS = {m.name: m for m in (DriftFixation(), ThresholdYield())}


# ---------------------------------------------------------------------------
# demo claims
# ---------------------------------------------------------------------------

NEUTRAL_TOL = 0.08


def monotone_in_advantage(readings):
    """
    Gradient predicate for the drift sweep. Reads the whole set of levels:
    p_fix must rise with advantage and the neutral level must sit between
    its neighbours. A predicate that could only look at one level would be
    the point claim again.
    """
    pts = [(lvl, o.get("p_fix_a")) for lvl, o in readings]
    if any(p is None for _, p in pts):
        raise Undecidable("a level produced no resolved replicate")
    pts.sort()
    ps = [p for _, p in pts]
    rising = all(b >= a - 0.02 for a, b in zip(ps, ps[1:]))
    return (rising,
            "p_fix across advantage %s = %s"
            % ([l for l, _ in pts], [round(p, 3) for p in ps]),
            {"levels": [l for l, _ in pts], "p_fix": ps})


def drift_claims():
    def p_fix_matches_neutral(o):
        """
        Carries its own resolution guard. The claim is a statement about a
        proportion measured to +/- TOL, and a run whose standard error is
        wider than TOL cannot decide it in either direction. Without the
        guard the verdict is a coin flip reported as a refutation -- which
        is reasoning-gate G-RES, instrument resolution against the feature
        being resolved, inside a predicate rather than around one.
        """
        n = o.get("resolved") or 0
        require(n, "no replicate resolved; p_fix undefined")
        se = (0.25 / n) ** 0.5
        require(NEUTRAL_TOL >= 2 * se,
                "tolerance %.3f is inside 2 SE (%.3f) at %d resolved "
                "replicates; the run cannot decide this claim"
                % (NEUTRAL_TOL, 2 * se, n))
        p = o["p_fix_a"]
        return (abs(p - 0.5) < NEUTRAL_TOL,
                "p_fix(A) = %.3f +/- %.3f against neutral 0.5" % (p, se),
                {"p_fix_a": p, "se": se})

    def all_resolve(o):
        u = o.get("unresolved")
        require(u is not None, "unresolved not reported")
        return (u == 0, "unresolved = %d of %d" % (u, o["replicates"]),
                {"unresolved": u})

    return [
        Claim("ACL_drift_neutral",
              "With no advantage, A fixes about half the time.",
              p_fix_matches_neutral,
              "p_fix(A) departs from 0.5 by more than 0.08"),
        Claim("ACL_drift_resolves",
              "Every replicate reaches fixation within the step cap.",
              all_resolve,
              "any replicate is still segregating at the cap"),
    ]


def threshold_claims():
    def linear(o):
        d = abs(o["yield"] - o["linear_prediction"])
        return (d < 0.05, "|yield - linear| = %.4f" % d, {"gap": d})

    return [
        Claim("ACL_thresh_linear",
              "Yield falls linearly with load.",
              linear,
              "yield departs from the linear prediction by more than 0.05"),
    ]


CLAIMS = {"drift": drift_claims, "threshold": threshold_claims}


# ---------------------------------------------------------------------------
# a responder -- the stub, not the contribution
# ---------------------------------------------------------------------------

class ConservativeResponder(object):
    """
    Rule-based. Exists so the loop runs and so every refusal branch is
    reachable in the selftest. It is not an agent and makes no claim to be
    one; swap it for a person or a model and the gates are unchanged.

    Its one real policy is the protocol's default: when a claim breaks and
    nothing independent explains it, update the claim.
    """

    def __init__(self, allow_sweep=True):
        self.allow_sweep = allow_sweep
        self.seen = set()

    def respond(self, claim, outcomes, params, model, verdict=REFUTED):
        if verdict == UNDECIDED:
            return self.resolve(claim, outcomes, params)
        if claim.cid in self.seen:
            return Stand(claim.cid,
                         "already restated once; a second restatement on the "
                         "same evidence is fitting, not learning")
        self.seen.add(claim.cid)

        if claim.cid == "ACL_drift_resolves":
            # The break is at the instrument, not in the population: the step
            # cap truncates the tail of the fixation-time distribution, and
            # the claim was written over a quantity the readout cannot see.
            return InstrumentEdit(
                readout="fixation counted only within max_steps",
                artifact="replicates still segregating at the cap are counted "
                         "as neither fixation nor loss",
                unchanged="p_fix among resolved replicates",
                rationale="the cap is a property of the harness, not of the "
                          "population")

        if claim.cid == "ACL_thresh_linear":
            return ClaimUpdate(
                claim_id=claim.cid,
                new_statement="Yield falls linearly with load below a "
                              "threshold, and collapses above it.",
                new_refuted_if="yield is linear across a load range that "
                               "spans the threshold, or the departure has no "
                               "threshold in it",
                old_refuted_if=claim.refuted_if,
                exposed="tip",
                independently_falsifiable=True,
                predicts_beyond_parent=True,
                rationale="the departure is one-sided and grows with load")

        if self.allow_sweep and claim.cid == "ACL_drift_neutral":
            cur = params.get("advantage", 0.0)
            # Levels are centred on the CURRENT value. The first version of
            # this responder used a fixed ladder [-0.05, 0, 0.05], which the
            # bracketing guard refused as soon as the scenario started above
            # 0.05: a ladder that sits entirely below the current setting,
            # proposed against a claim that fails because the setting is
            # high, is the parameter walk. The guard caught it here before
            # any finding rested on it.
            return Sweep(
                parameter="advantage",
                current=cur,
                levels=[round(cur - 0.06, 4), cur, round(cur + 0.06, 4)],
                gradient_claim="p_fix(A) rises monotonically with advantage "
                               "and brackets 0.5 at advantage 0",
                gradient_predicate=monotone_in_advantage,
                rationale="the claim is a statement about one point on a "
                          "gradient; read the gradient")

        return Stand(claim.cid, "no admissible response identified")

    def resolve(self, claim, outcomes, params):
        """
        The one legitimate reason to change a number in response to a result:
        the instrument could not resolve the question. It is admissible
        because the resolution gap is COMPUTABLE -- standard error against
        stated tolerance -- so the justification is a number and not the
        verdict. Raising replicates until a verdict flips is the removed
        move; raising them until the error bar is narrower than the
        tolerance the claim was written at is closing a stated gap.
        """
        key = claim.cid + ":resolution"
        if key in self.seen:
            return Stand(claim.cid,
                         "still undecidable after one resolution pass")
        self.seen.add(key)
        n = outcomes.get("resolved") or outcomes.get("replicates") or 0
        need = int(0.25 * (2.0 / NEUTRAL_TOL) ** 2) + 1
        if not n or n >= need:
            return Stand(claim.cid,
                         "undecidable for a reason the replicate count does "
                         "not fix")
        self.raise_to = need
        return InstrumentEdit(
            readout="p_fix estimated from %d replicates" % n,
            artifact="a standard error wider than the tolerance the claim is "
                     "written at, which makes the verdict a draw from noise",
            unchanged="the expectation of p_fix, which does not depend on "
                      "how many replicates estimate it",
            rationale="resolution gap is computable: %d replicates are "
                      "needed for 2 SE to fall inside the tolerance" % need)


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------

def report(result, prov):
    print("stop condition : %s" % result["stop"])
    print("iterations     : %d" % result["iterations"])
    print()
    print("  it  %-24s %-12s %s" % ("claim", "verdict", "note"))
    print("  " + "-" * 74)
    for h in result["history"]:
        for cid, v in sorted(h["verdicts"].items()):
            print("  %2d  %-24s %-12s %s"
                  % (h["iteration"], cid[:24], v["verdict"], v["note"][:30]))
    resp = [r for r in prov.rows if r["kind"] == "RESPONSE"]
    ref = [r for r in prov.rows if r["kind"] == "REFUSED"]
    print()
    print("  responses admitted : %d" % len(resp))
    for r in resp:
        print("    %-16s %s" % (r["response"]["kind"], r["claim_id"]))
    print("  responses refused  : %d" % len(ref))
    for r in ref:
        print("    %-16s %s" % (r["claim_id"], r["why"][:44]))
    print()
    print("A refutation is a result. The loop stops on `converged`,")
    print("`budget_exhausted`, `stood_on_refutation` or")
    print("`no_admissible_response` -- never on one branch that means two.")


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------

def selftest():
    ok, bad = [], []

    def is_(cond, name):
        (ok if cond else bad).append(name)

    def refuses(fn, name, exc=Refused):
        try:
            fn()
        except exc:
            ok.append(name)
        except Exception as e:                       # noqa: BLE001
            bad.append("%s (raised %s)" % (name, type(e).__name__))
        else:
            bad.append(name)

    # --- the removed move has no constructor
    is_(not any(getattr(c, "kind", "") == "PARAMETER_MOVE"
                for c in (ClaimUpdate, MechanismEdit, InstrumentEdit,
                          Sweep, Stand)),
        "no PARAMETER_MOVE response kind exists")

    # --- outcome-reason screening, on every free-text field
    refuses(lambda: MechanismEdit("m", "b", "p", ["c"],
                                  rationale="so the claim passes"),
            "screen catches rationale")
    refuses(lambda: MechanismEdit("m", "because the claim failed", "p", ["c"]),
            "screen catches basis")
    refuses(lambda: MechanismEdit("m", "b", "to make it pass", ["c"]),
            "screen catches prediction")
    is_(MechanismEdit("added a threshold", "reported in the source system",
                      "yield collapses above load 0.6", ["c"]).kind
        == "MECHANISM_EDIT", "clean mechanism edit admitted")

    # --- mechanism edit settling
    m = MechanismEdit("m", "b", "p", ["c"])
    refuses(lambda: m.settle("observed", None), "settle requires a bool")
    is_(m.settle("observed", False).held is False, "settle records a false")

    # --- epicycle guard
    refuses(lambda: ClaimUpdate("c", "s", "new break", "v",
                                independently_falsifiable=False,
                                predicts_beyond_parent=True,
                                old_refuted_if="old break"),
            "epicycle guard on measurability", EpicycleRejected)
    refuses(lambda: ClaimUpdate("c", "s", "new break", "v",
                                independently_falsifiable=True,
                                predicts_beyond_parent=False,
                                old_refuted_if="old break"),
            "epicycle guard on reach", EpicycleRejected)
    refuses(lambda: ClaimUpdate("c", "s", "Old  Break", "v",
                                independently_falsifiable=True,
                                predicts_beyond_parent=True,
                                old_refuted_if="old break"),
            "restatement with the same break condition refused")
    is_(ClaimUpdate("c", "s", "a different break", "v",
                    independently_falsifiable=True,
                    predicts_beyond_parent=True,
                    old_refuted_if="old break").kind == "CLAIM_UPDATE",
        "clean claim update admitted")

    # --- sweep guards
    gp = lambda readings: (True, "", {})            # noqa: E731
    refuses(lambda: Sweep("p", 0.0, [0.1], "gradient rises", gp),
            "one level refused")
    refuses(lambda: Sweep("p", 0.0, [0.1, 0.1], "gradient rises", gp),
            "duplicate levels refused")
    refuses(lambda: Sweep("p", 0.0, [0.1, 0.2], "", gp),
            "sweep without a gradient claim refused")
    refuses(lambda: Sweep("p", 0.0, [-0.1, 0.1], "gradient rises", None),
            "sweep without a gradient predicate refused")
    refuses(lambda: Sweep("p", 0.0, [0.1, 0.2], "gradient rises", gp),
            "one-sided sweep refused without a reason")
    s = Sweep("p", 0.0, [0.1, 0.2], "gradient rises", gp,
              one_sided_because="the parameter is non-negative")
    is_(s.brackets_current is False, "one-sided sweep flagged as one-sided")
    is_(Sweep("p", 0.0, [-0.1, 0.1], "g", gp).brackets_current is True,
        "bracketing sweep flagged")
    is_("gradient_predicate" not in s.record(),
        "the callable is not serialised into the log")

    # --- instrument edit takes no prediction
    is_(not hasattr(InstrumentEdit("r", "a", "u"), "prediction"),
        "instrument edit carries no prediction")

    # --- stand
    refuses(lambda: Stand("c", ""), "standing needs a stated reason")
    is_(Stand("c", "the refutation is the result").kind == "STAND",
        "stand admitted")

    # --- verdicts: four, and an unevaluable predicate is not a refutation
    def raiser(o):
        raise KeyError("size_distribution")

    c = Claim("x", "s", raiser, "r")
    is_(c.evaluate({})[0] == UNDECIDED, "predicate error is UNDECIDED")

    def empty(o):
        require(o.get("n"), "nothing to average over")
        return True, "", {}

    is_(Claim("y", "s", empty, "r").evaluate({})[0] == UNDECIDED,
        "unmet precondition is UNDECIDED")
    is_(Claim("z", "s", lambda o: (False, "", {}), "r").evaluate({})[0]
        == REFUTED, "a false predicate is REFUTED")
    is_(NOT_EVALUATED in VERDICTS, "not-evaluated is a distinct verdict")

    # --- provenance carries a session boundary
    p = Provenance(session_tag="t")
    p.run("m", {"a": 1}, 1, {}, {})
    p.close("done")
    kinds = [r["kind"] for r in p.rows]
    is_(kinds[0] == "SESSION_OPEN" and kinds[-1] == "SESSION_CLOSE",
        "session opens and closes in the log")
    is_(all(r.get("session") == "t" for r in p.rows),
        "every row carries its session")
    is_(p.rows[1]["ordinal"] == 1, "runs are ordinal within the session")

    # --- refusals are logged, not swallowed
    p2 = Provenance()
    p2.refusal("c", "SWEEP", Refused("levels do not bracket"))
    is_(p2.rows[-1]["kind"] == "REFUSED", "a refused proposal is logged")

    # --- models are deterministic under seed
    d = DriftFixation()
    is_(d.run({"replicates": 20, "n": 20}, 5)
        == d.run({"replicates": 20, "n": 20}, 5), "drift is seed-determined")
    t = ThresholdYield()
    is_(t.run({"load": 0.8}, 0)["yield"] < t.run({"load": 0.5}, 0)["yield"],
        "threshold model collapses above the tip")

    # --- a sweep is run at every level, not walked one per iteration
    seen_levels = []

    class _Rec(object):
        name = "rec"
        parameters = ("x",)

        def run(self, params, seed):
            seen_levels.append(params.get("x"))
            return {"x": params.get("x")}

    def _grad(readings):
        return (len(readings) == 3, "%d readings" % len(readings), {})

    c = Claim("s", "point claim", lambda o: (False, "point", {}), "r")

    class _R(object):
        def respond(self, claim, o, p, m, verdict=REFUTED):
            return Sweep("x", 0.0, [-1.0, 0.0, 1.0], "gradient rises", _grad)

    lp = Loop(_Rec(), [c], _R(), prov=Provenance())
    lp.run({"x": 0.0}, iterations=1, seed=0)
    # the baseline run comes first, then the three declared levels in order
    is_(seen_levels == [0.0, -1.0, 0.0, 1.0],
        "sweep evaluated at every declared level in one iteration")
    sr = [r for r in lp.prov.rows if r["kind"] == "SWEEP_RESULT"]
    is_(len(sr) == 1 and sr[0]["verdict"] == SUPPORTED,
        "the gradient predicate produced the verdict, not the point claim")
    is_(c.statement == "gradient rises",
        "the gradient claim replaced the point claim it was raised against")

    # --- an UNDECIDED claim reaches the responder
    reached = []

    class _R2(object):
        def respond(self, claim, o, p, m, verdict=REFUTED):
            reached.append(verdict)
            return Stand(claim.cid, "noted")

    und = Claim("u", "s", lambda o: (_ for _ in ()).throw(
        Undecidable("cannot compute")), "r")
    Loop(ThresholdYield(), [und], _R2(), prov=Provenance()).run(
        {"load": 0.5}, iterations=1, seed=0)
    is_(reached == [UNDECIDED], "an undecided claim is routed to the responder")

    # --- the resolution guard on the demo claim
    dc = drift_claims()[0]
    thin = DriftFixation().run({"n": 30, "replicates": 60, "max_steps": 4000}, 3)
    thick = DriftFixation().run({"n": 30, "replicates": 400, "max_steps": 4000}, 3)
    is_(dc.evaluate(thin)[0] == UNDECIDED,
        "claim is undecidable when 2 SE exceeds its tolerance")
    is_(dc.evaluate(thick)[0] in (SUPPORTED, REFUTED),
        "same claim is decidable once the error bar fits inside the tolerance")

    # --- termination states are distinct
    is_(len({CONVERGED, BUDGET, STOOD, NOTHING_ADMITTED}) == 4,
        "four distinct termination states")

    for n in ok:
        print("PASS %s" % n)
    for n in bad:
        print("FAIL %s" % n)
    print()
    print("%d/%d" % (len(ok), len(ok) + len(bad)))
    return 0 if not bad else 1


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

SCENARIOS = {
    # name            model        claims             params
    "drift": ("drift", drift_claims,
              {"n": 30, "advantage": 0.0, "replicates": 120,
               "max_steps": 4000}),
    "drift-selected": ("drift", drift_claims,
                       {"n": 30, "advantage": 0.06, "replicates": 400,
                        "max_steps": 4000}),
    "threshold": ("threshold", threshold_claims,
                  {"load": 0.8, "tip": 0.6, "slope": 1.0}),
}


def main(argv):
    if "--selftest" in argv:
        return selftest()
    path = None
    if "--log" in argv:
        path = argv[argv.index("--log") + 1]
    names = sorted(SCENARIOS)
    if "--scenario" in argv:
        want = argv[argv.index("--scenario") + 1]
        if want not in SCENARIOS:
            print("unknown scenario %r; have %s"
                  % (want, ", ".join(names)), file=sys.stderr)
            return 1
        names = [want]
    for i, name in enumerate(names):
        model_name, claim_fn, params = SCENARIOS[name]
        if i:
            print()
        print("=" * 78)
        print("SCENARIO  %s   (model: %s)" % (name, model_name))
        print("=" * 78)
        prov = Provenance(path=path, session_tag=name)
        loop = Loop(MODELS[model_name], claim_fn(), ConservativeResponder(),
                    prov=prov)
        res = loop.run(params, iterations=4, seed=11)
        report(res, prov)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
