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
A missing sigma or k removes the band step. branch_table() runs eight declared cases through
all three and marks SPLIT where they disagree.
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


def _closed(decl, m, band):
    return A.reading("PHYSICAL", "CLOSED_WITHIN", reason="|m| = %g <= k*sigma = %g" % (m, band),
                     sigma=decl.sigma, basis=decl.basis)


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


BRANCHES = {"A": verdict_branch_A, "B": verdict_branch_B, "C": verdict_branch_C}

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
        got = {b: _label(fn(res, obs)) for b, fn in BRANCHES.items()}
        rows.append({"case": cid, "m": m, "tol": tol, "sigma": sigma, "k": k, "floor": floor,
                     "complete": complete, "branches": got, "split": len(set(got.values())) > 1})
    return rows


def render_table(rows=None):
    rows = rows or branch_table()
    out = ["case  |m|          tol    k*sigma  floor   complete  A                       B                       C                       split"]
    for r in rows:
        band = "--" if r["sigma"] is None else "%g" % (r["k"] * r["sigma"])
        b = r["branches"]
        out.append("%-5s %-12.8g %-6g %-8s %-7s %-9s %-23s %-23s %-23s %s" % (
            r["case"], r["m"], r["tol"], band, r["floor"], r["complete"], b["A"], b["B"], b["C"],
            "SPLIT" if r["split"] else ""))
    return "\n".join(out)


if __name__ == "__main__":
    print(render_table())
