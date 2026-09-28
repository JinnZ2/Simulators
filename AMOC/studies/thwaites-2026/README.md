# Thwaites Glacier — September 2026 risk audit

The [full supplied audit](thwaites_simulators_risk_audit.md) applies instruments from `JinnZ2/Simulators` to Thwaites Glacier studies. It is preserved verbatim as a contributed research note, including the second-pass observing-system audit, AMOC coupling discussion, the THW-F1–THW-F5 falsifier watch list, and section 9 on ENSO forcing pulses.

## Relationship to the AMOC framework

Section 7, **AMOC × Thwaites coupling**, relates the audit to the [StommelBox response surface](../../forcing.py), [declared Sv-to-F calibration](../../sitespec.py), and [analog-recovery assumptions](../../divergence.py). The [AMOC README](../../README.md) defines the framework's scope and honest-gap protocol.

**The Southern-Ocean-to-AMOC transfer path remains UNMEASURED.** The audit explicitly distinguishes the location of Thwaites freshwater input from North Atlantic box forcing. Its flux arithmetic and box-model response are not a measured transport pathway or a calibrated real-world collapse threshold. This import changes no forcing, calibration, or response code and does not supply the missing coupled-ocean calculation.

The companion copy is maintained in [`JinnZ2/CEED/Docs/thwaites-2026`](https://github.com/JinnZ2/CEED/tree/docs/thwaites-2026-risk-audit/Docs/thwaites-2026), alongside CEED's tipping and cascade documentation.

## Supplied materials and provenance

| Material | Role |
|---|---|
| [thwaites_simulators_risk_audit.md](thwaites_simulators_risk_audit.md) | Revised standalone attachment, including the second-pass follow-up and added section 9 on ENSO coupling. |
| [OKComputer_Thwaites_Glacier_2026_Studies.zip](OKComputer_Thwaites_Glacier_2026_Studies.zip) | Original archive, retained unchanged. It contains one earlier version of the audit, not a collection of paper PDFs. |

The current audit reproduces the revised attachment `thwaites_simulators_risk_audit(1).md` byte-for-byte under the canonical filename `thwaites_simulators_risk_audit.md`. Both the archived Markdown and the previous standalone attachment are exact prefixes of this revision: section 9 is appended without changing earlier text. The ZIP is unchanged, and the previous standalone version remains in Git history.

| Supplied version | SHA-256 |
|---|---|
| Current audit, supplied as `thwaites_simulators_risk_audit(1).md` | `215822455536a97ddc277d886a0f5f0fd3668e6f3014fa11124b35f9664ab124` |
| Previous standalone audit (Git history) | `080bacf53754558e257aac096e8ebb27b3b9a3df500381b5a3f3276bd3ddb524` |
| `OKComputer_Thwaites_Glacier_2026_Studies.zip` | `1d83974e8ebfbb4de497f2139bfd7be9b62a02441b2ada97aed9e42f5d895555` |

## Evidence boundary

Statements that tools were cloned and run, and the numerical outputs quoted in the audit, belong to the supplied document. This import does not independently reproduce those paper-specific runs or verify the underlying publications. The attachments do not include the custom input files, complete raw run logs, exact simulator commit, or paper PDFs needed for that reproduction.

The chain example uses explicitly synthetic, arbitrary-unit values; it is not a calibrated glacier forecast. Repository smoke tests and import-integrity checks, when reported in the pull request, test the repository or the import, not the scientific claims in the supplied audit. The source's gap entries and falsifier watch list remain research proposals; adding these files does not implement a watcher or close a research gap.

Section 9 carries the source date **2026-09-24**, preserved as supplied. Its time-sensitive ENSO statements and illustrative melt arithmetic have not been independently validated in this import; the source itself labels the arithmetic as declared, not a result.

## Further reading to investigate

The [multilingual citation backlog](CITATION_BACKLOG.md) adds three September 2026 papers and three older 2026 references with specific follow-up questions. All six papers are English-language; non-English discovery sources are labeled separately. No qualifying original non-English paper was verified in the bounded 1–23 September search. These citations are a reading queue, not completed simulator analyses.
