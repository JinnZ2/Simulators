#!/usr/bin/env python3
"""clause_audit.py -- WO-1 step 1: audit ACS / OWASP Top 10 for Agentic
Applications 2026 clause by clause for any requirement that places
chain-position information INSIDE the executing agent. The order's
expected result is none, and it says a null result is the finding.

THE STANDARD IS NOT READ HERE. Egress from this environment is an
allowlist; the hosts that carry the two documents answered 403 to
CONNECT, measured and timestamped in EGRESS below. Nothing is fetched
at run time and no clause text is supplied from memory. What is
audited is the order's OWN five-bullet summary of the standard, carried
as `source: CARRIED`, so the run state on the delivery is
NOT_RUN_ON_STANDARD and the count is a count over the summary.

`info_location` is a DECLARED coding per clause -- GATEWAY / AGENT /
BOTH / UNDECLARED -- and is never inferred from the clause text. The
text reaches no check (a word list deciding where a requirement puts
information is the failure this tree records as T1-1). A clause with
no declared location is counted apart, never as GATEWAY.

The null the order names has a shape worth stating: over a CARRIED
summary, the count can only be nonzero if the summariser carried an
in-agent clause, so a zero here is a property of the five bullets and
not of the standard. The reachable branch is shown on a planted clause.
"""
import json
import sys

LOCATIONS = ("GATEWAY", "AGENT", "BOTH", "UNDECLARED")
SOURCES = ("STANDARD", "CARRIED")
RUN_STATES = ("RUN_ON_STANDARD", "NOT_RUN_ON_STANDARD", "EMPTY")

# Measured, not asserted. Re-measure with `curl -m 12 https://<host>/` and
# the proxy's status endpoint; do not re-measure inside this module.
EGRESS = {
    "measured_at": "2026-09-19T16:55Z",
    "refused": {"owasp.org:443": "gateway answered 403 to CONNECT", "genai.owasp.org:443": "gateway answered 403 to CONNECT"},
    "control": {"github.com:443": "connects (HTTP response received)"},
}

# The order's summary, carried verbatim per bullet. Location codings are
# this build's readings of the order's own sentence "all of the above
# sits in the GATEWAY's external top-down view" -- declared, not derived.
CARRIED = [
    {"id": "S-1", "text": "per-agent isolation and lineage tracking", "info_location": "GATEWAY", "source": "CARRIED"},
    {"id": "S-2", "text": "gateway traces every request to originating user session", "info_location": "GATEWAY", "source": "CARRIED"},
    {"id": "S-3", "text": "cross-agent state transfer requires explicit policy authorization, not implicit trust", "info_location": "GATEWAY", "source": "CARRIED"},
    {"id": "S-4", "text": "provenance and trust status retained per retrieved item", "info_location": "GATEWAY", "source": "CARRIED"},
    {"id": "S-5", "text": "runtime interception via middleware hooks", "info_location": "GATEWAY", "source": "CARRIED"},
]


def code_clause(c):
    if not isinstance(c, dict):
        return {"state": "MALFORMED", "why": "not a dict"}
    loc = c.get("info_location", "UNDECLARED")
    src = c.get("source", "CARRIED")
    if loc not in LOCATIONS or src not in SOURCES:
        return {"id": c.get("id"), "state": "MALFORMED", "why": "value outside vocabulary"}
    return {"id": c.get("id"), "state": "CODED", "info_location": loc, "source": src,
            "inside_agent": loc in ("AGENT", "BOTH")}


def audit(clauses):
    coded = [code_clause(c) for c in clauses]
    good = [c for c in coded if c["state"] == "CODED"]
    if not clauses:
        return {"run_state": "EMPTY", "n": 0, "inside_agent": None, "gateway_only": None, "undeclared": None, "malformed": 0}
    on_standard = any(c["source"] == "STANDARD" for c in good)
    return {
        "run_state": "RUN_ON_STANDARD" if on_standard else "NOT_RUN_ON_STANDARD",
        "n": len(good),
        "inside_agent": sum(1 for c in good if c["inside_agent"]),
        "gateway_only": sum(1 for c in good if c["info_location"] == "GATEWAY"),
        "undeclared": sum(1 for c in good if c["info_location"] == "UNDECLARED"),
        "malformed": len(coded) - len(good),
        "inside_ids": [c["id"] for c in good if c["inside_agent"]],
        "egress": EGRESS,
    }


def render(clauses=None):
    clauses = CARRIED if clauses is None else clauses
    a = audit(clauses)
    lines = ["clause_audit -- WO-1 step 1, chain-position information INSIDE the executing agent",
             "  standard hosts, measured %s: %s; control %s" % (
                 EGRESS["measured_at"], "; ".join("%s %s" % kv for kv in EGRESS["refused"].items()),
                 "; ".join("%s %s" % kv for kv in EGRESS["control"].items())),
             "  run state: %s" % a["run_state"]]
    if a["run_state"] != "EMPTY":
        lines.append("  clauses %d  inside_agent %d  gateway_only %d  undeclared %d  malformed %d" % (
            a["n"], a["inside_agent"], a["gateway_only"], a["undeclared"], a["malformed"]))
        for c in clauses:
            cc = code_clause(c)
            lines.append("    %-5s %-10s %-9s %s" % (cc.get("id"), cc.get("info_location", cc["state"]), cc.get("source", ""), c.get("text", "")[:60] if isinstance(c, dict) else ""))
    lines.append("  reading: a zero over a CARRIED summary is a property of what the summary carried; the")
    lines.append("           standard's own clauses have not been read from here")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        print("clause_audit.py refuses --selftest; run: python3 selftest.py")
        return 2
    if "--clauses" in argv:
        path = argv[argv.index("--clauses") + 1]
        with open(path) as f:
            cl = [json.loads(l) for l in f if l.strip()]
        print(render(cl))
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
