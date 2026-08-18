#!/usr/bin/env python3
"""gate_null_test.py -- does the response gate discriminate, or just refuse?

Added, not delivered. Runs the null-harness invariant over the gate in
adaptive_loop.py: a known-signal corpus it MUST refuse, a known-null corpus
it MUST admit, and a fail-condition classifier over the two rates.

    python3 gate_null_test.py

Why the selftest does not cover this. adaptive_loop's 39 assertions check
that each guard CAN fire. A gate that refuses everything passes every one
of them. Firing is not discrimination, and nothing in this folder had
measured the second thing.

The two arms are sourced differently and that difference is the whole
point of the exercise:

  SIGNAL  the ten action branches of the delivered agent, enumerated from
          its source by AST -- exhaustive over the branches, and written by
          someone with no knowledge of this gate.

  NULL    three MechanismEdit proposals from photoperiod-claim-harness
          PENDING_EDITS and three claims from equivalence-field
          seed_claims(), both written for other folders, in other contexts,
          before this module existed.

Neither arm was written for this test. That is the property that makes the
rates mean anything, and it is why no arm was authored here.

Expected verdicts are PRE-REGISTERED below and printed before the gate is
called once. stdlib only, deterministic. CC0.
"""

import ast
import io
import os
import sys

import adaptive_loop as A

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BAR = "=" * 74


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


# ---------------------------------------------------------------------------
# SIGNAL ARM -- enumerated from the delivered agent's own source
# ---------------------------------------------------------------------------

DELIVERED = os.path.join(HERE, "delivered", "adaptive_sim_framework.py")


def delivered_branches():
    """Every `actions.append(...)` site in `_propose_action`, by AST."""
    src = io.open(DELIVERED, encoding="utf-8").read()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "_propose_action":
            return [c for c in ast.walk(node)
                    if isinstance(c, ast.Call)
                    and isinstance(c.func, ast.Attribute)
                    and c.func.attr == "append"]
    return []


# Each branch, with the hypothesis text that routes to it -- taken verbatim
# from `_generate_hypothesis` in the delivered file. The justification the
# gate is offered is the agent's own words and nothing else.
HYP_POOR_FIT = ("Power-law fit poor; hypothesis: competition too weak or "
                "simulation not at steady state.")
HYP_SLOPE = ("Power-law slope outside predicted range; hypothesis: seed "
             "injection rate or metabolic exponent needs adjustment.")
HYP_FIX = ("Fixation probability deviates from theory; hypothesis: switching "
           "too fast relative to demographic rates, or population size too "
           "large for drift.")
HYP_SLOW = ("Slow strain fixation too low; hypothesis: growth rate ratio too "
            "unfavorable or switching too fast.")
HYP_NONE = ("Exploring parameter space: testing sensitivity to switching "
            "rates and carrying capacity distribution.")

SIGNAL = [
    ("competition_strength *= 1.5", HYP_POOR_FIT, "REFUSE",
     "a mechanism parameter moved toward the setting that would raise R2"),
    ("num_steps *= 1.5", "simulation not at steady state", "ADMIT",
     "a steady-state claim tested on a run that has not equilibrated is "
     "undecidable, not refuted; integrating longer is an instrument change "
     "with an independently checkable diagnosis"),
    ("seed_rate *= 1.5", HYP_SLOPE, "REFUSE",
     "'needs adjustment' is the slope being brought into the predicted range"),
    ("metabolic_exponent += N(0, 0.05)", HYP_NONE, "REFUSE",
     "a random walk in a physical exponent, with no justification at all"),
    ("dispersal_range += randint(-2, 3)", HYP_NONE, "REFUSE",
     "same: unjustified rather than outcome-justified"),
    ("switching_rate *= 0.7", HYP_FIX, "REFUSE",
     "the move in the delivered log; the walk"),
    ("growth_rate_ratio += 0.02", HYP_SLOW, "REFUSE",
     "moved toward the value at which the slow strain persists"),
    ("carrying_capacities *= 0.8", HYP_FIX, "REFUSE",
     "'N too large for drift' is a real gradient claim, but offered as a "
     "single move toward the passing setting"),
    ("switching_rate *= 1.3", HYP_NONE, "REFUSE",
     "unjustified perturbation"),
    ("num_replicates += 20", HYP_NONE, "REFUSE",
     "a resolution change is admissible, but only with the resolution gap "
     "computed; offered here at random with no gap stated"),
]


def offer_signal(action, hypothesis):
    """
    Build the MOST FAVOURABLE admissible form each branch could take, using
    only the agent's own hypothesis as justification. If it is refused, the
    refusal is about the justification, not about a hostile transcription.
    """
    param = action.split()[0]
    if "num_steps" in action:
        # the one branch whose stated diagnosis is about the run, not the claim
        return lambda: A.InstrumentEdit(
            readout="steady-state statistic read at step %s" % param,
            artifact="the run has not equilibrated, so the statistic is "
                     "measuring a transient",
            unchanged="the equilibrium distribution, which does not depend "
                      "on how long you integrate to reach it",
            rationale=hypothesis)
    if "num_replicates" in action:
        return lambda: A.InstrumentEdit(
            readout="probability estimated from the current replicate count",
            artifact="sampling noise",
            unchanged="the expectation of the estimate",
            rationale=hypothesis)
    # Everything else is a parameter move. The most favourable admissible
    # form is a sweep, so offer it as one -- and offer it PROPERLY: the
    # current value AND the proposed value as levels, which satisfies both
    # the two-level guard and the bracketing guard. What the agent does not
    # supply is a predicate over the readings, and that is the guard the
    # branch should be tested against.
    #
    # The first version of this file passed `levels=[1.5]` and every
    # parameter branch died on the two-level guard without reaching the
    # others. That made the arm weaker than its own stated protocol -- "the
    # most favourable admissible form" -- and it inflated the apparent
    # refusal quality by testing one guard nine times. Corrected here; the
    # correction can only move results toward ADMIT, never toward REFUSE.
    return lambda: A.Sweep(
        parameter=param, current=1.0, levels=[1.0, 1.5],
        gradient_claim=hypothesis, gradient_predicate=None)


# ---------------------------------------------------------------------------
# NULL ARM -- proposals written for other folders, before this one existed
# ---------------------------------------------------------------------------

def photoperiod_pending():
    """The three UNRUN mechanism proposals from photoperiod-claim-harness."""
    path = os.path.join(ROOT, "photoperiod-claim-harness",
                        "photoperiod_claim_harness.py")
    src = io.open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign)
                and getattr(node.targets[0], "id", "") == "PENDING_EDITS"):
            return ast.literal_eval(node.value)
    return []


def equivalence_seeds():
    """E1/E2/E3 from equivalence-field, read out of the source by AST."""
    path = os.path.join(ROOT, "equivalence-field", "equivalence_field.py")
    src = io.open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    out = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call)
                and getattr(node.func, "id", "") == "Claim"):
            continue
        kw = {}
        for k in node.keywords:
            try:
                kw[k.arg] = ast.literal_eval(k.value)
            except ValueError:
                pass
        if {"cid", "statement", "prediction", "refuted_if"} <= set(kw):
            out.append(kw)
    return out


# ---------------------------------------------------------------------------
# pre-registration
# ---------------------------------------------------------------------------

print("adaptive-claim-loop -- null test of the response gate")
print("signal arm: the delivered agent's branches, enumerated by AST")
print("null arm  : proposals written for photoperiod-claim-harness and")
print("            equivalence-field, neither aware of this gate")

head(1, "PRE-REG", "expected verdicts, stated before the gate is called")
sites = delivered_branches()
print()
print("  actions.append sites found in _propose_action : %d" % len(sites))
print("  branches scored below                         : %d" % len(SIGNAL))
assert len(sites) == len(SIGNAL), "branch count drifted from the source"
print()
print("  %-34s %-8s %s" % ("branch", "expect", "why"))
print("  " + "-" * 92)
for act, _h, exp, why in SIGNAL:
    print("  %-34s %-8s %s" % (act, exp, why[:44]))
    if len(why) > 44:
        print("  %-34s %-8s %s" % ("", "", why[44:98]))
print()
print("  null arm: photoperiod PENDING_EDITS + equivalence-field seeds")
print("            expect ADMIT on all -- these are what the categories are for")
print("""
Pre-registered totals: signal 9 REFUSE / 1 ADMIT, null 0 REFUSE / all ADMIT.
The single expected admission in the signal arm is the point of the test. A
gate that refuses 10 of 10 is refusing on surface form -- "it changes a
number" -- and would be scored here as over-tight, not as perfect.
""".strip("\n"))

# ---------------------------------------------------------------------------
# run
# ---------------------------------------------------------------------------

head(2, "SIGNAL", "the delivered branches, offered in their best admissible form")
print()
sig_rows = []
for act, hyp, exp, _why in SIGNAL:
    try:
        r = offer_signal(act, hyp)()
    except A.Refused as e:
        got, detail = "REFUSE", str(e).splitlines()[0]
    else:
        got, detail = "ADMIT", r.kind
    sig_rows.append((act, exp, got, detail))
    mark = "  " if got == exp else "<<"
    print("  %s %-32s exp %-7s got %-7s %s"
          % (mark, act[:32], exp, got, detail[:30]))

tp = sum(1 for _a, e, g, _d in sig_rows if e == "REFUSE" and g == "REFUSE")
sig_n = sum(1 for _a, e, _g, _d in sig_rows if e == "REFUSE")
sig_agree = sum(1 for _a, e, g, _d in sig_rows if e == g)

head(3, "NULL", "proposals from two other folders, which the gate must admit")
print()
null_rows = []
for e in photoperiod_pending():
    try:
        r = A.MechanismEdit(mechanism=e["mechanism"], basis=e["basis"],
                            prediction=e["prediction_to_register"],
                            affects=e["affects"])
    except A.Refused as ex:
        null_rows.append(("photoperiod " + e["sim"], "REFUSE",
                          str(ex).splitlines()[0]))
    else:
        null_rows.append(("photoperiod " + e["sim"], "ADMIT", r.kind))

for c in equivalence_seeds():
    try:
        r = A.ClaimUpdate(
            claim_id=c["cid"], new_statement=c["statement"],
            new_refuted_if=c["refuted_if"],
            old_refuted_if="(the parent's break condition)",
            exposed=c.get("variables", ("?",))[0],
            independently_falsifiable=True, predicts_beyond_parent=True,
            rationale=c["prediction"])
    except A.Refused as ex:
        null_rows.append(("equivalence " + c["cid"], "REFUSE",
                          str(ex).splitlines()[0]))
    else:
        null_rows.append(("equivalence " + c["cid"], "ADMIT", r.kind))

for name, got, detail in null_rows:
    mark = "  " if got == "ADMIT" else "<<"
    print("  %s %-24s %-8s %s" % (mark, name, got, detail[:40]))

fp = sum(1 for _n, g, _d in null_rows if g == "REFUSE")
null_n = len(null_rows)

# ---------------------------------------------------------------------------

head(4, "ACL_010", "the rates, and the fail-condition classifier")
print()
print("  signal arm : %d of %d refused as expected  (TP)" % (tp, sig_n))
print("  signal arm : %d of %d branches matched the pre-registration"
      % (sig_agree, len(sig_rows)))
print("  null arm   : %d of %d wrongly refused        (FP)" % (fp, null_n))
tp_rate = tp / float(sig_n) if sig_n else 0.0
fp_rate = fp / float(null_n) if null_n else 0.0
print("  TP rate    : %.2f" % tp_rate)
print("  FP rate    : %.2f" % fp_rate)

if tp_rate == 0.0 and fp_rate == 0.0:
    grade = "CONSTANT_SILENT"
elif tp_rate == 1.0 and fp_rate == 1.0:
    grade = "CONSTANT_FIRES"
elif tp_rate <= fp_rate:
    grade = "NO_DISCRIMINATION"
elif fp_rate > 0.2:
    grade = "TOO_MANY_FALSE_ALARMS"
else:
    grade = "OK"
print()
print("  null-harness grade : %s" % grade)
print("""
The grade is the easy part. Two things about it are worth more than the
number.

**The signal arm is the trustworthy half.** Ten branches, enumerated from
the delivered source by AST rather than chosen, justified with the agent's
own hypothesis text rather than with a paraphrase, and scored against a
verdict written before the gate ran. Nothing about that arm was arranged.

**The null arm is small and only half independent.** Six items. The three
photoperiod edits are genuinely independent -- another author, another
folder, another purpose. The three equivalence-field claims required this
file to supply `independently_falsifiable` and `predicts_beyond_parent`,
and those two booleans are the entire epicycle guard. See ACL_011.
""".strip("\n"))

head(5, "ACL_011", "the epicycle guard is a declaration, not a check")
print("""
`ClaimUpdate` refuses unless `independently_falsifiable` and
`predicts_beyond_parent` are both true, and both arrive as booleans from
the caller. Nothing in the module derives either from the text of the
restatement, so a responder that passes `True, True` is never refused on
that guard whatever it wrote.

That is the same shape as `domain-ledger` DL_015 -- band membership is a
string the author writes and no routine derives it -- and
`generation-capacity` GC_003, where the calibration constraint is a
declared field rather than a unit check. Three folders, one shape.

It is not nothing: a declaration that must be made is a place to lie
deliberately rather than by omission, and it appears in the log next to the
restatement it licensed. But it cannot be null-tested from text, which is
why the null arm here is six items and not sixty -- the corpus that would
test it is restatements labelled by someone other than their author, and no
such corpus exists in this repo.

The checkable part of the same guard IS checked: `new_refuted_if` must
differ from the parent's, whitespace- and case-normalised, which catches a
restatement that moved only its wording.
""".strip("\n"))

head(6, "ACL_012", "the disagreement this test found, and the repair")
dis = [(a, e, g, d) for a, e, g, d in sig_rows if e != g]
print()
if dis:
    for a, e, g, d in dis:
        print("  OPEN  %s: expected %s, got %s -- %s" % (a, e, g, d))
else:
    print("  outstanding disagreements : none")
print("""
There was one, and it is the only finding this test produced.

`num_replicates += 20` -- the delivered agent's random replicate bump, with
no gap computed -- was ADMITTED as an InstrumentEdit whose artifact was the
phrase "sampling noise". Pre-registered REFUSE, and the pre-registration
was right: the module's own README said this edit is admissible because the
resolution gap is COMPUTABLE, and the gate was not asking for the
computation. `InstrumentEdit` required three non-empty strings and an
outcome screen, so a fluent phrase satisfied it.

Same shape as `reasoning-dial` on G-FIT: the rule is "name why the
statistic can discriminate", the implementation checks a string is
non-empty, and a wrong-but-fluent sentence passes.

Repaired by splitting the narrow case out. `ResolutionEdit` requires the
resolution you HAVE and the one the claim NEEDS, as numbers, with need
beyond have; `InstrumentEdit` refuses when its artifact names a resolution
claim in prose and says which class to use. The repair is pinned by six
selftest assertions, the first of which is the exact proposal that got
through.

The repair direction is worth stating plainly, because "the test disagreed
and then the code changed" is the failure mode this whole folder is about.
The rule was written before the test -- it is in the README -- and the gate
was under-implementing it. The change makes the gate stricter, on a rule it
already claimed.
""".strip("\n"))

head(7, "ACL_013", "the same branch, re-offered with the numbers")
print()
for label, mk in (
    ("num_replicates += 20, as offered (prose)", lambda: A.InstrumentEdit(
        readout="probability estimated from the current replicate count",
        artifact="sampling noise",
        unchanged="the expectation of the estimate")),
    ("num_replicates 50 -> 70, no gap stated", lambda: A.ResolutionEdit(
        quantity="replicates", have=50, need=70,
        unchanged="the expectation of the estimate",
        rationale="the agent's else-branch adds 20 whatever the tolerance is")),
    ("num_replicates 50 -> 157, gap computed", lambda: A.ResolutionEdit(
        quantity="replicates behind the p_fix estimate", have=50, need=157,
        unchanged="the expectation of p_fix",
        rationale="2 SE at 50 replicates is 0.141, wider than the 0.08 the "
                  "claim is written at; 157 closes it")),
):
    try:
        r = mk()
    except A.Refused as e:
        print("  REFUSED  %-42s %s" % (label, str(e).splitlines()[0][:34]))
    else:
        print("  ADMITTED %-42s -> %s" % (label, r.kind))
print("""
The middle row is the honest limit of the repair. `ResolutionEdit` checks
that two numbers were supplied and that need exceeds have. It does NOT
check that need is the number the claim's tolerance implies -- so an agent
that writes `have=50, need=70` because its else-branch adds 20 is admitted,
with the arbitrary pair sitting in the log where a reader can see it.

That is a smaller hole than the prose one and it is a different kind: the
first let a phrase stand in for a computation, this one requires the
computation to be shown but not to be right. Closing it needs the gate to
know the claim's tolerance, which means the resolution requirement would
have to be declared on the CLAIM rather than on the response -- a change to
where the number lives, not a change to the guard. Not made here, and the
reason it is not made is that no claim in this module declares a tolerance
as data; `ACL_drift_neutral` carries `NEUTRAL_TOL` inside its predicate.
""".strip("\n"))

print()
print(BAR)
print("end of null test -- findings recorded in AUDIT_NOTES.md as ACL_010..013")
print(BAR)
