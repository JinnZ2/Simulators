#!/usr/bin/env python3
"""
naming -- S6 of the work order, enforced rather than remembered.

The order: do not use the two-word phrase naming an error-correcting
operation on a lean, anywhere in the tool or its output. That phrasing
asserts the lean WAS an error, which is a ruling the tool does not make.
The approved terms are "residual adjustment" for the operation and
"adjusted / unadjusted" for the state.

WHY THE PATTERNS ARE COMPOSED FROM TOKENS. A screen that stores the
banned phrase as a literal puts the phrase in the file it is screening,
and the file then has to skip a region of itself -- a hand-broken loop,
which this repository has recorded as UNI_010 and does not want a second
instance of. Composing the pattern from parts means the literal never
appears in this source at all, so `naming.py --source .` can scan its
own directory including itself with nothing excluded.

Note what is NOT banned. The single word "correction" is required by S5,
which names three fields with it. The order bans the two-word phrase and
its close forms, not the vocabulary of adjustment.

CC0. stdlib only. Parses under Python 3.9. ASCII only.
"""

import os
import re
import sys

# Composed, never written out. See the docstring.
_B = "b" + "ias"
_C = "correct"
_D = "de"

BANNED = [
    (r"\b%s[\s_-]*%sion\b" % (_B, _C), "%s %sion" % (_B, _C)),
    (r"\b%s[\s_-]*%sed\b" % (_B, _C), "%s %sed" % (_B, _C)),
    (r"\b%s[\s_-]*%sing\b" % (_B, _C), "%s %sing" % (_B, _C)),
    (r"\b%s[\s_-]*%s\b" % (_D, _B), "%s%s" % (_D, _B)),
    (r"\b%s[\s_-]*%sed\b" % (_D, _B), "%s%sed" % (_D, _B)),
]

APPROVED = {
    "operation": "residual adjustment",
    "state": "adjusted / unadjusted",
}

_PATTERNS = [(re.compile(p, re.I), label) for p, label in BANNED]


def hits(text):
    out = []
    for lineno, line in enumerate((text or "").splitlines(), 1):
        for pat, label in _PATTERNS:
            for m in pat.finditer(line):
                out.append((lineno, label, m.group(0), line.strip()[:70]))
    return out


def check(text):
    h = hits(text)
    return (not h), h


def report(text, label="text"):
    clean, h = check(text)
    if clean:
        return "%s: none of the %d screened forms present" % (label,
                                                              len(BANNED))
    lines = ["%s: %d screened form(s) present" % (label, len(h))]
    for lineno, form, got, line in h:
        lines.append("  line %d  %-18s %r | %s" % (lineno, form, got, line))
    return "\n".join(lines)


# The specification is not the tool. S6 has to name the phrase it bans,
# so the delivered order contains it by necessity, and a screen over this
# folder that did not say so would either fail forever or hide the
# exemption. It is named here, it is exactly one file, and the selftest
# checks BOTH that the scan is clean with it excluded AND that it is the
# only file that fires without the exclusion -- so the exemption is
# measured rather than assumed.
SPEC_FILES = ("WORK_ORDER.md",)


def scan_dir(directory, exts=(".py", ".md", ".json", ".txt"), exclude=()):
    """Every file under `directory` except the named exclusions."""
    out = {}
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
        for fn in sorted(files):
            if not fn.endswith(exts) or fn in exclude:
                continue
            p = os.path.join(root, fn)
            try:
                with open(p) as fh:
                    h = hits(fh.read())
            except (IOError, UnicodeDecodeError):
                continue
            if h:
                out[os.path.relpath(p, directory)] = h
    return out


def _selftest():
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-58s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("naming selftest")

    # Known signal: each banned form, assembled here the same way.
    for sep in (" ", "-", "_"):
        ck("the phrase with %r is caught" % sep,
           check("we applied %s%s%sion" % (_B, sep, _C))[0], False)
    ck("the -ed form is caught", check("%s-%sed values" % (_B, _C))[0], False)
    ck("the de- form is caught", check("%s%sed series" % (_D, _B))[0], False)

    # Known null: the approved vocabulary, and the words the order itself
    # requires.
    ck("'residual adjustment' passes",
       check("the residual adjustment was applied")[0], True)
    ck("'adjusted / unadjusted' passes",
       check("status: adjusted, then unadjusted")[0], True)
    ck("the field names S5 requires pass",
       check("correction_status correction_method correction_depth")[0], True)
    ck("the bare word 'correction' passes",
       check("a correction was recorded")[0], True)
    ck("the bare word for a lean passes",
       check("the %s of the estimator" % _B)[0], True)

    # Word boundaries, the UNI_009 failure.
    ck("'%ses' is not the phrase" % _B, check("%ses" % _B)[0], True)
    ck("'incorrect' is not the phrase", check("incorrect")[0], True)

    # The point of composing the patterns: this file can scan itself.
    here = os.path.dirname(os.path.abspath(__file__))
    ck("the tool is clean, with the specification excluded",
       sorted(scan_dir(here, exclude=SPEC_FILES)), [])
    ck("and the specification is the ONLY file that fires without it",
       sorted(scan_dir(here)), sorted(SPEC_FILES))
    ck("this file was itself scanned and is not exempt",
       os.path.basename(__file__) in SPEC_FILES, False)

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    if "--source" in sys.argv:
        d = sys.argv[sys.argv.index("--source") + 1]
        found = scan_dir(d, exclude=() if "--all" in sys.argv else SPEC_FILES)
        if not found:
            print("%s: clean across %d screened forms" % (d, len(BANNED)))
            sys.exit(0)
        for f, h in sorted(found.items()):
            print("%s: %d" % (f, len(h)))
            for lineno, form, got, line in h:
                print("  line %d  %-18s %r" % (lineno, form, got))
        sys.exit(1)
    data = sys.stdin.read()
    print(report(data, "stdin"))
    sys.exit(0 if check(data)[0] else 1)
