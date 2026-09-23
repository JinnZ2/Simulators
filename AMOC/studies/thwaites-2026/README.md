# Thwaites Glacier — September 2026 risk audit

The [full supplied audit](thwaites_simulators_risk_audit.md) applies instruments from `JinnZ2/Simulators` to Thwaites Glacier studies. It is preserved verbatim as a contributed research note, including the second-pass observing-system audit, AMOC coupling discussion, and THW-F1–THW-F5 falsifier watch list.

## Relationship to the AMOC framework

Section 7, **AMOC × Thwaites coupling**, relates the audit to the [StommelBox response surface](../../forcing.py), [declared Sv-to-F calibration](../../sitespec.py), and [analog-recovery assumptions](../../divergence.py). The [AMOC README](../../README.md) defines the framework's scope and honest-gap protocol.

**The Southern-Ocean-to-AMOC transfer path remains UNMEASURED.** The audit explicitly distinguishes the location of Thwaites freshwater input from North Atlantic box forcing. Its flux arithmetic and box-model response are not a measured transport pathway or a calibrated real-world collapse threshold. This import changes no forcing, calibration, or response code and does not supply the missing coupled-ocean calculation.

The companion copy is maintained in [`JinnZ2/CEED/Docs/thwaites-2026`](https://github.com/JinnZ2/CEED/tree/docs/thwaites-2026-risk-audit/Docs/thwaites-2026), alongside CEED's tipping and cascade documentation.

## Supplied materials and provenance

| Material | Role |
|---|---|
| [thwaites_simulators_risk_audit.md](thwaites_simulators_risk_audit.md) | Complete standalone attachment, including the second-pass follow-up dated 2026-09-23. |
| [OKComputer_Thwaites_Glacier_2026_Studies.zip](OKComputer_Thwaites_Glacier_2026_Studies.zip) | Original archive, retained unchanged. It contains one earlier version of the audit, not a collection of paper PDFs. |

The archived Markdown is an exact prefix of the standalone audit. The standalone file appends the follow-up wave; no earlier text was replaced. Both original attachments are retained so that their different contents remain traceable.

| Original attachment | SHA-256 |
|---|---|
| `thwaites_simulators_risk_audit.md` | `080bacf53754558e257aac096e8ebb27b3b9a3df500381b5a3f3276bd3ddb524` |
| `OKComputer_Thwaites_Glacier_2026_Studies.zip` | `1d83974e8ebfbb4de497f2139bfd7be9b62a02441b2ada97aed9e42f5d895555` |

## Evidence boundary

Statements that tools were cloned and run, and the numerical outputs quoted in the audit, belong to the supplied document. This import does not independently reproduce those paper-specific runs or verify the underlying publications. The attachments do not include the custom input files, complete raw run logs, exact simulator commit, or paper PDFs needed for that reproduction.

The chain example uses explicitly synthetic, arbitrary-unit values; it is not a calibrated glacier forecast. Repository smoke tests and import-integrity checks, when reported in the pull request, test the repository or the import, not the scientific claims in the supplied audit. The source's gap entries and falsifier watch list remain research proposals; adding these files does not implement a watcher or close a research gap.
