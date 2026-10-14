# SPDX-License-Identifier: CC0-1.0
"""Controls for the supplied maze instrument; not external validation.

The small seeded evolve fixture is only a reproducibility check. It is not
one of the twenty fixed-budget experimental runs in the committed sample.
Run: python3 tests/test_deceptive_maze_ga.py
"""
import hashlib
import importlib.util
from pathlib import Path
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "deceptive_maze_ga.py"
SPEC = importlib.util.spec_from_file_location("maze_controls", SOURCE)
maze = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(maze)


class MazeControls(unittest.TestCase):
    def test_original_source_hash(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()[:3876]).hexdigest(),
                         "c8aef02c9f891112e6fe7b0bc2fe7406321d19c5c2861d33c53955a4ec77f0e6")

    def test_parameters_unchanged(self):
        self.assertEqual((maze.POP, maze.GENS, maze.L, maze.MUT,
                          maze.TOUR, maze.ELITE, maze.K_NN, maze.ARCHIVE_ADD),
                         (100, 150, 60, 0.05, 3, 2, 15, 3))
        self.assertEqual(maze.SEEDS, list(range(10)))

    def test_handwritten_detour_reaches_goal(self):
        route = [2] * 11 + [0] * 12 + [3] * 11
        self.assertEqual(len(route), 34)
        self.assertEqual(maze.run_path(route), (maze.GOAL, True))

    def test_greedy_north_hits_pocket(self):
        self.assertEqual(maze.run_path([0] * maze.L), ((2, 6), False))
        self.assertEqual(maze.objective((2, 6)), -7.0)

    def test_border_walls_prevent_escape(self):
        self.assertEqual(maze.run_path([3] * maze.L), ((1, 1), False))
        self.assertEqual(maze.run_path([1] * maze.L), ((2, 1), False))

    def test_only_horizontal_gap_is_x13(self):
        self.assertEqual([x for x in range(1, 14) if (x, 7) not in maze.WALLS], [13])

    def test_solve_is_anytime_not_endpoint_only(self):
        route = [2] * 11 + [0] * 12 + [3] * 11 + [1]
        self.assertEqual(maze.run_path(route), ((2, 12), True))
        self.assertEqual(maze.objective((2, 12)), -1.0)

    def test_known_distance(self):
        self.assertEqual(maze.dist((0, 0), (3, 4)), 5.0)
        self.assertEqual(maze.dist((3, 4), (3, 4)), 0.0)

    def test_novelty_excludes_one_self(self):
        self.assertEqual(maze.novelty((0, 0), [(0, 0)] + [(3, 4)] * 15), 5.0)
        self.assertEqual(maze.novelty((0, 0), [(0, 0)] * 16), 0.0)

    def test_novelty_duplicates_are_peers_not_deduplicated(self):
        pool = [(0, 0)] * 8 + [(3, 4)] * 8
        self.assertAlmostEqual(maze.novelty((0, 0), pool), 8 / 3)

    def test_small_pool_fixed_denominator_limit_is_preserved(self):
        # Source divides by K=15 even with fewer than 15 neighbors.
        # Actual experiment pool >=100, so this is an out-of-regime limit.
        self.assertEqual(maze.novelty((0, 0), [(0, 0), (3, 4)]), 5 / 15)

    def test_known_mean_entropy(self):
        self.assertEqual(maze.locus_entropy([[0] * maze.L] * 4), 0.0)
        self.assertEqual(maze.locus_entropy([[0] * maze.L, [2] * maze.L]), 1.0)
        self.assertEqual(maze.locus_entropy([[i] * maze.L for i in range(4)]), 2.0)

    def test_half_threshold_is_strict(self):
        self.assertEqual(maze.half_gen([2.0, 1.0, 0.99]), 2)
        self.assertIsNone(maze.half_gen([2.0, 1.0, 1.0]))
        self.assertIsNone(maze.half_gen([0.0, 0.0]))

    def test_seed_reproducibility_on_small_fixture(self):
        with mock.patch.multiple(maze, POP=20, GENS=4, K_NN=5):
            for mode in ("objective", "novelty"):
                self.assertEqual(maze.evolve(mode, 7), maze.evolve(mode, 7))

    def test_passive_ledger_does_not_change_search(self):
        with mock.patch.multiple(maze, POP=20, GENS=4, K_NN=5):
            for mode in ("objective", "novelty"):
                original = maze.evolve(mode, 7)
                first = maze.evolve_ledger(mode, 7, "final_cell")
                again = maze.evolve_ledger(mode, 7, "final_cell")
                second = maze.evolve_ledger(mode, 7, "visited_cells")
                self.assertEqual(first, again)
                for run in (first, second):
                    self.assertEqual((run["solved_gen"], run["genotype_entropy_bits_per_locus"],
                                      run["archive_size"]), original)

    def test_same_final_cell_can_hide_different_visited_sets(self):
        self.assertEqual(maze.path_descriptor([], "final_cell"),
                         maze.path_descriptor([2, 3], "final_cell"))
        self.assertNotEqual(maze.path_descriptor([], "visited_cells"),
                            maze.path_descriptor([2, 3], "visited_cells"))

    def test_committed_sample_is_complete(self):
        text = (ROOT / "tools" / "samples" /
                "deceptive_maze.original.sample.txt").read_text()
        self.assertEqual(sum(line.startswith(" seed ") for line in text.splitlines()), 20)
        self.assertIn("--- objective ---", text)
        self.assertIn("--- novelty ---", text)
        # Completeness, not a tuned expected number of successes.
        self.assertEqual(sum(line.startswith(" => solved ") for line in text.splitlines()), 2)


if __name__ == "__main__":
    unittest.main()
