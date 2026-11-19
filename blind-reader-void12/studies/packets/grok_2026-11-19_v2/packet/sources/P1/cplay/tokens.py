# Excerpt of P1/cplay/tokens.py, original line numbers kept (lines 1-140 of 140). Lines not shown are omitted, not empty.

    1| """M2. State tokens, typed expiry, scoped absence, claims (COMBINED_SPEC section 4). CC0 1.0 Universal.
    2| 
    3| Rules:
    4|   - one distinct token per state; none ever reads as 0, OK or "no row" (no numeric or
    5|     truth value: float() and bool() raise)
    6|   - a reason is required on every token that is not a verdict (VERDICTS = {OK})
    7|   - UNKNOWN requires at least one TYPED expiry trigger; free text is UNTYPED and is not
    8|     an exit (Q4)
    9|   - ABSENT_AT_SENSITIVITY carries limit + basis (LADDER with a ladder ref, or DECLARED),
   10|     effect size of interest, and conditions, or it is refused (F7)
   11|   - claim tag and claim record are two objects linked 1:1 (Q8); untagged claims refused
   12| 
   13| VOID in the spec, so VOID here (never a default):
   14|   - the ExpiryTrigger `kind` vocabulary: the spec requires typed triggers and lists no kinds
   15|   - the ConditionBasis <-> #257 STATUSES mapping table (Q12 keeps the two vocabularies and
   16|     asks for a table; the table's rows are not in the spec)
   17| Reading added here: `covers_effect` (limit <= effect size) is reported on a scoped
   18| absence. It refuses nothing; the spec requires the fields, not the comparison.
   19| """
   20| 
   21| VERDICTS = ("OK",)
   22| STATES = (
   23|     "OK", "FAILED", "INDETERMINATE", "UNTESTED", "CRASHED", "CLOSED_WITHIN", "OUTSIDE_DOMAIN",
   24|     "NOT_COMPARABLE", "NOT_SCORED_STUB", "UNTYPED", "UNDECLARED", "REFUSED", "BRIEF_UNRECORDED",
   25|     "UNKNOWN", "ABSENT_AT_SENSITIVITY", "VOID",
   26|     "UNRESOLVED",   # M4 branch G: inside the guard band; carried on INSTRUMENT, never PHYSICAL
   27|     "TOLERANCE_UNRESOLVABLE",   # M4 branch G precondition: U >= tol, decided before m is read
   28|     "SYSTEMATIC_ERROR_INDICATED",   # M4 diagnostic: |m| > k*sigma*sqrt(n_legs), on DETERMINATION
   29| )
   30| TAGS = ("OBSERVED", "DERIVED", "PROPOSED")
   31| ABSENCE_BASES = ("LADDER", "DECLARED")
   32| 
   33| 
   34| class TokenError(ValueError):
   35|     pass
   36| 
   37| 
   38| def _need(value, what):
   39|     if value is None or (isinstance(value, str) and not value.strip()):
   40|         raise TokenError("%s required" % what)
   41|     return value
   42| 
   43| 
   44| class Token(object):
   45|     def __init__(self, state, reason=None):
   46|         if state not in STATES:
   47|             raise TokenError("unknown state %r; states are %r" % (state, STATES))
   48|         if state not in VERDICTS:
   49|             _need(reason, "reason on non-verdict token %s" % state)
   50|         self.state, self.reason = state, reason
   51| 
   52|     is_verdict = property(lambda self: self.state in VERDICTS)
   53| 
   54|     def __bool__(self):
   55|         raise TypeError("a state token has no truth value; read .state")
   56| 
   57|     def __float__(self):
   58|         raise TypeError("a state token is not a number; read .state")
   59| 
   60|     def __repr__(self):
   61|         return "%s(%s)" % (self.state, self.reason or "")
   62| 
   63| 
   64| class ExpiryTrigger(object):
   65|     """Typed: kind, target, condition all required. The vocabulary is the P3 expiry_condition register
   66|     (EXPIRY_VOCABULARY, pinned); its keys are not mapped onto kind/target/condition (9c item 12, open)."""
   67|     is_exit = True
   68| 
   69|     def __init__(self, kind, target, condition):
   70|         self.kind = _need(kind, "trigger kind")
   71|         self.target = _need(target, "trigger target")
   72|         self.condition = _need(condition, "trigger condition")
   73| 
   74| 
   75| def untyped(text):
   76|     t = Token("UNTYPED", _need(text, "untyped note text"))
   77|     t.is_exit = False
   78|     return t
   79| 
   80| 
   81| def unknown(reason, triggers):
   82|     triggers = list(triggers)
   83|     typed = [t for t in triggers if isinstance(t, ExpiryTrigger)]
   84|     if not typed:
   85|         raise TokenError("UNKNOWN refused: no typed expiry trigger (free text is UNTYPED, no exit)")
   86|     t = Token("UNKNOWN", reason)
   87|     t.typed = tuple(typed)
   88|     t.untyped = tuple(x for x in triggers if not isinstance(x, ExpiryTrigger))
   89|     return t
   90| 
   91| 
   92| def absent_at_sensitivity(limit, basis, effect_size, conditions, ladder=None):
   93|     _need(limit, "limit")
   94|     _need(basis, "basis (LADDER or DECLARED)")
   95|     _need(effect_size, "effect size of interest")
   96|     _need(conditions, "conditions the null holds under")
   97|     if basis not in ABSENCE_BASES:
   98|         raise TokenError("basis %r not in %r" % (basis, ABSENCE_BASES))
   99|     if basis == "LADDER":
  100|         _need(ladder, "ladder reference for a LADDER basis")
  101|     t = Token("ABSENT_AT_SENSITIVITY", "not found at limit %r (%s) under %s" % (limit, basis, conditions))
  102|     t.limit, t.basis, t.effect_size, t.conditions, t.ladder = limit, basis, effect_size, conditions, ladder
  103|     t.covers_effect = limit <= effect_size
  104|     return t
  105| 
  106| 
  107| class _Tag(object):
  108|     def __init__(self, claim, value):
  109|         self.claim, self.value = claim, value
  110| 
  111| 
  112| class _Record(object):
  113|     def __init__(self, claim, chain):
  114|         self.claim, self.chain = claim, chain
  115| 
  116| 
  117| class Claim(object):
  118|     """A statement with its tag (status) and its record (provenance chain), linked 1:1."""
  119| 
  120|     def __init__(self, statement, tag, chain):
  121|         _need(statement, "claim statement")
  122|         if tag not in TAGS:
  123|             raise TokenError("claim tag %r not in %r: untagged claims are refused" % (tag, TAGS))
  124|         chain = tuple(chain)
  125|         if not chain:
  126|             raise TokenError("claim record needs a provenance chain")
  127|         self.statement = statement
  128|         self.tag = _Tag(self, tag)
  129|         self.record = _Record(self, chain)
  130| 
  131| 
  132| VOCABULARY_MAPPING = Token("VOID", "Q12: the spec keeps s-a ConditionBasis and #257 STATUSES apart and calls for "
  133|                                    "a mapping table, but gives no rows; rows are not invented here")
  134| 
  135| 
  136| # 9c item 11: the expiry vocabulary is the P3 expiry_condition register, pinned, not copied.
  137| TAF_EXPIRY_KEYS = ("instrument_class", "sensitivity", "protocol", "provenance")
  138| EXPIRY_VOCABULARY = Token("REFUSED", "not redefined here: P3 calibration/expiry_register.py EXPIRY_KEYS, "
  139|                           "pin P11-p3-expiry-register (main [commit]); mapping onto ExpiryTrigger's "
  140|                           "kind/target/condition is 9c item 12, author's call")
