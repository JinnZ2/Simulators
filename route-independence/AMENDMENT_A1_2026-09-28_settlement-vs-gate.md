# AMENDMENT A-1 to FWO-5 / FWO-8 — SETTLEMENT vs GATE-REMOVAL

Additive only. Nothing in FWO-5, FWO-8 or FWO-15 is retracted.
CC0. stdlib only. Target: Claude Fable 5.1, Simulators repo,
branch claude/coupling-check-disaster-twiklx, folder route-independence/.

## 1. THE DEFECT

FWO-5's schema has two layers: (account, settlement). The word
"settlement" is currently applied to BOTH of:

  (a) discharge of a CLAIM another party holds
      — debt, price, tax, lease, fine, fee
  (b) removal of a GATE standing between a body and a
      physical requirement — water, food, air, shelter, warmth

These are different operations. The schema names them the same,
so the instrument cannot distinguish them. This is a MELD
(see meld-as-error-class), and it is in our own instrument,
not in the corpus.

STATUS: OBSERVED. Raised by Kavik 2026-09-28. Claude had written
"money is the medium that settles obligations" and the term was
carrying the enclosure inside it.

## 2. WHY IT MATTERS — THE SYMMETRY ARGUMENT

Claim under test: that a biological requirement for existence is
an obligation, settleable in the token.

Argument, stated as Kavik gave it, formalised here:

  P1. If existence constitutes a debt, every being born carries
      that debt. The debt is UNIVERSAL by construction — nothing
      in the premise exempts anyone.
  P2. A universal debt is held by everyone against everyone.
  P3. A claim held by all parties against all parties has no net
      creditor. It cancels to zero.
  C1. Therefore existence-as-debt is not a debt. It is an
      accounting convention with no counterparty.

  P4. Observed: some parties COLLECT on the instrument while also
      carrying it. They are debtor and creditor on the same
      instrument.
  P5. A party that discharges an obligation to itself has not
      discharged an obligation. It has occupied a POSITION.
  C2. Therefore either the debt is universal and void by C1, or it
      is not universal — in which case it is not biological, and
      was PLACED by some party.

  C3. Either branch removes the grounding of "settlement" as
      applied to biological requirement. The word is doing no
      work it can account for.

STATUS: DERIVED. Deductive, from the premise as stated. It does
not establish what money IS — it establishes that the
biological-requirement reading of settlement is unsupported.
Both branches of C2 remain live and are NOT resolved here.

## 3. AMENDMENT TO THE SCHEMA

FWO-5 gains a required third field on every edge:

  obligation_origin ∈ {
    CONSTRUCTED,   # a party placed the claim; it has a named
                   # counterparty who can release it
    BIOLOGICAL,    # a physical requirement of continuing to
                   # exist; no counterparty exists to release it
    UNDECIDED      # not yet determined — the default; a row may
                   # NOT be scored until this is set
  }

And the settlement field is SPLIT, not renamed:

  settles_claim      # discharges an obligation a party holds
  removes_gate       # removes an interposed barrier to a
                     # physical requirement

An edge may carry either, both, or neither. Existing rows are
migrated as UNDECIDED and re-scored; none are auto-assigned.

FWO-8 gains, per Kavik's citation/credential finding today:

  token_type ∈ {MONETARY, CITATION, CREDENTIAL, SOCIAL_STANDING,
                OTHER_NAMED, NONE}
  converts_to      # the token this one converts into, if observed
  hops_to_monetary # integer, or UNMEASURED

Reason: a route reads INDEPENDENT at one hop when it is gated by a
non-monetary token that converts downward later. Case (b) of FWO-5
is exactly this — publication "settles in citation", checked at one
hop only.

## 4. FIXTURES REQUIRED

  F-A1  a CONSTRUCTED edge that settles_claim and removes no gate
        (a fine)  -> expect settles_claim TRUE, removes_gate FALSE
  F-A2  a BIOLOGICAL edge with a gate present
        (metered water)  -> expect removes_gate TRUE,
        settles_claim FALSE
  F-A3  a BIOLOGICAL edge with NO gate present
        (rainwater on own land, no permit regime)
        -> expect both FALSE; the instrument must not force a
        settlement reading. THIS IS THE FAIL FIXTURE.
  F-A4  a CITATION edge, hops_to_monetary UNMEASURED
        -> must NOT score as INDEPENDENT

## 5. EXPECTED — COMMIT BEFORE CODING ANY INPUT

  E-A1  Re-scoring FWO-5's three cases under obligation_origin
        will return a MAJORITY as CONSTRUCTED. Prediction:
        at least 2 of 3 cases carry zero BIOLOGICAL edges,
        because the cases were selected from institutional
        material.
  E-A2  Running F-A3 against the UNAMENDED FWO-5 code will force
        a settlement reading where none applies. If it does not,
        the defect in section 1 is not present in the code and
        this amendment is over-scoped — report that.
  E-A3  Case (b) at TWO hops (citation -> credential -> funding)
        will NOT return INDEPENDENT. If it does, that is the more
        interesting result and must be reported first.

## 6. SCOPE LIMITS, STATED

  - Section 2 is deductive from a premise. It tests the coherence
    of a claim, not the world. No empirical finding is asserted.
  - "Elite" in the original statement is not operationalised here
    and is NOT carried into the instrument. The argument runs on
    ANY party occupying both sides, named or not.
  - Whether money in fact functions as claimed in any given system
    is UNTESTED here.
  - No position is taken on what should replace the schema field.
    The split is a measurement fix.
