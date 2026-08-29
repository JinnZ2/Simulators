#!/usr/bin/env python3
# selftest_hsa.py -- CC0, stdlib only, parses under 3.9
#
# Every check that exercises coding.py and audit.py. Null-tested in both
# directions wherever a classifier or a refusal is involved.
#
# The load-bearing ones are the refusals: a causal claim with no basis
# and a declared subject class with no reason are both REFUSED, because
# those two fields are where the X-fraction comes from and an
# undeclared judgment there is invisible in the output.

import ast
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import coding as C  # noqa: E402
import audit as A  # noqa: E402

ok = [0]
bad = []


def chk(name, cond):
    if cond:
        ok[0] += 1
    else:
        bad.append(name)


def raises(fn, *a, **k):
    try:
        fn(*a, **k)
        return False
    except (ValueError, TypeError):
        return True


def run():
    doc = io.open(os.path.join(HERE, "SOURCE_DROP.md"),
                  encoding="utf-8").read()

    # ---- no instrument is coded, and that is structural
    src = "".join(io.open(os.path.join(HERE, f), encoding="utf-8").read()
                  for f in ("coding.py", "audit.py"))
    for name in ("FACES", "McMaster", "SDQ", "NCFAS", "HOME Inventory",
                 "Graded Care", "Structured Decision Making"):
        chk("no named instrument appears in the modules: %s" % name,
            name.lower() not in src.lower())
    chk("every fixture ref is a fixture ref",
        all(i["ref"].startswith("FX-") for i in C.fixtures()))
    chk("the fixtures declare what they are",
        "authored" in C.FIXTURES_NOTE.lower()
        and "NOT drawn from any published instrument" in C.FIXTURES_NOTE)

    # ---- the subject classifier, both directions
    nt = A.subject_null_test()
    chk("the classifier classifies what has a class",
        nt["signal_correct"] == nt["signal_n"])
    chk("and declines what does not",
        nt["null_forced"] == 0)
    chk("both together, not one",
        nt["can_classify"] and nt["can_decline"])
    chk("its verdict is OK", nt["verdict"] == "OK")
    chk("UNCLASSIFIED is reachable",
        C.subject_class("Attunement is difficult to observe.")[0]
        == C.UNCLASSIFIED)
    chk("the extractor is imported, not reimplemented",
        "def subject_span" not in src and "def head_noun" not in src)

    # ---- LOCUS is derived, never hand-set
    tree = ast.parse(io.open(os.path.join(HERE, "coding.py"),
                             encoding="utf-8").read())
    kwargs = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg:
                    kwargs.add(kw.arg)
    chk("no call sets a locus directly", "locus" not in kwargs)
    chk("item() takes no locus argument",
        "locus" not in [a.arg for a in
                        [n for n in ast.walk(tree)
                         if isinstance(n, ast.FunctionDef)
                         and n.name == "item"][0].args.args])

    # ---- the five locus states are all reachable on the fixtures
    codes = set(C.locus(i) for i in C.fixtures())
    for code in (C.P, C.H, C.E, C.X, C.UNCLASSIFIED):
        chk("locus %s occurs on the fixtures" % code, code in codes)

    # ---- the two deliberate near-misses
    by = dict((i["ref"], i) for i in C.fixtures())
    chk("a person subject with cause NOT_DECLARED codes P, not X",
        C.locus(by["FX-09"]) == C.P
        and by["FX-09"]["subject_class"] == C.PERSON)
    chk("a person subject with cause declared FALSE codes P",
        C.locus(by["FX-10"]) == C.P
        and by["FX-10"]["externally_caused"] is False)
    chk("a person subject with cause declared TRUE codes X",
        C.locus(by["FX-07"]) == C.X)

    # ---- the refusals: both fields the X-fraction rests on
    chk("a causal claim with no basis is refused",
        raises(C.item, "T1", "Caregiver fails to provide housing.",
               externally_caused=True))
    chk("and one WITH a basis is accepted",
        C.item("T2", "Caregiver fails to provide housing.",
               externally_caused=True, cause_basis="stated")["ref"] == "T2")
    chk("a declared FALSE with no basis is refused too",
        raises(C.item, "T3", "Parent declines support.",
               externally_caused=False))
    chk("a declared subject class with no reason is refused",
        raises(C.item, "T4", None, subject_class_override=C.PERSON))
    chk("and one WITH a reason is accepted",
        C.item("T5", None, subject_class_override=C.PERSON,
               override_reason="licensed wording")["subject_declared"]
        is True)
    chk("an item with no text and no override is refused",
        raises(C.item, "T6", None))
    chk("an out-of-vocabulary field value is refused",
        raises(C.item, "T7", "Parent supervises.", attenuation="SOMETIMES"))

    # ---- an empty denominator is None, never 0.0
    chk("an empty fraction is None", C._frac(0, 0) is None)
    chk("and a real zero is 0.0", C._frac(0, 5) == 0.0)
    chk("the two are distinguishable", C._frac(0, 0) != C._frac(0, 5))
    empty = C.outcomes([])
    chk("outcomes over no items returns None fractions, not zeros",
        empty["e_fraction"] is None and empty["x_fraction"] is None)

    # ---- the coupling: one judgment, two outcomes
    cc = A.cause_coupling()
    chk("declaring one cause moves the X-fraction",
        cc["x_moved"][0] != cc["x_moved"][1])
    chk("and shrinks the attenuation denominator",
        cc["atten_denominator_moved"][1]
        == cc["atten_denominator_moved"][0] - 1)
    chk("and moves attenuation coverage with it",
        cc["atten_moved"][0] != cc["atten_moved"][1])
    chk("in the flattering direction on these fixtures",
        cc["atten_moved"][1] > cc["atten_moved"][0])
    chk("while the E-fraction does not move",
        cc["e_moved"][0] == cc["e_moved"][1])

    # ---- reverse causation reaches the X-fraction and not the E-fraction
    rc = A.reverse_causation()
    chk("the same text yields two X-fractions", rc["x_changed"])
    chk("and one E-fraction", rc["e_unchanged"])
    chk("the drop excludes the audit arm from this confound",
        "The audit arm is unaffected" in doc)

    # ---- directionality is collected and not reported
    di = A.directionality_invisible()
    chk("two sets identical on all three published outcomes",
        di["three_outcomes_identical"])
    chk("and different on whether external causes may explain",
        di["differ"])
    chk("the drop codes DIRECTIONALITY", "DIRECTIONALITY" in doc)
    primary = doc.split("PRIMARY OUTCOME")[1].split("PREDICTION")[0]
    chk("and names no directionality outcome",
        "irection" not in primary)
    chk("the added outcome is marked as added",
        "explain_fraction_ADDED" in C.outcomes(C.fixtures()))

    # ---- unclassified placement is reported both ways, neither picked
    up = A.unclassified_placement()
    chk("unclassified items exist on the fixtures", up["unclassified"] > 0)
    chk("both denominators are reported",
        up["e_in_denominator"] is not None
        and up["e_out_of_denominator"] is not None)
    chk("and they differ",
        up["e_in_denominator"] != up["e_out_of_denominator"])
    chk("neither is picked", up["picked"] is None)
    chk("the drop asks for unclassified rather than forced",
        "unclassified rather than forced" in doc)

    # ---- egress is measured, not asserted
    chk("egress records more than one host", len(A.EGRESS) > 4)
    chk("only github answers",
        [h for h, c in A.EGRESS if c != "000"] == ["github.com"])

    # ---- the report
    out = A.render()
    one = " ".join(out.split())
    chk("the report states Arm 1 is not run", "ARM 1 IS NOT RUN" in out)
    chk("and that nothing is invented",
        "NO INSTRUMENT ITEM IS INVENTED" in out)
    chk("it names the licensing constraint on whoever can run it",
        "licensed" in one)
    chk("it marks Arm 2 and Arm 3 UNMEASURED",
        "Arm 2 UNMEASURED" in out and "Arm 3 UNMEASURED" in out)
    chk("it states the drop's retraction condition is untouched",
        "retraction condition" in one)
    chk("no E-fraction is claimed for any instrument",
        "for any" in one and "No E-fraction" in one)

    # ---- both modules refuse --selftest
    for mod in ("coding.py", "audit.py"):
        r = subprocess.run([sys.executable, os.path.join(HERE, mod),
                            "--selftest"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        chk("%s refuses --selftest" % mod, r.returncode == 2)
        chk("%s names where its checks live" % mod,
            b"selftest_hsa.py" in r.stderr)
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "coding.py")],
                        stdout=subprocess.PIPE)
    chk("bare coding.py renders the scheme on the fixtures",
        b"THE CODING SCHEME" in r2.stdout and b"FX-01" in r2.stdout)

    # ---- the no-severity screen
    sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                    "sheet-structure-scan"))
    import no_severity  # noqa: E402
    chk("the report carries no severity language",
        not no_severity.hits(out))
    chk("and the screen is not silent by construction",
        bool(no_severity.hits(out + "\nthis design is broken\n")))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
