"""Tests for the genre-calibrated DynamicFourDLens engine."""
from fourd_municipal_engine.lens.dynamic import DynamicFourDLens
from fourd_municipal_engine.models.vectors import Genre

# Ambiguous phrase: "critical" reads as a mechanical state in a technical
# report but as an emotional injector in corporate PR.
AMBIGUOUS_PHRASE = (
    "The critical failure threshold was exceeded and the system was "
    "terminated. It is urgent that the optimization process be executed."
)


def test_genre_changes_manipulation_index():
    lens = DynamicFourDLens()
    tech = lens.analyze(AMBIGUOUS_PHRASE, genre=Genre.TECHNICAL_REPORT)
    pr = lens.analyze(AMBIGUOUS_PHRASE, genre=Genre.CORPORATE_PR)
    assert tech.genre_applied != pr.genre_applied
    assert tech.manipulation_index != pr.manipulation_index


def test_genre_dampening_direction_pr_higher_than_technical():
    lens = DynamicFourDLens()
    tech = lens.analyze(AMBIGUOUS_PHRASE, genre=Genre.TECHNICAL_REPORT)
    pr = lens.analyze(AMBIGUOUS_PHRASE, genre=Genre.CORPORATE_PR)
    # Corporate PR penalizes urgency/euphemism more heavily than a
    # technical report, where such terms are benign mechanical states.
    assert pr.manipulation_index >= tech.manipulation_index


def test_dynamic_signature_fields():
    lens = DynamicFourDLens(default_genre=Genre.LEGAL_CONTRACT)
    sig = lens.analyze(AMBIGUOUS_PHRASE)
    assert sig.genre_applied == "Legal Contract / Statute"
    assert set(sig.dimension_scores) == {
        "D1_agency",
        "D2_affect",
        "D3_reality",
        "D4_iconic",
    }
    assert 0.0 <= sig.manipulation_index <= 1.0
    assert sig.trace
