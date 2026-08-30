#!/usr/bin/env python3
"""Checks on the delivered `experience_ledger.py`. Imports it, edits it
not at all.

The thesis is right and it is the folder's point: an origin claim
confers present-tense standing, the standing is almost never rechecked,
and the module refuses to score the claim -- it emits the maintenance
question instead. Everything checked here is downstream of that.

Three arms:

  SELF        the module's own PROOF_CASE, rendered as a claim and run
              through the module's own check(). An instrument that
              classifies its own proof is worth reading.
  BRANCHES    every path of check() and transfer(), reached by
              audit-authored PROBES that are labelled probes and are
              not cases.
  SURFACE     the CLI, the None states, and the four header examples.

CC0. stdlib only. Parses under Python 3.9.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import experience_ledger as E  # noqa: E402

PROBES = os.path.join(HERE, "probes")
REGISTER = os.path.join(ROOT, "fold-matrix", "fold_register.py")


def probes():
    out = {}
    for fn in sorted(os.listdir(PROBES)):
        if fn.endswith(".json"):
            out[fn] = json.load(open(os.path.join(PROBES, fn),
                                     encoding="utf-8"))
    return out


def proof_case_verdict():
    """What the module says about its own proof."""
    p = probes()["proof_case_as_claim.json"]
    return E.check(p)


def branch_keys():
    """The keys each branch of check() returns."""
    return {
        "NOT CLASSIFIABLE": sorted(E.check({})),
        "ASSERTED/DISCARDED": sorted(E.check({"decay_class": "physiological",
                                              "continuity_granted": True})),
        "MEASURABLE": sorted(E.check({"decay_class": "physiological",
                                      "maintained_since": "2020"})),
    }


def maintained_states():
    """What counts as `measured`."""
    out = {}
    for val in ("", 0, False, None, "2020-01", []):
        c = {"decay_class": "physiological", "continuity_granted": True,
             "maintained_since": val}
        out[repr(val)] = E.check(c)["verdict"]
    return out


def none_meanings():
    """`None` in the output, and what it means in each place."""
    standing = E.check({"decay_class": "standing",
                        "continuity_granted": True})
    physio = E.check({"decay_class": "physiological",
                      "continuity_granted": True})
    return {
        "standing.question_skipped": standing["question_skipped"],
        "physiological.question_skipped": physio["question_skipped"],
        "standing.score": standing["score"],
    }


_AGE = re.compile(r"\b(since I was \w+|as a kid|from age \w+|since age \w+"
                  r"|aged? \d+)\b", re.I)


def header_examples():
    """The four examples in the header, and whether each carries an age
    marker.

    The header says `Same grammatical form. Opposite handling.` The
    handling claim is about fields and is not checkable here. The FORM
    claim is checkable against the four strings, and is checked -- not
    to dispute the argument, which does not need all four to match, but
    because a stated invariant over four items either holds over four
    items or does not.
    """
    src = open(os.path.join(HERE, "experience_ledger.py"),
               encoding="utf-8").read()
    block = re.search(r'#\s+"coded since.*?#\s*$', src, re.S | re.M)
    lines = re.findall(r'#\s+"([^"]+)"\s+->\s+(.+)$',
                       block.group(0) if block else src, re.M)
    out = []
    for text, handling in lines:
        m = _AGE.search(text)
        out.append({"example": text, "handling": handling.strip(),
                    "age_marker": m.group(0) if m else None})
    return out


def register_link():
    """The `experience` entry in fold-matrix's folded-term register."""
    if not os.path.exists(REGISTER):
        return None
    sys.path.insert(0, os.path.dirname(REGISTER))
    import fold_register as F
    rec = F.REGISTER.get("experience")
    return None if rec is None else {
        "source": rec["source"],
        "substitutes_for": rec["substitutes_for"],
        "residual_tell": rec["residual_tell"],
        "counter_case": rec["counter_case"],
    }


def cli(args):
    p = subprocess.run([sys.executable,
                        os.path.join(HERE, "experience_ledger.py")] + args,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       timeout=60)
    return p.returncode, p.stdout.decode("utf8", "replace")


def usage_vs_implemented():
    src = open(os.path.join(HERE, "experience_ledger.py"),
               encoding="utf-8").read()
    header = src.split("import json")[0]
    advertised = set(re.findall(r"experience_ledger\.py\s+(--\w+)", header))
    implemented = set(re.findall(r'"(--\w+)" in argv', src)) | \
        set(re.findall(r'argv\.index\("(--\w+)"\)', src))
    return {"advertised": sorted(advertised),
            "implemented": sorted(implemented),
            "advertised_not_implemented": sorted(advertised - implemented),
            "implemented_not_advertised": sorted(implemented - advertised)}


# ------------------------------------------------------------- report

def render():
    out = []
    out.append("EXPERIENCE LEDGER AUDIT")
    out.append("the module is imported and not modified")
    out.append("")
    out.append("No claim is judged here and no case is recorded. The")
    out.append("probes are audit-authored branch probes and say so in")
    out.append("every file.")
    out.append("")

    out.append("1. THE MODULE RUN ON ITS OWN PROOF")
    v = proof_case_verdict()
    out.append("   PROOF_CASE class: %s" % E.PROOF_CASE["class"])
    out.append("   check() verdict:  %s" % v["verdict"])
    out.append("   question skipped: %s" % (v["question_skipped"] or "")[:52])
    out.append("   The proof case asserts continuity and measures")
    out.append("   nothing, so the instrument returns its own verdict on")
    out.append("   it. That is the honest outcome and not a fault: the")
    out.append("   decay half is physiology and the granting half is a")
    out.append("   statement about fields that nothing here measures.")
    out.append("")

    out.append("2. THE HELP TEXT IS THE STRING `None`")
    uv = usage_vs_implemented()
    out.append("   __doc__ is None: %s  (the header is # comments, not a"
               % (E.__doc__ is None))
    out.append("   docstring, and main()'s else branch prints __doc__)")
    for args, label in ((["--transfer", "a", "b"], "--transfer a b"),
                        ([], "no argument"),
                        (["--classes"], "--classes"),
                        (["--schema"], "--schema"),
                        (["--check"], "--check with no file")):
        rc, o = cli(args)
        first = (o.strip().split("\n") or [""])[0]
        out.append("     %-22s rc=%-3s %s" % (label, rc, first[:40]))
    out.append("   advertised, not implemented: %s"
               % uv["advertised_not_implemented"])
    out.append("   implemented, not advertised: %s"
               % uv["implemented_not_advertised"])
    out.append("")

    out.append("3. WHAT COUNTS AS MEASURED")
    for k, v_ in sorted(maintained_states().items()):
        out.append("     maintained_since=%-10s %s" % (k, v_))
    out.append("   `is UNCHECKED` is an identity test against None, so")
    out.append("   an empty string, a zero and False all read as")
    out.append("   measured. There is no state for `checked, and nothing")
    out.append("   was found`.")
    out.append("")

    out.append("4. ONE FIELD, `None`, TWO READINGS")
    nm = none_meanings()
    out.append("     standing.question_skipped        %r"
               % nm["standing.question_skipped"])
    out.append("     physiological.question_skipped   %s"
               % (nm["physiological.question_skipped"] or "")[:40])
    out.append("   For `standing` the field is None because the class has")
    out.append("   no measurable by design -- standing is named as not a")
    out.append("   competence. Read as output, `question_skipped: null`")
    out.append("   says no question was skipped, which is the opposite.")
    out.append("")

    out.append("5. THE REFUSAL IS NOT UNIFORM ACROSS BRANCHES")
    for name, keys in branch_keys().items():
        out.append("     %-22s %s" % (name, keys))
    out.append("   `score: UNCHECKED` is on one branch of three. A caller")
    out.append("   reading `score` gets a KeyError on the other two.")
    out.append("")

    out.append("6. THE FOUR HEADER EXAMPLES")
    for r in header_examples():
        out.append("     %-34s %-26s age marker: %s"
                   % ('"%s"' % r["example"][:32], r["handling"][:26],
                      r["age_marker"] or "NONE"))
    out.append("   Three carry an age or origin marker and one does not.")
    out.append("   `Same grammatical form` holds over three of four; the")
    out.append("   argument does not need all four, and the line says")
    out.append("   four.")
    out.append("")

    out.append("7. THE REGISTER ENTRY THIS DECOMPOSES")
    rl = register_link()
    if rl is None:
        out.append("     fold-matrix/fold_register.py not found")
    else:
        out.append("     source          %s" % rl["source"])
        out.append("     substitutes_for %s" % rl["substitutes_for"])
        out.append("     residual_tell   %s" % rl["residual_tell"][:56])
        out.append("     counter_case    %r" % rl["counter_case"])
        out.append("   The register named the components and marked them")
        out.append("   unchecked. This module is the instrument for the")
        out.append("   three it names, and PROOF_CASE is material for the")
        out.append("   counter_case cell the register leaves UNFILLED.")
    return "\n".join(out)


# ------------------------------------------------------------ selftest

def selftest():
    ok = [0]
    bad = []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    # -- 1. the module on its own proof
    v = proof_case_verdict()
    chk("the module returns its own verdict on its own proof case",
        v["verdict"] == "CONTINUITY ASSERTED, NOT MEASURED")
    chk("PROOF_CASE names a decay class the module defines",
        E.PROOF_CASE["class"] in E.DECAY_CLASSES)
    chk("that class has a present_measurable",
        E.DECAY_CLASSES[E.PROOF_CASE["class"]]["present_measurable"])

    # -- 2. the help text
    chk("__doc__ is None", E.__doc__ is None)
    rc, o = cli([])
    chk("no argument prints the string None", rc == 0 and o.strip() == "None")
    rc, o = cli(["--transfer", "a", "b"])
    chk("--transfer, which is advertised, prints None",
        rc == 0 and o.strip() == "None")
    uv = usage_vs_implemented()
    chk("--transfer is advertised", "--transfer" in uv["advertised"])
    chk("--transfer is not implemented",
        "--transfer" in uv["advertised_not_implemented"])
    chk("--schema is implemented and not advertised",
        "--schema" in uv["implemented_not_advertised"])
    chk("--classes is both", "--classes" in uv["advertised"]
        and "--classes" in uv["implemented"])
    rc, o = cli(["--check"])
    chk("--check with no file raises rather than reporting",
        rc != 0 and "IndexError" in o)
    rc, o = cli(["--classes"])
    chk("--classes emits the six classes", rc == 0
        and set(json.loads(o)) == set(E.DECAY_CLASSES))

    # -- 3. what counts as measured
    ms = maintained_states()
    chk("None is the only unmeasured state", ms["None"]
        == "CONTINUITY ASSERTED, NOT MEASURED")
    chk("an empty string reads as measured", ms["''"] == "MEASURABLE")
    chk("zero reads as measured", ms["0"] == "MEASURABLE")
    chk("False reads as measured", ms["False"] == "MEASURABLE")
    chk("a real value reads as measured", ms["'2020-01'"] == "MEASURABLE")

    # -- 4. None in the output
    nm = none_meanings()
    chk("standing has no present_measurable",
        E.DECAY_CLASSES["standing"]["present_measurable"] is None)
    chk("so its question_skipped is None",
        nm["standing.question_skipped"] is None)
    chk("a competence class has a real one",
        isinstance(nm["physiological.question_skipped"], str))
    chk("score is None on that branch", nm["standing.score"] is None)

    # -- 5. branch keys
    bk = branch_keys()
    chk("score is on exactly one branch",
        sum(1 for k in bk.values() if "score" in k) == 1)
    chk("NOT CLASSIFIABLE carries a blocker",
        "blocker" in bk["NOT CLASSIFIABLE"])
    chk("MEASURABLE carries what to run", "run" in bk["MEASURABLE"])

    # -- 6. header examples
    he = header_examples()
    chk("four examples are extracted", len(he) == 4)
    chk("three carry an age marker",
        sum(1 for r in he if r["age_marker"]) == 3)
    chk("the one without is the school-paper line",
        [r["example"] for r in he if not r["age_marker"]]
        == ["ran the school paper / scouts"])
    chk("three are granted and one is not",
        sum(1 for r in he if r["handling"].startswith("continuity granted"))
        == 3)

    # -- 7. transfer refuses the aggregate
    t = E.transfer({"substrates": ["fault_propagation", "zzz_not_real"]})
    chk("transfer returns no aggregate", t["aggregate"] is None)
    chk("every substrate is carried as unchecked",
        all(x["carried"] is None for x in t["per_substrate"].values()))
    chk("an undefined substrate is named as undefined",
        t["per_substrate"]["zzz_not_real"]["test"] == "undefined substrate")
    chk("but it still occupies a row like a real one",
        len(t["per_substrate"]) == 2)
    chk("an empty substrate list gives an empty map",
        E.transfer({})["per_substrate"] == {})

    # -- the register entry
    rl = register_link()
    chk("the fold-matrix register is reachable", rl is not None)
    if rl:
        chk("experience is a candidate there", rl["source"] == "candidate")
        chk("its components are the three this module instruments",
            "continuity" in rl["substitutes_for"]
            and "transfer" in rl["substitutes_for"])
        chk("its counter_case is still UNFILLED",
            rl["counter_case"] is None)

    # -- probes are labelled probes
    ps = probes()
    chk("every probe declares its provenance",
        all("_provenance" in p for p in ps.values()))
    chk("every probe says it is not a case",
        all("Not a case" in p["_provenance"] for p in ps.values()))
    chk("the probes reach three distinct verdicts",
        len({E.check(p)["verdict"] for p in ps.values()}) == 3)

    txt = render()
    chk("render names all seven sections",
        all(("%d." % i) in txt for i in range(1, 8)))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for b in bad:
        print("  FAILED", b)
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
