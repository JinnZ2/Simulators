# worked_example.py -- the Section 5 example, delivered VERBATIM.
# Only the import line is added so the delivered `cases`/`report`
# block runs as its own file; nothing else is changed.
from effective_redundancy import Case, Channel, report

cases = [
    Case("Kerr County 2025", "county_em", "failed", {"C"}, [
        Channel("WEA_all_phones", False),
        Channel("CodeRED",        False),
        Channel("weather_radio",  False),   # escapes C, dies on reception
    ]),
    Case("Kerr County 2026", "county_em", "held", set(), [
        Channel("WEA_all_phones", True),
        Channel("CodeRED",        True),
    ]),
    # ... your 8-15 cases here, coded blind, two coders
]
report(cases)
