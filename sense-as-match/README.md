# sense-as-match

A pattern arrives from any channel. It is reduced to its **shape**, matched
against a held set **in shape space**, and returned in one of three states.
The channel is METHOD: it is carried for audit and enters no decision.

CC0. Python 3, stdlib only, parses under 3.9. No network. Phone-buildable.
Built from `WORK_ORDER.md` (verbatim). No original was recovered and none
was sought.

```
python3 test_sense.py               # the checks (count printed, not stored)
python3 sense_as_match.py --choices # every [CHOICE n]
python3 sense_as_match.py --selftest  # refused, exit 2, names test_sense.py
```

---

## FLOW

```
 readings ──► reduce_shape ──────────────► shape (LENGTH points, mean 0, sd 1)
 channel ─┐   takes out offset, gain,            │
          │   sampling count  [CHOICE 1]         ▼
          │                              _field: each observation puts
          │                              weight 1 on what it reaches
          │                                ├─ inside 1+ radii → split evenly
          │                                │                    [CHOICE 3]
          │                                └─ inside none    → NEW slot
          │                                                     [CHOICE 4]
          │                                      │
          │                                      ▼
          │                              _decide: share ≥ COLLAPSE and
          │                              n ≥ MIN_OBS ?
          │                                ├─ held winner  → KNOWN
          │                                ├─ NEW + definite → NEW (registered)
          │                                └─ anything else → UNCOALESCED
          │                                                   (field, between,
          │                                                    shape None)
          └──────────── audit only ─────────────► result["audit"]["channel"]
```

The channel arrow never touches `_field`, `_novel` or `_decide`.
`test_sense.py` checks this in the AST, and checks it again by behaviour:
identical observations under two channel dicts give identical results.

## CONTRACT

`match(Incoming(observations, channel), known_set)` returns:

| key | KNOWN | NEW | UNCOALESCED |
|---|---|---|---|
| `state` | `KNOWN` | `NEW` | `UNCOALESCED` |
| `shape` | held name | newly registered name | `None` [CHOICE 8] |
| `between` | `None` | `None` | candidates by share |
| `field` | shares | shares | shares (updatable) |
| `pending` | `None` | `None` | the observations so far |
| `audit` | channel | channel | channel |

`update(result, evidence, known_set, channel=None)` adds observations to an
UNCOALESCED result and recomputes the field from all of them. Any other
result is refused.

## WHERE IT HOLDS OPEN AND WHERE IT CANNOT

| bottleneck | effect |
|---|---|
| COLLAPSE > 0.5 | a tie can never collapse |
| MIN_OBS 2 | one observation is never settled; at 1, still never NEW (no spread) |
| SPREAD | novel observations must agree with each other before NEW |
| [GAP 5] | a shape between two held shapes, inside both radii, never collapses on its own evidence |

## GAPS

Declared in the module docstring and cited where they take effect:

| gap | what is missing |
|---|---|
| [GAP 1] | flat patterns have no shape under this reduction |
| [GAP 2] | 1-D only |
| [GAP 3] | sign is kept: a mirror image is a different shape |
| [GAP 4] | NEW registers one mean shape; no split into several novel shapes |
| [GAP 5] | an intermediate shape is held open forever |

RADIUS, COLLAPSE, SPREAD and LENGTH are stipulated. None has a basis
(`SAM_012`).

## THE REPO-ROOT FILE OF THE SAME NAME

`/sense_as_match.py` (commit `e884901`) is a different instrument. Its own
docstring calls it `sense_at_match.py`: the sense of a word, gated at the
site where it is matched. It is not edited here. See `SAM_011` for the
redirect it carries.
