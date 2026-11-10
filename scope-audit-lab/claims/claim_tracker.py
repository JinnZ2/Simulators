#!/usr/bin/env python3
"""SAL-WO4: a live claim registry for the AI-generated mathematics claims of
October 2026, run as the continuation report's sec. 7 tracking protocol.

Protocol, as the report states it: one initial event per claim with its own
scope notes as evidence; further events appended as working-group
statements, withdrawals or registrations arrive; no status ever edited in
place. The time each claim spends in each state is the measurement, and it
exists only if it is recorded from the start.

Two dates are kept apart on every event:
    event_date    the date the claimed thing happened, as the source reports it
    observed_at   the date this registry recorded it, at the stated depth
A registry that only had one of them could not say whether a long time in a
state was the claim's or the registry's.

States (none is a judgement on the mathematics):
    CLAIMED_UNREFEREED      announced; no outside review has reported
    UNDER_OUTSIDE_REVIEW    a named outside group is reviewing
    CERTIFIED_FORMAL_ONLY   reviewers certify the formal statement only
    CERTIFIED               reviewers certify the headline claim
    REFUTED                 reviewers or the claimant report an error
    WITHDRAWN               the claimant withdraws
    NOT_LOCATED             the claim's own source cannot be found at the stated depth

The registry is written by a Claude model. Items attributed to Anthropic or
Claude are recorded at the depth reached and are not adjudicated.

    python3 claim_tracker.py               current state and time-in-state per claim
    python3 claim_tracker.py --validate    stream checks
The module refuses --selftest; checks live in test_claim_tracker.py.
"""
import json
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
STREAM = HERE / "claims.jsonl"

STATES = ("CLAIMED_UNREFEREED", "UNDER_OUTSIDE_REVIEW", "CERTIFIED_FORMAL_ONLY",
          "CERTIFIED", "REFUTED", "WITHDRAWN", "NOT_LOCATED")
DEPTHS = ("search_result", "primary")
REQUIRED = ("event_id", "claim_id", "state", "event_date", "observed_at", "depth",
            "summary", "sources", "supersedes")


class TrackerError(ValueError):
    pass


def check_event(e):
    missing = [k for k in REQUIRED if k not in e]
    if missing:
        raise TrackerError(f"{e.get('event_id')}: missing {missing}")
    if e["state"] not in STATES:
        raise TrackerError(f"{e['event_id']}: state {e['state']!r} not in {STATES}")
    if e["depth"] not in DEPTHS:
        raise TrackerError(f"{e['event_id']}: depth {e['depth']!r} not in {DEPTHS}")
    if e["event_date"] is not None:
        date.fromisoformat(e["event_date"])
    date.fromisoformat(e["observed_at"])
    if e["state"] != "NOT_LOCATED" and not e["sources"]:
        raise TrackerError(f"{e['event_id']}: a located state needs a source")
    if e["event_date"] and e["event_date"] > e["observed_at"]:
        raise TrackerError(f"{e['event_id']}: event dated after it was observed")


def read(path=STREAM):
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def validate_stream(events):
    """Unique ids; supersedes points to an earlier event of the same claim;
    observed_at never goes backwards along a claim's chain."""
    out, seen = [], {}
    for e in events:
        try:
            check_event(e)
        except (TrackerError, ValueError) as x:
            out.append(str(x))
            continue
        if e["event_id"] in seen:
            out.append(f"{e['event_id']}: id repeated (edit in place?)")
        s = e["supersedes"]
        if s is not None:
            if s not in seen:
                out.append(f"{e['event_id']}: supersedes {s}, not earlier in the stream")
            elif seen[s]["claim_id"] != e["claim_id"]:
                out.append(f"{e['event_id']}: supersedes an event of another claim")
            elif seen[s]["observed_at"] > e["observed_at"]:
                out.append(f"{e['event_id']}: observed before the event it supersedes")
        seen[e["event_id"]] = e
    return out


def append(event, path=STREAM):
    """Append one event; refuses anything the stream check would reject."""
    events = read(path) if Path(path).exists() else []
    problems = validate_stream(events + [event])
    if problems:
        raise TrackerError("; ".join(problems))
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=True) + "\n")


def heads(events):
    sup = {e["supersedes"] for e in events if e["supersedes"]}
    return {e["claim_id"]: e for e in events if e["event_id"] not in sup}


def time_in_state(events, as_of):
    """Per claim: days in the current state, measured two ways.
    by_event: from the event_date (None if the source gave none)
    by_registry: from the observed_at"""
    as_of = date.fromisoformat(as_of)
    out = {}
    for cid, e in sorted(heads(events).items()):
        ed = (as_of - date.fromisoformat(e["event_date"])).days if e["event_date"] else None
        out[cid] = {"state": e["state"], "by_event": ed,
                    "by_registry": (as_of - date.fromisoformat(e["observed_at"])).days}
    return out


def render(as_of=None):
    events = read()
    as_of = as_of or max(e["observed_at"] for e in events)
    t = time_in_state(events, as_of)
    lines = ["scope-audit-lab / claims / claim_tracker.py", "=" * 64,
             f"{len(events)} events, {len(t)} claims, as of {as_of}", "",
             f"{'claim':<32} {'state':<22} {'days (event)':>12} {'days (registry)':>15}"]
    for cid, v in t.items():
        be = "--" if v["by_event"] is None else str(v["by_event"])
        lines.append(f"{cid:<32} {v['state']:<22} {be:>12} {v['by_registry']:>15}")
    lines += ["", "no verdict on any claim; depth per event is in claims.jsonl"]
    return "\n".join(lines)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("claim_tracker.py is a registry; run: python3 test_claim_tracker.py")
        sys.exit(2)
    if "--validate" in sys.argv[1:]:
        p = validate_stream(read())
        print("\n".join(p) if p else "stream valid")
        sys.exit(1 if p else 0)
    print(render())
