#!/usr/bin/env python3
"""
presignal_ledger.py — CC0, stdlib only.

Ledger of leading indicators. The person names what to watch and logs when it
fired; the ledger logs when the outcome event happened. The tool scores whether
each early read actually preceded the event, by how much, and how often it was
wrong. Earliness alone never counts as success.

Time is any single numeric unit (hours, days, km) — pick one and keep it.

SCORES PER INDEX (window W = longest lead you will credit)
  hits          fires followed by an event within (t, t+W]
  false_alarms  fires with no event in (t, t+W]
  caught        events preceded by a fire within [T-W, T)
  missed        events with no preceding fire in window
  precision     hits / fires
  chance        fraction of the observed span that sits inside some event's
                pre-window: precision a random or always-on index would get
  lift          precision / chance   (1.0 = no better than noise)
  recall        caught / events
  lead_median   median of (T - earliest fire in window) over caught events
  lead_gain     lead_median minus the baseline index's lead_median
                (baseline = the "obvious" signal, e.g. when it was plain to all)

VERDICTS (judgment of what to watch stays the person's; this only scores it)
  UNDERDETERMINED  fewer than n_min events — not enough record yet
  EARNED           lift >= lift_min, recall >= recall_min, lead_gain > 0
  NOISY_EARLY      early (lead_gain > 0) but lift < lift_min: fires a lot, wrong a lot
  BLIND            recall < recall_min: misses most events
  LATE             lead_gain <= 0: no earlier than the obvious signal
  BASELINE         this is the reference index

USAGE
  python presignal_ledger.py init LEDGER.json START END
  python presignal_ledger.py index LEDGER.json NAME "what is watched" [--baseline]
  python presignal_ledger.py fire  LEDGER.json NAME TIME
  python presignal_ledger.py event LEDGER.json TIME [label]
  python presignal_ledger.py score LEDGER.json WINDOW [n_min lift_min recall_min]
  python presignal_ledger.py selftest
"""
import json
import sys
from statistics import median

DEFAULTS = {"n_min": 5, "lift_min": 1.5, "recall_min": 0.5}


def new_ledger(start, end):
    if end <= start:
        raise ValueError("END must be after START")
    return {"span": [start, end], "indices": {}, "events": []}


def add_index(led, name, desc, baseline=False):
    if baseline:
        for v in led["indices"].values():
            v["baseline"] = False
    led["indices"][name] = {"desc": desc, "baseline": bool(baseline), "fires": []}


def add_fire(led, name, t):
    if name not in led["indices"]:
        raise KeyError("unknown index: " + name)
    led["indices"][name]["fires"].append(float(t))


def add_event(led, t, label=""):
    led["events"].append({"t": float(t), "label": label})


def chance_rate(span, events, W):
    """Fraction of span covered by the union of event pre-windows [T-W, T)."""
    s0, s1 = span
    iv = sorted((max(s0, e - W), min(s1, e)) for e in events)
    covered, cur_a, cur_b = 0.0, None, None
    for a, b in iv:
        if b <= a:
            continue
        if cur_b is None or a > cur_b:
            if cur_b is not None:
                covered += cur_b - cur_a
            cur_a, cur_b = a, b
        else:
            cur_b = max(cur_b, b)
    if cur_b is not None:
        covered += cur_b - cur_a
    return covered / (s1 - s0)


def score_index(fires, events, W):
    fires = sorted(f for f in fires)
    hits = sum(1 for f in fires if any(f < e <= f + W for e in events))
    leads = []
    for e in events:
        prior = [f for f in fires if e - W <= f < e]
        if prior:
            leads.append(e - min(prior))
    n_f = len(fires)
    return {
        "fires": n_f,
        "hits": hits,
        "false_alarms": n_f - hits,
        "caught": len(leads),
        "missed": len(events) - len(leads),
        "precision": hits / n_f if n_f else 0.0,
        "recall": len(leads) / len(events) if events else 0.0,
        "lead_median": median(leads) if leads else None,
    }


def score(led, W, n_min=None, lift_min=None, recall_min=None):
    n_min = DEFAULTS["n_min"] if n_min is None else n_min
    lift_min = DEFAULTS["lift_min"] if lift_min is None else lift_min
    recall_min = DEFAULTS["recall_min"] if recall_min is None else recall_min
    events = [e["t"] for e in led["events"]]
    ch = chance_rate(led["span"], events, W) if events else 0.0
    base_lead = None
    for v in led["indices"].values():
        if v["baseline"]:
            base_lead = score_index(v["fires"], events, W)["lead_median"]
    out = {}
    for name, v in led["indices"].items():
        r = score_index(v["fires"], events, W)
        r["chance"] = ch
        r["lift"] = (r["precision"] / ch) if ch > 0 else None
        if r["lead_median"] is not None and base_lead is not None:
            r["lead_gain"] = r["lead_median"] - base_lead
        elif r["lead_median"] is not None:
            r["lead_gain"] = r["lead_median"]  # no baseline: gain vs the event itself
        else:
            r["lead_gain"] = None
        if v["baseline"]:
            verdict = "BASELINE"
        elif len(events) < n_min:
            verdict = "UNDERDETERMINED"
        elif r["recall"] < recall_min:
            verdict = "BLIND"
        elif r["lead_gain"] is None or r["lead_gain"] <= 0:
            verdict = "LATE"
        elif r["lift"] is None or r["lift"] < lift_min:
            verdict = "NOISY_EARLY"
        else:
            verdict = "EARNED"
        r["verdict"] = verdict
        r["desc"] = v["desc"]
        out[name] = r
    return out


def selftest():
    led = new_ledger(0, 1000)
    add_index(led, "obvious", "plain to everyone", baseline=True)
    add_index(led, "early_true", "subtle index that really leads")
    add_index(led, "early_noisy", "fires constantly")
    add_index(led, "late", "fires after it is obvious")
    add_index(led, "blind", "fires once")
    ev = [100, 250, 400, 600, 850]
    for e in ev:
        add_event(led, e)
        add_fire(led, "obvious", e - 2)
        add_fire(led, "early_true", e - 20)
        add_fire(led, "late", e - 1)
    for t in range(0, 1000, 10):      # always-on: early but no better than noise
        add_fire(led, "early_noisy", t)
    add_fire(led, "blind", 80)
    r = score(led, W=40)
    want = {"obvious": "BASELINE", "early_true": "EARNED",
            "early_noisy": "NOISY_EARLY", "late": "LATE", "blind": "BLIND"}
    for k, v in want.items():
        assert r[k]["verdict"] == v, (k, r[k]["verdict"], v)
    assert r["early_true"]["lead_gain"] == 18
    assert r["early_true"]["false_alarms"] == 0
    assert 0.9 < r["early_noisy"]["lift"] < 1.1     # noise scores as noise
    assert abs(chance_rate([0, 100], [50], 10) - 0.1) < 1e-9
    assert abs(chance_rate([0, 100], [50, 55], 10) - 0.15) < 1e-9  # overlap merged
    led2 = new_ledger(0, 100)
    add_index(led2, "x", "too few events")
    add_fire(led2, "x", 40)
    add_event(led2, 50)
    assert score(led2, 20)["x"]["verdict"] == "UNDERDETERMINED"
    print("selftest ok")


def _load(p):
    with open(p) as f:
        return json.load(f)


def _save(p, led):
    with open(p, "w") as f:
        json.dump(led, f, indent=1)


def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = a[0]
    if cmd == "selftest":
        selftest()
    elif cmd == "init":
        _save(a[1], new_ledger(float(a[2]), float(a[3])))
    elif cmd == "index":
        led = _load(a[1])
        add_index(led, a[2], a[3], baseline="--baseline" in a)
        _save(a[1], led)
    elif cmd == "fire":
        led = _load(a[1])
        add_fire(led, a[2], a[3])
        _save(a[1], led)
    elif cmd == "event":
        led = _load(a[1])
        add_event(led, a[2], a[3] if len(a) > 3 else "")
        _save(a[1], led)
    elif cmd == "score":
        led = _load(a[1])
        extra = [float(x) for x in a[3:6]]
        n_min = int(extra[0]) if len(extra) > 0 else None
        lift_min = extra[1] if len(extra) > 1 else None
        recall_min = extra[2] if len(extra) > 2 else None
        print(json.dumps(score(led, float(a[2]), n_min, lift_min, recall_min), indent=1))
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
