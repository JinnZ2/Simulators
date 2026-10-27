"""domains.py — the eight biological boundaries as declared graphs.

Each domain is a Graph whose source is NEED and target is SATISFIED,
with channels carrying their KINDS and their token requirement.

These are constructed, not measured. Every channel in every domain is
this file's authored reading, tagged with its author and date. Nothing
here is a claim about the world; each domain is a graph whose topology
can be computed, and the topology is the finding.
"""

from graph import Graph, Channel, TOKEN_NODE

AUTHOR = "gate/domains.py"
DATE = "2026-09-28"

def _ch(src, dst, kinds, token=False, label=""):
    return Channel(src=src, dst=dst, kinds=frozenset(kinds),
                   requires_token=token, label=label)

def water():
    g = Graph("water", "NEED", "SATISFIED")
    # public fountain (thin today, historical)
    g.add_channel(_ch("NEED", "FOUNTAIN", ["physical", "practical"],
                      label="public fountain (physical, thin)"))
    g.add_channel(_ch("FOUNTAIN", "SATISFIED", ["physical", "practical"],
                      label="drink at fountain"))
    # private tap, requires account
    g.add_channel(_ch("NEED", "PRIVATE_TAP", ["physical", "legal", "practical"],
                      token=True, label="private tap (account)"))
    g.add_channel(_ch("PRIVATE_TAP", "SATISFIED", ["physical", "legal", "practical"],
                      label="drink at tap"))
    # bottled purchase
    g.add_channel(_ch("NEED", "BOTTLED", ["physical", "legal", "practical"],
                      token=True, label="bottled purchase"))
    g.add_channel(_ch("BOTTLED", "SATISFIED", ["physical", "legal", "practical"],
                      label="drink from bottle"))
    # rain / surface, physical only
    g.add_channel(_ch("NEED", "RAIN", ["physical"],
                      label="rain / surface (physical)"))
    g.add_channel(_ch("RAIN", "SATISFIED", ["physical"],
                      label="drink from source"))
    return g

def food():
    g = Graph("food", "NEED", "SATISFIED")
    # purchase
    g.add_channel(_ch("NEED", "GROCERY", ["physical", "legal", "practical"],
                      token=True, label="grocery purchase"))
    g.add_channel(_ch("GROCERY", "SATISFIED", ["physical", "legal", "practical"],
                      label="eat purchased food"))
    # food bank / SNAP (means-tested, legal, thin)
    g.add_channel(_ch("NEED", "FOODBANK", ["physical", "legal"],
                      label="food bank (means-tested)"))
    g.add_channel(_ch("FOODBANK", "SATISFIED", ["physical", "legal"],
                      label="eat distributed food"))
    # forage / glean — historically legal, now mostly not
    g.add_channel(_ch("NEED", "FORAGE", ["physical"],
                      label="forage (physical)"))
    g.add_channel(_ch("FORAGE", "SATISFIED", ["physical"],
                      label="eat foraged"))
    # garden
    g.add_channel(_ch("NEED", "GARDEN", ["physical", "legal"],
                      label="garden (needs land)"))
    g.add_channel(_ch("GARDEN", "SATISFIED", ["physical", "legal"],
                      label="eat grown"))
    return g

def shelter():
    g = Graph("shelter", "NEED", "SATISFIED")
    g.add_channel(_ch("NEED", "OWNED", ["physical", "legal", "practical"],
                      token=True, label="owned home"))
    g.add_channel(_ch("OWNED", "SATISFIED", ["physical", "legal", "practical"],
                      label="sleep in owned"))
    g.add_channel(_ch("NEED", "RENTED", ["physical", "legal", "practical"],
                      token=True, label="rented"))
    g.add_channel(_ch("RENTED", "SATISFIED", ["physical", "legal", "practical"],
                      label="sleep in rented"))
    # shelter system (thin, means-tested)
    g.add_channel(_ch("NEED", "SHELTER_SYS", ["physical", "legal"],
                      label="shelter system (capacity-limited)"))
    g.add_channel(_ch("SHELTER_SYS", "SATISFIED", ["physical", "legal"],
                      label="sleep in shelter"))
    # rough sleeping (physical only, prohibited in most jurisdictions)
    g.add_channel(_ch("NEED", "ROUGH", ["physical"],
                      label="rough sleeping (physical)"))
    g.add_channel(_ch("ROUGH", "SATISFIED", ["physical"],
                      label="sleep rough"))
    # squatting / homesteading (physical, historically legal)
    g.add_channel(_ch("NEED", "SQUAT", ["physical"],
                      label="squat (physical, historically legal)"))
    g.add_channel(_ch("SQUAT", "SATISFIED", ["physical"],
                      label="sleep in squat"))
    return g

def defecation():
    g = Graph("defecation", "NEED", "SATISFIED")
    g.add_channel(_ch("NEED", "OWN_BATH", ["physical", "legal", "practical"],
                      token=True, label="own bathroom (needs home)"))
    g.add_channel(_ch("OWN_BATH", "SATISFIED", ["physical", "legal", "practical"],
                      label="defecate at home"))
    g.add_channel(_ch("NEED", "BUSINESS", ["physical", "legal", "practical"],
                      token=True, label="business (customer only)"))
    g.add_channel(_ch("BUSINESS", "SATISFIED", ["physical", "legal", "practical"],
                      label="defecate at business"))
    g.add_channel(_ch("NEED", "PUBLIC_RR", ["physical", "legal"],
                      label="public restroom (thin)"))
    g.add_channel(_ch("PUBLIC_RR", "SATISFIED", ["physical", "legal"],
                      label="defecate in public RR"))
    # outdoor (physical only, prohibited)
    g.add_channel(_ch("NEED", "OUTDOOR", ["physical"],
                      label="outdoor (physical, prohibited)"))
    g.add_channel(_ch("OUTDOOR", "SATISFIED", ["physical"],
                      label="defecate outdoors"))
    return g

def thermal():
    g = Graph("thermal", "NEED", "SATISFIED")
    # pre-positioned (built during mild season)
    g.add_channel(_ch("NEED", "STRUCTURE", ["physical", "legal", "practical"],
                      label="pre-built structure (needs land)"))
    g.add_channel(_ch("STRUCTURE", "SATISFIED", ["physical", "legal", "practical"],
                      label="sheltered from heat/cold"))
    # public facility (library, cooling center)
    g.add_channel(_ch("NEED", "PUBLIC_FAC", ["physical", "legal", "practical"],
                      label="public cooling/heating center (thin)"))
    g.add_channel(_ch("PUBLIC_FAC", "SATISFIED", ["physical", "legal", "practical"],
                      label="sheltered at public facility"))
    # body-level in-situ (free within a narrow band)
    g.add_channel(_ch("NEED", "INSITU", ["physical"],
                      label="in-situ: air movement / wet cloth (narrow band)"))
    g.add_channel(_ch("INSITU", "SATISFIED", ["physical"],
                      label="physiological compensation"))
    return g

def sleep():
    g = Graph("sleep", "NEED", "SATISFIED")
    g.add_channel(_ch("NEED", "HOME", ["physical", "legal", "practical"],
                      token=True, label="home"))
    g.add_channel(_ch("HOME", "SATISFIED", ["physical", "legal", "practical"],
                      label="sleep at home"))
    g.add_channel(_ch("NEED", "SHELTER_SYS", ["physical", "legal"],
                      label="shelter system"))
    g.add_channel(_ch("SHELTER_SYS", "SATISFIED", ["physical", "legal"],
                      label="sleep in shelter"))
    g.add_channel(_ch("NEED", "ROUGH", ["physical"],
                      label="sleep rough (physical, prohibited)"))
    g.add_channel(_ch("ROUGH", "SATISFIED", ["physical"],
                      label="sleep rough"))
    return g

def medical():
    g = Graph("medical", "NEED", "SATISFIED")
    g.add_channel(_ch("NEED", "INSURED", ["physical", "legal", "practical"],
                      token=True, label="insured care"))
    g.add_channel(_ch("INSURED", "SATISFIED", ["physical", "legal", "practical"],
                      label="treated (insured)"))
    g.add_channel(_ch("NEED", "EMERGENCY", ["physical", "legal", "practical"],
                      label="emergency (EMTALA, only emergency)"))
    g.add_channel(_ch("EMERGENCY", "SATISFIED", ["physical", "legal", "practical"],
                      label="stabilized"))
    g.add_channel(_ch("NEED", "CHARITY", ["physical", "legal"],
                      label="charity / community clinic (thin)"))
    g.add_channel(_ch("CHARITY", "SATISFIED", ["physical", "legal"],
                      label="treated (charity)"))
    g.add_channel(_ch("NEED", "SELF", ["physical"],
                      label="self-care (physical)"))
    g.add_channel(_ch("SELF", "SATISFIED", ["physical"],
                      label="recovered"))
    return g

def identity():
    g = Graph("identity", "NEED", "SATISFIED")
    g.add_channel(_ch("NEED", "DOC", ["physical", "legal", "practical"],
                      token=True, label="identity document (needs address)"))
    g.add_channel(_ch("DOC", "SATISFIED", ["physical", "legal", "practical"],
                      label="recognized identity"))
    g.add_channel(_ch("NEED", "CASH_INFORMAL", ["physical"],
                      label="cash / informal (physical, narrow)"))
    g.add_channel(_ch("CASH_INFORMAL", "SATISFIED", ["physical"],
                      label="transacted informally"))
    return g

DOMAINS = {
    "water": water,
    "food": food,
    "shelter": shelter,
    "defecation": defecation,
    "thermal": thermal,
    "sleep": sleep,
    "medical": medical,
    "identity": identity,
}
