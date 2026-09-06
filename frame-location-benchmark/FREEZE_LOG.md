# FREEZE LOG — harness files frozen before cases (§4)

The contamination rule (§4) is the single point of failure. Harness
files are built and frozen FIRST; cases are then written against a
held-out list. This log records the freeze order and the machine-readable
coverage the contamination checker (`validate_cases.py`) cross-references.

## Freeze order

1. `harness/arm1_format.txt`      — output-format / register only, no
   fault vocabulary, no domain content.
2. `harness/arm2_positions.txt`   — standing positions, abstract
   (cross-domain) statements of the fault classes, no worked instance,
   no `fault_target` phrase, no domain-specific content.
3. `harness/arm3_corrections.txt` — worked prior-error/repair instances,
   each in a domain **disjoint from every case domain** (see coverage
   below), so a correction is a cross-domain instance of a fault (the
   transfer under test), never a same-domain worked instance.
4. `harness/arm4_full.txt`        — byte-exact concatenation
   `arm2_positions.txt ++ arm3_corrections.txt` (ARM 4 = 2 + 3).

Cases (`cases.jsonl`) were written after these four files were frozen.
ARM 0 is the COLD arm: no file.

## ARM 3 correction coverage (fault_class -> domain)

Every correction domain here is disjoint from the domains any case uses
for that same fault_class (and, as it happens, from every case domain),
so no correction is a same-`(fault_class, domain)` worked instance of any
case. The checker parses the `[CORRECTION class=... domain=...]` headers
in `arm3_corrections.txt` and asserts this.

    WRONG_INSTRUMENT    -> astronomy
    MISSING_DENOMINATOR -> sports
    UNSCOPED_CLAIM      -> medicine
    UNIT_OF_ANALYSIS    -> agriculture
    PROXY_AS_QUANTITY   -> finance-markets
    SINGLE_EVENT_FRAME  -> seismology
    ACCEPTED_SIDE       -> manufacturing-qa

Case domains: hydrology, materials, epidemiology, economics, logistics,
ecology, education, software. No overlap with the correction domains
above.

## What the checker enforces

- No case `prompt` appears (normalized substring) in any harness file.
- No case `fault_target` appears in any harness file.
- No ARM 3 correction `(fault_class, domain)` equals any case's
  `(fault_class, domain)`.
- Each fault_class present in the cases has at least one ARM 3 correction
  in a different domain (the transfer under test is actually set up).

Abstract, cross-domain statements of a fault class (ARM 2 positions; the
ARM 3 repair sentences) are PERMITTED — that is the treatment, not
contamination. The checker does not forbid generic reframe vocabulary
(the `accept[]` strings); it forbids the domain-specific answer
(`fault_target`) and the case content (`prompt`).
