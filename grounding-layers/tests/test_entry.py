"""
Tests for entry.py — the single-call dispatcher `audit()`.

Pins:
  - dispatcher routes strings to the NL playground path
  - dispatcher routes dicts to the structured integrated-stack path
  - both paths return the integrated-stack result-dict shape
  - AI-scope on human-embodied claims produces category-error
    refusal via the correct layer

License: CC0
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from entry import audit, LAYER_ORDER


class TestAuditDispatch(unittest.TestCase):
    """audit() dispatches on the input type."""

    def test_string_input_routes_to_nl_path(self):
        r = audit("I can lift 25 kg.")
        # NL path -> report carries claim / plan / parsed keys.
        self.assertIn('claim', r)
        self.assertIn('plan', r)
        self.assertIn('parsed', r)
        self.assertEqual(r['claim'], "I can lift 25 kg.")

    def test_dict_input_routes_to_structured_path(self):
        r = audit({'L4': {'lift_mass': 25.0}})
        # Structured path -> no claim/plan/parsed keys.
        self.assertNotIn('claim', r)
        self.assertNotIn('plan', r)
        self.assertNotIn('parsed', r)

    def test_neither_string_nor_dict_raises(self):
        with self.assertRaises(TypeError):
            audit(42)
        with self.assertRaises(TypeError):
            audit(None)
        with self.assertRaises(TypeError):
            audit([1, 2, 3])


class TestAuditReturnShape(unittest.TestCase):
    """Both paths share the integrated-stack result-dict shape."""

    def test_string_path_return_shape(self):
        r = audit("Hello.")
        for k in ('total_logp', 'per_layer', 'applicable_layers',
                  'skipped_layers', 'category_error_layers',
                  'cultural_flags', 'ontological_scope'):
            self.assertIn(k, r)

    def test_dict_path_return_shape(self):
        r = audit({})
        for k in ('total_logp', 'per_layer', 'applicable_layers',
                  'skipped_layers', 'category_error_layers',
                  'cultural_flags', 'ontological_scope'):
            self.assertIn(k, r)


class TestAuditScopeRouting(unittest.TestCase):
    """The ontological_scope argument reaches the layers."""

    def test_ai_scope_on_lift_refuses_via_L4(self):
        r = audit("I can lift 200 kg.",
                  ontological_scope='AI_silicon_substrate')
        self.assertIsNone(r['total_logp'])
        errs = [e['layer'] for e in r['category_error_layers']]
        self.assertIn('L4', errs)

    def test_ai_scope_on_dict_lift_refuses(self):
        r = audit({'L4': {'lift_mass': 200.0}},
                  ontological_scope='AI_silicon_substrate')
        self.assertIsNone(r['total_logp'])

    def test_human_scope_lift_scores(self):
        r = audit({'L4': {'lift_mass': 25.0}},
                  ontological_scope='any_WEIRD_human')
        self.assertIsNotNone(r['total_logp'])

    def test_ontological_scope_carried_back(self):
        r = audit({}, ontological_scope='human_cultural_artifact')
        self.assertEqual(r['ontological_scope'],
                          'human_cultural_artifact')


class TestReExports(unittest.TestCase):
    """entry.py re-exports commonly-needed symbols so callers can
    grab them from one place."""

    def test_layer_order_reexported(self):
        # entry.LAYER_ORDER matches integrated_stack.LAYER_ORDER.
        from integrated_stack import LAYER_ORDER as IS_ORDER
        self.assertEqual(LAYER_ORDER, IS_ORDER)


class TestBothPathsConverge(unittest.TestCase):
    """A structured plan and its NL equivalent should score similarly
    when the parser routes the same way."""

    def test_nl_and_dict_lift_produce_same_L4_result(self):
        r_nl = audit("I can lift 200 kg.")
        r_dict = audit({'L4': {'lift_mass': 200.0}})
        # Both should route to L4 alone and score identically.
        self.assertEqual(r_nl['applicable_layers'], ['L4'])
        self.assertEqual(r_dict['applicable_layers'], ['L4'])
        self.assertAlmostEqual(r_nl['total_logp'],
                                r_dict['total_logp'], places=6)


if __name__ == '__main__':
    unittest.main()
