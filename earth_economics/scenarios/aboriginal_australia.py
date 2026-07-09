"""
Aboriginal Australian kin-based economy (pre-contact ideal-type).
Land is not owned; it is cared for. Songlines encode economic geography.
"""

system_profile = {
    "system_name": "Aboriginal Australian Kin Economy",
    "description": "Land-based relational ontology. Kinship with country determines resource rights and obligations. Songlines as information infrastructure.",
    "data_sources": "ethnographic (Myers, Strehlow, Langton); illustrative",
    "confidence_level": "illustrative",

    "SID": 1.0,          # land itself is collective; no private property
    "VE_VL": 0.0,        # no extraction; you cannot extract from kin
    "MSI": 0.0,          # no money; trade is ceremonial and relational
    "ISR": 100.0,        "ISR_note": "∞ (infrastructure is the land and the Law)",
    "BSC": 0.0,
    "MM": 0.0,

    "UFR": 0.0,          "UFR_note": "flat; wealth is not accumulated, it is circulated in ceremony",
    "ER": 0.0,
    "HHI": 100.0,        # highly distributed; elders have authority but not command
    "DI": 10.0,          # relational authority; achieved through lifetime of learning
    "LWR": 3.0,          # labor (caring for country) is the entire economic category
    "RI": 0.1,           # kin network is the ultimate insurance

    "OCDI": -0.9,
    "OCDI_note": "deeply negative; the concept of 'capital' has no referent",
    "RPI": -5.0,         "RPI_note": "inapplicable in any meaningful sense; extraction is ontological error",

    "BEI": 0.01,         "BEI_note": "near zero; Law is embedded in landscape and ceremony, not documents",
    "ICD": 1.0,          "ICD_note": "everything is informal/relational; the distinction collapses",
    "NEI": 1.0,          "NEI_note": "maximum negative extraction; giving to country IS the economy",
    "RTF": 1.0,          "RTF_note": "kinship with country and each other; no institutional layer",
    "SC": 500.0,         "SC_note": "larger than Dunbar because land mediates relationships across generations"
}
