# WORK ORDER 12 — delivered verbatim

Delivered 2026-09-18 as one message with WO-11 and WO-13. Landed unedited
below this line. Research work order (study designs for the publication
loop), NOT a code build; see `README.md`.

---

# WORK ORDER 12 — The health-utility anchor: definition–instrument mismatch

**Class:** research work order (study designs for the publication loop). Not a code build.
**Issued:** 2026-09-18 · **License:** CC0-1.0
**Source object:** `qol-anchor-definition-instrument-mismatch`
**Arms:** G1, G2, G3

Status tags: `OBSERVED` read off a source · `DERIVED` follows from two or more · `PROPOSED` offered for test.

---

## 0. The documented mismatch this work order rests on

`OBSERVED`. The WHO definition of the state anchored at 1.00 is *"a state of complete physical, mental and social well-being and not merely the absence of disease or infirmity"* — a definition that incorporates peace, security, and societal dangers. Quoted inside the health-economics literature itself (JHEOR).

`OBSERVED`. The EQ-5D operationalises 1.00 as five items: mobility, self-care, usual activities, pain/discomfort, anxiety/depression. Peace, security and societal danger are not items.

`DERIVED`. The mismatch sits **at the anchor**, and every other score on the scale is a fraction of it. A definition–instrument gap anywhere else scales one score; a gap at the anchor scales all of them.

`OBSERVED`. The published critique literature runs **entirely on the low side**: states worse than dead, ableist scoring, discrimination by age/race/disability, generic-instrument insensitivity, "the math doesn't work." Every arm argues the scale **under-values** people.

`OBSERVED`. Two prohibitions sit in the same field, unjoined:
- **No-decrement rule** (HRQL evidentiary standard): improvement is not demonstrated if any domain declined.
- **Compensation critique** (Quality of Life Research 2020, statistical): sum scores imply a gain in one domain compensates a deficit in another.

`OBSERVED`. The anchor-inequality problem is already named in print — *"What if 0 is not equal to 0?"* (European Journal of Health Economics) — on the ground that equating the dead-to-full-health distance across people ignores that interpersonal utility comparisons are forbidden, or at least problematic, in economics.

---

## G1 — The high-side boundary test

**The gap.** `DERIVED`. No test found of the instrument returning a score that is **too high** — a case scoring at or near 1.00 that the WHO definition would not call perfect health. The low-side critique is mature; the high side is unrun. An instrument tested from one side only has a characterised error in one direction and an uncharacterised one in the other.

**Design.**

```
CONSTRUCT a set of vignettes describing people
whose EQ-5D profile is 11111 (no problems on
any dimension) and whose circumstances differ
on the WHO-named terms absent from the
instrument:

  V1  baseline: no problems, ordinary life
  V2  no problems, incarcerated
  V3  no problems, active conflict zone
  V4  no problems, coercive labour
  V5  no problems, no security of person
  V6  no problems, stateless / no legal standing

ADMINISTER, three arms:
  A  score each vignette on EQ-5D as written
     PREDICTION: all return 11111, utility 1.00
  B  ask raters: is this person in
     "complete physical, mental and social
     well-being"? (the WHO wording, unattributed)
  C  ask raters to place each vignette on a
     dead-to-perfect-health VAS

MEASURE the divergence between A and B,
and between A and C.
```

**What the arms separate.** Arm A measures the instrument. Arm B measures the definition. Arm C measures whether raters spontaneously apply the absent terms when the scale is open rather than itemised. `DERIVED`

**Predicted result, sign stated in advance.** `PROPOSED` — A returns 1.00 across V2–V6; B and C do not. The size of the B−A and C−A gaps is the quantity of interest, and it is an estimate of how much of the WHO anchor the instrument does not carry.

**Falsifier.** If B and C also return perfect-health readings for V2–V6, the WHO definition's extra terms are not operative for raters either, and the mismatch is in the definition's wording rather than in the instrument. That is a different finding and G1 retires as stated.

**Cost.** Vignette study. No patient recruitment, no clinical access. `DERIVED` — this is the cheapest arm in the work order.

**Ethical note.** V2–V6 are constructed vignettes describing circumstances, rated by third parties. No person in those circumstances is being scored or recruited.

---

## G2 — Join the compensation critique to the no-decrement rule

**The gap.** `DERIVED`. The two prohibitions above are the **same prohibition stated at two levels** — one about information loss in aggregation, one about what counts as evidence of benefit — and the literatures do not cite each other. The statistical arm treats it as a modelling choice; the regulatory arm treats it as an evidentiary standard.

**The consequence that makes it worth running.** `DERIVED`. The same patient state can return **demonstrated improvement** under a utility measure and **not demonstrated** under the HRQL no-decrement rule, with no stated procedure for which governs.

**Design, two stages.**

```
G2a  CITATION TRACE
     Do papers invoking the no-decrement rule
     cite the compensation/aggregation
     literature, and vice versa?
     Code a sample on:
       - which rule is invoked
       - whether the other is cited
       - whether the conflict is named

G2b  DIVERGENCE RATE ON REAL TRIALS
     Take published trials reporting BOTH a
     preference-based utility change AND
     domain-level profile data.
     For each:
       U_verdict = improvement by utility change
       P_verdict = improvement by no-decrement
     COUNT disagreements.
     Report the rate, and the DIRECTION —
     which rule is more permissive, and by
     how much.
```

**Required output.** A disagreement rate with a direction, not a recommendation about which rule is right. `DERIVED` — both rules are defensible on their own terms; the finding is that a trial's verdict depends on an undeclared choice between them.

**Falsifier.** If the two verdicts agree in nearly all cases, the conflict is formal rather than operative and G2 retires to a footnote.

**Access.** G2a needs literature only. G2b needs trials publishing both quantities — a constraint that may itself be the finding, since a trial reporting only the utility change cannot be checked against the other rule at all.

---

## G3 — The frame question at the anchor, not at the items

**The gap.** `DERIVED`. Value sets are built by asking populations to rate EQ-5D **state descriptions**. If security, peace and social standing are absent from the description, each respondent supplies their own assumption about them. That assumption is unmeasured, and there is no reason to expect it constant across populations.

**Why this is not the standard cross-cultural value-set question.** `DERIVED`. Existing work compares value sets across countries and reports that weights differ. It treats the difference as variation in *preferences over the described states*. This arm asks whether respondents are rating **the same state at all** — because the unstated terms are being filled in privately, the described state is underdetermined, and two respondents may be valuing two different things while appearing to disagree about one.

**Design.**

```
G3a  ELICIT THE FILL-IN
     Give respondents an EQ-5D state description.
     BEFORE asking for a valuation, ask:
       "What else do you assume is true about
        this person's situation?"
     Free response. Code for:
       security / safety
       social standing, family position
       economic circumstance
       legal standing
       anything else supplied unprompted
     Report the fill-in distribution.

G3b  SPECIFY AND RE-ELICIT
     Same state descriptions, now with the
     absent terms EXPLICITLY SPECIFIED
     (secure / insecure, etc.).
     Re-elicit valuations.
     MEASURE: how much of the between-respondent
     valuation variance closes when the
     assumption is supplied rather than filled in.

G3c  ACROSS POPULATIONS
     Run G3a in populations with different
     baseline security conditions.
     PREDICTION, PROPOSED: the fill-in
     distribution differs, and differs in a way
     that tracks the respondent's own baseline
     rather than the described state.
```

**Why the time-trade-off method is the sharp case.** `OBSERVED` — TTO asks how many years of diseased life a respondent would sacrifice for perfect health. The sacrifice is priced against *perfect health as the respondent imagines it*, which is precisely the underdetermined anchor. `DERIVED` — so the anchor problem enters TTO twice: once in the state being valued, once in the target being traded toward.

**Falsifier.** If G3a returns few or no spontaneous fill-ins, respondents are rating the description as given, the anchor is not being privately completed, and G3 retires.

**Connects to the in-print anchor critique.** The "What if 0 is not equal to 0?" argument runs on the **lower** anchor and treats the problem as statistical (interpersonal comparison). G3 runs on the **upper** anchor and treats it as underspecification of the stimulus. Different anchors, different mechanisms; the in-print arm does not cover this one. `DERIVED`

---

## 1. Ranking

| Arm | Data needed | Access | Runnable now |
|---|---|---|---|
| G1 | Constructed vignettes | Rater panel | Yes |
| G2a | Published literature | None | Yes |
| G2b | Trials reporting both quantities | None (published) | Yes, if such trials exist |
| G3a | Respondent panel | Panel recruitment | Yes |
| G3b | Same panel, second wave | Panel | Yes |
| G3c | Panels in ≥2 baseline conditions | Multi-site | Harder |

**Cheapest decisive: G2a.** Pure citation coding, no recruitment, and it settles whether the two literatures are genuinely unjoined or whether the join exists under vocabulary not searched. If the join exists, G2b is unnecessary and G2 retires at low cost.

**Highest information per unit cost: G1.** Vignette study, no patients, and it tests the one side of the instrument that has never been tested.

---

## 2. What this work order does not claim

- It does not claim the QALY framework should be abandoned, replaced, or de-funded. No arm here produces a policy result.
- It does not claim the scale prices lives by wealth. `OBSERVED` — the scale is blind to wealth in both directions; a wealthy person and a poor person in the same body score the same. That feature reads as the equity claim and as the validity problem, and this work order does not adjudicate between those readings.
- The utility scale is **dimensionless**, not currency. `OBSERVED`. Money enters one step later, as cost-per-QALY against a payer threshold. Nothing here treats the scale itself as a price.
- The disability-deprioritization critique — a permanently sub-1.00 score yields fewer QALYs per unit spend, by construction — is `OBSERVED`, old, and unresolved. It is not an arm of this work order and is not restated as a finding.

---

## 3. Known bias

`DERIVED`, stated so it is not rediscovered:

- Three arms were generated from a documented mismatch found in a single session's search. The prior-art check is **unrun** for all three. Health economics is a large literature; some of this may exist under vocabulary not searched.
- G1's vignette set is constructed by the author of the work order. A vignette set that makes the predicted result easy to obtain is a manufactured finding. Recommend a second author, blind to the prediction, constructs or vets the vignettes before any run.

---

## 4. Refutation protocol

Retired in whole if:

- the WHO anchor definition and the EQ-5D operationalisation are shown to be intentionally and explicitly scoped to different constructs by the instrument's own documentation, **with that scope stated where the instrument is used** rather than only in methodological commentary; or
- a published study is found running the high-side boundary test (G1) and reporting no divergence.

Arms retire independently on the falsifiers stated in each section.

