# CLAIM_TABLE — sustained-activation-gate

Every claim is refutable. **Refutation protocol: when a claim fails,
update the claim. Never retune constants to protect a favored surface.**
Results below are from the pinned sample run at
`samples/sustained_activation_gate.sample.txt`, seed=1 for the structural
surface, seed-averaged (12 seeds) for the exploration surfaces.

## Status legend
`SUPPORTED` · `REFUTED` · `INSTRUCTIVE-NEGATIVE` (question was mal-posed) · `SCOPE-LIMITED`

---

## Structural physics (`compare_programs`)

Tier 1 (FIRM). The whole exploration stack rests on these four.

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| **SG_001** | A brief drive spike relaxes on its own — no lock forms. | **SUPPORTED** | `brief_spike`: `locked_duration = 0`, ended RESTING. |
| **SG_002** | A sustained drive past threshold locks the order parameter — hysteresis. Elevated x persists after the drive drops. | **SUPPORTED** | `sustained_drive`: `locked_duration = 129`, `hysteresis_present = True`. |
| **SG_003** | A targeted inhibition (negative pulse) can release the lock — the system returns to RESTING. | **SUPPORTED** | `drive_then_inhibit`: `released_cleanly = True`, ended RESTING after LOCKED. |
| **SG_004** | Release spares baseline when `baseline_leak = 0`. | **SUPPORTED** | `drive_then_inhibit`: `baseline_swing = 0.000`, `baseline_preserved = True`. |

**Refuted if any row of `compare_programs()` output changes.** These are
the load-bearing outputs. Constants are frozen; if the row flips, the
CLAIM changes — or a WellConfig invariant has drifted and needs
diagnosis, not tuning.

---

## Separability boundary (`explore_separability`)

Tier 2 (SOLID, one clean result).

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| **SG_005** | There exists a leak boundary θ below which a sustained lock spares baseline and above which it corrupts baseline. | **SUPPORTED** | Bisection converges to **θ ≈ 0.0052** at default `WellConfig`. |
| **SG_005a** | Verdict progression is monotonic in leak: SEPARABLE → LEAKING → CORRUPTED. | **SUPPORTED** | Grid sweep 0.00 → 0.20 shows SEPARABLE only at 0.000, LEAKING at 0.010–0.040, CORRUPTED at 0.050+. No verdict skipping or reversal. |
| **SG_005b** | θ is not universal — it scales with `WellConfig.b` (well depth). Deeper wells hold longer locks and require smaller leak. | **SCOPE-LIMITED (pinned at default config)** | Not directly measured in the pinned run; documented as CAVEAT in the module header. Building a θ(b) surface would test this. |

**Refuted if:** a config with the same `b` and `tilt` shows SEPARABLE at
a leak > 0.006 in the seed-averaged surface; or the verdict progression
skips a state in either direction under monotonic leak.

---

## Persistence axis (`explore_theta_vs_persistence`)

Tier 3 (INSTRUCTIVE NEGATIVE). The naive "θ falls with lock duration"
question was mal-posed. Two things had to be fixed to see this honestly.

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| **SG_006** | The lock is metastable (Kramers escape), so single-seed lock durations swing 0 → full-length on noise alone. Must seed-average. | **SUPPORTED** | `exp_lock` at noise 0.006 varies 94.8 → 173.2 across the noise grid — noise-driven, not drive-driven. Seed averaging (12 seeds) is what makes the numbers interpretable. |
| **SG_006a** | θ is duration-independent in the metastable regime — drag saturates fast, set by leak not by dwell time. | **INSTRUCTIVE-NEGATIVE (this was the naive prediction; the honest result is flat)** | θ = 0.0052 ± 0.0002 across noise 0.006 → 0.060 (persistence factor ~2×). The scaling-read fires the "θ ≈ flat" branch. |
| **SG_006b** | Drive duration is not the controlling axis; noise (which sets Kramers escape rate) is. | **SUPPORTED** | Held drive_dur fixed at 60 across the sweep; θ moved only with noise, and moved not at all with lock duration. |

**Refuted if:** the same sweep, run at higher noise or shorter drive_dur,
shows θ moving > 20% across the persistence factor.

---

## θ(restore_rate) — the frontier surface

Tier 3 diagnosed that separability is a race between baseline restoration
and coupling, not between persistence and coupling. This surface tests
that relocated axis.

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| **SG_007** | θ rises with `baseline_restore`. Faster homeostasis tolerates more x→baseline coupling. | **SUPPORTED** | θ moves 0.0013 → 0.0307 as restore moves 0.02 → 0.80 — **23.9× rise for 40× restore**. Scaling-read fires the "θ RISES" branch. |
| **SG_007a** | The "spares baseline" claim is possible on either side of the trade-off — near-zero coupling OR fast restoration. | **SUPPORTED** | Below θ at any restore, baseline_swing < leak_tol. Same viability from two very different substrate physics: slow homeostasis + tiny coupling, or fast homeostasis + moderate coupling. |
| **SG_007b** | Trajectory-check catches axis bugs the aggregate surface hides. | **SUPPORTED (methodological)** | `_sanity_trajectory` at slow / mid / fast restore shows baseline settling at 0.000 / 0.762 / 0.937 — the exact restoration-vs-coupling race the summary curve represents. If the trajectory-check output ever disagrees with the surface, the surface is wrong; do not trust the smooth curve. |

**Refuted if:** the same sweep, seed-averaged, shows θ flat or falling
across the same restore factor; OR trajectory-check at any restore point
shows baseline behavior incompatible with the surface value.

**Wet-lab payoff:** a measured value for autonomic restoration rate OR
for the order-parameter → baseline coupling pins the other via this
curve. Either measurement falsifies the other's SOFT-tier assumption.

---

## Interpretation swap (SOFT layer)

The registry pattern claim.

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| **SG_100** | Swapping `SELECTED_INTERPRETATION` between the registered dicts changes only the printed labels, not any physics reading. | **SUPPORTED** | `INTERPRETATION` is a computed alias into `INTERPRETATIONS`; `compare_programs()` reads `field` and `order_param` from it for the header line but nothing else. No dynamics function references any interpretation key. |
| **SG_100a** | Adding a new interpretation dict is safe as long as the substrate's shape matches (brief-relaxes / sustained-locks / inhibition-releases / baseline-spared). | **SUPPORTED (by construction)** | The dict is opaque to the dynamics; the four-row shape is what the module actually measures. If a substrate doesn't have the release arm, the "spares baseline" claim is not the right claim for that substrate — the interpretation should say so in its `caveat` field. |

**Refuted if:** a change to `SELECTED_INTERPRETATION` changes any
numerical column in `compare_programs()`, `explore_separability()`,
`explore_theta_vs_persistence()`, or `explore_theta_vs_restore()`. Any
such divergence is a bug in a dynamics function that unexpectedly
depends on a label.

---

## Scope bounds

- All θ values are for the shipped `WellConfig` (`b=2.0`, `tilt=0.3`,
  `relax=0.30`). Deeper wells, different tilts, or different relax rates
  produce different θ — that θ scales with these config choices is
  itself a testable claim not surveyed here.
- The `long-lock regime` for the frontier surface uses `noise=0.006`,
  below the default 0.015, so the Kramers escape time is much longer
  than the drive window. At higher noise the trade-off surface exists
  but is smeared by faster escapes.
- The three shipped interpretations map the same physics to biology,
  geophysics, and infrastructure. The `caveat` field of each dict names
  the specific dimension where the analogy is weakest — read it before
  citing a numerical θ against any real substrate.
