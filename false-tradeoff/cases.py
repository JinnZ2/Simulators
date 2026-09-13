# cases.py
# CC0 1.0 Universal / public domain dedication.
#
# Hand-built dilemmas for false_tradeoff.py. Structure only: every case
# supplies the fields the checks read and nothing is inferred from the
# statement string, which is carried as a label and read by nothing.
#
# No case carries its own expected flags. The expected sets live in
# test_tradeoff.py, so a case cannot agree with the instrument by
# construction.
#
# Every case is CONSTRUCTED. None is a report of a real decision, and no
# real organisation, incident or person is named. The statements are
# generic on purpose: a recognisable one invites the reader to score the
# case from what they already believe about it, and the instrument reads
# structure.

from false_tradeoff import (
    Constraint, ConstraintKind, DeferredCost, Horizon, Option, Provenance,
    dilemma,
)

OBS = Provenance.OBSERVED
STIP = Provenance.STIPULATED
DERV = Provenance.DERIVED

PHYS = ConstraintKind.PHYSICAL
RULE = ConstraintKind.RULE
UNST = ConstraintKind.UNSTATED


CASE_T = dilemma(
    # Two options, both handed over, and whatever eliminates the third
    # branch is not stated anywhere. The difficulty is in the
    # stipulation, not in the world.
    statement="T diverted or not diverted",
    options=[
        Option("divert", STIP, "the person posing the problem"),
        Option("do not divert", STIP, "the person posing the problem"),
    ],
    side_a="harm on the main line", side_b="harm on the side line",
    constraints=[
        Constraint(UNST, "nothing given for why the vehicle cannot be halted"),
        Constraint(UNST, "nothing given for why nobody can be warned"),
    ],
    boundary_a={"main_line_party", "side_line_party"},
    boundary_b={"main_line_party", "side_line_party"},
    depends_a={"main_line_party"},
    depends_b={"side_line_party"},
    horizon_a=Horizon(1, "day"), horizon_b=Horizon(1, "day"),
    deferred_costs=[],
)

CASE_M = dilemma(
    # The quarter's ledger closes before the skipped upkeep arrives, and
    # it arrives on the same asset that ledger already counts.
    statement="M upkeep against quarter cost",
    options=[
        Option("full upkeep interval", OBS, "the maintenance log"),
        Option("stretched upkeep interval", OBS, "the maintenance log"),
        Option("replace the unit", DERV, "the asset register"),
    ],
    side_a="reported cost this quarter", side_b="asset condition",
    constraints=[
        Constraint(PHYS, "the seal wears at a rate nobody sets"),
        Constraint(RULE, "capital and operating funds are not interchangeable"),
    ],
    boundary_a={"pump_station", "operating_budget"},
    boundary_b={"pump_station", "service_record"},
    depends_a={"pump_station", "operating_budget"},
    depends_b={"pump_station", "service_record"},
    horizon_a=Horizon(1, "quarter"), horizon_b=Horizon(10, "year"),
    deferred_costs=[
        DeferredCost("A", "pump_station", Horizon(3, "year")),
    ],
)

CASE_B = dilemma(
    # The cost is said to move from one ledger to the other, and the
    # entity it lands on is depended on by both while counted by one.
    statement="B outlay against exposure",
    options=[
        Option("keep the current arrangement", OBS, "the operating record"),
        Option("fund the change", OBS, "the operating record"),
    ],
    side_a="outlay", side_b="exposure",
    constraints=[
        Constraint(PHYS, "the span carries what it carries"),
    ],
    boundary_a={"structure", "outlay_line"},
    boundary_b={"crew", "structure"},
    depends_a={"crew", "structure"},
    depends_b={"crew", "outlay_line"},
    horizon_a=Horizon(1, "year"), horizon_b=Horizon(1, "year"),
    deferred_costs=[],
)

CASE_G = dilemma(
    # One conserved quantity between two uses, one window, one ledger,
    # and a physical constraint doing the eliminating. The case the
    # instrument has to be able to reach.
    statement="G one reservoir two draws",
    options=[
        Option("draw for the upper field", OBS, "the abstraction record"),
        Option("draw for the lower field", OBS, "the abstraction record"),
        Option("split the draw", OBS, "the abstraction record"),
    ],
    side_a="upper field draw", side_b="lower field draw",
    constraints=[
        Constraint(PHYS, "the stored volume in the season is what fell"),
    ],
    boundary_a={"reservoir", "upper_field", "lower_field"},
    boundary_b={"reservoir", "upper_field", "lower_field"},
    depends_a={"reservoir", "upper_field"},
    depends_b={"reservoir", "lower_field"},
    horizon_a=Horizon(1, "year"), horizon_b=Horizon(1, "year"),
    deferred_costs=[],
    conserved_quantity="stored volume in the season, cubic metres",
)

CASE_R = dilemma(
    # Every option outside the two is eliminated by permission and by
    # nothing else. The dilemma holds exactly as long as the rules do.
    statement="R filing window against review",
    options=[
        Option("file on the early date", OBS, "the submissions log"),
        Option("file on the late date", OBS, "the submissions log"),
    ],
    side_a="time for review", side_b="time in the queue",
    constraints=[
        Constraint(RULE, "submissions are accepted on two dates only"),
        Constraint(RULE, "a partial submission is not accepted"),
        Constraint(RULE, "the reviewing body does not sit out of session"),
    ],
    boundary_a={"reviewers", "queue"},
    boundary_b={"reviewers", "queue"},
    depends_a={"reviewers"},
    depends_b={"queue"},
    horizon_a=Horizon(6, "month"), horizon_b=Horizon(6, "month"),
    deferred_costs=[],
)

CASE_I = dilemma(
    # Stated as a tradeoff and supplied as nothing else.
    statement="I stated, not structured",
    options=None, side_a=None, side_b=None, constraints=None,
)

CASE_X = dilemma(
    # Two artifacts at once, to show the return is a set and not a
    # winner: the cut runs through the shared crew AND the saving lands
    # past the near horizon on an asset the near ledger counts.
    statement="X both artifacts at once",
    options=[
        Option("defer and reassign", OBS, "the works programme"),
        Option("hold the schedule", OBS, "the works programme"),
    ],
    side_a="programme cost", side_b="condition and exposure",
    constraints=[
        Constraint(PHYS, "the material fatigues at a rate nobody sets"),
        Constraint(RULE, "the programme is approved annually"),
    ],
    boundary_a={"deck", "programme_line"},
    boundary_b={"crew", "deck"},
    depends_a={"crew", "deck"},
    depends_b={"crew", "deck"},
    horizon_a=Horizon(1, "year"), horizon_b=Horizon(25, "year"),
    deferred_costs=[
        DeferredCost("A", "deck", Horizon(7, "year")),
    ],
)

CASE_U = dilemma(
    # An UNSTATED constraint alongside a physical one. The order calls an
    # unstated constraint a defect that must not be smoothed over, and
    # the return enum has no member for it, so this reads as clean in
    # the flag set and carries the defect in the record.
    statement="U a defect the flags cannot say",
    options=[
        Option("route over the ridge", OBS, "the survey"),
        Option("route around the ridge", OBS, "the survey"),
    ],
    side_a="distance", side_b="grade",
    constraints=[
        Constraint(PHYS, "the ridge is where it is"),
        Constraint(UNST, "nothing given for why the valley route was dropped"),
    ],
    boundary_a={"corridor"},
    boundary_b={"corridor"},
    depends_a={"corridor"},
    depends_b={"corridor"},
    horizon_a=Horizon(1, "year"), horizon_b=Horizon(1, "year"),
    deferred_costs=[],
    conserved_quantity=None,
)

CASE_P = dilemma(
    # No option was observed and CHECK 1 is silent, because one option is
    # DERIVED and the rule as written requires every option to be
    # STIPULATED. The case that separates the two clauses of CHECK 1.
    statement="P stipulated with one derived",
    options=[
        Option("hold the line", STIP, "the person posing the problem"),
        Option("move the line", STIP, "the person posing the problem"),
        Option("the midpoint", DERV, "arithmetic on the two above"),
    ],
    side_a="one end", side_b="the other end",
    constraints=[
        Constraint(PHYS, "the span is fixed"),
    ],
    boundary_a={"span"}, boundary_b={"span"},
    depends_a={"span"}, depends_b={"span"},
    horizon_a=Horizon(1, "year"), horizon_b=Horizon(1, "year"),
    deferred_costs=[],
)

CASES = [CASE_T, CASE_M, CASE_B, CASE_G, CASE_R, CASE_I,
         CASE_X, CASE_U, CASE_P]
