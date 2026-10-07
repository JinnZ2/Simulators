# SPDX-License-Identifier: CC0-1.0
"""
test_sense.py -- the redirect target named by sense_as_match.py (root).

sense_as_match.py refuses --selftest and says "run test_sense.py". This is
that file. It runs the module's own run_checks(), then the added cases
below, and exits nonzero if either has a failure.

SELF-GRADED. Every check here was written by the same hand as the module it
checks, so a pass is a REGRESSION result, not validation -- the same status
tools/known_answer.py records for its own registry (MSV_023). What would
change that: an expected value traced to a source outside this repository,
or to a second author.

NOT the instrument in sense-as-match/. That folder is a shape-space matcher
built to its own work order, with its own test_sense.py (SAM_011). This file
is about the root module only, which is a sense-at-match-site gate.

KNOWN STATE as committed: 18 of 18 module checks and 13 of 13 added cases (7 cases, 6 intake)
pass, 0 outside cases, state SELF-GRADED, exit 0.

History (KNOWN_RED.md sections 17-18; numbered 12-13 before renumbering). At dd0f794 this file ran 16 of 18:
the positive control and "score returns UNRATED on a failed gate" both
failed because gate() checked only that the TERM appeared whole-word, never
the BASIS. The author confirmed the control was correct and the gate was
missing a clause. Before the gate was touched, one added case (term
present, basis present, basis in a different paragraph) was written here
and run against the unpatched gate: FAIL, as predicted. gate() then gained
[CHOICE 6] (the basis must sit inside a match site, a paragraph holding the
term). After: 18/18 and 3/3.

PINNED SINCE (KNOWN_RED.md section 18): the two-paragraph cases that were
hand-checked only -- a term used in two paragraphs passes when either one
holds the basis, in both orders -- and the stated cost of [CHOICE 6]: a
sense stated ACROSS a paragraph break reads NOT_AT_MATCH_SITE. That last
pin records a known false refusal as current behaviour, so a repair turns
it red and forces section 18 to be corrected. It is the same text shape as
SPLIT_SITE_TEXT; the gate cannot tell them apart, and only the author's
intent differs.

OUTSIDE CASES. If sense_outside_cases.json sits beside this file, its cases
are run against gate() as it stands and reported in their own block. The
self-graded flag lifts on THOSE ONLY, and only when the file is admissible
([CHOICE T1], [CHOICE T2]) and every case agrees with the gate. With no file
the state prints SELF-GRADED, 0 outside cases. Nothing here authors one.

Stdlib only.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import sense_as_match  # noqa: E402


# ADDED CASE, outside the module's run_checks(). Term present, basis present,
# basis NOT at the match site: the two sit in different paragraphs. Written
# before gate() was patched, and run against the unpatched gate first, so its
# first result is on record (KNOWN_RED.md section 18). Same hand as the
# module: this does not lift the self-graded flag.
SPLIT_SITE_TEXT = ("His disrespect was noted.\n\n"
                   "Elsewhere: taking for granted, and thereby missing "
                   "information.")


def added_cases():
    rec = sense_as_match.SenseRecord(
        term="disrespect",
        sense="informational",
        sense_class="speaker_supplied",
        basis="taking for granted, and thereby missing information",
        locator="ops/CONTORT-AXIS.md:14",
    )
    term_present = sense_as_match.locate(SPLIT_SITE_TEXT, rec.term) is not None
    basis_present = rec.basis in SPLIT_SITE_TEXT
    ok, reason = sense_as_match.gate(rec, SPLIT_SITE_TEXT)
    return [
        ("[added] fixture: term present in text", term_present),
        ("[added] fixture: basis present in text", basis_present),
        ("[added] basis present but not at match site -> NOT_AT_MATCH_SITE",
         ok is False and reason == "NOT_AT_MATCH_SITE"),
    ] + two_paragraph_cases() + limit_cases()


def _record():
    return sense_as_match.SenseRecord(
        term="disrespect", sense="informational",
        sense_class="speaker_supplied",
        basis="taking for granted, and thereby missing information",
        locator="ops/CONTORT-AXIS.md:14")


# PINNED, formerly hand-checked only. A term used in two paragraphs passes
# when either paragraph holds the basis, in both orders; the basis alone,
# with no term anywhere, has no match site and refuses.
TWO_PARA_BASIS_SECOND = ("disrespect here.\n\n"
                         "His disrespect was taking for granted, and thereby "
                         "missing information.")
TWO_PARA_BASIS_FIRST = ("His disrespect was taking for granted, and thereby "
                        "missing information.\n\ndisrespect again.")
BASIS_NO_TERM = ("taking for granted, and thereby missing information.\n\n"
                 "No term here.")


def two_paragraph_cases():
    rec = _record()
    out = []
    for name, text, want in (
            ("[pinned] term in two paragraphs, basis in the second -> OK",
             TWO_PARA_BASIS_SECOND, (True, "OK")),
            ("[pinned] term in two paragraphs, basis in the first -> OK",
             TWO_PARA_BASIS_FIRST, (True, "OK")),
            ("[pinned] basis present, term absent -> NOT_AT_MATCH_SITE",
             BASIS_NO_TERM, (False, "NOT_AT_MATCH_SITE"))):
        out.append((name, sense_as_match.gate(rec, text) == want))
    return out


# PINNED LIMIT -- the stated cost of [CHOICE 6], recorded as current
# behaviour. The author states the sense across a paragraph break; the
# reading is correct and the gate refuses it. FALSE NOT_AT_MATCH_SITE. This
# text is the same shape as SPLIT_SITE_TEXT (term in paragraph 1, basis in
# paragraph 2); only intent differs, which the gate does not read. A repair
# that admits this case will also admit SPLIT_SITE_TEXT unless it reads
# something other than layout -- and either way this pin turns red, which
# is the point: KNOWN_RED.md section 18 must then be corrected.
CROSS_BREAK_SENSE = ("His disrespect was not ethical.\n\n"
                     "It was taking for granted, and thereby missing "
                     "information.")


def limit_cases():
    ok, reason = sense_as_match.gate(_record(), CROSS_BREAK_SENSE)
    return [("[pinned limit] sense stated across a paragraph break -> "
             "NOT_AT_MATCH_SITE (false refusal, cost of [CHOICE 6])",
             ok is False and reason == "NOT_AT_MATCH_SITE")]


# ---------------------------------------------------------------------------
# OUTSIDE CASES -- the only thing that can lift the self-graded flag.
#
# [CHOICE T1] Admissible file: a JSON object with a non-empty "author", a
#   non-empty "provenance", "authored_outside_module": true, and 3 to 5
#   "cases". Each case: "id", "text", "record" (the five SenseRecord
#   fields), "expect": {"ok": bool, "reason": str}, and a non-empty "why".
#   "reason" must be one gate() can return (INCOMPLETE matched as a prefix).
#   The author fields are DECLARED, not verified; this file cannot check who
#   wrote a case, only that the file says.
# [CHOICE T2] "at least one expected FAIL" is read as at least one case
#   with expect.ok == false -- a gate refusal the author expects. It is also
#   required that at least one case expect ok == true: a set of refusals
#   alone passes a gate that refuses everything, the constant-output failure
#   tools/known_answer.py refuses for the same reason.
# The flag lifts iff the file is admissible AND every case agrees with gate()
# on both ok and reason. A disagreement is reported as a finding and exits
# nonzero; the case is never edited to match.
# ---------------------------------------------------------------------------
OUTSIDE_FILE = os.path.join(HERE, "sense_outside_cases.json")
GATE_REASONS = ("OK", "NO_RECORD", "INCOMPLETE", "UNDECLARED_SENSE",
                "NO_SOURCE_TEXT", "NOT_AT_MATCH_SITE")
RECORD_FIELDS = ("term", "sense", "sense_class", "basis", "locator")


def _reason_known(r):
    return isinstance(r, str) and (r in GATE_REASONS or
                                   r.startswith("INCOMPLETE:"))


def admissible(doc):
    """List of reasons the file cannot lift the flag; [] when it can."""
    why = []
    if not isinstance(doc, dict):
        return ["not a JSON object"]
    for k in ("author", "provenance"):
        if not (isinstance(doc.get(k), str) and doc[k].strip()):
            why.append("missing or empty %r" % k)
    if doc.get("authored_outside_module") is not True:
        why.append("authored_outside_module is not true")
    cases = doc.get("cases")
    if not isinstance(cases, list):
        return why + ["cases is not a list"]
    if not 3 <= len(cases) <= 5:
        why.append("%d cases; 3 to 5 required [CHOICE T1]" % len(cases))
    oks = []
    for i, c in enumerate(cases):
        tag = "case %d" % i
        if not isinstance(c, dict):
            why.append(tag + " not an object"); continue
        for k in ("id", "text", "why"):
            if not (isinstance(c.get(k), str) and c[k].strip()):
                why.append("%s missing %r" % (tag, k))
        rec = c.get("record")
        if not (isinstance(rec, dict) and
                all(isinstance(rec.get(f), str) for f in RECORD_FIELDS)):
            why.append(tag + " record lacks one of " + ",".join(RECORD_FIELDS))
        exp = c.get("expect")
        if not (isinstance(exp, dict) and isinstance(exp.get("ok"), bool)
                and _reason_known(exp.get("reason"))):
            why.append(tag + " expect needs ok:bool and a gate reason")
        else:
            oks.append(exp["ok"])
    if oks and False not in oks:
        why.append("no case expects a refusal (ok false) [CHOICE T2]")
    if oks and True not in oks:
        why.append("no case expects a pass (ok true) [CHOICE T2]")
    return why


def run_outside(path=OUTSIDE_FILE):
    """(state, lines, n_disagree). state: SELF-GRADED / NOT_ADMISSIBLE /
    OUTSIDE_DISAGREES / OUTSIDE_AGREES. Only the last lifts the flag."""
    if not os.path.exists(path):
        return "SELF-GRADED", ["0 outside cases (no %s)"
                               % os.path.basename(path)], 0
    raw = open(path, "rb").read()
    lines = ["file %s sha256 %s" % (os.path.basename(path),
                                    hashlib.sha256(raw).hexdigest()[:16])]
    try:
        doc = json.loads(raw.decode("utf-8"))
    except ValueError as e:
        return "NOT_ADMISSIBLE", lines + ["unparseable: %s" % e], 0
    why = admissible(doc)
    if why:
        return "NOT_ADMISSIBLE", lines + ["  " + w for w in why], 0
    lines.append("author (declared): %s" % doc["author"])
    n_dis = 0
    for c in doc["cases"]:
        rec = sense_as_match.SenseRecord(
            **{f: c["record"][f] for f in RECORD_FIELDS})
        got = sense_as_match.gate(rec, c["text"])
        want = (c["expect"]["ok"], c["expect"]["reason"])
        agree = got == want
        n_dis += not agree
        lines.append("%s [outside] %s  want=%s got=%s"
                     % ("PASS" if agree else "FAIL", c["id"], want, got))
    state = "OUTSIDE_AGREES" if n_dis == 0 else "OUTSIDE_DISAGREES"
    return state, lines, n_dis


def intake_checks():
    """The intake's four states are reachable. Constructed files in a temp
    dir, by the same hand: they show the reader works and LIFT NOTHING --
    run_outside() is called on the real path only in main()."""
    rec = dict(term="disrespect", sense="informational",
               sense_class="speaker_supplied",
               basis="taking for granted, and thereby missing information",
               locator="x:1")

    def case(i, text, ok, reason):
        return {"id": "c%d" % i, "text": text, "record": rec,
                "expect": {"ok": ok, "reason": reason}, "why": "constructed"}
    good = [case(1, TWO_PARA_BASIS_SECOND, True, "OK"),
            case(2, SPLIT_SITE_TEXT, False, "NOT_AT_MATCH_SITE"),
            case(3, TWO_PARA_BASIS_FIRST, True, "OK")]
    base = {"author": "constructed", "provenance": "test_sense.py",
            "authored_outside_module": True}
    docs = {
        "agree": dict(base, cases=good),
        "disagree": dict(base, cases=good[:2] + [
            case(3, CROSS_BREAK_SENSE, True, "OK")]),
        "too_few": dict(base, cases=good[:2]),
        "no_refusal": dict(base, cases=[good[0], good[2], good[0]]),
        "not_outside": dict(base, authored_outside_module=False, cases=good),
    }
    got = {}
    d = tempfile.mkdtemp()
    for k, doc in docs.items():
        fp = os.path.join(d, k + ".json")
        with open(fp, "w") as f:
            json.dump(doc, f)
        got[k] = run_outside(fp)[0]
    got["absent"] = run_outside(os.path.join(d, "none.json"))[0]
    return [
        ("[intake] no file -> SELF-GRADED", got["absent"] == "SELF-GRADED"),
        ("[intake] admissible, all agree -> OUTSIDE_AGREES",
         got["agree"] == "OUTSIDE_AGREES"),
        ("[intake] cross-break case expected OK -> OUTSIDE_DISAGREES",
         got["disagree"] == "OUTSIDE_DISAGREES"),
        ("[intake] 2 cases -> NOT_ADMISSIBLE", got["too_few"] == "NOT_ADMISSIBLE"),
        ("[intake] no expected refusal -> NOT_ADMISSIBLE",
         got["no_refusal"] == "NOT_ADMISSIBLE"),
        ("[intake] authored_outside_module false -> NOT_ADMISSIBLE",
         got["not_outside"] == "NOT_ADMISSIBLE"),
    ]


def main() -> int:
    print("sense_as_match.py run_checks() -- self-graded, see header")
    rc = sense_as_match.run_checks()
    print("added cases (test_sense.py) -- self-graded, same hand")
    added = added_cases() + intake_checks()
    for name, ok in added:
        print(("PASS " if ok else "FAIL ") + name)
    n_fail = sum(1 for _, ok in added if not ok)
    print("%d/%d" % (len(added) - n_fail, len(added)))
    print("outside cases (sense_outside_cases.json) -- the only flag-lifter")
    state, lines, n_dis = run_outside()
    for ln in lines:
        print(ln)
    print("STATE: %s%s" % (state, "" if state == "OUTSIDE_AGREES"
                           else "  (self-graded flag stays)"))
    return 1 if (rc or n_fail or n_dis) else 0


if __name__ == "__main__":
    sys.exit(main())
