# SPDX-License-Identifier: CC0-1.0
"""
Selftest for cycle-ledger (Deliverable 1 cycle_ledger.py, Deliverable 2
rate_gap.py). Null tests run both directions:

  Deliverable 1 -- the SEED (marker's corridor) returns AHEAD == 0, so the
  claim's support is absent HERE; a CONSTRUCTED cycle carrying a DECISION
  element with decision_latency_binds TRUE returns AHEAD > 0, so the tool
  can say "the claim holds here."

  Deliverable 2 -- a CONSTRUCTED structural series returns STRUCTURAL; a
  CONSTRUCTED kept-up series with an empty unrecorded set returns
  MATURITY_GAP. Neither verdict is constant.

Every render line is asserted <= 60 columns (the build constraint).

Run:  python3 cycle-ledger/selftest_cll.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import cycle_ledger as cl        # noqa: E402
import rate_gap as rg            # noqa: E402

_checks = 0
_failed = 0


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


# ------------------------------------------------------------------ Del 1

# validate_element enforces the record's own rule.
try:
    cl.validate_element(cl.Element("x", "d", cl.HARDWARE,
                                   decision_latency_binds=True))
    check(False, "decision_latency_binds TRUE on non-DECISION must raise")
except cl.BadElement:
    check(True, "decision_latency_binds TRUE on non-DECISION raises")

# a DECISION element with the flag TRUE is legal.
try:
    cl.validate_element(cl.Element("x", "d", cl.DECISION,
                                   decision_latency_binds=True))
    check(True, "DECISION + decision_latency_binds TRUE is legal")
except cl.BadElement:
    check(False, "DECISION + decision_latency_binds TRUE should be legal")

# bad rate_setter / absorber rejected.
try:
    cl.validate_element(cl.Element("x", "d", "NOPE"))
    check(False, "bad rate_setter must raise")
except cl.BadElement:
    check(True, "bad rate_setter raises")
try:
    cl.validate_element(cl.Element("x", "d", cl.HARDWARE,
                                   currently_absorbed_by="NOPE"))
    check(False, "bad absorber must raise")
except cl.BadElement:
    check(True, "bad absorber raises")

for e in cl.SEED:
    cl.validate_element(e)
check(True, "SEED validates")

# NULL, direction A: the SEED returns AHEAD == 0 (claim support absent here).
cS = cl.classify(cl.SEED)
check(cS["ahead"] == 0, "SEED AHEAD == 0")
check(cS["claim_holds_here"] is False, "SEED claim_holds_here is False")
check(cS["tied"] == len(cl.SEED), "SEED all TIED (every rate_setter is tied)")
check(cS["behind"] == 3, "SEED BEHIND == 3 (parallel/fault/leave-vehicle)")

# NULL, direction B: a cycle with a DECISION-bound element returns AHEAD > 0.
decision_cycle = list(cl.SEED) + [
    cl.Element("route_choice", "bound by choosing, not executing",
               cl.DECISION, decision_latency_binds=True)]
cD = cl.classify(decision_cycle)
check(cD["ahead"] == 1, "decision cycle AHEAD == 1")
check(cD["claim_holds_here"] is True, "decision cycle claim_holds_here True")

# the two directions differ -> classify is not constant.
check(cS["claim_holds_here"] != cD["claim_holds_here"],
      "claim_holds_here is not constant across the two cycles")

# histogram: KEY READOUT fraction.
h = cl.rate_setter_histogram(cl.SEED)
check(h["decision_binds_fraction"] == 0.0, "SEED decision fraction 0.0")
hD = cl.rate_setter_histogram(decision_cycle)
check(hD["decision_binds_fraction"] > 0.0, "decision cycle fraction > 0")
# empty cycle: fraction is None, not 0 (absent-vs-known-negative).
hE = cl.rate_setter_histogram([])
check(hE["decision_binds_fraction"] is None,
      "empty cycle fraction is None, not 0")

# unnotated register: total and safety subset.
u = cl.unnotated_register(cl.SEED)
check(u["total"] == 14, "SEED unnotated total 14")
check(u["safety_count"] == 7, "SEED unnotated safety 7")
check("backing" in u["safety_relevant"], "backing is safety-relevant")

# relocation ledger: only OPERATOR-absorbed leave the sheet.
r = cl.relocation_ledger(cl.SEED)
op = [e.element_id for e in cl.SEED if e.currently_absorbed_by == cl.OPERATOR]
check(len(r["wage_lines_leaving"]) == len(op),
      "wage lines == OPERATOR-absorbed count")
check("gate" not in r["wage_lines_leaving"],
      "COUNTERPARTY-absorbed gate does not leave the sheet")

# serial-interface condition: one per TERMINAL element.
si = cl.serial_interface_condition(cl.SEED)
nterm = sum(1 for e in cl.SEED if e.rate_setter == cl.TERMINAL)
check(len(si["conditions"]) == nterm, "one condition per TERMINAL element")
check(str(nterm) in si["precondition"], "precondition names the count")

# render <= 60 columns.
for ln in cl.render(cl.SEED).splitlines():
    check(len(ln) <= 60, "Del1 render line <= 60: %r" % ln)

# --selftest refuses (rc 2) via subprocess.
import subprocess  # noqa: E402
rc = subprocess.call([sys.executable,
                      os.path.join(_HERE, "cycle_ledger.py"), "--selftest"],
                     stderr=subprocess.DEVNULL)
check(rc == 2, "cycle_ledger.py --selftest exits 2")

# ------------------------------------------------------------------ Del 2

# validate rejects a bad event class and a bad date.
try:
    rg.validate([rg.EnvEvent("e", "NOPE", "2026-04-01")], [])
    check(False, "bad event_class must raise")
except rg.BadEvent:
    check(True, "bad event_class raises")
try:
    rg.validate([rg.EnvEvent("e", rg.CLOSURE, "2026-13-01")], [])
    check(False, "bad date must raise")
except ValueError:
    check(True, "bad date raises")

# NULL, direction A: structural demo -> STRUCTURAL with nonzero unrecorded.
ev, up = rg._demo_structural()
gS = rg.gap_verdict(ev, up)
check(gS["verdict"] == rg.GAP_STRUCTURAL, "structural demo -> STRUCTURAL")
check(gS["rate_verdict"] == rg.STRUCTURAL, "structural demo rate STRUCTURAL")
check(gS["unrecorded_total"] > 0, "structural demo unrecorded > 0")

# NULL, direction B: maturity demo -> MATURITY_GAP with empty unrecorded.
ev, up = rg._demo_maturity()
gM = rg.gap_verdict(ev, up)
check(gM["verdict"] == rg.GAP_MATURITY, "maturity demo -> MATURITY_GAP")
check(gM["rate_verdict"] == rg.MATURITY_GAP, "maturity demo rate MATURITY_GAP")
check(gM["unrecorded_total"] == 0, "maturity demo unrecorded == 0")

# the two verdicts differ -> gap_verdict is not constant.
check(gS["verdict"] != gM["verdict"], "gap_verdict is not constant")

# the two conditions are kept apart: a rate-structural series with an EMPTY
# unrecorded set is UNDETERMINED, not STRUCTURAL (a refresh gap, not absence).
ev2, up2 = [], []
base = rg.date(2026, 4, 1)
for i in range(20):
    eid = "z%02d" % i
    d = rg._add_days(base, i * 3)
    ev2.append(rg.EnvEvent(eid, rg.CLOSURE, d.isoformat()))
    # record every event but late and clustered so dE>dM per-window is
    # sustained while the unrecorded set stays empty.
    up2.append(rg.RecordUpdate(eid, rg._add_days(base, 70 + i).isoformat()))
gU = rg.gap_verdict(ev2, up2)
check(gU["unrecorded_total"] == 0, "all-recorded control: unrecorded 0")
check(gU["verdict"] != rg.GAP_STRUCTURAL,
      "sustained excess with empty unrecorded is NOT STRUCTURAL")

# lag distribution: recorded event has a numeric lag; an unrecorded class is
# NO_RECORDED, not a large lag.
ev3 = [rg.EnvEvent("a", rg.CLOSURE, "2026-04-01"),
       rg.EnvEvent("b", rg.REPAINT, "2026-04-10")]
up3 = [rg.RecordUpdate("a", "2026-04-06")]     # b never recorded
ld = rg.lag_distribution(ev3, up3)
check(ld[rg.CLOSURE]["state"] == "OK", "CLOSURE recorded -> OK")
check(ld[rg.CLOSURE]["median"] == 5, "CLOSURE lag median 5")
check(ld[rg.REPAINT]["state"] == rg.NO_RECORDED,
      "REPAINT class with no recorded event -> NO_RECORDED")
un = rg.unrecorded_set(ev3, up3)
check(un["total"] == 1 and "b" in un["events"], "b is in the unrecorded set")
check(un["lag"] == rg.UNRECORDED, "unrecorded lag state is UNRECORDED")

# anomalous: a record dated BEFORE its event is flagged, not folded in.
ev4 = [rg.EnvEvent("q", rg.CLOSURE, "2026-04-10")]
up4 = [rg.RecordUpdate("q", "2026-04-05")]
ld4 = rg.lag_distribution(ev4, up4)
check(ld4[rg.CLOSURE]["state"] == rg.NO_RECORDED,
      "anomalous-only class has no numeric lag")
check(ld4[rg.CLOSURE]["anomalous"] == 1, "anomalous record counted apart")

# empty input: rate series has zero windows, no crash.
check(rg.rate_series([], [])["windows"] == 0, "empty input -> 0 windows")

# sustained_excess / rate_verdict are the IMPORTED objects.
check(rg.sustained_excess is rg.rate_form.sustained_excess,
      "sustained_excess is imported from rate_form, not redefined")
check(rg.rate_verdict is rg.rate_form.rate_verdict,
      "rate_verdict is imported from rate_form, not redefined")

# render <= 60 columns (both demos).
for demo in (rg._demo_structural, rg._demo_maturity):
    ev, up = demo()
    for ln in rg.render(ev, up).splitlines():
        check(len(ln) <= 60, "Del2 render line <= 60: %r" % ln)

# --selftest refuses (rc 2).
rc = subprocess.call([sys.executable,
                      os.path.join(_HERE, "rate_gap.py"), "--selftest"],
                     stderr=subprocess.DEVNULL)
check(rc == 2, "rate_gap.py --selftest exits 2")

# ------------------------------------------------------------------ report
print("selftest: %d checks, %d failed" % (_checks, _failed))
sys.exit(1 if _failed else 0)
