"""
Smoke tests for grounding-layers extractions.

Same shape as play-sims/tests/test_extraction_shape.py: parse check,
module-docstring check, expected top-level-name check. No import, no
execution — purely lexical (ast.parse + ast.walk).

License: CC0
Dependencies: stdlib only (ast, unittest, pathlib)
"""

import ast
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LAYERS = REPO_ROOT / 'grounding-layers'

EXPECTED_FILES = [
    'l0_physics_causality.py',
    'l1_thermodynamics_entropy.py',
    'l2_planetary_mass_balance.py',
    'l3_ecological_homeostasis.py',
    'l4_biomechanical_sensorimotor.py',
    'l5_human_construct.py',
    'l_epsilon_epistemic.py',
    'temporal_dysrhythmia.py',
    'tensor_field_resilience_v1.py',
    'tensor_field_resilience_v2.py',
]


class TestFolderShape(unittest.TestCase):
    def test_all_ten_files_present(self):
        for name in EXPECTED_FILES:
            with self.subTest(name=name):
                self.assertTrue((LAYERS / name).is_file(),
                                f'missing: grounding-layers/{name}')

    def test_readme_and_requirements_exist(self):
        self.assertTrue((LAYERS / 'README.md').is_file())
        self.assertTrue((LAYERS / 'requirements.txt').is_file())


class TestExtractionParses(unittest.TestCase):
    def test_each_layer_parses(self):
        for name in EXPECTED_FILES:
            path = LAYERS / name
            with self.subTest(file=name):
                try:
                    ast.parse(path.read_text(encoding='utf-8'),
                              filename=str(path))
                except SyntaxError as e:
                    self.fail(f'{name}: SyntaxError at line {e.lineno}: '
                              f'{e.msg}')


class TestProvenanceDocstring(unittest.TestCase):
    """Each extracted .py has a module docstring that names its
    legacy/Organize3.md source and line range. Contract check on
    provenance."""

    def test_every_layer_has_docstring_citing_source(self):
        for name in EXPECTED_FILES:
            path = LAYERS / name
            with self.subTest(file=name):
                tree = ast.parse(path.read_text(encoding='utf-8'))
                doc = ast.get_docstring(tree)
                self.assertIsNotNone(doc, f'{name}: no module docstring')
                self.assertIn('Organize', doc,
                              f'{name}: docstring must name '
                              f'the legacy/Organize*.md source')


class TestExpectedNamesDefined(unittest.TestCase):
    """The L-stack sims all define a class or function whose name
    references the layer. Contract check that the extraction landed
    the code, not just the banner comments."""

    EXPECTED = {
        'l5_human_construct.py': ['L5_Faction'],
        'tensor_field_resilience_v1.py': ['coupling_monoculture',
                                           'coupling_tensegrity'],
        'tensor_field_resilience_v2.py': ['coupling_unstable',
                                           'coupling_resilient'],
    }

    def test_expected_names_present(self):
        for filename, names in self.EXPECTED.items():
            path = LAYERS / filename
            with self.subTest(file=filename):
                tree = ast.parse(path.read_text(encoding='utf-8'))
                defined = set()
                for n in ast.walk(tree):
                    if isinstance(n, (ast.FunctionDef,
                                      ast.AsyncFunctionDef,
                                      ast.ClassDef)):
                        defined.add(n.name)
                    elif isinstance(n, ast.Assign):
                        for t in n.targets:
                            if isinstance(t, ast.Name):
                                defined.add(t.id)
                for expected in names:
                    self.assertIn(expected, defined,
                                  f'{filename}: expected top-level '
                                  f'{expected} not found')


if __name__ == '__main__':
    unittest.main()
