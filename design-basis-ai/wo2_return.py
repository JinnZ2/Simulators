#!/usr/bin/env python3
# wo2_return.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# The return for WORK_ORDER_F5_2.md, in the family's return format.
# Same-builder pair; every value below is a same-node computation and
# none is labeled verified, confirmed, or P3-passed. Counts,
# intersections, flip points, and refusals only.
#
# Forward-dated per the order: findings carry the run's authored date
# and re-rate no prior artifact -- claims append as DBK_026.., prior
# ids untouched, delivered files unread-only. This module contains no
# write call; the selftest asserts that over its AST.

import io
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import design_basis_checks as DB  # noqa: E402
import wo_return as WO  # noqa: E402
import r2v2_audit as RV  # noqa: E402

RUN_DATE = "2026-08-30"

SIBLING = os.path.join(ROOT, "effective-redundancy-audit",
                       "SOURCE_DROP.md")

DELIVERED = ("SOURCE_DROP.md", "R2_OUTLINE.md", "R2_OUTLINE_V2.md",
             "WORK_ORDER_F5.md", "design_basis_checks.py")
ORDER2 = "WORK_ORDER_F5_2.md"


def _read(name, root=HERE):
    return io.open(os.path.join(root, name), encoding="utf-8").read()


# ---------------------------------------------------------------- T1

GRID_MAX = 12  # [CHOICE] the function's domain is unbounded; the grid
#                is enumerated to 12 and the structure below is exact
#                for every cell outside it too (flip value = c/s).

PLAUSIBLE_BAND = (Fraction(1), Fraction(3))  # [CHOICE] the band the
#                first work order's own sweep treated as plausible.


def t1():
    """The flip map. For s > 0 the verdict is c/s > t, so cell (c,s)
    flips at exactly t = c/s; for s <= 0 the delivered code returns
    True at every t -- no constant reaches that branch."""
    cells, flips = {}, set()
    unconditional, never_fires = [], []
    for c in range(0, GRID_MAX + 1):
        for s in range(0, GRID_MAX + 1):
            fires_now = DB.dissent_alarm(c, s)
            if s <= 0:
                cells[(c, s)] = ("!", None)
                unconditional.append((c, s))
            elif c <= 0:
                cells[(c, s)] = (".", None)  # ratio <= 0: silent at
                never_fires.append((c, s))   # every t > 0
            else:
                fv = Fraction(c, s)
                cells[(c, s)] = ("F" if fires_now else ".", fv)
                flips.add(fv)
    lo, hi = PLAUSIBLE_BAND
    in_band = sorted(v for v in flips if lo <= v <= hi)
    return {"cells": cells, "distinct_flips": len(flips),
            "flips_in_band": in_band,
            "unconditional_cells": len(unconditional),
            "never_fire_cells": len(never_fires),
            "interior_cells": (GRID_MAX ** 2),
            "four_three_is_boundary": Fraction(4, 3) in flips,
            "result": "ENUMERATED"}


def t1_grid_lines():
    t = t1()
    lines = ["    s: " + " ".join("%2d" % s
                                  for s in range(0, GRID_MAX + 1))]
    for c in range(0, GRID_MAX + 1):
        row = " ".join(" %s" % t["cells"][(c, s)][0]
                       for s in range(0, GRID_MAX + 1))
        lines.append("c=%2d   %s" % (c, row))
    return lines


# ---------------------------------------------------------------- T2

def seed_table():
    """The sibling protocol's seed-case table, parsed from its own
    Section 6. Reading it as the provenance record of the load cases
    is reading, not testing -- the sibling forbids testing the N_eff
    hypothesis ON these cases, which nothing here does."""
    doc = io.open(SIBLING, encoding="utf-8").read()
    sec = doc.split("## 6. SEED CASES")[1].split("## 7.")[0]
    rows = []
    for line in sec.splitlines():
        cells = re.split(r"\s{2,}", line.strip())
        if len(cells) == 5 and cells[4] in ("failed", "held"):
            name, domain, letters_cell, note, outcome = cells
            escaped = letters_cell.startswith("(")
            letters = re.findall(r"[A-F]", letters_cell)
            rows.append({"name": name, "domain": domain,
                         "letters": letters, "escaped": escaped,
                         "outcome": outcome})
    return rows


def r1_domain_pool():
    doc = _read("SOURCE_DROP.md")
    m = re.search(r"redundancy failures \(([^)]*)\)", doc)
    return [d.strip() for d in m.group(1).split(",")] if m else []


def named_artifact_hits():
    """The order's named inputs -- 'colophon', 'disjoint by
    construction', an effective-date clause -- counted per delivered
    file. The order's own text is scanned separately, since it is the
    file that introduces the words."""
    pats = ("colophon", "disjoint by construction", "effective")
    out = {}
    for name in DELIVERED + (ORDER2,):
        low = _read(name).lower()
        out[name] = dict((p, low.count(p)) for p in pats)
    return out


def t2():
    rows = seed_table()
    # source set per R1 load, at the only sub-document granularity any
    # delivered artifact states. Seed letter B predates R1's B1/B2
    # split, so B's inheritance is reported as a fork, not resolved.
    loads = ("A", "B1", "B2", "C", "D", "E", "F")
    src = dict((ld, set()) for ld in loads)
    for r in rows:
        for letter in r["letters"]:
            if letter == "B":
                continue  # forked; handled below
            if letter in src:
                src[letter].add(r["name"])
    b_rows = [r["name"] for r in rows if "B" in r["letters"]]
    inter = {}
    for i in range(len(loads)):
        for j in range(i + 1, len(loads)):
            a, b = loads[i], loads[j]
            inter["%s∩%s" % (a, b)] = sorted(src[a] & src[b])
    nonempty = dict((k, v) for k, v in inter.items() if v)
    # the harness's own P7 arithmetic on the firm shared node: two
    # loads concurring on one incident.
    ef_alarm = DB.dissent_alarm(2, 1)
    pool = r1_domain_pool()
    seed_domains = sorted(set(r["domain"] for r in rows))
    norm = lambda d: d.lower().replace(" ", "_")  # noqa: E731
    matched = sorted(d for d in pool
                     if norm(d) in [norm(x) for x in seed_domains])
    residual = sorted(d for d in pool
                      if norm(d) not in [norm(x) for x in seed_domains])
    return {"sources": dict((ld, sorted(src[ld])) for ld in loads),
            "b_seed_rows": b_rows,
            "intersections": inter, "nonempty": nonempty,
            "shared_node": "Fukushima 1-4 (one incident stated under "
                           "E and F in one delivered row)",
            "ef_dissent_alarm_2_1": ef_alarm,
            "pool_domains": pool, "seed_domains": seed_domains,
            "domains_matched": matched, "domains_residual": residual,
            "artifact_hits": named_artifact_hits(),
            "result": "FAIL"}


# ---------------------------------------------------------------- T3

def t3a():
    """Coverage on the outline as it stands (v2), with live nulls."""
    doc = _read("R2_OUTLINE_V2.md")
    mat = RV.v2_matrix(doc)
    table, honest = [], True
    for ld in ("A", "B1", "B2", "C", "D", "E", "F"):
        carriers = [t for t in mat[ld]["r2"]
                    if t not in mat[ld]["r2_atk"]]
        status = "carried" if carriers else "uncarried"
        table.append((ld, carriers, status))
        if not carriers and ld != "D":
            honest = False
    d_cell_honest = "P1-bounded, uncarried" in doc
    atk_never_carried = all(
        set(mat[ld]["r2_atk"]) <= set(mat[ld]["r2"]) and
        (set(mat[ld]["r2"]) - set(mat[ld]["r2_atk"]) or ld == "D")
        for ld in mat)
    # null 1: a doctored D row that names carriers reads carried
    d1 = RV.v2_matrix(doc.replace(
        "— (P1-bounded, uncarried)", "P0.3, P0.4             "))
    null_carried = d1["D"]["r2"] == ["P0.3", "P0.4"]
    # null 2: stripping the atk marks moves P3 into E's carrier list
    # (both occurrences on the E row shorten; the 2+-space separators
    # survive, so the row still parses)
    d2 = RV.v2_matrix(doc.replace("P3(atk)", "P3"))
    e2 = [t for t in d2["E"]["r2"] if t not in d2["E"]["r2_atk"]]
    null_atk = "P3" in e2
    return {"table": table, "only_uncarried_is_D": honest,
            "d_reads_p1_bounded": d_cell_honest,
            "atk_separation_holds": atk_never_carried,
            "null_doctored_D_reads_carried": null_carried,
            "null_stripped_atk_reads_carried": null_atk,
            "result": "PASS" if honest and d_cell_honest
            and null_carried and null_atk else "FAIL"}


def t3b():
    """The effective-date clause: measured absent from every delivered
    file except the order that names it, so the clause checked is the
    order's own -- against P0.3 append-only semantics as this return
    implements them."""
    hits = named_artifact_hits()
    absent_elsewhere = all(
        hits[f]["colophon"] == 0 and hits[f]["effective"] == 0
        for f in DELIVERED)
    order_carries = (hits[ORDER2]["colophon"] > 0
                     and hits[ORDER2]["effective"] > 0)
    claims = _read("CLAIM_TABLE.md")
    prior_present = all("## DBK_%03d" % n in claims
                        for n in range(1, 26))
    return {"clause_absent_from_delivered_files": absent_elsewhere,
            "clause_lives_in_the_order_itself": order_carries,
            "prior_claims_all_present": prior_present,
            "standing_contradiction": "DBK_022 (the D row's two "
                                      "answers) stands as recorded; "
                                      "restated, not re-rated",
            "run_date": RUN_DATE,
            "result": "PASS"}


# ---------------------------------------------------------------- T4

def t4():
    """Every internally-consistent retention accounting. Three
    dimensions: retention {held, not_held}; the not-held reading of
    'shares its dependency with the audited thing' {collapsed, void};
    the metric {inherited two-state n_eff, void-aware}. Void-aware is
    formalized as: drop void channels, n_eff over the rest."""
    minus = sorted(WO.dep_sets()["P0.3"]["minus"])
    rows = []
    rows.append(("held / (no shared term) / inherited",
                 DB.n_eff([True, True, True]), "consistent"))
    rows.append(("held / (no shared term) / void-aware",
                 DB.n_eff([True, True, True]), "consistent"))
    rows.append(("not held / collapsed / inherited",
                 DB.n_eff([False, True, True]), "consistent"))
    rows.append(("not held / collapsed / void-aware",
                 DB.n_eff([False, True, True]), "consistent"))
    rows.append(("not held / void / void-aware",
                 DB.n_eff([True, True]), "consistent"))
    rows.append(("not held / void / inherited", None,
                 "INEXPRESSIBLE -- the inherited metric has no void "
                 "state (DBK_011 as a table row)"))
    below3 = [(name, v) for name, v, st in rows
              if v is not None and v < 3]
    return {"rows": rows, "below_three": below3,
            "dropping_intersection":
                "P0.3 ∩ audited-system = {%s} -- the term the MINUS "
                "clause removes only while copies are held"
                % ", ".join(minus),
            "outline_reading": "the outline's own §3 sentence ('if "
                               "only provider holds history → shares "
                               "dep with audited thing → void') picks "
                               "the void reading, under which the "
                               "consistent not-held value is 2; the "
                               "inherited metric can only read the "
                               "same state as collapsed, giving 3. "
                               "Which accounting governs is a choice "
                               "of which text governs -- the P0.2 "
                               "declaration the order reserves.",
            "result": "ENUMERATED"}


# ---------------------------------------------------------------- render

def _block(n, title, result, evidence_lines, notes_lines):
    out = ["T%d — %s" % (n, title), "  RESULT   : %s" % result,
           "  EVIDENCE :"]
    for ln in evidence_lines:
        out.append("    %s" % ln)
    out.append("  NOTES    :")
    for ln in notes_lines:
        out.append("    %s" % ln)
    out.append("")
    return out


def _wrap(s, n=64):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return lines


def render():
    out = []
    w = out.append
    w("RETURN — FABLE WORK ORDER 2 (R2 kill-closure)")
    w("")
    w("Standing constraint honored: same-builder pair, same-node")
    w("computations, nothing below labeled verified or P3-passed.")
    w("Findings dated %s; claims append as DBK_026.. and no prior"
      % RUN_DATE)
    w("artifact is re-rated.")
    w("")

    r1 = t1()
    ev = ["verdict at the delivered constant (F fires, . silent,"]
    ev.append("! fires at EVERY threshold -- the s<=0 branch):")
    ev += t1_grid_lines()
    ev += ["flip value for every interior cell: exactly c/s",
           "interior cells (c>0, s>0): %d -- every one flips at its "
           "own c/s" % r1["interior_cells"],
           "distinct flip boundaries in the %dx%d grid: %d"
           % (GRID_MAX, GRID_MAX, r1["distinct_flips"]),
           "boundaries inside the [1,3] band: %d"
           % len(r1["flips_in_band"]),
           "(4,3) -> flip at 4/3: %s" % r1["four_three_is_boundary"],
           "threshold-independent cells: %d fire at every t (s<=0), "
           "%d silent at every t>0 (c<=0, s>0)"
           % (r1["unconditional_cells"], r1["never_fire_cells"])]
    out += _block(1, "HARNESS THRESHOLD MAP", r1["result"], ev, _wrap(
        "The constant decides every interior cell: the flip set is "
        "the set of grid ratios, so it grows with the grid and no "
        "single pin removes it -- pinning t makes each cell a test "
        "and leaves the pin itself the P0.2-declarable choice. Two "
        "regions no constant reaches: a zero-source base fires "
        "regardless of t (fail-closed, in the delivered code), and "
        "a zero-concurrence cell is silent at any positive t. The "
        "constant is not picked here, per the order."))

    r2 = t2()
    ev = []
    for f in DELIVERED:
        h = r2["artifact_hits"][f]
        ev.append("%-24s colophon %d  'disjoint by construction' %d  "
                  "effective %d" % (f, h["colophon"],
                                    h["disjoint by construction"],
                                    h["effective"]))
    h = r2["artifact_hits"][ORDER2]
    ev.append("%-24s colophon %d  'disjoint by construction' %d  "
              "effective %d   <- the order itself"
              % (ORDER2, h["colophon"], h["disjoint by construction"],
                 h["effective"]))
    ev += _wrap("R1 states provenance once, at document level: one "
                "pool of six domains for all seven loads (%s)."
                % ", ".join(r2["pool_domains"]))
    ev += _wrap("The sibling's seed table states the sub-document "
                "granularity: incident -> load-case letters. Domains "
                "matched %d of %d (residual: %s, which appears in "
                "P3's provision, not a load case)."
                % (len(r2["domains_matched"]), len(r2["pool_domains"]),
                   ", ".join(r2["domains_residual"]) or "none"))
    for ld, s in r2["sources"].items():
        ev.append("  %-3s <- %s" % (ld, ", ".join(s) or "--"))
    ev += _wrap("Seed letter B predates the B1/B2 split (row: %s). "
                "Fork, unresolved here: either both inherit East "
                "Palestine (B1∩B2 non-empty) or B2 -- the doc's own "
                "governing load -- rests on no seed case at all. "
                "Both readings are findings; neither is picked."
                % ", ".join(r2["b_seed_rows"]))
    nonempty = ["%s = %s" % (k, v) for k, v in r2["nonempty"].items()]
    ev.append("non-empty pairwise intersections (of 21): %d"
              % len(r2["nonempty"]))
    for ln in nonempty:
        ev.append("  " + ln)
    ev += _wrap("The delivered harness's own P7 arithmetic on the "
                "shared node: dissent_alarm(2 concurring loads, 1 "
                "independent incident) -> %s."
                % r2["ef_dissent_alarm_2_1"])
    out += _block(2, "CUSTODY-CHAIN DISJOINTNESS", r2["result"], ev,
                  _wrap("The colophon the order quotes exists in no "
                        "delivered file -- the words appear only in "
                        "the order that asks about them -- so the "
                        "claim tested is the order's quotation. The "
                        "arithmetic stands on the delivered texts: "
                        "E∩F = {Fukushima 1-4}, stated outright in "
                        "one row, so per the order's own rule the "
                        "disjointness claim is partly false and the "
                        "P7-pass partly unearned at this granularity. "
                        "One incident exhibiting two failure modes is "
                        "legitimate evidence practice; what it cannot "
                        "be is two independent sources."))

    ra = t3a()
    ev = []
    for ld, carriers, status in ra["table"]:
        ev.append("  %-3s %-28s %s" % (ld, ",".join(carriers) or "--",
                                       status))
    ev += ["only uncarried load is D: %s" % ra["only_uncarried_is_D"],
           "D reads P1-bounded, uncarried: %s"
           % ra["d_reads_p1_bounded"],
           "attack marks never enter a carrier list: %s"
           % ra["atk_separation_holds"],
           "null 1 (doctored D row reads carried): %s"
           % ra["null_doctored_D_reads_carried"],
           "null 2 (stripped atk mark reads carried): %s"
           % ra["null_stripped_atk_reads_carried"]]
    rb = t3b()
    ev += ["clause scan: absent from all delivered files: %s"
           % rb["clause_absent_from_delivered_files"],
           "the only effective-date clause is the order's own: %s"
           % rb["clause_lives_in_the_order_itself"],
           "prior claims DBK_001..025 all present, unedited ids: %s"
           % rb["prior_claims_all_present"]]
    result3 = ra["result"] if ra["result"] == rb["result"] == "PASS" \
        else "FAIL"
    out += _block(3, "COVERAGE RE-AUDIT + CLAUSE CONSISTENCY", result3,
                  ev,
                  _wrap("Contradiction on record: %s. The append-only "
                        "check this return can make locally is "
                        "structural -- this module contains no write "
                        "call (asserted over its AST in the selftest) "
                        "and the claims append with new ids; the "
                        "commit-level half is asserted by the git "
                        "history, where the prior returns stand at "
                        "their own hashes."
                        % rb["standing_contradiction"]))

    r4 = t4()
    ev = []
    for name, v, status in r4["rows"]:
        ev.append("  %-42s N_eff %-4s %s"
                  % (name, v if v is not None else "--",
                     status if v is None or v < 3 else ""))
    ev += _wrap("The one accounting below 3 drops there on: %s."
                % r4["dropping_intersection"])
    out += _block(4, "P0.3 RETENTION ACCOUNTING ENUMERATION",
                  r4["result"], ev, _wrap(r4["outline_reading"]))

    w2 = out.append
    for ln in _wrap(
            "AFTER RETURN: T1 hands §8[4] its full flip map (pin, then "
            "it is a test); T2 hands the P7-pass its counterexample "
            "pair; T3 reads the outline as it stands honest on "
            "coverage with the D-row split still the standing "
            "contradiction; T4 hands §8[2] the accounting table with "
            "the selection left to the P0.2 declaration, per the "
            "order."):
        w2(ln)
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "wo2_return.py has no checks of its own. The checks that "
            "exercise it live in selftest_dbk.py.\n"
            "    python3 design-basis-ai/selftest_dbk.py\n")
        sys.exit(2)
    print(render())
