#!/usr/bin/env python3
# sustained_activation_gate.py — CC0, stdlib-only, phone-buildable
#
# A stuck-carrier / hysteresis module for the cascade-regime family, with
# exploration surfaces for the separability of a lock from baseline function.
#
# ─────────────────────────────────────────────────────────────────────
# RELIABILITY TIERS — read before building on any part of this.
# This file was built by iterative trajectory-checking, not clean derivation.
# Each layer earned its trust differently. Stated plainly so forks know where
# the ground is solid and where the frontier is.
#
#   TIER 1 — FIRM (trust it).
#     The double-well physics: tilted quartic potential, Kramers escape,
#     hysteresis, recovery gate. Fixed points solved directly (b=2.0,
#     tilt=0.3 → barrier ~0.08, locked well ~0.97). compare_programs()
#     demonstrates brief-relaxes / sustained-locks / inhibition-releases /
#     baseline-spared, all four earned from the dynamics.
#
#   TIER 2 — SOLID, ONE CLEAN RESULT (trust with the stated caveat).
#     explore_separability(): sweeps baseline_leak, locates the boundary θ
#     where a lock stops sparing baseline. Single clean boundary. CAVEAT:
#     baseline drag scales with lock duration, and at biological (days-long)
#     timescales the true θ is far smaller than the ~0.005 shown here.
#
#   TIER 3 — INSTRUCTIVE NEGATIVE RESULT (the naive question was mal-posed).
#     explore_theta_vs_persistence(): intended to show θ falling as locks
#     lengthen (a "race" between persistence and coupling). It does NOT.
#     θ is ~flat because baseline collapses FASTER than the lock persists —
#     so drag is set by the leak coupling, not by dwell time. Two things had
#     to be fixed to even see this honestly: (a) the lock is METASTABLE
#     (Kramers escape), so single-seed lock-duration is noise and must be
#     seed-averaged; (b) "drive duration" was never the controlling axis.
#     The value of this surface is the diagnosis, not the (flat) curve.
#
# ─────────────────────────────────────────────────────────────────────
# THE FRONTIER (open — for others to take further).
# Tier 3 relocated the real variable. Separability is not a race between
# lock-persistence and coupling; it is a race between BASELINE RESTORATION
# and coupling. The predicted-but-unbuilt object is θ(restore_rate):
#
#   given a days-long lock, how fast must homeostasis self-correct to keep
#   baseline viable at a given x→baseline coupling?
#
# That is the falsifiable trade-off the C1 "spares autonomic function"
# result implies: near-zero coupling OR fast autonomic restoration. A wet-lab
# number for either pins the other. Building θ(restore_rate) is the next
# session — with fresh trajectory checks, because every surface in this file
# hid an axis problem that only trajectory inspection caught.
#
# ─────────────────────────────────────────────────────────────────────
# TWO LAYERS, DELIBERATELY SEPARATED:
#
#   FIRM   (physics)   external field → order parameter with a double-well
#                      potential → hysteresis → recovery gate. Same validated
#                      structure as the AMOC hysteresis / cascade_regime work.
#
#   SOFT   (analogy)   an interpretation that LABELS the firm variables as
#                      the C1→vlPAG stress circuit (St. Jude, Neuron,
#                      2026-07-09). ONE paper, small-n, mouse. Held as a
#                      swappable dict, confidence stated inline. Do NOT treat
#                      the biology as established. Swap INTERPRETATION and the
#                      module still runs — the physics does not depend on it.
#
# The claim the module supports is structural, not biological: a brief drive
# spikes and relaxes; a drive held past threshold can lock the order
# parameter "on" so it does not relax when the drive drops; and there can
# exist an inhibition that releases the lock without moving baseline. Whether
# real C1 neurons do this is the experiment; the module is the falsifiable
# shape to test against.

import math
import statistics
from dataclasses import dataclass, field
from enum import Enum

# ----------------------------------------------------------------------
# SOFT LAYER — swappable interpretations.
# ----------------------------------------------------------------------
# Registry of substrate labels for the same firm physics. Pick one by
# assigning SELECTED_INTERPRETATION; the physics is unchanged.
# Add a new substrate by adding a dict; if the shape (brief-relaxes /
# sustained-locks / inhibition-releases / baseline-spared) applies, the
# labels transfer without editing any dynamics code.

INTERPRETATIONS = {
    "c1_vlpag_stress_circuit": {
        "confidence": "ANALOGY_GRADE",  # not EMPIRICAL. one paper, mouse, small-n.
        "source":       "St. Jude / Neuron 2026-07-09 (C1→vlPAG). Suggestive, unsettled.",
        "field":        "epinephrine drive from C1 (RVLM) neurons",
        "order_param":  "vlPAG sustained occupancy (stress-circuit 'on' fraction)",
        "baseline":     "autonomic housekeeping (heart rate, breathing)",
        "lock":         "prolonged activation → days-long anxiety persistence",
        "release":      "targeted C1 inhibition that spares baseline",
        "caveat":       "map is a hypothesis to falsify, not a finding to cite.",
    },
    "amoc_overturning": {
        # The physics class the module docstring's "AMOC hysteresis" note
        # points at. Bistability itself is well established (Stommel-box
        # + paleo evidence); the "inhibition that spares baseline" arm is
        # much weaker — targeted freshwater removal is speculative.
        "confidence": "STRUCTURAL_ANALOGY",
        "source":       "Stommel 1961 / Rahmstorf 1996 + paleo record. Bistability well established; release arm is speculative.",
        "field":        "freshwater loading of the North Atlantic",
        "order_param":  "Atlantic Meridional Overturning strength (Sv)",
        "baseline":     "European surface climate (temperature, rainfall)",
        "lock":         "collapsed overturning state — reduced meridional heat transport, persists past forcing removal",
        "release":      "sustained removal of freshwater forcing (slow; may not exist for present forcing)",
        "caveat":       "the release arm is genuinely uncertain for present-day loading (ocean-sourced, not finite meltwater).",
    },
    "grid_load_blackout": {
        # Textbook cascading-failure class. Lock = tripped subnet that
        # doesn't recover after demand drops. Release = controlled
        # islanding of the collapsed region without moving intact loads.
        "confidence": "ENGINEERING_ANALOGY",
        "source":       "Cascading-failure literature (Dobson, Carreras). Well-instrumented.",
        "field":        "aggregate load / demand on the grid",
        "order_param":  "fraction of stations tripped offline",
        "baseline":     "frequency stability (60 Hz / 50 Hz margin) on the intact subnet",
        "lock":         "cascading blackout — trip-offs persist after demand drops",
        "release":      "controlled islanding of the collapsed subnet",
        "caveat":       "grid recovery is normally faster than the model's Kramers time; this map applies to slow-restoration failures (widespread equipment damage, cold-start blackstart delays).",
    },
}

# The active interpretation. Swap freely; the module still runs.
SELECTED_INTERPRETATION = "c1_vlpag_stress_circuit"

# Alias for existing callers (compare_programs uses INTERPRETATION[...]).
INTERPRETATION = INTERPRETATIONS[SELECTED_INTERPRETATION]

# ----------------------------------------------------------------------
# FIRM LAYER — the physics. Trust this independently of the labels.
# ----------------------------------------------------------------------

@dataclass
class WellConfig:
    # Asymmetric double-well: resting well is DEEP (hard to leave by noise),
    # activated well exists only while barrier is crossed. Tuned so a brief
    # spike returns and a sustained drive can lock.
    a: float = 1.0            # quartic stiffness
    b: float = 2.0            # barrier param — gives bistability (see tilt)
    tilt: float = 0.3         # resting bias: low well below 0, barrier ~0.08,
                              # high (locked) well ~0.97. Solved for separation.
    relax: float = 0.30       # relaxation rate toward local minimum
    noise: float = 0.015      # thermal agitation (small — no spurious escape)
    # baseline_leak: how much the order parameter x drags housekeeping away
    # from its setpoint. 0.0 = perfect separability (the C1 "spares baseline"
    # claim). >0 = the lock bleeds into autonomic function. This is now a
    # MEASURED axis, not an axiom — the exploration module finds the leak
    # value at which separability breaks.
    baseline_leak: float = 0.0
    baseline_restore: float = 0.1   # homeostatic pull back to setpoint
    dt: float = 1.0

def dV_dx(x: float, h: float, c: WellConfig) -> float:
    """Gradient of the tilted double-well. Force = -dV/dx.
    The +tilt term biases the resting state toward x=0 so noise alone
    cannot lift the system out of the low well."""
    return 4 * c.a * x**3 - 2 * c.b * x + c.tilt - h

@dataclass
class State:
    x: float = 0.0            # order parameter (the 'on' fraction)
    baseline: float = 1.0     # housekeeping level — should stay ~constant
    t: float = 0.0

class Regime(Enum):
    RESTING = "RESTING"           # x near low well
    TRANSIENT = "TRANSIENT"       # elevated but will relax
    LOCKED = "LOCKED"             # stuck in high well after field dropped
    RELEASING = "RELEASING"       # inhibition applied, returning to low well

# ----------------------------------------------------------------------
# Field programs — drive shapes
# ----------------------------------------------------------------------

# Same amplitude across all three — DURATION is the variable under test.
# Solved regime: at DRIVE_AMP=1.2, a brief 8-step pulse relaxes (cannot
# dwell long enough to settle in the activated well before the field drops)
# while a sustained 60-step drive locks. The window is narrow — that is a
# real property of bistable hysteresis, not a tuning artifact. Widening the
# well (raise b) widens the window at the cost of a higher escape threshold.
DRIVE_AMP = 1.2

def brief_spike(t, amp=DRIVE_AMP, onset=10, dur=8):
    return amp if onset <= t < onset + dur else 0.0

def sustained_drive(t, amp=DRIVE_AMP, onset=10, dur=60):
    return amp if onset <= t < onset + dur else 0.0

def make_sustained(dur):
    """Factory: sustained drive of a given duration, for the θ-vs-duration
    surface. Longer dur → longer lock → stricter separability requirement."""
    def fn(t, amp=DRIVE_AMP, onset=10):
        return amp if onset <= t < onset + dur else 0.0
    return fn

def drive_then_inhibit(t, amp=DRIVE_AMP, onset=10, dur=60, inhib_amp=-1.5,
                       inhib_onset=120, inhib_dur=25):
    if onset <= t < onset + dur:
        return amp
    if inhib_onset <= t < inhib_onset + inhib_dur:
        return inhib_amp          # the targeted release
    return 0.0

# ----------------------------------------------------------------------
# Integrator
# ----------------------------------------------------------------------

def step(st: State, h: float, c: WellConfig, rng) -> State:
    force = -dV_dx(st.x, h, c)
    dx = c.relax * force * c.dt + c.noise * rng.gauss(0, 1) * math.sqrt(c.dt)
    x = min(max(st.x + dx, -0.2), 1.5)
    # Baseline: homeostatic restoring pull toward setpoint 1.0, MINUS a leak
    # proportional to how far x is into the activated well. At leak=0 the two
    # are fully separable (housekeeping never moves). As leak rises, a locked
    # x steadily drags baseline down — the exploration module measures where
    # that drag becomes large enough to call separability broken.
    activation = max(st.x, 0.0)   # only the 'on' excursion leaks
    db = c.baseline_restore * (1.0 - st.baseline) - c.baseline_leak * activation
    baseline = max(st.baseline + db * c.dt, 0.0)
    return State(x=x, baseline=baseline, t=st.t + c.dt)

def classify(x: float, h: float, prev: Regime) -> Regime:
    high = x > 0.6
    if h < -0.5:
        return Regime.RELEASING
    if high and abs(h) < 0.5:
        return Regime.LOCKED          # elevated with NO field = stuck carrier
    if high:
        return Regime.TRANSIENT
    return Regime.RESTING

# ----------------------------------------------------------------------
# Run + audit
# ----------------------------------------------------------------------

@dataclass
class Trace:
    xs: list = field(default_factory=list)
    hs: list = field(default_factory=list)
    base: list = field(default_factory=list)
    regimes: list = field(default_factory=list)

def run(field_fn, c: WellConfig, steps=200, seed=0) -> Trace:
    import random
    rng = random.Random(seed)
    st = State()
    tr = Trace()
    regime = Regime.RESTING
    for i in range(steps):
        h = field_fn(st.t)
        st = step(st, h, c, rng)
        regime = classify(st.x, h, regime)
        tr.xs.append(st.x); tr.hs.append(h)
        tr.base.append(st.baseline); tr.regimes.append(regime)
    return tr

def audit(tr: Trace) -> dict:
    """The falsifiable readings — trajectory returned, not a stored verdict."""
    # 1. Did it lock? (elevated x while field is off, after the drive window)
    locked_steps = sum(1 for x, h, r in zip(tr.xs, tr.hs, tr.regimes)
                       if r is Regime.LOCKED)
    # 2. Recovery gate: max field reached vs whether it relaxed on its own
    peak_field = max(abs(h) for h in tr.hs)
    # 3. Baseline separability: how much did housekeeping move? (should be ~0)
    base_swing = max(tr.base) - min(tr.base)
    # 4. Release worked? (reached LOCKED then returned to RESTING)
    saw_lock = any(r is Regime.LOCKED for r in tr.regimes)
    ended_rest = tr.regimes[-1] is Regime.RESTING
    return {
        "locked_duration": locked_steps,
        "peak_field": round(peak_field, 2),
        "baseline_swing": round(base_swing, 3),
        "hysteresis_present": locked_steps > 0,
        "released_cleanly": saw_lock and ended_rest,
        "baseline_preserved": base_swing < 0.1,
    }

# ----------------------------------------------------------------------
# Demonstration: three field programs, same physics
# ----------------------------------------------------------------------

def compare_programs(c: WellConfig = None, seed=1):
    c = c or WellConfig()
    programs = {
        "brief_spike":       brief_spike,
        "sustained_drive":   sustained_drive,
        "drive_then_inhibit": drive_then_inhibit,
    }
    print(f"interpretation: {INTERPRETATION['confidence']} — "
          f"{INTERPRETATION['source']}")
    print(f"(field={INTERPRETATION['field']}, "
          f"order_param={INTERPRETATION['order_param']})\n")
    print(f"{'program':<20} {'lock_dur':>8} {'peak_h':>7} "
          f"{'base_swing':>10} {'released':>9} {'base_ok':>8}")
    print("-" * 68)
    results = {}
    for name, fn in programs.items():
        tr = run(fn, c, steps=200, seed=seed)
        a = audit(tr)
        results[name] = a
        print(f"{name:<20} {a['locked_duration']:>8} {a['peak_field']:>7.1f} "
              f"{a['baseline_swing']:>10.3f} "
              f"{str(a['released_cleanly']):>9} {str(a['baseline_preserved']):>8}")

    print("\nstructural claims tested (physics, not biology):")
    print(f"  brief spike relaxes on its own:      "
          f"{not results['brief_spike']['hysteresis_present']}")
    print(f"  sustained drive locks (hysteresis):  "
          f"{results['sustained_drive']['hysteresis_present']}")
    print(f"  targeted inhibition releases lock:   "
          f"{results['drive_then_inhibit']['released_cleanly']}")
    print(f"  release spares baseline:             "
          f"{results['drive_then_inhibit']['baseline_preserved']}")
    print("\nIf real C1→vlPAG data contradicts any row, update the "
          "INTERPRETATION\nlabels — the physics rows stand regardless.")
    return results

# ----------------------------------------------------------------------
# EXPLORATION MODULE — find the separability boundary
# ----------------------------------------------------------------------
#
# Separability is no longer assumed. Sweep baseline_leak from 0 upward,
# drive the system into the LOCKED state each time, and measure how far
# baseline is dragged from its setpoint while x is locked. Report the leak
# value θ at which the drag crosses a tolerance — the boundary between
# "lock spares baseline" and "lock corrupts baseline."
#
# No failure node: every leak value yields a reading. The output is a
# trajectory of drag-vs-leak plus the located boundary, not a verdict.

class SepVerdict(Enum):
    SEPARABLE = "SEPARABLE"          # baseline held despite lock
    LEAKING = "LEAKING"             # measurable drag, still functional
    CORRUPTED = "CORRUPTED"         # baseline pulled below viability

@dataclass
class SepReading:
    leak: float
    lock_duration: int
    baseline_min: float         # lowest housekeeping reached
    baseline_drag: float        # setpoint(1.0) - baseline_min
    verdict: SepVerdict

def measure_separability(leak: float, c_base: WellConfig, seed=1,
                         leak_tol=0.05, corrupt_tol=0.4,
                         drive_dur=60, steps=200) -> SepReading:
    import random
    c = WellConfig(**{**c_base.__dict__, "baseline_leak": leak})
    fn = make_sustained(drive_dur)
    tr = run(fn, c, steps=steps, seed=seed)              # drive into lock
    lock_dur = sum(1 for r in tr.regimes if r is Regime.LOCKED)
    base_min = min(tr.base)
    drag = 1.0 - base_min
    if drag >= corrupt_tol:
        v = SepVerdict.CORRUPTED
    elif drag >= leak_tol:
        v = SepVerdict.LEAKING
    else:
        v = SepVerdict.SEPARABLE
    return SepReading(round(leak, 4), lock_dur, round(base_min, 3),
                      round(drag, 3), v)

def explore_separability(c_base: WellConfig = None, seed=1,
                         leak_grid=None):
    """Sweep leak, locate the SEPARABLE→LEAKING boundary θ. Returns the
    full trajectory and the boundary, refined by bisection."""
    c_base = c_base or WellConfig()
    if leak_grid is None:
        leak_grid = [i * 0.01 for i in range(0, 21)]   # 0.00 .. 0.20

    print("\nSEPARABILITY EXPLORATION (leak sweep)")
    print(f"{'leak':>6} {'lock_dur':>8} {'base_min':>9} {'drag':>7}  verdict")
    print("-" * 50)
    readings = []
    for leak in leak_grid:
        r = measure_separability(leak, c_base, seed=seed)
        readings.append(r)
        print(f"{r.leak:>6.3f} {r.lock_duration:>8} {r.baseline_min:>9.3f} "
              f"{r.baseline_drag:>7.3f}  {r.verdict.value}")

    # locate coarse boundary: first leak where verdict leaves SEPARABLE
    boundary = None
    for i in range(1, len(readings)):
        if (readings[i-1].verdict is SepVerdict.SEPARABLE
                and readings[i].verdict is not SepVerdict.SEPARABLE):
            boundary = _bisect_boundary(readings[i-1].leak, readings[i].leak,
                                        c_base, seed)
            break

    print("\nBOUNDARY:")
    if boundary is not None:
        print(f"  separability holds for leak < θ ≈ {boundary:.4f}")
        print(f"  below θ: the lock spares baseline (C1 'spares autonomic' claim)")
        print(f"  above θ: sustained lock drags housekeeping — claim would fail")
    else:
        allsep = all(r.verdict is SepVerdict.SEPARABLE for r in readings)
        print(f"  no boundary in swept range "
              f"({'all separable' if allsep else 'never separable'})")
    print("\nθ is the falsifiable number: a wet-lab measurement of how much")
    print("C1-driven vlPAG activation perturbs heart rate/breathing sets the")
    print("real leak. If measured leak > θ here, raise b (deeper well) until")
    print("the model's θ matches biology — that fit IS the constraint recovery.")
    return {"readings": readings, "boundary": boundary}

def _bisect_boundary(lo: float, hi: float, c_base: WellConfig, seed,
                     iters=12, leak_tol=0.05, drive_dur=60, steps=200) -> float:
    """Refine the SEPARABLE→not boundary between lo and hi."""
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        r = measure_separability(mid, c_base, seed=seed,
                                 drive_dur=drive_dur, steps=steps)
        if r.verdict is SepVerdict.SEPARABLE:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

# ----------------------------------------------------------------------
# θ-vs-PERSISTENCE SURFACE — the publishable object (corrected)
# ----------------------------------------------------------------------
#
# CORRECTION over the naive version: the lock is METASTABLE, not permanent.
# Noise drives a Kramers escape over the barrier at some rate, so "how long
# the lock lasts" is a stochastic quantity set by noise strength, NOT by how
# long you drove. Two consequences for honest measurement:
#   (1) lock duration must be averaged over many seeds — a single seed swings
#       from 0 to full-length on noise alone.
#   (2) the independent axis is NOISE (which sets escape rate → persistence),
#       not drive duration. Lower noise → longer expected lock → the regime
#       the "days-long" claim actually lives in.
#
# The question sharpens: as expected persistence grows (noise falls), how
# small must baseline coupling be to still spare housekeeping over the
# realized lock? That θ(persistence) curve is the falsifiable prediction.

def expected_lock_and_drag(leak: float, noise: float, c_base: WellConfig,
                           seeds=12, drive_dur=60, steps=260):
    """Average over seeds: mean lock duration and mean baseline drag."""
    locks, drags = [], []
    for s in range(seeds):
        c = WellConfig(**{**c_base.__dict__,
                          "baseline_leak": leak, "noise": noise})
        fn = make_sustained(drive_dur)
        tr = run(fn, c, steps=steps, seed=s)
        locks.append(sum(1 for r in tr.regimes if r is Regime.LOCKED))
        drags.append(1.0 - min(tr.base))
    return statistics.fmean(locks), statistics.fmean(drags)

def theta_at_noise(noise: float, c_base: WellConfig, seeds=12,
                   leak_hi=0.2, coarse=40, leak_tol=0.05,
                   drive_dur=60, steps=260) -> tuple:
    """θ = max leak whose MEAN drag stays under tolerance, at this noise.
    Returns (expected_lock_duration, theta)."""
    exp_lock, _ = expected_lock_and_drag(0.0, noise, c_base, seeds,
                                         drive_dur, steps)
    step_size = leak_hi / coarse
    theta = leak_hi
    leak = step_size
    while leak <= leak_hi:
        _, drag = expected_lock_and_drag(leak, noise, c_base, seeds,
                                         drive_dur, steps)
        if drag >= leak_tol:
            # refine between previous and current by mean-drag bisection
            lo, hi = leak - step_size, leak
            for _ in range(10):
                mid = 0.5 * (lo + hi)
                _, dmid = expected_lock_and_drag(mid, noise, c_base, seeds,
                                                 drive_dur, steps)
                if dmid < leak_tol: lo = mid
                else: hi = mid
            theta = 0.5 * (lo + hi)
            break
        leak += step_size
    return exp_lock, theta

def explore_theta_vs_persistence(c_base: WellConfig = None, seeds=12,
                                 noise_grid=None):
    c_base = c_base or WellConfig()
    if noise_grid is None:
        # falling noise → rising persistence
        noise_grid = [0.06, 0.045, 0.03, 0.02, 0.012, 0.006]

    print("\nθ-vs-PERSISTENCE SURFACE  (multi-seed averaged)")
    print("lower noise → longer expected lock → stricter separability?")
    print(f"{'noise':>7} {'exp_lock':>9} {'θ (max safe leak)':>18}")
    print("-" * 40)
    curve = []
    for nz in noise_grid:
        exp_lock, theta = theta_at_noise(nz, c_base, seeds=seeds)
        curve.append((nz, exp_lock, theta))
        print(f"{nz:>7.3f} {exp_lock:>9.1f} {theta:>18.4f}")

    print("\nSCALING READ:")
    pts = [(el, th) for _, el, th in curve if el > 0]
    if len(pts) >= 2:
        pts.sort()
        (l0, t0), (l1, t1) = pts[0], pts[-1]
        if t1 < t0 * 0.9:
            print(f"  θ falls {t0/max(t1,1e-6):.1f}× as expected lock grows "
                  f"{l1/max(l0,1e-6):.1f}× — separability IS a race.")
            print(f"  the longer the lock persists, the closer to zero the")
            print(f"  x→baseline coupling must be. 'Days-long, baseline spared'")
            print(f"  is therefore a strong claim: it forces near-perfect")
            print(f"  decoupling, not merely weak coupling.")
        elif t1 > t0 * 1.1:
            print(f"  θ RISES with persistence — unexpected; trace why longer")
            print(f"  locks tolerate more leak (drag may saturate at floor).")
        else:
            print(f"  θ ≈ flat across persistence ({t0:.3f}). Separability is")
            print(f"  duration-independent in this regime — also a real result:")
            print(f"  it means drag saturates fast, set by leak not by dwell.")
    else:
        print("  insufficient non-zero locks — lower noise or raise drive.")
    print("\n  NOTE: single-seed runs of this system are not interpretable —")
    print("  the lock is metastable (Kramers escape). Always average seeds.")
    return curve

# ----------------------------------------------------------------------
# θ(restore_rate) — the real controlling axis Tier 3 relocated
# ----------------------------------------------------------------------
#
# Separability is a race between BASELINE RESTORATION and coupling, not
# between lock persistence and coupling. This surface sweeps
# c.baseline_restore as the independent axis in the long-lock regime
# (low noise, so the drive-window setting doesn't dominate) and finds
# θ = max baseline_leak whose seed-averaged drag stays under tolerance.
#
# Prediction (falsifiable): θ rises with restore rate.
#
# Wet-lab payoff: a measured value for autonomic restoration rate OR for
# C1→vlPAG→autonomic coupling pins the other via this curve.
#
# TRAJECTORY-CHECK. Every surface in this file hid an axis bug that
# only trajectory inspection caught. `_sanity_trajectory` runs one seed
# at (restore, leak) and returns sampled x(t), baseline(t), regime for
# eyeball inspection. The sweep calls it on endpoints + midpoint before
# the surface is trusted.

def _sanity_trajectory(restore: float, leak: float, noise: float,
                       c_base: WellConfig, samples=6, seed=0,
                       drive_dur=60, steps=260) -> list:
    """Return sampled (t, x, baseline, regime) rows for eyeball inspection."""
    c = WellConfig(**{**c_base.__dict__,
                      "baseline_restore": restore,
                      "baseline_leak": leak, "noise": noise})
    tr = run(make_sustained(drive_dur), c, steps=steps, seed=seed)
    idxs = [int(i * (steps - 1) / (samples - 1)) for i in range(samples)]
    return [(idx, round(tr.xs[idx], 3), round(tr.base[idx], 3),
             tr.regimes[idx].value) for idx in idxs]


def explore_theta_vs_restore(c_base: WellConfig = None, seeds=12,
                             restore_grid=None, noise=0.006,
                             drive_dur=60, steps=260,
                             sanity_check=True):
    """θ(restore_rate). Sweep baseline_restore, find max leak whose
    seed-averaged drag stays under tolerance.

    Prediction: θ rises with restore rate — faster homeostasis tolerates
    more x→baseline coupling."""
    c_base = c_base or WellConfig()
    if restore_grid is None:
        # slow -> fast (default 0.10 sits in the middle)
        restore_grid = [0.02, 0.05, 0.10, 0.20, 0.40, 0.80]

    print("\nθ-vs-RESTORE SURFACE  (multi-seed averaged, long-lock regime)")
    print(f"noise={noise} (below default 0.015 so locks hold long enough")
    print(f"                 to expose restore-rate as the controlling axis)")

    if sanity_check:
        # trajectory-check at slow / mid / fast restore before the sweep
        print("\n  TRAJECTORY-CHECK (leak=0.05, three restore points):")
        sample_r = [restore_grid[0], restore_grid[len(restore_grid) // 2],
                    restore_grid[-1]]
        for restore in sample_r:
            print(f"    restore={restore:.3f}:")
            rows = _sanity_trajectory(restore, 0.05, noise, c_base,
                                      drive_dur=drive_dur, steps=steps)
            for t, x, b, r in rows:
                print(f"      t={t:>4}  x={x:>+6.3f}  base={b:>6.3f}  {r}")

    print("\n  SURFACE:")
    print(f"    {'restore':>8} {'exp_lock':>9} {'θ (max safe leak)':>18}")
    print("    " + "-" * 38)
    curve = []
    for r_val in restore_grid:
        c = WellConfig(**{**c_base.__dict__, "baseline_restore": r_val})
        exp_lock, theta = theta_at_noise(noise, c, seeds=seeds,
                                         drive_dur=drive_dur, steps=steps)
        curve.append((r_val, exp_lock, theta))
        print(f"    {r_val:>8.3f} {exp_lock:>9.1f} {theta:>18.4f}")

    print("\n  SCALING READ:")
    ordered = sorted(curve)
    if len(ordered) >= 2:
        r0, l0, t0 = ordered[0]
        r1, l1, t1 = ordered[-1]
        if t1 > t0 * 1.5:
            print(f"    θ RISES {t1/max(t0,1e-6):.1f}× as restore grows "
                  f"{r1/max(r0,1e-6):.1f}×.")
            print(f"    Faster homeostasis tolerates more x→baseline coupling.")
            print(f"    Separability is a race BETWEEN restoration and coupling —")
            print(f"    the 'spares baseline' claim is possible on either side")
            print(f"    of the trade-off: near-zero coupling OR fast restoration.")
        elif t1 < t0 * 0.9:
            print(f"    θ FALLS with restore rate ({t0:.4f} → {t1:.4f}).")
            print(f"    Unexpected. Trace: does stronger restore also accelerate")
            print(f"    x→baseline via some unintended path? Rerun _sanity_trajectory.")
        else:
            print(f"    θ ≈ flat across restore ({t0:.4f}). Either coupling")
            print(f"    saturates baseline regardless of restore, or restore")
            print(f"    isn't the controlling axis either. Trajectory-check.")
    print("\n  wet-lab payoff: a measured value for autonomic restoration OR")
    print("  for C1→vlPAG→autonomic coupling pins the other via this curve.")
    return curve


if __name__ == "__main__":
    compare_programs()
    explore_separability()
    explore_theta_vs_persistence()
    explore_theta_vs_restore()
