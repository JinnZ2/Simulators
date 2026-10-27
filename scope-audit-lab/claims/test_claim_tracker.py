#!/usr/bin/env python3
"""Checks for claim_tracker.py (SAL-WO4). Stdlib only. Uses a temp stream;
the committed claims.jsonl is read, never written, here."""
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import claim_tracker as ct  # noqa: E402

checks = []


def ok(name, cond):
    checks.append((name, bool(cond)))


def ev(i, cid, state, ed="2026-10-26", ob="2026-10-27", sup=None, src=("u",)):
    return dict(event_id=i, claim_id=cid, state=state, event_date=ed, observed_at=ob,
                depth="search_result", summary="s", sources=list(src), supersedes=sup)


real = ct.read()
ok("committed stream valid", ct.validate_stream(real) == [])
ok("four claims seeded", len(ct.heads(real)) == 4)
ok("Anthropic-attributed item NOT_LOCATED, no event date",
   ct.heads(real)["anthropic-attributed-3sat"]["state"] == "NOT_LOCATED"
   and ct.heads(real)["anthropic-attributed-3sat"]["event_date"] is None)

with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "s.jsonl"
    ct.append(ev("A1", "c", "CLAIMED_UNREFEREED"), p)
    ct.append(ev("A2", "c", "UNDER_OUTSIDE_REVIEW", ed="2026-10-30", ob="2026-11-01", sup="A1"), p)
    s = ct.read(p)
    ok("chain head is the latest event", ct.heads(s)["c"]["event_id"] == "A2")
    t = ct.time_in_state(s, "2026-11-10")["c"]
    ok("time in state measured two ways", t == {"state": "UNDER_OUTSIDE_REVIEW", "by_event": 11, "by_registry": 9})

    def refused(e):
        try:
            ct.append(e, p)
        except ct.TrackerError:
            return True
        return False

    ok("repeated id refused (no edit in place)", refused(ev("A1", "c", "REFUTED", sup="A2")))
    ok("unknown state refused", refused(ev("A3", "c", "FALSE")))
    ok("superseding another claim refused", refused(ev("A4", "other", "REFUTED", sup="A2")))
    ok("forward reference refused", refused(ev("A5", "c", "REFUTED", sup="A9")))
    ok("event dated after observation refused", refused(ev("A6", "c", "REFUTED", ed="2026-12-01", ob="2026-11-02", sup="A2")))
    ok("located state without a source refused", refused(ev("A7", "c", "WITHDRAWN", sup="A2", src=())))
    ok("observed before the superseded event refused", refused(ev("A8", "c", "REFUTED", ed="2026-10-26", ob="2026-10-28", sup="A2")))
    ok("stream unchanged by refusals", len(ct.read(p)) == 2)

src = (HERE / "claim_tracker.py").read_text(encoding="utf-8")
ok("module refuses --selftest", "sys.exit(2)" in src)
failed = [n for n, v in checks if not v]
for n, v in checks:
    print(("PASS " if v else "FAIL ") + n)
print(f"checks: {len(checks)}   failed: {len(failed)}")
sys.exit(1 if failed else 0)
