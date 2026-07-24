#!/usr/bin/env python3
"""
thermo_pipeline_demo.py -- end-to-end walk through the four-module stack.
CC0 / Public Domain.  stdlib-only.

Story: rural forested site with clay soil rated adequate. Goal: a footing.
Two paths exist under the code overlay:
    physics   lay_stone_pad on the adequate soil (all site, 0 external)
    code      approve -> import fill -> pour  (mandated by 1974 requirement
                                                with no basis on file)

The demo runs the pipeline top-to-bottom and shows one specific thing:
CLOSING AN ASSUMPTION GAP (adding an air-quality state) turned a silent
zero-cost approval into a metered ventilation debt. The tool never
invented that cost; it made the air debt visible so the referee could
weigh it.

Stages:
  1. Assumption audit on the naive site           -> 5 gaps flagged
  2. Naive interrogation                          -> reports what's there
  3. Close the air-related gaps with the library  -> 4 gaps cleared
  4. Walk the code path manually via propose()    -> hits the air gate,
                                                     FAILS on presence
  5. Add ventilation between import and pour      -> code path completes
                                                     but at metered cost
  6. Physics path unchanged, still 0 external
  7. Print the delta the audit-and-close cycle SURFACED (not invented)
"""

import copy
from thermo_pm import Resource
from thermo_explore import Playground
from thermo_interrogate import build_site, CodeRequirement, interrogate, print_report
from thermo_assume import (audit_assumptions, print_audit,
                           air_quality_kit, emit_into_air, gate_labor_on_air,
                           solar_pv, human_power)


def _hr(title): print("\n" + "=" * 66 + f"\n {title}\n" + "=" * 66)


def _amounts(sys, keys):
    return {k: round(sys.resources[k].amount, 2)
            for k in keys if k in sys.resources}


def _replay(site, plan):
    s = copy.deepcopy(site)
    for pname in plan:
        s.run_process(s.processes[pname])
    return s


def main():
    site = build_site()
    goal = {"footing": 1}
    code = [CodeRequirement(
        id="footing_min_500mm",
        enacted_year=1974,
        required_by=["pour_footing_code"],
        basis=None,
        intent_met_by="soil_bearing:adequate",
    )]

    # =================================================================
    _hr("STAGE 1  assumption audit on the naive site")
    # =================================================================
    flags_before = audit_assumptions(site)
    print(f"\n  {len(flags_before)} gaps flagged (dimensions with zero coverage):")
    for f in flags_before:
        print(f"    - {f.dimension}: {f.detail}")
    print("\n  the tool INVENTS nothing here. it names which dimensions the")
    print("  operator has not populated. filling them is the operator's job.")

    # =================================================================
    _hr("STAGE 2  naive interrogation")
    # =================================================================
    print("\n  full report against the naive site (delta = 0 -- the code")
    print("  overlay is PERMISSIVE, not FORCING; BFS routes around it):")
    print_report(interrogate(site, goal, code))

    # =================================================================
    _hr("STAGE 3  close air-related gaps with the library")
    # =================================================================
    # add air state, ventilation, external grid_power to run it
    air, ventilation, thr = air_quality_kit(threshold=50)
    site.add_resource(air)
    site.add_resource(Resource("grid_power", "energy", 30_000, "J", "external"))
    site.register_process(ventilation(energy_cost=2000, restored=20))
    # couple diesel-import to the air it fouls, tuned so ONE import drops
    # air below the labor gate (60-point hit on a 100-clean baseline).
    # particulate_kg=0: exhaust mass is negligible next to fuel mass and the
    # tool doesn't need to bookkeep it as a matter output; the air debt lives
    # in side_effect. Setting a nonzero particulate_kg with no compensating
    # matter input would violate TPM-2 (matter conservation).
    emit_into_air(site.processes["import_fill"], particulate_kg=0, air_hit=60)
    gate_labor_on_air(site.processes["pour_footing_code"], min_air=50)
    # also add a second energy source so the energy-diversity flag clears
    site.add_resource(solar_pv("solar", 80_000))
    site.add_resource(human_power("crew_power", 40_000))

    flags_after = audit_assumptions(site)
    cleared = {f.dimension for f in flags_before} - {f.dimension for f in flags_after}
    print(f"\n  {len(cleared)} gaps cleared: {sorted(cleared)}")
    print(f"  {len(flags_after)} still open: {[f.dimension for f in flags_after]}")

    # =================================================================
    _hr("STAGE 4  walk the code path manually  (institutional fact:")
    print("           lay_stone_pad is not an APPROVED method under the")
    print("           code, so an operator forced down the code path")
    print("           must run these three steps, in order)")
    # =================================================================
    # add the mode marker so approve_footing_code's gate is satisfied
    site.add_resource(Resource("mode:code_compliant", "information", 1))
    pg = Playground(site, goal)
    code_path = ["approve_footing_code", "import_fill", "pour_footing_code"]
    v = pg.propose(code_path)
    print(f"\n  propose({' -> '.join(code_path)})")
    print(f"    verdict : {'ok' if v.ok else 'FAILED'} "
          f"@step {v.step} law={v.law!r}")
    print(f"    process : {v.process}")
    print(f"    detail  : {v.detail}")
    if not v.ok and v.law == "presence":
        print("\n  the air-quality gate on pour_footing_code fired. import_fill")
        print("  dropped air 100 -> 40 (60-point exhaust hit); pour needs 50.")
        print("  BEFORE closing the air gap this failure was INVISIBLE.")

    # =================================================================
    _hr("STAGE 5  add ventilation between import and pour")
    # =================================================================
    code_path_vented = ["approve_footing_code", "import_fill",
                        "ventilation", "pour_footing_code"]
    v = pg.propose(code_path_vented)
    print(f"\n  propose({' -> '.join(code_path_vented)})")
    print(f"    verdict: {'ok' if v.ok else 'FAILED'}  "
          f"goal_reached={v.reached_goal}")
    ended = _replay(site, code_path_vented)
    print(f"    air_quality: 100 -> "
          f"{ended.resources['air_quality'].amount:.0f}  (dropped 60, restored 20)")
    print(f"    waste_heat : {ended.resources['waste_heat'].amount:.0f} J  (computed residual)")

    # =================================================================
    _hr("STAGE 6  physics path unchanged")
    # =================================================================
    phys_path = ["lay_stone_pad"]
    v = pg.propose(phys_path)
    print(f"\n  propose({' -> '.join(phys_path)})")
    print(f"    verdict: {'ok' if v.ok else 'FAILED'}  "
          f"goal_reached={v.reached_goal}")
    phys_ended = _replay(site, phys_path)
    print(f"    air_quality: 100 -> {phys_ended.resources['air_quality'].amount:.0f}"
          f"  (no combustion, no debt)")
    print(f"    waste_heat : {phys_ended.resources['waste_heat'].amount:.0f} J")

    # =================================================================
    _hr("STAGE 7  the delta the audit-and-close cycle SURFACED")
    # =================================================================
    def ext(after):
        e = m = 0.0
        for name, r0 in site.resources.items():
            if r0.location != "external":
                continue
            drawn = r0.amount - after.resources.get(name, r0).amount
            if drawn > 1e-9 and r0.type in ("energy", "matter"):
                if r0.type == "energy": e += drawn
                else:                   m += drawn
        return e, m

    e_code, m_code = ext(ended)
    e_phys, m_phys = ext(phys_ended)
    print(f"\n  physics path external draw : {e_phys:>8.0f} J   {m_phys:>6.0f} kg")
    print(f"  code    path external draw : {e_code:>8.0f} J   {m_code:>6.0f} kg")
    print(f"  DELTA (code - physics)     : {e_code-e_phys:>+8.0f} J   "
          f"{m_code-m_phys:>+6.0f} kg")
    print("\n  of that delta, 20000 J diesel + 1200 kg offsite live in")
    print("  import_fill and were always in the code path's definition --")
    print("  Stage 2 hid them by taking the shorter physics route. The 2000 J")
    print("  ventilation cost is DIFFERENT: it did not exist as a step at all")
    print("  before Stage 3 added the air state. Modeling the air turned a")
    print("  free approval into a metered restoration. Same physics; more of")
    print("  it visible.")
    print("\n" + "=" * 66)


if __name__ == "__main__":
    main()
