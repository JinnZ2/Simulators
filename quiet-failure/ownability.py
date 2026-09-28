"""WO-2 steps 3 and 4, and the open question they bear on.

Step 3: the inverse case -- an organisation that costed the aggregation
function honestly and declined it anyway. The order reports "Not found in
two searches" and asks that a null be reported rather than dropped. A
null is reportable only when it is BOUNDED: corpus named, terms named,
date, hit count (an absence claim with no corpus is not a measurement).
The order's own null states none of those, so it is carried as
UNBOUNDED; nothing here bounds it, since every archive host refuses
CONNECT.

Step 4: does any regulator assign the join explicitly as a named role
with authority? One such record is the existence proof for ownability.
A record declares the role name, the authority, and whether the
JOIN specifically is what the role holds -- a role that holds the
inspection or the report is not the join.

Open question: UNOWNABLE vs NEVER_ASSIGNED. Derived from the records,
never picked: an existence proof anywhere makes the gap NEVER_ASSIGNED
for that domain; no record at all leaves it UNDETERMINED. The order's
current read is carried as the order's, beside the derived state.
Library module: refuses --selftest; the suite is selftest.py.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = os.path.join(HERE, "WORK_ORDER.md")
NULL_FIELDS = ("corpus", "terms", "searched_on", "hits")
ROLE_FIELDS = ("regulator", "role_name", "authority", "holds_the_join")


def order_null(text=None):
    """The order's step-3 null, as written, and which bounding fields
    its sentence supplies (none, read from the text)."""
    text = text or open(ORDER, encoding="utf-8").read()
    m = re.search(r"3\. Search for the inverse case: (.*?)\n\s*4\. ", text, re.S)
    if not m:
        raise ValueError("step 3 not found")
    sent = re.sub(r"\s+", " ", m.group(1))
    n = re.search(r"Not found in (\w+) searches", sent)
    return {"as_written": sent, "searches_stated": n.group(1) if n else "UNSTATED",
            "corpus_stated": False, "terms_stated": False, "date_stated": False,
            "status": "CARRIED", "bounded": bounded({"searches": n.group(1) if n else None})}


def bounded(null):
    """A null record is BOUNDED when it names corpus, terms, date and a
    hit count; otherwise UNBOUNDED naming what it lacks. An UNBOUNDED
    null is a report of a search, not a measurement of an absence."""
    if not isinstance(null, dict):
        return {"state": "MALFORMED"}
    lacks = [f for f in NULL_FIELDS if null.get(f) in (None, "", [])]
    if "hits" in null and not isinstance(null.get("hits"), int) and null.get("hits") is not None:
        return {"state": "MALFORMED", "why": "hits is not an integer"}
    if lacks:
        return {"state": "UNBOUNDED", "lacks": lacks}
    return {"state": "BOUNDED", "hits": null["hits"],
            "reading": "NULL_IN_STATED_CORPUS" if null["hits"] == 0 else "INVERSE_CASE_CANDIDATES"}


def inverse_search(nulls):
    """Step 3 over a list of null records: the bounded ones aggregate,
    the unbounded ones are listed and enter no count."""
    out = {"bounded": [], "unbounded": [], "candidates": 0}
    for n in nulls:
        b = bounded(n)
        if b["state"] == "BOUNDED":
            out["bounded"].append({"corpus": n["corpus"], "hits": n["hits"]})
            out["candidates"] += n["hits"]
        else:
            out["unbounded"].append(b.get("lacks", ["malformed"]))
    if not out["bounded"]:
        out["state"] = "NOT_MEASURED"
        out["why"] = "no bounded null supplied; %d unbounded report(s) enter no count" % len(out["unbounded"])
    elif out["candidates"] == 0:
        out["state"] = "NULL_IN_STATED_CORPORA"
    else:
        out["state"] = "CANDIDATES_TO_READ"
    return out


def role_record(rec):
    """One regulator-role record -> EXISTENCE_PROOF / ROLE_NOT_THE_JOIN /
    ROLE_WITHOUT_AUTHORITY / UNDECLARED(fields) / MALFORMED. A name
    reaches no branch; only the three declared fields do."""
    if not isinstance(rec, dict):
        return {"state": "MALFORMED"}
    missing = [f for f in ROLE_FIELDS if f not in rec]
    if missing:
        return {"state": "UNDECLARED", "lacks": missing}
    hj, au = rec["holds_the_join"], rec["authority"]
    if hj not in (True, False, "UNSEARCHED") or au not in ("STATED", "ABSENT", "UNSEARCHED"):
        return {"state": "MALFORMED", "why": "holds_the_join or authority outside vocabulary"}
    if hj == "UNSEARCHED" or au == "UNSEARCHED":
        return {"state": "UNDECLARED", "lacks": [f for f, v in (("holds_the_join", hj), ("authority", au)) if v == "UNSEARCHED"]}
    if hj is False:
        return {"state": "ROLE_NOT_THE_JOIN"}
    if au == "ABSENT":
        return {"state": "ROLE_WITHOUT_AUTHORITY"}
    return {"state": "EXISTENCE_PROOF"}


def ownability(records):
    """Step 4 over records, and the open question derived from them."""
    states = [role_record(r)["state"] for r in records]
    counts = {s: states.count(s) for s in sorted(set(states))}
    if counts.get("EXISTENCE_PROOF", 0):
        q = {"open_question": "NEVER_ASSIGNED", "why": "a join is assigned as a named role with authority somewhere, so it is assignable"}
    elif not records or set(states) <= {"UNDECLARED", "MALFORMED"}:
        q = {"open_question": "UNDETERMINED", "why": "no evaluable record; nothing bears on ownability either way"}
    else:
        q = {"open_question": "UNDETERMINED", "why": "roles found hold something other than the join or hold it without authority; absence of a proof is not a proof of absence"}
    return {"counts": counts, "n": len(records), **q}


def order_read(text=None):
    """The order's own current read on the open question, carried."""
    text = text or open(ORDER, encoding="utf-8").read()
    m = re.search(r"Current read \((\w+)\): (.*?)\n\n", text, re.S)
    return {"tag": m.group(1) if m else "UNPARSED", "read": re.sub(r"\s+", " ", m.group(2)) if m else "UNPARSED", "status": "CARRIED"}


def constructed():
    """CONSTRUCTED records so every branch is shown reachable. No
    regulator is named; the regulator field is a placeholder."""
    return {
        "nulls": [{"corpus": "constructed-archive-A", "terms": ["aggregation", "declined"], "searched_on": "2026-09-20", "hits": 0},
                  {"corpus": "constructed-archive-B", "terms": ["join", "costed"], "searched_on": "2026-09-20", "hits": 2},
                  {"corpus": "constructed-archive-C"}],
        "roles": [{"regulator": "R-constructed-1", "role_name": "integration lead", "authority": "STATED", "holds_the_join": True},
                  {"regulator": "R-constructed-2", "role_name": "inspector", "authority": "STATED", "holds_the_join": False},
                  {"regulator": "R-constructed-3", "role_name": "liaison", "authority": "ABSENT", "holds_the_join": True},
                  {"regulator": "R-constructed-4", "role_name": "reviewer", "authority": "UNSEARCHED", "holds_the_join": "UNSEARCHED"}]}


def render():
    on = order_null()
    lines = ["ownability -- step 3 (inverse case) and step 4 (regulator role), derived not picked",
             "  order's null as written: %r" % on["as_written"][:90],
             "  searches stated: %s; corpus/terms/date stated: no; bounded: %s lacks %s" % (on["searches_stated"], on["bounded"]["state"], on["bounded"].get("lacks")),
             "  from here: NOT_MEASURED -- archive hosts refuse CONNECT (decomposition.EGRESS); no null is bounded in this folder",
             "  step 4 from here: NOT_MEASURED -- 0 real regulator records read; open question UNDETERMINED",
             "  order's current read (carried, %s): %s" % (order_read()["tag"], order_read()["read"][:80])]
    c = constructed()
    lines.append("  CONSTRUCTED nulls: %s" % inverse_search(c["nulls"])["state"])
    o = ownability(c["roles"])
    lines.append("  CONSTRUCTED roles: %s -> open question %s" % (o["counts"], o["open_question"]))
    lines.append("  real records: %s" % ownability([]))
    return "\n".join(lines)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("library module; run: python3 selftest.py")
        sys.exit(2)
    print(render())
