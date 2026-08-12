"""Automated 4D Ordinance Metrics Parser.

Extracts structured 4D metrics (Density, Design, Delay, Dollars) from raw
municipal ordinance text or PDF documents using a hybrid LLM (pydantic
structured output) + deterministic Regex fallback approach.
"""
import logging
import re
from dataclasses import asdict
from typing import Any, Dict, List, Optional

from fourd_municipal_engine.parser.schemas import (
    DelayMetricsModel,
    DensityMetricsModel,
    DesignMetricsModel,
    DollarMetricsModel,
    FourDOrdinanceMetricsSchema,
)
from fourd_municipal_engine.analysis.root_cause import RegulationRootCauseAnalyzer
from fourd_municipal_engine.analysis.citations import CitationGraph

# For PDF text extraction
try:
    import pypdf
except ImportError:
    pypdf = None

# For OpenAI structured output
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("4D_Ordinance_Parser")

_WORD_NUMBERS = {
    "one": 1.0, "two": 2.0, "three": 3.0, "four": 4.0, "five": 5.0,
    "six": 6.0, "seven": 7.0, "eight": 8.0, "nine": 9.0, "ten": 10.0,
}


class Ordinance4DParser:
    """Parses raw text or PDF documents into structured 4D metrics."""

    SYSTEM_PROMPT = """You are a specialized municipal code and urban planning AI parser.
Your task is to extract quantitative, operational metrics from municipal ordinances and output them according to the strict 4D framework:
- Density: Capacity and bulk metrics (FAR, height, lot size, coverage, units/acre).
- Design: Spatial and building standards (setbacks, parking, referenced building codes).
- Delay: Timeframes (staff review days, notice periods, required approvals, total lead time).
- Dollars: Financial compliance costs (flat fees, square footage rates, valuation percentages, formulas).

Extract exact numerical values. Convert percentages to decimals (e.g., 0.5% -> 0.005). If a value is unstated, return null."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name
        if OpenAI and api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
            logger.warning("OpenAI client not initialized. Parsing will fall back to heuristic Regex extraction.")
        self._root_cause_analyzer = RegulationRootCauseAnalyzer()
        self._citation_graph = CitationGraph()

    def parse_pdf(self, pdf_path: str) -> str:
        """Extracts plain text from a local PDF file."""
        if not pypdf:
            raise ImportError("pypdf is required for PDF parsing. Install with `pip install pypdf`.")

        text_content = []
        with open(pdf_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_content.append(extracted)
        return "\n".join(text_content)

    def _extract_with_llm(self, raw_text: str) -> FourDOrdinanceMetricsSchema:
        """Extracts 4D metrics using OpenAI Structured Outputs."""
        completion = self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": f"Parse the following municipal ordinance text:\n\n{raw_text}"},
            ],
            response_format=FourDOrdinanceMetricsSchema,
            temperature=0.0,
        )
        return completion.choices[0].message.parsed

    # ------------------------------------------------------------------
    # Deterministic regex fallback
    # ------------------------------------------------------------------

    @staticmethod
    def _to_number(token: str) -> Optional[float]:
        token = token.strip().replace(",", "")
        if token.lower() in _WORD_NUMBERS:
            return _WORD_NUMBERS[token.lower()]
        try:
            return float(token)
        except ValueError:
            return None

    def _extract_dollars(self, raw_text: str) -> DollarMetricsModel:
        flat_fee = 0.0
        flat_fee_match = re.search(
            r"\$(\d+(?:\,\d{3})*(?:\.\d{2})?)\s*(?:application|permit|fixed|base)?\s*fee",
            raw_text, re.I,
        )
        if not flat_fee_match:
            # "a fixed processing fee of $450.00" / "application fee: $1,250.00"
            flat_fee_match = re.search(
                r"fee\s*(?:of|:)?\s*\$(\d+(?:\,\d{3})*(?:\.\d{2})?)",
                raw_text, re.I,
            )
        if flat_fee_match:
            flat_fee = float(flat_fee_match.group(1).replace(",", ""))

        sqft_rate = 0.0
        sqft_fee_match = re.search(
            r"\$(\d+(?:\.\d{2})?)\s*per\s*(?:square\s*foot|sq\.?\s*ft\.?|sqft)",
            raw_text, re.I,
        )
        if sqft_fee_match:
            sqft_rate = float(sqft_fee_match.group(1))

        val_pct = 0.0
        val_fee_match = re.search(
            r"(\d+(?:\.\d+)?)\%\s*of\s*(?:total\s*)?(?:project\s*)?valuation",
            raw_text, re.I,
        )
        if val_fee_match:
            val_pct = float(val_fee_match.group(1)) / 100.0

        return DollarMetricsModel(
            flat_fee_usd=flat_fee,
            sqft_rate_usd=sqft_rate,
            valuation_pct=val_pct,
        )

    def _extract_delay(self, raw_text: str) -> DelayMetricsModel:
        days_matches = re.findall(r"(\d+)\s*days", raw_text, re.I)
        review_days = int(days_matches[0]) if days_matches else None

        notice_match = re.search(r"(\d+)\s*days?\s*(?:of\s*)?(?:public\s*)?notice", raw_text, re.I)
        notice_days = int(notice_match.group(1)) if notice_match else None

        board_req = bool(re.search(
            r"(?:planning commission|city council|board of adjustment)\s+approval",
            raw_text, re.I,
        ))
        # Negations such as "No board approval is required" keep the flag False.
        if re.search(r"\bno\s+(?:\w+\s+){0,3}approval\s+is\s+required", raw_text, re.I):
            board_req = False

        return DelayMetricsModel(
            admin_review_days=review_days,
            public_notice_days=notice_days,
            board_approval_required=board_req,
            total_lead_time_days=review_days,
        )

    def _extract_density(self, raw_text: str) -> DensityMetricsModel:
        max_height = None
        height_match = re.search(
            r"(?:height\s*(?:limit|restriction)?\s*of)\s*(\d+(?:\.\d+)?)\s*feet",
            raw_text, re.I,
        )
        if not height_match:
            # "Maximum building height shall not exceed 18 feet."
            height_match = re.search(
                r"height[^.\n]*?(?:not\s+exceed|no\s+more\s+than|maximum\s+of)\s*(\d+(?:\.\d+)?)\s*(?:feet|ft\.?)",
                raw_text, re.I,
            )
        if height_match:
            max_height = float(height_match.group(1))

        max_far = None
        far_match = re.search(
            r"(?:floor\s+area\s+ratio|FAR)[^.\n]*?(\d+(?:\.\d+)?)",
            raw_text, re.I,
        )
        if far_match:
            max_far = float(far_match.group(1))

        coverage_match = re.search(
            r"lot\s+coverage[^.\n]*?(\d+(?:\.\d+)?)\s*(?:%|percent)",
            raw_text, re.I,
        )
        max_coverage = float(coverage_match.group(1)) if coverage_match else None

        upa_match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:dwelling\s*)?units?\s+per\s+acre",
            raw_text, re.I,
        )
        max_upa = float(upa_match.group(1)) if upa_match else None

        lot_match = re.search(
            r"minimum\s+lot\s+size[^.\n]*?(\d[\d,]*(?:\.\d+)?)\s*(?:square\s*feet|sq\.?\s*ft\.?|sqft)",
            raw_text, re.I,
        )
        min_lot = float(lot_match.group(1).replace(",", "")) if lot_match else None

        return DensityMetricsModel(
            max_far=max_far,
            max_height_ft=max_height,
            max_units_per_acre=max_upa,
            max_lot_coverage_pct=max_coverage,
            min_lot_size_sqft=min_lot,
        )

    def _extract_design(self, raw_text: str) -> DesignMetricsModel:
        setbacks: Dict[str, Optional[float]] = {"front": None, "rear": None, "side": None}
        for direction in setbacks:
            match = re.search(
                direction + r"\s*(?:yard\s*)?setback[^.\n;]*?(\d+(?:\.\d+)?)\s*(?:feet|ft\.?)",
                raw_text, re.I,
            )
            if match:
                setbacks[direction] = float(match.group(1))

        parking = None
        parking_match = re.search(
            r"(one|two|three|four|five|six|seven|eight|nine|ten|\d+(?:\.\d+)?)"
            r"[^.\n;]*?parking\s+spaces?[^.\n;]*?per\s+unit",
            raw_text, re.I,
        )
        if not parking_match:
            parking_match = re.search(
                r"(\d+(?:\.\d+)?)\s*parking\s+spaces?\s+per\s+unit",
                raw_text, re.I,
            )
        if parking_match:
            parking = self._to_number(parking_match.group(1))

        codes_found = re.findall(r"\b(?:IBC|IRC|NFPA|NEC|ANSI)\s*\d{4}\b", raw_text, re.I)

        return DesignMetricsModel(
            setback_front_ft=setbacks["front"],
            setback_rear_ft=setbacks["rear"],
            setback_side_ft=setbacks["side"],
            parking_spaces_per_unit=parking,
            building_codes=list(set(codes_found)),
        )

    def _extract_with_regex_fallback(self, raw_text: str) -> FourDOrdinanceMetricsSchema:
        """Deterministic regex heuristics used as a fallback when the LLM API is unavailable."""
        logger.info("Running deterministic Regex fallback parser...")

        return FourDOrdinanceMetricsSchema(
            citation="EXTRACTED-SECTION",
            title="Municipal Ordinance Section",
            summary=raw_text[:200] + "...",
            target_zoning_codes=[],
            density=self._extract_density(raw_text),
            design=self._extract_design(raw_text),
            delay=self._extract_delay(raw_text),
            dollars=self._extract_dollars(raw_text),
        )

    # ------------------------------------------------------------------
    # Addendum analyses: stated intent, root causes, cross-references
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_stated_intent(raw_text: str) -> Optional[str]:
        """Extracts a Purpose/Intent statement block, if present."""
        match = re.search(
            r"(?:purpose|intent|purpose\s+and\s+intent)\s*[:\-]?\s*(.+?)(?:\n\s*\n|\Z)",
            raw_text, re.I | re.S,
        )
        if not match:
            return None
        return " ".join(match.group(1).split()).strip()

    def _analyze_root_causes(self, raw_text: str) -> List[str]:
        return self._root_cause_analyzer.analyze(raw_text)

    def _extract_references(self, raw_text: str) -> List[Dict[str, Any]]:
        return [asdict(ref) for ref in self._citation_graph.extract_references(raw_text)]

    def parse(self, input_data: str, is_pdf_path: bool = False) -> Dict[str, Any]:
        """
        Main entry point. Accepts raw ordinance text or a path to a PDF.
        Outputs a dictionary formatted for direct ingestion into the 4D ETL pipeline.
        """
        raw_text = self.parse_pdf(input_data) if is_pdf_path else input_data

        if self.client:
            try:
                parsed_schema = self._extract_with_llm(raw_text)
            except Exception as e:
                logger.error(f"LLM Structured Extraction failed: {e}. Falling back to Regex.")
                parsed_schema = self._extract_with_regex_fallback(raw_text)
        else:
            parsed_schema = self._extract_with_regex_fallback(raw_text)

        # Transform schema into the exact dictionary structure expected by Municipal4DETLPipeline
        metrics_dict = {
            "section_data": {
                "citation": parsed_schema.citation or "Uncited Section",
                "title": parsed_schema.title or "Municipal Ordinance",
                "raw_text": raw_text,
                "summary": parsed_schema.summary or "",
            },
            "target_zoning_codes": parsed_schema.target_zoning_codes,
            "metrics_data": {
                # Density
                "max_far": parsed_schema.density.max_far,
                "max_height_ft": parsed_schema.density.max_height_ft,
                "max_units_per_acre": parsed_schema.density.max_units_per_acre,
                "max_lot_coverage_pct": parsed_schema.density.max_lot_coverage_pct,
                "min_lot_size_sqft": parsed_schema.density.min_lot_size_sqft,
                # Design
                "setback_front_ft": parsed_schema.design.setback_front_ft,
                "setback_rear_ft": parsed_schema.design.setback_rear_ft,
                "setback_side_ft": parsed_schema.design.setback_side_ft,
                "parking_spaces_per_unit": parsed_schema.design.parking_spaces_per_unit,
                "building_codes": parsed_schema.design.building_codes,
                # Delay
                "admin_review_days": parsed_schema.delay.admin_review_days,
                "public_notice_days": parsed_schema.delay.public_notice_days,
                "board_approval_required": parsed_schema.delay.board_approval_required,
                "total_lead_time_days": parsed_schema.delay.total_lead_time_days or parsed_schema.delay.admin_review_days,
                # Dollars
                "flat_fee_usd": parsed_schema.dollars.flat_fee_usd,
                "sqft_rate_usd": parsed_schema.dollars.sqft_rate_usd,
                "valuation_pct": parsed_schema.dollars.valuation_pct,
                "fee_formulas": parsed_schema.dollars.fee_formulas,
            },
            # SPEC V2 addendum enrichments
            "stated_intent": self._extract_stated_intent(raw_text),
            "root_causes": self._analyze_root_causes(raw_text),
            "references": self._extract_references(raw_text),
        }

        return metrics_dict
