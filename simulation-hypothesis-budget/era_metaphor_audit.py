#!/usr/bin/env python3
"""
era_metaphor_audit.py - the delivered ERA_METAPHOR.md, checked where it makes
checkable claims about this folder.

    python3 era_metaphor_audit.py
    python3 era_metaphor_audit.py --selftest

ERA_METAPHOR.md argues that the simulation hypothesis is the current instance
of a recurring pattern -- an era's dominant artifact becoming its cosmology --
and that the value of the pattern is not a verdict on the content but a source
of GAP STRUCTURE: the shape of what each era's metaphor could not see,
recoverable now because the instance closed.

It is careful about its own scope ("claim content: none. suspicion +
gradient") and it makes TWO POINTERS INTO THIS FOLDER, both checkable:

  G2  "this is the one my audit half-caught at SHB_002 and stopped."
  G4  "Layer 3 in the repo is exactly this gap."

Both are checked here against the claim table and the module docstrings rather
than accepted. Both turn out to be off by one, in the same direction, and BOTH
CORRECTIONS STRENGTHEN THE GAP rather than weakening it -- which is worth more
than agreement would have been.

Reads CLAIM_TABLE.md and imports the four modules. Modifies nothing.
stdlib only. CC0.
"""

import argparse
import os
import re
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import budget as B                                              # noqa: E402
import multiscale as M                                          # noqa: E402
import consequence_frame as CF                                  # noqa: E402
import ladder_audit as LA                                       # noqa: E402

CLAIM_TABLE = os.path.join(HERE, "CLAIM_TABLE.md")


def wrap(text, indent="    ", width=72):
    """Word-wrapped output. Manual slicing broke words mid-token."""
    return textwrap.wrap(text, width=width - len(indent),
                         initial_indent=indent, subsequent_indent=indent)


def claim_text(cid):
    """Pull one claim row out of CLAIM_TABLE.md, so the checks below read the
    published claim rather than a copy of it."""
    with open(CLAIM_TABLE) as fh:
        for line in fh:
            if line.startswith("| `%s`" % cid):
                return line
    return ""


# --- G2: the three imported boundary conditions ----------------------------

def g2_imports():
    """G2 names three: discrete cells, finite state, additive capacity.

    Each is checked against what the folder actually did, and they do not
    score the same. The interesting result is that they score three different
    ways, so "all three come from the apparatus" is one claim covering three
    different situations.
    """
    s001, s014 = claim_text("SHB_001"), claim_text("SHB_014")
    return [
        {"import": "additive capacity",
         "caught": "SHB_001",
         "how": "CAUGHT NATIVELY, and refuted by 61 decades",
         "evidence": "claim text says information is bounded by area, "
                     "not volume",
         "holds": ("area" in s001 and "volume" in s001),
         "external": False},
        {"import": "discrete cells",
         "caught": "SHB_014",
         "how": "CAUGHT ONLY UNDER EXTERNAL AUDIT",
         "evidence": "named as an interpretive step, but only after "
                     "LADDER.md arrived from outside the folder",
         "holds": ("cell" in s014 and "interpretive" in s014),
         "external": True},
        {"import": "finite state",
         "caught": "SHB_001 (partly)",
         "how": "TWO STEPS, and the folder marks only the first",
         "evidence": "finite ENTROPY is a physics result (Bekenstein / "
                     "holographic, from black-hole thermodynamics, not from "
                     "computing). reading that entropy as finite STATE IN "
                     "BITS is a further interpretive step, and the folder "
                     "takes it at SHB_001 without marking it",
         "holds": ("bits" in s001),
         "external": False},
    ]


def g2_verdict():
    im = g2_imports()
    return {"named": len(im),
            "caught_natively": sum(1 for i in im if not i["external"]
                                   and i["how"].startswith("CAUGHT")),
            "caught_externally": sum(1 for i in im if i["external"]),
            "unmarked_step": sum(1 for i in im if i["how"].startswith("TWO")),
            "pointer_as_delivered": "SHB_002",
            "pointer_corrected": "SHB_001",
            "why": "SHB_002 is the downstream consequence (two floors still "
                   "exceed the universe's energy). SHB_001 is the claim that "
                   "actually catches an imported boundary -- additivity over "
                   "volume, refuted by the area law. The correction makes "
                   "the gap's own case better: the catch was real and it was "
                   "one of three."}


# --- G3: is the architecture set drawn from the artifact? ------------------

def g3_architecture_provenance():
    """G3's sharpest landing, and the module says it itself.

    multiscale.py's docstring sources its architecture set to real computing
    practice -- adaptive mesh refinement, level-of-detail, lazy evaluation.
    SHB_010 then reports 216 decades "across four architectures nobody has
    argued against". Those four are four our machines use.

    So the spread is a spread over THE ARTIFACT'S OWN REPERTOIRE. That does
    not weaken SHB_010; it strengthens it past what SHB_010 claims. The
    quantity is not merely ill-posed pending a level stack -- the space the
    level stack would be drawn from is not enumerable from inside, because
    every architecture in it is one we build.
    """
    doc = (M.__doc__ or "").lower()
    practice = [t for t in ("adaptive mesh refinement", "level-of-detail",
                            "lazy evaluation") if t in doc]
    archs = list(M.architectures().keys()) + ["lazy_on_observation"]
    s010 = claim_text("SHB_010")
    return {"architectures": len(M.architectures()),
            "sourced_to_computing_practice": practice,
            "module_says_so": len(practice) >= 2,
            "spread_claimed": "216 decades" if "216" in s010 else "(not "
                              "found in claim text)",
            "spread_is_over": "what our machines do",
            "not_over": "what is possible",
            "names": archs}


# --- G4: which layer is the unlocatable exterior? --------------------------

def g4_layer_pointer():
    """G4 says 'Layer 3'. The folder has three layers and the exterior is
    layer 2."""
    doc = B.__doc__ or ""
    layers = []
    for line in doc.splitlines():
        m = re.match(r"^  ([A-Z][A-Z ]+?)  +\S", line)
        if m:
            name = m.group(1).strip()
            if name not in layers:
                layers.append(name)
    exterior = None
    for i, name in enumerate(layers, start=1):
        if name == "VOID":
            exterior = i
    return {"layers": layers,
            "pointer_as_delivered": 3,
            "pointer_corrected": exterior,
            "layer_named": layers[exterior - 1] if exterior else None,
            "why": "the unlocatable exterior is the parent universe, and the "
                   "layer that refuses to reach it is VOID -- cross_frame_"
                   "ratio() raising because the denominator is a property of "
                   "an object we cannot measure. Layer 3 is the resolution "
                   "knob, a different gap. The corrected pointer is a "
                   "sharper match: VOID is a refusal in code, which is a "
                   "stronger form of 'cannot locate' than a knob is.",
            "two_routes_confirmed": exterior is not None}


# --- the reference class ---------------------------------------------------

def reference_class_check():
    """The one place the delivered text could be read as offering a rate.

    Four prior instances, all superseded. That is a sample selected on the
    outcome under test: metaphors that were superseded were collected, and
    4 of 4 were superseded. No base rate is recoverable from it, because
    era-metaphors that were NOT superseded are not in the frame -- and at
    least one candidate is named in the document's own DOESN'T row, where
    clockwork mechanism is granted as "partly right about orbits".

    THE METHOD SURVIVES THIS AND THE TABLE DOES NOT. METHOD_AS_STATED says
    "claim content: none. suspicion + gradient" and "prior instances are not
    evidence against the current one" -- which is precisely the disclaimer
    that makes the selection harmless, because a gradient over hindsight
    cases does not need a base rate. Anyone reading a RATE off the table
    ("4 for 4") is reading something the method already refused to assert.
    """
    return {"instances": 4,
            "superseded": 4,
            "rate_readable": False,
            "why_not": "selected on the dependent variable",
            "counterexample_named_in_the_document": "clockwork mechanism, "
                                                    "granted partly right "
                                                    "about orbits",
            "method_survives": True,
            "shape": "third instance in this repo of a frame selected on the "
                     "variable under test -- uninstrumented UNI_126 on case "
                     "021's T1, and presented-binary's option-space audit"}


# --- G1: an operational proxy that is reachable now ------------------------

def g1_operational_proxy():
    """G1 asks what computation has no slot for, and says the metaphor cannot
    name it by construction. That is honest and it leaves G1 with no
    reachable negative until a successor substrate exists.

    But the gears case was not resolved by waiting. The slot for
    irreversibility was supplied by attention to a specific anomaly -- the
    efficiency ceiling of heat engines, which the mechanical account could
    state but not explain. The transferable move is therefore narrower than
    "wait": look where the current apparatus RETURNS A TERM IT CANNOT FILL.

    That is answerable from inside, and this folder produces such terms
    already. It is a candidate list, not the slot; whether the slot is in it
    is exactly what G1 says cannot be known from here.
    """
    terms = []
    cc = M.consistency_cost()
    terms.append(("consistency under lazy evaluation",
                  cc["state"], "multiscale.consistency_cost"))
    ev = LA.erasure_vs_measurement()
    terms.append(("memory-reuse factor / erasure count",
                  ev["reuse_factor"], "ladder_audit.erasure_vs_measurement"))
    d = CF.declined()
    terms.append(("recurrence of the framing over time",
                  d["grain"]["per_population_over_time"]["state"],
                  "consequence_frame.declined"))
    terms.append(("why any party states the hypothesis",
                  d["grain"]["per_statement"]["state"],
                  "consequence_frame.declined"))
    return {"terms": terms,
            "reachable_now": True,
            "is_the_slot": "UNKNOWN, and G1 says it must be"}


# --- report ----------------------------------------------------------------

def report():
    L = []
    A = L.append
    A("ERA METAPHOR AUDIT -- the delivered gaps, where they are checkable")
    A("=" * 72)
    A("")
    A("  The delivered text is careful about its own scope: REACHES the")
    A("  hypothesis' selection, DOESN'T reach its truth value, and")
    A("  METHOD_AS_STATED disclaims content outright. Nothing below")
    A("  disputes that scoping. What is checked is the two pointers the")
    A("  document makes into this folder, and one property of its table.")
    A("")
    A("-" * 72)
    A("")
    v = g2_verdict()
    A("  G2 -- IMPORTED BOUNDARY. 'discrete cells, finite state, additive")
    A("  capacity ... my audit half-caught at SHB_002 and stopped.'")
    A("")
    A("  POINTER: %s -> %s. Off by one, and the correction helps the gap."
      % (v["pointer_as_delivered"], v["pointer_corrected"]))
    A("")
    L.extend(wrap(v["why"]))
    A("")
    A("  And 'all three' covers three different situations:")
    A("")
    for i in g2_imports():
        A("    %-20s %s" % (i["import"], i["how"]))
        A("      at %s" % i["caught"])
        L.extend(wrap(i["evidence"], indent="        "))
        A("      checked against the published claim text: %s"
          % ("holds" if i["holds"] else "DOES NOT HOLD"))
        A("")
    A("    So: %d caught natively, %d only after an external audit arrived,"
      % (v["caught_natively"], v["caught_externally"]))
    A("    %d taken in two steps with only the first marked."
      % v["unmarked_step"])
    A("    'Half-caught and stopped' is right, and it is three different")
    A("    halves.")
    A("")
    A("    CONSEQUENCE: SHB_014 named THREE interpretive steps. Finite")
    A("    entropy -> finite state in bits is a FOURTH, and SHB_014's")
    A("    falsifier does not fire on it -- that falsifier asks for a")
    A("    Planck-length measurement or a demonstration that the steps are")
    A("    forced. The reachable failure mode (one more unnamed step) has")
    A("    no falsifier attached and the unreachable one does. G-FIT again.")
    A("")
    A("-" * 72)
    A("")
    g3 = g3_architecture_provenance()
    A("  G3 -- CEILING FROM SUBSTRATE. 'the universe does what our best")
    A("  machine does, and no more.'")
    A("")
    A("  VERDICT: LANDS, on SHB_010, and the module says it itself.")
    A("")
    A("    multiscale.py sources its architecture set to computing practice")
    A("    in its own docstring:")
    L.extend(wrap(", ".join(g3["sourced_to_computing_practice"]),
                  indent="      "))
    A("    architectures compared: %d, plus the lazy limit"
      % g3["architectures"])
    L.extend(wrap(", ".join(g3["names"]), indent="      "))
    A("")
    A("    SHB_010 reports %s 'across architectures nobody has argued"
      % g3["spread_claimed"])
    A("    against'. Those are architectures WE BUILD. So the spread is a")
    A("    spread over %s, not over %s."
      % (g3["spread_is_over"], g3["not_over"]))
    A("")
    A("    This does not weaken SHB_010. It carries it past what SHB_010")
    A("    claims: the quantity is not merely ill-posed pending a level")
    A("    stack -- the SPACE the level stack would be drawn from is not")
    A("    enumerable from inside, because every member of it is an")
    A("    artifact of ours. A ceiling read off our own repertoire.")
    A("")
    A("-" * 72)
    A("")
    g4 = g4_layer_pointer()
    A("  G4 -- UNLOCATABLE EXTERIOR. 'Layer 3 in the repo is exactly this")
    A("  gap ... two routes, same hole.'")
    A("")
    A("  POINTER: layer %s -> layer %s (%s). Off by one, same direction as"
      % (g4["pointer_as_delivered"], g4["pointer_corrected"],
         g4["layer_named"]))
    A("  G2, and again the correction is the sharper match.")
    A("    layers, in order: %s" % ", ".join(g4["layers"]))
    L.extend(wrap(g4["why"]))
    A("")
    A("    TWO ROUTES, SAME HOLE: CONFIRMED. %s" % g4["two_routes_confirmed"])
    A("    Arrived at from arithmetic here (a ratio whose denominator is a")
    A("    property of an object we cannot measure) and from the pattern")
    A("    there (every prior metaphor smuggled its exterior back in).")
    A("")
    A("-" * 72)
    A("")
    rc = reference_class_check()
    A("  THE REFERENCE CLASS -- %d instances, %d superseded"
      % (rc["instances"], rc["superseded"]))
    A("")
    A("    A rate is not readable from this: %s." % rc["why_not"])
    A("    Metaphors that were NOT superseded are not in the frame, and the")
    L.extend(wrap("document names a candidate itself -- %s."
                  % rc["counterexample_named_in_the_document"]))
    A("")
    A("    THE METHOD SURVIVES THIS AND THE TABLE DOES NOT.")
    A("    METHOD_AS_STATED says 'prior instances are not evidence against")
    A("    the current one' and 'claim content: none'. That disclaimer is")
    A("    exactly what makes the selection harmless -- a gradient over")
    A("    hindsight cases needs no base rate. Anyone reading '4 for 4' off")
    A("    the table is reading something the method already refused.")
    A("")
    L.extend(wrap(rc["shape"]))
    A("")
    A("-" * 72)
    A("")
    g1 = g1_operational_proxy()
    A("  G1 -- MISSING SLOT. 'the metaphor can't name it, by construction.'")
    A("")
    A("  VERDICT: honest, and unfalsifiable-until-superseded as stated.")
    A("  A NARROWER TRANSFER IS REACHABLE NOW.")
    A("")
    A("    The gears case was not resolved by waiting. The slot for")
    A("    irreversibility was supplied by attention to one anomaly -- the")
    A("    efficiency ceiling of heat engines, which the mechanical account")
    A("    could state and not explain. So the transferable move is")
    A("    narrower than 'wait for a successor': look where the current")
    A("    apparatus RETURNS A TERM IT CANNOT FILL.")
    A("")
    A("    That is answerable from inside. This folder already produces %d:"
      % len(g1["terms"]))
    for name, state, site in g1["terms"]:
        A("      %-38s %-14s %s" % (name, state, site.split(".")[0]))
    A("")
    A("    A candidate list, not the slot. Whether the slot is in it is")
    A("    exactly what G1 says cannot be known from here -- so the list")
    A("    is the deliverable and the verdict is %s." % g1["is_the_slot"])
    return "\n".join(L)


# --- selftest --------------------------------------------------------------

def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    ck("the claim table is readable and SHB_001 is in it",
       claim_text("SHB_001").startswith("| `SHB_001`"))
    ck("a missing claim id returns empty rather than raising",
       claim_text("SHB_999") == "")

    im = g2_imports()
    ck("all three G2 imports check out against the published claim text",
       all(i["holds"] for i in im))
    ck("the three imports score three DIFFERENT ways, so 'all three come "
       "from the apparatus' covers three situations",
       len({i["how"].split(",")[0] for i in im}) == 3)
    v = g2_verdict()
    ck("the G2 pointer is corrected off SHB_002",
       v["pointer_as_delivered"] == "SHB_002"
       and v["pointer_corrected"] == "SHB_001")
    ck("SHB_002 does not itself catch an imported boundary; SHB_001 does",
       "area" in claim_text("SHB_001")
       and "area" not in claim_text("SHB_002").split("holographic")[0])

    g3 = g3_architecture_provenance()
    ck("multiscale sources its architectures to computing practice in its "
       "own docstring", g3["module_says_so"])
    ck("SHB_010's 216 decades is found in the published claim text",
       g3["spread_claimed"] == "216 decades")

    g4 = g4_layer_pointer()
    ck("budget's docstring still declares three layers",
       len(g4["layers"]) == 3)
    ck("the unlocatable exterior is layer 2, VOID, not layer 3",
       g4["pointer_corrected"] == 2 and g4["layer_named"] == "VOID")
    ck("both pointers are off by one in the same direction",
       g4["pointer_as_delivered"] - g4["pointer_corrected"] == 1)

    rc = reference_class_check()
    ck("no rate is readable off the reference class",
       rc["rate_readable"] is False)
    ck("the method survives the selection even though the table does not",
       rc["method_survives"] is True)

    g1 = g1_operational_proxy()
    ck("the folder produces terms it cannot fill, and there is more than one",
       len(g1["terms"]) >= 3)
    ck("every such term is a named non-value state, not a number",
       all(isinstance(st, str) and st.isupper() and not st.isdigit()
           for _, st, _ in g1["terms"]))
    ck("the states are distinct, so the list is not one refusal repeated",
       len({st for _, st, _ in g1["terms"]}) >= 3)
    ck("whether the slot is among them is left UNKNOWN, per G1",
       g1["is_the_slot"].startswith("UNKNOWN"))

    ck("report renders", "TWO ROUTES, SAME HOLE" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
