"""
Sámi reindeer-herding economy (Northern Scandinavia/Russia).
Cyclical, kin-based, land-embedded. Siida as collective management unit.
"""

system_profile = {
    "system_name": "Sámi Siida Economy",
    "description": "Kin-based collective management of reindeer herds and seasonal territories. Mobility and reciprocity are core infrastructure.",
    "data_sources": "ethnographic (Paine, Ingold, Beach); illustrative",
    "confidence_level": "illustrative",

    "SID": 0.85,         # siida is collective; herding territories shared
    "VE_VL": 0.0,        # no extraction; herd ownership is relational and seasonal
    "MSI": 0.0,          # traditional; money enters only at the colonial interface
    "ISR": 100.0,        "ISR_note": "∞ (migration routes, knowledge, and reciprocity are infrastructure)",
    "BSC": 0.0,
    "MM": 0.0,

    "UFR": -0.5,         "UFR_note": "slightly negative; surplus animals shared within siida",
    "ER": 0.0,
    "HHI": 200.0,        # distributed; siida decisions are consensus-based
    "DI": 20.0,          # relational authority; elders and active herders hold weight
    "LWR": 2.5,          # labor and knowledge of the land produce all value
    "RI": 0.3,           # kin network absorbs; but colonial pressure introduces new risks

    "OCDI": -0.7,
    "OCDI_note": "negative; herding is maintenance of relationship, not extraction",
    "RPI": -4.0,         "RPI_note": "deeply negative; extraction logic is colonial, not indigenous",

    "BEI": 0.05,         "BEI_note": "low; coordination is seasonal and embodied in practice",
    "ICD": 0.9,          "ICD_note": "high informal dependency; siida is the collective unit",
    "NEI": 0.7,          "NEI_note": "high; giving to the herd and to kin is the economic logic",
    "RTF": 0.95,         "RTF_note": "nearly pure relational trust; siida decisions are face-to-face",
    "SC": 200.0,         "SC_note": "siida-scale; larger assemblies exist but core unit is kin-based"
}
