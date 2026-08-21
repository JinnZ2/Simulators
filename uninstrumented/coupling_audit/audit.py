#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
# To the extent possible under law, the authors have waived all copyright and
# related or neighboring rights to this file.
"""
audit.py - record schema and scoring for the coupling audit.

    python3 audit.py --report
    python3 audit.py --template
    python3 audit.py --mechanisms     # gate types vs the parent register
    python3 audit.py --selftest

THE OBJECT. When a model measures a flow (calories, CO2e, freshwater) across a
set of agents, does the model's own coupling-variability machinery get applied
evenly to every agent drawing on that flow, or is it gated?

Not "count the pets". The question is about EVENNESS: whether a capability the
model already has runs on all the agents in scope, or stops at a line.

RELATIONSHIP TO THE PARENT REGISTER. ../uninstrumented.py asks whether an
instrument's constitution prevents a quantity from APPEARING AT ALL. This asks
something different and weaker: the quantity CAN be registered, the machinery
exists in the model and is named in the model's own vocabulary, and it is
applied to some agents and not others. An exclusion register would find
nothing here, because nothing is excluded from the apparatus -- the apparatus
is simply pointed at a subset.

Marker under exploration. Not a thesis.

stdlib only, parses under Python 3.9.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)

# --- vocabulary ------------------------------------------------------------

VERDICTS = (
    "ABSENT_NO_MACHINERY",       # agent unrepresented, model has no coupling
                                 # term for anyone
    "ABSENT_MACHINERY_PRESENT",  # agent unrepresented, model HAS a coupling
                                 # term and runs it on others
    "PRESENT_FIXED",             # agent represented, draw fixed or folded
                                 # into another agent's line
    "PRESENT_COUPLED",           # agent represented with a supply-coupled
                                 # draw, same rule as the other agents
)

GATES = (
    "species",         # the unit of analysis is one species
    "market_output",   # an agent enters if it yields a priced commodity
    "unstated",        # no rule is written; the boundary is in a definition
    "other",
)

VERDICT_GLOSS = {
    "ABSENT_NO_MACHINERY":
        "the agent is not in the ledger and the model has no coupling term "
        "for any agent -- a uniform simplification, not an asymmetry",
    "ABSENT_MACHINERY_PRESENT":
        "the agent is not in the ledger and the model DOES have a coupling "
        "term, which it runs on other agents. the capability exists and "
        "stops at a line",
    "PRESENT_FIXED":
        "the agent is in the ledger with a fixed draw, or folded into "
        "another agent's line, while other agents get the coupling term",
    "PRESENT_COUPLED":
        "the agent is in the ledger with a supply-coupled draw under the "
        "same rule as the other agents -- the falsifier",
}


class SchemaError(Exception):
    pass


def record(model_id, flow_measured, agents_drawing_on_flow, agents_represented,
           coupling_machinery_present, coupling_machinery_name, gate,
           gate_stated, verdict, agents_coupled=None, note=None, sources=None,
           model_seeded=False, provenance=None):
    """One audited model.

    model_id                     what was audited
    flow_measured                the flow and its units
    agents_drawing_on_flow       enumerated. every agent that draws on it,
                                 whether or not the model carries a term
    agents_represented           the subset the model carries a term for
    coupling_machinery_present   bool
    coupling_machinery_name      its name in the MODEL'S OWN vocabulary, not
                                 in this audit's. empty string if absent
    gate                         one of GATES
    gate_stated                  bool. is the rule written down anywhere, or
                                 is it a consequence of a definition
    verdict                      one of VERDICTS, as DECLARED by the entry

    agents_coupled               NOT IN THE ORIGINAL FIELD LIST. added because
                                 without it the verdict can only be declared,
                                 never derived, and an entry that declares its
                                 own verdict is a rubric rather than an
                                 instrument. score() derives the verdict from
                                 the other fields and reports agreement with
                                 the declared one. Recorded as a schema
                                 addition in LOG.md.
    """
    if gate not in GATES:
        raise SchemaError("gate must be one of %s, got %r" % (GATES, gate))
    if verdict not in VERDICTS:
        raise SchemaError("verdict must be one of %s, got %r"
                          % (VERDICTS, verdict))
    if coupling_machinery_present and not coupling_machinery_name:
        raise SchemaError(
            "coupling_machinery_present is True but the machinery is not "
            "named. the name must be the model's own term (rCSI, OECD "
            "equivalence scale, GLEAM drinking+service water), because "
            "naming it in this audit's vocabulary would make the field "
            "unfalsifiable against the model's documentation")
    missing = [a for a in agents_represented
               if a not in agents_drawing_on_flow]
    if missing:
        raise SchemaError(
            "agents_represented must be a subset of agents_drawing_on_flow; "
            "these are not in the draw list: %s" % missing)
    coupled = list(agents_coupled or [])
    stray = [a for a in coupled if a not in agents_represented]
    if stray:
        raise SchemaError(
            "an agent cannot be coupled without being represented: %s" % stray)
    return {
        "model_id": model_id,
        "flow_measured": flow_measured,
        "agents_drawing_on_flow": list(agents_drawing_on_flow),
        "agents_represented": list(agents_represented),
        "agents_coupled": coupled,
        "coupling_machinery_present": bool(coupling_machinery_present),
        "coupling_machinery_name": coupling_machinery_name,
        "gate": gate,
        "gate_stated": bool(gate_stated),
        "verdict": verdict,
        "note": note or "",
        "sources": list(sources or []),
        "MODEL_SEEDED": bool(model_seeded),
        "provenance": provenance or "",
    }


SKELETON = {
    "model_id": "",
    "flow_measured": "",
    "agents_drawing_on_flow": [],
    "agents_represented": [],
    "agents_coupled": [],
    "coupling_machinery_present": False,
    "coupling_machinery_name": "",
    "gate": "unstated",
    "gate_stated": False,
    "verdict": "ABSENT_NO_MACHINERY",
    "note": "",
    "sources": [],
    "MODEL_SEEDED": False,
    "provenance": "",
}


# --- scoring ---------------------------------------------------------------

def derive_verdict(rec):
    """Compute the verdict from the fields instead of reading it off.

    An entry that carries its own verdict cannot disagree with itself. This
    lets it.
    """
    unrepresented = [a for a in rec["agents_drawing_on_flow"]
                     if a not in rec["agents_represented"]]
    if unrepresented:
        if rec["coupling_machinery_present"]:
            return "ABSENT_MACHINERY_PRESENT"
        return "ABSENT_NO_MACHINERY"
    uncoupled = [a for a in rec["agents_represented"]
                 if a not in rec["agents_coupled"]]
    if uncoupled:
        return "PRESENT_FIXED"
    return "PRESENT_COUPLED"


def evenness(rec):
    """The test the audit is named for.

    Returns the two sets that make the verdict, and whether the machinery is
    applied to every agent drawing on the flow. `None` where there is no
    machinery to apply -- an absence, not a False.
    """
    if not rec["coupling_machinery_present"]:
        return {"applied_to": [], "not_applied_to": [], "even": None,
                "why": "no coupling machinery in the model; evenness is not "
                       "defined, and this is an absence rather than a "
                       "failure"}
    applied = list(rec["agents_coupled"])
    not_applied = [a for a in rec["agents_drawing_on_flow"]
                   if a not in applied]
    return {"applied_to": applied, "not_applied_to": not_applied,
            "even": not not_applied,
            "why": "the machinery named %r runs on %d of %d agents drawing "
                   "on the flow" % (rec["coupling_machinery_name"],
                                    len(applied),
                                    len(rec["agents_drawing_on_flow"]))}


def score(rec):
    derived = derive_verdict(rec)
    ev = evenness(rec)
    return {
        "model_id": rec["model_id"],
        "declared": rec["verdict"],
        "derived": derived,
        "agrees": derived == rec["verdict"],
        "evenness": ev,
        "gate": rec["gate"],
        "gate_stated": rec["gate_stated"],
        "gate_justified_in_units": gate_justified_in_units(rec),
        "unrepresented": [a for a in rec["agents_drawing_on_flow"]
                          if a not in rec["agents_represented"]],
    }


def gate_justified_in_units(rec):
    """Is the gate justified in the units being measured?

    FALSIFIER.md: a gate that is both STATED and justified in the measured
    quantity is a pass, not a hit. A gate on species or on market category is
    not a justification in the units, however clearly it is written down.

    Returns True / False / None -- None where no gate has been identified, so
    "not justified" and "not yet examined" do not share a value.
    """
    if rec["gate"] == "other":
        return None
    if rec["gate"] in ("species", "market_output"):
        return False
    if rec["gate"] == "unstated":
        return False
    return None


# --- gate types against the parent register --------------------------------

def parent_mechanisms():
    """Import the register rather than copying it.

    A copied vocabulary drifts; the repo has instances of exactly that. If the
    parent module is unavailable the check reports that rather than falling
    back to a stale list.
    """
    sys.path.insert(0, PARENT)
    try:
        import uninstrumented as U
        return list(U.MECHANISMS), dict(U.MECHANISM_GLOSS)
    except Exception as exc:                                # pragma: no cover
        return None, {"error": str(exc)}


# Hand adjudication. Each gate type against the register's closed vocabulary.
# Match strength is stated, never asserted as identity.
GATE_MECHANISM_NOTES = [
    {
        "gate": "species",
        "nearest": "AUDIT_ASYMMETRY",
        "strength": "STRONG",
        "why": "the register's gloss is 'guard fires on one side only'. Here "
               "a capability the model already has -- a coupling-variability "
               "term -- runs on one class of agent and not on another drawing "
               "on the same flow. Same shape, one level up: the asymmetry is "
               "in the MODEL's machinery rather than in an audit's hedging. "
               "This is close enough that a new mechanism should not be "
               "claimed for it.",
    },
    {
        "gate": "market_output",
        "nearest": "PROXY_SUBSTITUTION",
        "strength": "PARTIAL",
        "why": "the register's gloss is 'enforceable measure displaces the "
               "target it stood in for'. Salability is enforceable and it "
               "does displace the biological criterion. But proxy "
               "substitution names a measure standing in for a QUANTITY, and "
               "this is a criterion standing in for MEMBERSHIP -- what enters "
               "the ledger at all, rather than what value it is given. The "
               "difference may not survive scrutiny; it is recorded rather "
               "than resolved.",
    },
    {
        "gate": "unstated",
        "nearest": "BUDGET_BOUNDARY",
        "strength": "PARTIAL",
        "why": "the register's gloss is 'closed budget compared to open'. A "
               "per-capita denominator is a boundary imported from an "
               "accounting convention: the numerator is open (all emissions "
               "from the expenditure) and the denominator is closed to one "
               "species. The gate is not a separate exclusion so much as an "
               "arithmetic choice nobody restates as one.",
    },
]


def mechanism_check():
    """Does any gate type here duplicate an existing register mechanism?"""
    mechs, gloss = parent_mechanisms()
    out = {"register_available": mechs is not None,
           "register_size": len(mechs) if mechs else None,
           "notes": [], "candidate_ninth": None}
    for n in GATE_MECHANISM_NOTES:
        row = dict(n)
        row["in_register"] = bool(mechs and n["nearest"] in mechs)
        row["gloss"] = gloss.get(n["nearest"], "") if mechs else ""
        out["notes"].append(row)
    strong = [n for n in out["notes"] if n["strength"] == "STRONG"]
    out["candidate_ninth"] = {
        "claimed": False,
        "why": "at least one gate type (species) matches an existing "
               "mechanism strongly, so a new mechanism is not claimed here. "
               "Separately, the ordinal is already taken: MECHANISM_09, "
               "MECHANISM_10 and MECHANISM_11 are proposed in sibling "
               "folders (category-weld, generation-capacity, "
               "derivation-discarded) against this same register of eight, "
               "so 'a candidate ninth' would collide even if the shape were "
               "new.",
        "strong_matches": [n["gate"] for n in strong],
    }
    return out


# --- report ----------------------------------------------------------------

def report(entries):
    L = []
    A = L.append
    A("COUPLING AUDIT")
    A("=" * 72)
    A("")
    A("  Does the model's own coupling-variability machinery get applied")
    A("  evenly to every agent drawing on the measured flow, or is it gated?")
    A("")
    A("-" * 72)
    A("")
    for rec in entries:
        s = score(rec)
        for line in _wrap(rec["model_id"], "  "):
            A(line)

        def field(label, value):
            head = "    %-20s " % label
            wrapped = _wrap(value, " " * len(head))
            wrapped[0] = head + wrapped[0].strip()
            L.extend(wrapped)

        field("flow", rec["flow_measured"])
        field("drawing on it", ", ".join(rec["agents_drawing_on_flow"]))
        field("represented", ", ".join(rec["agents_represented"]) or "--")
        field("coupling machinery",
              rec["coupling_machinery_name"]
              if rec["coupling_machinery_present"] else "ABSENT")
        field("coupling applied to", ", ".join(rec["agents_coupled"]) or "--")
        A("    gate                 %s (%s)"
          % (rec["gate"], "stated" if rec["gate_stated"] else "implicit"))
        just = s["gate_justified_in_units"]
        A("    justified in units   %s"
          % ("--" if just is None else ("yes" if just else "no")))
        ev = s["evenness"]
        A("    even                 %s"
          % ("--" if ev["even"] is None else ("yes" if ev["even"] else "no")))
        A("    verdict declared     %s" % s["declared"])
        A("    verdict derived      %s" % s["derived"])
        A("    agrees               %s" % ("yes" if s["agrees"] else "NO"))
        if rec["note"]:
            A("    note")
            for line in _wrap(rec["note"], "      "):
                A(line)
        if rec["MODEL_SEEDED"]:
            A("    MODEL_SEEDED         True")
        A("")
    A("-" * 72)
    A("")
    A("  COUNTS")
    for v in VERDICTS:
        n = sum(1 for r in entries if derive_verdict(r) == v)
        A("    %-28s %d" % (v, n))
    A("")
    falsifier = [r for r in entries if derive_verdict(r) == "PRESENT_COUPLED"]
    passes = [r for r in entries
              if r["gate_stated"] and gate_justified_in_units(r)]
    A("    entries meeting the falsifier (PRESENT_COUPLED)   %d"
      % len(falsifier))
    A("    entries with a stated, units-justified gate       %d" % len(passes))
    A("")
    A("    Either would refute the marker. See FALSIFIER.md.")
    A("")
    A("-" * 72)
    A("")
    mc = mechanism_check()
    A("  GATE TYPES AGAINST THE PARENT REGISTER")
    A("    register imported, not copied: %s" % mc["register_available"])
    A("    mechanisms in the register:    %s" % mc["register_size"])
    A("")
    for n in mc["notes"]:
        A("    gate %-14s nearest %-20s %s"
          % (n["gate"], n["nearest"], n["strength"]))
        for line in _wrap(n["why"], "      "):
            A(line)
        A("")
    A("    CANDIDATE NINTH CLAIMED: %s" % mc["candidate_ninth"]["claimed"])
    for line in _wrap(mc["candidate_ninth"]["why"], "      "):
        A(line)
    return "\n".join(L)


def _wrap(text, indent, width=72):
    words = text.split()
    lines, cur = [], indent
    for w in words:
        if len(cur) + len(w) + 1 > width and cur.strip():
            lines.append(cur.rstrip())
            cur = indent + w + " "
        else:
            cur += w + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


# --- selftest --------------------------------------------------------------

def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    def base(**kw):
        args = dict(model_id="m", flow_measured="x (units)",
                    agents_drawing_on_flow=["a", "b"],
                    agents_represented=["a"], agents_coupled=["a"],
                    coupling_machinery_present=True,
                    coupling_machinery_name="named term",
                    gate="species", gate_stated=False,
                    verdict="ABSENT_MACHINERY_PRESENT")
        args.update(kw)
        return record(**args)

    ck("a bad gate is refused",
       _raises(lambda: base(gate="nonsense")))
    ck("a bad verdict is refused",
       _raises(lambda: base(verdict="MAYBE")))
    ck("machinery present but unnamed is refused, because the name must be "
       "the model's own",
       _raises(lambda: base(coupling_machinery_name="")))
    ck("represented must be a subset of drawing",
       _raises(lambda: base(agents_represented=["a", "z"],
                            agents_coupled=["a"])))
    ck("coupled must be a subset of represented",
       _raises(lambda: base(agents_coupled=["a", "b"])))

    r = base()
    ck("unrepresented agent + machinery -> ABSENT_MACHINERY_PRESENT",
       derive_verdict(r) == "ABSENT_MACHINERY_PRESENT")
    r2 = base(coupling_machinery_present=False, coupling_machinery_name="",
              agents_coupled=[], verdict="ABSENT_NO_MACHINERY")
    ck("unrepresented agent + no machinery -> ABSENT_NO_MACHINERY",
       derive_verdict(r2) == "ABSENT_NO_MACHINERY")
    r3 = base(agents_represented=["a", "b"], agents_coupled=["a"],
              verdict="PRESENT_FIXED")
    ck("represented but uncoupled -> PRESENT_FIXED",
       derive_verdict(r3) == "PRESENT_FIXED")
    r4 = base(agents_represented=["a", "b"], agents_coupled=["a", "b"],
              verdict="PRESENT_COUPLED")
    ck("represented and coupled -> PRESENT_COUPLED",
       derive_verdict(r4) == "PRESENT_COUPLED")
    ck("all four verdicts are reachable from the schema, so the instrument "
       "is not CONSTANT_SILENT on any of them",
       len({derive_verdict(x) for x in (r, r2, r3, r4)}) == 4)

    ck("evenness is None where there is no machinery, not False",
       evenness(r2)["even"] is None)
    ck("evenness is False where machinery runs on a subset",
       evenness(r3)["even"] is False)
    ck("evenness is True where machinery runs on everyone drawing",
       evenness(r4)["even"] is True)

    ck("a declared verdict that disagrees with the derived one is reported "
       "rather than silently corrected",
       score(base(verdict="PRESENT_COUPLED"))["agrees"] is False)

    ck("gate justification is None for 'other', so unexamined and "
       "unjustified do not share a value",
       gate_justified_in_units(base(gate="other")) is None)
    ck("a species gate is not justified in the units however clearly stated",
       gate_justified_in_units(base(gate="species", gate_stated=True))
       is False)

    mc = mechanism_check()
    ck("the parent register is imported, not copied",
       mc["register_available"] and mc["register_size"] == 8)
    ck("every nearest mechanism named is actually in the register",
       all(n["in_register"] for n in mc["notes"]))
    ck("no candidate ninth is claimed",
       mc["candidate_ninth"]["claimed"] is False)
    ck("at least one gate matches an existing mechanism strongly",
       len(mc["candidate_ninth"]["strong_matches"]) >= 1)

    ck("the skeleton is a legal record",
       _no_raise(lambda: record(**{k2: v for k2, v in SKELETON.items()
                                   if k2 not in ("MODEL_SEEDED",)},
                                model_seeded=SKELETON["MODEL_SEEDED"])))
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def _raises(fn):
    try:
        fn()
    except SchemaError:
        return True
    except Exception:
        return False
    return False


def _no_raise(fn):
    try:
        fn()
    except Exception:
        return False
    return True


def main():
    ap = argparse.ArgumentParser(description="coupling audit")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--template", action="store_true")
    ap.add_argument("--mechanisms", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.template:
        import json
        print(json.dumps(SKELETON, indent=2))
        return 0
    if a.mechanisms:
        import json
        print(json.dumps(mechanism_check(), indent=2))
        return 0
    sys.path.insert(0, HERE)
    import entries as E
    print(report(E.ENTRIES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
