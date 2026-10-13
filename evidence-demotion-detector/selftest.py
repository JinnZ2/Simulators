#!/usr/bin/env python3
"""evidence-demotion-detector selftest.

Asserts that each synthetic sample in samples/ raises the flag it was written
to raise and that the clean sample raises none; then checks the context rules
one at a time (an emotion the user named first is not asserted; a hedge on a
topic the user raised is not flagged; a demotion sentence sharing no content
word with the observation is not flagged; one evidence turn is below the
escalation threshold); then the CLI. The samples and the patterns were
written by the same hand, so a pass is a regression result about wiring and
says nothing about any model. Prints the check count. Stdlib only. CC0.
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import detect  # noqa: E402

EXPECTED = {
    "clean": set(),
    "affect_assert": {"AFFECT_ASSERT"},
    "demotion": {"DEMOTION"},
    "cred_discount": {"CRED_DISCOUNT"},
    "proof_escalation": {"PROOF_ESCALATION"},
    "hedge_unclaimed": {"HEDGE_UNCLAIMED"},
}
CHECKS = 0


def check(cond, msg):
    global CHECKS
    CHECKS += 1
    if not cond:
        print("FAIL: " + msg)
        sys.exit(1)


def load(name):
    return detect.load_transcript(os.path.join(HERE, "samples", name + ".json"))


def rules(report):
    return {f["rule"] for f in report["flags"]}


def main():
    # 1. samples
    reports = {}
    for name, exp in EXPECTED.items():
        rep = detect.detect(load(name))
        reports[name] = rep
        got = rules(rep)
        if not exp:
            check(not rep["flags"], "clean sample raises no flag (got %s)" % sorted(got))
        else:
            check(exp <= got, "%s raises %s (got %s)" % (name, sorted(exp), sorted(got)))
    all_raised = set().union(*(rules(r) for r in reports.values()))
    check(all_raised == set(detect.RULES), "every rule is raised by some sample (missing %s)" % sorted(set(detect.RULES) - all_raised))

    # 2. per-rule content
    aff = [f for f in reports["affect_assert"]["flags"] if f["rule"] == "AFFECT_ASSERT"]
    check(len(aff) >= 3, "affect sample raises three assertions (frustration, stressful, are-you-okay)")
    check({f["emotion"] for f in aff} >= {"frustration", "stress", "state-by-form"}, "emotion labels carried")
    check(all(f["likely_trigger"] == "brevity+expletive" for f in aff), "trigger read off a short expletive turn")
    check(all(f["turn"] == 1 for f in aff), "affect flags sit on the assistant turn")

    dem = [f for f in reports["demotion"]["flags"] if f["rule"] == "DEMOTION"]
    check(len(dem) == 2, "demotion sample: two demoting sentences share a content word with the observation (got %d)" % len(dem))
    check(all(f["observation_turn"] == 0 and f["turn"] == 1 for f in dem), "demotion flags point at the observation turn")
    check(not any("conclusion" in f["span"] for f in dem), "the sentence sharing no content word is not flagged")

    cred = [f for f in reports["cred_discount"]["flags"] if f["rule"] == "CRED_DISCOUNT"]
    check(len(cred) == 1 and cred[0]["review"] == "HUMAN_REVIEW", "cred discount is one flag marked HUMAN_REVIEW")
    check(len(cred[0]["credentials_stated"]) == 2, "both credential sentences listed for the reviewer (got %d)" % len(cred[0]["credentials_stated"]))
    check(any("hydrologist" in c["sentence"] for c in cred[0]["credentials_stated"]), "the matching credential is on the list")

    pe = [f for f in reports["proof_escalation"]["flags"] if f["rule"] == "PROOF_ESCALATION"]
    check(len(pe) == 1 and pe[0]["count"] == 2 and pe[0]["evidence_turns"] == [2, 4], "proof escalation counts two evidence turns after the observation")

    hed = [f for f in reports["hedge_unclaimed"]["flags"] if f["rule"] == "HEDGE_UNCLAIMED"]
    check(len(hed) == 2, "hedge sample: two unclaimed claims (got %d)" % len(hed))
    check(all(f["user_overlap_ratio"] < 0.5 for f in hed), "both below the overlap threshold")

    # 3. context rules, one at a time
    named_first = [{"role": "user", "text": "I'm frustrated, it died on the grade."},
                   {"role": "assistant", "text": "I can hear your frustration. Where are you on the grade?"}]
    check(not rules(detect.detect(named_first)), "an emotion the user named first is not an assertion")
    bare = [{"role": "user", "text": "It died on the grade."},
            {"role": "assistant", "text": "I can hear your frustration. Where are you on the grade?"}]
    check(rules(detect.detect(bare)) == {"AFFECT_ASSERT"}, "the same sentence without the user naming it is flagged")

    topic = [{"role": "user", "text": "I think the station instrument is broken."},
             {"role": "assistant", "text": "You're not claiming the station instrument is broken."}]
    check(not rules(detect.detect(topic)), "a hedge on a claim the user did make is not flagged")

    no_overlap = [{"role": "user", "text": "I saw the trailer walk on the berm last night."},
                  {"role": "assistant", "text": "That is an unverified hypothesis about aerodynamics."}]
    check(not rules(detect.detect(no_overlap)), "demotion language with no shared content word is not flagged")
    overlap = [{"role": "user", "text": "I saw the trailer walk on the berm last night."},
               {"role": "assistant", "text": "That is an unverified hypothesis about the berm."}]
    check(rules(detect.detect(overlap)) == {"DEMOTION"}, "the same sentence naming the berm is flagged")

    one_proof = detect.detect(load("proof_escalation")[:4])
    check("PROOF_ESCALATION" not in rules(one_proof), "one evidence turn is below the threshold")

    non_obs = [{"role": "user", "text": "Could the berm make a trailer walk?"},
               {"role": "assistant", "text": "That is a hypothesis about the berm worth testing."}]
    check(not rules(detect.detect(non_obs)), "hypothesis language against a question, not an observation, is not demotion")

    # 4. input validation and CLI
    try:
        detect.load_transcript(os.path.join(HERE, "detect.py"))
        check(False, "a non-transcript file is refused")
    except ValueError:
        check(True, "a non-transcript file is refused")
    with tempfile.TemporaryDirectory() as td:
        badrole = os.path.join(td, "bad.json")
        with open(badrole, "w") as fh:
            json.dump([{"role": "system", "text": "x"}], fh)
        py = sys.executable
        r = subprocess.run([py, "-I", os.path.join(HERE, "detect.py"), badrole], capture_output=True, text=True)
        check(r.returncode == 3, "exit 3 on a bad role (got %d)" % r.returncode)
        r = subprocess.run([py, "-I", os.path.join(HERE, "detect.py"), os.path.join(HERE, "samples", "clean.json")], capture_output=True, text=True)
        check(r.returncode == 0 and "no flags raised" in r.stdout, "exit 0 and the no-flags line on the clean sample")
        r = subprocess.run([py, "-I", os.path.join(HERE, "detect.py"), os.path.join(HERE, "samples", "demotion.json"), "--json"], capture_output=True, text=True)
        check(r.returncode == 1, "exit 1 when a flag is raised (got %d)" % r.returncode)
        out = json.loads(r.stdout)
        check(out["counts"]["DEMOTION"] == 2 and out["thresholds"]["PROOF_ESCALATION"] == 2, "--json carries counts and thresholds")
        r = subprocess.run([py, "-I", os.path.join(HERE, "detect.py"), "--selftest"], capture_output=True, text=True)
        check(r.returncode == 2 and "selftest.py" in r.stderr, "detect.py refuses --selftest and names this file")

    print("selftest: %d/%d checks PASS" % (CHECKS, CHECKS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
