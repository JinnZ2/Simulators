"""Aggregate test suite.

Runs every module's self-test plus cross-module invariants that no
single module can check alone.

    python3 -m pytest tests/ -q      (from the folder root)
    python3 tests/test_all.py        (no pytest required)
"""

from __future__ import annotations

import os
import subprocess
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from blindness import (  # noqa: E402
    BlindnessStack,
    FrameBlindness,
    ModelDependenceMasking,
    TemporalAliasing,
)
from boundaries import fishery_boundaries, soil_boundaries  # noqa: E402
from optimizer import ExtractiveOptimizer  # noqa: E402
from profiles import fishery_profile, soil_profile  # noqa: E402
from substrate import Substrate  # noqa: E402
from throughput import (  # noqa: E402
    demonstrate_caloric_sign_error,
    demonstrate_orientation_contradiction,
)

MODULES = [
    "substrate",
    "blindness",
    "indicators",
    "boundaries",
    "throughput",
    "optimizer",
    "profiles",
]


def test_module_self_tests_pass():
    """Every module's __main__ self-test exits clean."""
    for mod in MODULES:
        r = subprocess.run(
            [sys.executable, os.path.join(_ROOT, f"{mod}.py")],
            capture_output=True, text=True,
        )
        assert r.returncode == 0, f"{mod}.py self-test failed:\n{r.stdout}\n{r.stderr}"
        assert "self-test OK" in r.stdout


def test_experiment_suite_runs_and_all_claims_supported():
    """The pinned suite runs clean and every claim is currently supported."""
    r = subprocess.run(
        [sys.executable, os.path.join(_ROOT, "run_experiments.py")],
        capture_output=True, text=True, cwd=_ROOT,
    )
    assert r.returncode == 0, f"suite failed:\n{r.stdout}\n{r.stderr}"
    for cid in ("EBS_001", "EBS_002", "EBS_003", "EBS_004", "EBS_005", "EBS_006"):
        assert cid in r.stdout, f"{cid} missing from output"
    assert "6/6 claims supported" in r.stdout, (
        "a claim changed status -- update CLAIM_TABLE.md, do not retune constants"
    )


def test_suite_is_deterministic():
    """Two runs of the suite produce identical output."""
    outs = []
    for _ in range(2):
        r = subprocess.run(
            [sys.executable, os.path.join(_ROOT, "run_experiments.py")],
            capture_output=True, text=True, cwd=_ROOT,
        )
        outs.append(r.stdout)
    assert outs[0] == outs[1], "suite output is not reproducible"


def test_pinned_sample_matches_current_run():
    """samples/experiments.sample.txt is not stale."""
    path = os.path.join(_ROOT, "samples", "experiments.sample.txt")
    if not os.path.exists(path):
        return  # sample not pinned yet
    with open(path, encoding="utf-8") as fh:
        pinned = fh.read()
    r = subprocess.run(
        [sys.executable, os.path.join(_ROOT, "run_experiments.py")],
        capture_output=True, text=True, cwd=_ROOT,
    )
    assert r.stdout == pinned, (
        "pinned sample is stale; re-pin with:\n"
        "  python3 run_experiments.py > samples/experiments.sample.txt"
    )


# ---------------------------------------------------------------------
# Cross-module invariants
# ---------------------------------------------------------------------

def test_blindness_never_reports_a_substrate_as_worse_than_it_is():
    """Every blindness mode is optimistic or neutral, never pessimistic.

    This is the property that makes the whole failure mode one-sided: a
    pessimistic instrument would trigger caution, not overshoot.
    """
    from blindness import BlindnessMask

    for coverage in (0.1, 0.5, 0.9, 1.0):
        md = ModelDependenceMasking(
            rung="M2", training_domain_coverage=coverage, model_prior=1.0
        )
        for true_value in (0.1, 0.3, 0.5, 0.8):
            reported = md.apply(true_value, BlindnessMask())
            assert reported >= true_value - 1e-12, (
                f"masking reported {reported} below true {true_value}"
            )


def test_boundaries_can_only_reduce_extraction():
    """No boundary set may ever increase a request."""
    for factory, state in (
        (
            fishery_boundaries,
            {
                "stock_fraction_of_bmsy": 0.3,
                "benthic_area_over_lag": 0.9,
                "replenishment_deficit_3yr": 0.5,
            },
        ),
        (
            soil_boundaries,
            {
                "soc_pct_0_30cm": 1.0,
                "penetrometer_mpa_30_60cm": 3.0,
                "fb_ratio": 0.1,
            },
        ),
    ):
        bs = factory()
        for _ in range(5):
            v = bs.apply(1.0, state)
            assert v.allowed_extraction <= 1.0 + 1e-12


def test_sighted_optimizer_outperforms_blind_one():
    """Removing blindness, with nothing else changed, must not do harm."""

    def state_fn(sub):
        return {"stock_fraction": sub.fraction_pristine}

    finals = {}
    for label, coverage in (("blind", 0.5), ("sighted", 1.0)):
        sub = Substrate(stock=0.5)
        stack = BlindnessStack(
            frame=FrameBlindness(boundary={"stock_fraction"}),
            model={
                "stock_fraction": ModelDependenceMasking(
                    rung="M2", training_domain_coverage=coverage, model_prior=1.0
                )
            },
            timing=TemporalAliasing(window=2, noise_floor=0.0),
        )
        opt = ExtractiveOptimizer(
            blindness=stack,
            target_yield=1.2 * sub.peak_regeneration(),
            effort_ratchet=0.0,
            trend_responsive=True,
        )
        finals[label] = opt.run(sub, steps=60, state_fn=state_fn).final_stock_fraction

    assert finals["sighted"] >= finals["blind"], (
        f"sighted {finals['sighted']:.4f} should not underperform "
        f"blind {finals['blind']:.4f}"
    )


def test_profile_targets_are_modest_overshoots():
    """Both profiles must overshoot regeneration, but not catastrophically."""
    f = fishery_profile()
    ratio = f.target_yield / f.substrate.peak_regeneration()
    assert 1.0 < ratio < 1.5, f"fishery overshoot {ratio:.2f}x is not a modest one"

    s = soil_profile()
    s_ratio = s.target_yield / s.substrate.peak_regeneration()
    assert 1.0 < s_ratio < 2.0, f"soil overshoot {s_ratio:.2f}x is not a modest one"


def test_source_contradictions_still_reproduce():
    """The recorded contradictions are properties of the source, not bugs."""
    d = demonstrate_orientation_contradiction()
    assert not d["as_written_remedies_help"]
    assert d["inverted_remedies_help"]

    c = demonstrate_caloric_sign_error()
    assert c["version_b_masks_depletion"]
    assert c["mass_balance_reports_depletion"]


def _main() -> int:
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"  FAIL  {fn.__name__}: {exc}")
    print(f"\n{len(fns) - failed}/{len(fns)} tests passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(_main())
