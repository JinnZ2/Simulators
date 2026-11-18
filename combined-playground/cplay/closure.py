"""M4: closure gate declarations (COMBINED_SPEC section 2 R-A1, R-A4; section 8 rows 4-7, 41).

Built: per-account tolerance declared before the run with no default; sigma and k passed
explicitly per account (None accepted as a passed value); the roundoff floor as its own field;
the ledger's declared-complete flag in three states; the intervention registry as a non-empty
list or a token; misclosure value provenance as a field; the pre-registration hashed before the
run; an undeclared account refusing the run.

SPEC GAP (stops this module at the verdict): section 2 names a tolerance, a sigma, a k and a
roundoff floor per account, and says NOISE is "misclosure within k sigma", but gives no rule
combining them into OK / CLOSED_WITHIN / FAILED, and does not state how a misclosure is
computed. verdict() raises SpecGap rather than choosing one.

Beside it (follow-up item 2), three candidate rules, none adopted. Each takes the misclosure as a
declared input that the run accepted; a FAILED reading lands on PHYSICAL only when the ledger is
DECLARED complete (R-A1), else on DETERMINATION:
  A  tolerance first   OK if |m| <= tol; CLOSED_WITHIN if |m| <= k*sigma; else FAILED
  B  floor added       OK if |m| <= tol + roundoff floor; CLOSED_WITHIN if |m| <= k*sigma;
                       else FAILED. A token floor (not a number) makes B VOID.
  C  band first        CLOSED_WITHIN if |m| <= k*sigma; OK if |m| <= tol; else FAILED
A missing sigma or k removes the band step.

Added (branch completion), none adopted:
  D  floor first       OK if |m| <= roundoff floor; CLOSED_WITHIN if |m| <= tol; else FAILED
  E  floor, then band  band = max(tol, k*sigma); OK if |m| <= floor; CLOSED_WITHIN if |m| <= band;
                       else FAILED
  F  legs              allowable = k*sigma*sqrt(n_legs), tol a hard cap: FAILED if |m| > tol or
                       |m| > allowable; else CLOSED_WITHIN with sigma*sqrt(n_legs). n_legs is a
                       declared call input; missing -> VOID. F as given states no OK condition, so
                       F returns no OK (reading taken here).
  G  guard band        U = k*sigma + roundoff floor. OK if |m| <= tol - U; FAILED if |m| > tol + U;
                       otherwise UNRESOLVED (inside the guard band), carried on INSTRUMENT, never
                       PHYSICAL. sigma or k missing -> VOID; a token floor -> VOID. When U >= tol
                       the acceptance zone is empty and OK is unreachable (reading taken here).
                       Source: "ISO 14253-1 / JCGM 106 decision rule, recalled, not re-read
                       (VERIFY)"; COMBINED_SPEC section 7 status NOT_CHECKED.
D and E need a numeric floor (a token floor -> VOID); a CLOSED_WITHIN with no declared sigma is
VOID, since Q2 makes sigma part of CLOSED_WITHIN. F needs sigma and k (missing -> VOID).

FAILED routing (all branches): PHYSICAL when the ledger is DECLARED complete, else DETERMINATION.
Source: COMBINED_SPEC section 2 mapping table, lines 62-65 ("closure fail, ledger declared
complete -> PHYSICAL : FAILED" / "ledger NOT declared complete -> DETERMINATION : FAILED"), and
R-A1, lines 82-84. branch_table() runs eight declared cases through all six and marks SPLIT where
they disagree.
"""
import hashlib
import json
from collections import namedtuple

from . import axes as A
from . import tokens as T


class ClosureError(ValueError):
    pass


class SpecGap(NotImplementedError):
    pass


class _Absent(object):
    def __repr__(self):
        return "ABSENT"


ABSENT = _Absent()   # R-A1: a ledger that never stated the flag


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _filled(x):
    return isinstance(x, str) and x.strip() != ""


class AccountDecl(namedtuple("AccountDecl", "account tolerance sigma k basis")):
    __slots__ = ()

    def __new__(cls, *, account, tolerance, sigma, k, basis):
        if not _filled(account):
            raise ClosureError("account name required")
        if not _num(tolerance) or tolerance < 0:
            raise ClosureError("tolerance for %r must be a number >= 0, declared (R-A4)" % (account,))
        for name, v in (("sigma", sigma), ("k", k)):
            if v is not None and (not _num(v) or v < 0):
                raise ClosureError("%s for %r must be a number >= 0 or None" % (name, account))
        if not _filled(basis):
            raise ClosureError("basis required for %r" % (account,))
        return super().__new__(cls, account, float(tolerance), sigma, k, basis)


class Prereg(object):
    def __init__(self, *, accounts, declared_complete, registry, roundoff_floor):
        names = [a.account for a in accounts]
        if not accounts or not all(isinstance(a, AccountDecl) for a in accounts):
            raise ClosureError("at least one AccountDecl required")
        if len(set(names)) != len(names):
            raise ClosureError("duplicate account declaration")
        if declared_complete is True:
            self.complete_state = "DECLARED"
        elif declared_complete is False:
            self.complete_state = "NOT_DECLARED"
        elif declared_complete is ABSENT:
            self.complete_state = "ABSENT"
        else:
            raise ClosureError("declared_complete must be True, False or ABSENT (R-A1)")
        if isinstance(registry, T.Token):
            if registry.is_verdict:
                raise ClosureError("an empty registry is a non-verdict token with a reason")
        elif isinstance(registry, (list, tuple)) and registry and all(_filled(r) for r in registry):
            registry = tuple(registry)
        else:
            raise ClosureError("registry: non-empty list of entries, or a token (section 8 row 4)")
        if not (_num(roundoff_floor) and roundoff_floor >= 0) and not isinstance(roundoff_floor, T.Token):
            raise ClosureError("roundoff floor: a number >= 0 or a token, recorded on its own")
        self.accounts = {a.account: a for a in accounts}
        self.registry = registry
        self.roundoff_floor = roundoff_floor

    @property
    def counts_as_declared(self):
        return self.complete_state == "DECLARED"   # R-A1: ABSENT counts as not declared

    def _canon(self):
        reg = (["TOKEN", self.registry.state, self.registry.reason]
               if isinstance(self.registry, T.Token) else list(self.registry))
        rf = (["TOKEN", self.roundoff_floor.state, self.roundoff_floor.reason]
              if isinstance(self.roundoff_floor, T.Token) else self.roundoff_floor)
        return {"accounts": [list(self.accounts[n]) for n in sorted(self.accounts)],
                "complete": self.complete_state, "registry": reg, "roundoff_floor": rf}

    @property
    def sha256(self):
        blob = json.dumps(self._canon(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


class Misclosure(namedtuple("Misclosure", "account value provenance")):
    __slots__ = ()

    def __new__(cls, *, account, value, provenance):
        if not _filled(account) or not _num(value) or not _filled(provenance):
            raise ClosureError("misclosure needs account, numeric value and provenance (row 6)")
        return super().__new__(cls, account, value, provenance)


RunResult = namedtuple("RunResult", "state reason prereg_sha256 roundoff_floor observations prereg")


def run(prereg, prereg_sha256, observations):
    if prereg_sha256 != prereg.sha256:
        raise ClosureError("run must cite the hash taken before the run (row 41)")
    missing = sorted({o.account for o in observations} - set(prereg.accounts))
    if missing:
        return RunResult("REFUSED", "no declared tolerance for: %s (R-A4)" % ", ".join(missing),
                         prereg_sha256, prereg.roundoff_floor, tuple(observations), prereg)
    return RunResult("ACCEPTED", None, prereg_sha256, prereg.roundoff_floor, tuple(observations), prereg)


def verdict(result, account):
    raise SpecGap("section 2: no rule combines tolerance, k*sigma and the roundoff floor into "
                  "OK / CLOSED_WITHIN / FAILED, and the misclosure formula is not stated")


def _accepted(result, misclosure):
    if result.state != "ACCEPTED":
        raise ClosureError("no branch verdict on a %s run" % result.state)
    if not isinstance(misclosure, Misclosure) or misclosure not in result.observations:
        raise ClosureError("misclosure must be declared input, one the run accepted")
    decl = result.prereg.accounts[misclosure.account]
    band = decl.k * decl.sigma if decl.sigma is not None and decl.k is not None else None
    return decl, abs(misclosure.value), band


def _failed(result, decl, m):
    field = "PHYSICAL" if result.prereg.counts_as_declared else "DETERMINATION"
    return A.reading(field, "FAILED", reason="|m| = %g beyond tolerance %g (account %s)"
                     % (m, decl.tolerance, decl.account))


def _closed(decl, m, band, sigma=None, what="k*sigma"):
    sigma = decl.sigma if sigma is None else sigma
    if sigma is None:
        return T.Token("VOID", "CLOSED_WITHIN needs a declared sigma (Q2); account %s has none"
                       % decl.account)
    return A.reading("PHYSICAL", "CLOSED_WITHIN", reason="|m| = %g <= %s = %g" % (m, what, band),
                     sigma=sigma, basis=decl.basis)


def _floor(result, branch):
    floor = result.prereg.roundoff_floor
    if isinstance(floor, T.Token):
        return None, T.Token("VOID", "branch %s reads the roundoff floor; the floor is a token, "
                                     "not a number" % branch)
    return floor, None


def verdict_branch_A(result, misclosure=None):
    decl, m, band = _accepted(result, misclosure)
    if m <= decl.tolerance:
        return A.reading("PHYSICAL", "OK")
    if band is not None and m <= band:
        return _closed(decl, m, band)
    return _failed(result, decl, m)


def verdict_branch_B(result, misclosure=None):
    decl, m, band = _accepted(result, misclosure)
    floor = result.prereg.roundoff_floor
    if isinstance(floor, T.Token):
        return T.Token("VOID", "branch B adds the roundoff floor; the floor is a token, not a number")
    if m <= decl.tolerance + floor:
        return A.reading("PHYSICAL", "OK")
    if band is not None and m <= band:
        return _closed(decl, m, band)
    return _failed(result, decl, m)


def verdict_branch_C(result, misclosure=None):
    decl, m, band = _accepted(result, misclosure)
    if band is not None and m <= band:
        return _closed(decl, m, band)
    if m <= decl.tolerance:
        return A.reading("PHYSICAL", "OK")
    return _failed(result, decl, m)


def verdict_branch_D(result, misclosure=None):
    decl, m, _ = _accepted(result, misclosure)
    floor, void = _floor(result, "D")
    if void is not None:
        return void
    if m <= floor:
        return A.reading("PHYSICAL", "OK")
    if m <= decl.tolerance:
        return _closed(decl, m, decl.tolerance, what="tol")
    return _failed(result, decl, m)


def verdict_branch_E(result, misclosure=None):
    decl, m, band = _accepted(result, misclosure)
    floor, void = _floor(result, "E")
    if void is not None:
        return void
    wide = decl.tolerance if band is None else max(decl.tolerance, band)
    if m <= floor:
        return A.reading("PHYSICAL", "OK")
    if m <= wide:
        return _closed(decl, m, wide, what="max(tol, k*sigma)")
    return _failed(result, decl, m)


def verdict_branch_F(result, misclosure=None, n_legs=None):
    decl, m, _ = _accepted(result, misclosure)
    if isinstance(n_legs, bool) or not isinstance(n_legs, int) or n_legs < 1:
        return T.Token("VOID", "branch F needs n_legs as a declared integer >= 1; got %r" % (n_legs,))
    if decl.sigma is None or decl.k is None:
        return T.Token("VOID", "branch F needs sigma and k declared for account %s" % decl.account)
    s_legs = decl.sigma * n_legs ** 0.5
    allowable = decl.k * s_legs
    if m > decl.tolerance or m > allowable:
        return _failed(result, decl, m)
    return _closed(decl, m, allowable, sigma=s_legs, what="k*sigma*sqrt(%d)" % n_legs)


G_SOURCE = "ISO 14253-1 / JCGM 106 decision rule, recalled, not re-read (VERIFY)"
G_SOURCE_STATUS = "NOT_CHECKED"


class FieldToken(namedtuple("FieldToken", "field token")):
    """A non-axis state carried on a named failure axis (branch G's UNRESOLVED)."""
    __slots__ = ()

    def __new__(cls, field, token):
        if field != "INSTRUMENT":
            raise ClosureError("UNRESOLVED is carried on INSTRUMENT, never %s" % field)
        if not isinstance(token, T.Token) or token.state != "UNRESOLVED":
            raise ClosureError("FieldToken carries an UNRESOLVED token")
        return super().__new__(cls, field, token)


def verdict_branch_G(result, misclosure=None):
    decl, m, band = _accepted(result, misclosure)
    if band is None:
        return T.Token("VOID", "branch G needs sigma and k declared for account %s" % decl.account)
    floor, void = _floor(result, "G")
    if void is not None:
        return void
    u = band + floor
    if m <= decl.tolerance - u:
        return A.reading("PHYSICAL", "OK")
    if m > decl.tolerance + u:
        return _failed(result, decl, m)
    return FieldToken("INSTRUMENT", T.Token(
        "UNRESOLVED", "|m| = %g within guard band tol +/- U = %g +/- %g (source %s: %s)"
        % (m, decl.tolerance, u, G_SOURCE_STATUS, G_SOURCE)))


BRANCHES = {"A": verdict_branch_A, "B": verdict_branch_B, "C": verdict_branch_C,
            "D": verdict_branch_D, "E": verdict_branch_E, "F": verdict_branch_F,
            "G": verdict_branch_G}
N_LEGS = 4    # declared for every constructed case, so F's VOIDs come from sigma / k, not legs

# case: (misclosure, tolerance, sigma, k, roundoff floor, declared_complete) -- constructed
CASES = (
    ("c1", 1e-7, 1e-6, 1e-6, 3, 1e-12, True),
    ("c2", 2e-6, 1e-6, 1e-6, 3, 1e-12, True),
    ("c3", 5e-6, 1e-6, 1e-6, 3, 1e-12, True),
    ("c4", 1.0000005e-6, 1e-6, None, None, 1e-9, True),
    ("c5", 5e-7, 1e-6, None, None, 1e-12, True),
    ("c6", 5e-7, 1e-6, None, None, "TOKEN", True),
    ("c7", 2e-6, 1e-6, None, None, 1e-12, True),
    ("c8", 5e-6, 1e-6, 1e-6, 3, 1e-12, "ABSENT"),
)


def _label(r):
    if isinstance(r, FieldToken):
        return "%s:%s" % (r.field, r.token.state)
    if isinstance(r, T.Token):
        return r.state
    return "%s:%s" % (r.field, r.status)


def branch_table():
    rows = []
    for cid, m, tol, sigma, k, floor, complete in CASES:
        fl = T.Token("UNTESTED", "floor not measured") if floor == "TOKEN" else floor
        dc = ABSENT if complete == "ABSENT" else complete
        p = Prereg(accounts=[AccountDecl(account="N", tolerance=tol, sigma=sigma, k=k, basis="declared")],
                   declared_complete=dc, registry=("constructed case",), roundoff_floor=fl)
        obs = Misclosure(account="N", value=m, provenance="declared case %s" % cid)
        res = run(p, p.sha256, [obs])
        got = {b: _label(fn(res, obs, n_legs=N_LEGS) if b == "F" else fn(res, obs))
               for b, fn in BRANCHES.items()}
        abc = {got[b] for b in "ABC"}
        live = {v for v in got.values() if v != "VOID"}
        a_f = {got[b] for b in "ABCDEF"}
        rows.append({"case": cid, "m": m, "tol": tol, "sigma": sigma, "k": k, "floor": floor,
                     "complete": complete, "branches": got, "split": len(set(got.values())) > 1,
                     "split_abc": len(abc) > 1, "split_live": len(live) > 1,
                     "split_af": len(a_f) > 1, "g_differs": got["G"] not in a_f})
    return rows


def render_table(rows=None):
    rows = rows or branch_table()
    short = {"PHYSICAL:OK": "P:OK", "PHYSICAL:CLOSED_WITHIN": "P:CW", "PHYSICAL:FAILED": "P:FAIL",
             "DETERMINATION:FAILED": "D:FAIL", "VOID": "VOID", "INSTRUMENT:UNRESOLVED": "I:UNRES"}
    out = ["P = PHYSICAL, D = DETERMINATION, I = INSTRUMENT, CW = CLOSED_WITHIN; n_legs = %d for F" % N_LEGS,
           "G source: %s [%s]" % (G_SOURCE, G_SOURCE_STATUS),
           "case  |m|           tol    k*sigma  floor   complete  A       B       C       D       E       F       G        split  G-differs"]
    for r in rows:
        band = "--" if r["sigma"] is None else "%g" % (r["k"] * r["sigma"])
        cells = " ".join("%-7s" % short.get(r["branches"][b], r["branches"][b]) for b in "ABCDEFG")
        out.append("%-5s %-13.8g %-6g %-8s %-7s %-9s %s  %-6s %s" % (
            r["case"], r["m"], r["tol"], band, r["floor"], r["complete"], cells,
            "SPLIT" if r["split"] else "", "G" if r["g_differs"] else ""))
    out.append("SPLIT (A-G): " + ", ".join(r["case"] for r in rows if r["split"]))
    out.append("G differs from every A-F cell: " + ", ".join(r["case"] for r in rows if r["g_differs"]))
    out.append("SPLIT (A-F, as before): " + ", ".join(r["case"] for r in rows if r["split_af"]))
    out.append("SPLIT (A-G) on non-VOID cells only: " + ", ".join(r["case"] for r in rows if r["split_live"]))
    out.append("SPLIT (A-C only, as before): " + ", ".join(r["case"] for r in rows if r["split_abc"]))
    return "\n".join(out)

if __name__ == "__main__":
    print(render_table())
