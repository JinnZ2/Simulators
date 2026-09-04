# envelope-asymmetry

A protocol delivered verbatim in `PROTOCOL.md`: does envelope
discipline — the operating range, out-of-scope declaration, degradation
mode, revalidation trigger, quantified margin and named responsible
party a document states — track the host domain's return channel rather
than liability, field prestige or AI regulation itself? A six-marker
instrument, two tests (within-vendor paired across host domains; between
arms inside one filing regime), four named threats. `envelope_score.py`
is the instrument and both tests, computed from a JSONL in the
protocol's schema; `protocol_audit.py` reads the protocol against it on
constructed rows and on the protocol's own text.

**No document is coded.** No vendor documentation site and no filing
registry answers from here (the registry host probed once, no response),
and no row is invented; with no rows every reading is `undetermined`
and the gate refuses before either test runs. The T4 domain list is
pre-registered in `domains.json` with its hash printed on every render.

    python3 envelope-asymmetry/envelope_score.py                      # unfilled
    python3 envelope-asymmetry/envelope_score.py --rows RECORDS.jsonl
    python3 envelope-asymmetry/envelope_score.py --domains
    python3 envelope-asymmetry/protocol_audit.py
    python3 envelope-asymmetry/selftest_env.py

| step | function | reads |
|---|---|---|
| schema | `validate_rows` | stored score equals the marker sum; a structural absence carries no marker and no words; refusals, not repairs |
| gate | `agreement` / `gate` | percent and Cohen's kappa (imported from `effective-redundancy-audit`), per marker and pooled; the gate reads pooled kappa `[CHOICE 1]` and the 20% double-coding share |
| test 1 | `test1` / `sign_test` | paired mean difference and an exact sign test, per-marker deltas, the E6 reading, and both accountings of structural absence |
| test 2 | `test2` | E1/E2/E4 rates between arms inside one filing period; zero variance across every marker is the template kill |
| T1 | `covariate` / `per_1000` | score on `doc_words` plus an arm indicator (OLS imported from `sim-span`); markers per 1000 words beside it |
| T3 | `unblindable` | the fraction of coded documents whose domain was inferable |
| T4 | `domains` | the pre-registered list, its hash, and the two mid-standard domains |

Three choices the protocol leaves open are printed on every render:
which agreement statistic the 0.7 gate reads, what "A >> B" is (a
paired mean difference of at least one marker), and the sign-test
alpha.

What the constructed rows show, with the numbers in `CLAIM_TABLE.md`:
the gate passes on an instrument whose E6 has kappa 0.0, and on one
that has never coded a marker present (`ENV_002`); the two accountings
of structural absence the protocol asks for return opposite readings on
one set of pairs (`ENV_003`); "E6 flat" has two values and the split
reading fits one of them (`ENV_004`); the per-1000-words secondary
outcome ranks a short document above a long one the primary ranks below
it (`ENV_005`); the template kill is a property of one record
(`ENV_006`); five of the six markers already have a field in this
tree's claim record and the sixth, the named responsible party, has none
(`ENV_007`); and the compressed restatement the protocol ends with
drops nine of ten probed elements of the full text (`ENV_008`).

| file | what |
|---|---|
| `PROTOCOL.md` | delivered verbatim, the compressed restatement included |
| `envelope_score.py` | the instrument and both tests |
| `domains.json` | T4 pre-registration |
| `protocol_audit.py` | the protocol read against the instrument; every number in the claim table |
| `selftest_env.py` | known answers first, both directions; writes `samples/` |
| `CLAIM_TABLE.md` | `ENV_001..ENV_010` |

Both modules refuse `--selftest`. Renders screen clean through the
repo's `no_severity` with no exemption. No author section. Stdlib only,
parses under 3.9, runs on a phone, CC0.
