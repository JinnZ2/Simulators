"""
Arabic trust-based trade profile (ideal-type: pre-modern Suq, hawala, mudarabah).
"""

system_profile = {
    "system_name": "Arabic Trust-Based Trade (Ideal-Type)",
    "description": "Relational enforcement, profit-sharing, community infrastructure via waqf, limited scale.",
    "data_sources": "historical/ethnographic; illustrative",
    "confidence_level": "illustrative",

    "SID": 0.2,      # formal state infrastructure minimal
    "VE_VL": 0.05,   # mudarabah profit-sharing limits extraction
    "MSI": 0.3,      # commodity money, not fiat
    "ISR": 2.0,      # waqf (endowment) provides some public goods
    "ISR_note": "collective via religious endowment",
    "BSC": 0.0,      # no bailouts; reputation-based loss absorption
    "MM": 1.0,       # full-reserve or commodity

    "UFR": 0.5,      # wealth flows weakly upward; charity redistributes
    "ER": 0.1,
    "HHI": 1200.0,   # competitive within suq
    "DI": 100.0,     # merchant council influence
    "DI_note": "moderate; reputation-based authority",
    "LWR": 3.0,      # labor/trade dominates over passive ownership
    "RI": 1.0,       # risk shared in mudarabah

    "OCDI": 0.2,     "OCDI_note": "low extraction, no lock-in",
    "RPI": -0.5,     "RPI_note": "extraction counter-cyclical; declines under stress",

    "BEI": 0.1,      "BEI_note": "low bureaucratic overhead",
    "ICD": 0.7,      "ICD_note": "high informal collective dependency (community reputation)",
    "NEI": None,     "NEI_note": "no negative extraction, but charity operates as gift stream",
    "RTF": 0.9,      "RTF_note": "almost purely relational enforcement",
    "SC": 5000.0,    "SC_note": "Dunbar-limited; trust decays beyond community scale"

}
