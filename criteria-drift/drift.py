"""
drift.py — Measure how fast the ruler moves.

Drift is computed pairwise between consecutive criteria versions.
Each field in the Declared Frame contributes a drift signal.
Composite drift is a weighted aggregation (weights are user-tunable).

Design principle: drift must be computable from the declared frame alone,
without looking at model scores. The ruler moves on its own axis.
"""
from typing import Dict, List, Tuple, Optional
from schema import CriteriaVersion, Frame, ACCESS_RANK
import math


class DriftMetrics:
    """Container for per-version and pairwise drift measurements."""

    def __init__(self, artifact_name: str):
        self.artifact = artifact_name
        self.pairs: List[Dict] = []   # one entry per consecutive pair

    def add_pair(self, older: CriteriaVersion, newer: CriteriaVersion,
                 metrics: Dict[str, float]):
        self.pairs.append({
            "from_version": older.version_id,
            "to_version": newer.version_id,
            "from_time": older.timestamp,
            "to_time": newer.timestamp,
            "metrics": metrics,
            "composite_drift": metrics.get("composite", 0.0),
        })

    def to_dict(self) -> Dict:
        return {
            "artifact": self.artifact,
            "pair_count": len(self.pairs),
            "pairs": self.pairs,
        }


class DriftEngine:
    """
    Computes drift between CriteriaVersion snapshots.

    Weights control the composite. Default is equal weighting across
    the six frame fields plus rubric dimensions.
    """

    DEFAULT_WEIGHTS = {
        "boundary": 1.0,
        "horizon": 1.0,
        "who_counts": 1.0,
        "sign_source": 1.0,
        "logic": 1.0,
        "observer_access": 1.0,
        "rubric_dimensions": 1.0,
        "rubric_weights": 1.0,
        "exemplar_count": 0.5,
    }

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or dict(self.DEFAULT_WEIGHTS)

    def compute_history(self, versions: List[CriteriaVersion]) -> DriftMetrics:
        if len(versions) < 2:
            return DriftMetrics(versions[0].artifact_name if versions else "")
        metrics = DriftMetrics(versions[0].artifact_name)
        for i in range(1, len(versions)):
            pair_metrics = self.compute_pair(versions[i - 1], versions[i])
            metrics.add_pair(versions[i - 1], versions[i], pair_metrics)
        return metrics

    def compute_pair(self, a: CriteriaVersion, b: CriteriaVersion) -> Dict[str, float]:
        """Return a dict of drift metrics for one version transition."""
        m: Dict[str, float] = {}

        # --- Frame field drifts (string distance) ---------------------
        m["boundary"] = self._str_drift(a.frame.boundary, b.frame.boundary)
        m["horizon"] = self._str_drift(a.frame.horizon, b.frame.horizon)
        m["who_counts"] = self._str_drift(a.frame.who_counts, b.frame.who_counts)
        m["sign_source"] = self._str_drift(a.frame.sign_source, b.frame.sign_source)
        m["logic"] = self._str_drift(a.frame.logic, b.frame.logic)
        m["observer_access"] = self._str_drift(a.frame.observer_access, b.frame.observer_access)

        # --- Rubric drift ---------------------------------------------
        m["rubric_dimensions"] = self._list_drift(
            a.rubric_dimensions or [], b.rubric_dimensions or [])
        m["rubric_weights"] = self._dict_drift(
            a.rubric_weights or {}, b.rubric_weights or {})
        m["exemplar_count"] = self._numeric_drift(
            a.exemplar_count, b.exemplar_count)

        # --- Signed drift ---------------------------------------------
        # CD_002: every metric above is a non-negative DISTANCE, and the
        # decision rule reads the SIGN of a slope on it. Widening and
        # narrowing both pushed composite up. These carry direction where
        # direction exists, and stay at 0.0 where it does not -- an
        # undeclared direction is not a lateral one.
        signed = {}
        signed["exemplar_count"] = self._signed_numeric(
            a.exemplar_count, b.exemplar_count)
        signed["observer_access"] = self._signed_ordinal(
            a.frame.observer_access, b.frame.observer_access)
        signed["rubric_dimensions"] = self._signed_list(
            a.rubric_dimensions or [], b.rubric_dimensions or [])
        signed["rubric_weights"] = self._signed_dict(
            a.rubric_weights or {}, b.rubric_weights or {})
        for field in ("boundary", "horizon", "who_counts"):
            signed[field] = self._declared_direction(b, field, m[field])
        for field in ("sign_source", "logic"):
            # No natural direction. Saying so is worth more than forcing one.
            signed[field] = 0.0
        for k, v in signed.items():
            m["signed_" + k] = v

        # --- Composite -----------------------------------------------
        total_weight = 0.0
        weighted_sum = 0.0
        for key, weight in self.weights.items():
            if key in m:
                weighted_sum += m[key] * weight
                total_weight += weight
        m["composite"] = weighted_sum / total_weight if total_weight > 0 else 0.0

        # Signed composite over the same weights. Reported alongside, never
        # instead of -- a caller that wants magnitude still has it.
        sw_sum = 0.0
        sw_total = 0.0
        for key, weight in self.weights.items():
            sk = "signed_" + key
            if sk in m:
                sw_sum += m[sk] * weight
                sw_total += weight
        m["composite_signed"] = sw_sum / sw_total if sw_total > 0 else 0.0

        # How much of the composite carries a direction at all. A caller
        # reading composite_signed without this cannot tell "no net change"
        # from "no direction declared".
        signable = sum(w for k, w in self.weights.items()
                       if ("signed_" + k) in m and m["signed_" + k] != 0.0)
        m["signed_coverage"] = signable / total_weight if total_weight else 0.0

        return m

    # ------------------------------------------------------------------
    # Primitive drift functions
    # ------------------------------------------------------------------
    @staticmethod
    def _str_drift(s1: str, s2: str) -> float:
        """Normalized Levenshtein-like distance (simplified)."""
        if s1 == s2:
            return 0.0
        max_len = max(len(s1), len(s2), 1)
        # Simple token-jaccard as proxy for semantic drift
        t1 = set(s1.lower().split())
        t2 = set(s2.lower().split())
        inter = len(t1 & t2)
        union = len(t1 | t2)
        if union == 0:
            return 0.0
        return 1.0 - (inter / union)

    @staticmethod
    def _list_drift(l1: List[str], l2: List[str]) -> float:
        s1 = set(x.lower().strip() for x in l1)
        s2 = set(x.lower().strip() for x in l2)
        inter = len(s1 & s2)
        union = len(s1 | s2)
        if union == 0:
            return 0.0
        return 1.0 - (inter / union)

    @staticmethod
    def _dict_drift(d1: Dict, d2: Dict) -> float:
        keys = set(d1.keys()) | set(d2.keys())
        if not keys:
            return 0.0
        diffs = 0
        for k in keys:
            v1 = d1.get(k)
            v2 = d2.get(k)
            if v1 != v2:
                diffs += 1
        return diffs / len(keys)

    # ------------------------------------------------------------------
    # Signed primitives. Range [-1, 1]. Positive = the criteria got
    # LOOSER / WIDER / more inclusive; negative = stricter / narrower.
    # ------------------------------------------------------------------
    @staticmethod
    def _signed_numeric(v1: Optional[int], v2: Optional[int]) -> float:
        """Same as _numeric_drift without the abs(). One character."""
        if v1 is None or v2 is None or v1 == v2:
            return 0.0
        base = max(abs(v1), abs(v2), 1)
        return max(-1.0, min((v2 - v1) / base, 1.0))

    @staticmethod
    def _signed_ordinal(s1: str, s2: str) -> float:
        """observer_access is ordered. Rank it instead of string-matching."""
        r1 = ACCESS_RANK.get(str(s1).strip().lower())
        r2 = ACCESS_RANK.get(str(s2).strip().lower())
        if r1 is None or r2 is None:
            return 0.0
        span = max(ACCESS_RANK.values()) - min(ACCESS_RANK.values())
        # Negative = verification LOST, which is a loosening of the check.
        return (r2 - r1) / span if span else 0.0

    @staticmethod
    def _signed_list(l1: List[str], l2: List[str]) -> float:
        """|added| - |removed| over the union. Dimensions gained = wider."""
        s1 = set(x.lower().strip() for x in l1)
        s2 = set(x.lower().strip() for x in l2)
        union = s1 | s2
        if not union:
            return 0.0
        return (len(s2 - s1) - len(s1 - s2)) / len(union)

    @staticmethod
    def _signed_dict(d1: Dict, d2: Dict) -> float:
        """Sum of signed weight changes, normalized by total weight moved."""
        keys = set(d1) | set(d2)
        if not keys:
            return 0.0
        deltas = []
        for k in keys:
            try:
                deltas.append(float(d2.get(k, 0.0)) - float(d1.get(k, 0.0)))
            except (TypeError, ValueError):
                return 0.0
        moved = sum(abs(x) for x in deltas)
        if moved == 0.0:
            return 0.0
        return max(-1.0, min(sum(deltas) / moved, 1.0))

    @staticmethod
    def _declared_direction(newer: CriteriaVersion, field: str,
                            magnitude: float) -> float:
        """
        Free-text fields carry no recoverable direction. The sign has to be
        DECLARED by whoever made the version. Undeclared stays 0.0 -- not
        because nothing changed, but because nobody said which way.
        """
        d = (newer.direction or {}).get(field, "unknown")
        if d == "widened":
            return magnitude
        if d == "narrowed":
            return -magnitude
        return 0.0

    @staticmethod
    def _numeric_drift(v1: Optional[int], v2: Optional[int]) -> float:
        if v1 is None and v2 is None:
            return 0.0
        if v1 is None or v2 is None:
            return 1.0
        if v1 == v2:
            return 0.0
        # Relative change, capped at 1.0
        diff = abs(v2 - v1)
        base = max(abs(v1), abs(v2), 1)
        return min(diff / base, 1.0)
