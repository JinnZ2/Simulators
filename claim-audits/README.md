# claim-audits

Standalone single-file audits of external documents. Each audit assigns
one of eight verdicts to every claim it addresses, with per-claim
attribution so a document's own moves are not conflated with model
overlay.

CC0. stdlib-only. Phone-buildable.

## The convention

Every audit in this folder follows the same shape:

```
CLAIMS: List[Claim]
class Claim: cid, who, text, verdict, why, fix
report() prints the table + tally + attribution split + headline
```

**Per-claim attribution** (`who`):

| code | meaning |
|------|---------|
| `K` | original author's move (documented as theirs, audited on its own terms) |
| `M` | model overlay (what an LLM added on top; audited separately) |

Auditing the overlay as though it were the claim wastes both authors'
time. Separation first.

**Eight verdict codes:**

| verdict | meaning |
|---------|---------|
| `VERIFIED` | source checked, mechanism holds |
| `SOUND` | holds as stated (no external source required) |
| `SIGN_BACKWARDS` | the quantity is real; the direction of the claim is inverted |
| `UNGROUNDED_NUMBER` | threshold with no derivation, units, or calibration |
| `DIMENSIONALLY_VOID` | the expression is not a quantity |
| `GAMEABLE` | metric is maximized by doing the opposite of the intent |
| `IDENTITY` | true but empty — a bookkeeping relation, no predictive content |
| `UNVERIFIED` | cited source not locatable; absence of evidence, not absence |

`GAMEABLE` and `SIGN_BACKWARDS` are the two verdicts that carry the
most information — both name a mechanism that works AGAINST the stated
intent. `UNVERIFIED` is deliberately distinct from any negative
verdict (it flags a gap, not a failure).

Each Claim carries `why` (the audit's reasoning) and `fix` (the
smallest actionable repair). The `fix` field is where the audit stops
being critique and starts being useful.

## Files

```
claim_audit_visibility.py   audit of the Visibility Protocol document.
                            14 claims (V0..V13), 4 K-moves + 10 M-overlay,
                            headline V0: no null model anywhere -- every
                            threshold in the doc is undecidable until each
                            metric has a distribution under "nothing
                            happening."
```

Sibling files named in the module docstrings but not yet in the tree:

```
adversarial_corpus.py       (sibling; not yet landed)
claim_audit_spin.py         (sibling; not yet landed)
```

They will follow the same shape (`Claim` dataclass, `CLAIMS` list,
`report()`) when they land, and share this README's convention.

## Boundaries

- **No auto-verdict.** Every entry is hand-written by the auditor. The
  module runs a printer over the list; the reasoning is authored.
- **`fix` is a suggestion, not a prescription.** Some audits will show
  a `fix` the original author will reject on principle. That's the
  point of separation: the audit surfaces the choice.
- **`SOUND` and `VERIFIED` are separable.** `SOUND` means the reasoning
  is internally coherent; `VERIFIED` means an external source was
  actually checked. A claim can be `SOUND` without being `VERIFIED`
  when the source hasn't been visited but the reasoning stands on
  ground the audit trusts.

## License

CC0 1.0 Universal. Public domain.
