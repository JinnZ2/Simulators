```markdown
# Study Paths — Research Projects in the Simulation Hypothesis Budget

Every gap in this folder is a **research project**. Each one is scoped to a semester, a summer, or a few weeks of focused work.

---

## Project 1: Area‑law vs. Volume‑law Entanglement

**Gap:** The quantum line in the scaling classes is about worst‑case entanglement. The ratio of area‑law to volume‑law matter in the universe is unknown.

**Discipline:** Quantum physics / condensed matter

**Time estimate:** 1 semester

**Prerequisites:** Undergraduate quantum mechanics, some exposure to quantum information

**What to do:**
1. Review the literature on area‑law vs. volume‑law entanglement in many‑body systems
2. Identify which classes of physical systems (materials, fields, cosmological structures) fall into each category
3. Estimate the fraction of mass/energy in the universe that is in each entanglement regime
4. Compute the simulation cost under both scenarios
5. Write a report with your estimate and its uncertainty

**What success looks like:** A defensible estimate of the area‑law / volume‑law fraction in the observable universe, with a sensitivity analysis showing how the simulation cost depends on it.

**What falsifies it:** Finding that all matter is in one regime (area‑law or volume‑law) — which would simplify the cost calculation dramatically.

---

## Project 2: Lazy‑Consistency Cost Lower Bound

**Gap:** `consistency_cost()` returns `UNMEASURED` and refuses to estimate. No one knows how to bound the cost of making a lazy‑evaluation simulation internally consistent.

**Discipline:** Computer science / computational complexity

**Time estimate:** 1 semester

**Prerequisites:** Algorithms, some complexity theory

**What to do:**
1. Define the problem formally: what is the minimal computation required to ensure that a lazily‑rendered observation is consistent with all other observations?
2. Derive a lower bound (or prove that no finite bound exists)
3. Implement a version of `consistency_cost()` that returns a bound (or raises an exception with a proof)
4. Write a report with your derivation and implementation

**What success looks like:** A formal lower bound on the consistency cost, implemented in code.

**What falsifies it:** Finding that the consistency cost is zero (i.e., lazy evaluation is trivially consistent) — which would mean the gap is not real.

---

## Project 3: SHB‑013 Falsifier Repair

**Gap:** `SHB‑013` was refuted by the repository's own audit. The falsifier wrote "the fourth term is missing" — but the actual failure was that the fourth term was **measured incorrectly**.

**Discipline:** Logic / metascience / research methodology

**Time estimate:** 2–4 weeks

**Prerequisites:** None

**What to do:**
1. Read `SHB‑013` and its refutation in the claim table
2. Understand why the original falsifier was too narrow
3. Write a revised falsifier that would have caught the actual failure mode
4. Test your revised falsifier against the code
5. Submit a pull request updating the claim

**What success looks like:** A revised `SHB‑013` falsifier that catches the actual failure mode and is integrated into the claim table.

**What falsifies it:** Finding that the original falsifier was actually sufficient — which would be a different kind of finding (that the audit was mis‑interpreted).

---

## Project 4: Earth Transition Count at Different Coarse‑Grainings

**Gap:** `EARTH_TRANSITIONS.md` counts Earth's phase transitions using eight coarse‑grained labels. The count may depend on the coarse‑graining level.

**Discipline:** Geology / evolutionary biology / complex systems

**Time estimate:** 1 semester

**Prerequisites:** None (geology interest useful)

**What to do:**
1. Define what counts as a "phase transition" for Earth
2. Count transitions at multiple coarse‑graining levels (e.g., geological epochs, eras, eons)
3. Test whether the count is stable across levels
4. Identify the level at which the count stabilises
5. Write a report with your findings and a recommendation for the repository

**What success looks like:** A stable Earth‑transition count with a clear justification for the chosen coarse‑graining level.

**What falsifies it:** Finding that the count does not stabilise at any level — which would mean the concept is not well‑defined.

---

## Project 5: Discourse Analysis of Simulation Hypothesis

**Gap:** `ERA_METAPHOR.md` positions the simulation hypothesis as a recurring pattern. The framework notes four gaps, including "missing slot" and "imported boundary."

**Discipline:** Philosophy / discourse analysis / science and technology studies (STS)

**Time estimate:** 1 semester

**Prerequisites:** None (reading required)

**What to do:**
1. Collect texts that use the simulation hypothesis (philosophical papers, pop culture, scientific debates)
2. Analyse how the hypothesis is deployed in each text
3. Classify each usage as "responsibility‑avoidance" vs. "genuine inquiry"
4. Test whether the classification correlates with author background, era, or medium
5. Write a report with your discourse analysis

**What success looks like:** A classification of simulation‑hypothesis usages with a test of whether the "responsibility‑avoidance" pattern is real.

**What falsifies it:** Finding that all usages are sincere inquiry — which would mean the framework's framing is not empirically supported.

---

## Project 6: Cryptographic Seal Replacement for Divergence Playground

**Gap:** The `divergence‑playground` uses XOR obfuscation, which defends against accidental peeking but not determined attackers.

**Discipline:** Cryptography / security

**Time estimate:** 2–4 weeks

**Prerequisites:** Basic cryptography

**What to do:**
1. Review cryptographic commitment schemes
2. Implement a replacement for `seal.py` using a real cryptographic primitive
3. Test the replacement against the existing API
4. Document the security properties and trade‑offs
5. Submit a pull request with your implementation

**What success looks like:** A `seal_crypto.py` module with real cryptographic security, passing the same API tests.

**What falsifies it:** Finding that the XOR obfuscation is sufficient for all use cases — which would mean the replacement is not needed.

---

## Project 7: Fork Harvesting from Other Domains

**Gap:** The `divergence‑playground` can carry any project's own `FORKS.jsonl`. No forks have been harvested from other domains.

**Discipline:** Domain‑specific science / metascience

**Time estimate:** 1 semester

**Prerequisites:** None

**What to do:**
1. Identify candidate forks from other domains (climate, pharmacology, AI, engineering)
2. For each candidate, define the fork point
3. Write a `FORKS.jsonl` entry for each
4. Run the playground on the harvested forks
5. Write a report with cross‑domain spread patterns

**What success looks like:** A `FORKS.jsonl` file with 5+ forks from other domains, and a cross‑domain spread analysis.

**What falsifies it:** Finding that no forks exist in other domains — which would mean the playground is domain‑specific.

---

## How to Choose a Project

- **If you have a background in physics:** Projects 1 or 4
- **If you have a background in computer science:** Projects 2 or 6
- **If you have a background in philosophy or social science:** Projects 3 or 5
- **If you have no specific background:** Project 3 (falsifier repair) is the easiest entry point

---

## What to Do When You Finish

1. Write a short report (2–5 pages) with your findings
2. Update the relevant code or claim table
3. Submit a pull request to the repository
4. Your result becomes part of the argument — and the next person builds on it
```

---

File 3: FALSIFIER_WORKBOOK.md

```markdown
# Falsifier Workbook — How to Write Claims That Can Be Refuted

## What This Workbook Is For

Every claim in this repository has a **falsifier** — a condition that would refute it. This workbook teaches you how to write claims that can be refuted, using `SHB‑013` as a case study.

---

## The SHB‑013 Case Study

### Original Claim

**SHB‑013:** "Before assigning any cost value, four terms are needed: hierarchy stack, consistency term, ratio frame, and erasure count. A number cited without these terms is not a contested number; it is a quantity without a value."

### Original Falsifier

"The falsifier was: the fourth term is missing."

### What Actually Happened

The repository's audit ran. The fourth term **was present** — but it was **measured incorrectly**. The falsifier was too narrow. It predicted that the term would be missing; the actual failure was that the term was present but wrong.

### The Lesson

A good falsifier does not just name a missing condition. It names a **specific measurable property** of that condition. "Missing" is a binary state; "measured incorrectly" requires a threshold, a reference, and a test.

---

## How to Write a Falsifier

### Step 1: State the Claim

Write your claim as a **testable proposition**. Avoid vague language.

**Bad:** "The cost is high."
**Good:** "The cost exceeds 10^50 joules under all architectures."

### Step 2: Identify the Critical Variable

What would have to change for the claim to be false?

- The architecture
- The resolution
- The frame of reference
- The measurement method
- The coarse‑graining level

### Step 3: Write the Falsifier as a Measurable Condition

**Template:** "If [condition], then the claim is refuted."

**Example:** "If a lazy‑evaluation simulation produces a consistency cost ≤ 0, then the claim that consistency cost is always positive is refuted."

### Step 4: Test the Falsifier

Run the test. If the falsifier fires, update the claim. Do not correct it — record the refutation.

---

## Practice Exercises

### Exercise 1: Write a Falsifier for a Simple Claim

**Claim:** "All swans are white."

Write a falsifier.

<details>
<summary>Possible answer</summary>
"If a black swan is observed, the claim is refuted."
</details>

### Exercise 2: Write a Falsifier That Is Too Narrow

**Claim:** "The simulation requires more energy than the universe contains."

Write a falsifier that is too narrow — one that would miss the actual failure mode.

<details>
<summary>Possible answer</summary>
"If the universe contains more energy than 10^50 joules, the claim is refuted."
Why this is too narrow: The actual failure mode might be that the energy requirement depends on resolution, not that the universe's energy is larger than a fixed number.
</details>

### Exercise 3: Repair the Narrow Falsifier

Rewrite the falsifier so it catches the resolution‑dependent failure.

<details>
<summary>Possible answer</summary>
"If the energy requirement at the measured resolution is less than the universe's energy at any plausible cosmological model, the claim is refuted."
</details>

---

## Common Mistakes

### Mistake 1: The Falsifier Is Too Broad

"If the simulation is possible, the claim is refuted."

This is not a falsifier — it is the opposite of the claim. A falsifier must name a **specific condition**, not a negation.

### Mistake 2: The Falsifier Depends on the Claim Being True

"If the simulation is impossible, the claim is false."

This is circular. The falsifier must be independent of the claim.

### Mistake 3: The Falsifier Is Not Measurable

"If the simulation is wrong."

"Wrong" is not measurable. What does "wrong" mean? Incorrect output? Inconsistent physics? Unobservable effects? Name the measurable property.

### Mistake 4: The Falsifier Is Never Tested

The best falsifier in the world is useless if it is never run. Make sure your falsifier is implemented as a test in the code.

---

## Falsifier Checklist

Before you finalise a claim, check your falsifier against this list:

- [ ] The falsifier names a **specific condition** (not a negation)
- [ ] The falsifier is **measurable** (not vague)
- [ ] The falsifier is **independent** of the claim (not circular)
- [ ] The falsifier is **testable** (code exists or can be written)
- [ ] The falsifier is **recorded** in the claim table
- [ ] If the falsifier fires, the claim is **refuted** (not hidden or corrected)

---

## Documenting a Refutation

When a falsifier fires, update the claim table:

1. Change the status from `SUPPORTED` to `REFUTED`
2. Write a brief explanation of why the falsifier fired
3. Note whether the falsifier was correct or too narrow
4. If the falsifier was too narrow, propose a repair

**Example from SHB‑013:**

| id | claim | status |
|---|---|---|
| `SHB_013` | [Original claim] | **REFUTED** |

**Explanation:** The falsifier predicted that the fourth term would be missing. The term was present but measured incorrectly. The falsifier was too narrow.

**Repair:** The falsifier should have specified a measurement threshold, not just presence.

---

## Why This Matters

Falsifiers are not just for science — they are for **survival epistemology**.

If you do not know what would refute your reading of the field, you do not know when to change course. You do not know when the ice is thin. You do not know when the wind is shifting.

The falsifier is the boundary. The falsifier is the edge of the safe zone.

Learn to write them. Learn to test them. Learn to accept them when they fire.

That is how we learn to do better.
```
