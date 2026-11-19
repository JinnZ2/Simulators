# Excerpt of P1/cplay/closure.py, original line numbers kept (lines 284-336 of 448). Lines not shown are omitted, not empty.

  284| class FieldToken(namedtuple("FieldToken", "field token")):
  285|     """A non-axis state carried on INSTRUMENT: branch G's UNRESOLVED, and its precondition flag
  286|     TOLERANCE_UNRESOLVABLE."""
  287|     __slots__ = ()
  288|     STATES = ("UNRESOLVED", "TOLERANCE_UNRESOLVABLE")
  289| 
  290|     def __new__(cls, field, token):
  291|         if field != "INSTRUMENT":
  292|             raise ClosureError("UNRESOLVED / TOLERANCE_UNRESOLVABLE are carried on INSTRUMENT, never %s"
  293|                                % field)
  294|         if not isinstance(token, T.Token) or token.state not in cls.STATES:
  295|             raise ClosureError("FieldToken carries one of %r" % (cls.STATES,))
  296|         return super().__new__(cls, field, token)
  297| 
  298| 
  299| def verdict_branch_G(result, misclosure=None):
  300|     decl, m, band = _accepted(result, misclosure)
  301|     if band is None:
  302|         return T.Token("VOID", "branch G needs sigma and k declared for account %s" % decl.account)
  303|     floor, void = _floor(result, "G")
  304|     if void is not None:
  305|         return void
  306|     u = band + floor
  307|     if m <= floor:
  308|         return A.reading("PHYSICAL", "OK")
  309|     if m <= decl.tolerance - u:
  310|         return _closed(decl, m, decl.tolerance - u, what="tol - U")
  311|     if m > decl.tolerance + u:
  312|         return _failed(result, decl, m)
  313|     return FieldToken("INSTRUMENT", T.Token(
  314|         "UNRESOLVED", "|m| = %g within guard band tol +/- U = %g +/- %g (source %s: %s)"
  315|         % (m, decl.tolerance, u, G_SOURCE_STATUS, G_SOURCE)))
  316| 
  317| 
  318| def g_precondition(result, account):
  319|     """Decided from the declarations alone, before any misclosure is read. Returns the flag
  320|     FieldToken("INSTRUMENT", TOLERANCE_UNRESOLVABLE) when U >= tol, None when U < tol, and a VOID
  321|     token when U cannot be formed (no sigma / k, or a token floor)."""
  322|     if result.state != "ACCEPTED":
  323|         raise ClosureError("no precondition on a %s run" % result.state)
  324|     decl = result.prereg.accounts[account]
  325|     if decl.sigma is None or decl.k is None:
  326|         return T.Token("VOID", "U needs sigma and k declared for account %s" % account)
  327|     floor, void = _floor(result, "G")
  328|     if void is not None:
  329|         return void
  330|     u = decl.k * decl.sigma + floor
  331|     if u >= decl.tolerance:
  332|         return FieldToken("INSTRUMENT", T.Token(
  333|             "TOLERANCE_UNRESOLVABLE", "U = %g >= tol = %g: no misclosure can prove conformance "
  334|             "(account %s)" % (u, decl.tolerance, account)))
  335|     return None
  336| 
