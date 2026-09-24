# thwaites-risk-audit

An outside document that says it **ran this repository**, landed verbatim,
plus the checks on it.

`external-audit/` and `deep-research-correction/` hold reports *about*
this tree. This one is different in the way that matters: its first line
is *"All tools below were **actually cloned and run** from
`github.com/JinnZ2/Simulators`"*, and every tool it names is in the tree
beside it. So the **tool** claims are reproducible here and the **paper**
claims are not — the egress gate is an allowlist and only `github.com`
answers. `audit.py` enforces that split: every `run_*` function imports
the sibling module and executes it; everything resting on a publication is
CARRIED and enters no verdict.

Nothing in this folder is a statement about Thwaites Glacier, any ice
sheet, the AMOC, ENSO, sea level, or any paper.

## What is here

```
SOURCE_DROP.md       v1, delivered in a zip.  46767 bytes.
SOURCE_DROP_V2.md    v2, the delivered "diff test".  v1 with a six-row
                     repair log and the repairs applied in place.
OPERATIONS_REDUNDANCY_AUDIT_TEMPLATE.md   three derived deliverables,
WARNING_CARD_SPEC.md                      delivered in the same zip,
WORKER_FIELD_BRIEF_DESIGN_LIFE.md         verbatim.
audit.py             the checks.  Imports the siblings, edits nothing.
CLAIM_TABLE.md       TRA_001..TRA_028.
test_audit.py        prints its own check count.
samples/             pinned render.
```

Both renderings land side by side and neither supersedes the other —
`observer-exclusion` `SPEC_V2`, `failure-mode-register` `WORK_ORDER_V2..V4`,
`move-set` V2, `mining-increment` V2/V3. A revision that quotes its own
repairs is a copy, and copies drift.

## A third copy already exists, and it is the headline

Section 12c reads *"Repo convergence note: `Simulators/AMOC/research.md`
(commit f35e1f5) independently added Kasuya and Nian while these searches
ran. Same two papers, two independent routes."*

`f35e1f5:AMOC/research.md` is a **byte-exact prefix of v1** — 27070 of
46767 bytes, sections 1 through 10, under v1's own title and v1's own
uncorrected *"Bradley et al."* heading. It names those two papers because
**it is this document**, committed to `main` as AMOC research. The two
routes are one route (`TRA_002`).

That file is on `main` and is **not touched from here**. Whether it should
move, be replaced by a pointer, or stay is the operator's call; this
folder records that it exists, where, and what it is.

## What the checks found

Sharpest first. Every number is computed by `audit.py`.

- **`TRA_002`** the convergence note is refuted by content: one document
  in two places. `TP_003`'s shared-bias result arriving on a citation
  claim, in the document that computes `N_eff = 1` for somebody else.
- **`TRA_006`** the `reservoir-chain-coupling` block is
  `signal_chain()`'s shipped fixture output with four node names
  substituted. Every number identical.
- **`TRA_008`** relabelling that fixture's columns `independent`/`coupled`
  to `max`/`sum` makes all four rows read as arithmetically impossible
  (`a+b ≤ 2·max(a,b)`; row 1 is 9.00 against 8.40). Under the module's own
  names there is no difficulty.
- **`TRA_013`** κ = 0.000 is **forced** by the reported `N_eff = 1`: a
  constant second coder returns exactly 0.0 in 62 of 62 non-degenerate
  codings. The document's R6 flags it invalid for the weaker reason.
- **`TRA_010`** `compare.py` holds a hardcoded three-arm dict, so the
  *"four-arm result"* is not what it computed.
- **`TRA_012`** `[COVERED widen]` means the question was **reached**; the
  document reads it as residual. And a `COVERED`-by-widen is `MF_004`,
  still unrepaired — so the document's conclusion is right in spite of the
  line it cites.
- **`TRA_019` / `TRA_020`** *"≈ 0.50 Sv"* is the calibration's own anchor
  read back out, and the docstring hands the document a published band
  (0.1–0.4 Sv added) that it does not report — against its own opening
  rule, *"report the band, plan against the short end."*
- **`TRA_022`** the one step that runs toward overstating: 50–60 Gt →
  ~0.15 mm SLE is exact **for grounded ice**, and the quantity named is
  floating-shelf **basal** melt, whose direct contribution is ~9.3×
  smaller.
- **`TRA_026`** R1's citation repair reached the audit and **not** the
  one-page field brief, which still names Bradley twice — including in its
  own PROVENANCE line.
- **`TRA_004`** none of the nine stated input files is in the delivery, so
  no run is reproducible; what is checkable is the tools' behaviour.
- **`TRA_024`** `THW-02` carries two KINDs in a single-valued field, and
  its `STATE` (`assembly`) forces the other one — two gaps in one block.

And what holds: the exact reproductions (`TRA_005` S1, `TRA_017` OIR,
`TRA_021` the flux conversion), and **`TRA_028`**, the document's own
repair discipline — a repair log before the body, a retired falsifier, a
counterweight entered against its own narrative, an over-transfer scoped
down on the operator's critique, and a *"still unrepaired"* list naming
two unsourced assumptions in its own load-bearing section.

## Commands

```sh
python3 thwaites-risk-audit/audit.py             # the checks, rendered
python3 thwaites-risk-audit/audit.py --choices   # the six declared choices
python3 thwaites-risk-audit/test_audit.py        # prints its own count
```

`audit.py` refuses `--selftest` and names the suite. `TRA_002` needs
`origin/main` fetched; without it the check degrades to
`NOT_RESOLVABLE_IN_THIS_CLONE` and names the remedy rather than reporting
the claim as holding.

Stdlib only, no network, parses under 3.9, phone-buildable. CC0.
