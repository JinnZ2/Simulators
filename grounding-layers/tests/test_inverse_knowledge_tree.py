"""
Audit-grade tests for inverse_knowledge_tree — verification by
demonstrated lineage. Peer to the L-stack rather than a member of it.

SCOPE at the framework level (see SCOPE_TAXONOMY.md):
  T = uncalibrated  (span_years/failures caller-defined)
  S = uncalibrated  (domain-agnostic — bridges, drugs, algorithms)
  O = any_information_system
  C = culture_neutral (framework)

Specific trees (like BRIDGES) encode specific engineering-culture
epistemology and land at C=engineering_epistemology_frame; the tests
are careful not to conflate framework claims with the domain-scoped
demo pin.

Pins:

  GL_IKT_001 [PHENOMENON]: Node holds claimed + demonstrated separately
  GL_IKT_002 [PHENOMENON]: backward closure walks requires edges
  GL_IKT_003 [PHENOMENON]: failure_load aggregates over closure
  GL_IKT_004 [PHENOMENON]: four priority-ordered verdicts
  GL_IKT_005 [PHENOMENON]: terminal and chain-wide gates checked
                            independently
  GL_IKT_006 [INSTRUMENT]: gap_tol=0.15, terminal_tol=0.20 frozen
  GL_IKT_PIN [INSTRUMENT]: BRIDGES demo verdicts pinned

License: CC0
Dependencies: stdlib only.
"""

import inspect
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from inverse_knowledge_tree import (
    BRIDGES,
    Node,
    audit,
    closure,
    failure_load,
    report,
)


class TestGL_IKT_001_NodeShape(unittest.TestCase):
    """[PHENOMENON] Node carries claimed + demonstrated as
    independent fields; gap = claimed - demonstrated."""

    def test_node_has_claimed_and_demonstrated_fields(self):
        fields = {f for f in Node.__dataclass_fields__}
        self.assertIn('claimed', fields)
        self.assertIn('demonstrated', fields)
        self.assertNotEqual('claimed', 'demonstrated')

    def test_gap_is_claimed_minus_demonstrated(self):
        n = Node('n', 'yields x', claimed=0.9, demonstrated=0.5)
        self.assertAlmostEqual(n.gap, 0.4, places=10)

    def test_gap_negative_when_overbuilt(self):
        n = Node('n', 'yields x', claimed=0.3, demonstrated=0.9)
        self.assertAlmostEqual(n.gap, -0.6, places=10)

    def test_gap_zero_when_matched(self):
        n = Node('n', 'yields x', claimed=0.5, demonstrated=0.5)
        self.assertEqual(n.gap, 0.0)


class TestGL_IKT_002_Closure(unittest.TestCase):
    """[PHENOMENON] Backward closure walks requires-edges. Returns
    (reached, missing)."""

    def test_closure_reaches_root_alone_when_no_requires(self):
        tree = {'a': Node('a', 'y')}
        reached, missing = closure(tree, 'a')
        self.assertEqual(set(reached), {'a'})
        self.assertEqual(missing, [])

    def test_closure_reaches_all_ancestors(self):
        tree = {
            'a': Node('a', 'y', ()),
            'b': Node('b', 'y', ('a',)),
            'c': Node('c', 'y', ('b',)),
        }
        reached, missing = closure(tree, 'c')
        self.assertEqual(set(reached), {'a', 'b', 'c'})
        self.assertEqual(missing, [])

    def test_closure_flags_missing_ancestors(self):
        tree = {
            'a': Node('a', 'y', ('ghost',)),
        }
        reached, missing = closure(tree, 'a')
        self.assertEqual(set(reached), {'a'})
        self.assertEqual(set(missing), {'ghost'})

    def test_closure_terminates_on_cycles(self):
        # Cycle: a -> b -> a. The `if nid in seen` guard must
        # prevent infinite recursion.
        tree = {
            'a': Node('a', 'y', ('b',)),
            'b': Node('b', 'y', ('a',)),
        }
        reached, missing = closure(tree, 'a')
        self.assertEqual(set(reached), {'a', 'b'})
        self.assertEqual(missing, [])

    def test_closure_bridges_demo_aqueduct(self):
        # aqueduct -> roman_arch -> lime_mortar -> fire_control.
        reached, missing = closure(BRIDGES, 'aqueduct_span')
        self.assertEqual(set(reached),
                         {'aqueduct_span', 'roman_arch',
                          'lime_mortar', 'fire_control'})
        self.assertEqual(missing, [])


class TestGL_IKT_003_FailureLoad(unittest.TestCase):
    """[PHENOMENON] failure_load aggregates over the closure."""

    def _basic_tree(self):
        return {
            'a': Node('a', 'y', (), failures_absorbed=10,
                     span_years=100.0,
                     claimed=0.5, demonstrated=0.7),   # gap = -0.2 (held)
            'b': Node('b', 'y', ('a',), failures_absorbed=20,
                     span_years=50.0,
                     claimed=0.8, demonstrated=0.5),   # gap = +0.3 (spent)
            'c': Node('c', 'y', ('b',), failures_absorbed=5,
                     span_years=25.0,
                     claimed=0.6, demonstrated=0.6),   # gap = 0
        }

    def test_failure_load_sums_across_closure(self):
        load = failure_load(self._basic_tree(), 'c')
        self.assertEqual(load['failures'], 35)
        self.assertEqual(load['span_years'], 175.0)
        self.assertEqual(load['nodes'], 3)

    def test_margin_spent_only_positive_gaps(self):
        load = failure_load(self._basic_tree(), 'c')
        # Only b has gap > 0 (0.3).
        self.assertAlmostEqual(load['margin_spent'], 0.3, places=3)

    def test_margin_held_only_negative_gaps(self):
        load = failure_load(self._basic_tree(), 'c')
        # Only a has gap < 0 (-0.2). Held as absolute value.
        self.assertAlmostEqual(load['margin_held'], 0.2, places=3)

    def test_spenders_lists_positive_gap_ids(self):
        load = failure_load(self._basic_tree(), 'c')
        self.assertEqual(set(load['spenders']), {'b'})

    def test_missing_forwarded_from_closure(self):
        tree = {'a': Node('a', 'y', ('ghost',))}
        load = failure_load(tree, 'a')
        self.assertEqual(set(load['missing']), {'ghost'})


class TestGL_IKT_004_VerdictsInPriority(unittest.TestCase):
    """[PHENOMENON] Four verdicts, priority-ordered. UNGROUNDED >
    EXCEEDS > BORROWS(terminal) > BORROWS(chain-wide) > HOLDS."""

    def test_holds_when_all_gates_pass(self):
        tree = {
            'a': Node('a', 'y', (), 10, 100,
                     claimed=0.5, demonstrated=0.5),
        }
        verdict, _ = audit(tree, 'a', margin_attempts=1000)
        self.assertEqual(verdict, 'HOLDS')

    def test_ungrounded_fires_when_missing(self):
        tree = {'a': Node('a', 'y', ('ghost',))}
        verdict, _ = audit(tree, 'a', margin_attempts=1000)
        self.assertEqual(verdict, 'UNGROUNDED')

    def test_exceeds_fires_when_failures_over_margin(self):
        tree = {
            'a': Node('a', 'y', (), failures_absorbed=1000,
                     claimed=0.3, demonstrated=0.4),  # gap held
        }
        verdict, _ = audit(tree, 'a', margin_attempts=500)
        self.assertEqual(verdict, 'EXCEEDS')

    def test_borrows_fires_on_terminal_gap(self):
        # Small chain, terminal_gap = 0.5 > terminal_tol = 0.20.
        tree = {
            'a': Node('a', 'y', (), 10, 100,
                     claimed=0.9, demonstrated=0.4),   # gap 0.5
        }
        verdict, _ = audit(tree, 'a', margin_attempts=1000)
        self.assertEqual(verdict, 'BORROWS')

    def test_borrows_fires_on_chain_wide_spend(self):
        # Two nodes; terminal_gap = 0.15 < 0.20 (below terminal),
        # but chain spend = 0.15 + 0.19 = 0.34 > gap_tol * 2 = 0.30.
        tree = {
            'a': Node('a', 'y', (), 10, 100,
                     claimed=0.7, demonstrated=0.51),  # gap 0.19
            'b': Node('b', 'y', ('a',), 10, 100,
                     claimed=0.6, demonstrated=0.45),  # gap 0.15
        }
        verdict, load = audit(tree, 'b', margin_attempts=1000)
        # Terminal gap 0.15 is UNDER 0.20 so terminal gate doesn't fire.
        self.assertLess(load['terminal_gap'], 0.20)
        # Chain-wide 0.34 > 0.15 * 2 = 0.30 so chain gate does fire.
        self.assertGreater(load['margin_spent'], 0.15 * load['nodes'])
        self.assertEqual(verdict, 'BORROWS')

    def test_verdict_priority_ungrounded_over_exceeds(self):
        # A tree with both missing ancestors AND excess failures
        # should return UNGROUNDED, not EXCEEDS.
        tree = {'a': Node('a', 'y', ('ghost',), failures_absorbed=10000)}
        verdict, _ = audit(tree, 'a', margin_attempts=1)
        self.assertEqual(verdict, 'UNGROUNDED')

    def test_verdict_deterministic_on_repeated_calls(self):
        v1, _ = audit(BRIDGES, 'i35w_span', margin_attempts=1000)
        v2, _ = audit(BRIDGES, 'i35w_span', margin_attempts=1000)
        v3, _ = audit(BRIDGES, 'i35w_span', margin_attempts=1000)
        self.assertEqual(v1, v2)
        self.assertEqual(v2, v3)


class TestGL_IKT_005_TerminalAndChainGates(unittest.TestCase):
    """[PHENOMENON] Two gates: terminal AND chain-wide, checked
    independently."""

    def test_terminal_gate_fires_alone(self):
        # 5-node chain, all ancestors honest (gap=0), terminal_gap=0.3.
        # Chain-wide spend = 0.3, gap_tol * 5 = 0.75, so chain gate
        # DOES NOT fire. Terminal gate alone triggers BORROWS.
        tree = {
            'a': Node('a', 'y', (), 5, 50,
                     claimed=0.5, demonstrated=0.5),
            'b': Node('b', 'y', ('a',), 5, 50,
                     claimed=0.5, demonstrated=0.5),
            'c': Node('c', 'y', ('b',), 5, 50,
                     claimed=0.5, demonstrated=0.5),
            'd': Node('d', 'y', ('c',), 5, 50,
                     claimed=0.5, demonstrated=0.5),
            'e': Node('e', 'y', ('d',), 5, 50,
                     claimed=0.8, demonstrated=0.5),  # terminal gap 0.3
        }
        verdict, load = audit(tree, 'e', margin_attempts=1000)
        self.assertAlmostEqual(load['terminal_gap'], 0.3, places=3)
        # Chain-wide 0.3 < gap_tol * 5 = 0.75.
        self.assertLess(load['margin_spent'], 0.15 * load['nodes'])
        # But terminal 0.3 > 0.20 -> BORROWS.
        self.assertEqual(verdict, 'BORROWS')

    def test_chain_gate_fires_alone(self):
        # Terminal_gap = 0.10 (below 0.20). Two ancestors each spend
        # 0.19 (below terminal_tol individually), but chain-wide sum
        # = 0.10 + 0.19 + 0.19 = 0.48 > 0.15 * 3 = 0.45.
        tree = {
            'a': Node('a', 'y', (), 5, 50,
                     claimed=0.7, demonstrated=0.51),  # gap 0.19
            'b': Node('b', 'y', ('a',), 5, 50,
                     claimed=0.7, demonstrated=0.51),  # gap 0.19
            'c': Node('c', 'y', ('b',), 5, 50,
                     claimed=0.6, demonstrated=0.5),   # gap 0.10 term
        }
        verdict, load = audit(tree, 'c', margin_attempts=1000)
        self.assertLess(load['terminal_gap'], 0.20)
        self.assertGreater(load['margin_spent'],
                           0.15 * load['nodes'])
        self.assertEqual(verdict, 'BORROWS')


class TestGL_IKT_006_FrozenTolerances(unittest.TestCase):
    """[INSTRUMENT] Frozen default tolerances."""

    def test_default_gap_tol_is_0p15(self):
        sig = inspect.signature(audit)
        self.assertEqual(sig.parameters['gap_tol'].default, 0.15)

    def test_default_terminal_tol_is_0p20(self):
        sig = inspect.signature(audit)
        self.assertEqual(sig.parameters['terminal_tol'].default, 0.20)


class TestIKTBridgesDemoPin(unittest.TestCase):
    """[INSTRUMENT] GL_IKT_PIN — BRIDGES demo verdicts pinned."""

    def test_aqueduct_holds_at_margin_1000(self):
        v, load = audit(BRIDGES, 'aqueduct_span',
                        margin_attempts=1000)
        self.assertEqual(v, 'HOLDS')
        self.assertEqual(load['nodes'], 4)
        self.assertEqual(load['failures'], 107)
        self.assertAlmostEqual(load['margin_held'], 2.34, places=2)

    def test_i35w_borrows_at_margin_1000(self):
        v, load = audit(BRIDGES, 'i35w_span',
                        margin_attempts=1000)
        self.assertEqual(v, 'BORROWS')
        self.assertEqual(load['nodes'], 7)
        self.assertEqual(load['failures'], 825)
        self.assertAlmostEqual(load['terminal_gap'], 0.37,
                               places=2)

    def test_new_gorge_borrows_at_margin_2000(self):
        v, load = audit(BRIDGES, 'new_gorge_span',
                        margin_attempts=2000)
        self.assertEqual(v, 'BORROWS')
        self.assertAlmostEqual(load['terminal_gap'], 0.93,
                               places=2)

    def test_new_gorge_exceeds_at_margin_500(self):
        v, load = audit(BRIDGES, 'new_gorge_span',
                        margin_attempts=500)
        self.assertEqual(v, 'EXCEEDS')
        # 810 historical failures > 500 margin.
        self.assertEqual(load['failures'], 810)

    def test_nano_lattice_ungrounded(self):
        # Extend the tree with a node whose ancestor is not in the
        # ledger.
        ghost = dict(BRIDGES)
        ghost['nano_lattice_span'] = Node(
            'nano_lattice_span', 'spans via unproven nano-lattice',
            ('self_healing_alloy',), 0, 0,
            claimed=0.98, demonstrated=0.0)
        v, load = audit(ghost, 'nano_lattice_span',
                        margin_attempts=5000)
        self.assertEqual(v, 'UNGROUNDED')
        self.assertIn('self_healing_alloy', load['missing'])


class TestReportShape(unittest.TestCase):
    """The report string returns a stable set of lines callers can
    parse or display."""

    def test_report_returns_string(self):
        v, load = audit(BRIDGES, 'aqueduct_span',
                        margin_attempts=1000)
        s = report(v, load)
        self.assertIsInstance(s, str)

    def test_report_contains_verdict_and_root(self):
        v, load = audit(BRIDGES, 'i35w_span',
                        margin_attempts=1000)
        s = report(v, load)
        self.assertIn('BORROWS', s)
        self.assertIn('i35w_span', s)

    def test_report_flags_missing_when_ungrounded(self):
        ghost = dict(BRIDGES)
        ghost['bad'] = Node('bad', 'y', ('ghost_dep',))
        v, load = audit(ghost, 'bad', margin_attempts=1000)
        s = report(v, load)
        self.assertIn('MISSING', s)
        self.assertIn('ghost_dep', s)


if __name__ == '__main__':
    unittest.main()
