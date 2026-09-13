# SPDX-License-Identifier: CC0-1.0
"""register.py -- the failure-mode register as an instrument.

Built to WORK_ORDER.md, landed verbatim beside this file. The register's
content is the four delivered ENTRY blocks and nothing else; this module
computes what the order asks to be computed over them and refuses what
cannot be computed here, naming the input it lacks.

SCOPE, FROM THE ORDER'S OWN SECTION 0, RESTATED SO IT IS NOT READ PAST

    DURABILITY AND RECONSTRUCTABILITY ONLY -- can the deployed object still
    be identified, re-produced, load-rated and inspected at t + N years, by
    someone who is not the original author and does not hold the tacit
    stack.

  not model behaviour, alignment, or misuse
  not harm incidents
  not a code of ethics

Nothing here rates a model, a vendor, a deployment or a person. Every
verdict is about whether a RECORD is sufficient to rebuild or identify an
object, and the entries are the order's own.

WHAT IS AUTHORED HERE AND WHAT IS NOT

Authored:   the computations, the refusals, and the findings in
            CLAIM_TABLE.md.
Not authored: any register entry. ENTRY 0 is named by the order and was not
            delivered; it is reported absent (entry_zero) and not written,
            because its mechanism is a property of the register rather than
            of a deployment -- it has no load_condition and its detection
            channel is the field itself. Section 3C is likewise not
            populated (step4_status): authoring PROJECTED entries from
            inside is exactly the failure F_D names, and the order's own
            fraction rule caps them at one on a register this short.

THREE THINGS THE ORDER ASKS FOR THAT CANNOT RUN HERE, EACH NAMED RATHER
THAN APPROXIMATED

  Step 0 / F_B  prior-art check. Egress is an allowlist; every catalogue
                host refuses CONNECT. Measured, not assumed -- see
                step0_prior_art(). The order says "do not build a second
                copy of an existing list", so the register cannot be
                cleared to ship from here.
  F_G           hand the schema to a reader outside the domain. There is
                no second reader, and F_G asks for five entries where four
                were delivered. A computable proxy is reported instead and
                is labelled as a proxy.
  F_E           what would make the register binding. That is a claim about
                the world, not a computation. The honest answer is stated
                and is not dressed as a measurement.

F_H, ENFORCED RATHER THAN PROMISED

"Define the event boundary before any count appears anywhere in the
deliverable." Every function here that returns a count returns it inside a
dict carrying a `unit` naming what is being counted. A test asserts it over
every counting function.

LIMITS STATED AT THE TOP

* control_state_split() reads a marker list over delivered English. A
  paraphrase steps around it, which is the standing limit of every keyword
  screen in this tree. The markers found are returned with the verdict so
  the reading is auditable rather than asserted.
* "consequence non-trivial" in Step 6 has no test in the order -- no scale,
  no threshold, no comparison. The gate runs on the existing_control
  conjunct alone and says so.
"""

from __future__ import annotations

import math
import os
import sys

import entries as E

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# [CHOICE 4] Two readings run through the delivered text and the order has
# no axis for them: a field's value often states the CURRENT state and then
# the state UNDER THE PROPOSED CONTROL. Detection is a marker list over
# delivered English, stated here and returned with every verdict. It is a
# word list; a paraphrase steps around it.
CONTROL_MARKERS = ("PROPOSED:", "With the control", "with the control",
                   "With it:", "without the control")

# The three fields whose delivered values carry both readings.
TWO_READING_FIELDS = ("detection_channel", "detection_latency",
                      "reconstruction")

CHOICES = {
    4: "the as-is / with-control split is read by a marker list over "
       "delivered English; markers found are returned with the verdict",
    5: "an entry's reconstruction reading is taken by counting declared "
       "vocabulary tokens in the value, not by a marker -- mechanical, and "
       "it is what makes MULTI_VALUE visible",
    6: "Step 6's gate runs on existing_control alone; the order's second "
       "conjunct (consequence non-trivial) has no test anywhere in it",
    7: "PROJECTED fraction f is an argument, printed on every render; "
       "the order requires a stated fraction and states none",
    8: "high_priority is reported under both readings and neither is "
       "picked -- section 1 defines it on detection_channel = NONE and "
       "three entries say NONE now and propose a channel in the same cell",
}

DEFAULT_PROJECTED_FRACTION = 0.2   # [CHOICE 7], argument, printed

FILED = "FILED"
UNRATED = "UNRATED"
CONFORMS = "CONFORMS"
OUT_OF_VOCAB = "OUT_OF_VOCAB"
MULTI_VALUE = "MULTI_VALUE"
NOT_EVALUABLE = "NOT_EVALUABLE"
NOT_RUN = "NOT_RUN"
BLOCKED = "BLOCKED"
AMBIGUOUS = "AMBIGUOUS"


# ------------------------------------------------------------------ filing

def filing(eid, rec=None):
    """Section 2: an entry missing any field is UNRATED and is FILED AS SUCH.

    An entry carrying an EXTRA field has no state in the order at all.  It
    is reported on its own line and never merged into `missing`, because a
    field the schema does not have and a field the entry does not have are
    different facts about the record.
    """
    rec = E.entries()[eid] if rec is None else rec
    schema = E.schema_field_names()
    missing = [f for f in schema if f not in rec]
    extra = [f for f in rec if f not in schema]
    return {
        "id": eid,
        "status": UNRATED if missing else FILED,
        "missing": missing,
        "extra": extra,
        "unit": "schema field",
        "n_missing": len(missing),
        "n_extra": len(extra),
    }


def filings():
    return [filing(eid) for eid in sorted(E.entries())]


# ----------------------------------------------------------- vocabularies

def _tokens_present(value, vocab):
    """Declared vocabulary tokens appearing in a delivered value.

    [CHOICE 5] Mechanical -- no marker list.  A token counts if it appears
    as a whole word.  Order preserved as found, because the first and last
    token of a two-token cell are different readings.
    """
    found, up = [], value
    for i in range(len(up)):
        for tok in vocab:
            if up.startswith(tok, i):
                before = up[i - 1] if i else " "
                after = up[i + len(tok)] if i + len(tok) < len(up) else " "
                if not before.isalnum() and not after.isalnum():
                    if not found or found[-1][1] != tok:
                        found.append((i, tok))
    out = []
    for _, tok in found:
        if tok not in out:
            out.append(tok)
    return out


def conformance(eid=None):
    """Per entry, per vocabulary field: CONFORMS | MULTI_VALUE | OUT_OF_VOCAB.

    The three are never merged.  OUT_OF_VOCAB is a value outside the
    declared set; MULTI_VALUE is two declared values in one cell.  They
    call for different repairs and a single "non-conforming" bucket would
    hide which.
    """
    vocabs = E.vocabularies()
    ids = [eid] if eid else sorted(E.entries())
    out = {}
    for i in ids:
        rec = E.entries()[i]
        row = {}
        for field, vocab in sorted(vocabs.items()):
            value = rec.get(field)
            if value is None:
                row[field] = {"verdict": NOT_EVALUABLE, "tokens": [],
                              "reason": "field absent from the entry"}
                continue
            toks = _tokens_present(value, vocab)
            if len(toks) == 1:
                verdict = CONFORMS
            elif len(toks) == 0:
                verdict = OUT_OF_VOCAB
            else:
                verdict = MULTI_VALUE
            row[field] = {"verdict": verdict, "tokens": toks, "reason": ""}
        out[i] = row
    return out


def conformance_counts():
    counts = {}
    for _i, row in conformance().items():
        for field, cell in row.items():
            counts.setdefault(field, {CONFORMS: 0, MULTI_VALUE: 0,
                                      OUT_OF_VOCAB: 0, NOT_EVALUABLE: 0})
            counts[field][cell["verdict"]] += 1
    return {"counts": counts, "unit": "entry-field cell",
            "n_entries": len(E.entries())}


# ------------------------------------------------------ the control-state axis

def control_state_split():
    """Which delivered cells carry both an as-is and a with-control reading.

    [CHOICE 4].  The register is two registers superimposed: the state of
    practice now, and the state under controls the entries themselves
    propose.  The order's schema has no axis for it, so both live in one
    cell and any distribution taken over that cell is taken over a mixture.
    """
    rows = []
    for eid in sorted(E.entries()):
        rec = E.entries()[eid]
        for field in TWO_READING_FIELDS:
            value = rec.get(field)
            if value is None:
                rows.append({"id": eid, "field": field, "two_readings": None,
                             "markers": [], "reason": "field absent"})
                continue
            markers = [m for m in CONTROL_MARKERS if m in value]
            rows.append({"id": eid, "field": field,
                         "two_readings": bool(markers),
                         "markers": markers, "reason": ""})
    n = sum(1 for r in rows if r["two_readings"])
    return {"rows": rows, "n_two_readings": n, "of": len(rows),
            "unit": "entry-field cell", "fields": list(TWO_READING_FIELDS),
            "markers_declared": list(CONTROL_MARKERS)}


def multi_value_axes():
    """The MULTI_VALUE reconstruction cells are NOT one axis.

    DUR-001 reads NO-without-the-control / PARTIAL-with-it: a CONTROL axis.
    DUR-003 reads PARTIAL-now / NO-later: a TIME axis.  A distribution
    built by taking the first token of each, or the last, merges a control
    state with a date.  Reported per entry; no merged distribution is
    emitted.
    """
    out = {}
    split = {(r["id"], r["field"]): r for r in control_state_split()["rows"]}
    for eid, row in conformance().items():
        cell = row.get("reconstruction", {})
        if cell.get("verdict") != MULTI_VALUE:
            continue
        marked = split.get((eid, "reconstruction"), {}).get("two_readings")
        out[eid] = {
            "tokens": cell["tokens"],
            "axis": "control" if marked else "time-or-undeclared",
            "basis": ("a with-control marker is present in the cell"
                      if marked else
                      "no with-control marker; the two tokens are not a "
                      "control-state pair and the axis is not declared"),
        }
    return {"rows": out, "n": len(out), "unit": "entry",
            "merged_distribution": None,
            "reason": "the axes differ per entry; merging them would put a "
                      "control state and a date in one column"}


# --------------------------------------------------------------- the steps

def step0_prior_art():
    """BLOCKED. Egress here is an allowlist and the check cannot be run.

    The order's first step, and F_B.  It says: verify whether a durability
    scoped catalogue already exists, and if one does, stop or scope to the
    residual -- "Do not build a second copy of an existing list."  That
    verification is a literature and registry search and this environment
    reaches no host that would answer it.

    The consequence is not cosmetic: F_B says the absence of prior art
    "must be established, not assumed", so the register cannot be cleared
    to ship from here regardless of what else computes.
    """
    return {
        "status": BLOCKED,
        "blocker": "outbound egress is an allowlist; catalogue and registry "
                   "hosts refuse CONNECT",
        "what_it_needs": "a search of existing AI incident and harm "
                         "catalogues for durability and reconstruction "
                         "scoped entries",
        "consequence": "F_B is unresolved, so the register is not cleared "
                       "to ship; nothing here establishes that this work "
                       "order is not duplication",
        "substituted": False,
    }


def step1_deployment_class():
    """NOT FIXED. Step 1 says pick one deployment class; no entry declares one.

    Step 1 exists because "ML system" is too broad to load-rate, and Step 5
    (reconstruction scoring) and section 5 (load rating) both rest on it.
    The delivered entries state load_condition at four different breadths
    and one of them declines to narrow explicitly.
    """
    rows = []
    for eid in sorted(E.entries()):
        rows.append({"id": eid,
                     "load_condition": E.entries()[eid].get("load_condition")})
    refusals = [r for r in rows if "all of them" in (r["load_condition"] or "")]
    return {
        "status": NOT_RUN,
        "rows": rows,
        "explicit_refusals_to_narrow": [r["id"] for r in refusals],
        "unit": "entry",
        "reason": "no deployment class is declared anywhere in the delivered "
                  "register; Step 5 and section 5 both rest on Step 1",
    }


def fraction_cap(n_other, fraction):
    """Max PROJECTED entries admissible: largest n with n/(n+k) <= f.

    n/(n+k) <= f  =>  n <= f*k/(1-f).  Returns None at f >= 1, where the
    rule places no cap -- a large integer there would read as a cap.
    """
    if n_other < 0:
        raise ValueError("n_other must be >= 0")
    if not 0 <= fraction:
        raise ValueError("fraction must be >= 0")
    if fraction >= 1.0:
        return None
    return int(math.floor(fraction * n_other / (1.0 - fraction) + 1e-9))


def projected_fraction():
    """PROJECTED share of the register. None on an empty register."""
    ents = E.entries()
    if not ents:
        return {"fraction": None, "n_projected": 0, "of": 0,
                "unit": "entry", "reason": "empty register"}
    conf = conformance()
    proj = [eid for eid, row in conf.items()
            if "PROJECTED" in row.get("evidence_class", {}).get("tokens", [])]
    return {"fraction": len(proj) / float(len(ents)),
            "n_projected": len(proj), "of": len(ents),
            "projected": sorted(proj), "unit": "entry",
            "reason": ""}


def step4_status(fraction=DEFAULT_PROJECTED_FRACTION):
    """NOT RUN, and the order's own three constraints are why.

    Step 4 says populate section 3C and flag every entry PROJECTED.
    Section 2 caps the PROJECTED share at a stated fraction.  Section 8
    says the register is expected to be SHORT and "a long one is a warning
    sign".  Together: with k non-projected entries the cap is
    f*k/(1-f), which on this register is a small integer.

    Authoring PROJECTED entries from inside is also exactly what F_D
    names.  None is written.
    """
    k = len(E.entries())
    cap = fraction_cap(k, fraction)
    return {
        "status": NOT_RUN,
        "n_non_projected": k,
        "fraction_used": fraction,
        "cap": cap,
        "unit": "entry",
        "reason": "the order's fraction rule, Step 4 and section 8 bind "
                  "together: at f=%.2f with %d non-projected entries the "
                  "cap is %s. Authoring projected entries from inside is "
                  "F_D's own failure." % (fraction, k, cap),
        "note": "the cap is a property of the rule, not a judgement about "
                "whether 3C would yield anything",
    }


def step5_distribution():
    """Reconstruction distribution -- the order calls it a headline result.

    It is computable for the entries that state one value.  MULTI_VALUE
    and OUT_OF_VOCAB cells are reported apart and no distribution over all
    four is emitted (see multi_value_axes).
    """
    conf = conformance()
    single, multi, out_v, absent = {}, [], [], []
    for eid in sorted(conf):
        cell = conf[eid].get("reconstruction", {})
        v = cell.get("verdict")
        if v == CONFORMS:
            single[cell["tokens"][0]] = single.get(cell["tokens"][0], 0) + 1
        elif v == MULTI_VALUE:
            multi.append(eid)
        elif v == OUT_OF_VOCAB:
            out_v.append(eid)
        else:
            absent.append(eid)
    return {
        "single_value": single,
        "n_single": sum(single.values()),
        "multi_value": multi,
        "out_of_vocab": out_v,
        "field_absent": absent,
        "of": len(conf),
        "unit": "entry",
        "distribution_over_all": None,
        "reason": "3 of the %d delivered entries do not state one "
                  "reconstruction value; a distribution over all of them "
                  "would be taken over a mixture" % len(conf),
    }


def step6_requirements():
    """The requirement set: entries with existing_control = NONE.

    [CHOICE 6] The order's gate has two conjuncts and the second
    ("consequence non-trivial") has no test anywhere in the order -- no
    scale, no threshold, no comparison.  The gate runs on the first alone
    and the second is reported NOT_EVALUABLE rather than assumed met.

    The minimum artifact is taken from the entry's own PROPOSED clause
    where it names one.  Where it does not, NOT_SUPPLIED -- no artifact is
    authored here.
    """
    rows, excluded = [], []
    for eid in sorted(E.entries()):
        rec = E.entries()[eid]
        control = rec.get("existing_control", "")
        gated_in = control.strip().upper().startswith("NONE")
        chan = rec.get("detection_channel", "")
        artifact = None
        if "PROPOSED:" in chan:
            artifact = chan.split("PROPOSED:", 1)[1].strip()
        row = {"id": eid, "existing_control": control,
               "gated_in": gated_in,
               "minimum_artifact": artifact or "NOT_SUPPLIED",
               "consequence_nontrivial": NOT_EVALUABLE}
        if gated_in:
            rows.append(row)
        else:
            row["states_requirement_anyway"] = bool(artifact)
            excluded.append(row)
    return {
        "requirements": rows,
        "n": len(rows),
        "excluded": excluded,
        "n_excluded": len(excluded),
        "of": len(E.entries()),
        "unit": "entry",
        "second_conjunct": NOT_EVALUABLE,
        "second_conjunct_reason": "the order states no test for "
                                  "'consequence non-trivial'",
    }


def step7_null_set():
    """Modes checked and found already controlled.

    "A register that finds everything broken is not measuring, it is
    advocating."  Reported in three buckets; PARTIAL is its own, because
    the order names it as the null-set discipline in DUR-002.
    """
    controlled, partial, uncontrolled = [], [], []
    for eid in sorted(E.entries()):
        c = E.entries()[eid].get("existing_control", "")
        up = c.strip().upper()
        if up.startswith("NONE"):
            uncontrolled.append(eid)
        elif "PARTIAL" in up:
            partial.append(eid)
        else:
            controlled.append(eid)
    return {"fully_controlled": controlled, "partially_controlled": partial,
            "uncontrolled": uncontrolled, "of": len(E.entries()),
            "unit": "entry",
            "empty": not (controlled or partial)}


def high_priority():
    """Section 1's high-priority set: detection_channel = NONE.

    [CHOICE 8] Two readings, both reported, neither picked.  AS_IS takes
    the cell's current-practice clause; WITH_CONTROL takes the proposed
    channel the same cell offers.  Under one reading most of the register
    is high priority and under the other none of it is, and the difference
    is entirely whether a proposed control is treated as existing.
    """
    as_is, with_control = [], []
    for eid in sorted(E.entries()):
        chan = E.entries()[eid].get("detection_channel", "")
        none_now = chan.strip().upper().startswith("NONE")
        proposes = "PROPOSED:" in chan
        if none_now:
            as_is.append(eid)
        if none_now and not proposes:
            with_control.append(eid)
    return {"as_is": as_is, "n_as_is": len(as_is),
            "with_control": with_control, "n_with_control": len(with_control),
            "of": len(E.entries()), "unit": "entry", "picked": None}


def entry_zero():
    """Section 1 names ENTRY 0 and no ENTRY block for it was delivered."""
    delivered = set(E.entries())
    named = "ENTRY 0 OF THE REGISTER IS THE DETECTION GAP ITSELF" \
        in E.order_text()
    return {
        "named_in_order": named,
        "delivered": sorted(x for x in delivered if x.endswith("000")),
        "present": any(x.endswith("000") for x in delivered),
        "authored_here": False,
        "reason": "not constructible under the section 2 schema: its "
                  "mechanism is a property of the register rather than of "
                  "a deployment, so it has no load_condition, and its "
                  "detection_channel is the field itself",
    }


# ----------------------------------------------------------- 6B arithmetic

def hop_compression():
    """Section 6B: hops per year, ML against classical.

    The order states "Compressed by roughly fifty".  That is the equal-N
    reading (20 hops in 500 years against 20 in 10) and the LOW end of the
    band the same block delivers, since the block's ML range runs to 50
    hops over 10 years.  Both are returned; the stated figure is the
    conservative end of the order's own numbers, not their midpoint.
    """
    hb = E.hop_budget()
    spans = hb["spans_years"]
    counts = hb["hop_counts"]
    if len(spans) < 2 or len(counts) < 2:
        return {"low": None, "high": None, "unit": "hops per year, ratio",
                "reason": "the section 6B block did not yield two spans"}
    classical_rate = counts[0][0] / float(spans[0])
    ml_low = counts[1][0] / float(spans[1])
    ml_high = counts[1][1] / float(spans[1])
    return {
        "classical_hops_per_year": classical_rate,
        "ml_hops_per_year": (ml_low, ml_high),
        "low": ml_low / classical_rate,
        "high": ml_high / classical_rate,
        "equal_n": spans[0] / float(spans[1]),
        "stated": hb["stated_compression"],
        "stated_is": None,
        "unit": "dimensionless ratio of hop rates",
    }


def hop_compression_reading():
    hc = hop_compression()
    stated = hc.get("stated")
    if stated is None:
        return dict(hc, stated_is="NOT_STATED")
    if abs(stated - hc["low"]) < 1e-9:
        where = "the low end of the order's own band, and the equal-N reading"
    elif abs(stated - hc["high"]) < 1e-9:
        where = "the high end of the order's own band"
    else:
        where = "neither end of the order's own band"
    return dict(hc, stated_is=where)


def expected_losses_independent(m_objects, n_hops, p):
    """Section 6B-1 (i): M x N x p. Independent draws, which 6B-2 refutes."""
    return m_objects * n_hops * p


def expected_losses_correlated(m_objects, n_events, share):
    """Section 6B-2: a small number of shared events each taking a slice."""
    return m_objects * n_events * share


def volume_vs_correlation(m_objects, n_hops, p, n_events, share):
    """F_I: both readings or neither. This returns both and refuses one.

    The order: "Check both appear together or neither does."  There is no
    single-number accessor -- a caller wanting the volume figure alone has
    to build the product itself, which is visible in a diff.
    """
    vol = expected_losses_independent(m_objects, n_hops, p)
    cor = expected_losses_correlated(m_objects, n_events, share)
    return {
        "volume": {"expected": vol, "mode": "DUR-003",
                   "shape": "steady rate, individually invisible"},
        "correlation": {"expected": cor, "mode": "NOT_ENTERED",
                        "shape": "synchronous blocks, defeats redundancy "
                                 "counted as independent"},
        "unit": "expected objects lost over the horizon",
        "operator_level": "per object the rate stays small enough that no "
                          "individual operator observes enough events to "
                          "update; detection fails where decisions are made",
        "correlation_entry_exists": False,
        "correlation_entry_reason": "section 6B-2 says correlation 'needs "
                                    "its own entry' and none was delivered; "
                                    "not authored here",
    }


def _era():
    path = os.path.join(ROOT, "effective-redundancy-audit")
    if path not in sys.path:
        sys.path.insert(0, path)
    import effective_redundancy  # noqa: E402
    return effective_redundancy


def redundancy_rule(claim):
    """Section 6B-2's REGISTER RULE, over the sibling's n_eff.

    "Any entry claiming redundancy as an existing_control must state what
    the redundant copies DO NOT SHARE. Copies on the same platform, in the
    same format, under the same dependency stack are one copy."

    That is exactly effective-redundancy-audit's Channel /
    survives_all_shared_nodes and its n_eff, so the arithmetic is IMPORTED
    and not restated here -- five stale copies of one gate across three
    drops is the repo's measurement of what restating costs (MF_019).

    A copy that does not declare what it does not share makes the claim
    UNRATED.  It is not scored as a shared copy, because that would be a
    measurement, and it is not scored as independent, because that is the
    claim under test.
    """
    era = _era()
    copies = claim.get("copies", [])
    undeclared = [c.get("name") for c in copies
                  if c.get("survives_all_shared_nodes") is None]
    if not copies:
        return {"id": claim.get("id"), "status": UNRATED,
                "reason": "no copies declared", "n_nominal": 0,
                "n_eff": None, "unit": "channel"}
    if undeclared:
        return {"id": claim.get("id"), "status": UNRATED,
                "reason": "copies do not state what they do not share: %s"
                          % ", ".join(str(u) for u in undeclared),
                "n_nominal": len(copies), "n_eff": None, "unit": "channel"}
    case = era.Case(
        name=str(claim.get("id")), domain="ml-infrastructure",
        outcome="held",
        channels=[era.Channel(name=c["name"],
                              survives_all_shared_nodes=bool(
                                  c["survives_all_shared_nodes"]))
                  for c in copies])
    return {"id": claim.get("id"), "status": FILED,
            "n_nominal": case.n_nominal, "n_eff": case.n_eff,
            "collapsed": case.n_eff == 1, "unit": "channel", "reason": ""}


def redundancy_claims_in_register():
    """Entries claiming redundancy as an existing_control. Expect zero."""
    rows = []
    for eid in sorted(E.entries()):
        c = E.entries()[eid].get("existing_control", "").lower()
        if "redundan" in c or "replica" in c or "backup" in c:
            rows.append(eid)
    return {"claims": rows, "n": len(rows), "of": len(E.entries()),
            "unit": "entry",
            "reason": "the rule fires on nothing in the delivered register; "
                      "a visible zero, not an untested rule"}


def shock_split(budget_lines=None):
    """Section 6B-3, plus the budget-line rule the same section states.

    "A planned shock with no budget line behaves exactly like an unplanned
    one."  So `scheduled` is not a mitigating property on its own; it
    mitigates only where a budget line is declared.  budget_line is
    DECLARED per class by the caller and defaults to None -- an undeclared
    budget is not a missing budget, and the two are kept apart.
    """
    classes = E.shock_classes()
    budget_lines = budget_lines or {}
    rows = []
    for key in sorted(classes):
        c = classes[key]
        scheduled = "scheduled" in (c.get("cadence") or "")
        budget = budget_lines.get(key)
        if not scheduled:
            mitigated, why = False, ("not scheduled; the budget rule does "
                                     "not apply")
        elif budget is None:
            mitigated, why = None, ("scheduled, budget line UNDECLARED. An "
                                    "undeclared budget is not a missing "
                                    "budget and the two are kept apart")
        elif budget:
            mitigated, why = True, "scheduled with a declared budget line"
        else:
            mitigated, why = False, ("scheduled with no budget line: the "
                                     "order's rule is that it behaves "
                                     "exactly like an unplanned shock")
        rows.append({
            "class": key, "name": c["name"], "cadence": c["cadence"],
            "verdict": c["verdict"], "scheduled": scheduled,
            "budget_line": budget, "mitigated": mitigated, "reason": why,
        })
    return {"rows": rows, "n": len(rows), "unit": "shock class",
            "substrate_state": "intact-and-unreadable is a distinct state "
                               "from decayed and is worse, because it reads "
                               "as retained"}


# ------------------------------------------------------------- falsifiers

# Markers for F_A, declared here rather than inferred. The TRANSPORT RULE
# turns on structure against resemblance, and whether a given justification
# IS structural is a reading -- so the markers are listed, both lists are
# returned, and the reading is left to whoever disagrees with them.
STRUCTURAL_MARKERS = ("abstract structure", "Structurally identical",
                      "same insufficiency", "Identical structure",
                      "structurally identical")
RESEMBLANCE_MARKERS = ("analogy", "resembl", "feel similar", "similar to")


def _contains_word(haystack, needle):
    """Whole-word containment. A substring scan matches `structural` inside
    `Structurally identical` and reports a source domain nobody named --
    the UNI_009 shape, avoided rather than found."""
    h, n = haystack.lower(), needle.lower()
    i = h.find(n)
    while i != -1:
        before = h[i - 1] if i else " "
        after = h[i + len(n)] if i + len(n) < len(h) else " "
        if not before.isalnum() and not after.isalnum():
            return True
        i = h.find(n, i + 1)
    return False


def evidence_class_audit():
    """Section 2's own requirements on evidence_class, per entry.

    MEASURED takes a cite. TRANSPORTED takes a named source domain plus a
    justification. The vocabulary check in conformance() reads the LABEL
    only, and a label is not a requirement -- this reads the requirement.
    """
    domains = [d.lower() for d, _ in E.source_domains()]
    rows = []
    for eid in sorted(E.entries()):
        rec = E.entries()[eid]
        ec = rec.get("evidence_class", "")
        toks = _tokens_present(ec, E.vocabularies()["evidence_class"])
        named = [d for d in domains
                 if any(_contains_word(ec, w) for w in d.split(" / "))]
        row = {
            "id": eid, "tokens": toks,
            "states_justification": "TRANSPORT JUSTIFICATION" in ec,
            "names_source_domain": named,
            "structural_markers": [m for m in STRUCTURAL_MARKERS if m in ec],
            "resemblance_markers": [m for m in RESEMBLANCE_MARKERS
                                    if m in ec],
            "cite": None,
        }
        row["meets_label"] = None
        if toks == ["MEASURED"]:
            row["meets_label"] = bool(row["cite"])
            row["reason"] = ("labelled MEASURED, which section 2 defines as "
                             "MEASURED (cite); no cite is given and the cell "
                             "says 'by analogy', which is the word the "
                             "TRANSPORT RULE rejects"
                             if not row["cite"] else "")
        elif "TRANSPORTED" in toks:
            row["meets_label"] = (row["states_justification"]
                                  and bool(named))
            row["reason"] = ""
        else:
            row["reason"] = "no evidence_class token found"
        rows.append(row)
    return {"rows": rows, "n": len(rows), "unit": "entry"}


def _f_a():
    """Does at least one transported mechanism survive the justification rule?

    The order: "does at least one transported mechanism survive Step 3's
    justification rule without appeal to resemblance? If none does, the
    transport section is decoration -- cut it and run on 3A alone."

    Presence of a justification and of structural-versus-resemblance
    language is mechanical and is what is returned. Whether a justification
    is CORRECT is a reading and is not scored.
    """
    survivors, resemblance_only, mentions = [], [], []
    for row in evidence_class_audit()["rows"]:
        if "TRANSPORTED" not in row["tokens"]:
            continue
        if row["structural_markers"]:
            if row["states_justification"]:
                survivors.append(row["id"])
        elif row["resemblance_markers"]:
            resemblance_only.append(row["id"])
        if row["resemblance_markers"]:
            mentions.append({"id": row["id"],
                             "markers": row["resemblance_markers"],
                             "clause": _clause_around(
                                 E.entries()[row["id"]]["evidence_class"],
                                 row["resemblance_markers"][0])})
    return {"status": "COMPUTED", "survivors": survivors,
            "n": len(survivors), "of": len(E.entries()), "unit": "entry",
            "resemblance_only": resemblance_only,
            "resemblance_mentioned": mentions,
            "verdict": "the transport section is not decoration"
                       if survivors else
                       "no transport survives; cut it and run on 3A alone",
            "limit": "the presence of structural language is checked; "
                     "whether the structure is correct is a reading. A "
                     "mention of resemblance is reported with its clause "
                     "and is NOT subtracted from the survivor set -- the "
                     "first version did subtract it, and struck DUR-001 on "
                     "the sentence in which DUR-001 disclaims resemblance"}


def _clause_around(text, needle, width=90):
    i = text.lower().find(needle.lower())
    if i == -1:
        return ""
    start = max(0, i - width // 2)
    return text[start:start + width].strip()


def _f_c(fraction=0.2):
    """Mandatory-field audit. The order asks for a random 20%.

    At four entries a 20% sample is under one entry, and a rejection rate
    computed from n<1 has no resolution.  A full census is run instead and
    the substitution is stated rather than taken quietly.
    """
    n = len(E.entries())
    sample_size = fraction * n
    required = ("mechanism", "detection_channel", "consequence")
    rejected = []
    for eid in sorted(E.entries()):
        rec = E.entries()[eid]
        if any(not rec.get(f, "").strip() for f in required):
            rejected.append(eid)
    return {"status": "COMPUTED", "census": True,
            "requested_sample": sample_size,
            "sample_substituted": "full census; a %.1f-entry sample gives a "
                                  "rejection rate no resolution"
                                  % sample_size,
            "rejected": rejected, "n_rejected": len(rejected),
            "of": n, "rate": len(rejected) / float(n) if n else None,
            "unit": "entry", "required_fields": list(required)}


def _f_d(fraction=DEFAULT_PROJECTED_FRACTION):
    pf = projected_fraction()
    cap = fraction_cap(len(E.entries()) - pf["n_projected"], fraction)
    return {"status": "COMPUTED", "fraction": pf["fraction"],
            "n_projected": pf["n_projected"], "of": pf["of"],
            "stated_cap_fraction": fraction, "cap_entries": cap,
            "unit": "entry",
            "reading": "the register passes because Step 4 was not run, "
                       "not because projection was resisted"}


def _f_g():
    """NOT RUN, with a computable proxy reported as a proxy.

    F_G asks for a reader outside the domain to classify five entries.
    There is no second reader here, and four entries were delivered where
    F_G asks for five.  The proxy: a field whose delivered values do not
    conform to its own declared vocabulary is underspecified by the order's
    own test, and that needs no second reader.
    """
    counts = conformance_counts()["counts"]
    flagged = []
    for field, row in sorted(counts.items()):
        bad = row[MULTI_VALUE] + row[OUT_OF_VOCAB]
        if bad:
            flagged.append({"field": field, "non_conforming": bad,
                            "of": sum(row.values())})
    return {"status": NOT_RUN,
            "blockers": ["no second reader",
                         "F_G asks for five entries; four were delivered"],
            "proxy": flagged, "proxy_is_a_proxy": True,
            "unit": "entry-field cell"}


def _f_i():
    """Both 6B-1 and 6B-2 appear, or neither does."""
    text = E.order_text()
    vol = "expected losses" in text
    cor = "THE INDEPENDENCE ERROR" in text
    return {"status": "COMPUTED", "volume_present": vol,
            "correlation_present": cor,
            "both_or_neither": vol == cor,
            "module_refuses_single": True,
            "reason": "volume_vs_correlation returns both and offers no "
                      "single-number accessor"}


def _f_h():
    """Event definition: every count states its unit. Asserted in the tests."""
    return {"status": "COMPUTED",
            "rule": "every function returning a count returns it in a dict "
                    "carrying a `unit` naming what is counted",
            "enforced_in": "test_register.py",
            "boundary": "the event boundary is the unit field; a silent "
                        "drift and a single wrong output never share one"}


def _f_b():
    return dict(step0_prior_art(), status=BLOCKED)


def _f_e():
    """A claim about the world, stated and not dressed as a measurement."""
    return {"status": NOT_RUN,
            "reason": "what would make a register binding is a claim about "
                      "the world, not a computation over the entries",
            "stated_answer": "nothing currently would. Bridge codes became "
                             "mandatory because failures were attributable "
                             "and expensive; the entries here are chosen for "
                             "producing no attributable event. Publishing "
                             "the register is not claimed to be sufficient.",
            "claims_publishing_sufficient": False}


def _f_f():
    """Every entry assuming something recoverable must name what and where."""
    rows = []
    for eid in sorted(E.entries()):
        rec = E.entries()[eid]
        chan = rec.get("detection_channel", "")
        named = chan.split("PROPOSED:", 1)[1].strip() if "PROPOSED:" in chan \
            else None
        holder = "third party" in chan or "not the operator" in chan
        rows.append({"id": eid, "names_what": named or "NOT_NAMED",
                     "names_a_holder": holder,
                     "names_a_location": None})
    return {"status": "COMPUTED", "rows": rows, "of": len(rows),
            "unit": "entry",
            "reason": "where is not stated by any entry; a holder is named "
                      "by one and a location by none"}


FALSIFIER_FNS = {
    "F_A": _f_a, "F_B": _f_b, "F_C": _f_c, "F_D": _f_d, "F_E": _f_e,
    "F_F": _f_f, "F_G": _f_g, "F_I": _f_i, "F_H": _f_h,
}


def falsifier_status():
    """Every falsifier, in the order's DELIVERED order (F_I before F_H)."""
    return [(fid, FALSIFIER_FNS[fid]()) for fid, _ in E.falsifiers()
            if fid in FALSIFIER_FNS]


# --------------------------------------------------------- cross-references

def _exists(rel):
    return os.path.isdir(os.path.join(ROOT, rel))


def cross_references():
    """The two the order asks to be cross-referenced rather than re-derived.

    Resolved by content, never by guess.  Where more than one folder in the
    tree is a candidate, AMBIGUOUS is returned with the candidates named
    and no pick made -- picking one would put a citation in the author's
    mouth.
    """
    out = []
    corr = [r for r in ("effective-redundancy-audit", "design-basis-ai")
            if _exists(r)]
    out.append({"asked_by": "6B-2",
                "marker": "correlated failure at scale",
                "status": "RESOLVED" if len(corr) >= 1 else NOT_RUN,
                "resolves_to": corr,
                "basis": "both hold a shared-node account of channels that "
                         "are nominally independent; the first supplies the "
                         "n_eff this module imports"})
    subs = [r for r in ("model-provenance", "criteria-drift",
                        "machine-record-format") if _exists(r)]
    out.append({"asked_by": "section 5",
                "marker": "silent substitution",
                "status": AMBIGUOUS if len(subs) > 1 else "RESOLVED",
                "resolves_to": subs,
                "basis": "more than one folder carries a claim about an "
                         "object being replaced without the record moving; "
                         "no pick is made here"})
    return {"rows": out, "n": len(out), "unit": "cross-reference"}


# ------------------------------------------------------------------ render

def _wrap(text, width, indent):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return ("\n" + " " * indent).join(lines)


def render_choices():
    rows = dict(E.CHOICES)
    rows.update(CHOICES)
    return "\n".join("  [CHOICE %d] %s" % (k, _wrap(v, 68, 14))
                     for k, v in sorted(rows.items()))


def render():
    out = []
    a = out.append
    a("FAILURE-MODE REGISTER -- ML AS INFRASTRUCTURE")
    a("scope: %s" % _wrap(E.scope_statement(), 66, 7))
    a("non-goals: %s" % "; ".join(E.non_goals()))
    a("")
    a("PROJECTED FRACTION  %s of %d entries (header figure, section 2 rule)"
      % (projected_fraction()["fraction"], projected_fraction()["of"]))
    a("")
    a("FILING")
    for f in filings():
        a("  %-9s %-8s missing %d  extra %s"
          % (f["id"], f["status"], f["n_missing"],
             ", ".join(f["extra"]) or "none"))
    a("  an extra field has no state in the order's section 2; it is "
      "reported here and never merged into `missing`")
    a("")
    a("VOCABULARY CONFORMANCE  (cells, never merged into one bucket)")
    for field, row in sorted(conformance_counts()["counts"].items()):
        a("  %-18s conforms %d  multi %d  out-of-vocab %d  absent %d"
          % (field, row[CONFORMS], row[MULTI_VALUE], row[OUT_OF_VOCAB],
             row[NOT_EVALUABLE]))
    a("")
    a("CONTROL-STATE AXIS  (the register is two registers superimposed)")
    cs = control_state_split()
    a("  cells carrying both an as-is and a with-control reading: %d of %d"
      % (cs["n_two_readings"], cs["of"]))
    for r in cs["rows"]:
        if r["two_readings"]:
            a("    %-9s %-18s markers: %s"
              % (r["id"], r["field"], ", ".join(r["markers"])))
    mv = multi_value_axes()
    a("  reconstruction cells holding two declared values: %d" % mv["n"])
    for eid, row in sorted(mv["rows"].items()):
        a("    %-9s %s  axis: %s" % (eid, " -> ".join(row["tokens"]),
                                     row["axis"]))
    a("  merged distribution: %s -- %s"
      % (mv["merged_distribution"], _wrap(mv["reason"], 60, 6)))
    a("")
    a("STEPS")
    s0 = step0_prior_art()
    a("  Step 0  %s  %s" % (s0["status"], _wrap(s0["blocker"], 58, 10)))
    a("          consequence: %s" % _wrap(s0["consequence"], 56, 12))
    s1 = step1_deployment_class()
    a("  Step 1  %s  %s" % (s1["status"], _wrap(s1["reason"], 58, 10)))
    a("          explicit refusals to narrow: %s"
      % (", ".join(s1["explicit_refusals_to_narrow"]) or "none"))
    a("  Step 2  the five section 3A seeds are delivered as seeds and "
      "carry no entry")
    eca = evidence_class_audit()
    a("  Step 3  %d entries survive the justification rule without appeal "
      "to resemblance" % _f_a()["n"])
    for row in eca["rows"]:
        a("    %-9s %-13s justification %-5s domain %-16s meets label %s"
          % (row["id"], "|".join(row["tokens"]) or "NONE",
             row["states_justification"],
             ",".join(row["names_source_domain"]) or "none",
             row["meets_label"]))
        if row.get("reason"):
            a("              %s" % _wrap(row["reason"], 58, 14))
    s4 = step4_status()
    a("  Step 4  %s  %s" % (s4["status"], _wrap(s4["reason"], 58, 10)))
    s5 = step5_distribution()
    a("  Step 5  single-value %s (n=%d)  multi %s  out-of-vocab %s"
      % (s5["single_value"], s5["n_single"], s5["multi_value"],
         s5["out_of_vocab"]))
    a("          distribution over all %d: %s"
      % (s5["of"], s5["distribution_over_all"]))
    s6 = step6_requirements()
    a("  Step 6  %d requirements, %d excluded by the gate"
      % (s6["n"], s6["n_excluded"]))
    for r in s6["requirements"]:
        a("    %-9s %s" % (r["id"], _wrap(r["minimum_artifact"], 56, 14)))
    for r in s6["excluded"]:
        a("    %-9s EXCLUDED (existing_control not NONE); states a "
          "requirement anyway: %s" % (r["id"], r["states_requirement_anyway"]))
    a("          second conjunct (consequence non-trivial): %s -- %s"
      % (s6["second_conjunct"], s6["second_conjunct_reason"]))
    s7 = step7_null_set()
    a("  Step 7  fully controlled %d  partial %d  uncontrolled %d  empty %s"
      % (len(s7["fully_controlled"]), len(s7["partially_controlled"]),
         len(s7["uncontrolled"]), s7["empty"]))
    a("")
    hp = high_priority()
    a("HIGH-PRIORITY SET  (section 1: detection_channel = NONE)")
    a("  as-is reading        %d of %d  %s"
      % (hp["n_as_is"], hp["of"], ", ".join(hp["as_is"]) or "none"))
    a("  with-control reading %d of %d  %s"
      % (hp["n_with_control"], hp["of"],
         ", ".join(hp["with_control"]) or "none"))
    a("  picked: %s" % hp["picked"])
    a("")
    ez = entry_zero()
    a("ENTRY 0  named in the order: %s   delivered: %s   authored here: %s"
      % (ez["named_in_order"], ez["present"], ez["authored_here"]))
    a("  %s" % _wrap(ez["reason"], 66, 2))
    a("")
    hc = hop_compression_reading()
    a("HOP BUDGET  (section 6B; unit: %s)" % hc["unit"])
    a("  classical %.3f hops/yr   ML %.1f-%.1f hops/yr"
      % (hc["classical_hops_per_year"], hc["ml_hops_per_year"][0],
         hc["ml_hops_per_year"][1]))
    a("  compression band %.0f to %.0f   stated %s -- %s"
      % (hc["low"], hc["high"], hc["stated"], hc["stated_is"]))
    a("")
    vc = volume_vs_correlation(1e6, 20, 1e-4, 3, 0.4)
    a("VOLUME AND CORRELATION  (F_I: both or neither; unit: %s)" % vc["unit"])
    a("  volume      %.0f  %s" % (vc["volume"]["expected"],
                                  vc["volume"]["shape"]))
    a("  correlation %.0f  %s" % (vc["correlation"]["expected"],
                                  _wrap(vc["correlation"]["shape"], 50, 18)))
    a("  a correlation entry exists: %s -- %s"
      % (vc["correlation_entry_exists"],
         _wrap(vc["correlation_entry_reason"], 56, 6)))
    rc = redundancy_claims_in_register()
    a("  entries claiming redundancy as a control: %d of %d (%s)"
      % (rc["n"], rc["of"], rc["reason"]))
    a("")
    a("SHOCK SPLIT  (section 6B-3)")
    for r in shock_split()["rows"]:
        a("  %-5s %-17s %-24s %-19s budget %-5s mitigated %s"
          % (r["class"], r["name"], r["cadence"], r["verdict"],
             r["budget_line"], r["mitigated"]))
    a("  %s" % _wrap(shock_split()["substrate_state"], 66, 2))
    a("")
    a("FALSIFIERS  (delivered order; F_I precedes F_H)")
    for fid, res in falsifier_status():
        a("  %-4s %s" % (fid, res.get("status")))
        for key in ("verdict", "reason", "reading", "sample_substituted",
                    "stated_answer"):
            if res.get(key):
                a("       %s" % _wrap(str(res[key]), 62, 7))
        for m in res.get("resemblance_mentioned", []):
            a("       %s mentions %s, in: %s"
              % (m["id"], "/".join(m["markers"]),
                 _wrap(m["clause"], 56, 9)))
        for b in res.get("blockers", []):
            a("       blocker: %s" % b)
    a("")
    a("CROSS-REFERENCES  (resolved by content; no pick where ambiguous)")
    for r in cross_references()["rows"]:
        a("  %-10s %-9s %s" % (r["marker"][:10], r["status"],
                               ", ".join(r["resolves_to"]) or "none"))
    a("")
    a("CHOICES")
    a(render_choices())
    return "\n".join(out)


def main(argv):
    if "--selftest" in argv:
        print("register.py is the instrument. The checks live in "
              "test_register.py; run: python3 test_register.py")
        return 2
    if "--choices" in argv:
        print(render_choices())
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
