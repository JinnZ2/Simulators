"""M6: trust keyed by (model, system scope, start state) (COMBINED_SPEC section 5; section 8
rows 12, 14).

Built: a bare model name is refused as a key; a lookup in a scope with no certification of its
own is UNTESTED; per-start-state records, with START_STATE_SENSITIVE and every arm listed when
the verdict varies (never a blanket UNTRUSTED); the harness class carried beside the INSTRUMENT
reading, never replacing it; one certification per key (a revision is not an overwrite).

Held VOID: how the gate tests a declared transfer argument (section 5 says it does, not how);
the harness-class vocabulary and its thresholds (#257 names them; the spec does not list them).
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
        if _filled(transfer_argument):
            return T.Token("VOID", "transfer argument declared (%s); section 5 does not say how the "
                                   "gate tests it" % transfer_argument)
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
