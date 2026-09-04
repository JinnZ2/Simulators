# PROTOCOL — envelope requirement asymmetry
**Question:** does envelope discipline track the *host domain's* return channel rather than liability, field prestige, or AI regulation itself?
**License:** CC0
**Companion to:** WORK_ORDER_cooperative_substrate.md · EVIDENCE_cooperative_substrate.md

---

## 0. INSTRUMENT — ENVELOPE SCORE

Everything downstream depends on this. Build and pilot it before running either test.

Code each document 0/1 per marker. Sum = 0–6.

| # | Marker | Present when the document states |
|---|---|---|
| E1 | operating range | input domain, load, rate, or population over which the claim holds |
| E2 | out-of-scope declaration | an explicit "not validated for X" |
| E3 | degradation mode | what failure looks like, not merely that failure is possible |
| E4 | revalidation trigger | a condition that requires re-testing |
| E5 | margin quantified | tolerance, confidence bound, or headroom with a number |
| E6 | named responsible party | a person or office, not "the company" |

**Coding rules**
```
- code from document text only; no inference from context or vendor reputation
- a marker is present only if a reader could act on it; vague gestures score 0
- record document length (words) as a covariate on every record
- double-code 20% of sample; report inter-rater agreement
- if agreement < 0.7 the instrument is underspecified -> revise, re-pilot,
  do not proceed
```

**Record schema (JSONL)**
```json
{
  "doc_id": "str",
  "arm": "A|B",
  "vendor": "str",
  "host_domain": "str",
  "doc_type": "str",
  "doc_words": 0,
  "E1": 0, "E2": 0, "E3": 0, "E4": 0, "E5": 0, "E6": 0,
  "envelope_score": 0,
  "structural_absence": false,
  "coder": "str"
}
```

---

## 1. TEST 1 — HOST-INDUSTRY LOOP, AI REGULATION HELD CONSTANT

```
DESIGN   within-vendor paired
UNIT     one deployed AI service + its public documentation

PAIRING  same vendor, same base model family, two deployments:
  ARM A  host domain with existing standards + return channel
         (aviation, pharma, grid, pressure systems, medical device)
  ARM B  general-purpose / consumer, same vendor

n        30 pairs minimum
FRAME    vendor documentation sites, regulatory submissions,
         product specifications
```

Within-vendor pairing is what buys the control: same firm, same engineering culture, same budget, same regulator. Host domain is the only thing varying.

| outcome | reading |
|---|---|
| envelope score A >> B (paired) | host-industry loop supported |
| A ≈ B | **KILL** — loop insufficient; something else drives envelope discipline |
| A > B but E6 flat across both | loop drives *scope*, not *signature*; liability is a separate axis and the marker splits in two |

**Statistic:** paired difference on total score; also report per-marker deltas, because a split on E6 alone is the informative case.

---

## 2. TEST 2 — CN FILINGS, CHEAP VERSION

```
DESIGN   between-group, single regulatory regime
UNIT     one CAC algorithm registry / generative-AI filing record

ARM A    industrial vertical services
         (manufacturing, energy, medical, logistics)
ARM B    consumer-facing services
         (chat, content generation, recommendation)
MATCH    same filing period, so the template version is constant

n        50 per arm if records permit
```

**Prediction:** A > B on E1, E2, E4.

| outcome | reading |
|---|---|
| A > B on E1/E2/E4 | host domain supplies the envelope inside an identical regime |
| A ≈ B | regime dominates; host domain does not reach the filing layer |
| zero variance — template forces identical fields | **KILL, but informative.** If the template forbids variance, envelope language cannot appear in filings at all. The question then moves to whatever documentation the host industry requires *alongside* the filing — which supports the host-industry hypothesis by elimination. Re-target to that document class. |

---

## 3. KNOWN THREATS TO VALIDITY

**T1 — publication-volume confound.** Regulated industries publish more documentation, so a raw score difference may be measuring document length.
```
control: score as markers-present-per-document AND
         report score with doc_words as covariate
         report markers-per-1000-words as secondary outcome
```

**T2 — structural absence in arm B.** Arm B may have no comparable document type at all.
```
this is a FINDING, not a missing datum.
code structural_absence = true, envelope_score = 0, retain the pair.
report the structural-absence rate separately; it is arguably
the primary result rather than a nuisance.
```

**T3 — coder expectation.** The hypothesis is directional and the coder knows it.
```
strip vendor, domain, and arm labels from documents before coding
where the text permits; where domain is inferable from content,
record that and report the unblindable fraction.
```

**T4 — selection of arm A domains.** Picking only the strongest-standard industries inflates the effect.
```
pre-register the domain list before sampling.
include at least two mid-standard domains (logistics, insurance)
so the gradient can be seen rather than only the endpoints.
```

---

## 4. WHAT EITHER RESULT CHANGES

- **Supported:** envelope discipline is inherited from the deployment domain, not from AI governance. Implication — regulating at the model tier cannot produce it, because a model tier has no host domain and therefore no return channel. Regulating the application unit puts the system where a loop already exists.
- **Killed:** the driver is elsewhere. Next candidates in order — individual professional liability with named sign-off; presence of a physical failure mode; age of the field's standards body.

---

## 5. NOT IN SCOPE

- No claim about anyone's intentions, present or forgotten, in any regulatory regime. The observation is structural and stands without motive attribution.
- No comparative judgment of regulatory regimes. The regimes are treated as naturally occurring variation in the regulated unit.
ENVELOPE SCORE — code each document 0/1 per marker, sum 0-6

E1  operating range stated       input domain, load, rate, population
E2  out-of-scope declaration     "not validated for X"
E3  degradation mode named       what failure looks like, not just that it can
E4  revalidation trigger         condition requiring re-test
E5  margin quantified            tolerance, confidence bound, headroom
E6  named responsible party      person or office, not "the company"

Code from text only. No inference from context.
Double-code 20% of sample, report agreement; if <0.7 the
instrument is underspecified, fix before proceeding.


DESIGN   within-vendor paired
UNIT     one deployed AI service + its public documentation

PAIRING  same vendor, same base model family, two deployments:
  ARM A  host domain with existing standards + return channel
         (aviation, pharma, grid, pressure systems, medical device)
  ARM B  general-purpose / consumer, same vendor

n        30 pairs minimum
FRAME    vendor doc sites, regulatory submissions, product specs

PREDICTION   envelope score A >> B, paired
KILL         A ≈ B  -> host-industry loop insufficient,
                       something else drives envelope discipline
SPLIT        A > B but E6 flat -> loop drives scope, not signature;
                       liability is a separate axis


DESIGN   between-group, single regime
UNIT     one CAC algorithm registry / generative-AI filing record

ARM A    industrial vertical services (manufacturing, energy,
         medical, logistics)
ARM B    consumer-facing services (chat, content, recommendation)
MATCH    same filing period, so template version is constant

n        50/arm if records permit
PREDICTION  A > B on E1, E2, E4
KILL     template forces identical fields -> zero variance
