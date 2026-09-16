# OVERRIDES

Append-only. One entry every time a red from the ledger was overridden,
waived, or ignored, including the ones with good reasons.

This file exists because `ADDENDUM.md` names the override count as **the
real signal** -- *a gate that gets routinely overridden has become bulk
regardless of what it catches* -- and it is the one quantity the ledger
cannot observe. An override happens outside the ledger: in a person's
head, in a CI config, in a commit that went in anyway. From inside the
gate, a gate that is routinely overridden and a gate that never is look
identical.

So the count is a **declared** field. Without a place to declare it, it
would read `UNRECORDED` forever, and the addendum's own strongest term
would be unreachable by construction.

`UNRECORDED` is not `0`. A review recording `0` is saying nobody
overrode a red. A review recording `UNRECORDED` is saying nobody
counted. `review.py --record` refuses either without a stated basis.

## Entries

One per override. Date, what fired, what was done, who decided.

*(none)*

A zero reading is the result, not an absence of one. If this file is
still empty at T+3 and T+9, that is a finding about how the gate is
being used, and it is only a finding if nobody was relying on it to fill
itself in.
