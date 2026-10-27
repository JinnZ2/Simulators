# SPDX-License-Identifier: CC0-1.0
"""floor_capability.py -- the FLOOR CAPABILITY SITE ASSESSMENT draft v0, read
and instrumented.

The draft (DRAFT_V0.txt, landed as delivered, sha256-pinned below) is a
PROPOSED instrument: six indicators a standard site-selection sheet does not
count, a hidden_cost sum, and three stated gaps. This module does two things
and keeps them apart.

    DRAFT_V0.txt --ast--> read_draft()  --> audit()       what the draft states, computed
         |                                                  (counts, bindings, overlaps)
         |
         +--> the indicators, made measurable on records:
              scrap            classify_event()   event level, never code level
              tenure x scrap   tenure_test()      equipment-only scrap as the control
              maintenance      task_class()       TRANSFERRED / NEW_TASK / CAPACITY
              part turnover    life_ratio()       declared basis or None
              worker tenure    handoff_overlap()  days both present, signed
              hr screening     screening_share()  NOT_RECORDED kept apart
              safety direction rule_origin()      REACTIVE / GENERATED / BOTH / NEITHER
              hidden_cost      cost_vector()      a vector; the scalar sum is refused

Every record this module scores is CONSTRUCTED in the test file and the
render. Nothing here is a statement about any plant, any workforce, or any
country. The draft's third gap (a three-country floor comparison, OBSERVED,
not quantified) is carried verbatim and no function takes a country.

Refuses --selftest (exit 2); the checks live in floor-capability/test_floor.py.
Stdlib only. Parses under Python 3.8. CC0.
"""

import ast
import hashlib
import importlib.util
import io
import os
import random
import sys
import tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

DRAFT = os.path.join(HERE, "DRAFT_V0.txt")
DRAFT_SHA256 = "7eb3ec711223386c095978dd9d34b3b2a9e70aa834398aefdd28a90afe43f09b"

sys.path.insert(0, os.path.join(ROOT, "sim-span"))
from three_column import ols  # noqa: E402  imported, not copied
sys.path.pop(0)


def _load(relpath, name):
    """A sibling module by path, under a private name, so a same-named
    module from another folder (there are several `common.py`) cannot
    shadow it."""
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, relpath))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_mp = _load("measurand-partition/common.py", "_flc_mp_common")
attribution = _mp.attribution  # imported, not copied

CHOICES = {
    1: "MARGIN = 2.0: a precursor is operator-catchable only if its lead time "
       "is at least twice the interval at which an operator samples that cue "
       "(a G-RES pair: the feature against the instrument's cadence). Not in "
       "the draft.",
    2: "Scrap events whose code is not in the draft's reclassify map are "
       "UNMAPPED and enter neither the numerator nor the denominator of the "
       "catchable share; they are counted on their own line.",
    3: "A rule can be both post-incident and floor-reported (a rule written "
       "from a near-miss report). The draft's two cells are not exclusive, so "
       "BOTH and NEITHER (imported from a code or standard) are added.",
    4: "The tenure test reads a slope as nonzero only outside the central 95% "
       "of a seeded permutation null (tenure shuffled, 400 draws). No "
       "stipulated tolerance.",
    5: "The hidden_cost term-to-indicator bindings and the three overlaps are "
       "this module's reading of the draft, declared as data below; they are "
       "not computed.",
}

MARGIN = 2.0          # [CHOICE 1]
PERMUTATIONS = 400    # [CHOICE 4]


# ---------------------------------------------------------------- the draft

class DraftPinError(ValueError):
    pass


def read_draft(path=DRAFT, pin=DRAFT_SHA256):
    """Parse the draft by AST. The pin is checked first; a draft whose bytes
    moved is refused, never read."""
    raw = open(path, "rb").read()
    got = hashlib.sha256(raw).hexdigest()
    if pin is not None and got != pin:
        raise DraftPinError("DRAFT_V0.txt sha256 %s, pinned %s" % (got, pin))
    src = raw.decode("utf-8")
    tree = ast.parse(src)
    out = {"sha256": got, "indicators": None, "hidden_cost_terms": None,
           "numeric_constants": 0, "names_with_weight": [],
           "status_lines": [], "gaps": [], "comments": []}
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) \
                and not isinstance(node.value, bool):
            out["numeric_constants"] += 1
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name == "indicators":
                out["indicators"] = ast.literal_eval(node.value)
            if name == "hidden_cost":
                out["hidden_cost_terms"] = _add_terms(node.value)
    for key in _all_keys(out["indicators"]):
        if "weight" in key.lower():
            out["names_with_weight"].append(key)
    in_gaps = False
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type != tokenize.COMMENT:
            continue
        text = tok.string.lstrip("#").strip()
        out["comments"].append(text)
        if text.startswith("GAPS"):
            in_gaps = True
            continue
        if in_gaps and text.startswith("- "):
            out["gaps"].append(text[2:])
        if tok.start[0] <= 3 and text and not text.startswith("\u2500\u2500"):
            out["status_lines"].append(text)
    return out


def _add_terms(node):
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _add_terms(node.left) + _add_terms(node.right)
    if isinstance(node, ast.Name):
        return [node.id]
    raise ValueError("hidden_cost is not a sum of names")


def _all_keys(d):
    keys = []
    if isinstance(d, dict):
        for k, v in d.items():
            keys.append(k)
            keys.extend(_all_keys(v))
    return keys


# [CHOICE 5] the reading, declared. unit_in_draft is what the bound indicator
# measures as the draft words it; a cost sum needs a cost.
HIDDEN_TERM_BINDING = {
    "scrap": {"indicator": "scrap", "unit_in_draft": "rate (scrap rate + root-cause codes)"},
    "machine_damage": {"indicator": "machine_part_turnover",
                       "unit_in_draft": "ratio (replacement rate vs expected service life)"},
    "retraining": {"indicator": None, "unit_in_draft": None},
    "hr_churn": {"indicator": "worker_tenure", "unit_in_draft": "rate (turnover by role)"},
    "outsourced_repair": {"indicator": "maintenance",
                          "unit_in_draft": "share (in-house vs outsourced, trended)"},
}

# Pairs a scalar sum counts twice: one event lands in both terms.
OVERLAPS = (
    ("scrap", "machine_damage",
     "a belt/drive failure that scraps parts also damages the machine; the "
     "draft's own reclassify map names belt/drive_failure as a scrap code"),
    ("machine_damage", "outsourced_repair",
     "repairing the damage outside is the outsourced repair"),
    ("hr_churn", "retraining",
     "the replacement for a leaver is the person retrained"),
)


def audit(d=None):
    """What the draft states, computed from the draft alone."""
    d = d or read_draft()
    ind = d["indicators"]
    terms = d["hidden_cost_terms"]
    name_match = [t for t in terms if t in ind]
    bound = {t: HIDDEN_TERM_BINDING.get(t, {"indicator": None}) for t in terms}
    unbound = [t for t, b in bound.items() if b["indicator"] is None]
    cost_unit = [t for t, b in bound.items()
                 if b.get("unit_in_draft") and "cost" in b["unit_in_draft"]]
    reclassify = ind["scrap"]["reclassify"]
    weights_state = "UNSTATED" if (d["numeric_constants"] == 0
                                    and not d["names_with_weight"]) else "PRESENT"
    return {
        "sha256": d["sha256"],
        "indicator_count": len(ind),
        "indicator_keys": list(ind),
        "numeric_constants": d["numeric_constants"],
        "weights_named_in_status": any("weight" in s for s in d["status_lines"]),
        "weights_state": weights_state,
        "hidden_cost_terms": terms,
        "terms_named_as_indicator": name_match,
        "terms_with_no_indicator": unbound,
        "terms_bound_to_a_cost_unit": cost_unit,
        "overlaps": [(a, b) for a, b, _ in OVERLAPS],
        "reclassify_codes": list(reclassify),
        "reclassify_level": "CODE",
        "gaps": d["gaps"],
        "gap_names_event_separation": any("separate" in g for g in d["gaps"]),
    }


# ---------------------------------------------------------------- scrap

PRECURSOR = ("PRESENT", "ABSENT", "UNKNOWN")
EVENT_STATES = ("CATCHABLE", "FASTER_THAN_CHECK", "EQUIPMENT_ONLY",
                "UNDETERMINED", "UNMAPPED")


def classify_event(ev, mapped_codes, margin=MARGIN):
    """One scrap event. The draft reclassifies a CODE; whether a catch was
    possible is a property of the EVENT: was there a precursor, and did it
    last long enough for the cue to be sampled.

    CATCHABLE          precursor present, lead_time >= margin * check_interval
    FASTER_THAN_CHECK  precursor present, but shorter than the cadence covers;
                       a cadence or staffing question, not a skill one
    EQUIPMENT_ONLY     searched, no precursor: true equipment failure
    UNDETERMINED       precursor unknown, or a time missing
    UNMAPPED           code outside the draft's map [CHOICE 2]
    """
    if ev.get("code") not in mapped_codes:
        return "UNMAPPED"
    p = ev.get("precursor", "UNKNOWN")
    if p not in PRECURSOR:
        raise ValueError("precursor must be one of %r, got %r" % (PRECURSOR, p))
    if p == "ABSENT":
        return "EQUIPMENT_ONLY"
    if p == "UNKNOWN":
        return "UNDETERMINED"
    lead, check = ev.get("lead_time_s"), ev.get("check_interval_s")
    if lead is None or check is None or check <= 0:
        return "UNDETERMINED"
    return "CATCHABLE" if lead >= margin * check else "FASTER_THAN_CHECK"


def scrap_readout(events, mapped_codes, margin=MARGIN):
    """Counts per state and the catchable share as a band.

    code_level_share is the draft's reading: every event of a mapped code is
    a missing human catch. It is an upper bound on the event-level share by
    construction, and the two are printed beside each other.
    """
    counts = {s: 0 for s in EVENT_STATES}
    for ev in events:
        counts[classify_event(ev, mapped_codes, margin)] += 1
    mapped = sum(counts[s] for s in EVENT_STATES if s != "UNMAPPED")
    total = len(events)
    c, u = counts["CATCHABLE"], counts["UNDETERMINED"]
    return {"counts": counts, "total": total, "mapped": mapped,
            # the draft's signal is a share of SCRAP: denominator all events
            "code_level_share": (mapped / total) if total else None,
            "catchable_share_of_all": ((c / total, (c + u) / total)
                                       if total else (None, None)),
            # the same count over mapped events only, printed apart
            "catchable_share_band": ((c / mapped, (c + u) / mapped)
                                     if mapped else (None, None))}


def catchable_share_low(states):
    """Known-answer handle: CATCHABLE over mapped events, from a list of
    event states. None when no event is mapped -- an empty denominator is
    not a share of zero."""
    mapped = [s for s in states if s != "UNMAPPED"]
    if not mapped:
        return None
    return round(sum(1 for s in mapped if s == "CATCHABLE") / len(mapped), 6)


def scrap_attribution(event_level):
    """The draft's reading and the event-level reading, through
    measurand-partition's attribution(). Event level narrows the unmeasured
    set; it does not empty it while staffing on the station goes unrecorded."""
    unmeasured = ["operator staffing on the station"]
    if not event_level:
        unmeasured = ["precursor existence", "precursor lead time",
                      "cue check cadence"] + unmeasured
    return attribution("scrap of a mapped code", "one plant's scrap log",
                       unmeasured, "scrap of a mapped code")


# ---------------------------------------------------------------- tenure

def _slope(ys, xs):
    beta, _ = ols(ys, [xs])
    return None if beta is None else beta[1]


def tenure_test(rows, seed=0, n_perm=PERMUTATIONS):
    """rows: dicts with tenure_years, catchable_rate, equipment_rate, one per
    operator (or operator-shift). The draft's first gap: no public dataset
    links tenure to scrap codes. This is the test that dataset would feed.

    The control is equipment-only scrap. If tenure tracks the catchable rate
    and not the equipment rate, the operator channel is supported. If it
    tracks both, newer operators may simply run older machines, and the two
    readings are not separable.
    """
    xs = [r["tenure_years"] for r in rows]
    if len(xs) < 4 or len(set(xs)) < 2:
        return {"verdict": "NOT_EVALUABLE", "reason": "fewer than 4 rows or one tenure value"}
    out = {}
    rng = random.Random(seed)
    for key in ("catchable_rate", "equipment_rate"):
        ys = [r[key] for r in rows]
        obs = _slope(ys, xs)
        null = []
        for _ in range(n_perm):
            sh = xs[:]
            rng.shuffle(sh)
            s = _slope(ys, sh)
            if s is not None:
                null.append(s)
        null.sort()
        lo = null[int(0.025 * len(null))]
        hi = null[int(0.975 * len(null)) - 1]
        sign = 0 if lo <= obs <= hi else (1 if obs > hi else -1)
        out[key] = {"slope": obs, "null_band": (lo, hi), "sign": sign}
    c, e = out["catchable_rate"]["sign"], out["equipment_rate"]["sign"]
    # The assignment confound predicts the SAME sign on both rates. An
    # equipment rate moving the other way runs against the catchable effect
    # and does not explain it. The first version tested e != 0 and read an
    # opposite-signed control as the confound; found by running (FLC_017).
    if c == 0:
        verdict = "NO_EFFECT"
    elif c > 0:
        verdict = "REVERSED"
    elif e < 0:
        verdict = "NOT_SEPARABLE"
    else:
        verdict = "OPERATOR_CHANNEL"
    out["control_runs_against"] = (c < 0 and e > 0)
    out["verdict"] = verdict
    return out


def tenure_world(kind, n=60, seed=1):
    """CONSTRUCTED operators, known generative model, labelled.

    operator   catchable scrap falls with tenure; equipment scrap does not
    assignment newer operators run older machines: both rates fall with
               tenure, no operator effect anywhere in the model
    null       neither rate depends on tenure
    """
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        t = rng.uniform(0.2, 20.0)
        machine_age = rng.uniform(1, 25)
        if kind == "assignment":
            machine_age = max(1.0, 25.0 - t + rng.gauss(0, 2))
        cat = 4.0 + rng.gauss(0, 0.4)
        eq = 1.0 + 0.08 * machine_age + rng.gauss(0, 0.3)
        if kind == "operator":
            cat -= 0.15 * t
        if kind == "assignment":
            cat += 0.08 * machine_age
        rows.append({"tenure_years": t, "catchable_rate": max(0.0, cat),
                     "equipment_rate": max(0.0, eq), "source": "CONSTRUCTED"})
    return rows


# ---------------------------------------------------------------- maintenance

TASK_CLASSES = ("TRANSFERRED", "NEW_TASK", "CAPACITY", "UNDETERMINED")


def task_class(base, later):
    """One task class, two periods. base/later: dicts with in_house and
    outsourced counts (None if not recorded).

    TRANSFERRED  done in house in the base period; in-house count fell and
                 outsourced rose. Fits "capability gone" and also a
                 make-or-buy decision; the counts do not separate them.
    NEW_TASK     never done in house in the base period
    CAPACITY     in-house count held or rose while outsourced rose: overflow
    UNDETERMINED a count missing, or outsourced did not rise
    """
    vals = [base.get("in_house"), base.get("outsourced"),
            later.get("in_house"), later.get("outsourced")]
    if any(v is None for v in vals):
        return "UNDETERMINED"
    bi, bo, li, lo = vals
    if lo <= bo:
        return "UNDETERMINED"
    if bi == 0:
        return "NEW_TASK"
    if li < bi:
        return "TRANSFERRED"
    return "CAPACITY"


def maintenance_readout(classes):
    """classes: {task_class_name: (base, later)}. The draft reads the
    AGGREGATE outsourced share; this reports it beside the per-class split,
    because the aggregate can rise with no TRANSFERRED class at all."""
    tally = {c: [] for c in TASK_CLASSES}
    tot = {"base_in": 0, "base_out": 0, "later_in": 0, "later_out": 0}
    for name, (b, l) in sorted(classes.items()):
        tally[task_class(b, l)].append(name)
        for k, src, f in (("base_in", b, "in_house"), ("base_out", b, "outsourced"),
                          ("later_in", l, "in_house"), ("later_out", l, "outsourced")):
            tot[k] += src.get(f) or 0

    def share(i, o):
        return None if (i + o) == 0 else round(o / (i + o), 6)
    return {"per_class": tally,
            "aggregate_outsourced_share": (share(tot["base_in"], tot["base_out"]),
                                           share(tot["later_in"], tot["later_out"])),
            "also_fits_transferred": "a make-or-buy decision"}


# ---------------------------------------------------------------- parts

LIFE_BASIS = ("OEM_RATED", "PLANT_HISTORY", "DUTY_ADJUSTED")


def life_ratio(observed_life, expected_life, basis):
    """observed / expected service life. The draft says "vs expected service
    life" and names no basis; an expected life with no declared basis is not
    a reference, so the ratio is None. Below 1 is early failure."""
    if basis not in LIFE_BASIS:
        return None
    if observed_life is None or expected_life is None or expected_life <= 0:
        return None
    return round(observed_life / expected_life, 6)


# ---------------------------------------------------------------- tenure handoff

def handoff_overlap(leaver_last_day, successor_first_day):
    """Days the leaver and the successor were both on the role: positive is
    overlap, 0 is back-to-back, negative is a gap. None if a date is missing.
    Overlap is necessary for a handoff and does not show one happened."""
    if leaver_last_day is None or successor_first_day is None:
        return None
    return leaver_last_day - successor_first_day + 1


def handoff_readout(transitions):
    out = {"OVERLAP": 0, "BACK_TO_BACK": 0, "GAP": 0, "NO_SUCCESSOR": 0, "UNKNOWN": 0}
    for t in transitions:
        if t.get("successor_first_day") is None and t.get("no_successor"):
            out["NO_SUCCESSOR"] += 1
            continue
        v = handoff_overlap(t.get("leaver_last_day"), t.get("successor_first_day"))
        if v is None:
            out["UNKNOWN"] += 1
        elif v > 0:
            out["OVERLAP"] += 1
        elif v == 0:
            out["BACK_TO_BACK"] += 1
        else:
            out["GAP"] += 1
    return out


# ---------------------------------------------------------------- screening

SCREENS = ("TACIT_TESTED", "CREDENTIAL_ONLY", "BOTH", "NOT_RECORDED")


def screening_share(roles):
    """Share of roles whose hiring tests tacit skill (TACIT_TESTED or BOTH),
    over roles with a recorded screen. NOT_RECORDED is counted, never read as
    CREDENTIAL_ONLY."""
    c = {s: 0 for s in SCREENS}
    for r in roles:
        s = r.get("screen", "NOT_RECORDED")
        if s not in SCREENS:
            raise ValueError("screen must be one of %r" % (SCREENS,))
        c[s] += 1
    rec = c["TACIT_TESTED"] + c["CREDENTIAL_ONLY"] + c["BOTH"]
    return {"counts": c,
            "tacit_share": None if rec == 0 else round((c["TACIT_TESTED"] + c["BOTH"]) / rec, 6)}


# ---------------------------------------------------------------- safety

def rule_origin(rule):
    """[CHOICE 3] from two declared booleans, each True / False / None."""
    pi, fr = rule.get("post_incident"), rule.get("floor_report")
    if pi is None or fr is None:
        return "UNKNOWN"
    if pi and fr:
        return "BOTH"
    if pi:
        return "REACTIVE"
    if fr:
        return "GENERATED"
    return "NEITHER"


def safety_readout(rules):
    c = {k: 0 for k in ("REACTIVE", "GENERATED", "BOTH", "NEITHER", "UNKNOWN")}
    for r in rules:
        c[rule_origin(r)] += 1
    known = sum(v for k, v in c.items() if k != "UNKNOWN")
    gen = c["GENERATED"] + c["BOTH"]
    return {"counts": c, "generated_share": None if known == 0 else round(gen / known, 6)}


# ---------------------------------------------------------------- hidden cost

class ScalarRefused(ValueError):
    pass


def cost_vector(values):
    """values: {term: (amount, unit) or None}. Returns one row per draft term
    with its state. There is no sum here; combine() is the only way to get
    one and it refuses."""
    terms = read_draft()["hidden_cost_terms"]
    rows = []
    for t in terms:
        v = values.get(t)
        rows.append({"term": t,
                     "amount": None if v is None else v[0],
                     "unit": None if v is None else v[1],
                     "state": "UNMEASURED" if v is None else "MEASURED",
                     "indicator": HIDDEN_TERM_BINDING[t]["indicator"]})
    return rows


def combine(rows, partitions=None):
    """The draft's hidden_cost as one number. Refused unless every term is
    measured, every unit is the same, and every declared overlap carries a
    partition rule saying which term an overlapping event is booked to."""
    partitions = partitions or {}
    missing = [r["term"] for r in rows if r["state"] != "MEASURED"]
    if missing:
        raise ScalarRefused("unmeasured terms: %s" % ", ".join(missing))
    units = sorted({r["unit"] for r in rows})
    if len(units) != 1:
        raise ScalarRefused("terms carry %d units: %s" % (len(units), ", ".join(units)))
    open_ = [(a, b) for a, b, _ in OVERLAPS if (a, b) not in partitions]
    if open_:
        raise ScalarRefused("overlaps with no partition rule: %s"
                            % "; ".join("%s/%s" % p for p in open_))
    return sum(r["amount"] for r in rows), units[0]


# ---------------------------------------------------------------- render

def _f(x):
    return "--" if x is None else ("%.3f" % x if isinstance(x, float) else str(x))


def render():
    a = audit()
    L = []
    w = L.append
    w("FLOOR CAPABILITY -- draft v0, read and instrumented")
    w("draft: floor-capability/DRAFT_V0.txt  sha256 %s..." % a["sha256"][:16])
    w("every record below is CONSTRUCTED; nothing here describes a plant or a workforce")
    w("")
    w("1. what the draft states (computed from the draft)")
    w("   indicators                  %d: %s" % (a["indicator_count"], ", ".join(a["indicator_keys"])))
    w("   numeric constants           %d" % a["numeric_constants"])
    w("   'weights' in the status     %s; weights in the draft: %s"
      % (a["weights_named_in_status"], a["weights_state"]))
    w("   hidden_cost terms           %d: %s" % (len(a["hidden_cost_terms"]), " + ".join(a["hidden_cost_terms"])))
    w("   term named as an indicator  %d of %d (%s)" % (len(a["terms_named_as_indicator"]),
                                                    len(a["hidden_cost_terms"]),
                                                    ", ".join(a["terms_named_as_indicator"])))
    w("   term with no indicator      %s   [CHOICE 5 binding]" % ", ".join(a["terms_with_no_indicator"]))
    w("   term bound to a cost unit   %d of %d" % (len(a["terms_bound_to_a_cost_unit"]), len(a["hidden_cost_terms"])))
    w("   overlaps a sum counts twice %d: %s" % (len(a["overlaps"]), "; ".join("%s/%s" % p for p in a["overlaps"])))
    w("   reclassify map              level %s, codes %d: %s" % (a["reclassify_level"], len(a["reclassify_codes"]),
                                                             ", ".join(a["reclassify_codes"])))
    w("   gap naming event separation %s" % a["gap_names_event_separation"])
    w("")
    codes = set(a["reclassify_codes"])
    rng = random.Random(7)
    evs = []
    for i in range(40):
        code = ("calibration_drift", "belt/drive_failure", "material_jam", "operator_misload")[i % 4]
        p = ("PRESENT", "PRESENT", "ABSENT", "UNKNOWN")[(i // 4) % 4]
        evs.append({"code": code, "precursor": p,
                    "lead_time_s": rng.choice([30, 300, 1800]),
                    "check_interval_s": rng.choice([60, 600])})
    s = scrap_readout(evs, codes)
    w("2. scrap at event level (40 CONSTRUCTED events)   [CHOICE 1 margin %.1f, CHOICE 2]" % MARGIN)
    for k in EVENT_STATES:
        w("   %-18s %d" % (k, s["counts"][k]))
    lo, hi = s["catchable_share_of_all"]
    w("   share of all %d scrap events:" % s["total"])
    w("     code level (the draft)    %s   every mapped event counted; an upper bound" % _f(s["code_level_share"]))
    w("     event level               [%s, %s]   CATCHABLE, plus UNDETERMINED at the top" % (_f(lo), _f(hi)))
    lo, hi = s["catchable_share_band"]
    w("   over the %d mapped events only  [%s, %s]   a different denominator, printed apart"
      % (s["mapped"], _f(lo), _f(hi)))
    for lvl, ev in (("draft (code level)", False), ("event level", True)):
        r = scrap_attribution(ev)
        w("   attribution, %-18s %s  unmeasured: %s" % (lvl, r["verdict"], ", ".join(r["unmeasured"])))
    w("")
    w("3. tenure x scrap, equipment-only scrap as the control   [CHOICE 4]")
    for kind in ("operator", "assignment", "null"):
        t = tenure_test(tenure_world(kind))
        w("   world %-10s catchable slope %+.3f  equipment slope %+.3f  -> %s"
          % (kind, t["catchable_rate"]["slope"], t["equipment_rate"]["slope"], t["verdict"]))
    w("")
    cls = {"spindle rebuild": ({"in_house": 0, "outsourced": 2}, {"in_house": 0, "outsourced": 6}),
           "drive belts": ({"in_house": 10, "outsourced": 1}, {"in_house": 12, "outsourced": 4}),
           "PLC upgrade": ({"in_house": 0, "outsourced": 0}, {"in_house": 0, "outsourced": 3})}
    m = maintenance_readout(cls)
    w("4. maintenance per task class (CONSTRUCTED)")
    for k in TASK_CLASSES:
        w("   %-13s %s" % (k, ", ".join(m["per_class"][k]) or "-"))
    w("   aggregate outsourced share  %s -> %s   rises with no TRANSFERRED class"
      % tuple(_f(x) for x in m["aggregate_outsourced_share"]))
    w("")
    w("5. part life, handoff, screening, rule origin (CONSTRUCTED)")
    w("   life_ratio 8000/10000 OEM_RATED %s   no basis %s"
      % (_f(life_ratio(8000, 10000, "OEM_RATED")), _f(life_ratio(8000, 10000, None))))
    h = handoff_readout([{"leaver_last_day": 100, "successor_first_day": 91},
                         {"leaver_last_day": 100, "successor_first_day": 101},
                         {"leaver_last_day": 100, "successor_first_day": 130},
                         {"leaver_last_day": 100, "successor_first_day": None, "no_successor": True},
                         {"leaver_last_day": None, "successor_first_day": 40}])
    w("   handoff  " + "  ".join("%s %d" % kv for kv in h.items()))
    sc = screening_share([{"screen": "TACIT_TESTED"}, {"screen": "CREDENTIAL_ONLY"},
                          {"screen": "CREDENTIAL_ONLY"}, {"screen": "NOT_RECORDED"}])
    w("   screening tacit share %s over recorded; NOT_RECORDED %d"
      % (_f(sc["tacit_share"]), sc["counts"]["NOT_RECORDED"]))
    sf = safety_readout([{"post_incident": True, "floor_report": False},
                         {"post_incident": True, "floor_report": True},
                         {"post_incident": False, "floor_report": False},
                         {"post_incident": None, "floor_report": True}])
    w("   rule origin  " + "  ".join("%s %d" % kv for kv in sf["counts"].items())
      + "   generated share %s" % _f(sf["generated_share"]))
    w("")
    w("6. hidden_cost")
    rows = cost_vector({"scrap": (1.0, "USD/yr"), "outsourced_repair": (1.0, "USD/yr")})
    w("   " + "  ".join("%s:%s" % (r["term"], r["state"]) for r in rows))
    try:
        combine(rows)
    except ScalarRefused as e:
        w("   scalar sum refused: %s" % e)
    w("")
    w("7. carried, not quantified")
    for g in a["gaps"]:
        w("   - %s" % g)
    w("   no function here takes a country; no claim about any country's workers")
    return "\n".join(L) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("floor_capability.py: checks run in floor-capability/test_floor.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
