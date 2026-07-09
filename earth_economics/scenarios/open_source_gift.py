"""
Open-source software gift economy (modern: Linux, Wikipedia, arXiv).
Status from contribution; value flows from contributors to public commons.
"""

system_profile = {
    "system_name": "Open-Source Gift Economy (Modern Digital)",
    "description": "Global-scale gift economy mediated by digital infrastructure. Contribution creates status; code is given, not sold.",
    "data_sources": "OSS contribution data, GitHub, Linux Foundation; illustrative",
    "confidence_level": "estimated",

    "SID": 0.9,          # digital infrastructure is collectively provided (internet, repos)
    "VE_VL": -0.3,       # value extraction negative: corporations extract from commons, but contributors give
    "MSI": 0.3,          # some monetary elements (corporate sponsorship) but core is non-monetary
    "ISR": 10.0,         # internet infrastructure subsidized
    "BSC": 0.0,          # no bailouts; abandoned projects are forked
    "MM": 0.0,

    "UFR": -2.0,         # contributors give value; corporations extract from commons (mixed signal)
    "UFR_note": "net downward flow from contributors to users, but corporate extraction creates upward eddy",
    "ER": 0.05,          "ER_note": "near zero for core contributors; corporate sponsors extract reputation",
    "HHI": 200.0,        # highly distributed; Linux kernel has thousands of contributors
    "DI": 5.0,           # meritocratic; commit access is earned
    "LWR": 5.0,          # labor (coding) directly produces status and value
    "RI": 0.3,           # contributors risk burnout, not financial ruin

    "OCDI": -0.3,
    "OCDI_note": "slightly negative; reputation economy inverts extraction logic",
    "RPI": -1.0,         "RPI_note": "negative: more efficiency means more contribution, not more extraction",

    "BEI": 0.2,          "BEI_note": "low; coordination via git, mailing lists, meritocracy",
    "ICD": 0.8,          "ICD_note": "high informal dependency on reputation and peer review",
    "NEI": 0.5,          "NEI_note": "moderate negative extraction; value flows to commons",
    "RTF": 0.7,          "RTF_note": "relational trust (peer review, reputation) + institutional (licenses, foundations)",
    "SC": 100000.0,      "SC_note": "global scale via digital mediation; Dunbar partly circumvented by tooling"
}
