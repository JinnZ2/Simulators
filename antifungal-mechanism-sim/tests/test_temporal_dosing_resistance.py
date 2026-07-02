"""
Tests for the temporal-axis / non-commutative-J antifungal module.

The two structural findings the module carries:

  [1] Resistance evolution is a KICKED RELAXOR: dose = kick, adaptation
      between kicks. Schedule decides the outcome. Simultaneous dosing
      suppresses more of the population than long mono blocks; fast
      cycling sits between the two. Sequential mono breeds RAB stepwise.

  [2] Sequence-dependent antagonism: the interaction "matrix" is
      NON-COMMUTATIVE. kill(azole -> polyene) != kill(polyene -> azole).

The tests pin the model constants (any silent retuning surfaces as
a test failure), the mechanical invariants (step is non-negative,
schedules have expected lengths, run's return shape), the *ordering*
of the three schedules by final population (the qualitative finding),
and the exact non-commutative kill numbers to one decimal place.

License: CC0
Dependencies: stdlib only (unittest)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from temporal_dosing_resistance import (
    K,
    KILL,
    MU,
    R,
    SENS,
    polyene_azole,
    run,
    schedules,
    step,
)


class TestFrozenConstants(unittest.TestCase):
    """Model constants are frozen estimates. Any silent retuning here
    would silently move every downstream number; surface it as a test
    failure instead."""

    def test_growth_rate_R(self):
        self.assertEqual(R, 0.5)

    def test_carrying_capacity_K(self):
        self.assertEqual(K, 1_000_000.0)

    def test_mutation_rate_MU(self):
        self.assertEqual(MU, 1e-4)

    def test_kill_rate_KILL(self):
        self.assertEqual(KILL, 1.2)


class TestSensitivityMap(unittest.TestCase):
    def test_four_genotypes(self):
        self.assertEqual(set(SENS.keys()), {'WT', 'RA', 'RB', 'RAB'})

    def test_WT_is_sensitive_to_both_drugs(self):
        self.assertEqual(SENS['WT'], {'A', 'B'})

    def test_RA_is_resistant_to_A_only(self):
        self.assertEqual(SENS['RA'], {'B'})

    def test_RB_is_resistant_to_B_only(self):
        self.assertEqual(SENS['RB'], {'A'})

    def test_RAB_is_fully_resistant(self):
        self.assertEqual(SENS['RAB'], set())


class TestStep(unittest.TestCase):
    INITIAL = {'WT': 1e5, 'RA': 1.0, 'RB': 1.0, 'RAB': 0.0}

    def test_output_has_all_four_genotypes(self):
        out = step(self.INITIAL, {'A', 'B'})
        self.assertEqual(set(out.keys()), set(self.INITIAL.keys()))

    def test_output_is_non_negative(self):
        out = step(self.INITIAL, {'A', 'B'})
        for g, n in out.items():
            self.assertGreaterEqual(n, 0.0, f'{g} went negative')

    def test_empty_dose_lets_wild_type_grow(self):
        # No drug pressure -> logistic growth on WT, no kill term.
        out = step(self.INITIAL, set())
        self.assertGreater(out['WT'], self.INITIAL['WT'])

    def test_both_drugs_kill_wild_type(self):
        # Under simultaneous dosing WT should decline (kill > growth for
        # a large WT population well below carrying capacity).
        out = step(self.INITIAL, {'A', 'B'})
        self.assertLess(out['WT'], self.INITIAL['WT'])

    def test_RAB_is_only_hit_by_growth_terms(self):
        # RAB is fully resistant; under any dose it experiences pure
        # logistic growth (plus a small mutation inflow), never kill.
        pop = {'WT': 0.0, 'RA': 0.0, 'RB': 0.0, 'RAB': 100.0}
        out_dosed = step(pop, {'A', 'B'})
        out_undosed = step(pop, set())
        # Two doses should be indistinguishable for RAB alone (no
        # sensitive population left to mutate off, no kill terms).
        self.assertAlmostEqual(out_dosed['RAB'], out_undosed['RAB'],
                               places=6)

    def test_collateral_sensitivity_hits_RA_extra_under_B(self):
        # RA has 100 units; without collateral, drug B kills the RA
        # population via SENS['RA'] == {'B'}. With collateral there is
        # an ADDITIONAL 0.8 * KILL * n hit on RA when B is active.
        pop = {'WT': 0.0, 'RA': 100.0, 'RB': 0.0, 'RAB': 0.0}
        out_normal = step(pop, {'B'}, collateral=False)
        out_coll = step(pop, {'B'}, collateral=True)
        self.assertLess(out_coll['RA'], out_normal['RA'])


class TestSchedules(unittest.TestCase):
    def test_three_named_schedules(self):
        s = schedules()
        self.assertEqual(set(s.keys()),
                         {'simultaneous', 'sequential mono', 'fast cycling'})

    def test_default_length_is_40(self):
        for name, sch in schedules().items():
            with self.subTest(schedule=name):
                self.assertEqual(len(sch), 40)

    def test_custom_length(self):
        s = schedules(n=20)
        self.assertEqual(len(s['simultaneous']), 20)
        self.assertEqual(len(s['fast cycling']), 20)

    def test_simultaneous_uses_both_drugs_every_step(self):
        s = schedules()
        for active in s['simultaneous']:
            self.assertEqual(active, {'A', 'B'})

    def test_sequential_mono_is_two_blocks(self):
        s = schedules(n=40)
        self.assertEqual(s['sequential mono'][:20], [{'A'}] * 20)
        self.assertEqual(s['sequential mono'][20:], [{'B'}] * 20)

    def test_fast_cycling_alternates_every_step(self):
        s = schedules(n=40)
        for i, active in enumerate(s['fast cycling']):
            expected = {'A'} if i % 2 == 0 else {'B'}
            self.assertEqual(active, expected)


class TestRun(unittest.TestCase):
    def test_returns_total_rfrac_cleared(self):
        result = run(schedules()['simultaneous'])
        self.assertEqual(len(result), 3)
        total, rfrac, cleared = result
        self.assertIsInstance(total, float)
        self.assertGreaterEqual(rfrac, 0.0)
        self.assertLessEqual(rfrac, 1.0)
        self.assertIsInstance(cleared, bool)

    def test_empty_schedule_leaves_initial_population(self):
        total, rfrac, cleared = run([])
        # Initial population is WT=1e5 + RA=1 + RB=1 = ~100_002.
        self.assertAlmostEqual(total, 1e5 + 2, places=0)
        self.assertFalse(cleared)


class TestKickedRelaxorOrdering(unittest.TestCase):
    """The load-bearing structural claim of the temporal module:
    schedule shape determines outcome. Simultaneous dosing is the
    strongest suppressor; sequential mono is the weakest. Fast cycling
    sits between them. All three eventually go to R_frac = 1.0 (RAB
    takes over) but their surviving populations rank in the documented
    order."""

    def setUp(self):
        s = schedules()
        self.simult = run(s['simultaneous'])
        self.seq = run(s['sequential mono'])
        self.cyc = run(s['fast cycling'])

    def test_simultaneous_suppresses_more_than_sequential_mono(self):
        self.assertLess(self.simult[0], self.seq[0])

    def test_simultaneous_suppresses_more_than_fast_cycling(self):
        self.assertLess(self.simult[0], self.cyc[0])

    def test_sequential_mono_leaves_the_largest_survivor(self):
        # sequential mono breeds RAB stepwise -> largest surviving pop.
        self.assertGreater(self.seq[0], self.cyc[0])

    def test_all_three_schedules_end_dominated_by_RAB(self):
        # Escape genotype takes over in every schedule; the differ is
        # in total population, not in R_frac.
        for total, rfrac, cleared in (self.simult, self.seq, self.cyc):
            self.assertAlmostEqual(rfrac, 1.0, places=2)

    def test_collateral_sensitivity_helps_fast_cycling(self):
        # RA hypersensitive to B under collateral should reduce the
        # surviving population under fast cycling.
        base_total, _, _ = self.cyc
        coll_total, _, _ = run(schedules()['fast cycling'],
                               collateral=True)
        self.assertLess(coll_total, base_total)


class TestNonCommutativeAntagonism(unittest.TestCase):
    """The second structural claim: the interaction matrix is
    NON-COMMUTATIVE. Applying polyene THEN azole kills more than
    applying azole THEN polyene, because azole depletes the ergosterol
    that polyene needs to bind."""

    def test_azole_first_blunts_polyene(self):
        # Documented in the demo: azole -> polyene = 9.4
        # E starts at 1.0; azole adds 7.0 and drops E to 0.3; polyene
        # then adds 8.0 * 0.3 = 2.4. Total = 9.4.
        self.assertAlmostEqual(polyene_azole(['azole', 'polyene']),
                               9.4, places=1)

    def test_polyene_first_full_effect(self):
        # Documented in the demo: polyene -> azole = 15.0
        # E starts at 1.0; polyene adds 8.0 * 1.0 = 8.0; azole then
        # adds 7.0 (E depletion is applied AFTER the azole kill). Total = 15.0.
        self.assertAlmostEqual(polyene_azole(['polyene', 'azole']),
                               15.0, places=1)

    def test_order_matters(self):
        forward = polyene_azole(['azole', 'polyene'])
        reverse = polyene_azole(['polyene', 'azole'])
        # Strictly greater under the polyene-first order.
        self.assertGreater(reverse, forward)
        # And meaningfully greater (>= 5 unit gap in this parameterization).
        self.assertGreater(reverse - forward, 5.0)

    def test_single_drug_is_deterministic(self):
        # Polyene alone: 8.0 * 1.0 = 8.0. Azole alone: 7.0.
        self.assertAlmostEqual(polyene_azole(['polyene']), 8.0, places=6)
        self.assertAlmostEqual(polyene_azole(['azole']), 7.0, places=6)

    def test_empty_order_is_zero(self):
        self.assertEqual(polyene_azole([]), 0.0)

    def test_unknown_drug_names_are_ignored(self):
        # Silent skip in the current implementation (no branch for
        # non-polyene/azole names). Pin this behavior so a future change
        # to error-on-unknown is visible.
        self.assertEqual(polyene_azole(['unknown_drug']), 0.0)


if __name__ == '__main__':
    unittest.main()
