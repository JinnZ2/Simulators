WORK ORDER — standing/A-6.3 : verification split,
lint labels, Part B status
from: Kavik via Claude (chat), 2026-09-30
repo state: test_sourcing_a62.py 145/0,
            test_standing_a61.py 148/0,
            root suite 4 known failures
            (tests/test_run_manifest.py)

0. PART B STATUS — report FIRST, before any work
   Order A-6.2 items 9–14 were not in the last
   report. For each: done / in progress / not
   started / dropped, with commit if done.
     9  P-17 UnboundLocalError (branch named?)
    10  P-18 selftest fixture
    11  README reading-order line (dependency or
        preference?)
    12  root CLAUDE.md potential/ paragraph
    13  KNOWN_RED §11 bounded half
    14  holding items
   Also: are the 4 test_run_manifest.py failures
   the §11 set, a subset, or separate?

1. RIN_142 — repo files as sources (DECIDED)
   accept location form:
     repo:<commit>:<path>
   required alongside: remote clone url
   → E-A2-4, E-A3.1-1 (both readings) re-gate
   → the CONSTRUCTED-first gate stays first; no
     fixture reads MATCH

2. RIN_150 — verification split (DECIDED)
   rule 0 now proves consistency only. Split:
     STORED_UNVERIFIED  span + hash + location
                        on file
     VERIFIED           an INDEPENDENT retrieval
                        returns bytes whose sha256
                        matches the stored hash
   verification record: who/what fetched, date,
   hash obtained
   → only VERIFIED lets a row read MATCH
   → repo:<commit>:<path> verifies by checkout at
     that commit; allowed in-session
   → web spans stay STORED_UNVERIFIED while egress
     is blocked
   → the placeholder test from RIN_150 must now
     read STORED_UNVERIFIED, not MATCH; keep it as
     the fail fixture

3. CE-4e erratum note — declare its coding rule
   finding (RIN_148): the ≥3 and ≥2 bounds match
   GEOGRAPHIC coding exactly; the move 1 → 3 was
   a coding-rule change, not new paths
   → add a status note to CE-4e: coding rule =
     GEOGRAPHIC, undeclared at issue
   → origin of the undeclared rule: the chat
     handover (Claude), not the agent

4. LINT — year heuristic
   [CHOICE 30] drops 1000–2999 as years
   → replace with: year-shaped numbers are
     FLAGGED, not dropped; treated as a year only
     with date context (a month name, "in",
     "since", "by", or a range to another
     year-shaped number)
   → fixture: "2036 paths" must be credited as a
     count
   → fixture: "since 1971" must not be credited

5. LINT — labels are not counts
   a number directly after an identifier token is
   a LABEL:
     rule N, item N, step N, A-N, RIN_N, P-N,
     E-A…, CE-N, FWO-N, [CHOICE N]
   → declare the identifier list as data in the
     module, not inline
   → fixture: "rule 0 these rows" credits nothing
   → re-run pins A-4..A-6.1; report any identity
     change

6. RIN_145 — alias map for id ranges
   "1 of P-0..P-4 (unit: profiles)" FLAGs because
   agreement doesn't read id ranges
   → add a DECLARED alias map (P-* → profiles),
     as data, one line per prefix
   → rows stay FLAG until their prefix is in the
     map; no inference of aliases
   → report whether A-6 returns to 3 once P-* is
     declared

7. RIN_146 — mutation test on gates
   for every status gate: flip one input and
   assert the output changes
   → a gate returning the same value on all
     inputs = test FAIL
   → run over every gate in the module; report
     any that fail

8. W-1a, W-2a — web address in description text
   → move the address into the url field
   → status stays STORED_UNVERIFIED; no span yet

REPORT FORMAT
  Part B status first
  then what didn't hold
  per item: status, RIN, test counts
  counts line: VERIFIED / STORED_UNVERIFIED /
               NO_SPAN / CONSTRUCTED across all
               re-gated rows
  no row reads MATCH on STORED_UNVERIFIED input
