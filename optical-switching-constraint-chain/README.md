# optical-switching-constraint-chain

A delivered deep-research report, landed verbatim, plus checks on it.

**Provenance.** `SOURCE_DROP.md` is Kimi output (OKComputer, an open-source
model), uploaded 2026-10-27 as
`OKComputer_All-Optical_Switching_Constraint_Chain.zip` (sha256 `213f13f9…`).
The operator states that material like this is a diagnosis and a set of
things to note from work with other AI systems. It is read that way here:
notes to check, not findings. Nothing in this folder turns a note into a
result.

The report's chain, as it draws it:

```
beam geometry ──► thickness ceiling dissolved (writable N = 1..9)
                        │ price
                        ▼
stripe-domain law ──► escaped by granularity ──► per-grain Bernoulli writing
                        │ price                    (P1 ~ 0.005, ~500 pulses, ~66%)
                        ▼
IFE amplifier ──► plausible for Co/Pt (0.3 T), not FePt (~10 T)
                        │
                        ▼
TERMINAL NODE: energy barrier per optically written bit, Delta = E_B / k_B T
   coherent estimate: well above 60 at 30 nm
   depinning precedent: ~100x lower
   measurement: Sharrock time-dependent coercivity, never done on a written bit
```

The report is not edited. Disagreements go in `check.py`'s output and in
`CLAIM_TABLE.md`. The six PNG figures are not checked in (the repo is
text-only); `FIGURES.md` records them by name, size and sha256.

## Run

    python3 check.py              # recompute the report's derived numbers
    python3 check.py --selftest   # prints its own check count

Stdlib only, parses under 3.9, CC0. Sample output: `samples/check.sample.txt`.

## What holds

- Every stripe-period value in the §3.1 table reproduces from the stated
  Kaplan–Gehring form and parameters (Ms 0.9 MA/m, Keff 0.5 MJ/m³,
  A 15 pJ/m): 2.46×10⁵, 224, 12.5, 2.69, 1.60, 0.751 µm.
- All four Δ = 60 crossing sizes reproduce (2.5, 6.4, 9.6, 12.4 nm).
- The latency arithmetic, the HAMR 2 pJ figure, and the depinning
  conversions (0.95 eV → 36.7 k_BT, 100 eV → 3870 k_BT) reproduce.
- The anchor paper exists as cited: Khalid et al., *Nat. Commun.*,
  15 Sep 2026, DOI 10.1038/s41467-026-77572-3 (search-result depth).
- The report's three corrections to its own source transcript are
  stated as corrections, with the claim and the counter-source side by side.

## What this audit adds (`CLAIM_TABLE.md`, OSC_001..010)

1. **The energy ledger does not follow from its stated inputs (OSC_004).**
   - Fluence × disc spot × pulses gives 34.5, 1815 and 8.2 pJ.
   - The report states 12, 640 and 4.9 pJ, labelled "absorbed".
   - That implies absorbed fractions of 0.35, 0.35 and 0.60.
   - No absorbed fraction is stated anywhere in the report.
2. **The UCSD energy row uses a fluence the report's own table rules out
   (OSC_005).**
   - It uses 7.6 µJ/cm², a value taken from a different single-shot
     experiment.
   - The report's §5 table gives the Co/Pt switching threshold as
     1.9–17 mJ/cm².
   - So the fluence is 250–2,200× below the report's own threshold. If
     it is a µ/m unit slip, the UCSD row is nJ-class, not 12 pJ.
3. **The stripe-law "confirmation" is one bin off and parameter-bound
   (OSC_002, OSC_003).**
   - At the report's own parameters, the period first falls below the
     1.5 µm top of the stated spot band at N = 11 (1.06 µm).
   - The experiment loses deterministic writing at N = 10. The report
     says the crossing happens "precisely" at N = 9–10.
   - Over a modest parameter box, the crossover runs from N = 5 to N = 21.
     The match is a property of the chosen parameters.
4. **GdFeCo limit (OSC_006).** 6 J/cm³ × 40×40×20 nm³ = 192 aJ. The report
   states 120 aJ, carried from Kimel & Li.
5. **"Every configuration sits at Δ = 350–1300" at 30 nm (OSC_007).** This
   holds for the three Co/Pt curves only. The FePt curve plotted in the
   same figure reaches about 8,500.
6. **Δ ≥ 60 versus single-bit survival (OSC_008).**
   - Ten years for one bit needs Δ = ln(t/τ₀) = 40–43.
   - The decision table's "marginal" 40–60 band is therefore where a
     single bit already lasts ten years.
   - The 60 line is a population-and-dispersion criterion, which the
     report notes in §6.1 but not in the table.
7. **Figure numbering (OSC_009).** The text calls the phase map Figure 1,
   but its file is `fig6`. The other five figures are offset by one.

Nothing here measures a barrier, rates a material, or ranks a technology.
