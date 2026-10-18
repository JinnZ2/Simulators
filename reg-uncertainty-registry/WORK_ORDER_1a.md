WO-REG-1a — ADDENDUM to WO-REG-1 (apply to Parts A, B, E)

PURPOSE: audit legacy mandates as decided, not as assumed correct.
Every DECISION / NON_DECISION must answer: who decided, under what
authority, based on what, with what conflicts.

A. New object: ACTOR
   fields: actor_id, type (person / office / agency / court / legislature /
           advisory_committee / sponsor), name, role_at_time, date_range
   edges:  decided_by, recommended_by, overruled (DECISION → ACTOR whose
           advice was set aside, e.g. advisory vote), delegated_from,
           funded_by (regulator funding: user fees, appropriations)

B. Authority chain on every DECISION
   statute → regulation → guidance → decision, each a node with citation.
   Flag any decision whose authority link is UNREACHABLE or NOT_FOUND.

C. Conflicts
   CONFLICT object: actor_id, type (financial / prior employment /
   reputational-institutional commitment / funding source), source,
   verification status. Record recusals. Absence of a disclosure record
   = NOT_FOUND, never "no conflict".

D. Unrecorded inputs (legacy)
   If a decision cites, or plainly relies on, an input that cannot be
   located (unpublished registrant study, lost docket item, sealed record):
   create the EVIDENCE node anyway, status UNREACHABLE, reason stated.
   Gaps stay visible as nodes, never as blanks.

E. Tools
   chain.py: print the actor + authority chain alongside the evidence chain.
   gaps.py:  add UNREACHABLE authority links, unlocated inputs, missing
             conflict records.
   who.py:   given ACTOR, list every decision, direction, and overruled
             advice; given DECISION, list everyone in its chain.

ACCEPTANCE: same as WO-REG-1. Log addendum items in the change log as
WO-REG-1a.
