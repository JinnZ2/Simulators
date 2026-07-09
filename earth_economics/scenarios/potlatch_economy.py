"""
Pacific Northwest Potlatch (ideal-type: Kwakwaka'wakw, Tlingit, Haida).
Status derived from giving, not accumulating. Wealth flows outward.
"""

system_profile = {
    "system_name": "Potlatch Gift Economy (PNW Indigenous)",
    "description": "Reciprocal redistribution through ceremonial giving. Status is a function of what you give away, not what you hold.",
    "data_sources": "ethnographic (Boas, Codere, Jonaitis); illustrative",
    "confidence_level": "illustrative",

    "SID": 0.9,         # collective infrastructure (longhouse, feast, oral tradition)
    "VE_VL": -0.5,       # extraction negative: value flows from holders to community
    "MSI": 0.0,          # no money in traditional form; wealth is in blankets, copper, names
    "ISR": 100.0,        # all infrastructure collectively provided
    "ISR_note": "∞ (no market pricing; prestige economy)",
    "BSC": 0.0,          # no bailouts; community absorbs individual failure
    "MM": 0.0,           # no fractional reserve

    "UFR": -5.0,         # wealth flows DOWNWARD from high-status to low-status
    "UFR_note": "negative: giving creates status; accumulation destroys it",
    "ER": 0.0,           # extraction rate near zero; labor value retained or given
    "HHI": 500.0,        # distributed authority; big men earn, don't take
    "DI": 50.0,          # achieved status, not inherited; competitive generosity
    "LWR": 1.0,          # labor and giving are the same category
    "RI": 0.5,           # community absorbs individual risk

    "OCDI": -0.8,
    "OCDI_note": "negative: capital dependent on giving it away; accumulation is pathology",
    "RPI": -2.0,         "RPI_note": "deeply negative; more efficiency = more giving",

    "BEI": 0.05,         "BEI_note": "ritual coordination, not bureaucratic",
    "ICD": 0.95,         "ICD_note": "nearly all infrastructure is informal/communal",
    "NEI": 0.8,          "NEI_note": "high negative extraction: value flows out of holders into community",
    "RTF": 1.0,          "RTF_note": "purely relational enforcement; reputation is everything",
    "SC": 300.0,         "SC_note": "village-scale; potlatch network extends but trust is face-to-face"
}
