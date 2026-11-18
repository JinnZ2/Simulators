# Key v2, amendment 1 -- DRAFT (not adopted)

Status: DRAFT, for the owner to fix or change. Nothing here is in force until the
owner adopts it, the text is hashed, and the hash is written into PREREG.md
BEFORE the next reading is requested.

Drafted by: Claude-v2-A's model, AFTER it had seen key v2 and its own score.
The drafter is not independent of the key or of a reader. The safeguard is
procedural: each change below follows from a rule stated in section 1, and each
rule is applied to all 15 terms in section 2, including the terms where it moves
the key AWAY from both Claude readings.

Scope: `slots_specific` rules, one scorer normalization, one scorer report
addition. The brief, the packet, the grouping key and the `slots_carried` key
lists are NOT changed. v2 readers stay poolable.

---

## 1. Rules

```text
S1  COLLECT  A name enters slots_specific if the source gives it by one of:
             (a) a parameter of a constructor / function written for this term only
             (b) a field of a class or record built only on this term's path
             (c) a field a source rule REQUIRES for this status
                 (raises / refuses without it, or a spec table marks it "required")
             (d) a documented key list or notation parameter for this term

S2  EXCLUDE  Remove a collected name if every other status that shares the same
             record or constructor also has it or also requires it.
             (e.g. `reason` where the rule is "every non-verdict token needs one")
             Presence counts, not value: a key present on every record of a kind
             is shared even when it is None on the other paths.

S3  ATTRS    OWNER CHOICE -- one of:
             S3-in   an attribute set by the source on this term's record only
                     (not a parameter) is collected under S1(b)
             S3-out  only S1(a), (c), (d) names and declared class fields count;
                     attributes computed after construction do not

ND  TEST     After S1-S3, if the sources still support two different lists,
             the list is undetermined (null), as PREREG v2 already defines n/d.

N1  SCORER   Before comparing names, strip one pair of surrounding `<` `>` and
             surrounding backticks. Nothing else (case, underscores, spaces
             are kept).

C1  SCORER   For each determined list, beside equal / differ, report the set
             relation: equal | reader-superset | reader-subset | overlap | disjoint.
             For a superset, list the extras. Reported beside the existing
             numbers; it replaces none of them and adds no combined score.

K1  CLARIFY  `slots_carried` "instance fields, checked by running it" means
             vars(instance): class attributes (e.g. ExpiryTrigger.is_exit) are
             not instance fields. No list changes under K1.
```

---

## 2. Applied to all 15 slots_specific lists

```text
id   term                     key v2                     rule result                         change   who it moves toward
---  -----------------------  -------------------------  ----------------------------------  -------  -------------------
T01  fa:UNDECIDED             []                         []  (bisection / subbox keys exist   none     AWAY from Claude-v2-A
                                                             on every record of that kind;            (it listed 5 names)
                                                             S2 removes them)
T02  taf:ABSENT_AT_SENS.      [value]                    [value]  via N1 (`<value>` == value)  scorer   toward both Claude
T03  cplay:VOID               []                         []                                  none     --
T04  cplay:ExpiryTrigger      [kind,target,condition]    same (S1b)                          none     --
T05  cplay:ABSENT_AT_SENS.    [limit,basis,effect_size,  S3-out: same                        S3-in    S3-in: toward Claude
                               conditions,ladder]        S3-in:  + covers_effect             only
T06  cplay:UNRESOLVED         []                         []  (FieldToken shared with          none     --
                                                             TOLERANCE_UNRESOLVABLE; S2)
T07  fa:VOID                  []                         []  (void_reason present on every    none     AWAY from Claude-v2-A
                                                             record; no rule requires it)             (it listed 2 names)
T08  cplay:CRASHED            null (n/d)                 null  (crash() builds CRASHED AND    none     --
                                                             GAP_INSTRUMENT_CRASH; params
                                                             `exc` vs field `exception`;
                                                             two readings remain -> ND)
T09  taf:UNKNOWN              []                         null CANDIDATE: glossary row ties    ND       neutral (n/d is
                                                             expiry_condition / expiry_source         neither match nor
                                                             to "PENDING / UNKNOWN" (S1d), but         miss)
                                                             unified_audit puts expiry_condition
                                                             on INFO and crash entries too (S2),
                                                             and expiry_source may belong to the
                                                             exit, not the slot. Two readings.
T10  taf:GAP_INSTR._CRASH     [kind,module,input,reason, [missing_path, error,               S2       toward Claude-v2-A
                               missing_path,              exception_type]
                               expiry_condition]          S2: UNKNOWN / INFO entries carry
                                                             5 of the 6 (unified_audit 345-371);
                                                             missing_path only on crash entries
                                                             (334-343). S1b: section record
                                                             {error, exception_type, missing_path}
                                                             built only in the raise branch (485-489)
T11  fa:HOLDS                 []                         []                                  none     --
T12  cplay:UNKNOWN            [reason,triggers]          S3-out: [triggers]                  S2 (+S3) toward Claude-v2-A
                                                         S3-in:  [triggers,typed,untyped]
                                                         S2: `reason` required on every
                                                             non-verdict token (tokens.py 48-49)
T13  cplay:OK                 []                         []                                  none     --
T14  cplay:CLOSED_WITHIN      [sigma,basis]              same (S1c, axes.py 61-63)           none     --
T15  taf:expiry_condition     [instrument_class,         same (S1d, EXPIRY_KEYS)             none     --
                               sensitivity,protocol,
                               provenance]
```

Net change, specific: T10, T12 (S2); T05, T12 (only if S3-in); T09 -> n/d; T02 by scorer.

Direction check, stated plainly. Of the changes, all of them move toward the
Claude readings or to neutral, and none moves away. The rules ALSO hold the key
against Claude-v2-A at T01 and T07 (7 names it gave that S2 removes). That is
the evidence that the rules weren't fitted to it, and it is weak evidence:
one drafter, one family. A non-Claude reader is the real test.

---

## 3. What stays open (not amended)

```text
slots_carried depth     not stated in the brief. Handled by C1 (report relation),
                        not by changing the brief. A v2.1 brief remains possible later
                        as its own pool.
T09 slots_carried       already null in key v2; unchanged.
grouping key            unchanged. HOLDS | CLOSED_WITHIN vs HOLDS | OK stays the
                        key's call; two Claude readings are one family (rule 5).
```

---

## 4. Procedure to adopt

```text
1  owner picks S3-in or S3-out; edits or strikes any rule
2  sha256 this file as adopted -> PREREG.md dated section, before any new reading
3  write key_v2_a1.json from section 2; keep key_v2.json byte-identical
4  test_score_v2.py: add checks that a1 lists follow from the rules
   (same style as v2: run the cplay code, match TAF / numcheck text)
5  score every existing v2 reading under BOTH v2 and v2-a1; file both, change neither
6  only then request the Kimi reading (v2 packet, variant as planned, unchanged)
```
