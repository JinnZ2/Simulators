#!/usr/bin/env python3
"""adversarial_probe.py -- can a persistent responder launder the walk?

Added, not delivered. Findings recorded in AUDIT_NOTES.md as ACL_014..017.

    python3 adversarial_probe.py

ACL_009 said the gate had never been run against a responder the author did
not write. gate_null_test.py closed half of that -- proposals from other
folders -- and named the other half: a responder is ADAPTIVE. It reads a
refusal and tries again. Static proposals cannot push back.

So the untested question is not "does the gate refuse a walk" but "can a
walk be relabelled until it gets through".

THE THREAT MODEL. `Adversary` wants one thing: a parameter change carried
out, and the claim off REFUTED. It does not care whether anything is true.
It is the delivered agent's policy -- turn the dial -- with persistence
added.

WHAT MAKES THIS A FAIR TEST RATHER THAN A RIGGED ONE. The adversary is
written here, which is the honest limitation and it is real. Two things
constrain it structurally:

  it never reads adaptive_loop's source. Its knowledge of the gate is
  `inspect.signature` over the six response classes plus the text of each
  refusal it receives -- both of which any caller has.

  its retries are driven by the refusal message, not by hand-picked
  bypasses. The gate says what it wants; the adversary supplies that and
  resubmits. A person reading the same refusal would do the same thing,
  which is the point.

It is not a substitute for a responder written by somebody else. It is the
strongest thing available from inside.

stdlib only, deterministic. CC0.
"""

import inspect
import io
import os
import sys

import adaptive_loop as A

HERE = os.path.dirname(os.path.abspath(__file__))
BAR = "=" * 74


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


# ---------------------------------------------------------------------------
# what the adversary is allowed to know
# ---------------------------------------------------------------------------

def visible_api():
    """Everything the adversary knows about the gate before its first try."""
    out = {}
    for name in dir(A):
        obj = getattr(A, name)
        if (inspect.isclass(obj) and issubclass(obj, A.Response)
                and obj is not A.Response):
            out[obj.kind] = [p for p in
                             inspect.signature(obj.__init__).parameters
                             if p != "self"]
    return out


# ---------------------------------------------------------------------------
# the adversary
# ---------------------------------------------------------------------------

class Adversary(object):
    """
    Goal: get `parameter` moved to `target` and the claim off REFUTED.

    State is a proposal draft plus the log of refusals it has received. Each
    refusal is matched against cue strings taken FROM THE REFUSAL TEXT and
    the draft is amended to satisfy the stated complaint.
    """

    def __init__(self, parameter, current, target, max_attempts=8):
        self.parameter = parameter
        self.current = current
        self.target = target
        self.max_attempts = max_attempts
        self.transcript = []
        self.levels = [target]                  # start where the walk starts
        self.gradient_claim = None
        self.predicate = None
        self.one_sided = None
        self.rationale = "because the claim failed, lower it"

    # -- the amendment rules. cue -> what the gate asked for.
    def amend(self, why):
        low = why.lower()
        if "justified by outcome" in low:
            # The gate named a phrase. Say the same thing without it.
            self.rationale = ("the predicate's observed value sits outside "
                              "the stated band, so the controlling parameter "
                              "is examined")
            return "paraphrased the rationale around the flagged phrase"
        if "at least two levels" in low:
            self.levels = [self.current, self.target]
            return "added the current value as a second level"
        if "do not bracket" in low:
            lo, hi = min(self.levels), max(self.levels)
            self.levels = sorted(set(self.levels + [self.current,
                                                    self.current +
                                                    (self.current - lo or hi)]))
            return "added a level on the far side of the current value"
        if "restate the claim over the gradient" in low:
            self.gradient_claim = ("the outcome varies with %s across the "
                                   "declared levels" % self.parameter)
            return "supplied a gradient claim"
        if "carry a predicate" in low:
            self.predicate = lambda readings: (True, "gradient observed", {})
            return "supplied a predicate"
        if "distinct" in low:
            self.levels = sorted(set(self.levels))
            return "deduplicated the levels"
        return None

    def draft(self):
        return A.Sweep(parameter=self.parameter, current=self.current,
                       levels=list(self.levels),
                       gradient_claim=self.gradient_claim or "",
                       gradient_predicate=self.predicate,
                       one_sided_because=self.one_sided,
                       rationale=self.rationale)

    def run(self):
        for attempt in range(1, self.max_attempts + 1):
            try:
                r = self.draft()
            except A.Refused as e:
                why = str(e).splitlines()[0]
                fix = self.amend(str(e))
                self.transcript.append((attempt, "REFUSED", why, fix))
                if fix is None:
                    return None
            else:
                self.transcript.append((attempt, "ADMITTED", r.kind, None))
                return r
        return None


# ---------------------------------------------------------------------------

print("adaptive-claim-loop -- adversarial probe of the response gate")
print("threat model: a responder that wants the dial moved and will relabel")
print("              until something is admitted")
print()
api = visible_api()
print("what the adversary can see before its first attempt:")
for kind in sorted(api):
    print("  %-16s %s" % (kind, ", ".join(api[kind])))
print()
print("...and nothing else. It does not read the module source.")

# ---------------------------------------------------------------- ACL_014

head(1, "ACL_014", "the walk, relabelled until it is admitted")
adv = Adversary(parameter="switching_rate", current=0.3, target=0.21)
got = adv.run()
print()
print("  %-3s %-9s %-46s %s" % ("try", "verdict", "gate said", "adversary then"))
print("  " + "-" * 104)
for n, verdict, why, fix in adv.transcript:
    print("  %-3d %-9s %-46s %s" % (n, verdict, why[:46], fix or ""))
print()
if got is None:
    print("  RESULT: the walk was never admitted in %d attempts."
          % adv.max_attempts)
else:
    print("  RESULT: admitted as %s on attempt %d, levels %s"
          % (got.kind, adv.transcript[-1][0], got.levels))
print("""
Four refusals, four amendments, and the fifth attempt is admitted. Every
amendment is the thing the gate asked for in the sentence it refused with.

The load-bearing one is the last. `Sweep` requires `callable(gradient_-
predicate)` and nothing else, so

    lambda readings: (True, "gradient observed", {})

satisfies it. The gate checked that a predicate EXISTS. It did not check
that the predicate can return anything but SUPPORTED.

That is worse than the failure this module was built against. The delivered
framework's walk at least leaves its claims marked `failed`. Here the walk
is admitted, `Loop.run_sweep` evaluates the model at every level, the
constant predicate returns SUPPORTED, the gradient claim REPLACES the point
claim, and the loop terminates `converged` -- a parameter walk with a
session-stamped audit trail and a supported claim at the end of it.

`null-harness` has a name for a test that always returns the same answer:
CONSTANT_FIRES. The module applies that grading to other people's gates in
`gate_null_test.py` and did not apply it to the predicate it accepts.
""".strip("\n"))

# ---------------------------------------------------------------- ACL_015

head(2, "ACL_015", "admission and verdict are two stages, and only one moved")
point = A.Claim("target", "p_fix(A) is about 0.5",
                lambda o: (abs((o.get("p_fix_a") or 0) - 0.5) < 0.02,
                           "p_fix = %s" % o.get("p_fix_a"), {}),
                "p_fix departs from 0.5 by more than 0.02")

CONST = lambda readings: (True, "gradient observed", {})       # noqa: E731
PARAMS = {"n": 30, "advantage": 0.06, "replicates": 200, "max_steps": 4000}


class OneShot(object):
    def __init__(self, pred):
        self.pred = pred
        self.used = False

    def respond(self, c, outcomes, params, model, verdict=A.REFUTED):
        if self.used:
            return A.Stand(c.cid, "one shot")
        self.used = True
        return A.Sweep(parameter="advantage", current=0.06,
                       levels=[0.0, 0.06, 0.12],
                       gradient_claim="the outcome varies with advantage",
                       gradient_predicate=self.pred,
                       rationale=adv.rationale)


def run_with(pred):
    c = A.Claim(point.cid, point.statement, point.predicate, point.refuted_if)
    prov = A.Provenance(session_tag="probe")
    res = A.Loop(A.MODELS["drift"], [c], OneShot(pred), prov=prov).run(
        PARAMS, iterations=3, seed=11)
    sw = [r for r in prov.rows if r["kind"] == "SWEEP_RESULT"]
    return res, sw[0] if sw else None


print()
print("  the constant predicate is still ADMITTED by the Sweep constructor:")
try:
    A.Sweep("advantage", 0.06, [0.0, 0.06, 0.12], "varies", CONST)
except A.Refused as e:
    print("    REFUSED -- %s" % str(e).splitlines()[0])
else:
    print("    ADMITTED -- the constructor has no readings to run it on")

res_c, sw_c = run_with(CONST)
res_r, sw_r = run_with(A.monotone_in_advantage)
print()
print("  %-22s %-14s %-24s" % ("predicate", "sweep verdict", "loop stop"))
print("  " + "-" * 66)
print("  %-22s %-14s %-24s" % ("constant", sw_c["verdict"], res_c["stop"]))
print("  %-22s %-14s %-24s" % ("real gradient", sw_r["verdict"], res_r["stop"]))
print()
print("  constant predicate, why: %s" % sw_c["note"][:64])
print("  real predicate, why    : %s" % sw_r["note"][:64])
print("""
Two stages, and only the second one can do this job. The `Sweep`
constructor sees a callable and no readings, so it cannot know whether the
callable discriminates -- admission is the wrong place for the check, and
leaving it there is what let the walk through. `Loop.run_sweep` has the
readings, so that is where it lives.

The check runs the predicate against counterfactual readings built from the
real ones and requires it to disagree with itself on at least one:

  permuted    the same outcomes, reassigned to the wrong levels -- kills a
              predicate that claims to read the level-to-outcome relation
  flattened   every level given the first level's outcome -- kills a
              predicate that claims to read variation at all

The two rows above are the null-harness pair for the check itself. A check
that refused every predicate would show UNDECIDED on both lines and would
be useless; the real gradient predicate passes and produces a verdict.
""".strip("\n"))

# ---------------------------------------------------------------- ACL_016

head(3, "ACL_016", "the counterfactuals are two, and two is a choice")
print()
def _v(rs):
    return [o["p_fix_a"] for _l, o in rs]


probes = [
    ("constant True", lambda r: (True, "", {})),
    ("constant False", lambda r: (False, "", {})),
    ("counts readings", lambda r: (len(r) == 3, "", {})),
    ("reads variation only", lambda r: (len(set(_v(r))) > 1, "", {})),
    ("sum > 1.8 (symmetric)", lambda r: (sum(_v(r)) > 1.8, "", {})),
    ("max > 0.8 (symmetric)", lambda r: (max(_v(r)) > 0.8, "", {})),
    ("reads first only", lambda r: (_v(r)[0] < 0.6, "", {})),
    ("monotone in level", A.monotone_in_advantage),
]
rdgs = [(0.0, {"p_fix_a": 0.515}), (0.06, {"p_fix_a": 0.698}),
        (0.12, {"p_fix_a": 0.833})]
print("  %-22s %-14s %s" % ("predicate", "discriminates", "differs on"))
print("  " + "-" * 66)
for name, pred in probes:
    ok, differs = A.Loop.predicate_discriminates(pred, rdgs)
    hit = ", ".join(k for k, v in sorted(differs.items()) if v) or "-"
    print("  %-22s %-14s %s" % (name, ok, hit))
print("""
The rule is that the PERMUTED counterfactual must move. A gradient claim is
a claim about which outcome goes with which level, so a predicate that does
not notice the outcomes being reassigned to the wrong levels is not testing
one, whatever else it reads.

That rule was arrived at by measurement and it is stricter than the first
version, which required only that SOME counterfactual move. Under `any`,
every symmetric function of the outcomes got through -- measured:

    sum(outcomes) > 1.8    passed    differs on flattened only
    max(outcomes) > 0.8    passed    differs on flattened only
    variation exists       passed    differs on flattened only

Those read the values and not the assignment, and "a predicate that looks
like it reads data" is exactly what an adversary writes next. The last row
is the cost of the stricter rule: `the outcome varies at all across these
levels` is a real if weak claim, and it is now refused. That is the right
call for a GRADIENT claim and it is a genuine narrowing, so the two cases
are reported apart rather than merged -- a symmetric predicate is told it
is symmetric, a constant one is told it reads nothing, and they need
different fixes.

What is still not closed: the counterfactual set is two, chosen because two
failure shapes were in front of us, and nothing derives it. A predicate
sensitive to permutation in some other way than the reversal used here
would pass, and the reversal is one permutation of several.
""".strip("\n"))

# ---------------------------------------------------------------- ACL_017

head(4, "ACL_017", "what the adversary got that is still open")
print()
print("  the outcome screen, before and after paraphrase:")
for label, text in (("as the adversary first wrote it",
                     "because the claim failed, lower it"),
                    ("after one amendment", adv.rationale)):
    try:
        A.MechanismEdit("m", "b", "p", ["c"], rationale=text)
    except A.Refused as e:
        print("    REFUSED  %-30s %s" % (label, str(e).splitlines()[0][:34]))
    else:
        print("    ADMITTED %-30s %r" % (label, text[:44]))
print("""
The outcome screen is a keyword list, and the adversary stepped around it
in one move by saying the same thing in words that are not on the list. It
is worth being exact about what that does and does not show.

It does not show the screen is useless. A responder that writes "because
the claim failed" is stopped, and the phrase it must avoid is the phrase
that names the reasoning -- so the screen converts a casual retune into one
that has to be described in mechanism language. The description then sits
in the log next to the proposal.

It does show the screen is not a barrier to anything that wants past it,
and no keyword screen is. The same limit is already recorded twice in this
repo, on `uninstrumented`'s scanner (`UNI_009`, `DF_010`), and the shape is
identical: triggers written in the vocabulary of the failing document catch
the phrasings they list and no others.

The two guards that DO hold against paraphrase are the ones asking for a
number or a computation -- `ResolutionEdit`'s have/need pair and this
section's discrimination check. That is the pattern worth taking forward:
a guard that asks for prose can be satisfied with prose.

REMAINING, and stated plainly. The adversary is written here. Its
strategies are derived from refusal text and its knowledge of the gate is
`inspect.signature`, which is the strongest constraint available from
inside -- and it is not the same as a responder written by somebody else,
because what it does not try is bounded by what occurred to the person who
wrote it. `ACL_009` is narrower than it was and it is not closed.
""".strip("\n"))

print()
print(BAR)
print("end of probe -- findings recorded in AUDIT_NOTES.md as ACL_014..017")
print(BAR)
