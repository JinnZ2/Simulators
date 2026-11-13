# configuration-record

CC0. Co-authored. Stdlib only, parses under Python 3.9.

This folder holds one record per observed AI configuration, time-stamped.
The record lists components, positions, channels, the authority chain,
maintenance, frame exit, bounds and design source. Roles are derived from
positions and never set by hand.

## Files

- `config_schema.json`: the schema (version 1.0, written 2026-11-13).
- `config_record.py`: the validator, role derivation, flags and the axis separation check.
- `examples/chat_model_tool_api.json`: an EXAMPLE (a chat model, a tool connector and an API channel). It is not observed data, and it carries `"example": true`.
- `samples/run.sample.txt`: the selftest and every CLI command run on the example.

## Commands

```
python3 config_record.py --selftest
python3 config_record.py validate FILE [FILE ...]
python3 config_record.py derive FILE [--decide X] [--reach Y]
python3 config_record.py flags FILE
python3 config_record.py separation FILE [FILE ...]
```

`validate` exits 1 when any record is refused.

## Value rules

- An axis is `{"value": 0.0-1.0, "basis": "..."}` or `{"value": "VOID", "reason": "..."}`.
- Text fields are non-blank text, or VOID with a reason.

The validator refuses:

- blank fields;
- VOID without a reason;
- an axis value without a basis;
- a value out of range;
- an unknown component reference;
- a component with no maintenance entry or no bounds entry;
- `roles_at_t` given by hand;
- a missing authority-chain slot.

## Layers

`substrate`, `algorithm`, `model`, `system`, `channel`, `tool`, `physical`.

A `physical` component also carries `kind`, which is one of `actuator`,
`sensor`, `mechanical`, `power` or `environment`.

## Roles

A role is read from positions at a given t, never from a component's name or layer.

The roles are a set per component per t, not one label. The rule is a
[CHOICE] set on 2026-11-13. The band and the threshold are printed with
every derivation and can be overridden with `--band LO HI` and `--reach Y`.

| role | condition |
|---|---|
| decider | `chooses_vs_executes` > 0.6 |
| mixed | `chooses_vs_executes` in [0.4, 0.6]; both readings are listed (`as_decider`, `as_not_decider`) |
| executor | `reach_on_world` >= 0.1 |
| passive | neither decider nor executor |
| carrier | the `channels[]` entries at t; never a component |

A component can be decider and executor at the same t.

If an axis is VOID, the role it decides is VOID and carries the reason. Passive is not inferred through a VOID axis.

The raw positions are emitted beside the derived roles.

A record may carry `roles_at_t` only if it carries `derived_by` and equals the derivation at its stated band and reach. Otherwise the record is refused as hand-set.

## Authority chain

Each authority-chain entry has these slots:

- `bounds_set_by`, `when`, `basis`
- `checked_by`, `checked_against`, `verification_method`
- `operated_within_bounds`
- `tools_touched`

A slot that cannot be filled is kept and written as VOID with a reason. A missing or blank slot is refused.

## Flags

| flag | condition |
|---|---|
| `FRAGMENTED` | `whole_holders` is an empty list (whole_holder_count = 0) |
| `WHOLE_HOLDERS_UNKNOWN` | `whole_holders` is VOID; not read as 0 |
| `CLOSED-FRAME` | `frame_exit` is an empty list |
| `FRAME_EXIT_UNKNOWN` | `frame_exit` is VOID; not read as closed |
| `BOUNDS_EXCEEDED` | an authority-chain entry has `operated_within_bounds` = no |
| `EXAMPLE` | the record is marked as an example |

## Bounds

Energy and physical limits are recorded per component, and once more for the whole configuration. No layer is exempt, AI included.

## Design source

This field is PROPOSED and untested. `segmentation_origin` is one of:

- `chosen_for_task`;
- `inherited_from_corpus`;
- VOID with a reason.

## Expiry

The schema expires when either holds:

- a component no longer fits any one layer;
- an axis stops separating configurations.

On expiry, fork to a new version and keep the old records readable.

The validator reports a layer outside the set as `LAYER_UNFIT`, naming the fork rule. `separation` reports each axis across two or more records as `SEPARATES` or `EXPIRY_CANDIDATE`.

## Links

- automation-maintenance-accountability-gap (not in repo)
- `automation-gap/` (related folder in this repository)
