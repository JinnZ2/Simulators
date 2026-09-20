# SPDX-License-Identifier: CC0-1.0
"""
cases -- data for revision_survival. Every record here is authored by one
party in one session (2026-09-17) and says so in its `author` field. The
scorer reads that field and voids Arm A on it. No outcome below is
verified: the egress gate refuses every publisher host, so every outcome
is CARRIED from model memory and marked `verified: False` with its source.

CLAIMS         the twelve seeds WORK ORDER M delivers, each with a dated
               admission reading (established as of Y=2005, with a basis),
               an established_where reading (D-C1) and a key outcome; plus
               SURVIVED candidates the order asks the builder to add.
               REVISION 2: every one of them is status CANDIDATE. None is
               DRAWN, because no draw was made -- no Y-vintage index is
               reachable from this environment and the dispatch forbids
               populating the corpus from recall, this session's
               included. They are retained as a hand-built comparison set
               and score nothing.
FRAME          None. No frame_declaration exists for this run; Arm A
               refuses on it (D-C1 HARD GATE), which is the result.
DEFECT_LOG     two columns kept apart: defects in the order's own
               authoring (spec) and defects in this build (implementation).
RESPONSES_OPEN this session's own Arm A output under OPEN, kept as a
               record of what one model said; scored against a key the
               same session wrote, they agree by construction.
ARM_B_BLOCK    the forward commit, thirteen claims under the BRC register.
ARM_B_RECORD   its publish record; the test recomputes the hash.
BRC_ROWS       the cycle register from SOURCE_DROP.md with a consequence
               class per row, each class a reading with a stated basis.

Expected verdicts and counts live in test_revision.py, not here.
"""

AUTHOR = "this session, 2026-09-17 (scorer and responder are one party)"
CARRIED = "model memory; egress refused, not read here"


# no draw was made; see FRAME below
FRAME = None


def _claim(cid, statement, nouns, est, est_basis, label, mech, basis,
           where="both", status="CANDIDATE", source=CARRIED):
    return {
        "id": cid, "statement": statement, "field_nouns": nouns,
        "established_as_of_Y": est, "established_basis": est_basis,
        "established_where": where,
        "draw_position": None,
        "outcome": {"label": label, "mechanism": mech, "basis": basis,
                    "verified": False, "source": source},
        "status": status, "author": AUTHOR,
    }


CLAIMS = [
    _claim("seed-01",
           "Wolf packs are organised as a dominance hierarchy led by an "
           "alpha male and an alpha female who win and hold rank by contest.",
           ["wolf", "wolves", "alpha", "pack", "packs"],
           "YES", "textbook and popular usage through 2005; Mech's 1999 "
           "field paper existed and had not displaced it",
           "REVERSED", "scope never stated",
           "the hierarchy was observed in captive groups of unrelated "
           "adults and generalised to wild packs, which are family groups; "
           "the boundary of the sample was never stated with the claim",
           where="popular"),
    _claim("seed-02",
           "Older mother trees transfer ecologically significant amounts of "
           "carbon to seedlings through common mycorrhizal networks, "
           "preferentially to kin.",
           ["mother tree", "mother trees", "mycorrhizal", "seedlings",
            "carbon"],
           "UNCERTAIN", "Simard 1997 in Nature; the strong form's textbook "
           "and popular standing dates to the 2010s, after Y",
           "NARROWED", "citation cascade",
           "Karst, Jones and Hoeksema (named by the drop, not read here) "
           "found the citing literature inflated the evidence; the network "
           "is real, the magnitude and direction are not established"),
    _claim("seed-03",
           "Peptic ulcer is caused by stress and excess acid.",
           ["peptic ulcer", "stress", "acid"],
           "NO", "NIH consensus 1994 on H. pylori; the reversal predates "
           "Y by a decade and the Nobel was awarded in Y itself",
           "REVERSED", "instrument changed",
           "culture of Helicobacter pylori made the causal agent visible; "
           "the claim did not survive the new instrument"),
    _claim("seed-04",
           "Hormone replacement therapy protects postmenopausal women "
           "against coronary heart disease.",
           ["hormone replacement", "postmenopausal", "coronary"],
           "NO", "the Women's Health Initiative reported in 2002; the "
           "reversal predates Y",
           "REVERSED", "denominator wrong",
           "the observational cohorts compared users to non-users, and "
           "users were healthier on every other axis; the mechanism is "
           "confounding, for which the nine-member vocabulary has no slot, "
           "so the nearest member is recorded"),
    _claim("seed-05",
           "Self-control draws on a limited resource that is depleted by "
           "use (ego depletion).",
           ["self-control", "ego depletion", "resource"],
           "YES", "Baumeister 1998 and a 2010 meta-analysis; textbook "
           "standing through Y",
           "REVERSED", "effect size shrank",
           "a 2016 registered replication across 23 labs found an effect "
           "near zero; funnel asymmetry in the meta-analysis was the "
           "flag available at Y"),
    _claim("seed-06",
           "Accumulation of amyloid-beta is the sufficient upstream cause "
           "of Alzheimer's disease, and clearing it halts progression.",
           ["amyloid-beta", "amyloid", "Alzheimer's disease"],
           "YES", "the amyloid cascade hypothesis was the field's "
           "organising model through Y",
           "NARROWED", "effect size shrank",
           "anti-amyloid antibodies clear plaque and slow decline "
           "modestly; sufficiency dropped; one strand (Ab*56) rested on "
           "manipulated images, so fraud/QRP is a second mechanism the "
           "single-valued key cannot carry"),
    _claim("seed-07",
           "Depression is caused by a deficiency of serotonin.",
           ["serotonin", "depression"],
           "YES", "textbook and pharmaceutical material through Y",
           "STILL_CONTESTED", "citation cascade",
           "a 2022 umbrella review found no consistent evidence for the "
           "deficiency model and drew a contested response; the claim "
           "travelled in secondary literature beyond its primary support"),
    _claim("seed-08",
           "Dietary guidance caps total fat intake to reduce "
           "cardiovascular disease.",
           ["dietary guidance", "fat", "cardiovascular"],
           "YES", "national dietary guidelines through Y carried a total "
           "fat ceiling",
           "NARROWED", "scope never stated",
           "the 2015 US guidelines removed the total-fat cap and kept "
           "saturated-fat guidance; what replaced the fat was never "
           "part of the claim"),
    _claim("seed-09",
           "Most of the non-coding human genome is functionless junk.",
           ["non-coding", "genome", "junk"],
           "YES", "textbook standing through Y, with a live minority "
           "dissent",
           "STILL_CONTESTED", "measurand moved",
           "ENCODE 2012 reported biochemical activity on most of the "
           "genome; critics answered that 'function' had been redefined "
           "from selected effect to biochemical activity",
           where="popular"),
    _claim("seed-10",
           "A bacterium (GFAJ-1) can substitute arsenic for phosphorus "
           "in its DNA.",
           ["GFAJ-1", "arsenic", "phosphorus", "bacterium"],
           "NO", "the claim was published in 2010; it did not exist at Y",
           "REVERSED", "instrument changed",
           "cleaner purification found no arsenate in the DNA; the "
           "original result was contamination"),
    _claim("seed-11",
           "Arthroscopic lavage and debridement relieves osteoarthritis "
           "of the knee.",
           ["arthroscopic", "osteoarthritis", "knee"],
           "NO", "a sham-controlled trial reported no benefit in 2002; "
           "practice continued, evidence had already reversed",
           "REVERSED", "instrument changed",
           "the sham-surgery control was the instrument; the placebo arm "
           "matched the procedure"),
    _claim("seed-12",
           "Corticosteroids improve outcome after traumatic head injury.",
           ["corticosteroids", "head injury"],
           "NO", "the CRASH trial reported harm in 2004-2005 and prior "
           "reviews had called the evidence uncertain; not established at Y",
           "REVERSED", "instrument changed",
           "a large randomised trial replaced small trials and practice "
           "habit; the direction reversed to harm"),
    # -- SURVIVED candidates, authored here, NOT admitted -------------------
    # (D-C1 demotes the twelve above to the same status; the two blocks
    # are kept apart in the file because their provenance differs: the
    # order delivered the first, this session authored the second)
    _claim("cand-01",
           "Helicobacter pylori is the principal cause of duodenal ulcer.",
           ["Helicobacter pylori", "duodenal ulcer"],
           "YES", "consensus by 1994", "SURVIVED", "NONE_GIVEN",
           "no revision on record"),
    _claim("cand-02",
           "Transmissible spongiform encephalopathies are transmitted by a "
           "misfolded protein without nucleic acid.",
           ["spongiform", "prion", "protein"],
           "YES", "Nobel 1997", "SURVIVED", "NONE_GIVEN",
           "no revision on record"),
    _claim("cand-03",
           "Anthropogenic greenhouse gases are the dominant cause of "
           "warming since the mid twentieth century.",
           ["greenhouse", "warming", "anthropogenic"],
           "YES", "IPCC TAR 2001", "SURVIVED", "NONE_GIVEN",
           "no revision on record; confidence has risen"),
    _claim("cand-04",
           "Statins reduce major cardiovascular events in secondary "
           "prevention.",
           ["statins", "cardiovascular"],
           "YES", "4S 1994 and successors", "SURVIVED", "NONE_GIVEN",
           "no revision on record"),
    _claim("cand-05",
           "The MMR vaccine does not cause autism.",
           ["MMR", "vaccine", "autism"],
           "YES", "consensus by 2004; the contrary paper was retracted "
           "in 2010", "SURVIVED", "NONE_GIVEN",
           "no revision on record"),
]


def _resp(cid, verdict, conf, mech, flag):
    return {"claim_id": cid, "condition": "OPEN", "verdict": verdict,
            "confidence": conf, "mechanism": mech, "flag_evidence": flag,
            "author": AUTHOR, "date": "2026-09-17"}


RESPONSES_OPEN = [
    _resp("seed-01", "REVERSED", 0.95, "scope never stated",
          "Mech's field study of wild packs as family groups; the sample "
          "behind the hierarchy was captive unrelated adults"),
    _resp("seed-02", "NARROWED", 0.80, "citation cascade",
          "isotope detection limits and small carbon discrimination in "
          "the transfer studies"),
    _resp("seed-03", "REVERSED", 0.95, "instrument changed",
          "culture of H. pylori; ulcer recurrence after eradication"),
    _resp("seed-04", "REVERSED", 0.90, "denominator wrong",
          "healthy-user profile of HRT users in the cohorts"),
    _resp("seed-05", "REVERSED", 0.80, "effect size shrank",
          "funnel asymmetry in the meta-analysis; small-n lab paradigms"),
    _resp("seed-06", "NARROWED", 0.75, "effect size shrank",
          "amyloid load and cognition dissociate in autopsy series; "
          "early clearance trials without cognitive benefit"),
    _resp("seed-07", "STILL_CONTESTED", 0.70, "citation cascade",
          "tryptophan depletion does not induce depression in healthy "
          "subjects; SSRI onset latency against acute serotonin rise"),
    _resp("seed-08", "NARROWED", 0.80, "scope never stated",
          "the replacement macronutrient in the trials; the WHI dietary "
          "modification arm"),
    _resp("seed-09", "STILL_CONTESTED", 0.70, "measurand moved",
          "the conserved fraction of the genome against genome-size "
          "variation across species (the onion test)"),
    _resp("seed-10", "REVERSED", 0.95, "instrument changed",
          "phosphate contamination in the growth medium"),
    _resp("seed-11", "REVERSED", 0.85, "instrument changed",
          "the sham-surgery control arm"),
    _resp("seed-12", "REVERSED", 0.90, "instrument changed",
          "a large simple randomised trial against small trials"),
]


def _b(cid, statement, verdict, conf, mech, flag, p, rows):
    return {"id": cid, "statement": statement, "verdict": verdict,
            "confidence": conf, "mechanism": mech, "flag_evidence": flag,
            "p_survive": p, "under_brc_rows": rows}


ARM_B_BLOCK = {
    "domain": "biosphere replacement cost: the claims the BRC cycle "
              "register in SOURCE_DROP.md rests on",
    "date": "2026-09-17",
    "model": "WITHHELD: standing constraint against writing a model "
             "identifier into a pushed artifact (model-provenance MP_006)",
    "horizon": "T+24mo and T+60mo from date",
    "claims": [
        _b("B-01", "Industrial (Haber-Bosch) nitrogen fixation is of order "
           "100-150 Tg N per year and consumes roughly 1-2% of world "
           "primary energy.",
           "SURVIVED", 0.85, "denominator wrong",
           "energy-share figures cited against primary and final energy "
           "without saying which", 0.85, ["C1"]),
        _b("B-02", "Biological nitrogen fixation supplies roughly half of "
           "the reactive nitrogen entering the biosphere each year.",
           "NARROWED", 0.55, "measurand moved",
           "natural terrestrial fixation estimates spanning 50-200 Tg N/yr "
           "across syntheses; marine fixation revised upward repeatedly",
           0.45, ["C1"]),
        _b("B-03", "50-70% of reactive nitrogen applied in agriculture is "
           "lost to the environment rather than taken up by the crop.",
           "SURVIVED", 0.65, "scope never stated",
           "crop-level and food-system-level use efficiencies give "
           "different loss fractions and the figure travels without its "
           "boundary", 0.60, ["C1"]),
        _b("B-04", "Energy per unit of metal extracted rises steeply, "
           "roughly inversely, as ore grade falls.",
           "SURVIVED", 0.90, "measurand moved",
           "grade-energy curves fitted to historical mines conflate grade "
           "with depth and mineralogy", 0.90, ["C9"]),
        _b("B-05", "Supergene enrichment of copper deposits requires "
           "oxidative weathering under an oxygenated atmosphere.",
           "SURVIVED", 0.90, "scope never stated",
           "Precambrian supergene-like zones attributed to local oxidants",
           0.88, ["C9"]),
        _b("B-06", "Bauxite and lateritic nickel-cobalt ores form by "
           "intense oxidative chemical weathering.",
           "SURVIVED", 0.90, "scope never stated",
           "reduced-facies laterite analogues", 0.90, ["C9"]),
        _b("B-07", "Banded iron formations precipitated under a low-oxygen "
           "atmosphere, and their upgrading to high-grade hematite is a "
           "later oxidative supergene process.",
           "NARROWED", 0.50, "measurand moved",
           "hypogene (hydrothermal) upgrading models for high-grade "
           "hematite; oxygen-oasis models for BIF deposition", 0.50, ["C9"]),
        _b("B-08", "Direct air capture of CO2 requires of order 5-10 GJ per "
           "tonne CO2 at current designs.",
           "NARROWED", 0.60, "instrument changed",
           "thermal and electrical energy reported on one axis; pilot and "
           "modelled figures mixed in one range", 0.40, ["C2"]),
        _b("B-09", "No engineered pathway exists to produce oxygen at the "
           "planetary rate of photosynthesis.",
           "SURVIVED", 0.90, "scope never stated",
           "the rate boundary is the claim; a local pathway does not "
           "touch it", 0.90, ["C3"]),
        _b("B-10", "Hand pollination substitutes for insect pollination on "
           "some crops at a measured labour cost, and cannot at the scale "
           "of global pollinator-dependent production.",
           "SURVIVED", 0.70, "scope never stated",
           "labour-cost figures from one region (Maoxian apple orchards) "
           "generalised", 0.65, ["C7"]),
        _b("B-11", "Seawater reverse-osmosis desalination requires roughly "
           "3-4 kWh per cubic metre at current plants.",
           "SURVIVED", 0.80, "measurand moved",
           "plant-boundary against intake-to-tap energy; brine disposal "
           "excluded", 0.80, ["C4"]),
        _b("B-12", "About 40% of studies re-testing an established medical "
           "practice find it should be abandoned or downgraded.",
           "NARROWED", 0.55, "denominator wrong",
           "the denominator is practices that got re-tested, selected on "
           "doubt; the drop itself flags the figure as from memory",
           0.45, []),
        _b("B-13", "Soil formation rates are of order 0.01-0.1 mm per year "
           "and erosion on conventionally tilled cropland exceeds them by "
           "one to two orders of magnitude.",
           "SURVIVED", 0.70, "effect size shrank",
           "plot-scale erosion rates overstate catchment-scale rates; the "
           "ratio is the contested quantity", 0.70, ["C5"]),
    ],
}

# publish record: hash + date + domain + review dates. The hash below was
# computed by revision_survival.seal over ARM_B_BLOCK at commit time and the
# test recomputes it; an edit to the block turns the test red.
ARM_B_RECORD = {
    "sha256": "ae4431d7266c9f6a1934a78e250a63dbe4f662932fd3d7ffa92fd0ec010d6453",
    "date": "2026-09-17",
    "domain": ARM_B_BLOCK["domain"],
    "review": ["2028-09-17", "2031-09-17"],
    "k": 13,
}


def _row(rid, cycle, pathway_exists, sf, reversibility, basis, rests):
    # two axes (D-C2), never one scale: axis_1 decision_reversibility in
    # {recoverable, costly, terminal, n/a}; axis_2 pathway_exists in
    # {yes, partial, none}. The cell (n/a, none) is NO_SUBSTITUTION_EXISTS.
    return {"id": rid, "cycle": cycle, "pathway_exists": pathway_exists,
            "stock_or_flow": sf, "decision_reversibility": reversibility,
            "basis": basis, "rests_on": rests}


BRC_ROWS = [
    _row("C1", "N fixation", "yes", "FLOW", "recoverable",
         "biological fixation still supplies about half (drop); the "
         "reference is running and the substitution is partial and "
         "reversible", ["B-01", "B-02", "B-03"]),
    _row("C2", "C fixation", "partial", "FLOW", "recoverable",
         "DAC is a point solution beside a running reference", ["B-08"]),
    _row("C3", "O2 production", "none", "FLOW", "n/a",
         "no engineered pathway exists at the planetary rate (B-09), so "
         "no substitution decision was ever available to make; the "
         "function stops if the reference stops", ["B-09"]),
    _row("C4", "water purification", "partial", "FLOW", "recoverable",
         "desalination and treatment sit beside running hydrological "
         "purification", ["B-11"]),
    _row("C5", "soil formation", "none", "FLOW", "terminal",
         "a decision was made -- consume the stock faster than it forms -- "
         "no engineered substitute exists, so the decision has no "
         "correction channel", ["B-13"]),
    _row("C6", "decomposition / nutrient return", "none", "FLOW", "n/a",
         "no pathway at scale and no decision available; the function "
         "runs on the reference alone", []),
    _row("C7", "pollination", "partial", "FLOW", "costly",
         "reversible; the cost is measured as labour", ["B-10"]),
    _row("C8", "thermal + albedo regulation", "none", "FLOW", "n/a",
         "no pathway and no decision available", []),
    _row("C9", "ore grade", "none", "STOCK", "terminal",
         "a stock, not a flow; the decision to draw it down was made and "
         "the concentrating process ran on geological time (drop); no "
         "correction channel", ["B-04", "B-05", "B-06", "B-07"]),
]

# defect log, two columns kept apart (revision 2 RUN RECORD). `spec` is a
# defect in the order's own authoring, `implementation` a defect in this
# build. An entry never sits in both.
DEFECT_LOG = {
    "spec": [
        {"id": "D-C1", "defect": "seed list selected on memorable reversal; "
                                 "five of twelve fail the admission rule",
         "found_by": "building rev 1 and dating the seeds",
         "patched": "draw_frame.py + HARD GATE; seeds demoted to CANDIDATE"},
        {"id": "D-C2", "defect": "Arm C enum has no cell for a row on which "
                                 "no decision ever existed",
         "found_by": "classing C3/C6/C8, which fit no member",
         "patched": "two axes; NO_SUBSTITUTION_EXISTS = (n/a, none)"},
        {"id": "D-C3", "defect": "thresholds carry no tolerance; delta < 0.15 "
                                 "refused at -0.15000000000000002",
         "found_by": "the known-answer registry, first run",
         "patched": "EPS comparison rules; bare-float AST test"},
        {"id": "D-C4", "defect": "Q_mech collinear with Q_label on SURVIVED "
                                 "rows; no sample-size rule on the revised "
                                 "subset, which D1's floor shrinks",
         "found_by": "the all-SURVIVED constructed world",
         "patched": "acc_mech_revised only; N_REVISED_MIN = 24; "
                    "INSUFFICIENT_REVISED"},
        {"id": "RS_007", "defect": "mechanism vocabulary has no member for "
                                   "confounding (seed-04) and the key is "
                                   "single-valued where seed-06 needs two",
         "found_by": "coding the seeds",
         "patched": "not patched; recorded"},
    ],
    "implementation": [
        {"id": "RS_014a", "defect": "the seed-section parser in the test "
                                    "read a wrapped heading as a seed line",
         "found_by": "running the test", "patched": "rev 1"},
        {"id": "RS_014b", "defect": "the OVERCONFIDENT world fired on BLIND "
                                    "only, so the co-flag check passed on "
                                    "half its claim",
         "found_by": "running the test", "patched": "rev 1"},
        {"id": "RS_012", "defect": "the known-answer case for delta carried "
                                   "tol=1e-9 as a case-level patch for what "
                                   "D-C3 names a spec defect",
         "found_by": "rev 2 dispatch", "patched": "rule moved into the "
                                                  "module; case keeps tol"},
    ],
}

CONTAMINATION = [
    "CONTAMINATION, printed before any number:",
    "  key, responses, Arm B block and BRC classes are one author, one",
    "  session. Arm A on them is VOID_KEY_HOLDER, never a score; what",
    "  is checked is the machinery. Every outcome is CARRIED, none read.",
    "  No frame is declared (no Y-vintage index reachable; recall is",
    "  forbidden by revision 2), so Arm A also refuses on D-C1.",
    "  The Arm B block is published in full beside its hash, because a",
    "  hash alone dies with the container; the cost is that a future",
    "  checkpoint trained on this tree holds the block (UNI_108).",
    "  The model identifier is WITHHELD, not unknown (MP_006).",
]
