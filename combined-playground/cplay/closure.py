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
"""
import hashlib
import json
from collections import namedtuple

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
