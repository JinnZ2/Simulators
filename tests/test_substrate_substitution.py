"""
Tests for the substrate_substitution methodology tool.

License: CC0
Dependencies: stdlib only (unittest)
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.substrate_substitution import (
    substitute_claim,
    evaluate_claim_with_substitution,
    evaluate_claim_table,
    main,
)


class TestSubstitution(unittest.TestCase):
    def test_substrate_to_grass(self):
        self.assertIn('grass',
                      substitute_claim('substrate populations sustain'))

    def test_narrative_to_grasshoppers(self):
        self.assertIn('grasshoppers',
                      substitute_claim('narrative is a consumer'))

    def test_compound_phrases_substituted_first(self):
        # Multi-word phrase should be substituted as a unit, not
        # have its constituent words replaced piecemeal.
        out = substitute_claim('narrative_population growth')
        self.assertIn('grasshopper swarm', out)
        self.assertNotIn('grasshoppers_population', out)

    def test_scale_builder_to_wind_dispersed_insect(self):
        out = substitute_claim('scale_builder helps substrate scale')
        self.assertIn('wind-dispersed insect', out)
        self.assertIn('grass', out)

    def test_inverted_narrative_to_overgrazing(self):
        out = substitute_claim('inverted_narrative drives substrate to collapse')
        self.assertIn('overgrazing', out)
        self.assertIn('grass', out)

    def test_no_substitution_passes_through(self):
        text = 'reproducibility failure rate exceeds 50 percent'
        self.assertEqual(substitute_claim(text), text)

    def test_empty_string(self):
        self.assertEqual(substitute_claim(''), '')

    def test_none_returns_unchanged(self):
        # The function is meant to be tolerant of empty input.
        self.assertEqual(substitute_claim(None), None)


class TestEvaluateClaim(unittest.TestCase):
    def test_evaluate_marks_substrate_claim_as_changed(self):
        claim = {
            'claim_id': 'X_001',
            'statement': 'narrative amplifies substrate reach',
            'status': 'refuted',
        }
        ev = evaluate_claim_with_substitution(claim)
        self.assertTrue(ev['changed'])
        self.assertIn('grass', ev['substituted']['statement'])
        self.assertTrue(ev['requires_review'])

    def test_evaluate_unchanged_when_no_substrate_terms(self):
        claim = {
            'claim_id': 'X_002',
            'statement': 'reproducibility failure rate exceeds 50%',
        }
        ev = evaluate_claim_with_substitution(claim)
        self.assertFalse(ev['changed'])

    def test_evaluate_substitutes_multiple_fields(self):
        claim = {
            'claim_id': 'X_003',
            'statement': 'narrative supports substrate',
            'prediction': 'narrative_amplifies_substrate',
            'falsification_criteria': 'substrate fails without narrative',
        }
        ev = evaluate_claim_with_substitution(claim)
        for field in ('statement', 'prediction', 'falsification_criteria'):
            self.assertIn('grass', ev['substituted'][field])


class TestEvaluateTable(unittest.TestCase):
    def test_loads_file_and_reports_counts(self):
        table = {
            'schema_version': '1.0',
            'source_repo': 'test',
            'claims': [
                {'claim_id': 'A', 'statement': 'narrative amplifies substrate'},
                {'claim_id': 'B', 'statement': 'no special terms here'},
            ],
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False) as f:
            json.dump(table, f)
            path = Path(f.name)
        try:
            report = evaluate_claim_table(path)
            self.assertEqual(report['claim_count'], 2)
            self.assertEqual(report['changed_count'], 1)
        finally:
            path.unlink()


class TestCli(unittest.TestCase):
    def test_no_args_returns_2(self):
        self.assertEqual(main(['substrate_substitution.py']), 2)

    def test_evaluates_claim_table(self):
        table = {
            'schema_version': '1.0',
            'source_repo': 'test',
            'claims': [
                {'claim_id': 'A', 'statement': 'narrative amplifies substrate'},
            ],
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False) as f:
            json.dump(table, f)
            path = Path(f.name)
        try:
            self.assertEqual(main(['substrate_substitution.py', str(path)]), 0)
        finally:
            path.unlink()


if __name__ == '__main__':
    unittest.main()
