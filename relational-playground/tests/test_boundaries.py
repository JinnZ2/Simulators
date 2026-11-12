import unittest
from helpers import *
from playground.boundaries import BoundaryMatrix, compare, choose
from playground.relationships import RelationalMatrix, Relationship

U = dict(location="UNDECLARED", thickness="UNDECLARED", permeability="UNDECLARED", exchange_rates="UNDECLARED",
         mobility="UNDECLARED", uncertainty="UNDECLARED")
REL = RelationalMatrix([Relationship("grid", "hardware", "energy transfer"), Relationship("hardware", "software", "structural dependency"),
                        Relationship("mine", "hardware", "matter transfer")])
Z = lambda **ext: {n: ("exterior" if n in ext else "interior") for n in ("software", "hardware", "grid", "mine")}
A_ = BoundaryMatrix("A software", "fixed", Z(hardware=1, grid=1, mine=1), **U)
D_ = BoundaryMatrix("D supply network", "distributed", Z(), **U)


class T(unittest.TestCase):
    def test_boundary_change_moves_classification_not_observations(self):
        obs = dict(power_kw=3.2)
        before = dict(obs)
        c = compare(A_, D_, REL)
        self.assertEqual(c["became_internal"], ["grid", "hardware", "mine"])
        self.assertEqual(len(c["relationships_new"]), 2)       # grid->hardware and mine->hardware become visible
        self.assertEqual(obs, before)

    def test_no_automatic_selection(self):
        self.assertRaises(RuntimeError, choose, [A_, D_])

    def test_unzoned_node_is_not_guessed(self):
        self.assertRaises(KeyError, A_.zone, "cooling")

    def test_reciprocity_not_assumed(self):
        self.assertFalse(REL.reciprocal(REL.rels[0]))

    def test_several_boundaries_coexist(self):
        s = system()
        s.add_boundary(A_)
        s.add_boundary(D_)
        self.assertEqual(sorted(s.boundaries), ["A software", "D supply network"])
        self.assertRaises(ValueError, s.add_boundary, A_)

    def test_fields_must_be_written(self):
        self.assertRaises(ValueError, BoundaryMatrix, "x", "fixed", {})


if __name__ == "__main__":
    unittest.main()
