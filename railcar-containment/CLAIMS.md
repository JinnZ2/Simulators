# CLAIMS — railcar_containment

Each claim states what would falsify it. Status is what the folder currently supports,
not what is established.

---

**RC_001 — The published tenability window is a floor for smaller cars.**
For the same vent-gas release, a smaller cabin volume reaches any concentration
threshold sooner. Direction of the bias is knowable without the absolute number.
*Falsified if:* measured tenability in a metro-volume car equals or exceeds the
intercity result at matched device and placement.
*Status:* model result, `tenability.py`. Sign is structural; magnitude is calibrated,
not measured.

---

**RC_002 — Containment fraction dominates cabin volume.**
Reducing the fraction of vent gas that reaches the breathing volume moves
`t_available` more than any realistic difference in car volume does.
*Falsified if:* an enclosure achieving ≤20% cabin gas fraction fails to extend
`t_available` beyond the volume effect in a full-scale test.
*Status:* model result. Untested. The enclosure performance figure is assumed, not
demonstrated.

---

**RC_003 — Required hold time is derivable from timetable and track data alone.**
`t_hold` follows from detection latency, decision latency, run-to-egress time, door
release and clearance time. No fire testing is needed to state the requirement.
*Falsified if:* a line's worst-case egress interval cannot be bounded from
operational data.
*Status:* demonstrated in `t_hold.py` against illustrative line parameters. Needs real
line data.

---

**RC_004 — Visual smoke is a late trigger by construction.**
Devices in the FSRI runs typically smoked only seconds before igniting, so a trigger
that waits for cabin smoke inherits that lateness. Off-gas sensing inside a sealed
enclosure fires before flaming.
*Falsified if:* off-gas signatures detectable at practical sensor thresholds do not
precede flaming by a usable margin, or if cabin smoke is reliably noticed and reported
faster than modelled.
*Status:* the precedence is physical; the usable-margin part is assumed and is the
weakest link in the folder. This is the first thing to test on a bench.

---

**RC_005 — In the tunnel case, detection alone does not rescue the outcome.**
Where egress requires a tunnel walkout, moving detection from visual to sensor barely
changes P(clear); containment changes it substantially.
*Falsified if:* a timeline model with realistic latencies shows detection improvement
closing the gap without containment.
*Status:* model result, `detection_loop.py`. This is the folder's least obvious output
and the one most worth attacking.

---

**RC_006 — Containment is device-agnostic where a ban is not.**
An enclosure treats a wheelchair pack, a delivery-bike pack and a certified scooter
pack identically, because it acts after initiation and does not require knowing whose
device it is.
*Falsified if:* enclosure sizing or hold time turns out to depend on device class in a
way that cannot be covered by a single worst-case specification.
*Status:* argued, not modelled. Sizing to worst-case capacity is the open question, and
capacity data was not retrieved.

---

**RC_007 — Capacity is a severity term, not a probability term.**
`risk = P(initiation) × severity|ignition`. Pack capacity sits almost entirely in the
second factor; P(initiation) is set by cell quality, BMS, pack architecture, charge
management, mechanical protection and abuse history. A size restriction therefore does
not reduce the number of events.
*Falsified if:* incident-rate data shows P(initiation) rising with capacity after
controlling for certification status, pack architecture and use pattern.
*Status:* decomposition, not a measurement. The controlling-for part is exactly what
published incident data does not currently support.

---

**RC_008 — The exclusion cost has no bearer in the current analysis.**
Fire testing measures harm from the device present. Nothing measures harm from the
device absent: displaced trips, mode shift, and the injury/exposure rate of the
substituted mode.
*Falsified if:* a published transit analysis includes the substituted-mode term.
*Status:* not modelled here either. Flagged rather than silently omitted.

---

## NOT CLAIMED

- No absolute tenability prediction for any real car, device or line.
- No claim that a ban is or is not warranted. The folder shows two levers that do not
  require the category question to be answered.
- No claim about anyone's intentions in any regulatory process.
