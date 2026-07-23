# info_taxonomy

A generalized taxonomy for information: **what is claimed**, **how it was
gotten**, **who supplied it**, and **how well it is supported** — computed,
not asserted.

CC0 · stdlib-only · phone-buildable · single file

---

## Provenance of this repo

Applying the framework to itself, at entry:

```
mode          model_generated      (drafted in conversation with an LLM)
source        no track record      ← "unknown", not "unreliable"
support       1 mode, 0 independent corroboration
executed      NO — correct-by-construction only, never run
staleness     n/a (2026)
```

Under this repo's own audit, that reads: **uncorroborated model output —
ground it.** Running it is the first independent mode. Do that before
trusting any claim below.

---

## The gap this fills

Each existing system holds one axis and drops the rest.

```
system            holds                        drops
────────────────────────────────────────────────────────────────────────
epistemology      the modes (perception,       operations — no decay,
                  testimony, inference...)     no freshness, no audit
GRADE / evidence  operational scoring          ranks modes into a fixed
pyramids                                       ladder (mode supremacy)
Admiralty code    two-axis grading             grades the source, not the
(NATO)            (source × credibility)       mode's structural blindness
W3C PROV          derivation chains            content-neutral — records
                                               THAT, carries no theory
library science   faceted categorization       acquisition, support
evidence law      independence rule            lives in doctrine, not code
```

None unify them. This does.

---

## Six commitments

```
1  faceted type, not a tree          content × form × open domain tags
2  modes carry blindness as DATA     every row states what it CANNOT read
3  two grades, never multiplied      source track-record ≠ claim support
4  support = independent modes only  same-mode agreement is echo, weight 0
5  staleness computed per mode       half-life, not assumed
6  chains PROV-compatible            to_prov() exports for free
```

---

## CLAIM_TABLE

Falsifiable by running. Each claim is a behavioral assertion about the code.

```
ID   CLAIM                                                    REFUTED BY
──────────────────────────────────────────────────────────────────────────
C1   same-mode agreement never raises support strength        a case where
                                                              strength rises
                                                              on an echo
C2   a mode cannot register without stating reads_well,       a registered
     blind_to, decays_by, stays_fresh_by                      mode missing one
C3   staleness is computed from mode half-life + item year,   a staleness flag
     never asserted per-item                                  with no half-life
C4   no ordering function exists over MODES — no mode         any code path
     outranks another                                         ranking modes
C5   contradictions are surfaced, never auto-resolved         an item silently
                                                              dropped/downweighted
C6   every derivation emits a PROV edge; broken chains are    a missing parent
     named, not skipped                                       passing silently
C7   source reliability and claim support are never combined  a single merged
     into one number                                          credibility score
C8   absent track record reads "unknown", never "unreliable"  None treated as 0
C9   the audit reports structure only — traceability,         any truth verdict
     independence, freshness — never truth                    in output
```

### Refutation protocol

```
counterexample found
   → UPDATE THE CLAIM. record the case.
   → do NOT retune the structure to make the claim survive.
a claim that needed the code bent to stay true was the wrong claim.
```

---

## Shape

```python
from info_taxonomy import Corpus, Item, Source, Mode, register_mode

c = Corpus(current_year=2026)
c.add_source(Source("operator", "person", track=[True, True, True]))

c.add(Item("soil.bearing", "ground holds 80k lb rig without rutting",
           content="measurement", form="embodied", about=["soil"],
           mode="direct_observation", source="operator", year=2026,
           corroborates=["soil.penetrometer"]))

c.support("soil.bearing")     # independent modes, echoes, contradictions
c.staleness("code.rule")      # per-mode half-life, or None
c.backing("plan.waste")       # transitive mode census at the leaves
c.audit()                     # structure flags only
c.to_prov()                   # PROV-JSON-shaped export
```

---

## Axes

```
TYPE     content: observation · measurement · claim · rule · procedure ·
                  model_output · story · teaching · record
         form:    numeric · text · oral · embodied · instrument_trace ·
                  drawing · artifact
         about:   open vocabulary, uncontrolled on purpose

MODE     each row: reads_well / blind_to / decays_by / stays_fresh_by
         direct_observation · repeated_practice · experiment · instrument ·
         transmission · inference · authority · model_generated ·
         measured_constant
         → extend with register_mode(). the table is meant to be re-cut.

SOURCE   who/what supplied it. graded on track record, separately.
LINKS    corroborates · contradicts · derived_from (PROV) · chain (lineage)
```

---

## Seeded vs supplied

Marked so no one inherits a draft default as a finding.

```
SEEDS — placeholder, awaiting re-cut
   MODES            9 rows. drafted by an LLM against Western analytic
                    epistemology. cultures cut acquisition differently —
                    ceremony, dreaming, land-reading, kinship-with-place
                    have no rows here. that is a gap, not an absence.
   half_life_yr     2 rows carry numbers. the STRUCTURE (decay per mode)
                    is the contribution; the numbers are placeholders.
   FACETS           content/form vocabularies. extend freely.

SUPPLIED BY DESIGN — never seeded, never guessed
   every item, every source, every track record, every year.
```

---

## Out of scope

By construction, not by omission:

```
- whether a claim is TRUE            (this grades support, not truth)
- whether a knower is honest         (grades track record, not character)
- whether a mode is superior         (no ordering exists)
- what a claim means to a person     (interior; not observable from here)
```

---

## License

CC0 1.0 Universal. Public domain. No attribution required.
