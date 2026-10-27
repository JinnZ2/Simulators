"""Regenerate examples/example_site.yaml (an invented plant).

    python3 examples/make_example.py

Seeded, so the file is the same every time. Every person, machine and number
in it is EXAMPLE: invented to exercise every module, not a real site.
Patterns planted on purpose, so the report has something to find:
  - lathe-2's catchable scrap share rises after veteran "Dale R." leaves
  - titled mechanics write up repairs that untitled operators did
  - mes depends on the PHP portal (a hidden chain for press-1)
  - one vendor's license checks cover more than 30% of output
"""
import datetime as dt
import random
from pathlib import Path

import yaml

R = random.Random(20261023)
OUT = Path(__file__).with_name("example_site.yaml")

operators = [
    dict(id="op01", name="Dale R.", tenure_months=310, role="lathe operator", titled=False,
         machines=["lathe-2"], left_date=dt.date(2025, 3, 1), sole_knower_of=["lathe-2 setup"]),
    dict(id="op02", name="Marta K.", tenure_months=280, role="mill operator", titled=False,
         retiring_within_months=14, machines=["mill-1"], sole_knower_of=["mill-1 spindle by ear", "coolant mix"],
         can_run_manual=["mill-1", "lathe-1"]),
    dict(id="op03", name="Gene P.", tenure_months=240, role="press operator", titled=False,
         retiring_within_months=30, machines=["press-1"], sole_knower_of=["press-1 die change"],
         can_run_manual=["press-1"]),
    dict(id="op04", name="Ruth A.", tenure_months=150, role="lathe operator", titled=False,
         machines=["lathe-1"], can_run_manual=["lathe-1"], sole_knower_of=[]),
    dict(id="op05", name="Tom B.", tenure_months=90, role="maintenance mechanic", titled=True,
         machines=[], sole_knower_of=[]),
    dict(id="op06", name="Lena S.", tenure_months=70, role="maintenance mechanic", titled=True,
         machines=[], sole_knower_of=["license server reset"]),
    dict(id="op07", name="Sam W.", tenure_months=40, role="operator", titled=False, machines=["saw-1"], can_run_manual=["saw-1"],
         sole_knower_of=[]),
    dict(id="op08", name="Jo H.", tenure_months=30, role="operator", titled=False, machines=["lathe-2"],
         sole_knower_of=[]),
    dict(id="op09", name="Ana V.", tenure_months=20, role="operator", titled=False, machines=["lathe-2"],
         sole_knower_of=[]),
    dict(id="op10", name="Luis F.", tenure_months=9, role="operator", titled=False, machines=["mill-1"]),
    dict(id="op11", name="Kim D.", tenure_months=7, role="operator", titled=False, machines=["press-1"]),
    dict(id="op12", name="Pat N.", tenure_months=5, role="operator", titled=False, machines=["saw-1"]),
    dict(id="op13", name="Cory L.", tenure_months=3, role="operator", titled=False, machines=["lathe-1"]),
    dict(id="op14", name="Ivy Q.", tenure_months=2, role="operator", titled=False, machines=["cnc-1"]),
]

machines = [
    dict(id="lathe-1", controller="manual", software_layers=[], vendor="Lathe Works (EXAMPLE)",
         license_check=False, manual_mode="full", power_draw_kw=11, priority=2, output_share=0.15,
         repair_knowledge="inhouse", expected_service_life_years=30, replacements_per_year=0.02,
         power=dict(none=dict(runs=False, manual_alternative=False, last_tested="never"),
                    intermittent=dict(runs=True, rehome_after_dropout=False, last_tested="2024-06-11"))),
    dict(id="lathe-2", controller="CNC retrofit", software_layers=["hmi_win"], vendor="Lathe Works (EXAMPLE)",
         license_check=False, manual_mode="partial", power_draw_kw=15, priority=3, output_share=0.15,
         repair_knowledge="inhouse", expected_service_life_years=25, replacements_per_year=0.06),
    dict(id="mill-1", controller="CNC", software_layers=["hmi_win", "license_server"], vendor="Vendor X (EXAMPLE)",
         license_check=True, manual_mode="none", power_draw_kw=22, priority=1, output_share=0.25,
         repair_knowledge="vendor", expected_service_life_years=15, replacements_per_year=0.12,
         power=dict(intermittent=dict(runs=False, rehome_after_dropout=True, last_tested="never"))),
    dict(id="cnc-1", controller="CNC", software_layers=["license_server", "vendor_remote"], vendor="Vendor X (EXAMPLE)",
         license_check=True, manual_mode="none", power_draw_kw=30, priority=4, output_share=0.20,
         repair_knowledge="vendor", expected_service_life_years=12, replacements_per_year=0.15),
    dict(id="press-1", controller="PLC", software_layers=["mes"], vendor="Press Co (EXAMPLE)",
         license_check=False, manual_mode="partial", power_draw_kw=18, priority=2, output_share=0.15,
         repair_knowledge="inhouse", expected_service_life_years=40, replacements_per_year=0.03),
    dict(id="saw-1", controller="manual", software_layers=[], vendor="Saw Co (EXAMPLE)",
         license_check=False, manual_mode="full", power_draw_kw=5, priority=5, output_share=None,
         repair_knowledge="unknown"),
]

software_layers = [
    dict(id="php_portal", kind="php_portal", version="8.1.31", depends_on=[]),
    dict(id="mes", kind="mes_scheduler", depends_on=["php_portal"]),
    dict(id="hmi_win", kind="hmi_java_windows", depends_on=[]),
    dict(id="cloud_link", kind="cloud_link", depends_on=[]),
    dict(id="license_server", kind="license_server", depends_on=["cloud_link"]),
    dict(id="vendor_remote", kind="vendor_remote_support", depends_on=["cloud_link"]),
]

functions = [
    dict(id="job_tickets", layers=["php_portal"], bridge="paper job tickets"),
    dict(id="scheduling", layers=["mes"]),
    dict(id="turning", machines=["lathe-1", "lathe-2"]),
    dict(id="milling", machines=["mill-1", "cnc-1"]),
    dict(id="pressing", machines=["press-1"]),
    dict(id="inspection_log", layers=["mes"], bridge="paper check sheet"),
]

# scrap: 2024-01 .. 2025-12, a few rows per machine-month
scrap = []
codes_ok = ["calibration_drift", "belt_drive_failure", "material_jam"]
for month in range(24):
    y, m = 2024 + month // 12, month % 12 + 1
    for mach in ("lathe-1", "lathe-2", "mill-1", "press-1", "cnc-1"):
        catch_p = 0.55
        if mach == "lathe-2" and (y, m) >= (2025, 3):
            catch_p = 0.82          # Dale R. left 2025-03-01
        for _ in range(3):
            code = R.choice(codes_ok) if R.random() < catch_p else R.choice(["sudden_fracture", "power_event"])
            if R.random() < 0.03:
                code = "operator_error"   # not in the map: shows as unmapped
            scrap.append(dict(date=dt.date(y, m, R.randint(1, 28)), machine=mach,
                              logged_cause_code=code, units=R.randint(5, 40),
                              shift=R.choice(["day", "night"])))

repairs = []
fixers = ["Marta K.", "Gene P.", "Ruth A.", "Tom B.", "Lena S."]
for i in range(24):
    fixer = R.choice(fixers)
    writer = R.choice(["Tom B.", "Lena S."]) if fixer not in ("Tom B.", "Lena S.") and R.random() < 0.8 else fixer
    rec = dict(date=dt.date(2025, R.randint(1, 12), R.randint(1, 28)),
               machine=R.choice(["lathe-1", "lathe-2", "mill-1", "press-1"]),
               who_diagnosed=fixer, who_fixed=fixer, who_wrote_up=writer)
    if R.random() < 0.7:
        rec["detection_lead_hours"] = round(R.uniform(2, 60) if fixer not in ("Tom B.", "Lena S.") else R.uniform(0, 12), 1)
        rec["first_fix"] = R.random() < (0.8 if fixer not in ("Tom B.", "Lena S.") else 0.6)
        rec["called_after_titled_failed"] = fixer not in ("Tom B.", "Lena S.") and R.random() < 0.4
    if R.random() < 0.25:
        rec["voice_memo"] = f"memos/repair-{i:02d}.m4a"
    repairs.append(rec)

site = dict(
    name="EXAMPLE: Ridgeview Machining (invented plant)",
    example=True,
    workforce=dict(operators=operators),
    hiring=dict(screen_type="written", job_channel="hands_on", first_year_quit_rate=0.38),
    maintenance=[dict(year=y, repairs_inhouse=a, repairs_outsourced=b)
                 for y, a, b in [(2021, 140, 22), (2022, 128, 35), (2023, 110, 51),
                                 (2024, 96, 63), (2025, 81, 77)]],
    repair_attribution=repairs,
    scrap=scrap,
    machines=machines,
    software_layers=software_layers,
    functions=functions,
    oversight=[dict(year=y, inspectors=i, supervisors=s, direct_operators=o)
               for y, i, s, o in [(2021, 2, 3, 16), (2022, 2, 3, 16), (2023, 3, 3, 15),
                                  (2024, 4, 3, 14), (2025, 5, 4, 14)]],
    safety=dict(rules=[dict(id=f"R{i}", origin=o) for i, o in enumerate(
        ["incident_driven"] * 6 + ["worker_reported"] * 2 + ["regulation"] * 3, 1)]),
    automation=dict(projects=[dict(id="cnc-1 cell", experienced_operators_involved=False),
                              dict(id="press-1 feeder", experienced_operators_involved=True),
                              dict(id="vision inspect", experienced_operators_involved=False)]),
    power_budget=dict(minimal_kw=60),
    reserve_line=dict(size=3, wage_cost_per_operator_year=68000, reserve_output_value_per_year=150000,
                      outage_days=10, daily_output_value=45000, outage_probability_per_year=0.15),
    drivers=[dict(id="truck-1", start_year=2009, has_kept_paper_logs_in_cab=True, completed_week_long_paper_drill=False),
             dict(id="truck-2", start_year=2015, has_kept_paper_logs_in_cab=True),
             dict(id="truck-3", start_year=2019, has_kept_paper_logs_in_cab=False, completed_week_long_paper_drill=False),
             dict(id="truck-4", start_year=2021, has_kept_paper_logs_in_cab=False, completed_week_long_paper_drill=True),
             dict(id="truck-5", start_year=2023)],
)

HEADER = """\
# EXAMPLE SITE: invented plant. No person, machine or number here is real.
# Regenerate with: python3 examples/make_example.py
# Every field is optional; delete any section and the assessment still runs,
# with lower confidence and the gap listed in the report.
"""
OUT.write_text(HEADER + yaml.safe_dump(site, sort_keys=False, allow_unicode=True), encoding="utf-8")
print(f"wrote {OUT}")
