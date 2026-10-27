# SPDX-License-Identifier: CC0-1.0
"""FWO-15 fixtures. CONSTRUCTED: every study and case below was authored by the
same agent that wrote the scorer and the expected verdicts, so every result on
them is REGRESSION, not validation. No study, population or date here refers
to a real publication. Expected verdicts live in test_fwo15.py, not here.
"""

ABSENT = "ABSENT"


def frame(fid, arm, declared_at="2026-10-04"):
    return {"frame_id": fid, "arm": arm, "description": "CONSTRUCTED frame %s (%s)" % (fid, arm),
            "declared_at": declared_at}


def studies(prefix, fid, arm, yes, no, absent=0, e2="ABSENT", sub=None, coded_at="2026-10-05"):
    out = []
    for i, e4 in enumerate(["YES"] * yes + ["NO"] * no + [ABSENT] * absent):
        s = {"study_id": "%s-%03d" % (prefix, i), "frame_id": fid, "coded_at": coded_at,
             "E1": "CONSTRUCTED population", "E2": e2, "E3": "humans" if arm == "human" else ABSENT,
             "E4": e4, "E5": arm}
        if sub:
            s["sub_literature"] = sub
        out.append(s)
    return out


def world(human_yes, human_no, animal_yes, animal_no, human_e2="ABSENT"):
    frames = [frame("h", "human"), frame("c", "captive-animal"), frame("p", "production-animal")]
    s = (studies("h", "h", "human", human_yes, human_no, absent=3, e2=human_e2)
         + studies("c", "c", "captive-animal", animal_yes, animal_no, e2="direct")
         + studies("p", "p", "production-animal", animal_yes, animal_no, e2="token-gated"))
    return frames, s


GAP = world(2, 28, 18, 12)
NO_GAP = world(12, 18, 13, 17)
INDETERMINATE = world(6, 19, 11, 14)
UNDER_FLOOR = world(1, 9, 18, 12)


def _scope():
    frames = [frame("h", "human"), frame("c", "captive-animal"), frame("p", "production-animal")]
    s = (studies("ha", "h", "human", 1, 24, sub="sub-A")
         + studies("hb", "h", "human", 15, 10, sub="sub-B", e2="token-gated")
         + studies("c", "c", "captive-animal", 18, 12, e2="direct")
         + studies("p", "p", "production-animal", 18, 12, e2="direct"))
    return frames, s


SCOPE = _scope()


def _fail():
    """Built to FAIL the frame-before-coding rule and the arm rule."""
    frames = [frame("h", "human", declared_at="2026-10-04"), frame("c", "captive-animal")]
    early = studies("early", "h", "human", 1, 0, coded_at="2026-10-01")
    wrong_arm = studies("arm", "h", "captive-animal", 1, 0)
    no_frame = studies("nof", "never-declared", "human", 1, 0)
    missing_field = studies("mf", "h", "human", 1, 0)
    del missing_field[0]["E3"]
    return frames, early + wrong_arm + no_frame + missing_field


FAIL_A = _fail()


def case(population, date=None, source="CONSTRUCTED source", before=True, after=True,
         confounds=None, reading=None, omit_confounds=False):
    c = {
        "population": population,
        "coupling_instrument": "permit",
        "coupling_date": ABSENT if date is None else ({"date": date, "source": source} if source else {"date": date}),
        "behavior_before": {"field": "CONSTRUCTED before", "source": "CONSTRUCTED"} if before else ABSENT,
        "behavior_after": {"field": "CONSTRUCTED after", "source": "CONSTRUCTED"} if after else ABSENT,
        "coupling_completeness": "full",
    }
    if not omit_confounds:
        c["confounds"] = [] if confounds is None else confounds
    if reading:
        c["shift_reading"] = {"reading": reading, "basis": "CONSTRUCTED basis"}
    return c


CASES_B = [
    case("undated"),
    case("dated-unsourced", date="1990", source=None),
    case("coincident", date="1990", confounds=[{"kind": "roads", "date": "1988"}], reading="VISIBLE"),
    case("visible", date="1990", confounds=[{"kind": "media", "date": "1950"}], reading="VISIBLE"),
    case("not-visible", date="1990", confounds=[{"kind": "media", "date": "1950"}], reading="NOT_VISIBLE"),
    case("none-declared", date="1990", reading="NOT_VISIBLE"),
    case("missing-after", date="1990", after=False, confounds=[{"kind": "media", "date": "1950"}], reading="VISIBLE"),
    case("shared-1", date="1990", confounds=[{"kind": "media", "date": "1950"}], reading="VISIBLE"),
]

FAIL_B = [
    case("no-confound-column", date="1990", omit_confounds=True),
    case("other-unnamed", date="1990", confounds=[{"kind": "other", "date": "1950"}]),
    case("reading-without-basis", date="1990", confounds=[]),
]
FAIL_B[2]["shift_reading"] = {"reading": "VISIBLE"}
