#!/usr/bin/env python3
"""
The revised order, audited. WORK_ORDER_V2.md is delivered verbatim beside
WORK_ORDER.md and neither is edited.

register.py holds the v1 instrument and is unchanged. This module reads
the ADDITIONS -- the loss-variable map, DUR-005 and DUR-006 with their
sub-sections, the compounding section, the four new falsifiers, the
amendment record -- and computes what they state. Where a v1 quantity is
recomputed on the larger register it is IMPORTED from register.py rather
than reimplemented, so the two cannot disagree about what a cap or a
compression ratio is.

WHAT THIS DOES NOT DO
  - it does not rate any firm, product, arrangement or person. DUR-006 is
    arithmetic about conjunctions and the order says so in its own text;
    nothing here attaches a probability to any real entity, and no
    function takes an entity as an argument.
  - it does not put a number on the conjunction. F_L and A-07 both say
    not to. The probability model here is a NAMED MODEL used to check the
    DIRECTION of a stated claim, and every function carrying one returns
    its parameters alongside the value.

CC0. Stdlib only. Parses under 3.9.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import entries as E1                                      # noqa: E402
import entries_v2 as E2                                   # noqa: E402
import register as R1                                     # noqa: E402
sys.path.insert(0, os.path.join(HERE, os.pardir, "tools"))
import sourced as S                                       # noqa: E402


CHOICES = {
    9: ("Correlation model for the DUR-006-B conjunction. A mixture: with "
        "probability rho all n terms take one common draw, otherwise they "
        "draw independently. Marginals are preserved exactly and rho IS "
        "the pairwise correlation, so the model has one interpretable "
        "parameter and no free scale. Used ONLY to check the DIRECTION of "
        "F_L's stated claim; no number from it attaches to anything."),
    10: ("Mechanical test for F_M(b), 'a currently measurable production "
         "rate'. A condition states one only if its text carries a "
         "numeral. Conservative and declared: a rate named in words with "
         "no value -- 'at replacement rate' -- does not satisfy it, which "
         "is the reading F_M's own word 'measurable' takes."),
    11: ("Mechanical test for F_K, 'expected lifetime within the retention "
         "horizon'. Both sides are checked for a numeral: the condition "
         "for a lifetime, the order for a horizon. Neither is a judgement "
         "about how long anything lasts."),
}


def choices_report():
    out = ["CHOICES -- register_v2", ""]
    for k in sorted(CHOICES):
        out.append("[CHOICE %d] %s" % (k, CHOICES[k]))
        out.append("")
    return "\n".join(out)


UNDECLARED = "UNDECLARED"
NOT_APPLICABLE = "NOT_APPLICABLE"


# ------------------------------------------------- the pair, mechanically

def pair_diff():
    """Is v2 an additive revision of v1? A revision that quotes, restates
    or re-renders an earlier document is a COPY, and copies drift
    (OE_011, DBK_010, MI_011, CAC_9). Measured with difflib rather than
    asserted."""
    import difflib
    v1 = E1.order_text().split("\n")
    v2 = E2.order_text().split("\n")
    sm = difflib.SequenceMatcher(None, v1, v2, autojunk=False)
    ins = dele = rep = 0
    moved = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "insert":
            ins += j2 - j1
        elif tag == "delete":
            dele += i2 - i1
            moved.append(("delete", v1[i1:i2]))
        elif tag == "replace":
            rep += 1
            moved.append(("replace", v1[i1:i2], v2[j1:j2]))
    return {"inserted": ins, "deleted": dele, "replaced_blocks": rep,
            "purely_additive": dele == 0 and rep == 0,
            "changed": moved,
            "v1_lines": len(v1), "v2_lines": len(v2)}


def falsifiers_added():
    """Which falsifier ids v2 adds, and whether every v1 falsifier body
    survives verbatim."""
    a = dict(E1.falsifiers())
    b = dict(E2.falsifiers_v2())
    added = [f for f in [i for i, _ in E2.falsifiers_v2()] if f not in a]
    removed = [f for f in a if f not in b]
    changed = [f for f in a if f in b and a[f] != b[f]]
    return {"v1": [i for i, _ in E1.falsifiers()],
            "v2": [i for i, _ in E2.falsifiers_v2()],
            "added": added, "removed": removed, "changed_bodies": changed}


# ---------------------------------------------------------- the V-map

def amended_map():
    """The map with section 9's amendments applied, which the order says
    is the authoritative reading."""
    a = E2.amended_scores()
    order = sorted(a, key=lambda v: int(v[1:]))
    prot = [v for v in order if a[v]["amended"].startswith("+")]
    loss = [v for v in order if a[v]["amended"].startswith("-")]
    split = [v for v in order if a[v]["amended"] == "SPLIT"]
    moved = [v for v in order if a[v]["amended"] != a[v]["original"]]
    return {"rows": a, "order": order, "protective": prot,
            "loss_driving": loss, "split": split, "moved_by_amendment": moved}


def f3_check():
    """F3 names the wins after amendment. Count them from the table."""
    m = amended_map()
    claim = E2.f3_claim()
    prot = m["protective"]
    unaccounted = [v for v in prot if v not in claim["wins"]]
    # F2 argues one of them away by name; read that out of F2's own text.
    f2 = " ".join(" ".join(E2._section("### 1B-1",
                                       stop_prefix=("## ",))).split())
    i = f2.find("F2 ")
    f2_body = f2[i:f2.find("F3 ")] if i >= 0 else f2
    argued_away = [v for v in unaccounted if (v + " ") in f2_body
                   or (v + ".") in f2_body or (v + ",") in f2_body]
    silent = [v for v in unaccounted if v not in argued_away]
    return {"protective_after_amendment": prot,
            "f3_names": claim["wins"],
            "f3_original_wins": claim["original_wins"],
            "unaccounted": unaccounted,
            "argued_away_in_F2": argued_away,
            "unaccounted_and_unargued": silent,
            "f3_losses": claim["losses"],
            "loss_driving_after_amendment": m["loss_driving"]}


def v5_definition():
    """V5's own gloss, for the reading in CLAIM_TABLE FMR_029."""
    for vid, name, gloss in E2.v_definitions():
        if vid == "V5":
            return {"id": vid, "name": name, "gloss": gloss}
    return None


# ------------------------------------------- the conjunction, direction

def joint_survival(p, n, rho):
    """P(all n terms hold) under [CHOICE 9]: with probability rho one
    common draw applies to every term, otherwise the terms are
    independent. Marginals are p exactly and the pairwise correlation is
    rho exactly, so nothing is smuggled in by the parameterisation.

    Returns None for n < 1. This is a model, not a measurement, and
    nothing in this folder attaches it to any entity."""
    if n < 1:
        return None
    return rho * p + (1.0 - rho) * (p ** n)


def f_l_direction(p=0.9, n=7, grid=(0.0, 0.25, 0.5, 0.75, 1.0)):
    """F_L states a DIRECTION: 'Correlation makes the joint failure
    probability HIGHER than the naive product of independent terms.'

    Under any model that preserves the marginals, survival is
    non-decreasing in correlation -- for [CHOICE 9] the derivative is
    d/drho = p - p^n >= 0 for p in [0,1], n >= 1 -- so joint FAILURE is
    non-INcreasing. The stated direction is backwards.

    Reported two ways because F_L's sentence admits two readings and
    neither rescues it:
      LIKE_FOR_LIKE  failure(rho) against failure(0). Backwards at every
                     parameter, provably.
      CROSS_TYPE     failure(rho) against the product prod(p_i), which is
                     a SURVIVAL number. Value-dependent, therefore not a
                     general claim.
    """
    rows = []
    for rho in grid:
        s = joint_survival(p, n, rho)
        rows.append({"rho": rho, "survival": s, "failure": 1.0 - s})
    indep_failure = rows[0]["failure"]
    indep_product = p ** n
    like = all(r["failure"] <= indep_failure + 1e-12 for r in rows)
    cross = [r["failure"] > indep_product for r in rows]
    return {"model": "[CHOICE 9] mixture", "p": p, "n": n, "rows": rows,
            "derivative_sign": "non-negative (p - p^n >= 0)",
            "independent_failure": indep_failure,
            "independent_product": indep_product,
            "like_for_like_failure_is_non_increasing": like,
            "f_l_states": "HIGHER",
            "like_for_like_verdict": "BACKWARDS" if like else "AS_STATED",
            "cross_type_true_at": sum(1 for c in cross if c),
            "cross_type_of": len(cross),
            "cross_type_verdict": ("VALUE_DEPENDENT"
                                   if 0 < sum(1 for c in cross if c)
                                   < len(cross) else "UNIFORM"),
            "conclusion_unaffected": True,
            "note": ("A-07 states the same correction WITHOUT a direction "
                     "and is right; section 9 is the authoritative record "
                     "by the order's own rule. The conclusion -- cannot be "
                     "ensured, put no number on it -- rests on the "
                     "inability to ensure each term and is untouched.")}


def conjunction_vs_disjunction(p=0.9, n_terms=None, q=0.5, m_holders=4):
    """DUR-006-C, stated as arithmetic. Single custodian survives only if
    every term holds; distributed retention survives if any holder does.
    Both numbers are properties of the stated model and of nothing else."""
    if n_terms is None:
        n_terms = len(E2.conjunction_terms())
    conj = joint_survival(p, n_terms, 0.0)
    disj = 1.0 - (1.0 - q) ** m_holders
    return {"n_terms": n_terms, "per_term_p": p,
            "conjunction_survival": conj,
            "m_holders": m_holders, "per_holder_q": q,
            "disjunction_survival": disj,
            "per_holder_below_per_term": q < p,
            "note": ("the distributed arrangement is modelled with a LOWER "
                     "per-holder number and survives more often; that is "
                     "the order's point and it does not depend on the "
                     "values"),
            "shape": "product of probabilities vs complement of a product"}


# ------------------------------------------------------- F_K and F_M

TIME_UNITS = ("year", "yr", "month", "week", "day", "decade", "century",
              "generation", "hour")
RATE_MARKS = ("per ", "/", "%")


def _has_numeral(text):
    return any(ch.isdigit() for ch in text)


def _has_duration(text, locator=None, order_name=None):
    """A numeral adjacent to a time unit.

    NOT a bare numeral test. The first version of F_K's check used one and
    fired twice on digits that are not the quantity: the cross-reference
    "(see DUR-006)" scored as a condition carrying an expected lifetime,
    and "hop count over the retention horizon exceeds ~1" scored as a
    retention horizon carrying a value. Both false positives ran toward
    reporting the bound as APPLICABLE when the order states neither
    quantity -- the lexical-proxy shape (UNI_009, T1-1), found by reading
    the output.

    Delegates to tools/sourced.numeral_with_unit, so a duration that
    passes comes back as a SOURCED value carrying the span that covers
    the quantity, and one that does not comes back as a refusal naming
    what was missing rather than as a False that reads like a
    measurement."""
    loc = locator or S.Locator(order_name or E2.ORDER_NAME,
                               None, None, None, "text")
    return S.numeral_with_unit(text, loc, units=TIME_UNITS)


def _is_duration(text, locator=None, order_name=None):
    """The boolean form, for a caller that only needs the branch."""
    return isinstance(_has_duration(text, locator, order_name), S.Sourced)


def _has_rate(text):
    """A numeral together with a rate marker. F_M(b) asks for a MEASURABLE
    production rate; a rate named in words with no value does not satisfy
    it. [CHOICE 10]."""
    low = text.lower()
    return _has_numeral(low) and any(m in low for m in RATE_MARKS)


def f_k_bound(conds=None, order_name=None, text=None):
    """F_K: a condition enters the register only if its expected lifetime
    is within the retention horizon being claimed. [CHOICE 11].

    Both sides are read with the SOURCED duration rule, so a condition
    admitted here carries the span covering its quantity and one refused
    carries the reason. `~1` with no unit does not parse into a horizon;
    it fails the gate."""
    conds = E2.artifact_side_ambient() if conds is None else conds
    order_name = order_name or E2.ORDER_NAME
    with_lifetime, refused = [], []
    for k, c in enumerate(conds):
        loc = S.Locator(order_name, None, None, None,
                        "artifact-side condition %d" % (k + 1))
        d = _has_duration(c, loc, order_name)
        if isinstance(d, S.Sourced):
            with_lifetime.append({"condition": c, "quantity": d.value,
                                  "span": d.span})
        else:
            refused.append({"condition": c, "reason": d.reason})
    txt = E2.order_text() if text is None else text
    horizon_mentions = txt.count("retention horizon")
    horizon_valued, horizon_quantity = False, None
    for n, line in enumerate(txt.split("\n"), start=1):
        if "retention horizon" not in line:
            continue
        loc = S.Locator(order_name, n, None, None, "retention horizon")
        d = _has_duration(line, loc, order_name)
        if isinstance(d, S.Sourced):
            horizon_valued, horizon_quantity = True, d.value
            break
    return {"falsifier": "F_K", "n_conditions": len(conds),
            "conditions": conds,
            "with_stated_lifetime": [r["condition"] for r in with_lifetime],
            "lifetime_quantities": [r["quantity"] for r in with_lifetime],
            "n_with_stated_lifetime": len(with_lifetime),
            "refused": refused,
            "retention_horizon_mentions": horizon_mentions,
            "retention_horizon_has_a_value": horizon_valued,
            "retention_horizon_quantity": horizon_quantity,
            "applicable": bool(with_lifetime) and horizon_valued,
            "state": ("APPLIED" if (with_lifetime and horizon_valued)
                      else "NOT_APPLICABLE_AS_DELIVERED"),
            "why": ("the bound compares two quantities and the order "
                    "states neither: no condition carries an expected "
                    "lifetime and no retention horizon carries a value"),
            "choice": 11}


def f_m_bound(conds=None):
    """F_M: a carrier-side condition enters the register only with (a) a
    named producing mechanism and (b) a currently measurable production
    rate. Conditions failing (b) are UNINSTRUMENTED and excluded from the
    ACTIVE SET rather than carried as claims. [CHOICE 10]."""
    conds = E2.carrier_side_ambient() if conds is None else conds
    rows = []
    for c in conds:
        rate = _has_rate(c)
        rows.append({"condition": c, "states_a_rate_value": rate,
                     "names_rate_in_words": "rate" in c.lower(),
                     "admits": rate})
    active = [r["condition"] for r in rows if r["admits"]]
    uninstrumented = [r["condition"] for r in rows if not r["admits"]]
    return {"falsifier": "F_M", "n_conditions": len(conds), "rows": rows,
            "active_set": active, "n_active": len(active),
            "uninstrumented": uninstrumented,
            "n_uninstrumented": len(uninstrumented),
            "active_set_empty": not active,
            "why": ("F_M is delivered in the same document as the "
                    "candidate set it gates; on that set it admits "
                    "nothing"),
            "choice": 10}


def screen_has_null(text=None):
    """DUR-005-C states its own CONSTANT_FIRES property: every capacity
    scores PRODUCED or FLAGGED and nothing scores clean. Read out of the
    delivered text rather than asserted about it."""
    txt = E2.screen_rule() if text is None else text
    flat = " ".join(txt.split()).lower()
    return {"section": "DUR-005-C",
            "states_no_null": "has no null result" in flat,
            "states_intended": "intended behaviour" in flat,
            "read_case_insensitively": True,
            "reading": ("a screen with no null cannot separate an "
                        "examined capacity from an unexamined one; it "
                        "records what is unexamined, which is what the "
                        "section says it does"),
            "interaction_with_F_M": ("the screen admits everything and "
                                     "F_M then admits none of it; two "
                                     "stages, and the delivered candidate "
                                     "set comes out empty")}


# ------------------------------------------------ recounts on 6 entries

def reconstruction_distribution_v2(recs=None, axes=None):
    """Step 5 over the six delivered entries. A cell stating two of the
    three values is reported as two, not resolved to one, and the AXIS
    each multi-value cell varies along is named -- they are different
    axes and a merged distribution would put them on one."""
    rows = []
    for rec in (E2.entries_v2() if recs is None else recs):
        vals = E2.reconstruction_values(rec)
        rows.append({"id": rec["id"], "values": vals, "n": len(vals),
                     "cell": rec["fields"].get("reconstruction", "")})
    single = [r for r in rows if r["n"] == 1]
    multi = [r for r in rows if r["n"] > 1]
    none = [r for r in rows if r["n"] == 0]
    dist = {}
    for r in single:
        dist[r["values"][0]] = dist.get(r["values"][0], 0) + 1
    return {"rows": rows, "n_entries": len(rows),
            "single_valued": [r["id"] for r in single],
            "multi_valued": [r["id"] for r in multi],
            "no_declared_value": [r["id"] for r in none],
            "distribution_over_single_valued": dist,
            "axes": (axes if axes is not None else
                     {"DUR-001": "control state (without / with the "
                                 "control)",
                      "DUR-003": "time (degrades from PARTIAL toward "
                                 "NO)"}),
            "merged_distribution": None,
            "why_no_merge": ("the two multi-valued cells vary along "
                             "different axes; one distribution over both "
                             "would be a count across unlike objects")}


def projected_fraction_v2(fraction=None, recs=None):
    """The section 2 rule recounted on six entries, using register.py's
    own fraction_cap rather than a second copy of the inequality."""
    if fraction is None:
        fraction = R1.DEFAULT_PROJECTED_FRACTION
    rows = []
    for rec in (E2.entries_v2() if recs is None else recs):
        vals = E2.evidence_values(rec)
        rows.append({"id": rec["id"], "values": vals,
                     "projected": "PROJECTED" in vals})
    proj = [r["id"] for r in rows if r["projected"]]
    other = [r["id"] for r in rows if not r["projected"]]
    cap = R1.fraction_cap(len(other), fraction)
    return {"rows": rows, "n_entries": len(rows),
            "projected": proj, "n_projected": len(proj),
            "n_other": len(other), "stated_fraction": fraction,
            "cap": cap, "at_cap": cap is not None and len(proj) == cap,
            "over_cap": cap is not None and len(proj) > cap,
            "multi_valued_evidence": [r["id"] for r in rows
                                      if len(r["values"]) > 1],
            "choice": "[CHOICE 7] of register.py -- the order states no "
                      "fraction"}


def f_j_scope():
    """F_J says mark every 6C entry PROJECTED. Count the ENTRY blocks in
    section 6C."""
    lines = E2._section("## 6C. COMPOUNDING", stop_prefix=("## ",))
    blocks = [b for b in E1._fenced_blocks(lines)
              if b and b[0].strip().startswith("ENTRY")]
    return {"falsifier": "F_J", "section": "6C",
            "entry_blocks_in_6C": len(blocks),
            "subsections": sum(1 for line in lines
                               if line.startswith("### ")),
            "state": ("NO_ENTRIES_TO_MARK" if not blocks else "APPLIES"),
            "why": ("F_J directs a marking at entries in a section that "
                    "contains subsections and no ENTRY blocks; 9-1 records "
                    "separately that PROVENANCE REGRESS has no entry")}


def still_open_v2():
    items = E2.still_open()
    return {"n": len(items), "items": items,
            "name_a_missing_entry": [i for i in items
                                     if "no entry" in i.lower()]}


def amendment_record():
    """Every amendment with its four fields, and which are complete."""
    rows = []
    want = ("superseded", "replacement", "forcing_case", "consequence")
    for a in E2.amendments():
        missing = [f for f in want if f not in a]
        rows.append({"id": a["id"], "title": a["title"],
                     "missing": missing, "complete": not missing})
    return {"rows": rows, "n": len(rows),
            "complete": sum(1 for r in rows if r["complete"]),
            "incomplete": [r["id"] for r in rows if not r["complete"]]}


# --------------------------------------------------------------- render

def _fmt(v):
    if v is None:
        return "--"
    if isinstance(v, float):
        return "%.6g" % v
    return str(v)


def render():
    L = []
    L.append("WORK_ORDER_V2 -- the revised order, audited")
    L.append("")
    pd = pair_diff()
    L.append("THE PAIR")
    L.append("  v1 %d lines -> v2 %d lines" % (pd["v1_lines"], pd["v2_lines"]))
    L.append("  inserted %d   deleted %d   replaced blocks %d"
             % (pd["inserted"], pd["deleted"], pd["replaced_blocks"]))
    L.append("  purely additive: %s" % pd["purely_additive"])
    fa = falsifiers_added()
    L.append("  falsifiers added: %s" % ", ".join(fa["added"]))
    L.append("  v1 falsifier bodies changed: %s"
             % (fa["changed_bodies"] or "none"))
    L.append("")
    L.append("LOSS-VARIABLE MAP, amendments applied")
    m = amended_map()
    for v in m["order"]:
        r = m["rows"][v]
        mark = " <- %s" % r["amendment"] if r["amendment"] else ""
        L.append("  %-4s classical %-3s  ml %-3s  amended %-6s%s"
                 % (v, r["classical"], r["original"], r["amended"], mark))
    L.append("  protective after amendment: %s" % ", ".join(m["protective"]))
    L.append("")
    f3 = f3_check()
    L.append("F3 CHECK")
    L.append("  F3 names as wins       %s" % ", ".join(f3["f3_names"]))
    L.append("  table gives            %s"
             % ", ".join(f3["protective_after_amendment"]))
    L.append("  unaccounted            %s" % ", ".join(f3["unaccounted"]))
    L.append("  argued away in F2      %s"
             % (", ".join(f3["argued_away_in_F2"]) or "none"))
    L.append("  unaccounted, unargued  %s"
             % (", ".join(f3["unaccounted_and_unargued"]) or "none"))
    v5 = v5_definition()
    L.append("  V5 gloss: %s %s" % (v5["name"], v5["gloss"]))
    L.append("")
    L.append("F_L DIRECTION CHECK")
    d = f_l_direction()
    L.append("  model %s  p=%g  n=%d" % (d["model"], d["p"], d["n"]))
    for r in d["rows"]:
        L.append("    rho=%-5.2f survival=%-10.6f failure=%-10.6f"
                 % (r["rho"], r["survival"], r["failure"]))
    L.append("  derivative in rho: %s" % d["derivative_sign"])
    L.append("  F_L states %s; like-for-like verdict %s"
             % (d["f_l_states"], d["like_for_like_verdict"]))
    L.append("  cross-type reading true at %d of %d parameters -> %s"
             % (d["cross_type_true_at"], d["cross_type_of"],
                d["cross_type_verdict"]))
    L.append("  conclusion unaffected: %s" % d["conclusion_unaffected"])
    L.append("  %s" % d["note"])
    L.append("")
    cd = conjunction_vs_disjunction()
    L.append("CONJUNCTION VS DISJUNCTION (DUR-006-C, as arithmetic)")
    L.append("  %d terms at p=%.2f -> conjunction survival %.6f"
             % (cd["n_terms"], cd["per_term_p"], cd["conjunction_survival"]))
    L.append("  %d holders at q=%.2f -> disjunction survival %.6f"
             % (cd["m_holders"], cd["per_holder_q"],
                cd["disjunction_survival"]))
    L.append("  per-holder number below per-term: %s"
             % cd["per_holder_below_per_term"])
    L.append("  %s" % cd["note"])
    L.append("")
    L.append("F_K ON THE ARTIFACT-SIDE SET")
    k = f_k_bound()
    L.append("  conditions %d   with a stated lifetime %d"
             % (k["n_conditions"], k["n_with_stated_lifetime"]))
    L.append("  'retention horizon' appears %d times, carries a value: %s"
             % (k["retention_horizon_mentions"],
                k["retention_horizon_has_a_value"]))
    L.append("  state %s" % k["state"])
    L.append("  %s" % k["why"])
    L.append("")
    L.append("F_M ON THE CARRIER-SIDE SET")
    fm = f_m_bound()
    for r in fm["rows"]:
        L.append("    %-6s %s"
                 % ("ADMIT" if r["admits"] else "UNINST",
                    r["condition"][:66]))
    L.append("  active set %d of %d; empty: %s"
             % (fm["n_active"], fm["n_conditions"], fm["active_set_empty"]))
    L.append("  %s" % fm["why"])
    sn = screen_has_null()
    L.append("  DUR-005-C states no null result: %s (intended: %s)"
             % (sn["states_no_null"], sn["states_intended"]))
    L.append("  %s" % sn["interaction_with_F_M"])
    L.append("")
    L.append("STEP 5 OVER SIX ENTRIES")
    rd = reconstruction_distribution_v2()
    for r in rd["rows"]:
        L.append("  %-9s %s" % (r["id"], ", ".join(r["values"]) or "--"))
    L.append("  single-valued %d of %d: %s"
             % (len(rd["single_valued"]), rd["n_entries"],
                ", ".join(rd["single_valued"])))
    L.append("  multi-valued: %s" % ", ".join(rd["multi_valued"]))
    for eid, axis in sorted(rd["axes"].items()):
        L.append("     %s varies along %s" % (eid, axis))
    L.append("  no declared value: %s"
             % (", ".join(rd["no_declared_value"]) or "none"))
    L.append("  distribution over single-valued cells only: %s"
             % rd["distribution_over_single_valued"])
    L.append("  merged distribution: %s -- %s"
             % (_fmt(rd["merged_distribution"]), rd["why_no_merge"]))
    L.append("")
    L.append("PROJECTED FRACTION")
    pf = projected_fraction_v2()
    L.append("  entries %d   PROJECTED %d   other %d   cap %s   at cap %s"
             % (pf["n_entries"], pf["n_projected"], pf["n_other"],
                _fmt(pf["cap"]), pf["at_cap"]))
    L.append("  entries stating more than one evidence class: %s"
             % ", ".join(pf["multi_valued_evidence"]))
    L.append("  %s" % pf["choice"])
    L.append("")
    fj = f_j_scope()
    L.append("F_J SCOPE")
    L.append("  section 6C: %d subsections, %d ENTRY blocks -> %s"
             % (fj["subsections"], fj["entry_blocks_in_6C"], fj["state"]))
    L.append("")
    ar = amendment_record()
    L.append("AMENDMENT RECORD")
    L.append("  %d amendments, %d carrying all four fields; incomplete %s"
             % (ar["n"], ar["complete"], ar["incomplete"] or "none"))
    so = still_open_v2()
    L.append("  still open: %d, of which %d name a missing entry"
             % (so["n"], len(so["name_a_missing_entry"])))
    L.append("")
    L.append("HOP COMPRESSION, carried from the v1 reading")
    hc = R1.hop_compression()
    L.append("  stated %s; computed band %.3g to %.3g; equal-N %.3g"
             % (_fmt(hc.get("stated")), hc["low"], hc["high"],
                hc["equal_n"]))
    L.append("  the stated figure is the LOW end of the band and the "
             "equal-N reading;")
    L.append("  v2 did not move it (FMR_016 carries unchanged).")
    L.append("")
    L.append("Nothing here rates any firm, product, arrangement or person. "
             "The probability")
    L.append("model is named, its parameters are printed, and it is used "
             "to check the")
    L.append("direction of a stated claim and for nothing else.")
    return "\n".join(L)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "register_v2.py has no selftest. The checks live in "
            "test_register_v2.py; run `python3 test_register_v2.py`.\n")
        return 2
    if "--choices" in argv:
        print(choices_report())
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
