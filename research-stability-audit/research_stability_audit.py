#!/usr/bin/env python3
"""
research_stability_audit.py

Framework for testing claims about research stability and AI model
degradation through falsifiable, measurable hypotheses.

Not: "here's what we know"
But: "here's how to test what we claim to know"

Provides:
- ResearchClaim: a falsifiable claim with measurement method, threshold,
  time window, and cascade-risk threshold
- ResearchStabilityAudit: registers claims, detects bifurcation, scores
  cascade risk, exports CLAIM_TABLE.json
- ResearchPaper / ResearchDataset: light data structures for computing
  retraction, reproducibility, citation half-life from real records
- build_research_degradation_claims(): six preset claims sourced from
  documented reproducibility and model-drift literature

Cross-reference: emergence-stability-simulator demonstrates the same
structural pattern at the agent level — grounded baselines damp cascade,
ungrounded baselines amplify it. Failed-research and degraded-AI-model
dynamics are instances of the same physics.

License: CC0
Dependencies: Python stdlib only
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


# ============================================================
# CLAIM STRUCTURE
# ============================================================

class ResearchClaim:
    """A falsifiable claim about research stability or AI degradation."""

    def __init__(
        self,
        claim_id: str,
        hypothesis: str,
        measurement_method: str,
        threshold: float,
        time_window_days: int,
        cascade_risk_threshold: float = 0.5,
    ):
        self.claim_id = claim_id
        self.hypothesis = hypothesis
        self.measurement_method = measurement_method
        self.threshold = threshold
        self.time_window_days = time_window_days
        self.cascade_risk_threshold = cascade_risk_threshold

        # Filled in when the claim is measured
        self.measured_value: Optional[float] = None
        self.confidence: float = 0.0
        self.is_falsified: bool = False
        self.bifurcation_detected: bool = False
        self.test_date: Optional[str] = None
        self.notes: str = ''
        self.sources: List[str] = []

    def set_measurement(self, value: float, confidence: float = 1.0,
                        test_date: Optional[str] = None) -> None:
        """Record a measurement and update derived flags."""
        self.measured_value = value
        self.confidence = confidence
        self.test_date = test_date or datetime.utcnow().isoformat()
        # Claim is falsified if the measurement contradicts the hypothesis.
        # Claims here are written as "X exceeds threshold T"; falsified when
        # measured value falls below T.
        self.is_falsified = value < self.threshold
        self.bifurcation_detected = value >= self.cascade_risk_threshold

    def to_dict(self) -> Dict:
        return {
            'claim_id': self.claim_id,
            'hypothesis': self.hypothesis,
            'measurement_method': self.measurement_method,
            'threshold': self.threshold,
            'time_window_days': self.time_window_days,
            'cascade_risk_threshold': self.cascade_risk_threshold,
            # Derived from threshold so schema validators see an explicit
            # falsifiability statement.
            'falsification_criteria': (
                f'measured_value < {self.threshold} '
                f'over a {self.time_window_days}-day window'
            ),
            'measured_value': self.measured_value,
            'confidence': self.confidence,
            'is_falsified': self.is_falsified,
            'bifurcation_detected': self.bifurcation_detected,
            'test_date': self.test_date,
            'notes': self.notes,
            'sources': self.sources,
            'cascade_risk_score': (self.measured_value or 0.0) * self.confidence,
        }


# ============================================================
# AUDIT FRAMEWORK
# ============================================================

class ResearchStabilityAudit:
    """
    Aggregates claims, detects bifurcation, assesses cascade risk.

    Bifurcation here means: the system's claims are splitting into
    measurable-and-failing vs measurable-and-irreversible groups, which
    indicates the audited domain is decoupling its substrate (what is
    actually true) from its narrative (what is taught / cited / trained on).
    """

    def __init__(self, audit_id: str = "RSA_001"):
        self.audit_id = audit_id
        self.claims: List[ResearchClaim] = []
        self.cascade_detected: bool = False
        self.bifurcation_onset_risk: float = 0.0
        self.audit_timestamp = datetime.utcnow().isoformat()

    def add_claim(self, claim: ResearchClaim) -> None:
        self.claims.append(claim)

    def detect_bifurcation(self) -> Dict:
        total = len(self.claims)
        if total == 0:
            return {'bifurcation_detected': False, 'reason': 'no_claims_tested'}

        falsified = sum(1 for c in self.claims if c.is_falsified)
        bifurc = sum(1 for c in self.claims if c.bifurcation_detected)

        bifurcation_rate = bifurc / total
        falsification_rate = falsified / total

        is_bifurcating = bifurcation_rate > 0.5 or falsification_rate > 0.7
        self.bifurcation_onset_risk = max(bifurcation_rate, falsification_rate)
        self.cascade_detected = is_bifurcating

        return {
            'bifurcation_detected': is_bifurcating,
            'bifurcation_onset_risk': self.bifurcation_onset_risk,
            'bifurcation_rate': bifurcation_rate,
            'falsification_rate': falsification_rate,
            'claims_tested': total,
            'claims_falsified': falsified,
            'claims_bifurcating': bifurc,
        }

    def cascade_risk_assessment(self) -> Dict:
        base_risk = self.bifurcation_onset_risk
        total = max(len(self.claims), 1)
        high_falsification_rate = sum(1 for c in self.claims if c.is_falsified) / total

        # Propagation speed: faster failure → higher risk
        propagation_scores: List[float] = []
        for c in self.claims:
            if c.is_falsified:
                days = max(c.time_window_days, 1)
                propagation_scores.append(1.0 / days)
        avg_propagation_speed = (
            sum(propagation_scores) / len(propagation_scores)
            if propagation_scores else 0.0
        )

        # Substrate separation: how many claims explicitly target the
        # substrate-vs-narrative split
        sub_keywords = ('bifurcation', 'separation', 'substrate', 'narrative')
        sub_claims = [
            c for c in self.claims
            if any(k in c.claim_id.lower() or k in c.hypothesis.lower()
                   for k in sub_keywords)
        ]
        substrate_separation = len(sub_claims) / total

        cascade_risk = (
            base_risk * 0.4
            + high_falsification_rate * 0.3
            + avg_propagation_speed * 0.2
            + substrate_separation * 0.1
        )

        return {
            'cascade_risk_score': cascade_risk,
            'risk_level': self._risk_level(cascade_risk),
            'bifurcation_risk': base_risk,
            'falsification_risk': high_falsification_rate,
            'propagation_speed': avg_propagation_speed,
            'substrate_separation_degree': substrate_separation,
            'recommendation': self._cascade_recommendation(cascade_risk),
        }

    @staticmethod
    def _risk_level(score: float) -> str:
        if score < 0.2:
            return 'LOW'
        if score < 0.4:
            return 'MODERATE'
        if score < 0.6:
            return 'HIGH'
        if score < 0.8:
            return 'CRITICAL'
        return 'CASCADE_IMMINENT'

    @staticmethod
    def _cascade_recommendation(score: float) -> str:
        if score < 0.3:
            return 'monitor: collect more data'
        if score < 0.5:
            return 'alert: implement falsifiability checks'
        if score < 0.7:
            return 'action: distribute substrate knowledge now'
        return 'emergency: bifurcation already occurring'

    def to_dict(self) -> Dict:
        bif = self.detect_bifurcation()
        cas = self.cascade_risk_assessment()
        return {
            'schema_version': '1.0',
            'source_repo': 'research-stability-audit',
            'audit_id': self.audit_id,
            'timestamp': self.audit_timestamp,
            'total_claims': len(self.claims),
            'claims': [c.to_dict() for c in self.claims],
            'bifurcation_analysis': bif,
            'cascade_risk_assessment': cas,
        }

    def write_claim_table(self, path: str = 'CLAIM_TABLE.json') -> None:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


# ============================================================
# DATA STRUCTURES (for analyzing real records)
# ============================================================

class ResearchPaper:
    """One published research paper, with the fields needed for stability stats."""

    def __init__(
        self,
        paper_id: str,
        title: str,
        publish_date: str,                          # ISO-8601
        field: str,
        retracted: bool = False,
        retraction_date: Optional[str] = None,
        reproducible: Optional[bool] = None,
        citations_over_time: Optional[Dict[int, int]] = None,
        methodology_explicitness: float = 0.0,
    ):
        self.paper_id = paper_id
        self.title = title
        self.publish_date = publish_date
        self.field = field
        self.retracted = retracted
        self.retraction_date = retraction_date
        self.reproducible = reproducible
        self.citations_over_time = citations_over_time or {}
        self.methodology_explicitness = methodology_explicitness

    def time_to_retraction_years(self) -> Optional[float]:
        if not self.retracted or not self.retraction_date:
            return None
        return int(self.retraction_date[:4]) - int(self.publish_date[:4])

    def is_failed_reproduction(self) -> bool:
        return self.reproducible is False

    def citation_half_life(self) -> Optional[float]:
        if not self.citations_over_time:
            return None
        years = sorted(self.citations_over_time.keys())
        peak = max(self.citations_over_time.values())
        if peak <= 0:
            return None
        threshold = peak / 2.0
        for y in years:
            if self.citations_over_time[y] < threshold:
                return float(y - years[0])
        return None


class ResearchDataset:
    """Aggregates papers and computes the statistics that feed claims."""

    def __init__(self, papers: List[ResearchPaper]):
        self.papers = papers

    def retraction_rate(self) -> float:
        if not self.papers:
            return 0.0
        return sum(1 for p in self.papers if p.retracted) / len(self.papers)

    def reproducibility_failure_rate(self) -> float:
        rated = [p for p in self.papers if p.reproducible is not None]
        if not rated:
            return 0.0
        return sum(1 for p in rated if p.is_failed_reproduction()) / len(rated)

    def average_time_to_retraction(self) -> Optional[float]:
        times = [p.time_to_retraction_years() for p in self.papers
                 if p.time_to_retraction_years() is not None]
        if not times:
            return None
        return sum(times) / len(times)

    def average_citation_half_life(self) -> Optional[float]:
        halves = [p.citation_half_life() for p in self.papers
                  if p.citation_half_life() is not None]
        if not halves:
            return None
        return sum(halves) / len(halves)

    def by_field(self) -> Dict[str, 'ResearchDataset']:
        grouped: Dict[str, List[ResearchPaper]] = {}
        for p in self.papers:
            grouped.setdefault(p.field, []).append(p)
        return {f: ResearchDataset(ps) for f, ps in grouped.items()}


# ============================================================
# PRESET CLAIMS
# ============================================================

def build_research_degradation_claims() -> List[ResearchClaim]:
    """Six preset claims sourced from documented reproducibility data."""
    claims: List[ResearchClaim] = []

    c = ResearchClaim(
        claim_id='RES_REPRO_001',
        hypothesis='Research reproducibility failure rate exceeds 50% in fast-moving fields',
        measurement_method='Attempt to replicate published studies; count failures',
        threshold=0.5,
        time_window_days=365,
        cascade_risk_threshold=0.6,
    )
    c.sources = [
        'Nature (2024): Half of social-science studies fail replication (3,900 papers)',
        "Nature survey: 70% of researchers failed to reproduce others' work; 50% own",
        'PNAS: psychology ~40% replicate (implying ~60% fail)',
    ]
    c.notes = ('Real failure rate is 40-60% but formal retraction is 0-5%. '
               'The gap is the bifurcation: corpus retains broken claims for years.')
    claims.append(c)

    c = ResearchClaim(
        claim_id='RES_RETLAG_001',
        hypothesis='Formal retractions lag failed replications by at least 2 years',
        measurement_method='Track time from first failed replication to formal retraction',
        threshold=2.0,
        time_window_days=1825,
        cascade_risk_threshold=0.7,
    )
    c.sources = [
        'Nature (2024): biomedical retractions quadrupled in 20 years',
        'Scholarly Kitchen: 51% of retractions from 34 journals (concentrated)',
    ]
    c.notes = 'Downstream work builds on false foundations during the lag.'
    claims.append(c)

    c = ResearchClaim(
        claim_id='RES_DECAY_001',
        hypothesis='Citation half-life in fast-moving fields is below 5 years',
        measurement_method='Compute citation half-life across 10 fields, correlate with innovation velocity',
        threshold=5.0,
        time_window_days=1825,
        cascade_risk_threshold=0.65,
    )
    c.sources = [
        'LIS Academy: fast-moving fields (AI, medicine) have 3-5yr half-life',
        'ACM: computing research shows wide variation by subfield',
    ]
    c.notes = 'Conservative estimate; AI subfields are closer to 2-3 years.'
    claims.append(c)

    c = ResearchClaim(
        claim_id='AI_DEGRAD_001',
        hypothesis='91% or more of ML models degrade within one year of deployment',
        measurement_method='Deploy N models, track accuracy over time, count those that degrade',
        threshold=0.91,
        time_window_days=30,
        cascade_risk_threshold=0.8,
    )
    c.sources = [
        'Nature (2025): 91% of ML models degrade over time',
        'IBM / Splunk: concept drift occurs in weeks to months',
    ]
    c.notes = ('AI model obsolescence is FASTER than research-paper obsolescence; '
               'training AI on AI accelerates the cycle.')
    claims.append(c)

    c = ResearchClaim(
        claim_id='BIF_ONSET_001',
        hypothesis='Substrate knowledge transmission collapses when adoption falls below 50% per generation',
        measurement_method='Survey practitioner cohorts; measure rate of knowledge handoff',
        threshold=0.5,
        time_window_days=1095,
        cascade_risk_threshold=0.75,
    )
    c.sources = [
        'Anthropological observation: skilled-trade knowledge loss in <1 generation',
        'Historical precedent: Roman concrete, Damascus steel, agricultural varieties',
    ]
    c.notes = 'Once broken, recovery requires more than one generation.'
    claims.append(c)

    c = ResearchClaim(
        claim_id='CASCADE_METHOD_001',
        hypothesis='Falsifiable-methodology corpora replicate at higher rate than narrative-conclusion corpora',
        measurement_method='Compare replication rates of registered/methodology-explicit papers vs narrative-only papers',
        threshold=0.5,
        time_window_days=1095,
        cascade_risk_threshold=0.6,
    )
    c.sources = [
        'Pre-registration studies: registered reports show higher replication rate',
        'Cross-reference: emergence-stability-simulator EMRG_001..EMRG_006',
    ]
    c.notes = ('Same physics as emergence-stability-simulator: grounded baselines '
               'damp cascade, narrative baselines amplify. CC0 corpora that embed '
               'falsifiable claims behave like physics-grounded agents.')
    claims.append(c)

    return claims


# ============================================================
# CROSS-REFERENCE TO emergence-stability-simulator
# ============================================================

CROSS_REFERENCES = {
    'AI_DEGRAD_001': {
        'maps_to': ['EMRG_003', 'EMRG_004'],
        'principle': (
            'AI model degradation is cascade amplification at the model level. '
            'A trained model without continued grounding behaves like a parasitic '
            'agent: total_pressure (data drift) is absorbed and amplified rather '
            'than damped by physics_baseline.'
        ),
    },
    'RES_REPRO_001': {
        'maps_to': ['EMRG_001', 'EMRG_002'],
        'principle': (
            'Reproducibility failure is drift from baseline at the field level. '
            'Fields with strong physics grounding (math, classical physics) show '
            'lower drift; fields driven by engagement metrics (citations, novelty) '
            'show higher drift.'
        ),
    },
    'BIF_ONSET_001': {
        'maps_to': ['EMRG_005', 'EMRG_006'],
        'principle': (
            'A grounded minority can dominate dynamics when coupled to a parasitic '
            'majority — but only if the coupling and the minority size pass the '
            'attractor threshold identified in EMRG_006.'
        ),
    },
    'CASCADE_METHOD_001': {
        'maps_to': ['EMRG_001', 'EMRG_006'],
        'principle': (
            'Methodology-explicit research is the field-level analog of the '
            'physics baseline. The same falsifiability that lets the simulator '
            'damp cascade lets a corpus damp narrative drift.'
        ),
    },
}


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    print("=" * 60)
    print("RESEARCH STABILITY AUDIT")
    print("=" * 60)

    audit = ResearchStabilityAudit(audit_id='RSA_001')
    for claim in build_research_degradation_claims():
        audit.add_claim(claim)

    audit.write_claim_table('CLAIM_TABLE.json')
    print(f"Registered {len(audit.claims)} falsifiable claims")
    print(f"Wrote CLAIM_TABLE.json (no measurements yet)")

    # Cross-reference manifest
    Path('CROSS_REFERENCES.json').write_text(
        json.dumps({
            'source_repo': 'research-stability-audit',
            'target_repo': 'emergence-stability-simulator',
            'mappings': CROSS_REFERENCES,
        }, indent=2)
    )
    print(f"Wrote CROSS_REFERENCES.json ({len(CROSS_REFERENCES)} mappings)")

    print("\nClaims registered:")
    for c in audit.claims:
        print(f"  {c.claim_id}: {c.hypothesis[:70]}")


if __name__ == "__main__":
    main()
