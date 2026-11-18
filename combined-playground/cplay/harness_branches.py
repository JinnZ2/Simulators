"""G5 item 7: harness classes, two branches side by side, no winner (9c VOID-7, BRANCHED).

H-A  by INFORMATION SOURCE, M7's labels: KNOWN_ANSWER (>= 1 non-circular case), CIRCULAR (every
     case derived from the formula under test), PLANTED_FAULT (signal plants, no cases), NULL_ONLY
     (null plants only).
H-B  by MEASURED POWER: plant N faults into the harness's own domain (mutants of the function under
     test, formula-audit practice) and count how many the harness's cases catch; run equivalent
     rewrites (nulls) and count false alarms. Bins come from the measured counts only:
     CATCHES_ALL / PARTIAL / CATCHES_NONE and QUIET / NOISY; no case -> NOT_MEASURABLE.
     There is no pre-set threshold.
SPLIT  H-A says KNOWN_ANSWER and H-B does not measure CATCHES_ALL.

DECIDED on evidence (2026-11-18): H-A is kept as the provenance field, H-B is the power rating.
Evidence round: ADDED cases (RSS vs linear-sum separation; Poisson lam = 1) re-measured; the
before / after counts are both reported.

Scope (reading taken here): "every harness in the repo" is read as every known-answer harness the
combined playground can run as code: en_compare, extinction_poisson and the M4 verdict (G), plus
two constructed harnesses showing NULL_ONLY and PLANTED_FAULT. Mutants and nulls are written here
and listed by name.
"""
import math
from collections import namedtuple

from . import closure as C
from . import families as F
from . import gates as G

HA_LABELS = ("KNOWN_ANSWER", "NULL_ONLY", "PLANTED_FAULT", "CIRCULAR")

Case = namedtuple("Case", "inputs expected provenance")
Harness = namedtuple("Harness", "name tested fn cases mutants nulls plants_signal plants_null")


def _en(x1, U1, x2, U2):
    return G.en_compare(x1, U1, x2, U2).token.state


def _en_mut(rule):
    def f(x1, U1, x2, U2):
        d = x1 - x2
        uc = rule["uc"](U1, U2)
        if uc == 0:
            return "VOID"
        en = rule["en"](d, uc)
        return "OK" if rule["cmp"](en) else "FAILED"
    return f


_SQ = lambda U1, U2: math.sqrt(U1 * U1 + U2 * U2)
EN_MUTANTS = {
    "uc_linear_sum": _en_mut({"uc": lambda a, b: a + b, "en": lambda d, u: abs(d) / u, "cmp": lambda e: e <= 1}),
    "strict_less": _en_mut({"uc": _SQ, "en": lambda d, u: abs(d) / u, "cmp": lambda e: e < 1}),
    "uc_first_only": _en_mut({"uc": lambda a, b: a, "en": lambda d, u: abs(d) / u, "cmp": lambda e: e <= 1}),
    "always_ok": lambda x1, U1, x2, U2: "OK",
    "threshold_two": _en_mut({"uc": _SQ, "en": lambda d, u: abs(d) / u, "cmp": lambda e: e <= 2}),
}
EN_NULLS = {
    "hypot": _en_mut({"uc": lambda a, b: math.hypot(a, b), "en": lambda d, u: abs(d) / u, "cmp": lambda e: e <= 1}),
    "fabs": _en_mut({"uc": _SQ, "en": lambda d, u: math.fabs(d) / u, "cmp": lambda e: e <= 1}),
}

EN_CASES_STRONG = (
    Case((10.0, 0.3, 10.4, 0.4), "OK", "hand calc: |d| 0.4, U_c 0.5, En 0.8"),
    Case((10.0, 0.3, 11.0, 0.4), "FAILED", "hand calc: En 2.0"),
    Case((0.0, 3.0, 5.0, 4.0), "OK", "hand calc: En exactly 1 (3-4-5)"),
    Case((10.0, 0.3, 11.5, 0.4), "FAILED", "hand calc: En 3.0"),
    Case((1.0, 0.0, 1.0, 0.0), "VOID", "hand calc: U_c 0"),
    Case((0.0, 0.0, 1.0, 1.0), "OK", "hand calc: one-sided U, En 1"),
)
EN_CASES_WEAK = (Case((1.0, 0.5, 1.0, 0.5), "OK", "hand calc: identical values"),)


def _poisson(lam):
    return round(F.extinction_poisson(lam), 8)


def _p_mut(fn):
    return lambda lam: round(fn(lam), 8)


def _iter(f, s0=0.0):
    s = s0
    for _ in range(100000):
        t = f(s)
        if abs(t - s) <= 1e-15:
            return t
        s = t
    return s


POISSON_MUTANTS = {
    "start_at_one": _p_mut(lambda lam: 1.0 if lam <= 1 else _iter(lambda s: math.exp(lam * (s - 1)), 1.0)),
    "sign_flip": _p_mut(lambda lam: 1.0 if lam <= 1 else _iter(lambda s: math.exp(-lam * (1 - s) * 0.5))),
    "always_one": _p_mut(lambda lam: 1.0),
    "critical_strict": _p_mut(lambda lam: 1.0 if lam < 1 else _iter(lambda s: math.exp(lam * (s - 1)))),
}
POISSON_NULLS = {"tol_1e14": _p_mut(lambda lam: 1.0 if lam <= 1 else _iter(lambda s: math.exp(lam * (s - 1))))}
POISSON_CASES = (
    Case((0.5,), 1.0, "subcritical: q = 1 (Galton-Watson, recalled, VERIFY)"),
    Case((2.0,), 0.20318787, "q = e^{2(q-1)}, recalled value 0.2031878699 (VERIFY)"),
)


def _g(m, tol, sigma, k, floor):
    p = C.Prereg(accounts=[C.AccountDecl(account="N", tolerance=tol, sigma=sigma, k=k, basis="h")],
                 declared_complete=True, registry=("harness",), roundoff_floor=floor)
    o = C.Misclosure(account="N", value=m, provenance="harness")
    return C._label(C.verdict_branch_G(C.run(p, p.sha256, [o]), o))


def _g_mut(no_floor_tier=False, floor_out_of_u=False, unresolved_is_fail=False):
    def f(m, tol, sigma, k, floor):
        u = k * sigma + (0 if floor_out_of_u else floor)
        m = abs(m)
        if not no_floor_tier and m <= floor:
            return "PHYSICAL:OK"
        if m <= tol - u:
            return "PHYSICAL:CLOSED_WITHIN"
        if m > tol + u or unresolved_is_fail:
            return "PHYSICAL:FAILED"
        return "INSTRUMENT:UNRESOLVED"
    return f


G_MUTANTS = {"no_floor_tier": _g_mut(no_floor_tier=True), "floor_out_of_u": _g_mut(floor_out_of_u=True),
             "unresolved_is_fail": _g_mut(unresolved_is_fail=True)}
G_NULLS = {"reimplemented": _g_mut()}
# cases from samples/closure_branch_table.txt rows c1, c3, c9, c10, c11: computed BY G -> circular
G_TESTED = ("formula:verdict_branch_G",)
G_CASES = tuple(Case(inp, _g(*inp), "closure_branch_table, computed by formula:verdict_branch_G")
                for inp in ((1e-7, 1e-6, 1e-6, 3, 1e-12), (5e-6, 1e-6, 1e-6, 3, 1e-12),
                            (5e-6, 1e-5, 1e-7, 2, 1e-12), (0.0, 1e-5, 1e-7, 2, 1e-12),
                            (1.1e-5, 1e-5, 1e-7, 2, 1e-12)))

HARNESSES = (
    Harness("en_strong", ("formula:en_compare",), _en, EN_CASES_STRONG, EN_MUTANTS, EN_NULLS, (), ()),
    Harness("en_weak", ("formula:en_compare",), _en, EN_CASES_WEAK, EN_MUTANTS, EN_NULLS, (), ()),
    Harness("poisson", ("formula:extinction_poisson",), _poisson, POISSON_CASES, POISSON_MUTANTS,
            POISSON_NULLS, (), ()),
    Harness("g_table", G_TESTED, _g, G_CASES, G_MUTANTS, G_NULLS, (), ()),
    Harness("en_null_only", ("formula:en_compare",), _en, (), {}, EN_NULLS, (), ("hypot", "fabs")),
    Harness("en_plants_only", ("formula:en_compare",), _en, (), EN_MUTANTS, EN_NULLS,
            tuple(EN_MUTANTS), ()),
)


def get(name):
    return next(h for h in HARNESSES if h.name == name)


def _circular(case, tested):
    return any(t in case.provenance for t in tested)


def classify_source(h):
    counted = [c for c in h.cases if not _circular(c, h.tested)]
    if counted:
        return "KNOWN_ANSWER"
    if h.cases:
        return "CIRCULAR"
    if h.plants_signal:
        return "PLANTED_FAULT"
    if h.plants_null:
        return "NULL_ONLY"
    raise ValueError("harness %s carries no information source" % h.name)


# Evidence round (2026-11-18): cases added to close the gaps H-B measured. Base cases stay as they
# were so the before / after counts are both reported.
ADDED = {
    "en_strong": (Case((10.0, 0.3, 10.6, 0.4), "FAILED",
                       "hand calc: |d| 0.6; RSS U_c 0.5 -> En 1.2 FAILED; linear sum 0.7 -> 0.857 would pass"),),
    "poisson": (Case((1.0,), 1.0, "critical: q = 1 at lam = 1 (Galton-Watson, recalled, VERIFY)"),),
}


def _cases(h, base_only=False):
    return tuple(h.cases) + (() if base_only else ADDED.get(h.name, ()))


def failures(h, fn, base_only=False):
    return [c for c in _cases(h, base_only) if fn(*c.inputs) != c.expected]


def measure_power(h, base_only=False):
    n, nn = len(h.mutants), len(h.nulls)
    if not _cases(h, base_only):
        return {"n_faults": n, "caught": None, "catch": None, "catch_rate": None,
                "bin_catch": "NOT_MEASURABLE", "n_nulls": nn, "false_alarms": None,
                "bin_false_alarm": "NOT_MEASURABLE", "missed": ()}
    caught = [m for m, fn in h.mutants.items() if failures(h, fn, base_only)]
    fa = [m for m, fn in h.nulls.items() if failures(h, fn, base_only)]
    k = len(caught)
    return {"n_faults": n, "caught": k, "catch": (k, n), "catch_rate": k / n if n else None,
            "bin_catch": "CATCHES_ALL" if k == n else ("CATCHES_NONE" if k == 0 else "PARTIAL"),
            "n_nulls": nn, "false_alarms": len(fa), "bin_false_alarm": "QUIET" if not fa else "NOISY",
            "missed": tuple(sorted(set(h.mutants) - set(caught)))}


def table():
    rows = []
    for h in HARNESSES:
        a, b, b0 = classify_source(h), measure_power(h), measure_power(h, base_only=True)
        rows.append({"harness": h.name, "provenance": a, "power": b["bin_catch"], "H-A": a,
                     "H-B": b["bin_catch"], "catch": b["catch"], "catch_before": b0["catch"],
                     "power_before": b0["bin_catch"], "added": len(ADDED.get(h.name, ())),
                     "false_alarm": b["bin_false_alarm"], "missed": b["missed"],
                     "split": a == "KNOWN_ANSWER" and b["bin_catch"] != "CATCHES_ALL"})
    return rows


def render():
    f = lambda c: "--" if c is None else "%d/%d" % c
    out = ["DECIDED on evidence: provenance = H-A (a field), power = H-B (the rating)",
           "harness         provenance     power before    caught before  added  power after     caught after  false alarms  missed  SPLIT"]
    for r in table():
        out.append("%-15s %-14s %-15s %-14s %-6s %-15s %-13s %-13s %-7s %s" % (
            r["harness"], r["provenance"], r["power_before"], f(r["catch_before"]), r["added"], r["power"],
            f(r["catch"]), r["false_alarm"], ",".join(r["missed"]) or "--", "SPLIT" if r["split"] else ""))
    out.append("SPLIT (provenance KNOWN_ANSWER, power not CATCHES_ALL): "
               + (", ".join(r["harness"] for r in table() if r["split"]) or "none"))
    out.append("bins are measured counts, no threshold")
    return "\n".join(out)


if __name__ == "__main__":
    print(render())
