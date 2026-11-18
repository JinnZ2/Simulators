"""M4 closure gate declarations (COMBINED_SPEC section 2, R-A1 / R-A4; section 8 rows 4-7, 41).

Written before cplay/closure.py. The verdict rule is a spec gap (see test_verdict_is_a_spec_gap).
"""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import closure as C  # noqa: E402
from cplay import tokens as T  # noqa: E402


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
        self.assertEqual(len(rows), 8)
        split = [r["case"] for r in rows if r["split"]]
        self.assertEqual(split, ["c1", "c4", "c6"])
        for r in rows:
            self.assertEqual(sorted(r["branches"]), ["A", "B", "C"])
