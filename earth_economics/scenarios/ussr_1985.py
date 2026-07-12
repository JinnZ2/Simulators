"""
USSR economic system profile (circa 1985, pre-perestroika).
"""

system_profile = {
    "system_name": "USSR State Socialism 1985",
    "description": "Central planning with single-party control, collective infrastructure, and bureaucratic coordination.",
    "data_sources": "historical estimates; illustrative",
    "confidence_level": "illustrative",

    "SID": 0.99,
    "VE_VL": 0.05,   # nomenklatura extraction small but present
    "MSI": 1.0,      # all money state-created
    "ISR": 100.0,    # infrastructure fully state-provided
    "ISR_note": "∞ effectively (no market pricing)",
    "BSC": 100.0,    # all losses absorbed by state
    "MM": 1.0,       # limited fractional reserve

    "UFR": 0.0,      # officially no upward flow; but shadow economy unknown
    "ER": 0.1,
    "HHI": 10000.0,  # single-plan monopoly
    "DI": float("inf"),  # single-party
    "DI_note": "∞ (one-party control)",
    "LWR": 2.0,      # wealth from labor, not ownership
    "RI": 0.2,       # guaranteed employment and basics

    "OCDI": 0.15,
    "OCDI_note": "low extraction, yet system collapsed → non-extraction failure mode",
    "RPI": 0.0,

    "BEI": 0.8,      "BEI_note": "very high: coordination without price signals is expensive",
    "ICD": 0.0,      "ICD_note": "informal networks exist but not measured",
    "NEI": None,     "NEI_note": "no negative extraction",
    "RTF": 0.3,      "RTF_note": "blat (informal relational trust) filled gaps",
    "SC": 300e6,     "SC_note": "scale attempted beyond relational capacity"

}
