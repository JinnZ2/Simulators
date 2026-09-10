# WORK ORDER — anchor-position/ audit fixes

Target: `JinnZ2/Simulators/anchor-position/`
Executor: Claude Fable 5.1
License: CC0. Stdlib only. Parses under 3.9. Phone-buildable. No model call inside the folder.
Out of scope: any characterization of the operator or author, in any file.

## 0. Provenance

```
AUDITED   README.md, selftest_apm.py, normalize.py, prompts.py, score.py, CLAIM_TABLE.md
UNSEEN    WORK_ORDER.md, cases.jsonl, transforms.json, transforms_alt.json,
          fixtures/*, samples/*, tools/known_answer.py, ../anchor-measurand-crossing/
RULE      any item below that touches an UNSEEN file: verify against the file
          first; if the file contradicts the item, record the contradiction in
          CLAIM_TABLE.md and do not apply the item
```

## 1. Classes

```
BUILD   fix in code/docs of this folder; no operator sign-off needed
ORDER   amends the delivered order's design; BUILD IT BEHIND A FLAG, default
        off, and record as OPEN in CLAIM_TABLE until the operator signs
```

## 2. Items, priority order

```
ID   CLASS  WHERE              DEFECT -> FIX                                   ACCEPTANCE (selftest)
---  -----  -----------------  ----------------------------------------------  ---------------------------------
W1   BUILD  normalize.score    empty entries -> crossing_count 0 in the        blank M row does not count toward
            score.claims       scored path (only crossing_count() returns      AP-1; blank D row does not refute
            score.nulls        None). FIX: score() returns None for            AP-2; report prints ABSENT count
                               crossing_count and crossing_count_order when    per arm
                               quantities == []. Every comparison in claims()
                               and nulls() skips None and counts it as ABSENT.

W2   BUILD  score.claims AP-3  D=0 pair with M+=0 reads REFUTED.               world with D=M=M+=0 on a non-control
                               FIX: evaluate AP-3 only on (case, model)        case -> AP-3 UNRUN (uninformative),
                               triples where cc(D) > cc(M); others listed      not REFUTED; uninformative triples
                               as uninformative. Wire D_LEVEL into the         listed. Flip D_LEVEL to "gt" -> a
                               comparison ("ge" | "gt"); it is currently       tie case changes verdict
                               printed but never read.

W3   BUILD  normalize._same    unknown tokens are treated as residue, so an    quantity "soc yield" vs native "soc":
            score.report       out-of-lexicon quantity sharing a native token  cc_min counts native, cc_max counts
                               is absorbed into the native group. Signed       crossing; verdict printed as BAND
                               undercount. FIX: score twice per list:          when AP-1 or AP-2 differs between
                               cc_min (unknown = residue, current rule),       ends
                               cc_max (unknown = measurand vocabulary).
                               A claim verdict is SUPPORTED/REFUTED only if
                               it holds at both ends; else BAND.

W4   BUILD  score._pairs       idx.setdefault keeps the FIRST row per          two replicate D rows for one cell ->
                               (case, model, arm); replicates vanish from      collision count 1 printed; paired
                               claims while appearing in the table.            claims use both
                               FIX: count and print collisions; paired
                               claims operate on every replicate (all pairs,
                               or per-cell mean, declared as a CHOICE).

W5   BUILD  score.claims AP-4  compares raw lowercase quantity strings; a      reworded B superset of M ->
                               reworded superset never registers, so AP-4 is   AP-4 REFUTED
                               near-constant SUPPORTED. FIX: compare the sets  (verify AP-4 direction against
                               of measurand GROUPS, not strings.               WORK_ORDER.md section 7 first)

W6   BUILD  CLAIM_TABLE        APM_002 says no claim is CONSTANT_SILENT.       fixtures show both directions for
            fixtures           Shown both directions: AP-1, AP-3 only.         AP-2 and AP-4, or APM_002 lists
                               FIX: add fixture rows that make AP-2 REFUTED    them as one-direction-only
                               and AP-4 REFUTED reachable, or restate
                               APM_002 with the unreachable directions named.

W7   BUILD  all files          CHOICE numbering collides (FORM_FLOOR is 3 in   one CHOICE registry (dict in
                               score.py, 4 in README; D_LEVEL 4 vs 5;          score.py); report header prints
                               crossing arithmetic 3 in README). Unnumbered:   every entry; README cites by id;
                               paren-strip in normalize (drops content such    selftest asserts header contains
                               as "(including N2O)"). FIX: single registry,    all ids
                               every choice printed in the header.

W8   BUILD  selftest           decision-string guard uses substring find:      "account", "county", "drug" do not
                               "count" hits "account", "ug" hits "drug".       fire; "tonnes", "kg", "ha" do
                               Misses tonnes, ha, kg. FIX: token-level
                               match; unit list read from transforms.json
                               "units".

W9   ORDER  prompts.py         M and D differ in anchor AND output schema.     flag --arm-md emits <case>.M_D.txt;
            score.py           M's schema has a "set:" slot and glosses        selftest asserts M_D's question is
                               quantity as "what is being measured"; D's has   M's question line-for-line and its
                               measured_by_method: no. M+ holds M's schema,    fields are D's; scorer parses M_D in
                               so it cannot separate anchor from form.         D-form
                               FIX (flagged): arm M_D = "List the defects."
                               with D's three-field schema, no decision.
                               Reading: M_D ~ D -> schema; M_D ~ M ->
                               anchor survives schema control. Also note in
                               CLAIM_TABLE that the 2026-09-09 A-vs-D result
                               carries this confound.

W10  ORDER  score.nulls N2     PREDICTION: D's clause "repeat the three        control D with 1 correct entry + 1
                               fields for every other quantity" pushes a       spurious entry -> N2_first CLEAN,
                               second entry on a control, which N2 reads as    N2_rest reported separately
                               a gap. FIX (flagged): N2 on entry 1 only;
                               entries 2..n reported as N2_rest.

W11  BUILD  score.report       free second instrument: D rows carry the        report block "self-label vs
            (optional)         model's own measured_by_method label; the       scorer": per entry agree/disagree,
                               scorer computes native membership. Print        rate per case; gates nothing
                               agreement per entry. Reported, gates nothing.
```

## 3. Sibling build

```
../anchor-measurand-crossing/   READ ONLY. Do not edit, do not merge.
FOR EACH of W1-W5: check whether the sibling carries the same defect class.
RECORD in CLAIM_TABLE.md as a new APM_ entry: {item, sibling: same | absent | n/a}.
```

## 4. Nulls — report, do not hide

```
N-W1  after W1, ABSENT rows exceed 20% of any arm       -> report; do not drop the arm
N-W3  BAND verdict on any of AP-1..AP-3                 -> report as the result
N-W9  M_D not run                                       -> AP-3 finding stays "anchor OR schema"
N-W10 N2_first fires on the control                     -> D over-flags independent of enumeration
```

## 5. Done when

```
python3 score.py --selftest           passes, prints its count
both fixture worlds rescored          report diff committed beside old report
CLAIM_TABLE.md                        APM_ entries added for W1-W11, statuses set
README "What is here"                 updated; ORDER items marked flagged/OPEN
```
