"""M1. Input-brief record per builder (COMBINED_SPEC section 7). CC0 1.0 Universal.

Each build files what it was given, verbatim or by sha256. A build with no brief
reads BRIEF_UNRECORDED. A coincidence card's shared-source cause is read from the
briefs level by level (concept / naming / split), never wholesale.

Reading (not in the spec, stated here): the per-level states CUE_IN_BOTH /
CUE_IN_ONE / CUE_IN_NEITHER / CUE_UNSEARCHABLE are this module's tokens. A cue is
a literal substring searched in each brief's verbatim items; a hash-only item
cannot be searched and makes the level CUE_UNSEARCHABLE, never "absent".
"""
import collections, hashlib, re

BRIEF_UNRECORDED = "BRIEF_UNRECORDED"
RECORDED = "RECORDED"
CUE_IN_BOTH = "CUE_IN_BOTH"            # possible shared cue at this level
CUE_IN_ONE = "CUE_IN_ONE"              # cue reached one builder only: candidate independent convergence
CUE_IN_NEITHER = "CUE_IN_NEITHER"
CUE_UNSEARCHABLE = "CUE_UNSEARCHABLE"  # a brief holds hash-only items
STATES = (BRIEF_UNRECORDED, RECORDED, CUE_IN_BOTH, CUE_IN_ONE, CUE_IN_NEITHER, CUE_UNSEARCHABLE)

Reading = collections.namedtuple("Reading", "state reason")
_HEX = re.compile(r"^[0-9a-f]{64}$")


class BriefError(ValueError):
    pass


class Item(object):
    def __init__(self, name, verbatim=None, sha256=None):
        if not name:
            raise BriefError("item needs a name")
        if verbatim is None and sha256 is None:
            raise BriefError("item %r: verbatim text or sha256 required" % name)
        if verbatim is not None:
            h = hashlib.sha256(verbatim.encode("utf-8")).hexdigest()
            if sha256 is not None and sha256 != h:
                raise BriefError("item %r: sha256 does not match the verbatim text" % name)
            sha256 = h
        if not _HEX.match(sha256):
            raise BriefError("item %r: sha256 must be 64 lowercase hex characters" % name)
        self.name, self.verbatim, self.sha256 = name, verbatim, sha256


class InputBrief(object):
    def __init__(self, builder, recorded_at, items):
        if not builder:
            raise BriefError("brief needs the builder")
        if not recorded_at:
            raise BriefError("brief needs recorded_at (when it was filed)")
        items = tuple(items)
        if not items:
            raise BriefError("brief needs at least one item; a builder given nothing files that as an item")
        self.builder, self.recorded_at, self.items = builder, recorded_at, items

    def searchable(self):
        return all(i.verbatim is not None for i in self.items)

    def contains(self, cue):
        return any(cue in i.verbatim for i in self.items if i.verbatim is not None)


def brief_state(brief):
    if brief is None:
        return Reading(BRIEF_UNRECORDED, "no input brief was filed at build time")
    return Reading(RECORDED, "%s, recorded %s, %d item(s)" % (brief.builder, brief.recorded_at, len(brief.items)))


def shared_source(cues, a, b):
    """cues: {level: literal cue}. Returns {level: Reading}, one per level."""
    out = {}
    for level, cue in cues.items():
        if a is None or b is None:
            who = [x for x, br in (("first", a), ("second", b)) if br is None]
            out[level] = Reading(BRIEF_UNRECORDED, "%s builder's brief not filed; level %r cannot be read" % (" and ".join(who), level))
            continue
        hits = [br.builder for br in (a, b) if br.contains(cue)]
        blind = [br.builder for br in (a, b) if not br.searchable() and br.builder not in hits]
        if blind:
            out[level] = Reading(CUE_UNSEARCHABLE, "brief of %s holds hash-only items; %r not searchable there" % (", ".join(blind), cue))
        elif len(hits) == 2:
            out[level] = Reading(CUE_IN_BOTH, "%r in both briefs: possible shared cue" % cue)
        elif len(hits) == 1:
            out[level] = Reading(CUE_IN_ONE, "%r only in %s's brief: candidate independent convergence" % (cue, hits[0]))
        else:
            out[level] = Reading(CUE_IN_NEITHER, "%r in neither brief" % cue)
    return out
