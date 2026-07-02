"""
Smoke tests for play-sims extractions.

Two things this test module verifies:

  [1] Every .py in play-sims/ parses cleanly as Python. Extraction from
      Organize*.md is line-range surgery, so a bad boundary can leave
      dangling imports or half-statements. `ast.parse` catches those.

  [2] Every expected top-level function is defined in the file that
      claims it. The "pure-math helpers" we advertise in the top-level
      README have to actually exist in the modules they're supposed to
      live in.

We do NOT import the modules. Importing runs the demo (widget setup,
plt.figure, print, etc.), which is expensive AND requires numpy/mpl/
ipywidgets to all be installed. `ast.parse` is a lexical check only —
no execution, no external dependencies.

License: CC0
Dependencies: stdlib only (ast, unittest, pathlib)
"""

import ast
import os
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PLAY_SIMS = REPO_ROOT / 'play-sims'

DOMAINS = [
    'plasma-waves',
    'atmospheric-heating',
    'sponge-reef',
    'exoplanet-forensics',
    'photon-upconversion',
]


class TestFolderLayout(unittest.TestCase):
    def test_all_five_domain_folders_exist(self):
        for d in DOMAINS:
            with self.subTest(domain=d):
                self.assertTrue((PLAY_SIMS / d).is_dir(),
                                f'missing folder: play-sims/{d}')

    def test_every_domain_has_readme_and_requirements(self):
        for d in DOMAINS:
            with self.subTest(domain=d):
                self.assertTrue((PLAY_SIMS / d / 'README.md').is_file())
                self.assertTrue((PLAY_SIMS / d / 'requirements.txt').is_file())

    def test_top_level_readme_exists(self):
        self.assertTrue((PLAY_SIMS / 'README.md').is_file())


class TestExtractionParses(unittest.TestCase):
    """Every .py under play-sims/ must parse without SyntaxError. This
    is the extraction-boundary contract: sed pulled the right lines."""

    def test_all_play_sims_parse(self):
        py_files = sorted(p for d in DOMAINS
                          for p in (PLAY_SIMS / d).glob('*.py'))
        self.assertGreater(len(py_files), 0, 'no .py files found')
        for path in py_files:
            with self.subTest(file=path.relative_to(REPO_ROOT)):
                src = path.read_text(encoding='utf-8')
                try:
                    ast.parse(src, filename=str(path))
                except SyntaxError as e:
                    self.fail(f'{path.name}: SyntaxError at line '
                              f'{e.lineno}: {e.msg}')


class TestExpectedFunctionsDefined(unittest.TestCase):
    """Contract test: the pure-math helpers we advertise in the top-level
    README must actually be defined at module level. We parse the AST
    and look for FunctionDef / ClassDef nodes with the expected names —
    NO import, NO execution."""

    EXPECTED = {
        'plasma-waves/pic_plasma_dust_2d.py':
            ['poisson_solve', 'get_fields', 'deposit_charge',
             'interpolate_fields', 'init_particles'],
        'plasma-waves/wave_1d_fdtd_through_dust.py':
            ['run_simulation'],
        'plasma-waves/wave_2d_fdtd_through_dust.py':
            ['run_2d_simulation'],
        'exoplanet-forensics/multi_framework_forensics.py':
            ['generate_system', 'detect_transit', 'detect_rv',
             'detect_microlensing', 'detect_astrometry', 'run_survey'],
        'sponge-reef/reef_basic.py':
            ['Reef', 'Sponge', 'run_simulation'],
        'sponge-reef/reef_light_temp_herbivory.py':
            ['Reef', 'Sponge', 'run_simulation'],
        'sponge-reef/reef_seasons_pulses_larvae.py':
            ['Sponge', 'DynamicReef', 'run_dynamic_sim'],
        'atmospheric-heating/interactive_dashboard.py':
            ['density', 'atmospheric_density_profile',
             'orbital_entry_parameters', 'run_acoustic_simulation',
             'run_gcm_simulation', 'run_parameterised_sim'],
        'atmospheric-heating/flare_radio_climate_ultimate.py':
            ['AtmoCascade', 'ParticleSet', 'DischargeEngine',
             'RadioMapper', 'ClimateCoupling', 'run_master_sim'],
    }

    def test_expected_names_present(self):
        for rel, names in self.EXPECTED.items():
            path = PLAY_SIMS / rel
            with self.subTest(file=rel):
                self.assertTrue(path.is_file(), f'missing: {rel}')
                tree = ast.parse(path.read_text(encoding='utf-8'))
                defined = {n.name for n in ast.walk(tree)
                           if isinstance(n, (ast.FunctionDef,
                                             ast.AsyncFunctionDef,
                                             ast.ClassDef))}
                for expected in names:
                    self.assertIn(expected, defined,
                                  f'{rel}: expected {expected}() '
                                  f'/ class not found')


class TestSourceDocstringPresent(unittest.TestCase):
    """Each extracted .py gets a top-level docstring naming its Organize*.md
    source line range. Contract check: the extraction provenance is
    visible in every file, not hidden in the folder-level README."""

    def test_every_play_sim_has_module_docstring(self):
        py_files = sorted(p for d in DOMAINS
                          for p in (PLAY_SIMS / d).glob('*.py'))
        for path in py_files:
            with self.subTest(file=path.relative_to(REPO_ROOT)):
                tree = ast.parse(path.read_text(encoding='utf-8'))
                doc = ast.get_docstring(tree)
                self.assertIsNotNone(
                    doc, f'{path.name}: no module docstring')
                self.assertIn('Organize', doc,
                              f'{path.name}: docstring must mention '
                              f'the Organize*.md source')


if __name__ == '__main__':
    unittest.main()
