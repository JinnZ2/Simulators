"""
layer_zero.py -- the block declares frames and has no term outside them.

CC0-1.0. Standard library only. Deterministic. Imports check_frame; does not
modify it.

THE SPLIT
---------
    LAYER 0   physics -- applies to everything, including the reasoner
              unauthored, not switchable
              the fallback when a shape does not resolve

    LAYER 1   cultural frames -- many, each internally valid
              switchable, declared, none privileged
              contained by layer 0, not parallel to it

`THE_DECLARED_FRAME.md` is a layer-1 instrument and a good one: it makes the
frame explicit, it refuses to rank frames, and it reports a difference
between two of them as a finding rather than as one side being wrong.

That refusal is correct WITHIN layer 1 and it is the whole capability of the
tool. There is no term in the block that is not switchable, so two frames
that disagree can be reported as disagreeing and nothing adjudicates. This
is not a defect of the six fields -- it is the boundary of what a
frame-declaration instrument can do, and it is exactly the shape the layer
split names:

    layer 1 only   every frame is a peer, no term outside them to
                   adjudicate, drift with whichever frame dominates
    layer 0 present conflicts route down and terminate on something no
                   frame authored

WHAT THIS CHECKS
    1  every field in the block is layer 1. Demonstrated by exhibiting two
       frames that differ on a field whose value is settled by conservation
       and getting the same verdict as two frames differing on a convention.
    2  what a layer-0 field would have to look like to be checkable rather
       than declared -- and why it cannot be a seventh free-text field.
"""

from __future__ import annotations

import io
import contextlib
import json
import os

import check_frame

HERE = os.path.dirname(os.path.abspath(__file__))
RULE = "=" * 72


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def load(name: str) -> dict:
    with open(os.path.join(HERE, "frames", name)) as fh:
        return json.load(fh)["frame"]


def verdict(a: dict, b: dict) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        check_frame.compare(a, b)
    for line in buf.getvalue().splitlines():
        t = line.strip()
        for tag in ("DIRECTLY COMPARABLE on all", "NOT DIRECTLY COMPARABLE",
                    "UNDETERMINED"):
            if t.startswith(tag):
                return tag
    return "(none)"


# ---------------------------------------------------------------------------


def check_all_layer_one() -> None:
    section("1  every field in the block is switchable")

    base = load("panel_conversion.json")

    # (a) two frames differing on a pure convention -- who is counted.
    conv = dict(base)
    conv["who_counts"] = ("the operator only; upstream labour and downstream "
                          "disposal are outside the accounting")

    # (b) two frames differing on a quantity that is NOT a convention: one
    # side's boundary excludes an energy input that physically crossed it.
    # A closed budget and an open one are not two valid readings of the same
    # accounting -- one of them does not conserve.
    phys = dict(base)
    phys["boundary"] = ("photon capture to product, with the fabrication "
                        "energy input counted as zero rather than excluded")

    print("  A  differ on a convention (who_counts):")
    print("       %s\n" % verdict(base, conv))
    print("  B  differ on a boundary that does not close (an input that")
    print("     crossed it entered the budget as zero):")
    print("       %s\n" % verdict(base, phys))

    same = verdict(base, conv) == verdict(base, phys)
    print("  same verdict for both: %s" % same)
    print()
    if same:
        print("  The tool reports B exactly as it reports A: two declared")
        print("  frames that differ. It has no way to say that one of them")
        print("  fails to conserve, because conservation is not one of the")
        print("  six fields and there is nothing in the block that is not")
        print("  a declaration.")
        print()
        print("  That is the layer-1-only reading arriving in a tool: every")
        print("  frame is a peer, and 'this frame is coherent internally and")
        print("  does not match the shape' is not a statable verdict.")


def check_what_a_layer_zero_field_needs() -> None:
    section("2  a seventh free-text field would not fix it")

    print("  The obvious repair is a seventh field. It does not work, and")
    print("  the reason is the same reason the other six work:\n")

    print("  %-22s %s" % ("field", "checked by"))
    print("  " + "-" * 56)
    for f in check_frame.FIELDS:
        print("  %-22s %s" % (f, "the reader; the tool compares strings"))
    print("  %-22s %s" % ("(proposed) layer_0", "??"))
    print()
    print("  Every existing field is a DECLARATION, and comparability is")
    print("  string equality over declarations. A layer-0 field would have")
    print("  to be the one entry the tool can evaluate rather than compare --")
    print("  otherwise two frames declaring incompatible physics come back")
    print("  NOT DIRECTLY COMPARABLE, which is where they already are.")
    print()
    print("  Shape that would work, and it is not a field:\n")
    print("      an inputs/outputs list per frame, with units, and one")
    print("      check -- does the budget close")
    print()
    print("  That is two numbers and a subtraction, and it is the same shape")
    print("  as ../reasoning-gate/ G-RES: a pair the author declares and the")
    print("  tool arithmetically checks, not a sentence it string-matches.")
    print("  A frame whose budget does not close is not one of several valid")
    print("  readings; it is refused, and the refusal comes from a term the")
    print("  frame did not author.")
    print()
    print("  K18 in ../measurement-fork/ specifies precisely this audit --")
    print("  name every input and every disposal path, which are inside the")
    print("  boundary, which outside, and who set the line. It sits there as")
    print("  a widen move against a design. Here it would be a check.")


def main() -> None:
    print()
    print("LAYER 0 AND LAYER 1 IN THE DECLARED-FRAME BLOCK")
    print("subject: check_frame.compare(), unmodified")

    check_all_layer_one()
    check_what_a_layer_zero_field_needs()

    section("READING")
    print("""
  The six fields are all layer 1 and the tool is right not to rank them.
  Two frames that differ on who_counts are two accountings, and neither is
  wrong.

  The cost is that a frame whose budget does not close gets the same
  verdict as a frame that merely counts different people. Nothing in the
  block is unswitchable, so nothing adjudicates, and the position "this
  frame is internally coherent and does not match the shape" cannot be
  stated by the tool that exists to make frames comparable.

  A seventh free-text field inherits the same problem, because
  comparability here is string equality over declarations. The repair is
  an evaluated term rather than a compared one: inputs and outputs with
  units, and one check for closure. Two numbers and a subtraction, the
  G-RES shape.
""")


if __name__ == "__main__":
    main()
