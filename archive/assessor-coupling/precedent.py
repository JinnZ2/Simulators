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
        sys.stderr.write("precedent.py is a library; run python3 selftest.py\n")
        return 2
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
