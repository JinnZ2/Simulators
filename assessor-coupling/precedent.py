# precedent.py -- WO-6: the precedent record read as a corpus, the common
# prior defense scored against it, and the order's step 4 built and unrun.
#
# The order calls the precedent record the instrument. It is PARSED out of
# WORK_ORDER.md at call time and never retyped; the named parties in any
# render come out of the delivered document and none is authored here.
#
# NOT ABOUT ANY NAMED ORGANIZATION. The order's constraint is structural
# here: nothing in this module authors a party, and the one scorer that
# takes an arrangement (conditions.py) has no name field at all.
#
# CONSTRUCTED where constructed. The negative-arm corpus below is built to
# show that a verdict is reachable; it is not evidence about anything.
#
# stdlib only, parses under 3.9, ASCII.

import os
import re
import sys
from collections import namedtuple

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

import conditions as cond

ORDER = cond.ORDER

EVALUABLE = "EVALUABLE"
NOT_EVALUABLE = "NOT_EVALUABLE"
NOT_RUN = "NOT_RUN"

CHOICES = {
    6: "a precedent case is a top-level bullet inside one of the record's "
       "'###' era sections, keyed on the bolded lead. Sub-bullets and the "
       "prior-defense list are read separately.",
    7: "the negative arm of the precedent corpus is counted as the number "
       "of cases in which the prior defense held and the structure did NOT "
       "fail. The order's record has no such section, so the count is zero "
       "by parse and not by assumption.",
    8: "a cross-reference resolves only on a folder path that exists AND a "
       "content marker inside it; a work-order number occurring in prose "
       "is not a resolution.",
}


Case = namedtuple("Case", "era lead text")


def order_text(path=ORDER):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _section(txt, header, stop=r"^## "):
    m = re.search(r"^%s.*?$(.*?)%s" % (re.escape(header), stop), txt,
                  re.S | re.M)
    return m.group(1) if m else None


def _bullets(body):
    """Top-level '- ' bullets with their continuation lines."""
    out = []
    cur = None
    for line in body.splitlines():
        h = re.match(r"^- (.*)$", line)
        if h:
            if cur is not None:
                out.append(cur)
            cur = h.group(1).strip()
        elif cur is not None and line.startswith("  ") and line.strip():
            cur = cur + " " + line.strip()
        elif cur is not None and not line.strip():
            pass
    if cur is not None:
        out.append(cur)
    return out


def cases(path=ORDER):
    """Parse the precedent record. [CHOICE 6]"""
    txt = order_text(path)
    body = _section(txt, "## THE PRECEDENT RECORD")
    if body is None:
        raise cond.OrderUnparsed("%s: no precedent record section" % path)
    out = []
    era = None
    chunk = []
    eras = []
    for line in body.splitlines():
        h = re.match(r"^### (.*)$", line)
        if h:
            if era is not None:
                eras.append((era, "\n".join(chunk)))
            era = h.group(1).strip()
            chunk = []
        elif era is not None:
            chunk.append(line)
    if era is not None:
        eras.append((era, "\n".join(chunk)))
    for era, chunk in eras:
        if era.lower().startswith("the common prior defense"):
            continue
        for b in _bullets(chunk):
            m = re.match(r"^\*\*(.+?)\*\*\s*(.*)$", b)
            if m:
                out.append(Case(era, m.group(1).rstrip("."), m.group(2)))
            else:
                out.append(Case(era, None, b))
    if not out:
        raise cond.OrderUnparsed("%s: record present, no cases" % path)
    return out


def prior_defense(path=ORDER):
    """The four statements every case in the record is said to have made."""
    txt = order_text(path)
    body = _section(txt, "### The common prior defense", stop=r"^## ")
    if body is None:
        raise cond.OrderUnparsed("%s: no prior-defense section" % path)
    out = _bullets(body)
    if not out:
        raise cond.OrderUnparsed("%s: prior-defense section, no items"
                                 % path)
    return out


def non_financial_couplings(path=ORDER):
    txt = order_text(path)
    body = _section(txt, "## Non-financial couplings with no disclosure "
                         "field")
    if body is None:
        raise cond.OrderUnparsed("%s: no non-financial section" % path)
    return _bullets(body)


# --- the corpus, and what it can and cannot bound ----------------------

def corpus_shape(path=ORDER):
    cs = cases(path)
    eras = {}
    for c in cs:
        eras[c.era] = eras.get(c.era, 0) + 1
    return {"n_cases": len(cs), "n_eras": len(eras), "by_era": eras,
            "n_defense_items": len(prior_defense(path))}


def selection_declared(path=ORDER):
    """The order's own scope limit on the record. Verbatim containment."""
    flat = " ".join(order_text(path).split())
    return {
        "illustrative": "selected for documentation quality" in flat,
        "not_systematic": "Not a systematic sample" in flat,
        "no_base_rate": "no base rate is claimed" in flat,
    }


def negative_arm(path=ORDER, corpus=None):
    """Cases in which the prior defense held and the structure did NOT fail.

    Counted by parse. The record has no section for them. [CHOICE 7]
    """
    if corpus is not None:
        return sum(1 for c in corpus if not c.get("failed"))
    flat = " ".join(order_text(path).split())
    hits = re.findall(r"###\s+[^#]*?(held|did not fail|no failure)", flat)
    return len(hits)


def defense_discrimination(path=ORDER, corpus=None):
    """Does the four-item prior defense separate the cases that failed from
    the cases that did not?

    On the delivered record the answer is NOT_EVALUABLE, and the reason is
    the record's own construction, not a shortcoming of the check: every
    case in it is a case in which the structure failed, so there is no
    negative arm to separate from. A corpus carrying one returns a figure.
    """
    if corpus is None:
        cs = cases(path)
        failed = len(cs)
        held = negative_arm(path)
    else:
        failed = sum(1 for c in corpus if c.get("failed"))
        held = sum(1 for c in corpus if not c.get("failed"))
    if held == 0:
        return {"state": NOT_EVALUABLE,
                "reason": "selected_on_outcome",
                "failed": failed, "not_failed": held,
                "discrimination": None}
    total = failed + held
    return {"state": EVALUABLE, "reason": None,
            "failed": failed, "not_failed": held,
            "discrimination": failed / float(total)}


def order_finding_line(path=ORDER):
    """The record's own summary sentence, located verbatim."""
    flat = " ".join(order_text(path).split())
    line = ("hop-1 cleanliness has never once been sufficient, in any "
            "domain, at any point in the record")
    return {"present": line in flat, "line": line}


def finding_vs_scope(path=ORDER):
    """The summary sentence read against the order's own scope limit.

    The sentence is a statement about THE RECORD; the scope limit says the
    record is illustrative, not systematic, and claims no base rate. Both
    are in the document. The narrow reading survives and the universal one
    does not, and the order's own step 2 is the step it names for this.
    """
    sel = selection_declared(path)
    fin = order_finding_line(path)
    disc = defense_discrimination(path)
    both = fin["present"] and all(sel.values())
    return {
        "summary_present": fin["present"],
        "scope_limit_present": all(sel.values()),
        "in_tension": both,
        "supported_reading": "in the selected cases, hop-1 cleanliness was "
                             "not sufficient",
        "unsupported_reading": "how often hop-1 cleanliness IS sufficient; "
                               "the corpus has no case in which it held, "
                               "so it cannot bound the rate in either "
                               "direction",
        "discrimination_state": disc["state"],
        "step_named_by_order": "step 2, the systematic precedent survey",
    }


# --- condition 6 -------------------------------------------------------

def condition_six_position(path=ORDER):
    """The oldest remedy in the record against its current standing.

    Both readings are verbatim containment, not a classification.
    """
    flat = " ".join(order_text(path).split())
    cs = cases(path)
    first = cs[0] if cs else None
    return {
        "earliest_case_era": first.era if first else None,
        "earliest_case_is_personal_liability":
            bool(first) and "Personal liability" in first.text,
        "order_calls_it_least_discussed":
            "Condition 6 is the one least discussed in contemporary "
            "arrangements" in flat,
        "current_position_state": cond.stated_position(path).get(6),
    }


# --- step 4: the disclosure-field audit --------------------------------

def disclosure_coverage(instrument, path=ORDER):
    """Which of the eight conditions a declared disclosure instrument has a
    FIELD for. `instrument` is {condition number: True/False/UNDECLARED}.

    A condition the instrument does not mention is UNDECLARED, never a
    missing field -- the order's own point is that an absent field reads as
    ABSENT rather than unmeasured, and the audit must not commit the same
    move. [CHOICE 3]
    """
    out = {}
    for n in cond.condition_ids(path):
        v = instrument.get(n, cond.UNDECLARED)
        if v not in (True, False, cond.UNDECLARED):
            raise ValueError("condition %s: %r outside the declared set"
                             % (n, v))
        out[n] = v
    return out


STEP4 = {
    "run": False,
    "reason": "the order's step 4 scores existing conflict-of-interest "
              "disclosure instruments across fields. No instrument is "
              "reachable from this environment and none is composed from "
              "memory, so no instrument is scored.",
    "expected_by_order": "money only",
    "order_line": "A null result on the other seven is the finding.",
}


STEP5 = {
    "run": False,
    "reason": "scoring a field other than AI, blind, is a calibration check "
              "on the instrument. It takes an arrangement this session does "
              "not hold, and an arrangement composed here would be scored "
              "by the hand that composed it.",
}


# --- cross-references --------------------------------------------------

COMPANIONS = {
    "WO-1": ("chain-position", "chain_position.py"),
    "WO-4": ("unowned-join", "invariant.py"),
    "WO-5": ("reporting-chain-loss", "hop_compose.py"),
}


def companion_state(wo, root=ROOT):
    ent = COMPANIONS.get(wo)
    if ent is None:
        return "UNKNOWN_COMPANION"
    folder, marker = ent
    d = os.path.join(root, folder)
    if not os.path.isdir(d):
        return "ABSENT"
    if not os.path.exists(os.path.join(d, marker)):
        return "FOLDER_NO_MARKER"
    return "RESOLVED"


def companions(root=ROOT):
    return dict((w, companion_state(w, root)) for w in sorted(COMPANIONS))


def _fmt(v):
    return "--" if v is None else str(v)


def render(path=ORDER):
    lines = []
    lines.append("WO-6 PRECEDENT RECORD -- parsed from WORK_ORDER.md.")
    lines.append("Every case, era and defense item below comes out of the")
    lines.append("delivered document; none is authored here, and every")
    lines.append("fact in it is carried and checked against nothing.")
    lines.append("")
    sh = corpus_shape(path)
    lines.append("cases %d across %d eras; prior-defense items %d"
                 % (sh["n_cases"], sh["n_eras"], sh["n_defense_items"]))
    for era in sorted(sh["by_era"]):
        lines.append("  %-28s %d" % (era, sh["by_era"][era]))
    lines.append("")
    d = defense_discrimination(path)
    lines.append("DOES THE PRIOR DEFENSE SEPARATE THE CASES")
    lines.append("  state           %s" % d["state"])
    lines.append("  reason          %s" % _fmt(d["reason"]))
    lines.append("  cases that went %d   cases that held %d"
                 % (d["failed"], d["not_failed"]))
    lines.append("  separation      %s" % _fmt(d["discrimination"]))
    lines.append("")
    t = finding_vs_scope(path)
    lines.append("THE RECORD'S SUMMARY SENTENCE AGAINST ITS OWN SCOPE LIMIT")
    lines.append("  summary present       %s" % t["summary_present"])
    lines.append("  scope limit present   %s" % t["scope_limit_present"])
    lines.append("  in tension            %s" % t["in_tension"])
    lines.append("  supported reading     %s" % t["supported_reading"])
    lines.append("  not supported here    %s" % t["unsupported_reading"])
    lines.append("  step named by the order %s" % t["step_named_by_order"])
    lines.append("")
    c6 = condition_six_position(path)
    lines.append("CONDITION 6")
    lines.append("  earliest entry in the record is a personal-liability")
    lines.append("  remedy: %s (%s)"
                 % (c6["earliest_case_is_personal_liability"],
                    c6["earliest_case_era"]))
    lines.append("  the order records it as least discussed now: %s"
                 % c6["order_calls_it_least_discussed"])
    lines.append("  its state in the current-position reading: %s"
                 % c6["current_position_state"])
    lines.append("")
    nf = non_financial_couplings(path)
    lines.append("NON-FINANCIAL COUPLINGS WITH NO DISCLOSURE FIELD: %d"
                 % len(nf))
    lines.append("  the order: because there is no field, these read as")
    lines.append("  ABSENT rather than unmeasured")
    lines.append("")
    lines.append("STEP 4, the disclosure-field audit: %s" % NOT_RUN)
    lines.append("  %s" % STEP4["reason"])
    lines.append("  expected by the order: %s" % STEP4["expected_by_order"])
    lines.append("STEP 5, scoring another field blind: %s" % NOT_RUN)
    lines.append("  %s" % STEP5["reason"])
    lines.append("")
    lines.append("COMPANIONS [CHOICE 8]")
    for w, st in sorted(companions().items()):
        lines.append("  %-6s %s" % (w, st))
    return "\n".join(lines) + "\n"
"""WO-6, the precedent record parsed, and steps 2 and 3 as schemas.

The order calls the precedent table THE INSTRUMENT. It is parsed out of
WORK_ORDER.md at call time: every entry is CARRIED and verified against
nothing here (every archival and publisher host refuses CONNECT). Where
the order's own text carries a number adjacent to a unit word (dead,
deaths, BCE) it is extracted AS WRITTEN with its span, never asserted.

Step 2 (systematic survey) and step 3 (remedy decay) are shipped as
schemas with every cell UNMEASURED and the input each wants named. Step
2's sampling frame is stated: a survey of failure investigations is
selected on failure, and the order's own scope limit says the frequency
is not recoverable from surviving remedies.

Library module: refuses --selftest; the suite is selftest.py.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = os.path.join(HERE, "WORK_ORDER.md")
UNIT_WORDS = ("dead", "deaths", "BCE")
REMEDY_LEAD = ("Remedy", "remedy")


def entries(text=None):
    """Precedent entries under the three ### headings of THE PRECEDENT
    RECORD, each: era, name, body, numbers-as-written, remedy-stated."""
    text = text if text is not None else open(ORDER, encoding="utf-8").read()
    m = re.search(r"## THE PRECEDENT RECORD.*?\n(.*?)\n### The common prior defense", text, re.S)
    if not m:
        raise ValueError("precedent record not found")
    out = []
    era = None
    for block in re.split(r"\n(?=- \*\*|### )", m.group(1)):
        block = block.strip()
        if block.startswith("### "):
            era = block[4:].strip()
            continue
        if not block.startswith("- **"):
            continue
        name = re.match(r"- \*\*(.+?)\*\*", block).group(1).rstrip(".")
        body = " ".join(l.strip() for l in block.splitlines())
        nums = [{"as_written": mm.group(0), "span": mm.span()}
                for mm in re.finditer(r"~?[\d,]+\s+(?:%s)\b" % "|".join(UNIT_WORDS), body)]
        remedy = any(body.find(w + ":") >= 0 or body.find(w + " ") >= 0 for w in REMEDY_LEAD)
        out.append({"era": era, "name": name, "status": "CARRIED_NOT_VERIFIED",
                    "numbers_as_written": nums, "remedy_stated": remedy, "body": body})
    return out


def survey_schema():
    """Step 2 as a schema. Every cell UNMEASURED; the frame stated."""
    return {"step": 2, "state": "NOT_RUN",
            "unit": "one failure investigation naming assessor-assessed coupling as contributing",
            "fields": {"domain": "UNMEASURED", "investigation_id": "UNMEASURED", "coupling_named": "UNMEASURED",
                       "remedy_adopted": "UNMEASURED", "remedy_persisted": "UNMEASURED", "period": "UNMEASURED"},
            "frame": "selected on failure: an investigation exists because something failed, so the survey "
                     "reports coupling among failures and no rate over arrangements; the order's own scope "
                     "limit says the frequency is not recoverable",
            "wants": "accident and failure investigation corpora across domains (egress-refused here)"}


def decay_schema():
    """Step 3 as a schema over the four remedies the order names."""
    return {"step": 3, "state": "NOT_RUN",
            "remedies": ["assay offices", "boiler inspection", "SOX separation", "NRC split"],
            "fields": {"condition_at_adoption": "UNMEASURED", "condition_at_t": "UNMEASURED",
                       "decay_time": "UNMEASURED", "eroded_by": "UNMEASURED"},
            "tests": "WO-4 face 7 (description decoupled from referent); WO-4 is not in this tree",
            "wants": "archival record per remedy over its whole period, read by a historian of regulation"}


def render():
    es = entries()
    lines = ["precedent -- WO-6, the precedent record parsed; steps 2 and 3 as schemas",
             "  every entry CARRIED_NOT_VERIFIED; numbers extracted as written with a span, asserted by nobody here"]
    for e in es:
        nums = ", ".join(n["as_written"] for n in e["numbers_as_written"]) or "-"
        lines.append("    %-22s %-46s remedy_stated=%-5s numbers=%s" % (e["era"][:22], e["name"][:46], e["remedy_stated"], nums))
    lines.append("  entries %d  eras %d  with a stated remedy %d  with a number as written %d"
                 % (len(es), len({e["era"] for e in es}), sum(e["remedy_stated"] for e in es),
                    sum(1 for e in es if e["numbers_as_written"])))
    s, d = survey_schema(), decay_schema()
    lines.append("  step 2 survey: %s  frame: %s" % (s["state"], s["frame"].split(":")[0]))
    lines.append("  step 3 decay:  %s  remedies %s  every field UNMEASURED" % (d["state"], d["remedies"]))
    lines.append("  step 5 blind scoring of a non-AI field: NOT_RUN (requires a party outside the sample; the author is inside it)")
    lines.append("  reading: the table is the order's instrument and is carried whole; nothing in it was checked")
    lines.append("           against a source, and no base rate is claimed by the order or computed here")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "precedent is a library and a render; the checks live in "
            "assessor-coupling/test_assessor.py -- run "
            "python3 assessor-coupling/test_assessor.py\n")
        return 2
    if "--choices" in argv:
        for n in sorted(CHOICES):
            sys.stdout.write("[CHOICE %d] %s\n" % (n, CHOICES[n]))
        return 0
    sys.stdout.write(render())
        sys.stderr.write("precedent.py is a library; run python3 selftest.py\n")
        return 2
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
