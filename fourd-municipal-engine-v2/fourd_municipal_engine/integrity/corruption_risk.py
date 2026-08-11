"""
Corruption Risk Index (CRI) Engine — STDLIB ONLY.

Computes the Corruption Risk Index (CRI) scaled from 0 to 100:
  CRI = 0.35 * S_temporal + 0.25 * S_magnitude + 0.20 * S_network + 0.20 * S_recusal
"""

from typing import Dict, Any, Optional


class CorruptionRiskCalculator:
    """
    Computes the Corruption Risk Index (CRI) scaled from 0 to 100.

    Formula:
      CRI = 0.35 * S_temporal + 0.25 * S_magnitude + 0.20 * S_network + 0.20 * S_recusal
    """
    WEIGHT_TEMPORAL = 0.35
    WEIGHT_MAGNITUDE = 0.25
    WEIGHT_NETWORK = 0.20
    WEIGHT_RECUSAL = 0.20

    @classmethod
    def compute_temporal_score(cls, days_to_vote: Optional[int]) -> float:
        """Calculates temporal proximity subscore (0 - 100)."""
        if days_to_vote is None:
            return 0.0
        abs_days = abs(days_to_vote)
        if abs_days <= 14:
            return 100.0
        elif abs_days <= 30:
            return 85.0
        elif abs_days <= 60:
            return 60.0
        elif abs_days <= 90:
            return 40.0
        elif abs_days <= 180:
            return 15.0
        return 0.0

    @classmethod
    def compute_magnitude_score(
        cls,
        base_far: float,
        requested_far: float,
        base_height: float,
        requested_height: float
    ) -> float:
        """Calculates variance magnitude subscore (0 - 100)."""
        far_pct = ((requested_far - base_far) / base_far * 100) if base_far > 0 else 0.0
        height_pct = ((requested_height - base_height) / base_height * 100) if base_height > 0 else 0.0

        max_pct_increase = max(far_pct, height_pct)
        if max_pct_increase <= 0:
            return 0.0
        # Cap at 300% zoning expansion = 100 subscore
        return min(100.0, (max_pct_increase / 300.0) * 100.0)

    @classmethod
    def compute_network_score(cls, developer_funding_share_pct: float) -> float:
        """Calculates network density subscore (0 - 100)."""
        if developer_funding_share_pct <= 0:
            return 0.0
        # Cap at 20% of official's total campaign budget = 100 subscore
        return min(100.0, (developer_funding_share_pct / 20.0) * 100.0)

    @classmethod
    def compute_recusal_score(
        cls,
        voted_yes: bool,
        has_contribution: bool,
        recusal_filed: bool
    ) -> float:
        """Calculates recusal failure subscore (0 - 100)."""
        if has_contribution and voted_yes and not recusal_filed:
            return 100.0
        return 0.0

    @classmethod
    def calculate_cri(
        cls,
        days_to_vote: Optional[int],
        base_far: float,
        requested_far: float,
        base_height: float,
        requested_height: float,
        developer_funding_share_pct: float,
        voted_yes: bool,
        has_contribution: bool,
        recusal_filed: bool
    ) -> Dict[str, Any]:
        """Calculates the weighted Corruption Risk Index."""
        s_temp = cls.compute_temporal_score(days_to_vote)
        s_mag = cls.compute_magnitude_score(base_far, requested_far, base_height, requested_height)
        s_net = cls.compute_network_score(developer_funding_share_pct)
        s_rec = cls.compute_recusal_score(voted_yes, has_contribution, recusal_filed)

        cri_float = (
            (cls.WEIGHT_TEMPORAL * s_temp) +
            (cls.WEIGHT_MAGNITUDE * s_mag) +
            (cls.WEIGHT_NETWORK * s_net) +
            (cls.WEIGHT_RECUSAL * s_rec)
        )
        cri_int = max(0, min(100, int(round(cri_float))))

        return {
            "corruption_risk_index": cri_int,
            "subscores": {
                "temporal": s_temp,
                "magnitude": s_mag,
                "network": s_net,
                "recusal": s_rec
            }
        }
