"""
test_repairs.py -- one test per defect in CLAIM_TABLE.md.

CC0-1.0. Standard library only.

Each test asserted the BROKEN behaviour when it was written and asserts the
repair now, so a regression turns it red. Same arrangement as
../../reasoning-gate/tests/test_gate.py.

    python3 -m unittest discover tests
"""

import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..")))

import drift  # noqa: E402
import regress  # noqa: E402
from schema import ACCESS_RANK, DIRECTIONS, CriteriaVersion, Frame  # noqa: E402

E = drift.DriftEngine()

BASE = dict(
    boundary="pass at 1 on held-out unit tests",
    horizon="single submission",
    who_counts="the benchmark authors",
    sign_source="set by the benchmark authors",
    logic="classical bivalent",
    observer_access="verified",
)


def cv(vid, dims=None, weights=None, exemplars=100, direction=None,
       **overrides):
    f = dict(BASE)
    f.update(overrides)
    return CriteriaVersion(
        artifact_name="X", version_id=vid, timestamp="2024-01-01T00:00:00Z",
        frame=Frame(**f),
        rubric_dimensions=["correctness"] if dims is None else dims,
        rubric_weights={"correctness": 1.0} if weights is None else weights,
        exemplar_count=exemplars,
        direction=direction,
    )


# ---------------------------------------------------------------------------
# CD_002 -- the drift metric is unsigned


class SignedDrift(unittest.TestCase):

    def test_numeric_drift_carries_sign(self):
        """Was: 100->1000 and 1000->100 both 0.9. Now they differ by sign."""
        up = E._signed_numeric(100, 1000)
        down = E._signed_numeric(1000, 100)
        self.assertGreater(up, 0)
        self.assertLess(down, 0)
        self.assertAlmostEqual(up, -down)

    def test_unsigned_magnitude_is_preserved(self):
        """The repair adds a signal, it does not remove one."""
        self.assertEqual(E._numeric_drift(100, 1000),
                         abs(E._signed_numeric(100, 1000)))

    def test_observer_access_is_ranked_not_string_matched(self):
        """Was: every transition 1.0, including the loss of verification."""
        self.assertEqual(E._str_drift("verified", "unknown"),
                         E._str_drift("unknown", "verified"))
        self.assertLess(E._signed_ordinal("verified", "unknown"), 0)
        self.assertGreater(E._signed_ordinal("unknown", "verified"), 0)

    def test_observer_access_step_size_survives(self):
        """partial->verified is one step; unknown->verified is two."""
        one = abs(E._signed_ordinal("partial", "verified"))
        two = abs(E._signed_ordinal("unknown", "verified"))
        self.assertLess(one, two)

    def test_rank_covers_every_legal_value(self):
        from schema import Frame as _F  # noqa: F401
        for v in ("unknown", "partial", "verified"):
            self.assertIn(v, ACCESS_RANK)

    def test_dimension_added_and_removed_differ(self):
        added = E._signed_list(["a"], ["a", "b"])
        removed = E._signed_list(["a", "b"], ["a"])
        self.assertGreater(added, 0)
        self.assertLess(removed, 0)

    def test_weight_up_and_down_differ(self):
        up = E._signed_dict({"a": 1.0}, {"a": 1.5})
        down = E._signed_dict({"a": 1.5}, {"a": 1.0})
        self.assertGreater(up, 0)
        self.assertLess(down, 0)

    def test_free_text_stays_unsigned_unless_declared(self):
        """An undeclared direction is NOT a lateral one."""
        a = cv("a")
        b = cv("b", boundary="pass at 1")
        m = E.compute_pair(a, b)
        self.assertGreater(m["boundary"], 0.0)
        self.assertEqual(m["signed_boundary"], 0.0)

    def test_declared_direction_signs_a_free_text_field(self):
        a = cv("a")
        wider = cv("w", boundary="pass at 1 on held-out unit tests plus docs",
                   direction={"boundary": "widened"})
        narrower = cv("n", boundary="pass at 1",
                      direction={"boundary": "narrowed"})
        self.assertGreater(E.compute_pair(a, wider)["signed_boundary"], 0)
        self.assertLess(E.compute_pair(a, narrower)["signed_boundary"], 0)

    def test_directionless_fields_stay_zero(self):
        a = cv("a")
        b = cv("b", logic="paraconsistent", sign_source="set by a regulator")
        m = E.compute_pair(a, b)
        self.assertGreater(m["logic"], 0.0)
        self.assertEqual(m["signed_logic"], 0.0)
        self.assertEqual(m["signed_sign_source"], 0.0)

    def test_composite_signed_reports_coverage(self):
        """A caller must be able to tell 'no net change' from 'none declared'."""
        a = cv("a")
        b = cv("b", boundary="pass at 1")
        m = E.compute_pair(a, b)
        self.assertIn("composite_signed", m)
        self.assertIn("signed_coverage", m)
        self.assertLess(m["signed_coverage"], 1.0)

    def test_direction_values_are_validated(self):
        good = cv("g", direction={"boundary": "widened"})
        bad = cv("b", direction={"boundary": "bigger"})
        self.assertEqual(good.validate_direction(), [])
        self.assertTrue(bad.validate_direction())
        self.assertIn("unknown", DIRECTIONS)


# ---------------------------------------------------------------------------
# CD_003 / CD_004 -- the series


def make_history():
    versions = [cv("v1"), cv("v2", exemplars=200),
                cv("v3", exemplars=400), cv("v4", exemplars=800)]
    return versions, E.compute_history(versions)


class Series(unittest.TestCase):

    def setUp(self):
        self.versions, self.metrics = make_history()

    def test_no_planted_head(self):
        """Was: y[0] = 0.0 for every model, paired with a real drift value."""
        matrix = {"M": {"v1": 0.42, "v2": 0.38, "v3": 0.35}}
        r = regress.DriftRegressor(matrix, self.metrics)
        x, y = r.build_series("M", score_type="delta")
        self.assertNotIn(0.0, y)
        self.assertEqual(len(x), 2)
        self.assertAlmostEqual(y[0], 0.38 - 0.42)

    def test_first_version_is_in_the_order(self):
        """Was: version_order = [to_version ...], so v1 never appeared."""
        r = regress.DriftRegressor({}, self.metrics)
        self.assertEqual(r.version_order[0], "v1")
        self.assertEqual(len(r.version_order), len(self.versions))

    def test_baseline_only_model_is_not_dropped(self):
        """Was: scores at first+last filtered to one and returned ([], [])."""
        matrix = {"M": {"v1": 0.18, "v4": 0.05}}
        r = regress.DriftRegressor(matrix, self.metrics)
        x, y = r.build_series("M", score_type="delta")
        self.assertEqual(len(x), 1)
        self.assertAlmostEqual(y[0], 0.05 - 0.18)

    def test_span_drift_is_the_sum_over_the_interval(self):
        r = regress.DriftRegressor({}, self.metrics)
        total = sum(p["composite_drift"] for p in self.metrics.pairs)
        self.assertAlmostEqual(r.span_drift("v1", "v4"), total)

    def test_span_drift_refuses_a_backwards_or_unknown_pair(self):
        r = regress.DriftRegressor({}, self.metrics)
        self.assertIsNone(r.span_drift("v4", "v1"))
        self.assertIsNone(r.span_drift("v1", "nope"))

    def test_delta_is_paired_with_the_drift_it_spans(self):
        matrix = {"M": {"v1": 0.5, "v3": 0.4}}
        r = regress.DriftRegressor(matrix, self.metrics)
        x, _ = r.build_series("M", score_type="delta")
        self.assertAlmostEqual(x[0], r.span_drift("v1", "v3"))


# ---------------------------------------------------------------------------
# CD_006 -- drift is a property of the artifact


class Pooled(unittest.TestCase):

    def setUp(self):
        self.versions, self.metrics = make_history()
        self.matrix = {
            "A": {"v1": 0.42, "v2": 0.38, "v3": 0.35, "v4": 0.28},
            "B": {"v2": 0.55, "v3": 0.62, "v4": 0.58},
            "C": {"v1": 0.18, "v4": 0.05},
        }

    def test_every_model_regresses_against_the_same_x(self):
        r = regress.DriftRegressor(self.matrix, self.metrics)
        a, _ = r.build_series("A", score_type="delta")
        b, _ = r.build_series("B", score_type="delta")
        self.assertEqual(a[-len(b):], b)

    def test_pooled_has_more_observations_than_any_single_model(self):
        r = regress.DriftRegressor(self.matrix, self.metrics)
        pooled = r.regress_pooled()
        biggest = max(len(r.build_series(m, score_type="delta")[0])
                      for m in self.matrix)
        self.assertGreater(pooled.n, biggest)

    def test_pooled_has_degrees_of_freedom_where_per_model_does_not(self):
        r = regress.DriftRegressor(self.matrix, self.metrics)
        self.assertGreater(r.regress_pooled().df, r.regress("B").df)


# ---------------------------------------------------------------------------
# CD_007 -- the significance test


class Significance(unittest.TestCase):

    def test_t_distribution_matches_known_critical_values(self):
        for t, df in ((12.706, 1), (4.303, 2), (2.776, 4), (2.228, 10)):
            self.assertAlmostEqual(regress.t_two_sided_p(t, df), 0.05,
                                   places=3)

    def test_p_is_none_without_degrees_of_freedom(self):
        self.assertIsNone(regress.t_two_sided_p(1.0, 0))

    def test_result_reports_t_df_and_p(self):
        r = regress.ols_regression([0.1, 0.2, 0.3, 0.4],
                                   [0.1, 0.25, 0.28, 0.42])
        d = r.to_dict()
        for k in ("t_slope", "p_slope", "df", "significant_at_05"):
            self.assertIn(k, d)
        self.assertEqual(d["df"], 2)

    def test_r_squared_is_null_below_three_points(self):
        """Was: r_squared 1.0 at n=2, beside 'insufficient data' in prose."""
        d = regress.ols_regression([0.1, 0.2], [0.3, 0.4]).to_dict()
        self.assertIsNone(d["r_squared"])
        self.assertTrue(d["insufficient"])

    def test_a_clean_signal_is_reported_significant(self):
        xs = [0.1 * i for i in range(1, 13)]
        ys = [2.0 * x + 0.001 * ((i % 3) - 1) for i, x in enumerate(xs)]
        d = regress.ols_regression(xs, ys).to_dict()
        self.assertTrue(d["significant_at_05"])
        self.assertLess(d["p_slope"], 0.05)

    def test_pure_noise_is_not_reported_significant(self):
        xs = [0.1 * i for i in range(1, 13)]
        ys = [0.5, 0.2, 0.9, 0.1, 0.6, 0.3, 0.8, 0.2, 0.7, 0.4, 0.55, 0.35]
        d = regress.ols_regression(xs, ys).to_dict()
        self.assertFalse(d["significant_at_05"])

    def test_interpretation_names_the_test_when_it_fails(self):
        d = regress.ols_regression([0.1, 0.2, 0.3], [0.1, 0.3, 0.15]).to_dict()
        self.assertIn("not significant", d["interpretation"])


if __name__ == "__main__":
    unittest.main()
