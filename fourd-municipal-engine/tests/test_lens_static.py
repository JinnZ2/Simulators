"""Tests for the static FourDLens engine."""
from fourd_municipal_engine.lens.static import FourDLens

SAMPLE_TEXT = (
    "It was determined that the utilization of the aforementioned resources "
    "was commenced pursuant to the regulations. The implementation of the "
    "new policy is outstanding and amazing! Stakeholders were delighted. "
    "Studies indicate the optimization of the process may occur. NASA and "
    "the FBI issued statements..."
)


def test_static_lens_dimension_score_keys():
    sig = FourDLens().analyze(SAMPLE_TEXT)
    assert set(sig.dimension_scores) == {
        "D1_agency",
        "D2_affect",
        "D3_reality",
        "D4_iconic",
    }
    assert set(sig.normalized_scores) == set(sig.dimension_scores)
    assert set(sig.raw_counts) == set(sig.dimension_scores)


def test_static_lens_manipulation_index_bounds():
    sig = FourDLens().analyze(SAMPLE_TEXT)
    assert 0.0 <= sig.manipulation_index <= 1.0


def test_static_lens_trace_non_empty():
    sig = FourDLens().analyze(SAMPLE_TEXT)
    assert isinstance(sig.trace, list)
    assert len(sig.trace) > 0
    assert all(isinstance(entry, str) for entry in sig.trace)


def test_static_lens_normalized_scores_bounded():
    sig = FourDLens().analyze(SAMPLE_TEXT)
    for value in sig.normalized_scores.values():
        assert 0.0 <= value <= 1.0
