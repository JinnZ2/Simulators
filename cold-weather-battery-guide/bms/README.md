# BMS Sketches

Two Arduino sketches for the cold-weather ester-cell battery.

## `bms_1s_basic.ino` — start here

Minimal single-cell (1S) LFP protection: overvoltage / undervoltage /
overcurrent / charge-temperature lockout. Runs on an Arduino Nano or
Uno with an INA219 current sensor and one NTC thermistor.

Good for benching a first ester cell and confirming the electrolyte
survives a real charge/discharge cycle without gassing itself apart.

## `bms_1s_merged.ino` — the full system

Same electrical BMS, plus:

- **Thermal state machine** (STANDBY / PREHEAT / CHARGE_WAIT /
  OVERHEAT_PROTECT). Drives a damper servo and PWM fan to move heat
  from a Fresnel-heated solar block into the battery box when the
  battery is too cold to charge.
- **Predictive sunrise detection** — a photoresistor plus a 30-minute
  stability window predicts when the solar block will be hot enough
  to preheat. Lights a blue LED when the prediction fires.
- **PIR "jeans protection" safety shutter** — an HC-SR501 PIR sensor
  triggers a servo-driven shutter that blocks the Fresnel focal spot
  whenever motion enters the danger zone, plus a continuous buzzer
  while motion persists. Do not skip this one.

## Pin table (bms_1s_merged.ino)

| Pin | Function | Notes |
|---|---|---|
| A0 | Cell voltage (via 100k+10k divider to GND) | ratio ~11:1 |
| A1 | Battery NTC (10k @ 25°C, 10k series to 5V) | Beta 3950 |
| A2 | Block NTC (same divider) | Swap for MAX6675 thermocouple if block >250°C |
| A3 | Photoresistor + 10k to GND | Sunrise sensor |
| A4 / A5 | INA219 I²C (SDA / SCL) | 0.01 Ω shunt in battery negative lead |
| D2 | PIR motion input (HC-SR501, 5V) | HIGH = motion |
| D3 | Discharge MOSFET gate (IRLZ44N) | 100 Ω series, 10k pulldown |
| D4 | Charge relay via 2N2222 NPN + flyback diode | 12V relay coil |
| D5 | Fan MOSFET gate (PWM) | IRLZ44N + 10k pulldown |
| D6 | Damper servo signal (SG90) | 5V |
| D7 | Shutter servo signal (SG90) | 5V |
| D8 | OK LED (green) | 220 Ω series |
| D9 | Fault LED (red) | 220 Ω series |
| D10 | Buzzer (piezo, 5V) | Direct drive |
| D11 | Sunrise-predicted LED (blue) | 220 Ω series |

All grounds common. Power the Arduino from USB or a 12V step-down.
Cell voltage divider must include a shunt to GND (10k) so the ADC
sees a bounded voltage; the 100k+10k values give a 3.65 V cell a
~0.33 V reading — safely inside the 5 V ADC range.

## Calibration

- **Voltage divider:** measure your actual 100k and 10k with a
  multimeter and update `VOLTAGE_DIVIDER_RATIO`. A 1% pair is
  usually within 0.5% of nominal.
- **NTCs:** if your thermistor's Beta or nominal resistance differ,
  update `NTC_BETA` / `NTC_NOMINAL_RES`. Verify against a known
  temperature (ice water = 0°C, boiling water = 100°C at sea level).
- **Current range:** `setCalibration_16V_400mA()` in `setup()` picks
  the INA219 range. For a bigger battery use `setCalibration_32V_2A()`
  and update `OVERCURRENT_A`.
- **Servo positions:** the `0` and `90` degree values assume a
  particular damper/shutter geometry. Verify open/close mechanically
  before energizing anything hot.
- **Sunrise threshold:** `LIGHT_THRESHOLD = 30` percent and a
  30-minute confirm window are placeholders — tune to your specific
  photoresistor and thermal-mass time constant.
- **PIR sensitivity:** HC-SR501 has two pots on the board — set
  sensitivity high and delay to minimum, since we want the shutter
  to close immediately when motion is detected.

## Testing procedure

1. Bench-test with a variable power supply in place of the cell.
   Ramp voltage across the OV / UV thresholds and confirm the relay
   clicks and MOSFET switches. Watch the LEDs.
2. Simulate low temperature by wrapping the battery NTC around an
   ice cube (or dropping into a glass of ice water). Confirm the
   charge relay drops out when the reading goes below -10°C.
3. Simulate overcurrent by shorting through a low-value power
   resistor (short-duration only). Confirm the delayed trip fires
   after ~500 ms.
4. Wave a hand in front of the PIR sensor. Confirm the shutter
   servo swings closed and the buzzer sounds.
5. Only then take the whole thing outside near the Fresnel array.

## Scaling to 4S

The merged sketch is 1S. For a 4S LFP pack (12 V nominal), the
minimum additions are:

- A CD4051 8-channel analog multiplexer to sequentially read four
  cell taps (with dividers so each tap stays under 5 V), select
  lines on D8-D10. `analogRead(A0)` becomes a per-channel loop.
- A high-side charge disconnect — either a 40 A automotive 12 V
  relay driven by an NPN transistor (simplest, most robust for
  breadboard work), or a bootstrap-driven P-channel MOSFET with a
  small isolated DC-DC and optocoupler (compact but harder to
  debug).
- Passive balancing per cell if the pack drifts — 100 Ω + 1 W bleed
  resistor per cell switched by a small MOSFET, one optocoupler per
  channel to bridge the ground shift between cells. Or skip and
  balance manually with a hobby charger during pack service.

Not implemented here — the source conversation flagged the 4S
schematic as a next step but did not draw it.

## What these sketches are not

- **Not certified.** No BMS chip qualification, no UN 38.3, no UL.
  This is a learning and testing rig, not a shippable product.
- **Not a substitute for pack-level protection.** A hardware fuse
  in the battery negative lead and a proper enclosure vent are
  still required.
- **Not a substitute for reading the ester-cell chemistry section
  before energizing.** LiPF6 + moisture = HF gas. See
  `../index.html` sections on the dry box and formation cycling.

CC0.
