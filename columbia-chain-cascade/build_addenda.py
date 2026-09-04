#!/usr/bin/env python3
# build_addenda.py -- CC0, stdlib only, parses under 3.9
#
# Writes gap_addenda.json: what the completeness census found missing,
# supplied per gap as DATA beside the delivered entries -- never edited
# into them. Every tier is CARRIED (assigned from general knowledge of
# the institutions, not probed from here, egress being an allowlist);
# UNKNOWN is used where the holder or existence is not established.
# A route is named for every non-open source, per START_HERE.md.
#
# Sources are matched to the delivered bullets by a distinctive
# substring; the build refuses if any bullet is unmatched or any key
# matches two bullets, so the registry cannot drift from the entries.

import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gap_completeness as G  # noqa: E402

O, R, Gd, U = "OPEN", "REQUESTABLE", "GATED", "UNKNOWN"

# (substring of the bullet, tier, route or note)
TIERS = {
 1: [("NLCD impervious", O, "mrlc.gov download"),
     ("USGS gage records for Spokane", O, "USGS NWIS"),
     ("Naturalized flow estimates", O, "BPA / USACE modified-flows datasets, published"),
     ("Reservoir operating records", O, "USACE NWD DataQuery; PUD hydro pages; if a pool series is withheld, records request to the district")],
 2: [("MTBS", O, "mtbs.gov"),
     ("NIFC", O, "NIFC open data"),
     ("NLCD land cover pre-", O, "mrlc.gov"),
     ("HEC-RAS 2D model runs", Gd, "the engine is a free Windows download; the RUNS need terrain and geometry -- route: published post-fire hydraulic studies via a library, USGS OFR series"),
     ("Field Manning n", U, "not established who holds field n for these reaches; ask the state DOT hydraulics section and the USACE district; a documented 'none' is a finding")],
 3: [("Tribal government records", R, "direct request to each nation's emergency-management office AFTER the consultation step; federal FOIA does not reach tribal governments"),
     ("USACE Emergency Action Plans", Gd, "EAPs are commonly withheld as security-sensitive; FOIA to the district, expect redaction; document a refusal (it is a Gap 3 finding)"),
     ("PUD emergency coordination", R, "state public-records request (WA PRA) to each PUD"),
     ("Columbia River Treaty Permanent Engineering Board", O, "PEB annual reports, published"),
     ("Federal Register notices", O, "federalregister.gov")],
 4: [("National Inventory of Dams", O, "nid.sec.usace.army.mil public download"),
     ("USACE project design memoranda", Gd, "FOIA to the district; university depository libraries hold many USACE technical reports"),
     ("PUD annual reports", O, "published by each PUD; FERC eLibrary for license filings"),
     ("BC Hydro dam safety", Gd, "BC FOI request; BC Hydro water-use-planning documents, some public"),
     ("State dam safety office records", R, "public-records request: WA Ecology, OR OWRD, ID IDWR")],
 5: [("NID dam type", O, "nid.sec.usace.army.mil"),
     ("Froehlich (2008) and Xu", Gd, "journal paywall; university library, interlibrary loan, author preprints"),
     ("USACE dam safety inspection", Gd, "FOIA to the district; commonly withheld -- document the refusal"),
     ("State dam safety office breach", R, "public-records request to the state office"),
     ("Published case studies", Gd, "library; open-access where available")],
 6: [("USGS National Seismic Hazard", O, "usgs.gov hazard maps and tools"),
     ("PSHA", O, "USGS PSHA products for the Pacific Northwest"),
     ("Site-specific soil classification", O, "USGS VS30 map service"),
     ("Dam-specific seismic vulnerability", Gd, "FOIA to the district office holding the project file; the dam safety program manager; FERC eLibrary for FERC-licensed PUD dams (open); if refused, document it")],
 7: [("NOAA AR", O, "CW3E / Scripps AR catalog; NOAA PSL"),
     ("CMIP6", O, "ESGF nodes"),
     ("USACE reservoir rule curves", Gd, "water control manuals via FOIA to the district; some are published"),
     ("Historical flood records", O, "USGS and USACE published reports; NWIS"),
     ("SNOTEL", O, "NRCS SNOTEL")],
 8: [("NERC CIP", O, "nerc.com standards"),
     ("Dam owner SCADA documentation", Gd, "not public by design; CEII request through FERC for licensed dams; a refusal is the expected and documentable outcome"),
     ("USACE cyber vulnerability", Gd, "FOIA; expect refusal -- document it"),
     ("Human factors research", Gd, "journal literature; library, ILL"),
     ("Published cyber-physical attack", O, "open-access case studies and CISA advisories")],
 9: [("Historical compound events", U, "not established that any documented dam-cascade compound event exists; a search with a stated corpus is the first step"),
     ("Expert elicitation", R, "structured elicitation with dam-safety engineers; needs IRB and consent"),
     ("Published compound risk frameworks", O, "IPCC AR6, open"),
     ("Insurance industry compound", Gd, "commercial; route: published white papers, academic partnerships")],
 10: [("USGS gage records from 1948", O, "NWIS historical daily values"),
      ("Historical newspaper", O, "library newspaper archives; Oregon Historical Society"),
      ("USACE after-action", R, "NARA RG 77; district library"),
      ("Dam operating records from 1948", R, "NARA RG 77; the operating agencies' archives"),
      ("DEM of 1948", U, "not established that a 1948-condition surface exists; USGS historical topographic maps (open) and USACE historical hydrographic surveys at NARA are the route")],
 11: [("Census block groups", O, "data.census.gov"),
      ("National Structure Inventory", O, "USACE NSI 2.0 public"),
      ("Critical facility databases", O, "HIFLD open data"),
      ("FEMA P-2067", O, "fema.gov"),
      ("Dasymetric", O, "open tools")],
 12: [("3DEP DEM", O, "USGS national map"),
      ("NOAA bathymetry", O, "NOAA charts"),
      ("NLCD land cover", O, "mrlc.gov"),
      ("NID dam geometry", O, "nid.sec.usace.army.mil"),
      ("USACE reservoir surveys", R, "records request to the district; sedimentation surveys")],
 13: [("HEC-RAS 2D (Windows", O, "free USACE download; Windows only"),
      ("3DEP DEM", O, "USGS national map"),
      ("NID dam geometry", O, "nid.sec.usace.army.mil"),
      ("Published breach parameters", Gd, "journal literature; library, ILL"),
      ("Historical inflow hydrographs", O, "NWIS; USACE published records")],
 14: [("USGS Mineral Resources Data System", O, "mrdata.usgs.gov"),
      ("State mining permits", R, "state agency records request (WA DNR, OR DOGAMI, ID IDL, MT DEQ; BC EMLI)"),
      ("USGS groundwater monitoring wells", O, "NWIS groundwater"),
      ("InSAR subsidence products", O, "ESA Copernicus (Sentinel-1); ARIA products"),
      ("NLCD land cover change", O, "mrlc.gov"),
      ("USGS gage records for tributaries", O, "NWIS"),
      ("Reservoir rim stability assessments", Gd, "FOIA to the district office holding the project file; the dam safety program manager; university holdings of USACE technical reports; BC Hydro water-use-planning documents (some public); the FERC licensing record, which is open. IF REFUSED: document it -- a data point on the EAP coverage question in Gap 3"),
      ("The 2024-2025 subsurface literature", Gd, "journal paywall; DOIs are given; library, ILL")],
 15: [("National Bridge Inventory", O, "FHWA NBI public download"),
      ("USGS gage records and high-water", O, "NWIS; USGS flood event viewer for HWMs"),
      ("HEC-RAS 2D bridge routines", O, "free USACE download; Windows only"),
      ("Upstream debris supply sources", O, "state landslide inventories (WA DNR, OR DOGAMI); the Gap 14 and Gap 2 outputs"),
      ("USACE bridge scour and backwater", Gd, "FOIA to the district; state DOT scour-critical files via public-records request"),
      ("The 2024-2025 debris-scour", Gd, "journal paywall; identifiers given; library, ILL")],
}

# A positive control per gap: something the deliverable is run against
# before it is trusted. 'present' marks the gaps whose entry already has
# one (CCA_017). None is a run; each is a NAMED candidate.
KNOWN_ANSWER = {
 1: "present in the entry (validate against known storm events)",
 2: "present in the entry (post-flood gage records)",
 3: "a published dam-tribe MOU the matrix method must classify as coordinated, and a dam with no published agreement it must classify as absent-or-unknown -- both directions",
 4: "one node whose owner the FERC licensing record states openly; the seam map must place it",
 5: "a documented historical breach with published Froehlich inputs (the equation paper's own worked case); the table must reproduce it within the equation's stated scatter",
 6: "a USGS NSHM published PGA at a benchmark site; the extraction must return it",
 7: "a documented historical inflow peak (a published USACE flood report) reproduced from the AR catalog plus gage record",
 8: "a documented incident with a published override timeline; the trust model must reproduce its response time",
 9: "two independent synthetic events; the interaction factor must return 1.0 within the stated tolerance",
 10: "this gap IS the known answer for the whole spec",
 11: "a FEMA-published exposure count for a published flood zone; the overlay must reproduce it",
 12: "present in the entry (the falsifier -- reproduce on a second machine)",
 13: "reservoir-chain-coupling/chain.py: band width equals the antecedent pool on a constructed chain; the terrain run must reproduce it at one synthetic node before any real node is read",
 14: "present in the entry (Bondevik & Sorteberg 2021, measured u)",
 15: "bridge-impoundment/bridge_impoundment.py: gain above one iff release is faster than fill, on constructed inputs; and the Fjaerland volume as the release-half check",
}

CONSENT_STEP_GAP3 = (
 "0. Before any records request: initiate consultation with each "
 "nation's emergency-management or natural-resources office; obtain "
 "consent for the study and for publication of its findings; record "
 "the terms. Federal FOIA does not reach tribal governments -- "
 "requests are direct and voluntary, and a refusal is recorded, never "
 "worked around. The Columbia River Treaty's Joint Executive Board "
 "(tribal and First Nations representation) is a named route. See the "
 "ethics sections of revision-mechanism/ and transmission-decay/.")

SCHEMA_POINTER = {
 5: "initiator_schemas.py: breach_params.csv, 15 columns",
 6: "initiator_schemas.py: seismic_params.csv, 12 columns",
 7: "initiator_schemas.py: hydro_params.csv, 12 columns",
 8: "initiator_schemas.py: cyber_params.yaml, 10 columns",
 9: "initiator_schemas.py: compound_matrix.csv, 10 columns",
}


def build():
    ents = G.entries()
    out = {"probed": False,
           "basis": "tiers carried from general knowledge of the "
                    "holding institutions; not probed from this "
                    "environment (allowlist egress); UNKNOWN where the "
                    "holder or existence is not established",
           "gaps": {}}
    for g in sorted(ents):
        bullets = G._source_bullets(ents[g]) if hasattr(G, "_source_bullets") \
            else None
        if bullets is None:
            import kill_audit as K
            bullets = K._source_bullets(ents[g])
        rows = []
        used = set()
        for key, tier, route in TIERS[g]:
            hits = [i for i, b in enumerate(bullets) if key in b]
            if len(hits) != 1:
                raise SystemExit("gap %d key %r matched %d bullets"
                                 % (g, key, len(hits)))
            i = hits[0]
            if i in used:
                raise SystemExit("gap %d bullet %d matched twice" % (g, i))
            used.add(i)
            rows.append({"source": bullets[i][2:].strip(), "tier": tier,
                         "route": route})
        if len(used) != len(bullets):
            missing = [bullets[i] for i in range(len(bullets))
                       if i not in used]
            raise SystemExit("gap %d unmatched bullets: %s" % (g, missing))
        entry = {"tiers": rows, "known_answer": KNOWN_ANSWER[g]}
        if g == 3:
            entry["consent_step"] = CONSENT_STEP_GAP3
        if g in SCHEMA_POINTER:
            entry["deliverable_schema"] = SCHEMA_POINTER[g]
        out["gaps"][str(g)] = entry
    return out


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write("build_addenda.py has no checks of its own; they live "
                         "in selftest_kill.py.\n")
        sys.exit(2)
    data = build()
    p = os.path.join(HERE, "gap_addenda.json")
    io.open(p, "w", encoding="utf-8").write(
        json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    n = sum(len(v["tiers"]) for v in data["gaps"].values())
    print("gap_addenda.json: %d gaps, %d sources tiered" % (len(data["gaps"]), n))
