"""Batch 4D Ordinance & GIS Ingestion Pipeline.

Scans a directory for ordinance files (.pdf, .txt), parses them using
Ordinance4DParser, and loads them into the 4D PostGIS schema via
Municipal4DETLPipeline.
"""
import argparse
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fourd_municipal_engine.etl.models import ZoningDistrict
from fourd_municipal_engine.etl.pipeline import Municipal4DETLPipeline
from fourd_municipal_engine.parser.ordinance_parser import Ordinance4DParser

logger = logging.getLogger("Batch_4D_Ingestion")

DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/municipal_4d")


class BatchOrdinanceIngestor:
    def __init__(self, db_url: str, openai_api_key: str = None, max_workers: int = 4):
        self.engine = create_engine(db_url, pool_size=10, max_overflow=20)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.parser = Ordinance4DParser(api_key=openai_api_key)
        self.max_workers = max_workers

    def _get_active_district_map(self, session, jurisdiction_id) -> Dict[str, Any]:
        """Loads all active zoning district codes and UUIDs for a jurisdiction."""
        districts = session.query(ZoningDistrict).filter_by(jurisdiction_id=jurisdiction_id).all()
        return {d.district_code: d.zoning_district_id for d in districts}

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Processes a single file (PDF or TXT) into a 4D metric payload."""
        logger.info(f"Parsing file: {file_path}")
        is_pdf = file_path.lower().endswith(".pdf")

        try:
            parsed_payload = self.parser.parse(file_path, is_pdf_path=is_pdf)
            parsed_payload["source_file"] = file_path
            return parsed_payload
        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
            return {"source_file": file_path, "error": str(e)}

    def ingest_directory(
        self,
        directory_path: str,
        jurisdiction_name: str,
        state_code: str,
        fips_code: str,
    ):
        """Batch-processes all PDF/TXT files in directory_path and persists to DB."""
        session = self.SessionLocal()
        pipeline = Municipal4DETLPipeline(session)

        try:
            # 1. Ensure Jurisdiction & Spatial Mapping
            jurisdiction_id = pipeline.get_or_create_jurisdiction(
                name=jurisdiction_name,
                state_code=state_code,
                fips_code=fips_code,
            )
            district_map = self._get_active_district_map(session, jurisdiction_id)

            # 2. Collect Files
            target_path = Path(directory_path)
            files = [str(p) for p in target_path.glob("**/*") if p.suffix.lower() in [".pdf", ".txt"]]
            logger.info(f"Found {len(files)} files in {directory_path} for ingestion.")

            if not files:
                logger.warning("No valid files found. Exiting.")
                return

            # 3. Parallel Extraction Stage
            parsed_results = []
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(self.process_file, f): f for f in files}
                for future in as_completed(futures):
                    result = future.result()
                    if "error" not in result:
                        parsed_results.append(result)

            logger.info(f"Successfully extracted metrics for {len(parsed_results)}/{len(files)} documents.")

            # 4. Database Ingestion Stage
            ingested_count = 0
            for item in parsed_results:
                try:
                    pipeline.ingest_ordinance_with_4d_metrics(
                        jurisdiction_id=jurisdiction_id,
                        section_data=item["section_data"],
                        metrics_data=item["metrics_data"],
                        target_zoning_codes=item["target_zoning_codes"],
                        district_mapping=district_map,
                    )
                    ingested_count += 1
                except Exception as db_err:
                    session.rollback()
                    logger.error(f"Failed DB insertion for {item['source_file']}: {db_err}")

            logger.info(f"Batch ingestion complete: {ingested_count} records inserted successfully.")

        finally:
            session.close()


def main(argv=None):
    arg_parser = argparse.ArgumentParser(description="Batch-ingest ordinance files into the 4D PostGIS schema.")
    arg_parser.add_argument("directory", help="Directory containing .pdf/.txt ordinance files")
    arg_parser.add_argument("--jurisdiction", default="City of Austin", help="Jurisdiction name")
    arg_parser.add_argument("--state", default="TX", help="Two-letter state code")
    arg_parser.add_argument("--fips", default="4805000", help="FIPS code for the jurisdiction")
    arg_parser.add_argument("--workers", type=int, default=4, help="Max parallel parse workers")
    args = arg_parser.parse_args(argv)

    api_key = os.getenv("OPENAI_API_KEY")
    ingestor = BatchOrdinanceIngestor(db_url=DB_URL, openai_api_key=api_key, max_workers=args.workers)
    ingestor.ingest_directory(
        directory_path=args.directory,
        jurisdiction_name=args.jurisdiction,
        state_code=args.state,
        fips_code=args.fips,
    )


if __name__ == "__main__":
    main()
