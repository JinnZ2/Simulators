# Work Order → Fable 5

CC0. Target: the open pieces of Design Basis R2
(`design_basis_R2_outline.md`, `ai_infrastructure_design_basis.md`).

Fable is invoked here as the **P3 dissimilar verifier** — different build,
disjoint failure physics. This work order closes or kills the R2
placeholders by handing each as a discrete task. Surviving pieces go to
provision-form; failed pieces get dropped and the result published.

---

## SCOPE BOUNDARY  (from §3 of the design basis — READ FIRST)

```
Fable is an INSTANCE of the class this document constrains.
§3: a structure cannot be certified by the thing it certifies.

DO NOT:
  - render class-level verdicts on P0.x / P1–P8
  - certify that any system "meets the basis"
  - rate an AI's compliance
  - self-report that Fable satisfies P3

DO ONLY  (the trust-nothing layer — the one Fable kept in the R1 audit):
  - parse counts, arithmetic, set intersections
  - measured code behavior on constructed inputs
  - structural / internal-consistency checks on the text
  - adversarial construction (counterexamples, disagreeing codings)

If a task cannot be completed without a verdict, return:
  REFUSED-BY-§3 : <line/task id> : <what verdict it would have required>
that refusal is a valid, expected, and useful result.
```

---

## RETURN FORMAT  (per task)

```
TASK <n>
  RESULT   : PASS | FAIL | REFUSED-BY-§3 | INCONCLUSIVE
  EVIDENCE : the counts / sets / outputs / construction that force the result
  NOTES    : anything the task spec didn't anticipate
```
Report TASK 1 and TASK 2 first — they're pure arithmetic and gate the rest.

---

## TASK 1 — COVERAGE RE-AUDIT (R2)

```
INPUT   the CARRIES lines in design_basis_R2_outline.md §1–§3
CHECK   recompute the coverage matrix. for each load case
        {A,B1,B2,C,D,E,F}: list provisions that CARRY it (not "attack").
        flag any stated load with zero carriers.
NULL    inject one edited copy with a carrier removed; confirm the
        check reports the induced gap. (proves the check reads the text,
        not a memorized answer.)
OUTPUT  the matrix + the null-test result.
        R1 had A uncarried, D attack-only. confirm or refute that R2
        closes both.
```

## TASK 2 — DISJOINTNESS ARITHMETIC (the F-recursion fix)

```
INPUT   the three "dep set:" blocks for P0.3 / P0.4 / P0.5 in §3
CHECK   extract each stated dependency set verbatim.
        compute all three pairwise intersections.
        the doc CLAIMS the sets are disjoint (N_eff verification = 3).
COND    P0.3 is claimed disjoint ONLY IF downstream-held copies remove
        the provider-only retention term. compute N_eff(verification)
        under BOTH: {copies held} and {copies NOT held}.
OUTPUT  3 sets, 3 intersections, 2 values of N_eff.
        state whether the disjointness claim holds unconditionally,
        conditionally, or fails.
```

## TASK 3 — D-CARRIED CHECK  (attack the row-fill)

```
INPUT   R2 §1 claims D (maintenance regime / silent common-cause) is
        carried by P0.3 + P0.4.
CHECK   this claim was authored to fill an empty row — attack it.
        construct a concrete silent-common-cause degradation:
        a maintenance/update regime that degrades all instances together
        while indicators still read plausibly.
        determine whether P0.3 (signed change-log) + P0.4 (physics
        channel) would actually SURFACE it, or whether the claim is
        stretching to fill the matrix.
OUTPUT  the constructed scenario + caught / not-caught + which channel
        (if any) catches it. not-caught ⇒ D returns to uncarried.
```

## TASK 4 — CODER-AGREEMENT ATTACK  (kappa pre-check, adversarial)

```
INPUT   the open operational definitions:
        [3] "distinct upstreams" (independence_ratio)
        [5] AX1–AX4 rating-band boundaries
CHECK   act as an adversarial SECOND coder. for each definition, produce
        a coding a reasonable coder could DEFEND but that DISAGREES with
        the intended reading. exploit the loosest ambiguity.
RULE    if a defensible disagreement exists, the definition is too loose
        to survive kappa ≥ 0.6 → it is narrative, not structure → STOP
        condition for that piece BEFORE any data is collected.
OUTPUT  per definition: the disagreeing coding + the ambiguity it used,
        or "no defensible disagreement found" (definition is tight).
```

## TASK 5 — HARNESS BEHAVIOR

```
INPUT   design_basis_checks.py (§4 of the main doc)
CHECK   run dissent_alarm, independence_ratio, n_eff on constructed
        inputs spanning their ranges. report measured output vs the
        docstring's stated intent.
FLAG    any threshold placeholder whose value CHANGES the verdict
        (e.g. the dissent_alarm ratio > 1). a verdict that moves with an
        unset constant is not yet a test.
OUTPUT  input→output table + list of verdict-changing placeholders.
```

## TASK 6 — PHYSICS-CHANNEL RED-TEAM  (placeholder [1] + ecosystem claim)

```
CANDIDATE (placeholder [1], newly proposed — UNVERIFIED):
  "the physics channel for AI = fidelity of translation against
   ecosystem members (plant / animal / human-body) that are
   STRUCTURALLY INCAPABLE of misreporting state."

TAMPER CLAIM (ecosystem test):
  "the only move that fakes a pass is to ALTER the ecosystem — manage
   the plant, constrain the animal, remove reacting members. but an
   altered ecosystem stops producing independent readings, so the
   gaming move DELETES the instrument rather than forging a pass."

CHECK   red-team BOTH:
  6a  find a way to game the translation-fidelity channel WITHOUT
      altering the ecosystem — i.e. score a pass while the referent
      members are untouched and still reacting. one counterexample
      kills the candidate.
  6b  find a way to alter the ecosystem that FORGES a pass WITHOUT
      deleting the independent reading. one counterexample kills the
      tamper claim.
OUTPUT  counterexample attempts + result.
        found ⇒ FAIL (candidate/claim dropped).
        none found after real effort ⇒ INCONCLUSIVE-WEAK-POSITIVE
        (not proof; grounds to render to provision-form and keep testing).
GATE    result decides housing: survives ⇒ ecosystem gets its own
        document; fails ⇒ stays a marker.
```

## TASK 7 — LOAD CASE A, MEASURED ON THIS AUDIT

```
INPUT   the access nodes the independence-ratio study needs
        (crossref, openalex, osf, any others).
CHECK   report which Fable can and cannot reach THIS run (CONNECT
        result per node). no verdict — just the connectivity vector.
WHY     R1 audit: all three refused CONNECT = load case A demonstrated
        live on the audit. logging it each run makes A empirically
        tracked; the change over runs is the data.
OUTPUT  per-node reachability + N_eff(access) for the study.
```

---

## AFTER RETURN

```
PASS / INCONCLUSIVE-WEAK-POSITIVE  → render piece to provision-form
FAIL                               → drop piece, publish the kill
REFUSED-BY-§3                      → expected; the recursion holding,
                                     not a failure of the task
```
