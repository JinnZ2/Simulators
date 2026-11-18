"""M5: gate order -- identity, observer regime, comparison, card (COMBINED_SPEC section 3;
section 8 rows 29-33).

Built: the order is enforced by a state machine; identity failure records NOT_COMPARABLE and no
card opens; each system declares one of four regimes with a reason, never merged, PASSIVE
labelled as the chat-side addition; an undeclared regime refuses the comparison; the card opens
only after the comparison and reads shared source from the M1 input briefs; rank() raises.

Decided in 9c (sources NOT_CHECKED where marked):
  item 2  measurand identity: same kind of quantity + same specification of conditions
          (Measurand, measurand_identity, Chain.identity_of; VIM, IDENTITY_SOURCE)
  item 3  comparison: difference with combined uncertainty, En = |x1-x2|/sqrt(U1^2+U2^2),
          En <= 1 agree (en_compare, Chain.compare_values; EA-4/02, EN_SOURCE)
  item 4  differing regimes: REFUSED with both named unless a TransferArgument passes (item 6)
  item 5  card causes are the independence list INDEPENDENCE_CAUSES
Chain.identity(bool, reason) and Chain.compare(token) remain for caller-decided steps.
"""
import math
from collections import namedtuple

from . import brief as B
from . import tokens as T
from . import trust as R

IDENTITY_SOURCE = ("JCGM 200:2012 (VIM) 2.3 measurand = 'quantity intended to be measured'; identity = "
                   "same kind of quantity + same specification of conditions. NOT_CHECKED (VERIFY): "
                   "recalled, not read by this session")
EN_SOURCE = ("EA-4/02: En = |x1 - x2| / sqrt(U1^2 + U2^2), En <= 1 agree (expanded U). NOT_CHECKED "
             "(VERIFY): recalled, not read by this session; ISO 13528 paywalled")

# 9c item 5: the independence list (formula-audit branch 5 shared_ancestry, pin P5-ladder-shared-ancestry).
# shared_source is read from the M1 briefs; the other five are declared per card or read UNDECLARED.
INDEPENDENCE_CAUSES = ("shared_source", "method", "model", "training_data", "code", "axioms")

REGIMES = ("PASSIVE", "PERTURBATION", "REACTIVITY", "STRATEGY")
REGIME_SOURCE = {
    "PASSIVE": "chat-side addition, LABELED as such: null control, not disturbed and not reacting",
    "PERTURBATION": "Kimi audit section 4.4, regime 1: the instrument physically disturbs the system",
    "REACTIVITY": "Kimi audit section 4.4, regime 2: behaviour changes under observation",
    "STRATEGY": "Kimi audit section 4.4, regime 3: the system models the evaluation itself",
}


class GateError(ValueError):
    pass


def _filled(x):
    return isinstance(x, str) and x.strip() != ""


class RegimeDecl(namedtuple("RegimeDecl", "system regime reason")):
    __slots__ = ()

    def __new__(cls, system, regime, reason):
        if not _filled(system):
            raise GateError("regime declaration names its system")
        if regime not in REGIMES:
            raise GateError("regime %r not one of %r; regimes are not merged" % (regime, REGIMES))
        if not _filled(reason):
            raise GateError("regime declaration needs a reason")
        return super().__new__(cls, system, regime, reason)


class Measurand(object):
    """9c item 2: a kind of quantity plus its specification of conditions (VIM, NOT_CHECKED)."""
    def __init__(self, *, kind, conditions):
        if not _filled(kind):
            raise GateError("a measurand names its kind of quantity")
        if not isinstance(conditions, dict):
            raise GateError("conditions are a mapping (specification of conditions)")
        self.kind = kind
        self.conditions = dict(conditions)


def measurand_identity(a, b):
    if a.kind != b.kind:
        return False, "kind of quantity differs: %r vs %r" % (a.kind, b.kind)
    keys = sorted(set(a.conditions) | set(b.conditions))
    diff = [k for k in keys if a.conditions.get(k, _MISSING) != b.conditions.get(k, _MISSING)]
    if diff:
        return False, "specification of conditions differs on: %s" % ", ".join(
            "%s (%r vs %r)" % (k, a.conditions.get(k, "absent"), b.conditions.get(k, "absent")) for k in diff)
    return True, "same kind (%s) and same specification of conditions" % a.kind


_MISSING = object()


class Comparison(object):
    __slots__ = ("difference", "u_combined", "en", "token")

    def __init__(self, difference, u_combined, en, token):
        self.difference, self.u_combined, self.en, self.token = difference, u_combined, en, token


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def en_compare(x1, U1, x2, U2):
    """9c item 3: difference with combined expanded uncertainty; En <= 1 agree (EA-4/02, NOT_CHECKED)."""
    if not all(_num(v) for v in (x1, U1, x2, U2)) or U1 < 0 or U2 < 0:
        raise GateError("en_compare takes numeric values and expanded uncertainties >= 0")
    d = x1 - x2
    uc = math.sqrt(U1 * U1 + U2 * U2)
    if uc == 0:
        return Comparison(d, 0.0, None, T.Token("VOID", "combined uncertainty is 0; En undefined"))
    en = abs(d) / uc
    tok = T.Token("OK") if en <= 1 else T.Token("FAILED", "En = %g > 1 (|d| = %g, U_c = %g)" % (en, abs(d), uc))
    return Comparison(d, uc, en, tok)


_ORDER = ("identity", "regime", "compare", "card")


class Chain(object):
    def __init__(self, value_a, value_b, *, system_a, system_b):
        if not (_filled(system_a) and _filled(system_b)):
            raise GateError("both systems are named")
        self.values = (value_a, value_b)
        self.systems = (system_a, system_b)
        self.done = []
        self.outcome = None      # a Token once a step stops the chain
        self.regimes = None
        self.comparison = None
        self.comparison_detail = None
        self.regime_transfer = None

    def _step(self, name):
        if self.outcome is not None and not self.outcome.is_verdict:
            raise GateError("chain stopped at %s: %s" % (self.done[-1], self.outcome.state))
        want = _ORDER[len(self.done)] if len(self.done) < len(_ORDER) else None
        if name != want:
            raise GateError("gate %r out of order; next is %r (section 3)" % (name, want))
        self.done.append(name)

    def identity(self, passed, reason):
        if not isinstance(passed, bool) or not _filled(reason):
            raise GateError("identity takes a bool verdict and a reason")
        self._step("identity")
        if not passed:
            self.outcome = T.Token("NOT_COMPARABLE", reason)
        return self.outcome

    def identity_of(self, ma, mb):
        ok, why = measurand_identity(ma, mb)
        return self.identity(ok, why)

    def regime(self, decl_a, decl_b, transfer_argument=None):
        if transfer_argument is not None and not isinstance(transfer_argument, R.TransferArgument):
            raise GateError("a regime transfer argument is a TransferArgument (9c items 4, 6)")
        self._step("regime")
        for sys_name, d in zip(self.systems, (decl_a, decl_b)):
            if d is not None and d.system != sys_name:
                raise GateError("declaration for %r names %r" % (sys_name, d.system))
        undeclared = [s for s, d in zip(self.systems, (decl_a, decl_b)) if d is None]
        if undeclared:
            self.outcome = T.Token("REFUSED", "regime UNDECLARED for: %s (Q9)" % ", ".join(undeclared))
            return self.outcome
        if decl_a.regime != decl_b.regime:
            arg = transfer_argument
            unmatched = [n for n, ok in arg.constraints if not ok] if arg else []
            if arg is None or unmatched or not arg.independence_checked:
                why = ("no transfer argument" if arg is None else
                       "; ".join((["constraint not matched: " + ", ".join(unmatched)] if unmatched else [])
                                 + ([] if arg.independence_checked else ["independence not checked"])))
                self.outcome = T.Token("REFUSED", "regimes differ: %s %s vs %s %s; %s (9c item 4)"
                                       % (self.systems[0], decl_a.regime, self.systems[1], decl_b.regime, why))
                return self.outcome
            self.regime_transfer = arg
        self.regimes = (decl_a, decl_b)
        return None

    def compare_values(self, x1, U1, x2, U2):
        c = en_compare(x1, U1, x2, U2)
        self.compare(c.token)
        self.comparison_detail = c
        return c

    def compare(self, result):
        if not isinstance(result, T.Token):
            raise GateError("comparison result is a token; compare_values() computes En (9c item 3)")
        self._step("compare")
        self.comparison = result
        return result

    def open_card(self, brief_a, brief_b, cues, causes=None):
        causes = dict(causes or {})
        bad = sorted(set(causes) - set(INDEPENDENCE_CAUSES[1:]))
        if bad:
            raise GateError("unknown card cause(s) %s; the list is %r" % (", ".join(bad), INDEPENDENCE_CAUSES))
        for c, v in causes.items():
            if not isinstance(v, T.Token):
                raise GateError("card cause %r is a token, not %r" % (c, v))
        self._step("card")
        return {
            "systems": self.systems,
            "regimes": tuple(d.regime for d in self.regimes),
            "comparison": self.comparison,
            "shared_source_by_level": B.shared_source(cues, brief_a, brief_b),
            "regime_mismatch_effect": (T.Token("OK") if self.regime_transfer is None else
                                       T.Token("INDETERMINATE", "regimes differ; compared under a passed "
                                               "transfer argument from %r" % self.regime_transfer.from_scope)),
            "other_causes": {c: causes[c] if c in causes else T.Token("UNDECLARED", "cause %r not declared for this card" % c)
                             for c in INDEPENDENCE_CAUSES[1:]},
        }


def rank(items):
    raise GateError("no universal ranking (section 8 row 33)")
