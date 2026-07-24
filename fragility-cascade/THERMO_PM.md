# thermo_pm

A project-management engine that reasons from **physics first**: read the
site's fields, synthesize a method from what the land offers, weigh it
against conservation, and close the loop when the structure's purpose ends.

CC0 · stdlib-only · phone-buildable · no dependencies outside this repo

---

## Provenance of this repo

Applying `info_taxonomy` to itself, at entry:

```
mode          model_generated      (drafted in conversation with an LLM)
source        no track record      ← "unknown", not "unreliable"
executed      NO — correct-by-construction only, never run
grounding     the METHOD is operator-supplied (built from a working
              construction practice); the CODE is unverified
```

Run it before trusting it. Every magnitude in every demo is illustrative.

---

## Why physics-first

A catalog-limited planner answers "no crane available" with *no valid plan*.
A physics-first planner asks what produces **lifting force**, and finds that
water's latent heat, copper's melting point, and a lens's concentration
factor close the chain — the crane was never the requirement.

That inversion is the whole design:

```
artifact-first     need lift → select "crane" → needs diesel → BLOCKED
quantity-first     need FORCE → what phenomena make force? → which need
                   only what's on hand? → assemble → name it AFTER
```

---

## Stack

```
thermo_survey.py      READ THE FIELDS   11 domains, ambient gradients;
                                        unread field reported LOUD
        ↓ substances + ambient sources
thermo_synth.py       INVENT THE MOVE   goal = physical quantity;
                                        phenomena from properties;
                                        dimensional-algebra referee
        ↓ operator accepts a proposal → a named process
thermo_pm.py          WEIGH THE BUILD   per-type conservation referee
thermo_explore.py     DRIVE IT          propose · producers · frontier · solve
thermo_interrogate.py FIVE QUESTIONS    land / code / code age / waste / import
thermo_assume.py      COVER IT          assumption-coverage audit +
                                        alternative-source library
thermo_purpose.py     CLOSE THE LOOP    end-of-life return, three gates
thermo_value.py       READ THE CLAIM    token-primary vs substrate-primary
thermo_know.py        KNOWLEDGE         local taxonomy (→ becomes a client
                                        of the info_taxonomy repo)
thermo_spine.py       PROVENANCE        tag() at entry, derive() auto-chains,
                                        weakest-link reports
```

Everything imports downward toward `thermo_pm`.

---

## The five site questions

`thermo_interrogate.py` computes what the method asks on arrival:

```
1  what does the land offer?          site inventory + readings +
                                      buildable-from-site-alone
2  what does the code say?
3  how old is the code?               enacted_year → age
4  what waste comes from not          code-constrained plan MINUS
   aligning with thermodynamics?      physics-optimal plan, both refereed
5  what external energy is required?  consumed @location=external
```

Code provenance (`enacted_year`, `basis`, `intent_met_by`) is **reported
data**. The tool never invents a basis and never rules a code unjustified
on its own.

---

## CLAIM_TABLE

Falsifiable by running. Each claim is a behavioral assertion.

```
ID   LAYER          CLAIM                                  REFUTED BY
──────────────────────────────────────────────────────────────────────────
P1   thermo_pm      no plan passes that violates per-type  a passing plan
                    conservation (out + byproducts ≤ in)   with mass/energy
                                                           conjured
P2   thermo_pm      information inputs gate but are never  a depleted info
                    consumed                               gate after a run
P3   thermo_pm      every output is SOURCED from an input  an unsourced
                    or a declared stock                    output passing
P4   thermo_pm      waste_heat is the energy residual,     waste computed
                    not efficiency × output                from efficiency
S1   thermo_synth   no dimensionally-invalid assembly      a proposal whose
                    reaches the operator                   dims don't close
S2   thermo_synth   material selection is by PROPERTY      selection by name
                    (melting_K > steam_K), never by name   alone
S3   thermo_synth   the synthesizer proposes; it never     auto-execution
                    executes                               of a proposal
V1   thermo_survey  an unsurveyed domain is reported       a silent "nothing
                    UNREAD, never assumed empty            there"
A1   thermo_assume  the audit reports empty dimensions;    an invented
                    it never fills them                    magnitude
U1   thermo_purpose return is judged on three independent  quantity passing
                    gates — quantity, form, timing         standing in for form
U2   thermo_purpose objective is site_delta → 0 against    an unmeasured
                    the shape the site was found in        baseline
L1   thermo_value   token-primary and substrate-primary    a merged single
                    readings are reported separately       "value" number
L2   thermo_value   interior verdicts are named            any output judging
                    OUT_OF_SCOPE, not silently avoided     a person or desire
N1   thermo_spine   a computed result IS an inference —    a derived value
                    derive() builds the chain by the act   with no parents
                    of computing
N2   thermo_spine   a result's groundedness is bounded by  a headline number
                    its least-supported leaf input         hiding an aged leaf
```

### Refutation protocol

```
counterexample found
   → UPDATE THE CLAIM. record the case.
   → do NOT retune the engine to make the claim survive.
```

---

## Boundaries

Held in code, not in discipline:

```
INVENTS NO MAGNITUDES
   every joule, kilogram, threshold, need, and conversion ratio is
   operator-supplied. physical constants are physics. anything else
   is reported as unverified.

PROPOSES, NEVER EXECUTES
   thermo_synth hands assemblies to a human. a dimensionally-valid
   chain is not yet a feasible one — it self-flags as such.

NAMES ITS OWN INCOMPLETENESS
   thermo_assume flags only dimensions someone thought to encode.
   it is a growing checklist, never a complete one, and says so.

NO INTERIOR VERDICTS
   thermo_value.OUT_OF_SCOPE is a named constant. structure, ripples,
   and discrepancies are observable. what a desire means to a person
   is not, and is not output.
```

---

## Seeded vs supplied

```
SEEDS — drafted by an LLM, awaiting re-cut
   LIBRARY (thermo_synth)     9 phenomena. extend with the physics moves
                              that actually run in your head on a site.
   DOMAINS (thermo_survey)    11 fields.
   MODES (thermo_know)        9 acquisition modes. → migrating to the
                              info_taxonomy repo.
   fragility policy           what counts as a "weak link" in
   (thermo_spine)             thermo_spine.backing() is a policy knob.
   DEFAULT_CONVERSIONS        burn ratios in thermo_purpose.
   every demo magnitude       illustrative only.

SUPPLIED BY DESIGN — never seeded
   site readings · needs read at return time · code basis and enacted year ·
   conversion ratios from real materials · design life · every threshold.
```

---

## Related repos

```
info_taxonomy         the general parent of thermo_know / thermo_spine.
                      this stack becomes a client; the local copies
                      should be deleted once it imports.
assumption_validator  general-purpose. thermo_assume is NOT a duplicate —
                      it is the project-management-specific instance.
```

---

## Status

```
ten files cohere and import cleanly by construction.
NONE have been executed. first run is the first independent mode.
open: wiring tag()/derive() through the eight upstream files
      (one line per entry point, deliberately left for the repo
       so nothing running is broken by a bulk rewrite).
```

---

## License

CC0 1.0 Universal. Public domain. No attribution required.
