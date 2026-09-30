WORK ORDER — standing/A-6.2 : physical sourcing rule
from: Kavik via Claude (chat), 2026-09-29
repo state: erratum a2f6ec2, build 37c8e58,
            test_standing_a61.py 148/0

0. RULE (decided by Kavik)
   SOURCED iff the span is physically reproducible:
     url + retrieval_date + verbatim span stored
     + sha256 of span
   Reader identity is NOT a field in the test.
   "Graded S by someone" without a stored span
   = NOT sourced.
   → implement as a check in code; replaces both
     candidate meanings (other-reader / this-session)

1. APPLY RULE, READ-ONLY FIRST
   - re-run over A-1..A-6.1 (all MATCH rows)
   - per row report: span_stored Y/N, hash Y/N
   - E-A2-1, E-A2-2, E-A2-3, E-A2.1-1, E-A2.1-2 are
     the rows the meaning question hinged on;
     report them individually
   - do not edit prior amendments; relabels go in
     new RINs pointing back, ids kept

2. GRADE PROPAGATION TO DERIVED QUANTITIES
   "≥7 unread" and "≥2 residence-presuming outside
   retrieved text" derive from NOT_RECORDED bounds.
   → derived values inherit the parent grade
   → add test: a derived count printed without its
     grade = FAIL

3. PINS: IDENTITY, NOT TOTALS
   A-6.1 held 4/8 while two tokens swapped.
   → pin (position, token, unit) per credited count
   → re-run pins on A-4, A-5, A-6, A-6.1; report any
     identity change even where the total is unchanged

4. UNIT LINT: NON-NEAREST FIXTURE
   add fixture: "3 routes via 2 chains (unit: routes)"
   nearest-before assigns to 2 → wrong
   → add unit/noun agreement as a second signal
   → proximity and agreement disagree = FLAG,
     never assign
   → report whether any existing row flips

5. RETRO RUN, SECOND CONDITION
   the retro pass relabelled 9 rows, all
   CONSTRUCTED_PASS. Confirm whether the single-
   aggregate-case condition (→ UNFALSIFIABLE_AS_RUN)
   was also run over A-1..A-5. If not, run it and
   report which of the 9 change label.

6. E-A6-3 RESCOPE — 25 CFR 83.11(b) structure
   (read in chat 2026-09-29 from LII mirror; the
    span is NOT yet stored, so under rule 0 these
    rows stay unsourced until it is)
   (b)(1) 11 enumerated forms (i)-(xi) + "or by other
          evidence" → OPEN set; combination of TWO
          OR MORE required → a path is a pair+
   (b)(2) 5 forms (i)-(v), any ONE sufficient; also
          satisfies (c)
   cross-links (b)<->(c): (b)(1)(xi), (b)(2)(v),
          (c)(1)(iv), (c)(2)(ii)
   consequences:
   - a "complete path list" cannot exist (open
     catch-all); only the enumerated set is closed
   - rescope the RIN_139 target to "enumerated forms,
     83.11(b)(1)-(2)"; the open remainder files as
     NOT_EVALUABLE BY CONSTRUCTION, a distinct reason
     from truncated retrieval
   - define "path" explicitly: item vs combination.
     Under combination, (b)(1) alone yields
     2^11 - 1 - 11 = 2036 paths. Run both
     definitions; tag the definition on the output.

7. RESIDENCE CODING — DUAL RULE, like the ledger
   LITERAL    "reside" in text      → 1  ((b)(2)(i))
   GEOGRAPHIC residence|land|area   → 3  (+ (b)(1)(ix),
                                          (b)(1)(x))
   run both, keep both, tag rule name on output;
   the divergence is the finding

8. SPAN INTAKE
   the 83.11 text arrives separately (egress
   blocked). On arrival: store the verbatim span,
   url, date, sha256 → then re-evaluate E-A6-3
   under rule 0.
   source url:
   https://www.law.cornell.edu/cfr/text/25/83.11
   official-edition check (govinfo annual CFR) is an
   open sourcing target, since LII ≠ official

REPORT FORMAT
  what didn't hold, first
  then per item: status, RINs, test count
  no row reads MATCH on unsourced input