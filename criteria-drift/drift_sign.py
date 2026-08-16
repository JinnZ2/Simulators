"""
drift_sign.py -- the drift metric is unsigned, and the decision rule reads
the sign.

CC0-1.0. Standard library only. Deterministic. Imports the delivered engine;
modifies nothing.

THE DECISION RULE, from README.md
---------------------------------
    beta1 > 0, significant : criteria inflation explains some reported
                             improvement
    beta1 ~ 0              : improvement is orthogonal to criteria drift
    beta1 < 0              : stricter criteria are masking real gains

Three verdicts, separated by the SIGN of a slope on `composite_drift`.

THE METRIC
----------
Every primitive in DriftEngine returns a non-negative distance:

    _str_drift      1 - jaccard(tokens)         in [0, 1]
    _list_drift     1 - jaccard(sets)           in [0, 1]
    _dict_drift     fraction of keys changed    in [0, 1]
    _numeric_drift  abs(v2 - v1) / max(...)     in [0, 1]

So a version that WIDENS the boundary and one that NARROWS it both push
composite_drift up. The slope of an improvement series on a non-negative
regressor cannot distinguish "the ruler stretched" from "the ruler
tightened" -- it can only report whether score changes happen to be larger
when the criteria moved a lot, in either direction.

Sections 1-4 measure that on the delivered engine. Section 5 is what a
signed metric would need, per field, and where the sign is unrecoverable.
"""

from __future__ import annotations

import sys

from drift import DriftEngine
from schema import CriteriaVersion, Frame

RULE = "=" * 72
E = DriftEngine()

BASE = dict(
    boundary="pass at 1 on held-out unit tests",
    horizon="single submission",
    who_counts="the benchmark authors",
    sign_source="set by the benchmark authors",
    logic="classical bivalent",
    observer_access="verified",
)


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def cv(vid, dims=None, weights=None, exemplars=100, **overrides):
    f = dict(BASE)
    f.update(overrides)
    return CriteriaVersion(
        artifact_name="X", version_id=vid, timestamp="2024-01-01T00:00:00Z",
        frame=Frame(**f),
        rubric_dimensions=dims if dims is not None else ["correctness"],
        rubric_weights=weights if weights is not None else {"correctness": 1.0},
        exemplar_count=exemplars,
    )


# ---------------------------------------------------------------------------


def check_widen_narrow() -> None:
    section("1  widening and narrowing both read as positive drift")

    a = cv("a")
    wider = cv("wider",
               boundary="pass at 1 on held-out unit tests plus style and "
                        "documentation")
    narrower = cv("narrower", boundary="pass at 1")

    print("  base      %s" % BASE["boundary"])
    print("  wider     %s" % wider.frame.boundary)
    print("  narrower  %s" % narrower.frame.boundary)
    print()
    print("    base -> wider     boundary drift %.4f  composite %.4f"
          % (E.compute_pair(a, wider)["boundary"],
             E.compute_pair(a, wider)["composite"]))
    print("    base -> narrower  boundary drift %.4f  composite %.4f"
          % (E.compute_pair(a, narrower)["boundary"],
             E.compute_pair(a, narrower)["composite"]))
    print()
    print("  Both positive. The magnitudes differ, and the difference is a")
    print("  token-count artifact -- `narrower` deleted more words than")
    print("  `wider` added -- not a reading of direction. A narrowing that")
    print("  happened to be verbose would score below a widening that was")
    print("  terse.")


def check_numeric() -> None:
    section("2  the one numeric field discards its sign explicitly")

    print("  exemplar_count is an integer. `_numeric_drift` takes abs():\n")
    for v1, v2 in ((100, 1000), (1000, 100), (100, 120), (120, 100)):
        print("      %5d -> %-5d  %.4f" % (v1, v2, E._numeric_drift(v1, v2)))
    up = E._numeric_drift(100, 1000)
    down = E._numeric_drift(1000, 100)
    print()
    print("  100 -> 1000 and 1000 -> 100 are identical: %s" % (up == down))
    print()
    print("  A test set growing tenfold and a test set shrinking tenfold are")
    print("  different events for the hypothesis under test, and the field")
    print("  that could report which one happened is the only field with an")
    print("  unambiguous direction available.")


def check_ordinal() -> None:
    section("3  observer_access is an ordinal compared as a string")

    print("  schema.py declares the legal values, and they are ordered:\n")
    print("      unknown  <  partial  <  verified\n")
    print("  `_str_drift` compares them as token sets:\n")
    for x, y in (("unknown", "partial"), ("partial", "verified"),
                 ("unknown", "verified"), ("verified", "unknown"),
                 ("verified", "partial")):
        print("      %-9s -> %-9s  %.1f" % (x, y, E._str_drift(x, y)))
    print()
    print("  Every transition scores 1.0. Gaining verification and losing")
    print("  it are the same number, and a one-step move is the same number")
    print("  as a two-step move.")
    print()
    print("  This is the SCALAR DEMAND mechanism from ../uninstrumented/")
    print("  turned inside out: not a function collapsed to a number, but an")
    print("  ordered scale collapsed to a nominal one. Same loss, opposite")
    print("  direction -- the structure was there and the instrument does")
    print("  not read it.")


def check_free_text() -> None:
    section("4  free-text fields drift on rewording")

    a = cv("a")
    reworded = cv("reworded",
                  boundary="on held-out unit tests, pass at 1")
    print("  A  %s" % a.frame.boundary)
    print("  B  %s" % reworded.frame.boundary)
    print()
    m = E.compute_pair(a, reworded)
    print("    boundary drift  %.4f" % m["boundary"])
    print("    composite       %.4f" % m["composite"])
    print()
    print("  Same clause, reordered. Token Jaccard is order-free, so this is")
    print("  the words that changed rather than the order -- 'pass at 1 on")
    print("  held-out unit tests' against 'on held-out unit tests, pass at")
    print("  1' differ by punctuation attaching to a token.")
    print()
    print("  ../declared-frame/ DF_003 recorded exact string equality as")
    print("  UNDER-matching in the comparability checker -- two frames that")
    print("  mean the same thing reported as different. Here the same")
    print("  free-text field is the MEASURAND, so the same property becomes")
    print("  a positive reading on the quantity being regressed. A checker")
    print("  that under-matches refuses a comparison; a metric that")
    print("  under-matches emits drift.")


def check_what_signed_needs() -> None:
    section("5  what a signed metric needs, field by field")

    print("  %-18s %-14s" % ("field", "sign"))
    print("  " + "-" * 68)
    rows = (
        ("exemplar_count", "available",
         "drop abs(): (v2 - v1) / max(...). One character."),
        ("observer_access", "available",
         "rank unknown=0, partial=1, verified=2; drift = rank2 - rank1."),
        ("rubric_dimensions", "available",
         "|added| - |removed| rather than Jaccard distance."),
        ("rubric_weights", "available",
         "sum of signed weight changes on the shared keys."),
        ("boundary", "NOT from text",
         "widening vs narrowing is a semantic judgement. Needs a "
         "declared field -- `direction: widened|narrowed|lateral` -- "
         "supplied by whoever made the version."),
        ("horizon", "NOT from text",
         "same. A longer horizon is not obviously 'more' or 'less'."),
        ("who_counts", "NOT from text", "same."),
        ("sign_source", "not applicable",
         "a change of authority has no natural direction."),
        ("logic", "not applicable", "same."),
    )
    for f, sign, how in rows:
        print("  %-18s %-14s" % (f, sign))
        for line in _wrap(how, 6, 60):
            print(line)

    print()
    print("  Four of nine are signable from the data already stored, and")
    print("  three of those are one-line changes. Three more need a declared")
    print("  field, because widening and narrowing a free-text boundary is a")
    print("  judgement the text does not contain -- which is the")
    print("  ../declared-frame/ DF_007 shape: the block records declarations")
    print("  and nothing in it evaluates.")
    print()
    print("  Two are genuinely directionless and should stay unsigned, and")
    print("  saying so is worth more than forcing a sign on them.")
    print()
    print("  Until then the honest reading of a positive beta1 is:")
    print()
    print("      score changes are larger when the criteria moved a lot,")
    print("      in either direction")
    print()
    print("  which is a real finding and is not the one the README states.")


def _wrap(text, indent, width=60):
    words, out, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            out.append(" " * indent + cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(" " * indent + cur)
    return out


def main() -> int:
    print()
    print("DRIFT SIGN -- can the metric carry the hypothesis?")
    print("subject: DriftEngine, delivered")

    check_widen_narrow()
    check_numeric()
    check_ordinal()
    check_free_text()
    check_what_signed_needs()

    section("READING")
    print("""
  The README separates three verdicts by the sign of a slope on
  composite_drift, and every primitive in DriftEngine returns a
  non-negative distance. Widening and narrowing both push drift up;
  exemplar_count 100 -> 1000 and 1000 -> 100 are byte-identical at 0.9;
  every observer_access transition scores 1.0 including the loss of
  verification.

  So the instrument cannot distinguish the two readings it exists to
  distinguish. What a positive slope actually says is that score changes
  are larger when the criteria moved a lot, in either direction -- a real
  finding, and not the stated one.

  Four of nine fields are signable from data already in the schema, three
  of them as one-line changes. Three need a declared `direction` field,
  because whether a free-text boundary widened or narrowed is a judgement
  the text does not contain. Two have no natural direction and should stay
  unsigned.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
