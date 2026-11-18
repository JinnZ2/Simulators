"""M5: gate order -- identity, observer regime, comparison, card (COMBINED_SPEC section 3;
section 8 rows 29-33).

Built: the order is enforced by a state machine; identity failure records NOT_COMPARABLE and no
card opens; each system declares one of four regimes with a reason, never merged, PASSIVE
labelled as the chat-side addition; an undeclared regime refuses the comparison; the card opens
only after the comparison and reads shared source from the M1 input briefs; rank() raises.

Held VOID (the spec does not define them):
  - the measurand identity criterion: the caller supplies the verdict and its reason
  - what a comparison computes: the caller supplies its result as a token
  - the effect of two systems declaring different regimes
  (decided, 9c item 5: card causes are the independence list INDEPENDENCE_CAUSES)
"""
from collections import namedtuple

from . import brief as B
from . import tokens as T

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

    def regime(self, decl_a, decl_b):
        self._step("regime")
        for sys_name, d in zip(self.systems, (decl_a, decl_b)):
            if d is not None and d.system != sys_name:
                raise GateError("declaration for %r names %r" % (sys_name, d.system))
        undeclared = [s for s, d in zip(self.systems, (decl_a, decl_b)) if d is None]
        if undeclared:
            self.outcome = T.Token("REFUSED", "regime UNDECLARED for: %s (Q9)" % ", ".join(undeclared))
            return self.outcome
        self.regimes = (decl_a, decl_b)
        return None

    def compare(self, result):
        if not isinstance(result, T.Token):
            raise GateError("comparison result is a token; what a comparison computes is VOID here")
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
            "regime_mismatch_effect": T.Token("VOID", "section 3 does not say what differing regimes do"),
            "other_causes": {c: causes[c] if c in causes else T.Token("UNDECLARED", "cause %r not declared for this card" % c)
                             for c in INDEPENDENCE_CAUSES[1:]},
        }


def rank(items):
    raise GateError("no universal ranking (section 8 row 33)")
