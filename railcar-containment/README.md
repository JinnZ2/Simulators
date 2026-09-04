# railcar_containment

Three runnable screens for the e-mobility-fire-on-railcar problem, built around one inequality.

**License:** CC0. **Deps:** Python 3 stdlib only. No network at runtime. Phone-runnable.

---

## THE INEQUALITY

```
t_available  =  time until cabin conditions block escape
t_required   =  time until occupants can actually leave

survivable  <=>  t_available > t_required
```

Published measurement gives one side only. FSRI 2026 (DOI 10.60752/102376.32136697) measured
`t_available` at 3 min 37 s to 7 min 8 s after ignition, in a single-level intercity commuter
railcar, stationary, with suppression crew on site. The report states it did **not** measure
required safe egress time, and cites prior evacuation research suggesting available time is less
than required time.

So the policy question is being decided on one measured term and one unmeasured term.

Two engineering branches attack the same inequality from opposite sides:

```
STORAGE   raise t_available   -> decouple the vent path from the breathing volume
EGRESS    lower t_required    -> run to next station, don't stop in tunnel
```

Neither requires knowing whose device it is, which is the property a category-based ban lacks.

---

## WHAT'S HERE

| file | question it answers |
|---|---|
| `tenability.py` | how does `t_available` move with car volume and with containment fraction? |
| `t_hold.py` | how long must a containment enclosure hold, per line geometry? |
| `detection_loop.py` | does off-gas detection change the outcome, given real latencies? |
| `run_all.py` | runs all three against `params/example_lines.json` |

```
python3 run_all.py
python3 tenability.py --volume 100 --contained 0.05
python3 t_hold.py --lines params/example_lines.json
python3 detection_loop.py --trials 20000 --arm sensor
```

---

## ENVELOPE OF THESE SIMS

Stated here because the whole point of the exercise is that claims should carry one.

```
VALID FOR
  order-of-magnitude comparison BETWEEN configurations
  sensitivity of t_available to car volume
  sensitivity of outcome to detection latency
  deriving a t_hold REQUIREMENT from line geometry

NOT VALID FOR
  absolute tenability prediction
  certification, design sign-off, or code compliance
  any specific device, pack chemistry, or car
  any claim about a real transit line

DEGRADATION MODE
  well-mixed assumption fails early and near the source; the model
  UNDERSTATES local hazard within a few metres of the device and
  overstates uniformity along the car

REVALIDATION TRIGGER
  replace the source term with measured vent-gas mass rate and HRR
  from the FSRI dataset; recalibrate before any quantitative use

MARGIN
  none applied. outputs are nominal. apply your own.
```

`tenability.py` is **calibrated to the published window**, not derived from first principles:
the source term is scaled so the uncontained intercity case lands inside 3:37–7:08. Everything
downstream is a ratio against that anchor. Change the anchor, everything moves.

---

## WHY STORAGE IS THE TRACTABLE BRANCH

- retrofittable per car; bench-testable before it sees a train
- doesn't require knowing which device the passenger brought
- bypasses the category problem: a wheelchair pack, a delivery-bike pack and a certified scooter
  pack all get the same treatment, because containment doesn't care whose device it is

Detection couples the branches. Off-gassing precedes flaming, and devices in the FSRI runs
typically smoked only seconds before igniting — so **visible smoke is too late as a trigger**,
while off-gas sensing inside a sealed enclosure is not.

---

## SUBSTITUTION TERM — NOT MODELLED, AND IT MATTERS

If a carriage ban displaces first/last-mile trips to cars and gas motorbikes, the trade is a rare
high-consequence event against a continuous distributed one, and the second does not appear in
transit's numbers at all. Nothing in this folder models it. The metric it would need:

```
displaced trips  x  substituted-mode injury/exposure rate
        vs
fire incidents per million device-journeys
```

Flagged as a missing denominator rather than silently omitted.

---

## SOURCE CAVEAT

Battery capacities and the full test matrix were not retrieved when this folder was written; the
FSRI landing page does not carry them and the figshare PDF blocked automated access. Every number
attributed to the report above comes from the landing page and press release. **Verify against the
report before quantitative use.**
