# branch-set

CC0. Stdlib only. Phone-buildable. Item F of `WORK_ORDER.md` (verbatim),
marked `[OWN REPO]` there; built here as its own promotable folder, the
repository creation being the operator's call.

`branch_set.py` serializes a held branch set so it survives transport to
a model or a reader. Collapse happens at MEASUREMENT, not at intake: a
branch leaves the set when its discriminator eliminates it, and each
elimination is recorded as a result with the discriminator named.

```
python3 branch_set.py --new > branches.jsonl        # skeleton row
python3 branch_set.py branches.jsonl [--lag-years 20] [--json]
python3 branch_set.py --selftest
```

Outputs: the ranked test queue (priority = number of open branches
fitting the same result, then cost ascending: the cheapest discriminator
runs first, not the most central one), the eliminated-set record, the
gap list (predictions in other domains whose record state is unknown or
present, crossed with the branch's suppression cause), and a triage per
gap by stated rule: `answerable_now` / `buildable` / `simulable` /
`blocked(+blocker)`. An instrument-history lag at or above the threshold
on a branch that does not state ACCESS suppression is flagged and never
rewritten. The threshold is printed.

`samples/` holds the constructed fixture and its output.
