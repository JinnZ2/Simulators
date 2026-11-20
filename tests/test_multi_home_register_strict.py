"""Strict in_map rule: YES needs one map row that names the concept (concept or covers) and
lists every registered home. Constructed map rows only; no sibling checkout is read."""
import importlib.util
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("bmhr", os.path.join(ROOT, "build_multi_home_register.py"))
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)

HOMES = [{"repo": "A", "path": "x.py"}, {"repo": "B", "path": "y.py"}]


def data(concept="umbrella", covers=None, paths=(("A", "x.py"), ("B", "y.py"))):
    row = {"concept": concept, "locations": [{"repo": r, "path": p} for r, p in paths]}
    if covers is not None:
        row["covers"] = covers
    return {"rows": [row]}


class Strict(unittest.TestCase):
    def test_named_in_concept_all_homes(self):
        self.assertEqual(B.strict_in_map("fine", HOMES, data(concept="fine"))[0], "YES")

    def test_named_in_covers_all_homes(self):
        self.assertEqual(B.strict_in_map("fine", HOMES, data(covers=["fine"]))[0], "YES")

    def test_homes_listed_but_not_named(self):
        self.assertEqual(B.strict_in_map("fine", HOMES, data())[0], "PARTIAL")

    def test_named_but_a_home_missing(self):
        self.assertEqual(B.strict_in_map("fine", HOMES, data(covers=["fine"], paths=(("A", "x.py"),)))[0], "PARTIAL")

    def test_homes_split_across_two_rows(self):
        d = {"rows": [{"concept": "r1", "covers": ["fine"], "locations": [{"repo": "A", "path": "x.py"}]},
                      {"concept": "r2", "locations": [{"repo": "B", "path": "y.py"}]}]}
        self.assertEqual(B.strict_in_map("fine", HOMES, d)[0], "PARTIAL")

    def test_nothing(self):
        self.assertEqual(B.strict_in_map("fine", HOMES, data(paths=(("C", "z.py"),)))[0], "NO")


if __name__ == "__main__":
    unittest.main()
