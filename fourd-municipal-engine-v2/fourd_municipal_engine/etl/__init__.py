"""ETL subpackage: PostGIS persistence for 4D municipal data (optional deps guarded)."""

try:
    from fourd_municipal_engine.etl.models import (
        Base,
        Jurisdiction,
        ZoningDistrict,
        CodeSection,
        Code4DMetrics,
        CodeZoningJunction,
    )
    from fourd_municipal_engine.etl.pipeline import Municipal4DETLPipeline
    from fourd_municipal_engine.etl.batch import BatchOrdinanceIngestor
except ImportError:  # pragma: no cover - sqlalchemy/geoalchemy2 not installed
    pass

__all__ = [
    "Base",
    "Jurisdiction",
    "ZoningDistrict",
    "CodeSection",
    "Code4DMetrics",
    "CodeZoningJunction",
    "Municipal4DETLPipeline",
    "BatchOrdinanceIngestor",
]
