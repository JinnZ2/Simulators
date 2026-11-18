"""M4 closure gate declarations (COMBINED_SPEC section 2, R-A1 / R-A4; section 8 rows 4-7, 41).

Written before cplay/closure.py. The verdict rule is a spec gap (see test_verdict_is_a_spec_gap).
"""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import closure as C  # noqa: E402
from cplay import tokens as T  # noqa: E402
from cplay import axes as A  # noqa: E402


def _decl(acct="N", tol=1e-6, sigma=None, k=None, basis="declared"):
    return C.AccountDecl(account=acct, tolerance=tol, sigma=sigma, k=k, basis=basis)


def _prereg(accounts=None, **kw):
    base = dict(accounts=accounts or [_decl()], declared_complete=True,
                registry=("fertiliser input",), roundoff_floor=1e-12)
    base.update(kw)
    return C.Prereg(**base)


class Declarations(unittest.TestCase):
    def test_tolerance_required_per_account_no_default(self):
        with self.assertRaises(TypeError):
            C.AccountDecl(account="N", basis="b")
        for bad in (None, -1.0, "1e-9", True):
            with self.assertRaises(C.ClosureError):
                _decl(tol=bad)

    def test_sigma_and_k_must_be_passed_none_allowed(self):
        with self.assertRaises(TypeError):
            C.AccountDecl(account="N", tolerance=1e-6, basis="b")
        d = _decl(sigma=None, k=None)
        self.assertIsNone(d.sigma)

    def test_roundoff_floor_is_its_own_field_not_in_account(self):
        self.assertNotIn("roundoff", C.AccountDecl._fields)
        p = _prereg(roundoff_floor=5e-11)
        self.assertEqual(p.roundoff_floor, 5e-11)
        with self.assertRaises(TypeError):
            C.Prereg(accounts=[_decl()], declared_complete=True, registry=("x",))

    def test_duplicate_account_refused(self):
        with self.assertRaises(C.ClosureError):
            _prereg(accounts=[_decl("N"), _decl("N")])


class Ledger(unittest.TestCase):
    def test_R_A1_declared_complete_three_states(self):
        self.assertEqual(_prereg(declared_complete=True).complete_state, "DECLARED")
        self.assertEqual(_prereg(declared_complete=False).complete_state, "NOT_DECLARED")
        self.assertEqual(_prereg(declared_complete=C.ABSENT).complete_state, "ABSENT")
        for bad in (1, "True", None):
            with self.assertRaises(C.ClosureError):
                _prereg(declared_complete=bad)

    def test_ledger_counts_as_declared_only_when_declared(self):
        self.assertTrue(_prereg(declared_complete=True).counts_as_declared)
        self.assertFalse(_prereg(declared_complete=C.ABSENT).counts_as_declared)

    def test_empty_registry_is_a_token_not_an_absent_list(self):
        for bad in ((), [], None):
            with self.assertRaises(C.ClosureError):
                _prereg(registry=bad)
        p = _prereg(registry=T.Token("UNTESTED", "no intervention registered"))
        self.assertEqual(p.registry.state, "UNTESTED")
        with self.assertRaises(C.ClosureError):
            _prereg(registry=T.Token("OK"))


class Prereg(unittest.TestCase):
    def test_hash_stable_and_moves_on_change(self):
        a, b = _prereg(), _prereg()
        self.assertEqual(a.sha256, b.sha256)
        self.assertNotEqual(a.sha256, _prereg(accounts=[_decl(tol=2e-6)]).sha256)
        self.assertEqual(len(a.sha256), 64)


class Run(unittest.TestCase):
    def _obs(self, acct="N", m=3e-7, prov="ledger sum"):
        return C.Misclosure(account=acct, value=m, provenance=prov)

    def test_run_needs_the_preregistered_hash(self):
        p = _prereg()
        with self.assertRaises(C.ClosureError):
            C.run(p, "0" * 64, [self._obs()])
        C.run(p, p.sha256, [self._obs()])

    def test_R_A4_undeclared_account_refuses_the_run(self):
        p = _prereg()
        res = C.run(p, p.sha256, [self._obs("N"), self._obs("P")])
        self.assertEqual(res.state, "REFUSED")
        self.assertIn("P", res.reason)

    def test_value_provenance_is_a_field(self):
        with self.assertRaises(C.ClosureError):
            C.Misclosure(account="N", value=1e-7, provenance="")

    def test_accepted_run_carries_prereg_and_roundoff_floor(self):
        p = _prereg()
        res = C.run(p, p.sha256, [self._obs()])
        self.assertEqual(res.prereg_sha256, p.sha256)
        self.assertEqual(res.roundoff_floor, 1e-12)
        self.assertEqual(res.state, "ACCEPTED")

    def test_verdict_is_a_spec_gap(self):
        p = _prereg(accounts=[_decl(sigma=1e-6, k=3)])
        res = C.run(p, p.sha256, [self._obs()])
        with self.assertRaises(C.SpecGap):
            C.verdict(res, "N")


if __name__ == "__main__":
    unittest.main()


class Branches(unittest.TestCase):
    """Follow-up item 2: three candidate verdict rules beside verdict(), which keeps raising."""
    def _res(self, m, tol=1e-6, sigma=1e-6, k=3, floor=1e-12, complete=True):
        p = _prereg(accounts=[_decl(tol=tol, sigma=sigma, k=k)], roundoff_floor=floor,
                    declared_complete=complete)
        obs = C.Misclosure(account="N", value=m, provenance="declared ledger sum")
        return C.run(p, p.sha256, [obs]), obs

    def test_verdict_still_raises(self):
        res, obs = self._res(1e-7)
        with self.assertRaises(C.SpecGap):
            C.verdict(res, "N")

    def test_misclosure_must_be_declared_input(self):
        res, _ = self._res(1e-7)
        other = C.Misclosure(account="N", value=1e-7, provenance="not in the run")
        for fn in C.BRANCHES.values():
            with self.assertRaises(C.ClosureError):
                fn(res)                                    # misclosure argument required
            with self.assertRaises(C.ClosureError):
                fn(res, other)                             # must be one the run accepted

    def test_refused_run_has_no_branch_verdict(self):
        p = _prereg()
        obs = C.Misclosure(account="P", value=1e-7, provenance="x")
        res = C.run(p, p.sha256, [obs])
        with self.assertRaises(C.ClosureError):
            C.verdict_branch_A(res, obs)

    def test_branches_differ_where_designed(self):
        res, obs = self._res(1e-7)                         # inside tol and inside k*sigma
        self.assertEqual(C.verdict_branch_A(res, obs).status, "OK")
        self.assertEqual(C.verdict_branch_C(res, obs).status, "CLOSED_WITHIN")
        res, obs = self._res(1.0000005e-6, sigma=None, k=None, floor=1e-9)
        self.assertEqual(C.verdict_branch_A(res, obs).status, "FAILED")
        self.assertEqual(C.verdict_branch_B(res, obs).status, "OK")

    def test_failed_routes_by_declared_complete(self):
        res, obs = self._res(5e-6)
        self.assertEqual(C.verdict_branch_A(res, obs).field, "PHYSICAL")
        res, obs = self._res(5e-6, complete=C.ABSENT)
        self.assertEqual(C.verdict_branch_A(res, obs).field, "DETERMINATION")

    def test_branch_B_token_floor_is_void(self):
        res, obs = self._res(5e-7, floor=T.Token("UNTESTED", "floor not measured"))
        self.assertEqual(C.verdict_branch_B(res, obs).state, "VOID")

    def test_table_and_split_rows(self):
        rows = C.branch_table()
        self.assertEqual(len(rows), 11)
        cases = lambda key: [r["case"] for r in rows if r[key]]
        self.assertEqual(cases("split"), ["c1", "c2", "c4", "c5", "c6", "c7", "c9", "c10"])
        self.assertEqual(cases("split_live"), ["c1", "c2", "c4", "c9", "c10"])
        self.assertEqual(cases("split_abc"), ["c1", "c4", "c6", "c10"])
        self.assertEqual(cases("split_af"), ["c1", "c2", "c4", "c5", "c6", "c7", "c9", "c10"])
        self.assertEqual([r["case"] for r in rows if r["g_pre"] == "I:TOL_UNRES"], ["c1", "c2", "c3", "c8"])
        g = {r["case"]: r["branches"]["G"] for r in rows}
        self.assertEqual((g["c9"], g["c10"], g["c11"]),
                         ("PHYSICAL:CLOSED_WITHIN", "PHYSICAL:OK", "PHYSICAL:FAILED"))
        self.assertEqual([r["case"] for r in rows if r["g_differs"]], ["c1", "c2"])
        for r in rows:
            self.assertEqual(sorted(r["branches"]), list("ABCDEFG"))

    def test_branch_D_floor_first(self):
        res, obs = self._res(1e-13)
        self.assertEqual(C.verdict_branch_D(res, obs).status, "OK")
        res, obs = self._res(5e-7)
        self.assertEqual(C.verdict_branch_D(res, obs).status, "CLOSED_WITHIN")
        res, obs = self._res(2e-6)
        self.assertEqual(C.verdict_branch_D(res, obs).status, "FAILED")
        res, obs = self._res(5e-7, sigma=None, k=None)
        self.assertEqual(C.verdict_branch_D(res, obs).state, "VOID")      # CLOSED_WITHIN needs sigma
        res, obs = self._res(5e-7, floor=T.Token("UNTESTED", "x"))
        self.assertEqual(C.verdict_branch_D(res, obs).state, "VOID")

    def test_branch_E_band_is_max_of_tol_and_k_sigma(self):
        res, obs = self._res(2e-6)                        # tol 1e-6 < 2e-6 <= k*sigma 3e-6
        self.assertEqual(C.verdict_branch_E(res, obs).status, "CLOSED_WITHIN")
        res, obs = self._res(2e-6, sigma=1e-7, k=3)       # band = tol = 1e-6
        self.assertEqual(C.verdict_branch_E(res, obs).status, "FAILED")
        res, obs = self._res(1e-13)
        self.assertEqual(C.verdict_branch_E(res, obs).status, "OK")

    def test_branch_F_legs_and_cap(self):
        res, obs = self._res(5e-7)
        self.assertEqual(C.verdict_branch_F(res, obs).state, "VOID")        # n_legs missing
        for bad in (0, 2.0, True, "4"):
            self.assertEqual(C.verdict_branch_F(res, obs, n_legs=bad).state, "VOID")
        r = C.verdict_branch_F(res, obs, n_legs=4)
        self.assertEqual(r.status, "CLOSED_WITHIN")
        self.assertAlmostEqual(r.sigma, 2e-6)                               # sigma * sqrt(4)
        res, obs = self._res(2e-6, tol=1e-6)                                # above the hard cap
        self.assertEqual(C.verdict_branch_F(res, obs, n_legs=100).status, "FAILED")
        res, obs = self._res(9e-7, tol=1e-5, sigma=1e-7, k=3)               # allowable 3e-7*sqrt(1)
        self.assertEqual(C.verdict_branch_F(res, obs, n_legs=1).status, "FAILED")
        res, obs = self._res(5e-7, sigma=None, k=None)
        self.assertEqual(C.verdict_branch_F(res, obs, n_legs=4).state, "VOID")

    def test_failed_routing_cites_section_2(self):
        doc = C.__doc__
        self.assertIn("lines 62-65", doc)
        self.assertIn("R-A1, lines 82-84", doc)
        spec = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                            "playground-crossrun", "COMBINED_SPEC.md")
        lines = open(spec).read().splitlines()
        self.assertIn("ledger declared -> PHYSICAL : FAILED", lines[61])
        self.assertIn("ledger NOT      -> DETERMINATION : FAILED", lines[63])
        self.assertIn("R-A1", lines[81])


class BranchG(unittest.TestCase):
    """Guard-band rule: U = k*sigma + floor; UNRESOLVED on INSTRUMENT, never PHYSICAL."""
    def _res(self, m, tol=1e-5, sigma=1e-7, k=2, floor=1e-12, complete=True):
        p = _prereg(accounts=[_decl(tol=tol, sigma=sigma, k=k)], roundoff_floor=floor,
                    declared_complete=complete)
        obs = C.Misclosure(account="N", value=m, provenance="declared")
        return C.run(p, p.sha256, [obs]), obs

    def test_four_zones(self):                        # U = 2e-7 + 1e-12, tol 1e-5
        r, o = self._res(0.0)
        self.assertEqual(C.verdict_branch_G(r, o).status, "OK")        # exact tier: |m| <= floor
        r, o = self._res(5e-13)
        self.assertEqual(C.verdict_branch_G(r, o).status, "OK")
        r, o = self._res(9e-6)
        self.assertEqual(C.verdict_branch_G(r, o).status, "CLOSED_WITHIN")   # was OK before relabel
        r, o = self._res(1.0e-5)
        g = C.verdict_branch_G(r, o)
        self.assertIsInstance(g, C.FieldToken)
        self.assertEqual((g.field, g.token.state), ("INSTRUMENT", "UNRESOLVED"))
        self.assertIn("NOT_CHECKED", g.token.reason)
        r, o = self._res(1.1e-5)
        self.assertEqual(C.verdict_branch_G(r, o).status, "FAILED")
        r, o = self._res(1.1e-5, complete=C.ABSENT)
        self.assertEqual(C.verdict_branch_G(r, o).field, "DETERMINATION")

    def test_unresolved_never_physical(self):
        with self.assertRaises(C.ClosureError):
            C.FieldToken("PHYSICAL", T.Token("UNRESOLVED", "x"))
        with self.assertRaises(C.ClosureError):
            C.FieldToken("INSTRUMENT", T.Token("FAILED", "x"))
        with self.assertRaises(A.AxisError):
            A.reading("PHYSICAL", "UNRESOLVED", reason="x")     # not an axis status

    def test_sigma_or_k_missing_void(self):
        for kw in ({"sigma": None}, {"k": None}):
            r, o = self._res(5e-6, **kw)
            self.assertEqual(C.verdict_branch_G(r, o).state, "VOID")

    def test_token_floor_void_and_floor_added_to_u(self):
        r, o = self._res(5e-6, floor=T.Token("UNTESTED", "x"))
        self.assertEqual(C.verdict_branch_G(r, o).state, "VOID")
        # floor widens U: 9.75e-6 is CW with floor 0 (U = 2e-7) but not with floor 1e-7 (U = 3e-7)
        r, o = self._res(9.75e-6, floor=0)
        self.assertEqual(C.verdict_branch_G(r, o).status, "CLOSED_WITHIN")
        r, o = self._res(9.75e-6, floor=1e-7)
        self.assertEqual(C.verdict_branch_G(r, o).token.state, "UNRESOLVED")

    def test_empty_acceptance_zone_no_cw(self):
        r, o = self._res(1e-9, tol=1e-7, sigma=1e-7, k=2)       # U > tol
        self.assertEqual(C.verdict_branch_G(r, o).token.state, "UNRESOLVED")

    def test_precondition_tolerance_unresolvable_independent_of_m(self):
        for m in (0.0, 1e-9, 5e-8, 1.0):
            r, o = self._res(m, tol=1e-7, sigma=1e-7, k=2)      # U = 2e-7 >= tol
            pre = C.g_precondition(r, "N")
            self.assertEqual((pre.field, pre.token.state), ("INSTRUMENT", "TOLERANCE_UNRESOLVABLE"))
        r, o = self._res(0.0, tol=2e-7 + 1e-12, sigma=1e-7, k=2)   # U == tol -> flagged (>=)
        self.assertEqual(C.g_precondition(r, "N").token.state, "TOLERANCE_UNRESOLVABLE")
        r, o = self._res(0.0)                                   # U < tol
        self.assertIsNone(C.g_precondition(r, "N"))
        r, o = self._res(0.0, sigma=None)
        self.assertEqual(C.g_precondition(r, "N").state, "VOID")
        with self.assertRaises(C.ClosureError):
            C.FieldToken("PHYSICAL", T.Token("TOLERANCE_UNRESOLVABLE", "x"))

    def test_source_status(self):
        self.assertEqual(C.G_SOURCE_STATUS, "NOT_CHECKED")
        self.assertIn("VERIFY", C.G_SOURCE)


class SystematicCheck(unittest.TestCase):
    """F reinterpreted as a random-error consistency check: a diagnostic, never a verdict."""
    def _row(self, cid):
        return next(r for r in C.branch_table() if r["case"] == cid)

    def test_c9_cw_plus_systematic_flag(self):
        r = self._row("c9")
        self.assertEqual(r["branches"]["G"], "PHYSICAL:CLOSED_WITHIN")
        self.assertEqual(r["sys"], "D:SYS_ERR")
        self.assertEqual(r["branches"]["F"], "PHYSICAL:FAILED")       # F kept as history

    def test_flag_fields_and_reason(self):
        p = _prereg(accounts=[_decl(tol=1e-5, sigma=1e-7, k=2)])
        o = C.Misclosure(account="N", value=5e-6, provenance="x")
        res = C.run(p, p.sha256, [o])
        f = C.systematic_check(res, o, n_legs=4)
        self.assertEqual((f.field, f.token.state), ("DETERMINATION", "SYSTEMATIC_ERROR_INDICATED"))
        self.assertIn("exceeds random-error expectation for n legs", f.token.reason)
        g_before = C.verdict_branch_G(res, o)
        C.systematic_check(res, o, n_legs=4)
        self.assertEqual(C.verdict_branch_G(res, o), g_before)        # never changes G

    def test_within_random_error_no_flag_and_void_cases(self):
        p = _prereg(accounts=[_decl(tol=1e-5, sigma=1e-7, k=2)])
        o = C.Misclosure(account="N", value=3e-7, provenance="x")
        res = C.run(p, p.sha256, [o])
        self.assertIsNone(C.systematic_check(res, o, n_legs=4))       # 3e-7 <= 4e-7
        self.assertEqual(C.systematic_check(res, o).state, "VOID")    # n_legs missing
        p = _prereg(accounts=[_decl(sigma=None, k=None)])
        o = C.Misclosure(account="N", value=3e-7, provenance="x")
        res = C.run(p, p.sha256, [o])
        self.assertEqual(C.systematic_check(res, o, n_legs=4).state, "VOID")
        with self.assertRaises(C.ClosureError):
            C.DiagnosticFlag("PHYSICAL", T.Token("SYSTEMATIC_ERROR_INDICATED", "x"))

    def test_table_flags(self):
        self.assertEqual([r["case"] for r in C.branch_table() if r["sys"] == "D:SYS_ERR"], ["c9", "c11"])
