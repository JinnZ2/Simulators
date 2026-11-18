"""M2. State tokens, typed expiry, scoped absence, claims (COMBINED_SPEC section 4). CC0 1.0 Universal.

Rules:
  - one distinct token per state; none ever reads as 0, OK or "no row" (no numeric or
    truth value: float() and bool() raise)
  - a reason is required on every token that is not a verdict (VERDICTS = {OK})
  - UNKNOWN requires at least one TYPED expiry trigger; free text is UNTYPED and is not
    an exit (Q4)
  - ABSENT_AT_SENSITIVITY carries limit + basis (LADDER with a ladder ref, or DECLARED),
    effect size of interest, and conditions, or it is refused (F7)
  - claim tag and claim record are two objects linked 1:1 (Q8); untagged claims refused

VOID in the spec, so VOID here (never a default):
  - the ExpiryTrigger `kind` vocabulary: the spec requires typed triggers and lists no kinds
  - the ConditionBasis <-> #257 STATUSES mapping table (Q12 keeps the two vocabularies and
    asks for a table; the table's rows are not in the spec)
Reading added here: `covers_effect` (limit <= effect size) is reported on a scoped
absence. It refuses nothing; the spec requires the fields, not the comparison.
"""

VERDICTS = ("OK",)
STATES = (
    "OK", "FAILED", "INDETERMINATE", "UNTESTED", "CRASHED", "CLOSED_WITHIN", "OUTSIDE_DOMAIN",
    "NOT_COMPARABLE", "NOT_SCORED_STUB", "UNTYPED", "UNDECLARED", "REFUSED", "BRIEF_UNRECORDED",
    "UNKNOWN", "ABSENT_AT_SENSITIVITY", "VOID",
    "UNRESOLVED",   # M4 branch G: inside the guard band; carried on INSTRUMENT, never PHYSICAL
    "TOLERANCE_UNRESOLVABLE",   # M4 branch G precondition: U >= tol, decided before m is read
)
TAGS = ("OBSERVED", "DERIVED", "PROPOSED")
ABSENCE_BASES = ("LADDER", "DECLARED")


class TokenError(ValueError):
    pass


def _need(value, what):
    if value is None or (isinstance(value, str) and not value.strip()):
        raise TokenError("%s required" % what)
    return value


class Token(object):
    def __init__(self, state, reason=None):
        if state not in STATES:
            raise TokenError("unknown state %r; states are %r" % (state, STATES))
        if state not in VERDICTS:
            _need(reason, "reason on non-verdict token %s" % state)
        self.state, self.reason = state, reason

    is_verdict = property(lambda self: self.state in VERDICTS)

    def __bool__(self):
        raise TypeError("a state token has no truth value; read .state")

    def __float__(self):
        raise TypeError("a state token is not a number; read .state")

    def __repr__(self):
        return "%s(%s)" % (self.state, self.reason or "")


class ExpiryTrigger(object):
    """Typed: kind, target, condition all required. The kind vocabulary is VOID in the spec."""
    is_exit = True

    def __init__(self, kind, target, condition):
        self.kind = _need(kind, "trigger kind")
        self.target = _need(target, "trigger target")
        self.condition = _need(condition, "trigger condition")


def untyped(text):
    t = Token("UNTYPED", _need(text, "untyped note text"))
    t.is_exit = False
    return t


def unknown(reason, triggers):
    triggers = list(triggers)
    typed = [t for t in triggers if isinstance(t, ExpiryTrigger)]
    if not typed:
        raise TokenError("UNKNOWN refused: no typed expiry trigger (free text is UNTYPED, no exit)")
    t = Token("UNKNOWN", reason)
    t.typed = tuple(typed)
    t.untyped = tuple(x for x in triggers if not isinstance(x, ExpiryTrigger))
    return t


def absent_at_sensitivity(limit, basis, effect_size, conditions, ladder=None):
    _need(limit, "limit")
    _need(basis, "basis (LADDER or DECLARED)")
    _need(effect_size, "effect size of interest")
    _need(conditions, "conditions the null holds under")
    if basis not in ABSENCE_BASES:
        raise TokenError("basis %r not in %r" % (basis, ABSENCE_BASES))
    if basis == "LADDER":
        _need(ladder, "ladder reference for a LADDER basis")
    t = Token("ABSENT_AT_SENSITIVITY", "not found at limit %r (%s) under %s" % (limit, basis, conditions))
    t.limit, t.basis, t.effect_size, t.conditions, t.ladder = limit, basis, effect_size, conditions, ladder
    t.covers_effect = limit <= effect_size
    return t


class _Tag(object):
    def __init__(self, claim, value):
        self.claim, self.value = claim, value


class _Record(object):
    def __init__(self, claim, chain):
        self.claim, self.chain = claim, chain


class Claim(object):
    """A statement with its tag (status) and its record (provenance chain), linked 1:1."""

    def __init__(self, statement, tag, chain):
        _need(statement, "claim statement")
        if tag not in TAGS:
            raise TokenError("claim tag %r not in %r: untagged claims are refused" % (tag, TAGS))
        chain = tuple(chain)
        if not chain:
            raise TokenError("claim record needs a provenance chain")
        self.statement = statement
        self.tag = _Tag(self, tag)
        self.record = _Record(self, chain)


VOCABULARY_MAPPING = Token("VOID", "Q12: the spec keeps s-a ConditionBasis and #257 STATUSES apart and calls for "
                                   "a mapping table, but gives no rows; rows are not invented here")
