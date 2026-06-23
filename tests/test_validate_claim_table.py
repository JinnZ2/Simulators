"""
Tests for the shared CLAIM_TABLE validator.

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

from tools.validate_claim_table import (
    validate_claim_table,
    validate_file,
    main,
)


class TestValidateClaimTable(unittest.TestCase):
    def test_minimal_valid_table(self):
        report = validate_claim_table({
            'schema_version': '1.0',
            'source_repo': 'test',
            'claims': [
                {'claim_id': 'X_001', 'statement': 's',
                 'falsification_criteria': 'f', 'status': 'proposed'},
            ],
        })
        self.assertEqual(report['errors'], [])
        self.assertEqual(report['warnings'], [])
        self.assertEqual(report['claim_count'], 1)
        self.assertEqual(report['claim_ids'], ['X_001'])

    def test_missing_claims_is_error(self):
        report = validate_claim_table({'schema_version': '1.0'})
        self.assertTrue(any('claims' in e for e in report['errors']))

    def test_claims_must_be_list(self):
        report = validate_claim_table({
            'schema_version': '1.0', 'claims': {'x': 1},
        })
        self.assertTrue(any('list' in e for e in report['errors']))

    def test_missing_claim_id_is_error(self):
        report = validate_claim_table({
            'schema_version': '1.0',
            'claims': [{'statement': 's'}],
        })
        self.assertTrue(any('claim_id' in e for e in report['errors']))

    def test_hypothesis_accepted_as_descriptor(self):
        # research-stability-audit style
        report = validate_claim_table({
            'schema_version': '1.0',
            'source_repo': 'research-stability-audit',
            'claims': [{
                'claim_id': 'R_001', 'hypothesis': 'h',
                'is_falsified': False,
                'falsification_criteria': 'f',
            }],
        })
        self.assertEqual(report['errors'], [])

    def test_duplicate_claim_ids_flagged(self):
        report = validate_claim_table({
            'schema_version': '1.0',
            'claims': [
                {'claim_id': 'X_001', 'statement': 's'},
                {'claim_id': 'X_001', 'statement': 's'},
            ],
        })
        self.assertTrue(any('duplicate' in e for e in report['errors']))

    def test_missing_source_repo_is_warning(self):
        report = validate_claim_table({
            'schema_version': '1.0',
            'claims': [{'claim_id': 'X_001', 'statement': 's',
                        'falsification_criteria': 'f', 'status': 'proposed'}],
        })
        self.assertEqual(report['errors'], [])
        self.assertTrue(any('source' in w for w in report['warnings']))

    def test_missing_schema_version_is_warning(self):
        report = validate_claim_table({
            'source_repo': 'test',
            'claims': [{'claim_id': 'X_001', 'statement': 's',
                        'falsification_criteria': 'f', 'status': 'proposed'}],
        })
        self.assertTrue(any('schema_version' in w for w in report['warnings']))

    def test_top_level_must_be_dict(self):
        report = validate_claim_table([])
        self.assertTrue(any('object' in e for e in report['errors']))


class TestValidateFile(unittest.TestCase):
    def test_missing_file(self):
        report = validate_file(Path('/tmp/definitely_not_there.json'))
        self.assertTrue(any('not found' in e for e in report['errors']))

    def test_invalid_json(self):
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w') as f:
            f.write('{not valid json')
            path = Path(f.name)
        try:
            report = validate_file(path)
            self.assertTrue(any('invalid JSON' in e for e in report['errors']))
        finally:
            path.unlink()

    def test_round_trip_through_file(self):
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w') as f:
            json.dump({
                'schema_version': '1.0',
                'source_repo': 'test',
                'claims': [{'claim_id': 'X', 'statement': 's',
                            'falsification_criteria': 'f',
                            'status': 'proposed'}],
            }, f)
            path = Path(f.name)
        try:
            report = validate_file(path)
            self.assertEqual(report['errors'], [])
            self.assertEqual(report['claim_count'], 1)
        finally:
            path.unlink()


class TestCli(unittest.TestCase):
    def test_no_args_returns_2(self):
        self.assertEqual(main(['validate_claim_table.py']), 2)

    def test_clean_file_returns_0(self):
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w') as f:
            json.dump({
                'schema_version': '1.0',
                'source_repo': 'test',
                'claims': [{'claim_id': 'X', 'statement': 's',
                            'falsification_criteria': 'f',
                            'status': 'proposed'}],
            }, f)
            path = Path(f.name)
        try:
            self.assertEqual(main(['validate_claim_table.py', str(path)]), 0)
        finally:
            path.unlink()

    def test_error_file_returns_1(self):
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w') as f:
            json.dump({'schema_version': '1.0', 'claims': [{}]}, f)
            path = Path(f.name)
        try:
            self.assertEqual(main(['validate_claim_table.py', str(path)]), 1)
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
