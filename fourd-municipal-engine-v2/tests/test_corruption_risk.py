"""Corruption Risk Index (CRI) test suite — ported from the source unittest suite."""

import pytest

from fourd_municipal_engine.integrity import CorruptionRiskCalculator


def test_clean_baseline_project():
    """Clean project: No contributions, standard variance, clean vote -> CRI = 0."""
    res = CorruptionRiskCalculator.calculate_cri(
        days_to_vote=None,
        base_far=1.0, requested_far=1.0,
        base_height=35.0, requested_height=35.0,
        developer_funding_share_pct=0.0,
        voted_yes=True,
        has_contribution=False,
        recusal_filed=False
    )
    assert res["corruption_risk_index"] == 0
    assert res["subscores"]["temporal"] == 0.0
    assert res["subscores"]["magnitude"] == 0.0


def test_temporal_decay_proximity():
    """Immediate pre-vote donation vs 1-year prior donation."""
    recent_res = CorruptionRiskCalculator.calculate_cri(
        days_to_vote=5,
        base_far=1.0, requested_far=1.0,
        base_height=35.0, requested_height=35.0,
        developer_funding_share_pct=0.0,
        voted_yes=False, has_contribution=True, recusal_filed=False
    )
    old_res = CorruptionRiskCalculator.calculate_cri(
        days_to_vote=365,
        base_far=1.0, requested_far=1.0,
        base_height=35.0, requested_height=35.0,
        developer_funding_share_pct=0.0,
        voted_yes=False, has_contribution=True, recusal_filed=False
    )
    assert recent_res["subscores"]["temporal"] == 100.0
    assert old_res["subscores"]["temporal"] == 0.0
    assert recent_res["corruption_risk_index"] > old_res["corruption_risk_index"]


def test_post_vote_quid_pro_quo_timing():
    """Temporal proximity symmetrically handles post-vote donations (-10 days)."""
    post_vote_res = CorruptionRiskCalculator.calculate_cri(
        days_to_vote=-10,
        base_far=1.0, requested_far=1.0,
        base_height=35.0, requested_height=35.0,
        developer_funding_share_pct=0.0,
        voted_yes=True, has_contribution=True, recusal_filed=False
    )
    assert post_vote_res["subscores"]["temporal"] == 100.0


def test_flagrant_recusal_failure():
    """Contribution + YES vote without recusal -> recusal subscore = 100."""
    res = CorruptionRiskCalculator.calculate_cri(
        days_to_vote=10,
        base_far=1.0, requested_far=1.0,
        base_height=35.0, requested_height=35.0,
        developer_funding_share_pct=0.0,
        voted_yes=True,
        has_contribution=True,
        recusal_filed=False
    )
    assert res["subscores"]["recusal"] == 100.0


def test_proper_recusal_mitigation():
    """Contribution but recusal filed -> recusal subscore = 0."""
    res = CorruptionRiskCalculator.calculate_cri(
        days_to_vote=10,
        base_far=1.0, requested_far=1.0,
        base_height=35.0, requested_height=35.0,
        developer_funding_share_pct=0.0,
        voted_yes=False,
        has_contribution=True,
        recusal_filed=True
    )
    assert res["subscores"]["recusal"] == 0.0


def test_voted_no_with_contribution():
    """Received money but voted NO -> recusal subscore = 0."""
    res = CorruptionRiskCalculator.calculate_cri(
        days_to_vote=10,
        base_far=1.0, requested_far=1.0,
        base_height=35.0, requested_height=35.0,
        developer_funding_share_pct=0.0,
        voted_yes=False,
        has_contribution=True,
        recusal_filed=False
    )
    assert res["subscores"]["recusal"] == 0.0


def test_extreme_variance_magnitude_scaling():
    """300%+ FAR increase scales magnitude to 100; minor variance stays low."""
    minor_var = CorruptionRiskCalculator.calculate_cri(
        days_to_vote=None,
        base_far=1.0, requested_far=1.1,
        base_height=30.0, requested_height=30.0,
        developer_funding_share_pct=0.0, voted_yes=False,
        has_contribution=False, recusal_filed=False
    )
    extreme_var = CorruptionRiskCalculator.calculate_cri(
        days_to_vote=None,
        base_far=1.0, requested_far=4.0,
        base_height=30.0, requested_height=30.0,
        developer_funding_share_pct=0.0, voted_yes=False,
        has_contribution=False, recusal_filed=False
    )
    assert minor_var["subscores"]["magnitude"] == pytest.approx(3.33, abs=0.01)
    assert extreme_var["subscores"]["magnitude"] == 100.0


def test_downzoning_or_negative_variance():
    """Requested building smaller than allowed -> magnitude subscore = 0."""
    res = CorruptionRiskCalculator.calculate_cri(
        days_to_vote=None,
        base_far=2.0, requested_far=1.5,
        base_height=50.0, requested_height=40.0,
        developer_funding_share_pct=0.0, voted_yes=False,
        has_contribution=False, recusal_filed=False
    )
    assert res["subscores"]["magnitude"] == 0.0


def test_maximum_threat_scenario():
    """300% FAR, >20% funding share 5 days before vote, YES, no recusal -> CRI = 100."""
    res = CorruptionRiskCalculator.calculate_cri(
        days_to_vote=5,
        base_far=1.0, requested_far=4.0,
        base_height=30.0, requested_height=120.0,
        developer_funding_share_pct=25.0,
        voted_yes=True,
        has_contribution=True,
        recusal_filed=False
    )
    assert res["corruption_risk_index"] == 100
    assert res["subscores"]["temporal"] == 100.0
    assert res["subscores"]["magnitude"] == 100.0
    assert res["subscores"]["network"] == 100.0
    assert res["subscores"]["recusal"] == 100.0
