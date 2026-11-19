# Excerpt of P1/playground-crossrun/COMBINED_SPEC.md, original line numbers kept (lines 35-96, 122-145 of 390). Lines not shown are omitted, not empty.

   35| ## 2. Axes, statuses and the #257 mapping
   36| 
   37| Three failure axes, canonical from s-a: **PHYSICAL**, **INSTRUMENT**, **DETERMINATION**.
   38| APPLICABILITY is a separate field and is not a failure axis (Q11). **COVERAGE** is a separate
   39| field too, and never feeds severity (R-A2):
   40| 
   41| ```text
   42| COVERAGE entry   kind ∈ {UNKNOWN, INFO, GAP_INSTRUMENT_CRASH}, module, input, reason,
   43|                  missing_path, expiry_condition
   44| source           P3 calibration/unified_audit.py @ [commit], lines 96-101, CHECKED (section 7)
   45| ```
   46| 
   47| ```text
   48| status          meaning                                        reason field
   49| OK              ran and passed                                 --
   50| FAILED          ran and failed                                 required
   51| INDETERMINATE   ran; not enough to say                         required
   52| UNTESTED        no check addressed it                          required
   53| CRASHED         did not run: the check raised                  exception + path, required  (Q3)
   54| CLOSED_WITHIN   closure holds within sigma, not exactly        sigma + basis, required     (Q2)
   55| OUTSIDE_DOMAIN  APPLICABILITY only: input beyond a bound       the bound, required         (Q11)
   56| ```
   57| 
   58| Every reason #257 can emit, mapped:
   59| 
   60| ```text
   61| #257 source                              condition                     -> field : status (reason)
   62| l0.run_status INCOMPLETE "did not close" closure fail, ledger declared -> PHYSICAL : FAILED
   63|                                          complete                         (F9: the leak is a model defect)
   64| l0.run_status INCOMPLETE "did not close" closure fail, ledger NOT      -> DETERMINATION : FAILED
   65|                                          declared complete                (F8, F9: accounting gap)
   66| l0.run_status INCOMPLETE "no LIVE        every budget VOID             -> DETERMINATION : UNTESTED
   67|   budget"                                                                 (NO_LIVE_BUDGET)          (Q1)
   68| l0 NOISE                                 misclosure within k sigma     -> PHYSICAL : CLOSED_WITHIN
   69|                                                                           (sigma, basis; sigma per account) (Q2)
   70| certify / certify_tool UNTRUSTED         harness misses plants         -> INSTRUMENT : FAILED
   71| certify_tool raise (ZeroDivisionError)   tool gate crashes             -> INSTRUMENT : CRASHED
   72|                                                                           (exception, path); never a missing row (F2, Q3)
   73| trust with no cases written              zero known-answer cases       -> INSTRUMENT : UNTESTED (s-a KA_NO_CASES)
   74| known answer from the tested formula     circular case                 -> INSTRUMENT : UNTESTED
   75|                                                                           (CIRCULAR_KNOWN_ANSWER)   (Q6)
   76| size / population / founder bound hit    input beyond a declared bound -> APPLICABILITY : OUTSIDE_DOMAIN
   77|                                                                           on no failure axis (F13, Q11)
   78| ```
   79| 
   80| Rules:
   81| 
   82| - R-A1: the "declared complete" flag is part of the ledger record and must be set explicitly.
   83|   If it is absent, the ledger counts as NOT declared, and the failure lands on DETERMINATION,
   84|   never on PHYSICAL (F9).
   85| - R-A2: a crash is a record carrying the exception type, the call path that raised, and the
   86|   inputs. A crash never produces "no row" (F2). CRASHED stays an INSTRUMENT status, and it is
   87|   reported on the coverage axis (kinds UNKNOWN / INFO / GAP_INSTRUMENT_CRASH), never in severity.
   88|   The coverage entry carries P3's fields: kind, module, input, reason, missing_path,
   89|   expiry_condition (source: section 7).
   90| - R-A3: a field no gate read is UNTESTED, never OK by default.
   91| - R-A4: closure tolerance is declared PER ACCOUNT, BEFORE the run. There is no global default; a
   92|   missing tolerance refuses the run rather than filling 1e-9 silently (O4, Q13). The numerical
   93|   roundoff floor is recorded separately as its own known class (forest run 10), not folded into
   94|   sigma.
   95| - R-A5: step-1 rows are NOT relabelled. Step 3 adds a second column, "relabeled under COMBINED
   96|   mapping", beside the preserved step-1 code (Q15).
  ...

  122| ---
  123| 
  124| ## 4. States: one token per state, a reason on every non-verdict
  125| 
  126| - **UNKNOWN requires a typed expiry trigger** (from #257 `NEEDS_EXPIRY`, typed per s-a
  127|   `ExpiryTrigger`). Free text is accepted only as `UNTYPED` and counts as "no exit defined", so it
  128|   does not satisfy the requirement (F10, F14, Q4). An UNKNOWN with no typed trigger is refused.
  129| - **Scoped absence and detection limits** (from s-a `establish_sensitivity`, `claim_absence`).
  130|   `ABSENT_AT_SENSITIVITY` must carry three things, or it is refused (F7):
  131|   - the limit, and how it was established (from a ladder, or declared);
  132|   - the effect size of interest;
  133|   - the conditions the null holds under.
  134| - Each state has a distinct token: INDETERMINATE, UNTESTED, CRASHED, CLOSED_WITHIN,
  135|   OUTSIDE_DOMAIN, NOT_COMPARABLE, NOT_SCORED_STUB, UNTYPED, UNDECLARED and REFUSED are all
  136|   different. None is ever read as 0, OK or "no row".
  137| - A `reason` is required on every token that is not a verdict; an empty reason is refused at
  138|   construction.
  139| - Vocabularies are kept separate (s-a ConditionBasis, #257 STATUSES) with an explicit mapping
  140|   table between them; merging would lose one side's distinctions (Q12).
  141| - Claim tags (#257 OBSERVED / DERIVED / PROPOSED) and claim records (s-a ClaimRecord) are two
  142|   objects linked 1:1: the tag is the status of a statement, the record is its provenance chain
  143|   (Q8).
  144| 
  145| ---
