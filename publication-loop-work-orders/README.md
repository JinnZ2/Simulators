# publication-loop-work-orders

Three research work orders delivered as one message on 2026-09-18, landed
verbatim as `WORK_ORDER_11.md`, `WORK_ORDER_12.md`, `WORK_ORDER_13.md`.

**These are study designs, not code builds.** WO-11's own line 3 states the
class and the routing rule verbatim:

> **Class:** research work order (study designs for the publication loop).
> **Not** a code build. Do not route to a build model.

WO-12 and WO-13 repeat "Not a code build." on their own header lines. So
this folder ships **no `.py`, no CONSTRUCTED-data instrument, no
`CLAIM_TABLE.md`** — building one would be exactly the routing the delivery
forbids. It is the `external-audit/` / marker landing genre: the delivered
document is the artifact, landed unedited, and the folder's work is to
carry it and index it.

## What the three are

```
WO-11  Benchmark score as an unpartitioned residual
       Transfers the measurand-partition/ human-population designs
       (WO-1..WO-5) onto the model-evaluation population, where the
       intervening variables (frame, channel, band, training
       composition, control manifest) are directly settable rather
       than inferred. Six arms T-1..T-6; the transfer runs one way
       only and claims nothing about humans.

WO-12  The health-utility anchor: definition-instrument mismatch
       The WHO health definition anchored at 1.00 names peace,
       security and social standing; the EQ-5D operationalises 1.00
       as five items that do not. The gap sits AT the anchor, so it
       scales every score. Three arms G1..G3; the published critique
       runs entirely on the low side and G1 tests the untested high
       side.

WO-13  Introspective access as a training variable, and the
       untouched measurand
       Literature A (no privileged access) sampled an untrained
       population on the reasons-for-behaviour measurand; Literature
       B (training moves accuracy) moved the outcome but never on
       that measurand. Two cells were never run. Two arms G4, G5;
       G4 P1 carries a consent-and-co-authorship condition and
       machine introspection is deliberately NOT an arm.
```

## What each already states about itself

Each work order carries, in its own text, the caveats a landing would
otherwise have to add:

- **Prior-art check UNRUN** on every arm of all three (WO-11 §2, WO-12 §3,
  WO-13 §3). Some arms may exist under vocabulary not searched.
- **Known-bias sections** naming the generating process: WO-11's designs
  were transferred from human-population designs and may import their blind
  spots; WO-11's author is a model writing about model evaluation, and
  whether that fires a same-author condition is left declared-not-resolved;
  WO-12 and WO-13 were generated from a single session's search.
- **Refutation protocols** with per-arm falsifiers; arms retire
  independently.
- **Status tags** OBSERVED / DERIVED / PROPOSED throughout; anything
  PROPOSED is a design offered for test, not a finding.

The literature anchors the orders cite (Kalai, Nachum, Vempala & Zhang,
*Nature* 653:1047-1051 (2026), DOI 10.1038/s41586-026-10549-w, for WO-11
T-6a; the WHO definition and EQ-5D for WO-12; Nisbett & Wilson 1977, Fox et
al. 2012, Baird et al. 2014 for WO-13) are carried as the orders state them
and are not verified here — the egress gate refuses publisher hosts, and in
any case a study design is not a findings document, so nothing rests on a
checked citation.

## Cross-reference

WO-11 is the model-population transfer of `measurand-partition/` (the
five human-population designs WO-1..WO-5 built there on constructed data).
The shared instrument fault is the one `measurand-partition/common.py`
carries as a record shape: an observation made in one setting scored
against an outcome produced by many unmeasured variables, with the whole
residual assigned to the thing observed.

Delivered verbatim. Em dashes and mid dots are the delivered documents'
own; this folder has no ASCII constraint to meet because it ships no code.
CC0.
