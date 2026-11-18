"""M8: continuity (COMBINED_SPEC section 8 rows 21-26, Q7).

Built: a frozen anchor; return_to_anchor with a tolerance declared per variable, returning the
verdict and the deltas together (row 23); identity_check and return_to_anchor as two fields with
no composite, both kept when they disagree (Q7 "branch rule: keep both"); a one-change branch,
two changes refused with both named (row 24); reevaluation keeping the original (row 21); two
state tracks with crossing refused (row 26).

Readings taken here, stated: return passes iff every |delta| <= its declared tolerance; a
variable in the tolerance but absent from the observation makes the test UNTESTED, not OK.
Held VOID: the identity criterion (identity_check is a caller-supplied token).
"""
from collections import namedtuple
from types import MappingProxyType

from . import tokens as T


class ContinuityError(ValueError):
    pass


def _filled(x):
    return isinstance(x, str) and x.strip() != ""


class Anchor(object):
    def __init__(self, anchor_id, values):
        if not _filled(anchor_id) or not values:
            raise ContinuityError("anchor needs an id and values")
        self.anchor_id = anchor_id
        self.values = MappingProxyType(dict(values))


class ReturnResult(namedtuple("ReturnResult", "state reason deltas tolerance anchor_id")):
    __slots__ = ()
    is_verdict = property(lambda self: self.state == "OK")


def return_to_anchor(anchor, observed, *, tolerance):
    missing_tol = sorted(set(anchor.values) - set(tolerance))
    if missing_tol:
        raise ContinuityError("no declared tolerance for: %s" % ", ".join(missing_tol))
    absent = sorted(v for v in tolerance if v not in observed)
    deltas = {v: observed[v] - anchor.values[v] for v in tolerance if v in observed}
    if absent:
        return ReturnResult("UNTESTED", "not observed: %s" % ", ".join(absent), deltas,
                            dict(tolerance), anchor.anchor_id)
    out = sorted(v for v, d in deltas.items() if abs(d) > tolerance[v])
    if out:
        return ReturnResult("FAILED", "outside tolerance: %s" % ", ".join(out), deltas,
                            dict(tolerance), anchor.anchor_id)
    return ReturnResult("OK", None, deltas, dict(tolerance), anchor.anchor_id)


class Continuity(object):
    __slots__ = ("identity_check", "return_to_anchor")

    def __init__(self, *, identity_check, return_to_anchor):
        if not isinstance(identity_check, T.Token):
            raise ContinuityError("identity_check is a token; its criterion is VOID here")
        if not isinstance(return_to_anchor, ReturnResult):
            raise ContinuityError("return_to_anchor is a ReturnResult")
        self.identity_check = identity_check
        self.return_to_anchor = return_to_anchor

    @property
    def disagree(self):
        return self.identity_check.is_verdict != self.return_to_anchor.is_verdict

    def composite(self):
        raise ContinuityError("no composite of identity_check and return_to_anchor (Q7)")


def branch(parent, child):
    if set(parent) != set(child):
        raise ContinuityError("branch changes values, not the parameter set: %s"
                              % ", ".join(sorted(set(parent) ^ set(child))))
    changed = tuple(sorted(k for k in parent if parent[k] != child[k]))
    if len(changed) != 1:
        raise ContinuityError("a branch is one change; got %d: %s" % (len(changed), ", ".join(changed)))
    return changed


Revision = namedtuple("Revision", "original revised reason")


def reevaluate(original, revised, reason):
    if not _filled(reason):
        raise ContinuityError("a revision states its reason")
    return Revision(original, revised, reason)


class Tracks(object):
    def __init__(self, names):
        if len(names) != 2 or len(set(names)) != 2:
            raise ContinuityError("two named state tracks")
        self._t = {n: [] for n in names}

    def append(self, track, state, source_track=None):
        if track not in self._t:
            raise ContinuityError("unknown track %r" % (track,))
        if source_track is not None and source_track != track:
            raise ContinuityError("state from track %r may not cross into %r" % (source_track, track))
        self._t[track].append(state)
