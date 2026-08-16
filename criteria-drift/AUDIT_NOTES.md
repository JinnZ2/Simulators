# AUDIT_NOTES — criteria-drift

The kit is delivered **verbatim**: `README.md`, `schema.py`, `store.py`,
`drift.py`, `regress.py`, `audit.py`, `example_data/`,
`example_drift_plot.png`. Nothing in it is modified.

Added here:

```
drift_sign.py        can the metric carry the hypothesis?   CD_002
regression_audit.py  the series, and the term that is missing  CD_003..007
CLAIM_TABLE.md       seven claims
```

```bash
python3 audit.py init
for f in example_data/codebench_v*.json; do python3 audit.py ingest-criteria $f; done
for f in example_data/score_*.json;     do python3 audit.py ingest-score    $f; done

python3 drift_sign.py
python3 regression_audit.py      # needs the database above
```

`drift.db` is runtime state and is gitignored.

## What holds

**The kit is the declared-frame block's first real consumer.** `Frame` is a
first-class dataclass in `schema.py`, `unknown` is a legal value, omission
is flagged separately, and drift is computed per frame field rather than on
a blob. Every other use of the block so far has been a document; this one
puts it in a database and computes on it.

**The design constraints are met.** Stdlib only, SQLite, JSON in and out,
runs offline, every piece replaceable. `audit.py`'s quick start works as
written.

**The question is the right one and is not being asked elsewhere.**
`../anchor-interval/moving_reference.py` argues that a reported delta mixes
capability and criteria; this is a tool for measuring the second term. The
distinction it draws — existing work treats criteria drift as noise to
suppress, this treats it as signal to model — is real.

## What the audit found

Two mechanical defects, three structural results, in `CLAIM_TABLE.md`.

The short version: the metric is unsigned and the decision rule reads the
sign; the series is built with a fabricated point that flips a slope; and
the regression is missing the term that would let it identify what it
reports. The last one is not a bug — it is the reason the measurement is
hard, and the repair is already expressible in the shipped schema.

## Where this sits

`../anchor-interval/` `ANC_005` proves the non-separability with a
constructive example. `ANC_006` names the repair — a held-fixed benchmark,
which buys a share and not a capability. This folder is the first place in
the repo where that repair has a data model to land in.
