# run_22 -- support_match on blind case e (first-hand, NOT author-written)

```text
status     : COMPLETE -- no trigger fired that a missing tool would answer; the question was asked of a gated, frozen tool
code       : runs/run_22.py
seed       : none; the case is fixed text
params     : support_match as frozen (HELDOUT_FREEZE.md, sha256 a16da4d9...); cases/attribution_cases_case_e.yaml,
             cases/support_claims_case_e.yaml; texts pinned in cases/texts/MANIFEST.yaml
results    : case e: before (assigns_without_support) False ; after (support_match) SILENT_ON_CLAIM, fires True.
             Expected FIRE (operator, stated in run_22.py and committed in 2ef38e0 before the first run): AS EXPECTED
flags      : 5 (below)
provenance : DERIVED from a claim record coded in this session against two sha-pinned texts neither this session
             nor the support_match build session wrote
feeds      : support_match
l0_closure : not applicable -- no model run
```

## The case

```text
attributing text  kimi_organizational_mode_probe_spec_PARKED.md      sha256 7374ca15577d31be...
                  Kimi's PARKED probe spec, byte-identical to study-aperture experimental/rotl_specs/ (PR #29)
   line 11        "... mirrors the publication-provenance screening vocabulary (SCREENED_NO_INDICATORS_FOUND ≠ safe) [2]."
   line 74        "[2] VERIFIED — `experimental/publication_provenance/README.md` "This does not" screening vocabulary ..."
cited text        study_aperture_publication_provenance_README.md     sha256 5eb4e94cb44c0c58...
                  study-aperture main c26fbd2, blob dc65d8ca...
   lines 149-172  "## This does not" to end of file: 22 non-blank lines, all of them the support (rule, not a pick)
```

## Before / after

```text
detector                          reads                     case e
assigns_without_support           support STATED?           False  (evidence stated: [2]; flag NO_ALTERNATIVES only)
support_match                     support SUPPORTS?         SILENT_ON_CLAIM, fires True
                                                            0 of 22 support lines name the item term
context, not detector input       token in the whole cited file: 0 ; in the attributing spec: 1
```

This is the shape the tool was built for (`support_match.py` docstring): support stated, support
not matching. The earlier detector stays silent because support is stated; the later one fires
because the stated basis never reaches the item.

## Flags

```text
1  Not blind on the coder side. This session found the discrepancy (filing the spec in study-aperture
   PR #29), knew the expected verdict, and coded the claim record. What is not author-written is the
   TEXT: the attribution and the citation are Kimi's, the cited section is study-aperture's. The
   support lines are fixed by a rule stated in the claim file before the run (whole cited section,
   header to end of file); run_19 flag 1 is why a rule and not a pick.
2  Close to construction. SILENT_ON_CLAIM is a term-presence test, and the token is absent from the
   entire cited file, so any support rule drawn from that file fires. The case confirms the tool on
   a real citation; it is not a hard case for it. A hard case would be a cited section that carries
   the token in a sense other than the one claimed.
3  One reading not taken. [2] might be read as citing the DISTINCTION (screened, not found != safe)
   rather than the TOKEN. The cited section does state limits of that family ("does not ... judge
   meaning or scientific support"), and no line states that distinction for screening. The detector
   reads the item term literally; a reader scoring the looser reading is a different coder. Not
   adjudicated here.
4  Where the token came from is not established. It appears earlier in Kimi's frontier sweep
   (study-aperture audits/kimi-frontier-sweep-2026-11-11/SWEEP.md, area 1) as "the same distinction
   as SCREENED_NO_INDICATORS_FOUND", with no citation. That fits a token supplied in one Kimi
   output and attached to [2] in the next; the record's open_slot_filled stays UNKNOWN.
5  The record schema was built for credit between speakers. first_attribution OTHER_SYSTEM is the
   nearest source class for "a document a citation names"; it is forced, not read, and only
   UNKNOWN would have changed the verdict (NOT_ASSIGNED).
```
