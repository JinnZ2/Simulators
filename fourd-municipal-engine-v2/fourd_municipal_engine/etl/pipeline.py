"""4D Municipal Code & GIS Data Ingestion Pipeline.

Ingests municipal GIS shapefiles and raw ordinance text into a
PostgreSQL/PostGIS database.
- Reprojects GIS geometries to WGS 84 (EPSG:4326)
- Population of bitemporal valid and system time ranges
- Ingestion of 4D policy metrics (Density, Design, Delay, Dollars)
- Automated mapping of code sections to zoning districts

Engine/session creation is lazy: this module imports cleanly without a
database connection (and the optional geopandas dependency is only required
when ``ingest_gis_shapefile`` is actually called).
"""
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fourd_municipal_engine.etl.models import (
    Code4DMetrics,
    CodeSection,
    CodeZoningJunction,
    Jurisdiction,
    ZoningDistrict,
)

logger = logging.getLogger("4D_ETL_Pipeline")

DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/municipal_4d")


def create_session_factory(db_url: Optional[str] = None):
    """Lazily build an engine + sessionmaker for the given DB URL."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(db_url or DB_URL, echo=False)
    return sessionmaker(bind=engine)


class Municipal4DETLPipeline:
    def __init__(self, db_session):
        self.session = db_session

    def get_or_create_jurisdiction(self, name: str, state_code: str, fips_code: str) -> uuid.UUID:
        """Retrieves an existing jurisdiction or creates a new entry."""
        jurisdiction = self.session.query(Jurisdiction).filter_by(fips_code=fips_code).first()
        if not jurisdiction:
            jurisdiction = Jurisdiction(
                jurisdiction_id=uuid.uuid4(),
                name=name,
                state_code=state_code,
                fips_code=fips_code,
            )
            self.session.add(jurisdiction)
            self.session.commit()
            logger.info(f"Created jurisdiction record: {name} ({fips_code})")
        return jurisdiction.jurisdiction_id

    def ingest_gis_shapefile(
        self,
        shapefile_path: str,
        jurisdiction_id: uuid.UUID,
        code_col: str,
        name_col: str,
        valid_from: Optional[datetime] = None,
    ) -> Dict[str, uuid.UUID]:
        """
        Reads a GIS shapefile, normalizes spatial projection to EPSG:4326,
        and loads records into the zoning_districts table with bitemporal ranges.
        """
        try:
            import geopandas as gpd
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "geopandas is required for GIS ingestion. "
                "Install with `pip install fourd-municipal-engine[db]`."
            ) from exc
        from psycopg2.extras import DateTimeTZRange

        logger.info(f"Loading GIS Shapefile from {shapefile_path}...")
        gdf = gpd.read_file(shapefile_path)

        # Reproject to EPSG:4326 if necessary
        if gdf.crs and gdf.crs.to_epsg() != 4326:
            logger.info(f"Reprojecting geometry from EPSG:{gdf.crs.to_epsg()} to EPSG:4326...")
            gdf = gdf.to_crs(epsg=4326)

        # Normalize geometries to MultiPolygon
        gdf["geometry"] = gdf["geometry"].apply(
            lambda geom: geom if geom.geom_type == "MultiPolygon" else [geom]
        )

        now = datetime.now(timezone.utc)
        valid_start = valid_from or now
        valid_range = DateTimeTZRange(valid_start, None, bounds="[)")
        system_range = DateTimeTZRange(now, None, bounds="[)")

        district_mapping = {}

        for _, row in gdf.iterrows():
            district_id = uuid.uuid4()
            d_code = str(row[code_col]).strip()
            d_name = str(row[name_col]).strip()

            zoning_entry = ZoningDistrict(
                zoning_district_id=district_id,
                jurisdiction_id=jurisdiction_id,
                district_code=d_code,
                district_name=d_name,
                boundary=f"SRID=4326;{row['geometry'].wkt}",
                valid_period=valid_range,
                system_period=system_range,
            )
            self.session.add(zoning_entry)
            district_mapping[d_code] = district_id

        self.session.commit()
        logger.info(f"Successfully ingested {len(district_mapping)} zoning district geometries.")
        return district_mapping

    def ingest_ordinance_with_4d_metrics(
        self,
        jurisdiction_id: uuid.UUID,
        section_data: Dict[str, Any],
        metrics_data: Dict[str, Any],
        target_zoning_codes: List[str],
        district_mapping: Dict[str, uuid.UUID],
        valid_from: Optional[datetime] = None,
    ) -> uuid.UUID:
        """
        Ingests legal code sections, extracts 4D metrics, and links them to relevant zoning districts.
        """
        from psycopg2.extras import DateTimeTZRange

        now = datetime.now(timezone.utc)
        valid_range = DateTimeTZRange(valid_from or now, None, bounds="[)")
        system_range = DateTimeTZRange(now, None, bounds="[)")

        section_id = uuid.uuid4()

        # 1. Insert Legal Code Section
        code_section = CodeSection(
            section_id=section_id,
            jurisdiction_id=jurisdiction_id,
            section_citation=section_data["citation"],
            title=section_data["title"],
            raw_text=section_data["raw_text"],
            plain_english_summary=section_data.get("summary"),
            valid_period=valid_range,
            system_period=system_range,
        )
        self.session.add(code_section)

        # 2. Insert 4D Metrics (Density, Design, Delay, Dollars)
        metrics = Code4DMetrics(
            metric_id=uuid.uuid4(),
            section_id=section_id,
            max_far=metrics_data.get("max_far"),
            max_height_ft=metrics_data.get("max_height_ft"),
            max_units_per_acre=metrics_data.get("max_units_per_acre"),
            max_lot_coverage_pct=metrics_data.get("max_lot_coverage_pct"),
            min_lot_size_sqft=metrics_data.get("min_lot_size_sqft"),
            setback_front_ft=metrics_data.get("setback_front_ft"),
            setback_rear_ft=metrics_data.get("setback_rear_ft"),
            setback_side_ft=metrics_data.get("setback_side_ft"),
            parking_spaces_per_unit=metrics_data.get("parking_spaces_per_unit"),
            building_codes_referenced=metrics_data.get("building_codes", []),
            admin_review_days=metrics_data.get("admin_review_days"),
            public_notice_days=metrics_data.get("public_notice_days"),
            board_approval_required=metrics_data.get("board_approval_required", False),
            total_estimated_lead_time_days=metrics_data.get("total_lead_time_days"),
            flat_fee_usd=metrics_data.get("flat_fee_usd", 0.0),
            sqft_rate_usd=metrics_data.get("sqft_rate_usd", 0.0),
            valuation_pct=metrics_data.get("valuation_pct", 0.0),
            fee_formulas=metrics_data.get("fee_formulas", {}),
        )
        self.session.add(metrics)

        # 3. Create Spatial-Legal Junction Entries
        for z_code in target_zoning_codes:
            if z_code in district_mapping:
                junction = CodeZoningJunction(
                    section_id=section_id,
                    zoning_district_id=district_mapping[z_code],
                )
                self.session.add(junction)
            else:
                logger.warning(f"Zoning code '{z_code}' not found in active spatial mapping. Skipping junction.")

        self.session.commit()
        logger.info(f"Ingested Code Section '{section_data['citation']}' ({section_id}).")
        return section_id
