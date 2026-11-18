"""expiry_register.py -- every PENDING / UNKNOWN in this repo, classified, with an
expiry condition where one applies. CC0, stdlib only.

Work order 2026-11-10 (cross-model audit follow-up), item 1(b), confirmed by the
operator 2026-11-11. Source of the confound: Kimi audit C7 (unfalsifiability
drift): "every UNKNOWN must carry an expiry condition (an instrument class,
sensitivity, and protocol whose null result would downgrade the entry to
'absent-at-this-sensitivity')".

The counted base. "43 PENDING + 36 UNKNOWN" reproduces on this tree as
    PENDING  = lines containing the string PENDING       (grep -rn PENDING)      43
    UNKNOWN  = lines containing the WORD UNKNOWN          (grep -rnw UNKNOWN)     36
The two counts use different rules (PENDING has 45 occurrences on 43 lines;
UNKNOWN has 43 lines as a substring, 36 as a word). The rule each count used is
this session's reconstruction from the numbers, not a stated rule; recorded.

A count of a token is not a count of slots. Each occurrence gets one class:

    SLOT      a value held open in a record or ledger (a quantity not yet measured)
    EMITTER   code that returns the token under a condition the code states
    DEFAULT   an initial value a run overwrites
    VOCAB     a definition of the token: enum member, sentinel, rank map, counter
    RULE      prose stating the rule that a slot is held open
    MENTION   prose or a comment pointing at a slot or emitter registered elsewhere
    ARCHIVE   an archived copy of prose (README archive)
    OTHER_SENSE  the token used for something else (an unrecognised tag)

Only SLOT, EMITTER and DEFAULT carry expiry_condition. It is the string "void"
(no exit defined) or a dict with instrument_class, sensitivity, protocol,
provenance. sensitivity may be "void" (exit incomplete). Nothing fails on a
missing exit; the count is reported (work order: "flag as 'no exit defined';
report, do not fail").

ABSENT_AT_SENSITIVITY(<value>) is the state a slot moves to when its exit
instrument runs at a stated sensitivity and returns null. It is a scoped
absence, never a bare "absent". No slot in this repo is in that state today;
the count is printed as a visible zero.

Delivered files are not edited (docs/DCEA_v0.1.md and the road-driver ledger
are sha-pinned in docs/DCEA_checks.md). Exits live here, beside them.

    python3 calibration/expiry_register.py             # the register
    python3 calibration/expiry_register.py --selftest  # checks
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLASSES = ("SLOT", "EMITTER", "DEFAULT", "VOCAB", "RULE", "MENTION", "ARCHIVE", "OTHER_SENSE")
CARRY_EXPIRY = ("SLOT", "EMITTER", "DEFAULT")
EXPIRY_KEYS = ("instrument_class", "sensitivity", "protocol", "provenance")
SCOPED = re.compile(r"^ABSENT_AT_SENSITIVITY\((.+)\)$")
SELF = "calibration/expiry_register.py"


def E(instrument, protocol, provenance, sensitivity="void"):
    return dict(instrument_class=instrument, sensitivity=sensitivity, protocol=protocol, provenance=provenance)


_RUN = "DERIVED: the exit is the code path that replaces the token; read off the code"
_TXT = "DERIVED: named in the record's own text at this line"

# (path, line, quote that must be on that line, class, slot id or None, expiry or None, note)
REGISTER = [
    # ---- PENDING -------------------------------------------------------------
    ("README.md", 17, "unknown = PENDING, never 0", "RULE", None, None, "R11 restated"),
    ("CLAUDE.md", 3158, "filters PENDING", "MENTION", None, None, "audit note on S06"),
    ("CLAUDE.md", 3150, "Reproduces 43 PENDING + 36 UNKNOWN lines", "MENTION", None, None,
     "this register's own audit note, added after the base; registered so the loop is visible, not excluded"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 28, "PENDING in PR #52", "ARCHIVE", None, None,
     "a PR state, not a quantity"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 37, "Unknown = PENDING", "ARCHIVE", None, None, "R11"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 226, "PENDING items", "ARCHIVE", None, None, ""),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 494, "unmeasured slot", "ARCHIVE", None, None, "legend"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 505, "exploration", "ARCHIVE", None, None, "S05"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 506, "finance overhead", "ARCHIVE", None, None, "S05"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 507, "drilling equipment", "ARCHIVE", None, None, "S05"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 508, "trucking", "ARCHIVE", None, None, "S01"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 509, "digital overhead", "ARCHIVE", None, None, "S05"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 510, "produced water", "ARCHIVE", None, None, "S02"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 512, "gathering + pipeline", "ARCHIVE", None, None, "S03"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 513, "refining", "ARCHIVE", None, None, "S04"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 526, "filters PENDING", "ARCHIVE", None, None, "S06"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 532, "PENDING items", "ARCHIVE", None, None, ""),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 534, "CoHD PPP base year", "ARCHIVE", None, None, "S12"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 535, "section-4 costs", "ARCHIVE", None, None, "S06-S11"),
    ("docs/readme_archive/README_2026-11-03_node_map.md", 536, "WTI node numbers", "ARCHIVE", None, None, "S05"),
    ("docs/DCEA_checks.md", 13, "Filters PENDING", "MENTION", None, None, "S06"),
    ("docs/DCEA_checks.md", 27, "PENDING items", "MENTION", None, None, ""),
    ("docs/DCEA_checks.md", 45, "PPP base year stays PENDING", "SLOT", "S12_cohd_ppp_base_year",
     E("FAO / World Bank CoHD release carrying its PPP base year", "re-pull the CoHD figure with its method stamp (R13)",
       "DERIVED: DCEA_checks.md lines 45-46 name the hosts and say they were not reachable"),
     "a categorical lookup; sensitivity has no natural value"),
    ("docs/worker_side_ledger_road_driver.md", 30, "| Filters | PENDING |", "SLOT", "S06_filters_cost",
     E("current filter-pack price and per-site replacement count", "receipts per site over a stated period",
       _TXT + " ('$17 per 3-pack at older prices, rising; use varies by site')"), ""),
    ("docs/worker_side_ledger_road_driver.md", 35, "Not yet costed (PENDING)", "SLOT",
     "S07_S11_section4_group", "void",
     "heading over five uncosted items (vehicle, home semi parking + hookup, nutrition, reimbursement time, "
     "lost family time); the ledger names no instrument for any; one register row, five slots"),
    ("docs/worker_side_ledger_road_driver.md", 73, "Treat unmeasured nodes as PENDING", "RULE", None, None, ""),
    ("docs/DCEA_v0.1.md", 32, "R11 Unknown is a slot, not a zero", "RULE", None, None,
     "R11 already requires the PENDING count beside the result: the same shape as the no-exit count"),
    ("docs/DCEA_v0.1.md", 68, "PENDING", "RULE", None, None, "R13 deviation table"),
    ("docs/DCEA_v0.1.md", 72, "the node is PENDING", "RULE", None, None,
     "R13 states an exit for official prices: method stamp plus ground check"),
    ("docs/DCEA_v0.1.md", 81, "PENDING count", "RULE", None, None, ""),
    ("docs/DCEA_v0.1.md", 85, "Numbers are left PENDING until they are sourced", "SLOT", "S05_node_numbers_group",
     "void", "blanket: every node's number is PENDING; 'until they are sourced' names no source class"),
    ("docs/DCEA_v0.1.md", 93, "trips per well: PENDING", "SLOT", "S01_trips_per_well", "void", ""),
    ("docs/DCEA_v0.1.md", 95, "water-to-oil ratio: PENDING", "SLOT", "S02_water_oil_ratio", "void", ""),
    ("docs/DCEA_v0.1.md", 99, "| PENDING |", "SLOT", "S03_gathering_pipeline", "void", ""),
    ("docs/DCEA_v0.1.md", 100, "| PENDING |", "SLOT", "S04_refining", "void", "tag column empty ('—')"),
    ("docs/DCEA_v0.1.md", 111, "None = PENDING", "VOCAB", None, None, "sentinel in the spec's calculator"),
    ("docs/DCEA_v0.1.md", 145, "never counts a PENDING node as zero", "RULE", None, None, ""),
    ("core/dcea.py", 11, "a PENDING node", "MENTION", None, None, "docstring"),
    ("core/dcea.py", 28, "None = PENDING", "VOCAB", None, None, "sentinel"),
    ("core/dcea.py", 87, "PENDING in the ledger", "MENTION", None, None, "code form of S06"),
    ("core/dcea.py", 121, "filters PENDING", "MENTION", None, None, "render string for S06"),
    ("core/dcea.py", 139, "PENDING nodes never counted as 0", "VOCAB", None, None, "selftest"),
    ("core/dcea.py", 148, "all-PENDING chain", "VOCAB", None, None, "selftest"),
    ("core/dcea.py", 165, "filters stay PENDING", "VOCAB", None, None, "selftest pins S06 open"),
    # ---- UNKNOWN (word) ------------------------------------------------------
    ("labor_thermodynamics/driver_hours_evidence_register.py", 17, "relevance to the question UNKNOWN", "VOCAB",
     None, None, "rung definition"),
    ("labor_thermodynamics/driver_hours_evidence_register.py", 596, "gate map UNKNOWN", "MENTION", None, None, "X1, X2"),
    ("labor_thermodynamics/driver_hours_evidence_register.py", 617, 'relevance="UNKNOWN', "SLOT", "U01_X1_relevance",
     E("covariate early_motion_exposure in an adult rocking / vehicle-sleep study",
       "cross-cultural arm in communities that still carry infants",
       _TXT + " (the record's own cheapest_probe field)"), ""),
    ("CLAUDE.md", 6505, 'verdict="UNKNOWN"', "MENTION", None, None, "audit note on U13"),
    ("CLAUDE.md", 6508, "UNKNOWN verdicts", "MENTION", None, None, "audit note on U13"),
    ("knowledge/scope_mapper.py", 32, 'UNKNOWN = "unknown"', "VOCAB", None, None, "enum member"),
    ("knowledge/scope_mapper.py", 242, "MeasurementType.UNKNOWN", "EMITTER", "U02_measurement_type",
     E("a study description carrying any keyword the classifier lists", "re-run _classify_measurement", _RUN),
     "fall-through of a keyword classifier: UNKNOWN means no listed keyword, not an unmeasured quantity"),
    ("calibration/substrate_refusal_eval.py", 208, 'overall_status: str = "UNKNOWN"', "DEFAULT", "U03_status_default",
     E("the eval's own scorer", "run the eval; overall_status is set to the worst axis", _RUN), ""),
    ("calibration/architecture_mismatch.py", 609, "UNKNOWN tag", "OTHER_SENSE", None, None,
     "an unrecognised input tag, not an unknown value"),
    ("calibration/assumption_validator.py", 288, '"status": "UNKNOWN"', "EMITTER", "U04_assumption_no_value",
     E("a measured value for the boundary's parameter", "supply state[parameter] and re-run validate", _RUN), ""),
    ("calibration/assumption_validator.py", 436, '== "UNKNOWN"', "VOCAB", None, None, "counter"),
    ("calibration/unified_audit.py", 80, '"UNKNOWN": 1', "VOCAB", None, None,
     "rank map: UNKNOWN is given severity 1, between GREEN and RED, so a held-open state enters a worst-of score. "
     "Recorded, not changed"),
    ("calibration/anti_metaphor_locker.py", 272, 'overall_status: str = "UNKNOWN"', "DEFAULT", "U03_status_default",
     E("the eval's own scorer", "run the eval; overall_status is set to the worst axis", _RUN), ""),
    ("calibration/fork_width_scorer.py", 195, 'overall_status: str = "UNKNOWN"', "DEFAULT", "U03_status_default",
     E("the eval's own scorer", "run the eval; overall_status is set to the worst axis", _RUN), ""),
    ("calibration/cascade_length_eval.py", 243, 'overall_status: str = "UNKNOWN"', "DEFAULT", "U03_status_default",
     E("the eval's own scorer", "run the eval; overall_status is set to the worst axis", _RUN), ""),
    ("calibration/monoculture_detector.py", 220, 'overall_status: str = "UNKNOWN"', "DEFAULT", "U03_status_default",
     E("the eval's own scorer", "run the eval; overall_status is set to the worst axis", _RUN), ""),
    ("calibration/study_scope_audit.py", 56, 'UNKNOWN = "unknown"', "VOCAB", None, None, "coupling not declared by study"),
    ("calibration/study_scope_audit.py", 66, 'UNKNOWN = "unknown"', "VOCAB", None, None, "regime enum"),
    ("calibration/study_scope_audit.py", 192, "regime stability not characterized", "EMITTER", "U05_regime_stability",
     E("a declared regime_state for the study's baseline", "set regime_state and re-read", _RUN), ""),
    ("calibration/trapdoor_eval.py", 114, 'overall_status: str = "UNKNOWN"', "DEFAULT", "U03_status_default",
     E("the eval's own scorer", "run the eval; overall_status is set to the worst axis", _RUN), ""),
    ("core/integrations/earth_physics_fieldlink.py", 30, "``UNKNOWN`` verdicts", "MENTION", None, None, "docstring"),
    ("core/integrations/earth_physics_fieldlink.py", 159, "upstream package unavailable", "MENTION", None, None, "docstring"),
    ("core/integrations/earth_physics_fieldlink.py", 161, "UNKNOWN here", "MENTION", None, None,
     "F3/F5/F6/F7 are methodology-layer: the docstring says no physics anchor can close them"),
    ("core/integrations/earth_physics_fieldlink.py", 191, 'verdict="UNKNOWN"', "MENTION", None, None, "docstring"),
    ("core/integrations/earth_physics_fieldlink.py", 203, 'verdict="UNKNOWN"', "EMITTER", "U06_no_anchor_mapped",
     "void", "check has no physics anchor: an exit is not a physics instrument, by the module's own account"),
    ("core/integrations/earth_physics_fieldlink.py", 215, 'verdict="UNKNOWN"', "EMITTER", "U07_upstream_absent",
     E("earth-systems-physics assumption_validator, importable", "install the pinned upstream and re-run", _RUN), ""),
    ("core/integrations/earth_physics_fieldlink.py", 229, 'verdict="UNKNOWN"', "EMITTER", "U08_layer_state_absent",
     E("a layer_states input", "pass layer_states and re-run", _RUN), "condition read from the branch; check before relying"),
    ("core/integrations/earth_physics_fieldlink.py", 243, '"UNKNOWN"', "VOCAB", None, None, "get() fallback"),
    ("core/integrations/earth_physics_fieldlink.py", 258, 'verdict = "UNKNOWN"', "EMITTER", "U09_no_anchor_graded",
     E("upstream assessments carrying a RED / YELLOW / GREEN status for a mapped anchor",
       "re-run with assessments present", _RUN), ""),
    ("core/liability_routing.py", 117, "beneficiary income delta not measured", "EMITTER", "U10_beneficiary_delta",
     E("a measured beneficiary income delta", "set provenance='measured' with value_delta and re-run", _RUN), ""),
    ("core/liability_routing.py", 259, "will read UNKNOWN", "MENTION", None, None, "demo fixture"),
    ("metrology/translation_layer.py", 235, "UNKNOWN HANDLING", "MENTION", None, None, "section header"),
    ("metrology/in_progress.md", 680, "-> UNKNOWN", "RULE", None, None, ""),
    ("metrology/metrological_audit_framework.py", 75, "UNKNOWN = None", "VOCAB", None, None, "sentinel"),
    ("metrology/metrological_audit_framework.py", 119, "treat as UNKNOWN", "RULE", None, None, ""),
    ("metrology/metrological_audit_framework.py", 333, "-> UNKNOWN", "MENTION", None, None, "comment"),
]


def _grep(args):
    out = subprocess.run(["grep", "-rn", "--exclude-dir=.git", "--exclude=expiry_register.py",
                          "--exclude=EXPIRY_REGISTER_78.md"] + args + ["."], cwd=ROOT, capture_output=True, text=True).stdout
    found = set()
    for line in out.splitlines():
        p, n, _ = line.split(":", 2)
        found.add((p[2:] if p.startswith("./") else p, int(n)))
    return found


BASE = "d5e6b1c"   # the tree the work order's "43 PENDING + 36 UNKNOWN" was read from


def base_counts(commit=BASE):
    """The counted base at the commit it was read from, so later mentions do not move it."""
    def n(args):
        out = subprocess.run(["git", "grep", "-n"] + args + [commit], cwd=ROOT, capture_output=True, text=True).stdout
        return len([l for l in out.splitlines() if l])
    return n(["PENDING"]), n(["-w", "UNKNOWN"])


def occurrences():
    """The counted base, recomputed: (path, line) sets for PENDING and the word UNKNOWN.
    This file and its doc are excluded: they would otherwise count themselves."""
    return dict(PENDING=_grep(["PENDING"]), UNKNOWN=_grep(["-w", "UNKNOWN"]))


def exit_state(e):
    if e is None:
        return None
    if e == "void":
        return "none"
    if not isinstance(e, dict) or sorted(e) != sorted(EXPIRY_KEYS):
        raise ValueError(f"expiry_condition must be void or carry {EXPIRY_KEYS}")
    if any(e[k] in ("", "void") for k in ("instrument_class", "protocol", "provenance")):
        raise ValueError("partial expiry_condition: instrument_class, protocol and provenance are required")
    return "incomplete" if e["sensitivity"] == "void" else "complete"


def slot_state(s):
    """For a slot's state value: ABSENT_AT_SENSITIVITY needs its sensitivity; a bare absent is refused."""
    if s in ("absent", "ABSENT", "ABSENT_AT_SENSITIVITY"):
        raise ValueError("an absence needs its sensitivity: ABSENT_AT_SENSITIVITY(<value>)")
    m = SCOPED.match(s)
    if s.upper().startswith("ABSENT") and (not m or m.group(1).strip() in ("", "void")):
        raise ValueError("ABSENT_AT_SENSITIVITY with no sensitivity")
    return "scoped_absence" if m else s


def check(register=REGISTER, occ=None):
    occ = occ if occ is not None else occurrences()
    rows, problems, moved, claimed = {}, [], [], set()
    for path, line, quote, cls, sid, exp, note in register:
        if cls not in CLASSES:
            problems.append(f"{path}:{line} class {cls}")
        if (cls in CARRY_EXPIRY) != (exp is not None):
            problems.append(f"{path}:{line} expiry carried by class {cls}" if exp is not None
                            else f"{path}:{line} {cls} dropped its expiry_condition (write void)")
        try:
            lines = open(os.path.join(ROOT, path), encoding="utf-8").read().split("\n")
        except OSError:
            lines = []
        if 1 <= line <= len(lines) and quote in lines[line - 1]:
            at = line
        else:   # the file moved under the row: take the nearest line carrying the quote, report the move
            hits = [i + 1 for i, t in enumerate(lines) if quote in t and (i + 1, path) not in claimed]
            at = min(hits, key=lambda h: abs(h - line)) if hits else None
            if at is None:
                problems.append(f"{path}:{line} quote not found in file (drift): {quote!r}")
                at = line
            else:
                moved.append((path, line, at))
        claimed.add((at, path))
        rows[(path, at)] = dict(cls=cls, sid=sid, exit=exit_state(exp) if cls in CARRY_EXPIRY else None)
    every = occ["PENDING"] | occ["UNKNOWN"]
    unregistered = sorted(every - set(rows))
    stale = sorted(set(rows) - every)
    return dict(rows=rows, problems=problems, unregistered=unregistered, stale=stale, moved=moved,
                n_pending=len(occ["PENDING"]), n_unknown=len(occ["UNKNOWN"]))


def summary(res):
    by_cls = {c: 0 for c in CLASSES}
    for r in res["rows"].values():
        by_cls[r["cls"]] += 1
    carrying = {k: r for k, r in res["rows"].items() if r["exit"] is not None}
    exits = {s: sum(1 for r in carrying.values() if r["exit"] == s) for s in ("none", "incomplete", "complete")}
    slots = {}
    for r in carrying.values():
        slots.setdefault(r["sid"], set()).add(r["exit"])
    return dict(by_cls=by_cls, exits=exits, n_carrying=len(carrying), distinct_ids=len(slots),
                no_exit=sorted(s for s, e in slots.items() if "none" in e))


def render(res=None):
    res = res or check()
    s = summary(res)
    out = ["EXPIRY REGISTER -- PENDING / UNKNOWN occurrences, classified",
           f"counted base at {BASE}: PENDING {base_counts()[0]} lines ; UNKNOWN {base_counts()[1]} word-lines",
           f"live tree: PENDING {res['n_pending']} ; UNKNOWN {res['n_unknown']} ; {len(res['rows'])} registered",
           "by class: " + "  ".join(f"{c} {n}" for c, n in s["by_cls"].items()),
           f"carrying expiry_condition: {s['n_carrying']} occurrences, {s['distinct_ids']} slot/emitter ids",
           f"exits by occurrence: no exit defined {s['exits']['none']}  incomplete (sensitivity void) "
           f"{s['exits']['incomplete']}  complete {s['exits']['complete']}  (counted, not failed)",
           "no exit defined: " + ", ".join(s["no_exit"]),
           "ABSENT_AT_SENSITIVITY slots: 0 (no exit instrument has been run)",
           f"outside the counted base, not classified: {len(res['unregistered'])} (lines added after {BASE}; "
           f"listed, counted, not failed)",
           f"stale rows: {len(res['stale'])}  "
           f"problems: {len(res['problems'])}  rows moved by later edits: {len(res['moved'])}"]
    out += ["  " + p for p in res["problems"]] + [f"  after-base {p}:{n}" for p, n in res["unregistered"]] \
        + [f"  stale {p}:{n}" for p, n in res["stale"]]
    return "\n".join(out)


def selftest():
    checks = []
    res = check()
    checks.append((f"counted base at {BASE} reproduces 43 PENDING + 36 UNKNOWN", base_counts() == (43, 36)))
    checks.append(("every row of the counted base resolves: no stale row, no problem",
                   not res["stale"] and not res["problems"]))
    s = summary(res)
    checks.append(("no-exit count is reported, not failed", s["exits"]["none"] > 0))
    planted = [r for r in REGISTER]
    p0 = list(planted[22]); p0[5] = None                           # a SLOT that drops its expiry
    checks.append(("dropped expiry on a SLOT is caught",
                   any("dropped its expiry" in x for x in check([tuple(p0)], occ=dict(PENDING=set(), UNKNOWN=set()))["problems"])))
    p1 = list(planted[22]); p1[2] = "a quote the file does not carry"
    checks.append(("a quote gone from its file is caught", any("drift" in x for x in check([tuple(p1)], occ=dict(PENDING=set(), UNKNOWN=set()))["problems"])))
    checks.append(("an unregistered occurrence is reported",
                   check(REGISTER, occ=dict(PENDING=res["rows"].keys() | {("x.md", 1)}, UNKNOWN=set()))["unregistered"] == [("x.md", 1)]))
    for bad in ("absent", "ABSENT_AT_SENSITIVITY", "ABSENT_AT_SENSITIVITY()", "ABSENT_AT_SENSITIVITY(void)"):
        try:
            slot_state(bad); ok = False
        except ValueError:
            ok = True
        checks.append((f"bare / empty absence refused: {bad}", ok))
    checks.append(("scoped absence accepted", slot_state("ABSENT_AT_SENSITIVITY(0.1 mm/yr)") == "scoped_absence"))
    try:
        exit_state(dict(instrument_class="x", sensitivity="void")); ok = False
    except ValueError:
        ok = True
    checks.append(("partial expiry refused", ok))
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    failed = sum(not ok for _, ok in checks)
    print(f"checks: {len(checks)}   failed: {failed}")
    return failed


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(1 if selftest() else 0)
    print(render())
