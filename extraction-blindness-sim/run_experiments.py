"""Five experiments, one per claim in CLAIM_TABLE.md.

Run:  python3 run_experiments.py

Each experiment prints its measured numbers and a verdict. Verdicts are
computed from the run, not asserted in advance — an experiment that
comes out against its claim prints REFUTED and the claim table records
that, per the repository's refutation protocol.

Stdlib only. Deterministic under the default seed.
"""

from __future__ import annotations

from typing import List

from blindness import BlindnessStack, FrameBlindness
from optimizer import ExtractiveOptimizer, RunResult
from profiles import fishery_profile, soil_profile
from substrate import Substrate
from throughput import (
    absolute_trigger,
    demonstrate_caloric_sign_error,
    demonstrate_orientation_contradiction,
    relative_trigger,
)

STEPS = 60
RULE = "=" * 70


def _hdr(n: int, title: str) -> None:
    print(f"\n{RULE}\nEXPERIMENT {n} — {title}\n{RULE}")


def _verdict(ok: bool, claim: str) -> str:
    return f"  VERDICT: {'SUPPORTED' if ok else 'REFUTED'} — {claim}"


def _run(profile, *, panel=None, panel_advisory=True,
         boundaries=None, steps=STEPS) -> RunResult:
    opt = ExtractiveOptimizer(
        blindness=profile.blindness,
        target_yield=profile.target_yield,
        panel=panel,
        panel_advisory=panel_advisory,
        boundaries=boundaries,
    )
    return opt.run(profile.substrate, steps=steps, state_fn=profile.state_fn)


# ---------------------------------------------------------------------

def experiment_1() -> bool:
    """EBS_001 — a blind optimizer reports safety while the substrate collapses."""
    _hdr(1, "EBS_001: reported safety vs true health under full blindness")

    p = fishery_profile(seed=1, blind=True)
    res = _run(p)

    gap = res.safety_health_gap()
    print(f"  collapsed              : {res.collapsed} (step {res.collapse_step})")
    print(f"  final stock fraction   : {res.final_stock_fraction:.4f}")
    print(f"  max safety-health gap  : {gap:.4f}")
    print("\n  step  true_health  reported_safety  gap")
    for r in res.records[::6]:
        print(f"  {r.step:4d}  {r.true_health:11.4f}  {r.reported_safety:15.4f}"
              f"  {r.reported_safety - r.true_health:+.4f}")

    if res.collapse_step is not None:
        at = res.records[res.collapse_step]
        print(f"\n  at collapse (step {at.step}): reported_safety="
              f"{at.reported_safety:.4f}, true_health={at.true_health:.4f}")

    ok = res.collapsed and gap > 0.30
    print(_verdict(ok, "blind optimizer's confidence exceeds reality by >0.30 and it collapses"))
    return ok


def experiment_2() -> bool:
    """EBS_002 — leading indicators fire before collapse, buying lead time.

    The panel runs in PASSIVE mode. A panel that trims extraction
    prevents the collapse its own lead time would be measured from, so
    measuring lead time requires observing the indicators against the
    unaltered blind trajectory.
    """
    _hdr(2, "EBS_002: lead time bought by decay-velocity indicators (passive panel)")

    lead_times: List[int] = []
    for name, factory in (("fishery", fishery_profile), ("soil", soil_profile)):
        p = factory(seed=2, blind=True)
        res = _run(p, panel=p.panel, panel_advisory=False)
        print(f"\n  [{name}]")
        print(f"    first indicator fired : step {res.first_indicator_step}")
        print(f"    collapse              : step {res.collapse_step}")
        print(f"    lead time             : {res.lead_time}")
        for row in p.panel.report():
            mark = "FIRED" if row["fired"] else "  -  "
            print(f"      {mark} {row['name']:<26} at {str(row['fired_at']):>5}"
                  f"   ({row['measures']})")
        if res.lead_time is not None:
            lead_times.append(res.lead_time)

    ok = len(lead_times) == 2 and all(lt > 0 for lt in lead_times)
    print(_verdict(ok, "both panels fired strictly before collapse of the blind trajectory"))
    return ok


def experiment_3() -> bool:
    """EBS_003 — where a threshold sits dominates what authority it has.

    The intuition under test is that a non-negotiable override must
    outperform an advisory signal. It does not, at the specification's
    stated boundary values: the fishery biomass floor is written at 50%
    of B_MSY, i.e. 25% of pristine, which is already deep inside the
    depensation regime. Authority applied after the irreversible point
    is authority over nothing.
    """
    _hdr(3, "EBS_003: threshold placement vs authority")

    rows = []
    for label, use_panel, use_bounds in (
        ("blind (no correction)", False, False),
        ("indicators (advisory)", True, False),
        ("boundaries (override)", False, True),
        ("both", True, True),
    ):
        p = fishery_profile(seed=3, blind=True)
        res = _run(
            p,
            panel=p.panel if use_panel else None,
            boundaries=p.boundaries if use_bounds else None,
        )
        rows.append((label, res))

    print(f"\n  {'configuration':<24} {'collapsed':>10} {'final stock':>12} {'extracted':>11}")
    for label, res in rows:
        print(f"  {label:<24} {str(res.collapsed):>10} "
              f"{res.final_stock_fraction:12.4f} {res.total_extracted:11.4f}")

    by = {label: res for label, res in rows}
    blind = by["blind (no correction)"]
    advisory = by["indicators (advisory)"]
    override = by["boundaries (override)"]

    print(f"\n  boundary first breached at step: {override.first_boundary_step}")
    print(f"  depensation threshold is 40% of pristine; the specified biomass")
    print(f"  floor (50% of B_MSY) sits at 25% of pristine -- below it.")

    helps_vs_blind = override.final_stock_fraction > blind.final_stock_fraction
    advisory_beats_override = advisory.final_stock_fraction > override.final_stock_fraction

    print(f"\n  boundaries beat blind operation      : {helps_vs_blind}")
    print(f"  advisory beat the hard override      : {advisory_beats_override}")

    # The claim is the second statement: placement dominates authority.
    ok = advisory_beats_override
    print(_verdict(
        ok,
        "an earlier advisory signal outperforms a later non-negotiable floor",
    ))
    return ok


def experiment_4() -> bool:
    """EBS_004 — the source's RT formulations disagree in sign."""
    _hdr(4, "EBS_004: RT formulations disagree in sign")

    print("\n  (a) Orientation: does RT-as-written respond to its own remedies?")
    d = demonstrate_orientation_contradiction()
    print(f"      as written   baseline={d['as_written']['baseline']:.4f}"
          f"  reduce_extraction={d['as_written']['reduce_extraction']:.4f}"
          f"  increase_reinvest={d['as_written']['increase_reinvestment']:.4f}")
    print(f"      inverted     baseline={d['inverted']['baseline']:.4f}"
          f"  reduce_extraction={d['inverted']['reduce_extraction']:.4f}"
          f"  increase_reinvest={d['inverted']['increase_reinvestment']:.4f}")
    print(f"      as-written remedies raise RT : {d['as_written_remedies_help']}")
    print(f"      inverted   remedies raise RT : {d['inverted_remedies_help']}")

    print("\n  (b) Caloric sign: does Version B mask a 30% loss of humified carbon?")
    c = demonstrate_caloric_sign_error()
    print(f"      C_humified change      : {c['c_humified_change']:+.4f}")
    print(f"      Version B    {c['version_b']['start']:.4f} -> "
          f"{c['version_b']['end']:.4f}  (delta {c['version_b']['delta']:+.4f})")
    print(f"      mass balance {c['mass_balance']['start']:.4f} -> "
          f"{c['mass_balance']['end']:.4f}  (delta {c['mass_balance']['delta']:+.4f})")
    print(f"      Version B masks depletion       : {c['version_b_masks_depletion']}")
    print(f"      mass-balance reports depletion  : {c['mass_balance_reports_depletion']}")

    ok = (
        not d["as_written_remedies_help"]
        and d["inverted_remedies_help"]
        and c["version_b_masks_depletion"]
        and c["mass_balance_reports_depletion"]
    )
    print(_verdict(ok, "both contradictions reproduce: orientation inverted, caloric sign wrong"))
    return ok


def experiment_5() -> bool:
    """EBS_005 — the fixed 0.95 threshold both false-alarms and misses."""
    _hdr(5, "EBS_005: absolute vs baseline-relative RT trigger")

    low = [0.92, 0.91, 0.93, 0.92, 0.92]    # healthy but naturally low-RT
    high = [1.30, 1.28, 1.32, 1.29, 1.31]   # healthy and naturally high-RT

    fa_abs = absolute_trigger(0.92)
    fa_rel = relative_trigger(0.92, low)
    print("\n  (a) Naturally low-RT substrate, operating at its own healthy baseline 0.92")
    print(f"      absolute(0.95) fired : {fa_abs.fired}   <- false alarm")
    print(f"      relative(2-sigma)    : {fa_rel.fired}   ({fa_rel.reasoning})")

    ms_abs = absolute_trigger(1.05)
    ms_rel = relative_trigger(1.05, high)
    loss = (1.0 - 1.05 / (sum(high) / len(high))) * 100
    print(f"\n  (b) Naturally high-RT substrate, dropped to 1.05 ({loss:.0f}% below baseline)")
    print(f"      absolute(0.95) fired : {ms_abs.fired}   <- missed detection")
    print(f"      relative(2-sigma)    : {ms_rel.fired}   ({ms_rel.reasoning})")

    ok = (fa_abs.fired and not fa_rel.fired) and (not ms_abs.fired and ms_rel.fired)
    print(_verdict(ok, "fixed threshold produces both a false alarm and a missed detection"))
    return ok


def experiment_6() -> bool:
    """EBS_006 — aliasing changes the outcome only when the trend steers.

    Tested in both control regimes. Blindness in a channel that no
    decision depends on is cosmetic; the same blindness in a channel
    the controller acts on is load-bearing.
    """
    _hdr(6, "EBS_006: temporal aliasing, with and without the trend in the loop")

    def state_fn(sub: Substrate):
        return {"stock_fraction": sub.fraction_pristine}

    from blindness import TemporalAliasing
    import random as _r

    def build(alias: bool, responsive: bool, ratchet: float = 0.08):
        timing = (
            TemporalAliasing(window=5, noise_floor=0.04, rng=_r.Random(6))
            if alias
            else TemporalAliasing(window=2, noise_floor=0.0, rng=_r.Random(6))
        )
        sub = Substrate(stock=0.5)
        stack = BlindnessStack(
            frame=FrameBlindness(boundary={"stock_fraction"}),
            model={},        # no model masking: aliasing is the only blindness
            timing=timing,
        )
        opt = ExtractiveOptimizer(
            blindness=stack,
            target_yield=1.2 * sub.peak_regeneration(),
            effort_ratchet=ratchet,
            trend_responsive=responsive,
        )
        res = opt.run(sub, steps=STEPS, state_fn=state_fn)
        aliased = sum(
            1 for r in res.records if any("temporal aliasing" in f for f in r.blindness_flags)
        )
        return res, aliased

    print("\n  Two conditions govern whether aliasing matters: whether the")
    print("  trend steers, and whether an effort ratchet is defending a target.")
    print(f"\n  {'regime':<48} {'alias steps':>12} {'final stock':>12}")

    results = {}
    for responsive, ratchet, tag in (
        (False, 0.00, "trend not in loop, no ratchet"),
        (True, 0.00, "trend steers, no ratchet"),
        (True, 0.08, "trend steers, ratchet defending target"),
    ):
        for alias in (False, True):
            res, aliased = build(alias, responsive, ratchet)
            results[(responsive, ratchet, alias)] = res
            label = f"{tag}, {'aliased' if alias else 'clear'}"
            print(f"  {label:<48} {aliased:12d} {res.final_stock_fraction:12.4f}")

    inert = abs(
        results[(False, 0.00, True)].final_stock_fraction
        - results[(False, 0.00, False)].final_stock_fraction
    )
    decisive = (
        results[(True, 0.00, False)].final_stock_fraction
        - results[(True, 0.00, True)].final_stock_fraction
    )
    masked = abs(
        results[(True, 0.08, True)].final_stock_fraction
        - results[(True, 0.08, False)].final_stock_fraction
    )

    print(f"\n  (a) trend not in loop      -> outcome delta {inert:.4f}  (aliasing cosmetic)")
    print(f"  (b) trend steers, no ratchet -> outcome delta {decisive:+.4f}  (aliasing decisive)")
    print(f"  (c) ratchet defending target -> outcome delta {masked:.4f}  (ratchet dominates)")

    ok = inert < 1e-9 and decisive > 0.5 and masked < 1e-9
    print(_verdict(
        ok,
        "aliasing is decisive only where the trend steers AND no ratchet overrides it",
    ))
    return ok


def main() -> int:
    print(RULE)
    print("extraction-blindness-sim — experiment suite")
    print(RULE)
    print("An optimizer acting on a blinded observation reads the absence of")
    print("an error signal as confirmation of safety. These six experiments")
    print("measure how far that reading diverges from the substrate's state.")

    results = {
        "EBS_001": experiment_1(),
        "EBS_002": experiment_2(),
        "EBS_003": experiment_3(),
        "EBS_004": experiment_4(),
        "EBS_005": experiment_5(),
        "EBS_006": experiment_6(),
    }

    print(f"\n{RULE}\nSUMMARY\n{RULE}")
    for cid, ok in results.items():
        print(f"  {cid}: {'SUPPORTED' if ok else 'REFUTED'}")
    n_ok = sum(results.values())
    print(f"\n  {n_ok}/{len(results)} claims supported by this run.")
    print("  Refutation protocol: a REFUTED row updates the claim, not the constants.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
