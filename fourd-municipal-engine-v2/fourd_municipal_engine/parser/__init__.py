"""Parser subpackage: 4D ordinance metric extraction (optional deps guarded)."""

try:
    from fourd_municipal_engine.parser.schemas import (
        DensityMetricsModel,
        DesignMetricsModel,
        DelayMetricsModel,
        DollarMetricsModel,
        FourDOrdinanceMetricsSchema,
    )
    from fourd_municipal_engine.parser.ordinance_parser import Ordinance4DParser
except ImportError:  # pragma: no cover - pydantic not installed
    pass

__all__ = [
    "DensityMetricsModel",
    "DesignMetricsModel",
    "DelayMetricsModel",
    "DollarMetricsModel",
    "FourDOrdinanceMetricsSchema",
    "Ordinance4DParser",
]
