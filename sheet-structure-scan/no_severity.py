#!/usr/bin/env python3
"""
no_severity -- enforce the delivered output constraint.

The spec says: no interpretation, no severity language; the tool never
labels a site as an error. That is easy to write in a README and easy to
drift out of, one helpful sentence at a time. So it is a check that runs
over the emitted report rather than a paragraph asking the author to
remember.

WHAT THIS IS NOT. A keyword screen is stepped around by any paraphrase.
"This cell is wrong" is caught; "this cell will not survive contact with
the audit" is not. The same limit is on record three times elsewhere in
this repository under UNI_009, DF_010 and ACL_017, and it is stated here
at the top rather than at the bottom. What the screen buys is that the
FLUENT failure -- reaching for the ordinary vocabulary of severity
without noticing -- is the one it catches, and that is the one that
happens.

Word boundaries are load-bearing: a bare substring scan fires on
"terror" for "error" and on "misfired" for "fire". That failure is on
record here too.

CC0. stdlib only. Parses under Python 3.9.
"""

import re
import sys

# Words that grade a site. The tool reports structure; grading is the
# operator's.
SEVERITY = [
    "error", "errors", "erroneous", "warning", "warnings", "critical",
    "severe", "severity", "fatal", "bad", "wrong", "incorrect", "invalid",
    "broken", "risk", "risks", "risky", "danger", "dangerous", "issue",
    "issues", "problem", "problems", "violation", "violations", "violates",
    "suspicious", "smell", "smells", "flaw", "flaws", "defect", "defects",
    "unsafe", "alarm", "alert", "alerts", "offender", "offending",
    "bug", "bugs", "faulty", "corrupt", "corrupted",
]

# Words that do the operator's reading for them.
INTERPRETATION = [
    "should", "shouldn", "must", "ought", "recommend", "recommended",
    "recommendation", "advise", "advisable", "obviously", "clearly",
    "evidently", "surely", "certainly", "indicates", "implies", "means",
    "suggests", "proves", "confirms", "likely", "unlikely", "probably",
    "presumably", "needs", "fix", "fixes", "repair", "improve", "improved",
    "better", "worse", "worst", "best",
]

BANNED = SEVERITY + INTERPRETATION

_PATTERNS = [(w, re.compile(r"\b%s\b" % re.escape(w), re.I)) for w in BANNED]


def hits(text):
    """Every banned word present, with the line it is on."""
    out = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for word, pat in _PATTERNS:
            for m in pat.finditer(line):
                out.append((lineno, word, line.strip()))
    return out


def check(text):
    """(clean, hits). Never raises: the caller decides what to do."""
    h = hits(text)
    return (not h), h


def report(text, label="report"):
    clean, h = check(text)
    if clean:
        return "%s: no severity or interpretation vocabulary (%d words screened)" \
            % (label, len(BANNED))
    lines = ["%s: %d screened word(s) present" % (label, len(h))]
    for lineno, word, line in h:
        lines.append("  line %d  %-14s | %s" % (lineno, word, line[:70]))
    return "\n".join(lines)


def _selftest():
    """Two arms. A screen that never fires passes every one-arm test."""
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-52s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("no_severity selftest")

    # KNOWN NULL: text the tool actually emits.
    null_arm = (
        "rank  site           kind             absent\n"
        "3     Inputs!B9      CONSTANT_NUMBER  unit,date,sample_size\n"
        "0     Summary!B2     DERIVED          -\n"
        "labels grouped: 7   labels differing: 2\n"
        "neighborhood radius 2, clipped sides reported per row\n")
    ck("known null is clean", check(null_arm)[0], True)

    # KNOWN SIGNAL: one planted word per class. A screen that returns
    # clean on everything passes the null arm alone, which is why this
    # arm exists.
    ck("severity word caught", check("this cell is an error")[0], False)
    ck("interpretation word caught", check("the operator should recheck")[0], False)
    ck("grading word caught", check("a critical site")[0], False)

    # Word boundaries. Substring scanning fires on both of these.
    ck("terror is not error", check("the terror of the deep")[0], True)
    ck("mustard is not must", check("mustard and cress")[0], True)
    ck("bustle is not bug", check("bustle")[0], True)

    # The spec's own vocabulary must survive the screen, or the screen
    # forbids the tool from describing itself.
    ck("'flag' is permitted", check("flag any label whose cells differ")[0], True)
    ck("'missing' is permitted", check("report what is missing")[0], True)
    ck("'absent' is permitted", check("absent companion")[0], True)

    n = len(SEVERITY) + len(INTERPRETATION)
    ck("both classes populated", (len(SEVERITY) > 0, len(INTERPRETATION) > 0),
       (True, True))
    print("  %d words screened" % n)
    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    data = sys.stdin.read()
    print(report(data, "stdin"))
    sys.exit(0 if check(data)[0] else 1)
