"""M6: trust keyed by (model, system scope, start state) (COMBINED_SPEC section 5; section 8
rows 12, 14).

Built: a bare model name is refused as a key; a lookup in a scope with no certification of its
own is UNTESTED; per-start-state records, with START_STATE_SENSITIVE and every arm listed when
the verdict varies (never a blanket UNTRUSTED); the harness class carried beside the INSTRUMENT
reading, never replacing it; one certification per key (a revision is not an overwrite).

Decided (9c item 6): a transfer argument passes only when every declared constraint is matched
and independence is checked (pins P6-ladder-cross-domain, P6-card-constraint-reasoning).
Held VOID: the harness-class vocabulary and its thresholds (#257 names them; the spec does not list them).
"""
from collections import namedtuple

from . import axes as A
from . import tokens as T


class TrustError(ValueError):
    pass


def _filled(x):
    return isinstance(x, str) and x.strip() != ""


class TrustKey(namedtuple("TrustKey", "model scope start_state")):
    __slots__ = ()

    def __new__(cls, model, scope, start_state):
        if not (_filled(model) and _filled(scope) and _filled(start_state)):
            raise TrustError("trust key is (model, system scope, start state); a bare name is refused")
        return super().__new__(cls, model, scope, start_state)


TrustRecord = namedtuple("TrustRecord", "key reading harness_class")


class TransferArgument(namedtuple("TransferArgument", "from_scope constraints independence_checked")):
    """9c item 6 (pins P6-ladder-cross-domain, P6-card-constraint-reasoning): every declared constraint
    matched and independence checked, else the transfer is refused."""
    __slots__ = ()

    def __new__(cls, *, from_scope, constraints, independence_checked):
        cons = tuple(constraints)
        if not _filled(from_scope) or not cons or not all(
                len(c) == 2 and _filled(c[0]) and isinstance(c[1], bool) for c in cons):
            raise TrustError("transfer argument: a source scope and >= 1 (name, matched bool) constraint")
        if not isinstance(independence_checked, bool):
            raise TrustError("independence_checked is an explicit bool")
        return super().__new__(cls, from_scope, cons, independence_checked)


TransferredTrust = namedtuple("TransferredTrust", "source key argument")


class Registry(object):
    def __init__(self):
        self._recs = {}

    def certify(self, key, reading, harness_class):
        if not isinstance(key, TrustKey):
            raise TrustError("certify takes a TrustKey")
        if not isinstance(reading, A.Reading) or reading.field != "INSTRUMENT":
            raise TrustError("trust is an INSTRUMENT reading (section 5)")
        if not _filled(harness_class):
            raise TrustError("harness class sits beside the axis reading (F3)")
        if key in self._recs:
            raise TrustError("key already certified; record a revision beside it, do not overwrite")
        self._recs[key] = TrustRecord(key, reading, harness_class)
        return self._recs[key]

    def lookup(self, model, scope, start_state, transfer_argument=None):
        key = TrustKey(model, scope, start_state)
        if key in self._recs:
            return self._recs[key]
        if transfer_argument is not None:
            if not isinstance(transfer_argument, TransferArgument):
                raise TrustError("a transfer argument is a TransferArgument: declared constraints, each "
                                 "matched or not, plus an independence check (9c item 6)")
            src = TrustKey(model, transfer_argument.from_scope, start_state)
            if src not in self._recs:
                return T.Token("UNTESTED", "transfer source %r has no certification at start state %r"
                               % (transfer_argument.from_scope, start_state))
            unmatched = [n for n, ok in transfer_argument.constraints if not ok]
            if unmatched or not transfer_argument.independence_checked:
                why = []
                if unmatched:
                    why.append("constraint not matched: " + "; ".join(unmatched))
                if not transfer_argument.independence_checked:
                    why.append("independence not checked")
                return T.Token("REFUSED", "transfer %r -> %r refused: %s (pin P6-ladder-cross-domain)"
                               % (transfer_argument.from_scope, scope, ", ".join(why)))
            return TransferredTrust(self._recs[src], key, transfer_argument)
        return T.Token("UNTESTED", "no certification in scope %r at start state %r" % (scope, start_state))

    def scope_summary(self, model, scope):
        arms = {k.start_state: r.reading.status for k, r in self._recs.items()
                if k.model == model and k.scope == scope}
        if not arms:
            return {"arms": {}, "flag": None,
                    "status": T.Token("UNTESTED", "no start state certified in scope %r" % scope)}
        flag = "START_STATE_SENSITIVE" if len(set(arms.values())) > 1 else None
        return {"arms": arms, "flag": flag, "status": T.Token("VOID", "per-arm; no aggregate rule")
                if flag else next(iter(arms.values()))}
