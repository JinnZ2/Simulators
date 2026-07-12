"""All audits, in one list. Six built; ten frontier stubs pattern-follows."""

from .phase_change import PhaseChangeAudit
from .stationarity import StationarityAudit
from .missing_feedback import MissingFeedbackAudit
from .omitted_variable import OmittedVariableAudit
from .data_aggregation import DataAggregationAudit
from .cascade_speed import CascadeSpeedAudit
from .frontier_stubs import (
    MissingPositiveFeedbackAudit,
    ThresholdSmoothingAudit,
    TemporalAggregationExtremesAudit,
    SpatialHomogenizationAudit,
    MemoryAmnesiaAudit,
    CrossSystemCouplingAudit,
    BufferExhaustionAudit,
    ClusteredExtremesAudit,
    GaussianBlindnessAudit,
    IncentiveBiasAudit,
)

BUILT_AUDITS = [
    PhaseChangeAudit(),
    StationarityAudit(),
    MissingFeedbackAudit(),
    OmittedVariableAudit(),
    DataAggregationAudit(),
    CascadeSpeedAudit(),
]

FRONTIER_AUDITS = [
    MissingPositiveFeedbackAudit(),
    ThresholdSmoothingAudit(),
    TemporalAggregationExtremesAudit(),
    SpatialHomogenizationAudit(),
    MemoryAmnesiaAudit(),
    CrossSystemCouplingAudit(),
    BufferExhaustionAudit(),
    ClusteredExtremesAudit(),
    GaussianBlindnessAudit(),
    IncentiveBiasAudit(),
]

ALL_AUDITS = BUILT_AUDITS + FRONTIER_AUDITS
