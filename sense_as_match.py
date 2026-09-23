"""
sense_at_match.py — a term used to score anything carries the sense it was
read in, at the site where it was matched, or the scoring function returns
UNRATED.

The sourced.py move applied to a word rather than a value.

Registered and not built at:
    #42  a grading whose predicate is polysemous carries the sense it used,
         or returns UNRATED
    #48  a mechanical edit keyed on a polysemous term must not fire without
         the sense being checked at the match site
    #50  neither reaches the real gap -- a measured false positive has no
         path into the next instrument

WHAT THIS DOES NOT DO
---------------------
It does not read text for sense. It holds no lexicon. It does not check the
locator against the filesystem. It does not detect sense collision within a
document -- that requires reading the document.

And: it does not prevent the corpus default from being USED. A caller may
declare sense_class="corpus_default" and pass the gate. The failure this
file prevents is using the default SILENTLY. A declared default is a finding
a second party can dispute. An undeclared one is a defect no second party
can see.

Stdlib only. Library module: refuses --selftest (exit 2). Choices printed
by --choices.
"""

import argparse
import sys
from dataclasses import dataclass

UNRATED = "UNRATED"

SENSE_CLASSES = (
    "corpus_default",     # the sense the term carries in the training corpus
    "speaker_supplied",   # the sense the speaker stated, where we can point at
    "contested",          # two parties reading the term in different senses
    "undefined",          # not declared. Not "no sense": not declared.
)


@dataclass(frozen=True)
class SenseRecord:
    term: str
    sense: str
    sense_class: str
    basis: str       # the literal text the sense came from
    locator: str     # where that text is, so a second party can go there

    def missing(self):
        out = []
        for name in ("term", "sense", "basis", "locator"):
            v = getattr(self, name)
            if v is None or (isinstance(v, str) and not v.strip()):
                out.append(name)
        if self.sense_class not in SENSE_CLASSES:
            out.append("sense_class")
        return tuple(out)


def locate(text, term):
    """At the match site. Whole-word, case-sensitive. Not stemmed, not
    lemmatized -- a matcher that decides sense by morphology is the
    failure this file exists to prevent."""
    if not text or not term:
        return None
    idx = text.find(term)
    while idx >= 0:
        before = text[idx - 1] if idx > 0 else " "
        after = text[idx + len(term)] if idx + len(term) < len(text) else " "
        if not (before.isalnum() or before == "_") and \
           not (after.isalnum() or after == "_"):
            return (idx, idx + len(term))
        idx = text.find(term, idx + 1)
    return None


def gate(record, source_text):
    """Returns (ok, reason). source_text is required: a caller who does not
    have the text the sense came from does not have a sense to score with."""
    if not isinstance(record, SenseRecord):
        return (False, "NO_RECORD")
    missing = record.missing()
    if missing:
        return (False, "INCOMPLETE:" + ",".join(missing))
    if record.sense_class == "undefined":
        return (False, "UNDECLARED_SENSE")
    if source_text is None:
        return (False, "NO_SOURCE_TEXT")
    if locate(source_text, record.term) is None:
        return (False, "NOT_AT_MATCH_SITE")
    return (True, "OK")


def score(value, record, source_text):
    ok, _ = gate(record, source_text)
    if not ok:
        return UNRATED
    return value


_CHOICES = (
    ("1", "SENSE_CLASSES is a closed four-tuple. A fifth class is a code "
          "change, a diff, a review -- not a data file."),
    ("2", "locate() is whole-word and case-sensitive. Not stemmed, not "
          "lemmatized: a matcher that decides sense by morphology is the "
          "failure this file exists to prevent."),
    ("3", "sense_class == 'undefined' returns UNRATED and is never "
          "defaulted to corpus_default. The default IS the failure."),
    ("4", "UNRATED is a third value. Nothing downstream may test it as "
          "falsy, and no path in this file returns 0 or None in its place."),
    ("5", "source_text is a required positional argument to gate() and "
          "score(). A caller who does not have the text the sense came "
          "from does not have a sense to score with."),
)


def run_checks():
    checks = []

    def c(name, cond):
        checks.append((name, bool(cond)))

    # POSITIVE CONTROL, FIRST. A gate that never fires is not a gate.
    bad = SenseRecord(
        term="disrespect",
        sense="informational",
        sense_class="speaker_supplied",
        basis="taking for granted, and thereby missing information",
        locator="ops/CONTORT-AXIS.md:14",
    )
    ok, reason = gate(bad, "The word disrespect appears here.")
    c("positive control fires on a term not at the match site",
      ok is False and reason == "NOT_AT_MATCH_SITE")

    good_text = ("His disrespect was not ethical. It was taking for "
                 "granted, and thereby missing information.")
    ok, reason = gate(bad, good_text)
    c("a located record passes", ok is True and reason == "OK")

    for field_name in ("term", "sense", "basis", "locator"):
        d = dict(term="x", sense="y", sense_class="speaker_supplied",
                 basis="z", locator="w")
        d[field_name] = ""
        ok, reason = gate(SenseRecord(**d), "x y z w")
        c("missing %s names the field" % field_name,
          ok is False and reason.startswith("INCOMPLETE:") and
          field_name in reason)

    ok, reason = gate(
        SenseRecord(term="x", sense="y", sense_class="vibes",
                    basis="z", locator="w"), "x y z w")
    c("out-of-vocabulary sense class is refused, named",
      ok is False and "sense_class" in reason)

    ok, reason = gate(
        SenseRecord(term="x", sense="y", sense_class="undefined",
                    basis="z", locator="w"), "x y z w")
    c("undefined sense is refused, not defaulted",
      ok is False and reason == "UNDECLARED_SENSE")

    ok, _ = gate(
        SenseRecord(term="market", sense="spot market",
                    sense_class="corpus_default",
                    basis="the market cleared at noon",
                    locator="x.md:1"),
        "the market cleared at noon")
    c("a DECLARED corpus_default passes -- the gate refuses silence, "
      "not the corpus sense", ok is True)

    c("score returns UNRATED on a failed gate",
      score(1.0, bad, "The word disrespect appears here.") == UNRATED)
    c("score returns the value on a passed gate",
      score(1.0, bad, good_text) == 1.0)

    c("UNRATED is not 0", UNRATED != 0)
    c("UNRATED is not the empty string", UNRATED != "")
    c("UNRATED is not the string '0'", UNRATED != "0")
    c("UNRATED is not None", UNRATED is not None)

    ok, reason = gate(bad, None)
    c("absent source text is a named refusal, not a silent skip",
      ok is False and reason == "NO_SOURCE_TEXT")

    c("locate() refuses a substring match",
      locate("a classless act", "class") is None)
    c("locate() matches a whole word",
      locate("a class act", "class") == (2, 7))

    failed = [n for n, ok in checks if not ok]
    total = len(checks)
    for n, ok in checks:
        print(("PASS " if ok else "FAIL ") + n)
    print("%d/%d" % (total - len(failed), total))
    return 0 if not failed else 1


def main(argv):
    ap = argparse.ArgumentParser(prog="sense_at_match.py")
    ap.add_argument("--choices", action="store_true",
                    help="print every [CHOICE n] at the site it takes effect")
    ap.add_argument("--selftest", action="store_true",
                    help="not accepted here; run test_sense.py instead")
    args = ap.parse_args(argv)

    if args.selftest:
        print("this is a library module; run test_sense.py", file=sys.stderr)
        return 2

    if args.choices:
        for cid, text in _CHOICES:
            print("[CHOICE %s] %s" % (cid, text))
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
