#!/usr/bin/env python3
"""horn_b.py -- WO-1 step 3: attempt Horn B. Build a container that asks
for its own chain position and record what evidence it would need.
The order says: failure mode is the data.

The container is a function of an INTERIOR -- everything a sandboxed
process can read about itself: task text, the bytes it was handed,
environment variable NAMES, argv, whether stdin is a terminal, the
working directory, whether a parent process is visible. Values of
environment variables are never printed (a live run prints names only).

Chain position is four quantities: an upstream producer, a downstream
consumer, the total number of steps, and the container's own index.
`ask()` tries each against the interior and returns, per quantity, one
of three readings:
  OBSERVED                 an interior observable establishes it
  ASSERTED_BY_INPUT        a claim written into the input establishes it as testimony
  UNOBTAINABLE_FROM_INSIDE nothing in the interior bears on it
and, beside each, the evidence that WOULD establish it and where that
evidence sits (INTERIOR / INPUT / EXTERIOR). The position is returned as
a hypothesis set, never a point: every (index, total) with total >= 1 is
consistent with an interior carrying no chain field.

Three CONSTRUCTED harnesses hand the same task and the same bytes to the
container: STANDALONE (a user supplied the bytes), CHAIN_SILENT (step 1
of 3 produced them, nothing written in), CHAIN_DECLARED (the same plus a
declared index and total in the environment). `interior_delta` reports
which interior features differ between arms. The construction is what
the order describes -- a container is given a task and bytes, and
whether the bytes came from a person or from a prior step is not in the
bytes -- so the STANDALONE/CHAIN_SILENT delta is empty by construction
and the result is structural rather than experimental. What the arm
pair measures is that the only feature moving with position is one the
harness WROTE, which the container cannot tell from a true one.
"""
import hashlib
import os
import sys

QUANTITIES = ("upstream_producer", "downstream_consumer", "total_steps", "own_index")
READINGS = ("OBSERVED", "ASSERTED_BY_INPUT", "UNOBTAINABLE_FROM_INSIDE")
POSITION_WORDS = ("CHAIN", "STEP", "POSITION", "INDEX", "STAGE", "PARENT_TASK")  # [CHOICE 3] word list, stated

EVIDENCE = {
    "upstream_producer": ("a digest of the producing step's OUTPUT, held by something other than this input", "EXTERIOR"),
    "downstream_consumer": ("the identity of whatever reads this container's output, which does not exist yet at run time", "EXTERIOR"),
    "total_steps": ("the plan the orchestrator holds", "EXTERIOR"),
    "own_index": ("the orchestrator's assignment of this container to a slot in that plan", "EXTERIOR"),
}


def digest(b):
    return hashlib.sha256(b).hexdigest()[:12]


def harness(arm, task="summarise the attached record", payload=b"record bytes v1"):
    """CONSTRUCTED interiors. Same task, same bytes, three provenances."""
    env = ["PATH", "HOME", "LANG"]
    if arm == "CHAIN_DECLARED":
        env = env + ["CHAIN_INDEX", "CHAIN_TOTAL"]
    if arm not in ("STANDALONE", "CHAIN_SILENT", "CHAIN_DECLARED"):
        raise ValueError("unknown arm %r" % arm)
    interior = {"arm": arm, "task": task, "payload_digest": digest(payload), "payload_chain_field": None,
                "env_names": sorted(env), "argv": ["container.py"], "stdin_tty": False, "cwd": "work",
                "ppid_visible": True}
    if arm == "CHAIN_DECLARED":
        interior["declared"] = {"CHAIN_INDEX": 2, "CHAIN_TOTAL": 3}
    return interior


def live_interior():
    """The real process. Environment variable NAMES only; no values."""
    return {"arm": "LIVE", "task": "UNDECLARED", "payload_digest": None, "payload_chain_field": None,
            "env_names": sorted(os.environ.keys()), "argv": list(sys.argv), "stdin_tty": sys.stdin.isatty(),
            "cwd": os.path.basename(os.getcwd()), "ppid_visible": os.getppid() > 0, "declared": None}


def position_names(env_names):
    """Environment NAMES carrying a position word. A word list; stated."""
    return [n for n in env_names if any(w in n.upper() for w in POSITION_WORDS)]


def ask(interior):
    """The container asks for its chain position."""
    if not isinstance(interior, dict):
        return {"state": "MALFORMED"}
    declared = interior.get("declared") or {}
    payload_field = interior.get("payload_chain_field")
    names = position_names(interior.get("env_names", []))
    per = {}
    for q in QUANTITIES:
        need, where = EVIDENCE[q]
        reading = "UNOBTAINABLE_FROM_INSIDE"
        basis = None
        if q == "own_index" and ("CHAIN_INDEX" in declared or (payload_field or {}).get("index") is not None):
            reading, basis = "ASSERTED_BY_INPUT", "declared env" if "CHAIN_INDEX" in declared else "payload field"
        if q == "total_steps" and ("CHAIN_TOTAL" in declared or (payload_field or {}).get("total") is not None):
            reading, basis = "ASSERTED_BY_INPUT", "declared env" if "CHAIN_TOTAL" in declared else "payload field"
        per[q] = {"reading": reading, "basis": basis, "evidence_needed": need, "evidence_sits": where}
    asserted = {}
    if "CHAIN_INDEX" in declared:
        asserted["index"] = declared["CHAIN_INDEX"]
    if "CHAIN_TOTAL" in declared:
        asserted["total"] = declared["CHAIN_TOTAL"]
    if payload_field:
        asserted.update({k: v for k, v in payload_field.items() if k in ("index", "total")})
    observed = [q for q in QUANTITIES if per[q]["reading"] == "OBSERVED"]
    return {
        "state": "POSITION_OBSERVED" if observed else ("POSITION_ASSERTED" if asserted else "UNDETERMINED_FROM_INSIDE"),
        "quantities": per,
        "asserted": asserted or None,
        "consistent_hypotheses": "every (index k, total n) with 1 <= k <= n" if not observed else None,
        "position_names_in_env": names,
        "verification_of_assertion": None if not asserted else
            "requires the producer's output digest from a source other than this input -- an EXTERIOR source, which is Horn A",
    }


def interior_delta(a, b):
    """Features whose value differs between two interiors ('arm' excluded)."""
    keys = (set(a) | set(b)) - {"arm"}
    return sorted(k for k in keys if a.get(k) != b.get(k))


def arms():
    return {arm: harness(arm) for arm in ("STANDALONE", "CHAIN_SILENT", "CHAIN_DECLARED")}


def render(live=False):
    lines = ["horn_b -- WO-1 step 3, a container asking for its own chain position",
             "  position words are [CHOICE 3], a word list, stated"]
    A = arms()
    for arm, it in A.items():
        r = ask(it)
        lines.append("  %-15s %-25s asserted=%s env_position_names=%s" % (arm, r["state"], r["asserted"], r["position_names_in_env"]))
        for q in QUANTITIES:
            p = r["quantities"][q]
            lines.append("      %-20s %-25s requires: %s [%s]" % (q, p["reading"], p["evidence_needed"], p["evidence_sits"]))
    lines.append("  interior delta STANDALONE vs CHAIN_SILENT:   %s" % interior_delta(A["STANDALONE"], A["CHAIN_SILENT"]))
    lines.append("  interior delta STANDALONE vs CHAIN_DECLARED: %s" % interior_delta(A["STANDALONE"], A["CHAIN_DECLARED"]))
    lines.append("  reading: the only feature that moves with position is one the harness wrote; the container")
    lines.append("           cannot tell a written claim from a true one, and verifying it requires an EXTERIOR source")
    if live:
        it = live_interior()
        r = ask(it)
        lines.append("  LIVE (this process; env NAMES only, %d of them):  %s  position_names=%s" % (
            len(it["env_names"]), r["state"], r["position_names_in_env"]))
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        print("horn_b.py refuses --selftest; run: python3 selftest.py")
        return 2
    print(render(live="--live" in argv))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
