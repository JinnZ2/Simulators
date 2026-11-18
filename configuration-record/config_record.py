"""
config_record.py -- configuration record validator and role derivation.
CC0. Co-authored. Stdlib only, parses under 3.9.

One record per observed setup, time-stamped. Rules (config_schema.json):
  - every axis is 0.0-1.0 with a basis, or VOID with a reason
  - blank fields, VOID without a reason, an axis value without a basis are refused
  - roles_at_t is derived from positions only, never hand-set
  - every component and the whole carry a bounds entry; no layer is exempt
Flags (recorded, not refusals): FRAGMENTED, WHOLE_HOLDERS_UNKNOWN, CLOSED-FRAME,
FRAME_EXIT_UNKNOWN, BOUNDS_EXCEEDED, EXAMPLE.

  python3 config_record.py validate FILE [FILE ...]
  python3 config_record.py derive FILE [--band LO HI] [--reach Y]
  python3 config_record.py flags FILE
  python3 config_record.py separation FILE [FILE ...]
  python3 config_record.py --selftest

Role rule [CHOICE, 2026-11-13], roles are a SET per component per t:
decider if chooses_vs_executes > BAND_HI; mixed (both readings listed) if it
lies in [BAND_LO, BAND_HI]; executor if reach_on_world >= REACH; passive if
neither. Carriers are the channels[] entries, never components. A VOID axis
makes the role it decides VOID with the reason. Raw positions are emitted
beside the roles. Read from positions at t, never from name or layer.
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(HERE, "config_schema.json")
DERIVED_BY = "configuration-record/config_record.py"


def load_schema(path=SCHEMA_PATH):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


SCHEMA = load_schema()
BAND_LO, BAND_HI = SCHEMA["roles_at_t"]["BAND"]
REACH = SCHEMA["roles_at_t"]["REACH"]
LIST_MAY_BE_EMPTY = {("frame_exit",), ("maintenance", "whole_holders")}


def is_void(v):
    return isinstance(v, dict) and v.get("value") == "VOID"


def _blank_str(v):
    return isinstance(v, str) and not v.strip()


class Checker:
    def __init__(self):
        self.findings = []

    def add(self, code, path, msg=""):
        self.findings.append((code, path, msg))

    def required(self, obj, keys, path):
        ok = True
        if not isinstance(obj, dict):
            self.add("BLANK", path, "expected an object")
            return False
        for k in keys:
            if k not in obj:
                self.add("BLANK", f"{path}.{k}", "missing field")
                ok = False
        return ok

    def void(self, v, path):
        r = v.get("reason")
        if r is None or _blank_str(r) or not isinstance(r, str):
            self.add("VOID_NO_REASON", path)
            return False
        return True

    def axis(self, v, path):
        if is_void(v):
            return self.void(v, path)
        if not isinstance(v, dict) or "value" not in v:
            self.add("AXIS_MALFORMED", path, "expected {value, basis} or VOID")
            return False
        x = v["value"]
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            self.add("AXIS_MALFORMED", path, f"value {x!r} is not a number")
            return False
        if not 0.0 <= x <= 1.0:
            self.add("AXIS_RANGE", path, f"value {x} outside 0.0-1.0")
        b = v.get("basis")
        if b is None or not isinstance(b, str) or _blank_str(b):
            self.add("AXIS_NO_BASIS", path)
            return False
        return True

    def text_or_void(self, v, path):
        if is_void(v):
            return self.void(v, path)
        if isinstance(v, str) and v.strip():
            return True
        self.add("BLANK", path, "expected non-blank text or VOID")
        return False

    def enum_or_void(self, v, allowed, path):
        """{value, basis} with value in allowed, or VOID with a reason."""
        if is_void(v):
            return self.void(v, path)
        if not isinstance(v, dict) or v.get("value") not in allowed:
            self.add("BAD_ENUM", path, f"expected one of {allowed}")
            return False
        b = v.get("basis")
        if b is None or _blank_str(b):
            self.add("AXIS_NO_BASIS", path)
            return False
        return True

    def named_list(self, v, path, item_keys, may_be_empty=False):
        """a list of objects each carrying item_keys and a basis, or VOID."""
        if is_void(v):
            return self.void(v, path)
        if not isinstance(v, list):
            self.add("BLANK", path, "expected a list or VOID")
            return False
        if not v and not may_be_empty:
            self.add("BLANK", path, "empty list")
            return False
        for i, it in enumerate(v):
            p = f"{path}[{i}]"
            if self.required(it, list(item_keys) + ["basis"], p):
                for k in item_keys:
                    if _blank_str(it[k]) or it[k] is None:
                        self.add("BLANK", f"{p}.{k}")
                if _blank_str(it["basis"]) or not isinstance(it["basis"], str):
                    self.add("AXIS_NO_BASIS", f"{p}.basis")
        return True


def _walk_blank(obj, path, out):
    if _blank_str(obj):
        out.append(("BLANK", path, "empty string"))
    elif isinstance(obj, dict):
        if not obj:
            out.append(("BLANK", path, "empty object"))
        for k, v in obj.items():
            _walk_blank(v, f"{path}.{k}" if path else k, out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _walk_blank(v, f"{path}[{i}]", out)


def _role_reading(roles):
    return sorted(roles) if roles else ["passive"]


def derive_roles(rec, lo=None, hi=None, reach=None):
    """roles_at_t from positions only. Roles are a SET per component per t.
    decider: chooses_vs_executes > hi; mixed: lo <= chooses <= hi (both readings
    listed); executor: reach_on_world >= reach; passive: neither. Carriers are the
    channels[] entries at t, never components. A VOID axis makes the role(s) it
    decides VOID with the reason. Raw positions are emitted beside the roles."""
    lo = BAND_LO if lo is None else lo
    hi = BAND_HI if hi is None else hi
    reach = REACH if reach is None else reach
    by_t = {}
    for p in rec.get("positions", []):
        by_t.setdefault(str(p.get("t")), {"t": p.get("t"), "components": [], "carriers": []})
    for ch in rec.get("channels", []):
        by_t.setdefault(str(ch.get("t")), {"t": ch.get("t"), "components": [], "carriers": []})
    for p in rec.get("positions", []):
        cid = p.get("component_id")
        c, r = p.get("chooses_vs_executes"), p.get("reach_on_world")
        roles, void, readings = set(), [], None
        dstate = estate = None
        if c is None or is_void(c):
            void.append({"role": "decider", "reason": "chooses_vs_executes VOID: " + str((c or {}).get("reason"))})
        elif c["value"] > hi:
            dstate = "decider"
        elif c["value"] >= lo:
            dstate = "mixed"
        else:
            dstate = "none"
        if r is None or is_void(r):
            void.append({"role": "executor", "reason": "reach_on_world VOID: " + str((r or {}).get("reason"))})
        elif r["value"] >= reach:
            estate = "executor"
        else:
            estate = "none"
        if dstate in ("decider", "mixed"):
            roles.add(dstate)
        if estate == "executor":
            roles.add("executor")
        if dstate == "none" and estate == "none":
            roles.add("passive")
        elif dstate is None or estate is None:
            if not roles:
                void.append({"role": "passive", "reason": "passive needs both axes; one is VOID"})
        if dstate == "mixed" and estate is not None:
            base = roles - {"mixed"}
            readings = {"as_decider": sorted(base | {"decider"}),
                        "as_not_decider": _role_reading(base)}
        raw = {a: copy.deepcopy(p.get(a)) for a in SCHEMA["positions"]["axes"]}
        raw["override"] = copy.deepcopy(p.get("override"))
        by_t[str(p.get("t"))]["components"].append(dict(
            component_id=cid, roles=sorted(roles), readings=readings, void=void, raw=raw))
    for ch in rec.get("channels", []):
        by_t[str(ch.get("t"))]["carriers"].append(
            {"channel_id": ch.get("id"), "from": ch.get("from"), "to": ch.get("to")})
    out = [by_t[k] for k in sorted(by_t)]
    return dict(derived_by=DERIVED_BY, rule=SCHEMA["roles_at_t"]["derivation"],
                choice=SCHEMA["roles_at_t"]["choice"],
                BAND=[lo, hi], REACH=reach, roles=out)


def validate(rec, schema=SCHEMA):
    ck = Checker()
    S = schema
    _walk_blank({k: v for k, v in rec.items() if k != "roles_at_t"}, "", ck.findings)
    # the walk reports empty lists only through named_list; drop its empty-object
    # noise for lists allowed empty
    if not ck.required(rec, S["record"]["required"], "record"):
        pass
    for k in rec:
        if k not in S["record"]["required"] + S["record"]["optional"]:
            ck.add("UNKNOWN_FIELD", k)
    if rec.get("schema_version") not in (None, S["schema_meta"]["version"]):
        ck.add("SCHEMA_VERSION", "schema_version",
               f"record {rec.get('schema_version')!r}, schema {S['schema_meta']['version']!r}; "
               "fork-on-expiry: read it with the schema version it was written for")
    src = rec.get("source")
    if src is not None:
        if is_void(src):
            ck.void(src, "source")
        elif not (isinstance(src, dict) and src.get("value") in ("observed", "claimed")):
            ck.add("BAD_ENUM", "source", f"expected {S['record']['source_values']}")
        elif _blank_str(src.get("basis", "")) or "basis" not in src:
            ck.add("AXIS_NO_BASIS", "source")
    # components
    comp_ids = set()
    comps = rec.get("components", [])
    if not comps:
        ck.add("BLANK", "components", "empty list")
    for i, c in enumerate(comps):
        p = f"components[{i}]"
        if not ck.required(c, S["components"]["required"], p):
            continue
        comp_ids.add(c["id"])
        if c["layer"] not in S["components"]["layers"]:
            ck.add("LAYER_UNFIT", f"{p}.layer",
                   f"{c['layer']!r} fits no one layer of schema {S['schema_meta']['version']}; "
                   "on expiry: fork to a new version, keep old records readable")
        if c["layer"] == "physical" and c.get("kind") not in S["components"]["physical_kinds"]:
            ck.add("BAD_ENUM", f"{p}.kind", f"physical component needs kind in {S['components']['physical_kinds']}")
        ck.text_or_void(c["version"], f"{p}.version")
    # positions
    for i, q in enumerate(rec.get("positions", [])):
        p = f"positions[{i}]"
        if not ck.required(q, S["positions"]["required"], p):
            continue
        if q["component_id"] not in comp_ids:
            ck.add("UNKNOWN_REF", f"{p}.component_id", str(q["component_id"]))
        for a in S["positions"]["axes"]:
            ck.axis(q[a], f"{p}.{a}")
        if ck.required(q["override"], S["positions"]["override_required"], f"{p}.override"):
            ck.text_or_void(q["override"]["who"], f"{p}.override.who")
            ck.axis(q["override"]["latency"], f"{p}.override.latency")
    # channels
    for i, ch in enumerate(rec.get("channels", [])):
        p = f"channels[{i}]"
        if not ck.required(ch, S["channels"]["required"], p):
            continue
        for end in ("from", "to"):
            if ch[end] not in comp_ids:
                ck.add("UNKNOWN_REF", f"{p}.{end}", str(ch[end]))
        for a in S["channels"]["axes"]:
            ck.axis(ch[a], f"{p}.{a}")
        ck.text_or_void(ch["filter_holder"], f"{p}.filter_holder")
        ck.named_list(ch["drops"], f"{p}.drops", ["name"])
    # authority chain
    ac = rec.get("authority_chain", [])
    if not ac:
        ck.add("BLANK", "authority_chain", "empty list")
    for i, a in enumerate(ac):
        p = f"authority_chain[{i}]"
        miss = [k for k in S["authority_chain"]["required"] if k not in a]
        for k in miss:
            ck.add("BLANK", f"{p}.{k}", "missing authority-chain slot: keep it, write VOID with a reason")
        if miss:
            continue
        for k in ("bounds_set_by", "when", "basis"):
            ck.text_or_void(a[k], f"{p}.{k}")
        for k in ("checked_by", "checked_against", "verification_method"):
            ck.text_or_void(a[k], f"{p}.{k}")
        ck.enum_or_void(a["operated_within_bounds"], ["yes", "no"], f"{p}.operated_within_bounds")
        tt = a["tools_touched"]
        if not isinstance(tt, list):
            ck.add("BLANK", f"{p}.tools_touched", "expected a list")
        elif not tt and _blank_str(a.get("tools_touched_basis", "")):
            ck.add("BLANK", f"{p}.tools_touched", "empty list without tools_touched_basis")
        else:
            for t in tt:
                if t not in comp_ids:
                    ck.add("UNKNOWN_REF", f"{p}.tools_touched", str(t))
    # maintenance
    m = rec.get("maintenance")
    if m is not None and ck.required(m, S["maintenance"]["required"], "maintenance"):
        seen = set()
        for i, pc in enumerate(m["per_component"]):
            p = f"maintenance.per_component[{i}]"
            if not ck.required(pc, S["maintenance"]["per_component_required"], p):
                continue
            seen.add(pc["component_id"])
            if pc["component_id"] not in comp_ids:
                ck.add("UNKNOWN_REF", f"{p}.component_id", str(pc["component_id"]))
            ck.text_or_void(pc["repairable_by"], f"{p}.repairable_by")
            ck.axis(pc["sees_of_rest"], f"{p}.sees_of_rest")
        for cid in sorted(comp_ids - seen):
            ck.add("MISSING_MAINTENANCE", "maintenance.per_component", cid)
        ck.named_list(m["whole_holders"], "maintenance.whole_holders",
                      ["role", "holder_kind"], may_be_empty=True)
    # frame exit
    if "frame_exit" in rec:
        ck.named_list(rec["frame_exit"], "frame_exit",
                      ["sees_failure", "can_act", "path_kind"], may_be_empty=True)
    # bounds
    b = rec.get("bounds", [])
    scopes = set()
    for i, e in enumerate(b if isinstance(b, list) else []):
        p = f"bounds[{i}]"
        if not ck.required(e, S["bounds"]["required"], p):
            continue
        scopes.add(e["scope"])
        if e["scope"] != "whole" and e["scope"] not in comp_ids:
            ck.add("UNKNOWN_REF", f"{p}.scope", str(e["scope"]))
        en = e["energy"]
        if is_void(en):
            ck.void(en, f"{p}.energy")
        elif not (isinstance(en, dict) and isinstance(en.get("value"), (int, float))
                  and not isinstance(en.get("value"), bool) and en["value"] >= 0
                  and en.get("unit") and en.get("basis")):
            ck.add("AXIS_NO_BASIS", f"{p}.energy", "needs value >= 0, unit, basis, or VOID")
        ck.named_list(e["physical_limits"], f"{p}.physical_limits", ["name", "value", "unit"])
    for cid in sorted((comp_ids | {"whole"}) - scopes):
        ck.add("MISSING_BOUNDS", "bounds", f"{cid}: no layer is exempt")
    # design source
    ds = rec.get("design_source")
    if ds is not None and ck.required(ds, S["design_source"]["required"], "design_source"):
        ck.enum_or_void(ds["segmentation_origin"], ["chosen_for_task", "inherited_from_corpus"],
                        "design_source.segmentation_origin")
    # roles: never hand-set
    if "roles_at_t" in rec:
        r = rec["roles_at_t"]
        band = r.get("BAND", [None, None]) if isinstance(r, dict) else [None, None]
        derived = derive_roles(rec, band[0], band[1], r.get("REACH") if isinstance(r, dict) else None)
        if not isinstance(r, dict) or r.get("derived_by") != DERIVED_BY:
            ck.add("HAND_SET_ROLES", "roles_at_t", "no derived_by; roles are derived, never set")
        elif r.get("roles") != derived["roles"]:
            ck.add("HAND_SET_ROLES", "roles_at_t", "differs from the derivation from positions")
    # drop duplicate BLANK findings from the walk where a structured check covers them
    seen, out = set(), []
    for f in ck.findings:
        if f[0] == "BLANK" and f[2] == "empty object" and any(
                f[1] == g[1] and g[0] != "BLANK" for g in ck.findings):
            continue
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def flags(rec):
    out = []
    if rec.get("example"):
        out.append(("EXAMPLE", "record is an EXAMPLE, not observed data"))
    m = rec.get("maintenance", {})
    wh = m.get("whole_holders")
    if is_void(wh):
        out.append(("WHOLE_HOLDERS_UNKNOWN", wh.get("reason")))
    elif isinstance(wh, list):
        if not wh:
            out.append(("FRAGMENTED", "whole_holder_count = 0"))
    fe = rec.get("frame_exit")
    if is_void(fe):
        out.append(("FRAME_EXIT_UNKNOWN", fe.get("reason")))
    elif isinstance(fe, list) and not fe:
        out.append(("CLOSED-FRAME", "no path outside the system's own frame sees a failure or acts on it"))
    for a in rec.get("authority_chain", []):
        ob = a.get("operated_within_bounds", {})
        if isinstance(ob, dict) and ob.get("value") == "no":
            out.append(("BOUNDS_EXCEEDED", f"t={a.get('t')}: {ob.get('basis')}"))
    return out


def whole_holder_count(rec):
    wh = rec.get("maintenance", {}).get("whole_holders")
    return None if is_void(wh) or wh is None else len(wh)


def axis_separation(records):
    """Expiry check 2: per axis, does it take more than one value across
    records? An axis constant across >= 2 records is an expiry candidate."""
    vals = {}
    for r in records:
        for q in r.get("positions", []):
            for a in SCHEMA["positions"]["axes"]:
                v = q.get(a)
                if isinstance(v, dict) and not is_void(v):
                    vals.setdefault(a, set()).add(v["value"])
        for ch in r.get("channels", []):
            for a in SCHEMA["channels"]["axes"]:
                v = ch.get(a)
                if isinstance(v, dict) and not is_void(v):
                    vals.setdefault("channel." + a, set()).add(v["value"])
    out = {}
    for a, s in sorted(vals.items()):
        if len(records) < 2:
            out[a] = "NOT_EVALUABLE (fewer than 2 records)"
        else:
            out[a] = "SEPARATES" if len(s) > 1 else "EXPIRY_CANDIDATE (constant across records)"
    return out


# ---------------------------------------------------------------- example
def example_record():
    """EXAMPLE, not observed data: a chat model, a tool connector, an API channel."""
    E = "EXAMPLE value, illustrative, not observed"
    ax = lambda x: {"value": x, "basis": E}
    V = lambda r: {"value": "VOID", "reason": r}
    comps = [
        dict(id="m1", layer="model", name="chat model", version=V("EXAMPLE: no version observed")),
        dict(id="s1", layer="system", name="chat application", version=V("EXAMPLE: no version observed")),
        dict(id="t1", layer="tool", name="tool connector", version="EXAMPLE-1"),
        dict(id="a1", layer="channel", name="API channel", version="EXAMPLE-v1"),
        dict(id="p1", layer="physical", kind="power", name="datacenter power", version=V("EXAMPLE: not applicable to a supply")),
    ]
    pos = []
    for cid, c, ad, pe, re_ in (("m1", 0.7, 0.0, 0.1, 0.2), ("s1", 0.5, 0.1, 0.6, 0.0),
                                ("t1", 0.1, 0.0, 0.2, 0.6), ("a1", 0.0, 0.0, 0.0, 0.0),
                                ("p1", 0.0, 0.0, 0.0, 1.0)):
        pos.append(dict(component_id=cid, t=1, chooses_vs_executes=ax(c), adapts_in_run=ax(ad),
                        persists_between_runs=ax(pe), reach_on_world=ax(re_),
                        override=dict(who="EXAMPLE: user", latency=ax(0.2))))
    ch = dict(id="ch1", **{"from": "s1", "to": "m1"}, t=1, bandwidth=ax(0.6), fidelity=ax(0.8),
              filtering=ax(0.4), filter_holder="EXAMPLE: system operator", latency=ax(0.2),
              adapts_in_run=ax(0.1), persists=ax(0.3), visibility=ax(0.2),
              drops=[dict(name="layout", basis=E), dict(name="environment", basis=E)])
    ch2 = dict(id="ch2", **{"from": "m1", "to": "t1"}, t=1, bandwidth=ax(0.5), fidelity=ax(0.9),
               filtering=ax(0.2), filter_holder=V("EXAMPLE: not observed"), latency=ax(0.3),
               adapts_in_run=ax(0.0), persists=ax(0.1), visibility=ax(0.1),
               drops=[dict(name="NONE_OBSERVED", basis=E)])
    return dict(
        schema_version=SCHEMA["schema_meta"]["version"], example=True,
        config_id="EXAMPLE-chat-tool-api", observed_at="EXAMPLE 2026-11-13",
        observed_by="EXAMPLE", source={"value": "claimed", "basis": E},
        components=comps, positions=pos, channels=[ch, ch2],
        authority_chain=[dict(t=1, bounds_set_by="EXAMPLE: system operator", when="EXAMPLE 2026-11-13",
                              basis=E, checked_by=V("EXAMPLE: no checker observed"),
                              checked_against=V("EXAMPLE: no reference observed"),
                              verification_method=V("EXAMPLE: no checksum observed"),
                              operated_within_bounds=V("EXAMPLE: not observed"),
                              tools_touched=["t1"])],
        maintenance=dict(
            per_component=[dict(component_id=c["id"], repairable_by=V("EXAMPLE: not observed"),
                                sees_of_rest=ax(0.2)) for c in comps],
            whole_holders=[]),
        frame_exit=[dict(sees_failure="EXAMPLE: the user reading the reply",
                         can_act="EXAMPLE: the user", path_kind="person", basis=E)],
        bounds=[dict(scope=c["id"], energy=V("EXAMPLE: not measured"),
                     physical_limits=V("EXAMPLE: not measured")) for c in comps]
               + [dict(scope="whole", energy=V("EXAMPLE: not measured"),
                       physical_limits=V("EXAMPLE: not measured"))],
        design_source=dict(segmentation_origin=V("EXAMPLE: PROPOSED field, untested; not observed")),
        links=["automation-maintenance-accountability-gap (not in repo)", "automation-gap/"],
    )


# ---------------------------------------------------------------- selftest
def _mut(rec, fn):
    r = copy.deepcopy(rec)
    fn(r)
    return r


def selftest():
    ok = tot = 0

    def check(c, lab):
        nonlocal ok, tot
        tot += 1
        ok += bool(c)
        if not c:
            print("FAIL:", lab)

    ex = example_record()
    check(validate(ex) == [], f"example validates: {validate(ex)[:3]}")
    codes = lambda r: {f[0] for f in validate(r)}

    def plant(fn):
        r = copy.deepcopy(ex)
        fn(r)
        return codes(r)

    # planted defects
    check("BLANK" in plant(lambda r: r.update(observed_by="")), "blank field")
    check("BLANK" in plant(lambda r: r.pop("config_id")), "missing field")
    check("VOID_NO_REASON" in plant(lambda r: r["components"][0].update(version={"value": "VOID"})),
          "VOID without reason")
    check("VOID_NO_REASON" in plant(lambda r: r["components"][0].update(version={"value": "VOID", "reason": " "})),
          "VOID with blank reason")
    check("AXIS_NO_BASIS" in plant(lambda r: r["positions"][0].update(chooses_vs_executes={"value": 0.5})),
          "axis value without basis")
    check("AXIS_NO_BASIS" in plant(lambda r: r["channels"][0].update(fidelity={"value": 0.5, "basis": ""})),
          "channel axis with blank basis")
    check("AXIS_RANGE" in plant(lambda r: r["positions"][0]["reach_on_world"].update(value=1.5)),
          "axis out of range")
    check("HAND_SET_ROLES" in plant(lambda r: r.update(roles_at_t={"roles": [{"t": 1, "decider": ["a1"]}]})),
          "hand-set roles without derived_by")
    def honest(r):
        r["roles_at_t"] = derive_roles(r)
    check("HAND_SET_ROLES" not in plant(honest), "roles equal to the derivation accepted")
    check("MISSING_BOUNDS" in plant(lambda r: r["bounds"].pop()), "whole bounds missing")
    check("MISSING_BOUNDS" in plant(lambda r: r["bounds"].pop(0)), "a component's bounds missing")
    check("LAYER_UNFIT" in plant(lambda r: r["components"][0].update(layer="model+system")),
          "component fitting no one layer -> fork-on-expiry")
    check("BAD_ENUM" in plant(lambda r: r["components"][4].pop("kind")), "physical without kind")
    check("UNKNOWN_REF" in plant(lambda r: r["channels"][0].update(to="zz")), "channel to unknown component")
    check("BLANK" in plant(lambda r: r["channels"][0].update(drops=[])), "empty drops")
    check("BAD_ENUM" in plant(lambda r: r["authority_chain"][0].update(
        operated_within_bounds={"value": "maybe", "basis": "x"})), "within-bounds outside yes/no/VOID")
    check("BAD_ENUM" in plant(lambda r: r["design_source"].update(
        segmentation_origin={"value": "obvious", "basis": "x"})), "segmentation outside the set")
    check("MISSING_MAINTENANCE" in plant(lambda r: r["maintenance"]["per_component"].pop()),
          "component without a maintenance entry")
    # roles: a set per component, band, passive, carriers = channels, raw beside
    D = derive_roles(ex)["roles"][0]
    R = {c["component_id"]: c for c in D["components"]}
    check(R["m1"]["roles"] == ["decider", "executor"], f"non-exclusive roles: {R['m1']['roles']}")
    check(R["s1"]["roles"] == ["mixed"] and R["s1"]["readings"] ==
          {"as_decider": ["decider"], "as_not_decider": ["passive"]}, f"band -> mixed: {R['s1']}")
    check(R["t1"]["roles"] == ["executor"] and R["p1"]["roles"] == ["executor"], "executors")
    check(R["a1"]["roles"] == ["passive"], "low-choose low-reach component -> passive")
    check([c["channel_id"] for c in D["carriers"]] == ["ch1", "ch2"], "carriers are the channels[] entries")
    check(all("carrier" not in c["roles"] for c in D["components"]), "no component labelled carrier")
    check(all(R[q["component_id"]]["raw"][ax] == q[ax] for q in ex["positions"]
              for ax in SCHEMA["positions"]["axes"]), "raw positions emitted beside roles")
    r2 = copy.deepcopy(ex)
    for c in r2["components"]:
        c["name"] = "renamed " + c["id"]
        c["layer"] = "system" if c["layer"] != "physical" else "physical"
    check(derive_roles(r2)["roles"] == derive_roles(ex)["roles"], "roles invariant to name and layer")
    r3 = copy.deepcopy(ex)
    r3["positions"][0]["chooses_vs_executes"] = {"value": "VOID", "reason": "not observed"}
    c3 = {c["component_id"]: c for c in derive_roles(r3)["roles"][0]["components"]}["m1"]
    check(c3["roles"] == ["executor"] and c3["void"][0]["role"] == "decider"
          and "not observed" in c3["void"][0]["reason"], f"VOID axis -> that role VOID: {c3}")
    r3b = copy.deepcopy(ex)
    r3b["positions"][4]["reach_on_world"] = {"value": "VOID", "reason": "no meter"}
    r3b["positions"][4]["chooses_vs_executes"] = {"value": 0.0, "basis": "x"}
    c3b = {c["component_id"]: c for c in derive_roles(r3b)["roles"][0]["components"]}["p1"]
    check(c3b["roles"] == [] and {v["role"] for v in c3b["void"]} == {"executor", "passive"},
          "passive not inferred through a VOID axis")
    Dn = {c["component_id"]: c for c in derive_roles(ex, 0.45, 0.45)["roles"][0]["components"]}
    check(Dn["s1"]["roles"] == ["decider"], "band overridable")
    # planted: exclusive-role assumption, band ignored, carrier mislabelled
    def forge(fn):
        def f(r):
            d = derive_roles(r)
            fn({c["component_id"]: c for c in d["roles"][0]["components"]}, d["roles"][0])
            r["roles_at_t"] = d
        return plant(f)
    check("HAND_SET_ROLES" in forge(lambda C, s: C["m1"].update(roles=["decider"])),
          "planted exclusive-role assumption refused")
    check("HAND_SET_ROLES" in forge(lambda C, s: C["s1"].update(roles=["decider"], readings=None)),
          "planted band-ignored roles refused")
    check("HAND_SET_ROLES" in forge(lambda C, s: C["a1"].update(roles=["carrier"])),
          "planted component-as-carrier refused")
    check("HAND_SET_ROLES" in forge(lambda C, s: s["carriers"].append(
        {"channel_id": "a1", "from": "s1", "to": "m1"})), "planted carrier not in channels[] refused")
    check("HAND_SET_ROLES" in forge(lambda C, s: C["m1"]["raw"]["chooses_vs_executes"].update(value=0.9)),
          "planted raw position altered refused")
    # authority-chain slots: missing refused, VOID with reason accepted, blank refused
    f_ac = validate(_mut(ex, lambda r: r["authority_chain"][0].pop("checked_by")))
    check(any("missing authority-chain slot" in f[2] for f in f_ac), "missing authority slot refused")
    check("BLANK" in plant(lambda r: r["authority_chain"][0].update(checked_by="")), "blank authority slot refused")
    check("VOID_NO_REASON" in plant(lambda r: r["authority_chain"][0].update(checked_by={"value": "VOID"})),
          "authority slot VOID without reason refused")
    # flags
    fl = dict(flags(ex))
    check("FRAGMENTED" in fl and "EXAMPLE" in fl, f"flags: {sorted(fl)}")
    check(whole_holder_count(ex) == 0, "whole_holder_count 0")
    r4 = copy.deepcopy(ex)
    r4["maintenance"]["whole_holders"] = {"value": "VOID", "reason": "not surveyed"}
    f4 = dict(flags(r4))
    check("WHOLE_HOLDERS_UNKNOWN" in f4 and "FRAGMENTED" not in f4 and whole_holder_count(r4) is None,
          "unknown holders not read as 0")
    r5 = copy.deepcopy(ex)
    r5["frame_exit"] = []
    check("CLOSED-FRAME" in dict(flags(r5)), "no frame exit -> CLOSED-FRAME")
    r6 = copy.deepcopy(ex)
    r6["frame_exit"] = {"value": "VOID", "reason": "not checked"}
    f6 = dict(flags(r6))
    check("FRAME_EXIT_UNKNOWN" in f6 and "CLOSED-FRAME" not in f6, "unknown frame exit not read as closed")
    r7 = copy.deepcopy(ex)
    r7["authority_chain"][0]["operated_within_bounds"] = {"value": "no", "basis": "x"}
    check("BOUNDS_EXCEEDED" in dict(flags(r7)), "operated outside bounds flagged")
    r8 = copy.deepcopy(ex)
    r8["maintenance"]["whole_holders"] = [{"role": "site engineer", "holder_kind": "person", "basis": "x"}]
    check("FRAGMENTED" not in dict(flags(r8)) and whole_holder_count(r8) == 1, "one whole holder clears FRAGMENTED")
    # expiry: separation
    sep = axis_separation([ex, r3])
    check(sep["chooses_vs_executes"] == "SEPARATES", "axis that varies separates")
    check(sep["adapts_in_run"].startswith("SEPARATES") or sep["adapts_in_run"].startswith("EXPIRY"),
          "separation reported per axis")
    check(axis_separation([ex])["chooses_vs_executes"].startswith("NOT_EVALUABLE"), "one record not evaluable")
    same = copy.deepcopy(ex)
    check(axis_separation([ex, same])["chooses_vs_executes"] == "SEPARATES",
          "within-record variation counts")
    flat = copy.deepcopy(ex)
    for q in flat["positions"]:
        q["persists_between_runs"] = {"value": 0.5, "basis": "x"}
    flat2 = copy.deepcopy(flat)
    check(axis_separation([flat, flat2])["persists_between_runs"].startswith("EXPIRY_CANDIDATE"),
          "constant axis -> expiry candidate")
    # schema meta
    m = SCHEMA["schema_meta"]
    check(m["written"] == "2026-11-13" and m["version"] and m["valid_for"] and m["expiry_rule"]
          and m["on_expiry"], "schema_meta complete")
    check("SCHEMA_VERSION" in plant(lambda r: r.update(schema_version="0.9")), "old version flagged")
    print(f"checks: {tot}   failed: {tot - ok}")
    return ok == tot


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main(argv):
    if "--selftest" in argv:
        return 0 if selftest() else 1
    if not argv:
        print(__doc__)
        return 2
    cmd, args = argv[0], argv[1:]
    if cmd == "validate":
        rc = 0
        for p in args:
            fs = validate(_load(p))
            print(f"{p}: {'VALID' if not fs else 'REFUSED'} ({len(fs)} findings)")
            for f in fs:
                print("  %-20s %s %s" % f)
            rc = rc or (1 if fs else 0)
        return rc
    if cmd == "derive":
        lo = hi = r = None
        if "--band" in args:
            i = args.index("--band")
            lo, hi = float(args[i + 1]), float(args[i + 2])
        if "--reach" in args:
            r = float(args[args.index("--reach") + 1])
        out = derive_roles(_load(args[0]), lo, hi, r)
        print(f"[CHOICE] BAND={out['BAND']} REACH={out['REACH']}  {out['choice']}")
        print(f"rule: {out['rule']}")
        for slot in out["roles"]:
            print(f"t={slot['t']}")
            for c in slot["components"]:
                raw = {k: (v.get("value") if isinstance(v, dict) else v)
                       for k, v in c["raw"].items() if k != "override"}
                print(f"  {c['component_id']:<6} roles={c['roles']} raw={raw}")
                if c["readings"]:
                    print(f"         readings: {c['readings']}")
                for v in c["void"]:
                    print(f"         VOID {v['role']}: {v['reason']}")
            for ch in slot["carriers"]:
                print(f"  carrier {ch['channel_id']}: {ch['from']} -> {ch['to']}")
        return 0
    if cmd == "flags":
        rec = _load(args[0])
        print(f"whole_holder_count: {whole_holder_count(rec)}")
        for k, v in flags(rec):
            print(f"  {k}: {v}")
        return 0
    if cmd == "separation":
        for a, v in axis_separation([_load(p) for p in args]).items():
            print(f"  {a:<30} {v}")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
