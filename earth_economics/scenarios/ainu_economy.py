"""
Ainu reciprocal economy (Hokkaido, Sakhalin, Kurils).
Kamuy (gods/spirits) are economic partners. Gift exchange with the non-human world.
"""

system_profile = {
    "system_name": "Ainu Kamuy-Relational Economy",
    "description": "Reciprocal obligation between humans and kamuy (spirits). Hunting, fishing, and gathering are acts of ritual receiving, not extraction.",
    "data_sources": "ethnographic (Ohnuki-Tierney, Watanabe, Sjöberg); illustrative",
    "confidence_level": "illustrative",

    "SID": 1.0,          # the ecosystem itself is the collective infrastructure
    "VE_VL": 0.0,        # no extraction; you receive from kamuy and give back through ritual
    "MSI": 0.0,          # no money; trade is ceremonial
    "ISR": 100.0,        "ISR_note": "∞ (the land, rivers, and kamuy are infrastructure)",
    "BSC": 0.0,
    "MM": 0.0,

    "UFR": -0.8,         "UFR_note": "negative; surplus flows to ceremony and community, not accumulation",
    "ER": 0.0,           "ER_note": "extraction is ontological error; you do not take, you receive",
    "HHI": 50.0,         # highly egalitarian; kotan (village) decisions are collective
    "DI": 5.0,           # relational; elders and shamans have spiritual authority, not command
    "LWR": 4.0,          # labor, ritual, and ecological knowledge are a single category
    "RI": 0.05,          # community and kamuy relationship absorb all risk

    "OCDI": -1.0,
    "OCDI_note": "maximum negative; the concept of capital is absent; all value is relational",
    "RPI": -5.0,         "RPI_note": "inapplicable; the framework's premise (extraction) does not exist",

    "BEI": 0.005,        "BEI_note": "near zero; coordination is ritual practice, not administration",
    "ICD": 1.0,          "ICD_note": "the distinction between formal and informal collapses entirely",
    "NEI": 1.0,          "NEI_note": "maximum; all value flows from humans to kamuy and community through ceremony",
    "RTF": 1.0,          "RTF_note": "relational trust extends to non-human persons (kamuy, animals, rivers)",
    "SC": 100.0,         "SC_note": "kotan-scale; trust is face-to-face and extends to the non-human"
}
