# ai-reading-corpus -- landing notes

CC0. What landing this folder and its eight sibling artifacts did to the tree. The
corpus's own findings live in `ledger/` (claims, conflicts X-01..X-21, gaps); these
notes are only about the landing. Ids are permanent.

```text
ARC_001  eight AOS artifacts placed at their target paths, bytes identical to the drop
         category-weld/welds/{optical_switching_speed,deterministic_switching}.json
         constraint-assembly/cases/{aos-vector-beam,granular-reptation,ife-amplifier-scaling}.json
         presented-binary/cases/aos-thickness-ceiling.json
         uninstrumented/cases/025aoswritelatency.md
         scope-bound-shapes/aos_topology_scope.py
         aos-vector-beam is the v2 delivery; v1 is kept only in
         sources/aos/simulators-drop/constraint-assembly/cases/superseded/
         check: MANIFEST simulators_target + aos_sim_instruments, aos_case_number

ARC_002  the write-latency case arrived as 024; 024 is held on main by
         024refusalfalsepositiverate.md. Landed as 025 by FILENAME only. Its header
         ('# Case 024') and aos-vector-beam open[1] ('see uninstrumented case 024') are
         delivered text and still read 024. Conflict X-20.
         uninstrumented.py builds its registry from README.md, not from cases/, so the
         case is landed and not registered; the case also uses '## QUANTITY' sections
         where 022-024 use a 'Name:' prose form.

ARC_003  three folder audits now print different readings. All still exit 0.
         constraint-assembly/assembly_audit.py
           'two cases'                     True  -> False
           components across the cases     7     -> 25  (24 used, 1 unused)
           soft class                      0 instances -> present in 3 cases
             (line 401's prose 'soft is 0 across both cases' now reads against the data)
         category-weld/weld_audit.py       3 term files -> 5
         presented-binary/presented_binary_audit.py
           one more case row (aos-thickness-ceiling, documented 5/11, share 0.455)
         Recorded, not repaired: those audits are records of the drop they audited.

ARC_004  the two new welds put the low and high ends of an estimate range in before/after,
         where category-weld/README.md defines before/after as a movement observed in the
         field. weld.py then reports spread 10.00 (optical switching speed) and 2.00
         (deterministic switching); those numbers are range widths. Conflict X-15.

ARC_005  aos_topology_scope.py runs against scope-bound-shapes/scope.py: COMPARE
         UNDECLARED_OVERLAP, corroborate None, infer_frozen REFUSED_BY_CONSTRAINT. The
         session transcript (sources/aos/T1) reports this as 'corroborating'. Conflict X-16.

ARC_006  root suite before and after the landing: same 3 failures, none new
         test_compile_gate ... binds_a_toplevel_name_twice
         test_run_manifest ... redirect_names_a_target_that_is_missing
         test_run_manifest ... the_one_known_violation_is_pinned
```

What is not claimed here: nothing in this folder re-fetched a source. Every claim about
the world in H1, R4, R5, T0, T1 is NOT_CHECKED (gap G-B3).
