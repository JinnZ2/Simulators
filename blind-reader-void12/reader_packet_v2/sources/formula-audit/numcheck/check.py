"""check -- data points and intersections. Co-authored.

Units first: every formula goes through branch 1 (unitaudit). Unless that
verdict is PASS, the numeric check is VOID with branch 1's reason.

A data point: "lhs = rhs", a value per symbol (a number, or an interval
[lo, hi]; with its unit and its own status tag) and a tolerance t >= 0.
With D an enclosure of lhs - rhs:
  HOLDS      D lies inside [-t, t]
  FAILS      D lies wholly outside [-t, t]
  UNDECIDED  D straddles the edge at the last tier
  VOID       units not PASS, a missing or unreadable value, no value on
             these inputs (division by an interval containing 0, ...),
             unsupported syntax, internal error
The verdict comes from the interval tier: Fraction intervals, with sqrt exp
ln sin cos as outward enclosures (precision doubling up to max_precision
when one was used). It is the only rigorous tier. float and Decimal run
first as TRIAGE: each gives a predicted_verdict or says "too close to
call". Every HOLDS / FAILS is confirmed at the interval tier, and the record
sets predicted beside confirmed; a mismatch is listed on the record and
counted in the report. The margin rule behind a prediction is a heuristic
with no bound over a long chain of steps, so a prediction is never the
verdict, unless the check asks for fast (entry "fast": true, or --fast):
then confirmation is skipped, the prediction is the verdict, and the record
carries rigorous: false.

A straddle on interval inputs is bisected (the inputs are split, widest
first, to the depth limit) and every piece is read:
  every piece HOLDS                          -> HOLDS
  pieces that HOLD and pieces that FAIL      -> MIXED: both kinds are listed
  pieces that FAIL, none that hold           -> FAILS, located
  otherwise                                  -> UNDECIDED
An UNDECIDED at tolerance 0 with no piece against it, whose two sides agree
at every sampled exact point, is put on the record as an identity candidate
("proposal"). If lhs - rhs is a polynomial in the interval inputs and is 0
on a full grid of (degree + 1) exact points per variable, that is a proof:
the proposal's status is DERIVED and it carries the proof. Otherwise it
stays PROPOSED, with the reason. The check's own verdict is not changed.

An intersection: two formulas and a region (a box: an interval per region
variable). On a subbox, both formulas HOLD (enclosure inside tolerance:
true at every point of the subbox), or one FAILS (enclosure outside: false
at every point of it), or the subbox is bisected along its widest side, to
a depth limit.
  BOTH_HOLD   every subbox reached: both hold
  MIXED       subboxes where both hold, and subboxes where one fails
              everywhere (both kinds listed)
  ONE_FAILS   subboxes where one formula fails everywhere (located), and
              none where both hold
  UNDECIDED   neither, at the depth limit
  VOID        as above; or a subbox with no value at the depth limit and no
              failure found
"""
import ast
import itertools
from decimal import Decimal
from fractions import Fraction

from unitaudit.check import check_formula as unit_check
from unitaudit.check import slot_record, split_sides, Void as UnitVoid, STATUS

from .interval import Interval
from .poly import NonPolynomial, degree_of_difference
from .tiers import DecSys, FloatSys, IntSys, NumVoid, TierCannot, evaluate

VERSION = "numcheck branch2b-4"
DEFAULTS = {"decimal_precision": 50, "precision": 30, "max_precision": 120, "depth": 8}
MAX_SUBBOXES = 20000
GRID_CAP = 10 ** 4   # largest point grid a polynomial proof will evaluate
LIST_CAP = 32        # pieces listed per kind on a record; the counts are complete


class Bad(Exception):
    pass


def to_fraction(x, what):
    if isinstance(x, bool) or x is None:
        raise Bad(f"{what}: not a number")
    if isinstance(x, (int, Fraction)):
        return Fraction(x)
    if isinstance(x, Decimal):
        if not x.is_finite():
            raise Bad(f"{what}: not finite")
        return Fraction(x)
    if isinstance(x, float):
        raise Bad(f"{what}: a binary float reached the checker; give numbers as JSON "
                  "numbers read with read_json, or as strings")
    if isinstance(x, str):
        try:
            return Fraction(x.strip())
        except (ValueError, ZeroDivisionError):
            raise Bad(f"{what}: cannot read {x!r} as a number")
    raise Bad(f"{what}: not a number")


def to_interval(v, what):
    if isinstance(v, dict) and ("lo" in v or "hi" in v):
        v = [v.get("lo"), v.get("hi")]
    if isinstance(v, (list, tuple)):
        if len(v) != 2:
            raise Bad(f"{what}: an interval needs two bounds")
        lo, hi = to_fraction(v[0], what), to_fraction(v[1], what)
        if lo > hi:
            raise Bad(f"{what}: interval bounds out of order")
        return Interval(lo, hi)
    return Interval(to_fraction(v, what))


def _blank(kind, entry, index, input_path):
    get = entry.get if isinstance(entry, dict) else (lambda *_: None)
    return {"kind": kind, "verdict": "VOID", "void_reason": None, "status": None,
            "deciding_tier": None, "precision": None, "rigorous": None, "fast": None,
            "tiers": [], "triage": None, "located": None, "proposal": None,
            "intervals": None, "inputs": None, "units": None,
            "provenance": {"source_path": get("source_path"), "input": input_path,
                           "index": index, "tool": VERSION},
            "slots": slot_record(get("slots")),
            "human_interest": None, "ai_interest": None}


def _units(formula, values):
    """Branch 1 on the formula. Returns (record summary, reason or None)."""
    symbols = {}
    for name, spec in (values or {}).items():
        symbols[name] = {"unit": spec.get("unit"), "status": spec.get("status")} \
            if isinstance(spec, dict) else {"unit": None}
    r = unit_check({"formula": formula, "symbols": symbols})
    summary = {"verdict": r["verdict"], "status": r["status"], "dims": r["dims"],
               "located_error": r["located_error"], "void_reason": r["void_reason"]}
    if r["verdict"] == "PASS":
        return summary, None
    if r["verdict"] == "FAIL":
        e = r["located_error"]
        return summary, (f"units FAIL: {e['rule']}: " + " vs ".join(e["dims"])
                         + (f" at `{e['text']}`" if e.get("text") else ""))
    return summary, f"units VOID: {r['void_reason']}"


def _parse(formula):
    try:
        lhs, rhs = (s.strip() for s in split_sides(formula))
    except UnitVoid as e:
        raise Bad(e.reason)
    try:
        return (lhs, ast.parse(lhs, mode="eval").body), (rhs, ast.parse(rhs, mode="eval").body)
    except SyntaxError as e:
        raise Bad(f"formula does not parse: {e.msg}")


def _names(tree):
    funcs = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name)}
    return {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} - funcs


def _inputs(values, needed, region=None):
    """name -> Interval, and the input records (each keeps its own tag)."""
    env, recs = {}, {}
    region = region or {}
    for name in sorted(needed):
        spec = values.get(name) if isinstance(values, dict) else None
        if not isinstance(spec, dict):
            raise Bad(f"no value given for symbol {name!r}")
        status = spec.get("status")
        if status is not None and status not in STATUS:
            raise Bad(f"symbol {name!r}: status {status!r} is not one of {', '.join(STATUS)}")
        if name in region:
            iv = to_interval(region[name], f"region {name!r}")
        elif spec.get("value") is None:
            raise Bad(f"no value given for symbol {name!r}")
        else:
            iv = to_interval(spec["value"], f"value of {name!r}")
        env[name] = iv
        recs[name] = {"value": iv.as_record(), "unit": spec.get("unit"), "status": status,
                      "from_region": name in region}
    return env, recs


def _difference(sides, env, S):
    senv = {k: (v if S.name == "interval" else S.const(v.lo)) for k, v in env.items()}
    (ls, lt), (rs, rt) = sides
    lhs = evaluate(lt, ls, senv, S)
    rhs = evaluate(rt, rs, senv, S)
    return lhs, rhs, S.sub(lhs, rhs)


def _bisect_point(sides, tol, env, prec, depth_limit):
    """A straddle on interval inputs: split the inputs (widest first) and look
    again, on every piece, to the depth limit. Returns (verdict or None, detail).
      every piece HOLDS                               -> HOLDS
      pieces that HOLD and pieces that FAIL           -> MIXED (both kinds listed)
      pieces that FAIL, none that hold                -> FAILS, located
      otherwise (pieces straddle at the depth limit)  -> None (UNDECIDED)
    A piece HOLDS / FAILS when the formula does so at every point of it."""
    if depth_limit < 0 or 2 ** depth_limit > MAX_SUBBOXES:
        raise Bad(f"depth must be between 0 and {MAX_SUBBOXES.bit_length() - 1}")
    names = sorted(n for n, v in env.items() if not v.is_point)
    stack = [({n: env[n] for n in names}, 0)]
    counts = {"examined": 0, "hold": 0, "fail": 0, "straddle_at_depth_limit": 0}
    deepest, first_open, holds, fails = 0, None, [], []
    while stack:
        box, depth = stack.pop()
        counts["examined"] += 1
        deepest = max(deepest, depth)
        _, _, d = _difference(sides, dict(env, **box), IntSys(prec))
        v, _ = IntSys(prec).judge(d, tol)
        piece = {"subbox": {n: box[n].as_record() for n in names}, "depth": depth,
                 "difference": d.as_record()}
        if v == "HOLDS":
            counts["hold"] += 1
            if len(holds) < LIST_CAP:
                holds.append(piece)
        elif v == "FAILS":
            counts["fail"] += 1
            if len(fails) < LIST_CAP:
                fails.append(piece)
        elif depth >= depth_limit:
            counts["straddle_at_depth_limit"] += 1
            first_open = first_open or piece
        else:
            widest = max(names, key=lambda n: box[n].width)
            a, b = box[widest].split()
            stack.append((dict(box, **{widest: b}), depth + 1))
            stack.append((dict(box, **{widest: a}), depth + 1))
    h, f, o = counts["hold"], counts["fail"], counts["straddle_at_depth_limit"]
    verdict = ("MIXED" if h and f else "FAILS" if f else "HOLDS" if not o else None)
    return verdict, {**counts, "depth_limit": depth_limit, "deepest": deepest,
                     "variables_split": names, "tolerance": str(tol),
                     "list_cap": LIST_CAP,
                     "reading": {"MIXED": "holds on some pieces of the given values and "
                                          "fails on others",
                                 "FAILS": "fails at every point of the located pieces; "
                                          "no piece holds",
                                 "HOLDS": "holds on every piece",
                                 None: "pieces still straddle at the depth limit"}[verdict],
                     "pieces_that_hold": holds, "pieces_that_fail": fails,
                     "pieces_that_hold_listed": len(holds), "pieces_that_fail_listed": len(fails),
                     "located": fails[0] if fails else None,
                     "first_straddling_piece": first_open}


def _polynomial_proof(sides, env, names, prec):
    """lhs - rhs as a polynomial in the interval inputs (the other symbols are
    constants at their given values). Returns (proof or None, reading).
    proof is None with a reason when it is not a polynomial or the grid is too
    large; raises _Differs when a grid point shows the two sides differ."""
    try:
        deg = degree_of_difference(sides, set(names))
    except NonPolynomial as e:
        return None, {"polynomial": False, "reason": f"non_polynomial: {e}"}
    if any(not v.is_point for n, v in env.items() if n not in names):
        return None, {"polynomial": True, "degrees": deg, "reason": "an input is not exact"}
    size = 1
    for n in names:
        size *= deg[n] + 1
    reading = {"polynomial": True, "degrees": deg, "grid_size": size, "grid_cap": GRID_CAP}
    if size > GRID_CAP:
        return None, {**reading, "reason": f"grid too large: {size} points > {GRID_CAP}"}
    axes = []
    for n in names:
        d, iv = deg[n], env[n]
        # d + 1 distinct exact values, taken inside the domain
        axes.append([iv.lo + iv.width * Fraction(k, d) if d else iv.lo for k in range(d + 1)])
    point = dict(env)
    for combo in itertools.product(*axes):
        for n, v in zip(names, combo):
            point[n] = Interval(v)
        S = IntSys(prec)
        _, _, d = _difference(sides, point, S)
        if S.used_enclosure or not d.is_point:
            return None, {**reading, "reason": "a grid value was not exact"}
        if d.lo != 0:
            raise _Differs({n: str(v) for n, v in zip(names, combo)}, str(d.lo))
    return ({"method": "polynomial_identity_by_points",
             "degrees": deg, "degree_kind": "upper bounds read from the ast",
             "grid_points_per_variable": {n: deg[n] + 1 for n in names},
             "grid": {n: [str(v) for v in ax] for n, ax in zip(names, axes)},
             "grid_size": size, "difference_at_every_grid_point": "0",
             "arithmetic": "exact (Fraction)",
             "argument": "a polynomial of degree at most d_i in each variable that is 0 on "
                         "a full grid of d_i + 1 distinct values per variable is the zero "
                         "polynomial",
             "scope": "all values of " + ", ".join(names)
                      + (" (not only the given domain)" if names else "")
                      + "; every other symbol at its given value"},
            reading)


class _Differs(Exception):
    def __init__(self, at, value):
        super().__init__("differs")
        self.at, self.value = at, value


def _identity_candidate(entry, sides, tol, env, rec, prec, index, input_path):
    """tolerance 0, interval inputs, UNDECIDED, and nothing against it: the two
    sides may be the same function. Sample exact points; if the difference
    is 0 at every one, hand the pair on as a PROPOSED identity. Nothing is
    proved here by sampling. If lhs - rhs is a polynomial in the interval
    inputs, the full-grid check of _polynomial_proof IS a proof: the
    proposal then carries it and its status is DERIVED."""
    b = rec["bisection"]
    if tol != 0 or b is None or b["hold"] or b["fail"]:
        return None
    names = b["variables_split"]
    fracs = (Fraction(0), Fraction(1), Fraction(1, 2), Fraction(1, 3), Fraction(5, 7),
             Fraction(2, 11), Fraction(9, 13))
    points = [{n: env[n].lo + env[n].width * t for n in names} for t in fracs]
    if len(names) > 1:                      # off the diagonal too
        for k in range(len(fracs)):
            points.append({n: env[n].lo + env[n].width * fracs[(k + 2 * i + 1) % len(fracs)]
                           for i, n in enumerate(names)})
    exact = contain = void = 0
    for pt in points:
        try:
            _, _, d = _difference(sides, dict(env, **{n: Interval(v) for n, v in pt.items()}),
                                  IntSys(prec))
        except NumVoid:
            void += 1
            continue
        if not d.contains(0):
            return None                      # the two sides differ at a sampled point
        contain += 1
        exact += d.is_point
    if not contain:
        return None
    try:
        proof, reading = _polynomial_proof(sides, env, names, prec)
    except _Differs:
        return None                          # a grid point shows they are not equal
    return {"lhs": sides[0][0], "rhs": sides[1][0],
            "domain": {n: {"lo": str(env[n].lo), "hi": str(env[n].hi)} for n in names},
            "fixed": {n: str(v.lo) for n, v in sorted(env.items()) if v.is_point},
            "units": {n: rec["inputs"][n]["unit"] for n in sorted(env)},
            "source_check": {"input": input_path, "index": index, "formula": rec["formula"],
                             "source_path": rec["provenance"]["source_path"]},
            "status": "DERIVED" if proof else "PROPOSED",
            "polynomial": reading,
            "proof": proof, "proof_attempted": proof is not None,
            "why_not_proved": None if proof else reading["reason"],
            "evidence": {"verdict": "UNDECIDED at tolerance 0",
                         "pieces_straddling_at_depth_limit": b["straddle_at_depth_limit"],
                         "depth_limit": b["depth_limit"],
                         "sample_points": len(points),
                         "samples_with_difference_exactly_0": exact,
                         "samples_whose_enclosure_contains_0": contain,
                         "samples_with_no_value": void,
                         "note": "sampling is evidence, not proof"},
            "human_interest": None, "ai_interest": None}


def check_point(entry, index=None, input_path=None, fast=False):
    rec = _blank("point", entry, index, input_path)
    try:
        if not isinstance(entry, dict) or not isinstance(entry.get("formula"), str):
            raise Bad("no formula string")
        formula = entry["formula"]
        rec["formula"] = formula
        rec["units"], reason = _units(formula, entry.get("values"))
        if reason:
            raise Bad(reason)
        sides = _parse(formula)
        tol = to_fraction(entry.get("tolerance", 0), "tolerance")
        if tol < 0:
            raise Bad("tolerance is negative")
        env, rec["inputs"] = _inputs(entry.get("values"),
                                     _names(sides[0][1]) | _names(sides[1][1]))
        opt = {k: entry.get(k, d) for k, d in DEFAULTS.items()}
        fast = bool(entry.get("fast", fast))
        rec["fast"] = fast
        points = all(v.is_point for v in env.values())
        tiers = rec["tiers"]
        verdict = None
        # float and Decimal are TRIAGE: each predicts the verdict or says "too close
        # to call". Neither is an enclosure. They decide only under fast.
        for S in (FloatSys(), DecSys(int(opt["decimal_precision"]))):
            if not points:
                tiers.append({"tier": S.name, "role": "triage", "outcome": "skipped",
                              "predicted_verdict": None, "reason": "an input is an interval"})
                continue
            guess = None
            try:
                _, _, d = _difference(sides, env, S)
                guess, detail = S.judge(d, tol)
                tiers.append({"tier": S.name, "role": "triage", "precision": S.precision,
                              "outcome": "predicts" if guess else "too close to call",
                              "predicted_verdict": guess,
                              **{k: (v if isinstance(v, str) else repr(v))
                                 for k, v in detail.items()}})
            except (TierCannot, NumVoid) as e:
                tiers.append({"tier": S.name, "role": "triage", "precision": S.precision,
                              "outcome": "cannot run", "predicted_verdict": None, "reason": str(e)})
            if guess and fast:
                verdict = guess
                tiers[-1]["role"] = "decided (fast)"
                rec.update(verdict=verdict, deciding_tier=S.name, precision=S.precision,
                           rigorous=False, status="DERIVED")
                break
        if not verdict:
            prec = int(opt["precision"])
            while True:
                S = IntSys(prec)
                lhs, rhs, d = _difference(sides, env, S)
                verdict, _ = S.judge(d, tol)
                exact = not S.used_enclosure
                tiers.append({"tier": "interval", "role": "confirms", "predicted_verdict": None,
                              "precision": "exact" if exact else prec,
                              "outcome": "decided" if verdict else "straddles the tolerance edge"})
                rec["intervals"] = {"lhs": lhs.as_record(), "rhs": rhs.as_record(),
                                    "difference": d.as_record(), "tolerance": str(tol)}
                if verdict or exact or prec * 2 > int(opt["max_precision"]):
                    break
                prec *= 2
            rec["bisection"] = None
            if not verdict and not points:
                verdict, rec["bisection"] = _bisect_point(sides, tol, env, prec,
                                                          int(opt["depth"]))
                rec["located"] = rec["bisection"]["located"]
                rec["verdict"] = verdict or "UNDECIDED"
                rec["proposal"] = _identity_candidate(entry, sides, tol, env, rec, prec,
                                                      index, input_path)
            rec.update(verdict=verdict or "UNDECIDED", deciding_tier="interval",
                       precision="exact" if exact else prec, rigorous=True, status="DERIVED")
        confirmed = rec["verdict"] if rec["rigorous"] else None
        per_tier = [{"tier": t["tier"], "predicted_verdict": t["predicted_verdict"],
                     "confirmed_verdict": confirmed,
                     "match": None if confirmed is None else t["predicted_verdict"] == confirmed}
                    for t in tiers if t.get("predicted_verdict")]
        rec["triage"] = {"predictions": per_tier,
                         "confirmed_verdict": confirmed,
                         "confirmed_at": "interval" if confirmed else None,
                         "mismatches": [x["tier"] for x in per_tier if x["match"] is False],
                         "note": None if confirmed else
                         "fast: the prediction was taken as the verdict, not confirmed"}
    except (Bad, NumVoid) as e:
        rec.update(verdict="VOID", void_reason=str(e), status=None)
    except Exception as e:                       # fail closed
        rec.update(verdict="VOID", void_reason=f"internal: {type(e).__name__}: {e}", status=None)
    return rec


def check_intersection(entry, index=None, input_path=None):
    rec = _blank("intersection", entry, index, input_path)
    try:
        forms = entry.get("formulas") if isinstance(entry, dict) else None
        if not isinstance(forms, list) or len(forms) != 2:
            raise Bad("an intersection needs exactly two formulas")
        region = entry.get("region")
        if not isinstance(region, dict) or not region:
            raise Bad("an intersection needs a region: {variable: [lo, hi]}")
        values = entry.get("values")
        parsed, rec["units"], rec["formulas"] = [], [], []
        needed = set()
        for i, f in enumerate(forms):
            if not isinstance(f, dict) or not isinstance(f.get("formula"), str):
                raise Bad(f"formula {i + 1}: no formula string")
            u, reason = _units(f["formula"], values)
            rec["units"].append(u)
            rec["formulas"].append(f["formula"])
            if reason:
                raise Bad(f"formula {i + 1}: {reason}")
            sides = _parse(f["formula"])
            tol = to_fraction(f.get("tolerance", 0), f"tolerance {i + 1}")
            if tol < 0:
                raise Bad(f"tolerance {i + 1} is negative")
            parsed.append((sides, tol))
            needed |= _names(sides[0][1]) | _names(sides[1][1])
        for name in region:
            if name not in needed:
                raise Bad(f"region variable {name!r} is in neither formula")
        env, rec["inputs"] = _inputs(values, needed, region)
        prec = int(entry.get("precision", DEFAULTS["precision"]))
        depth_limit = int(entry.get("depth", DEFAULTS["depth"]))
        if depth_limit < 0 or 2 ** depth_limit > MAX_SUBBOXES:
            raise Bad(f"depth must be between 0 and {MAX_SUBBOXES.bit_length() - 1}")
        names = sorted(region)
        stack = [({n: env[n] for n in names}, 0)]
        counts = {"examined": 0, "both_hold": 0, "undecided_at_depth_limit": 0,
                  "no_value_at_depth_limit": 0}
        first_open, first_void, deepest = None, None, 0
        holds, fails = [], []
        counts["one_fails"] = 0
        while stack:
            box, depth = stack.pop()
            counts["examined"] += 1
            deepest = max(deepest, depth)
            cur = dict(env, **box)
            state, void_reason, diffs = [], None, []
            for sides, tol in parsed:
                S = IntSys(prec)
                try:
                    _, _, d = _difference(sides, cur, S)
                    state.append(S.judge(d, tol)[0])
                    diffs.append(d.as_record())
                except NumVoid as e:
                    state.append("VOID")
                    diffs.append(None)
                    void_reason = str(e)
            sub = {n: box[n].as_record() for n in names}
            if "FAILS" in state:
                i = state.index("FAILS")
                counts["one_fails"] += 1
                if len(fails) < LIST_CAP:
                    fails.append({"subbox": sub, "depth": depth, "formula_number": i + 1,
                                  "formula": rec["formulas"][i], "difference": diffs[i],
                                  "tolerance": str(parsed[i][1]),
                                  "other_formula_on_this_subbox": state[1 - i]})
            elif state == ["HOLDS", "HOLDS"]:
                counts["both_hold"] += 1
                if len(holds) < LIST_CAP:
                    holds.append({"subbox": sub, "depth": depth})
            elif depth >= depth_limit:
                if void_reason:
                    counts["no_value_at_depth_limit"] += 1
                    first_void = first_void or {"subbox": sub, "depth": depth,
                                                "reason": void_reason}
                else:
                    counts["undecided_at_depth_limit"] += 1
                    first_open = first_open or {"subbox": sub, "depth": depth,
                                                "states": state, "differences": diffs}
            else:
                widest = max(names, key=lambda n: box[n].width)
                if box[widest].width == 0:
                    counts["undecided_at_depth_limit"] += 1
                    first_open = first_open or {"subbox": sub, "depth": depth, "states": state,
                                                "differences": diffs}
                    continue
                a, b = box[widest].split()
                stack.append((dict(box, **{widest: b}), depth + 1))
                stack.append((dict(box, **{widest: a}), depth + 1))
        located = fails[0] if fails else None
        rec["subboxes"] = {**counts, "depth_limit": depth_limit, "deepest": deepest,
                           "list_cap": LIST_CAP}
        rec["located"] = located
        rec["subboxes_where_both_hold"] = holds
        rec["subboxes_where_one_fails"] = fails
        rec["first_undecided_subbox"] = first_open
        rec["first_subbox_with_no_value"] = first_void
        rec.update(deciding_tier="interval", precision=prec, rigorous=True)
        if located and counts["both_hold"]:
            rec.update(verdict="MIXED", status="DERIVED")
        elif located:
            rec.update(verdict="ONE_FAILS", status="DERIVED")
        elif counts["no_value_at_depth_limit"]:
            rec.update(verdict="VOID", status=None,
                       void_reason="no value on a subbox at the depth limit: "
                                   + first_void["reason"])
        elif counts["undecided_at_depth_limit"]:
            rec.update(verdict="UNDECIDED", status="DERIVED")
        else:
            rec.update(verdict="BOTH_HOLD", status="DERIVED")
    except (Bad, NumVoid) as e:
        rec.update(verdict="VOID", void_reason=str(e), status=None)
    except Exception as e:                       # fail closed
        rec.update(verdict="VOID", void_reason=f"internal: {type(e).__name__}: {e}", status=None)
    return rec


def check_all(data, input_path=None, fast=False):
    entries = data.get("checks") if isinstance(data, dict) and "checks" in data else data
    if not isinstance(entries, list):
        entries = [entries]
    records = []
    for i, e in enumerate(entries):
        kind = e.get("kind", "point") if isinstance(e, dict) else "point"
        if kind == "intersection":
            records.append(check_intersection(e, i, input_path))
        elif kind == "point":
            records.append(check_point(e, i, input_path, fast))
        else:
            r = _blank(str(kind), e, i, input_path)
            r["void_reason"] = f"unknown kind {kind!r}"
            records.append(r)
    names = ("HOLDS", "FAILS", "MIXED", "UNDECIDED", "VOID", "BOTH_HOLD", "ONE_FAILS")
    tri = [r["triage"] for r in records if r.get("triage")]
    return {"tool": VERSION, "input": input_path, "fast": fast,
            "counts": {v: sum(1 for r in records if r["verdict"] == v) for v in names},
            "triage": {"predictions": sum(len(t["predictions"]) for t in tri),
                       "confirmed": sum(1 for t in tri for x in t["predictions"]
                                        if x["match"] is True),
                       "mismatches": sum(len(t["mismatches"]) for t in tri),
                       "not_confirmed_fast": sum(1 for t in tri for x in t["predictions"]
                                                 if x["match"] is None),
                       "mismatch_log": [{"index": r["provenance"]["index"],
                                         "formula": r.get("formula"),
                                         "tiers": r["triage"]["mismatches"],
                                         "predictions": r["triage"]["predictions"]}
                                        for r in records
                                        if r.get("triage") and r["triage"]["mismatches"]]},
            "proposals": [r["proposal"] for r in records if r.get("proposal")],
            "records": records}
