"""
Entity Resolution Pipeline: Developer Shell LLCs vs. Campaign Donors

Resolves identities between corporate officers/LLC owners and political donors
using string distance heuristics (Jaro-Winkler / Levenshtein) and spatial
address clustering.

STDLIB-ONLY: rapidfuzz is used when installed; difflib is the fallback.
"""

import re
import logging
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass

try:
    from rapidfuzz import string_metric, process
except ImportError:
    # Fallback to difflib if rapidfuzz is unavailable
    import difflib
    string_metric = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Entity_Resolution_Pipeline")


@dataclass
class EntityRecord:
    record_id: str
    raw_name: str
    cleaned_name: str
    address: Optional[str] = None
    entity_type: str = "DONOR"  # "DONOR" or "CORPORATE_OFFICER"


class EntityNormalizer:
    """Standardizes personal and corporate names for high-accuracy matching."""

    CORP_SUFFIXES = re.compile(
        r'\b(llc|inc|corp|corporation|ltd|limited|lp|llp|holdings|group|development|properties|partners|management)\b',
        re.IGNORECASE
    )
    PUNCTUATION = re.compile(r'[^\w\s]')

    @classmethod
    def clean_name(cls, name: str) -> str:
        if not name:
            return ""
        # Lowercase and strip punctuation
        cleaned = name.lower()
        cleaned = cls.PUNCTUATION.sub(' ', cleaned)
        # Strip corporate suffixes
        cleaned = cls.CORP_SUFFIXES.sub('', cleaned)
        # Collapse multiple spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    @classmethod
    def parse_person_name(cls, name: str) -> Tuple[str, str]:
        """Splits 'Last, First' or 'First Last' into (first, last)."""
        cleaned = cls.clean_name(name)
        parts = cleaned.split()
        if not parts:
            return "", ""
        if ',' in name:
            return parts[-1], parts[0]
        if len(parts) == 1:
            return parts[0], ""
        return parts[0], parts[-1]


class EntityResolutionMatcher:
    def __init__(self, match_threshold: float = 0.88):
        self.match_threshold = match_threshold

    @staticmethod
    def _token_sort_ratio(s1: str, s2: str) -> float:
        """difflib SequenceMatcher ratio over token-sorted strings (order-insensitive)."""
        t1 = ' '.join(sorted(s1.split()))
        t2 = ' '.join(sorted(s2.split()))
        return difflib.SequenceMatcher(None, t1, t2).ratio()

    def calculate_similarity(self, record1: EntityRecord, record2: EntityRecord) -> float:
        """Computes composite similarity score based on name and address overlap."""
        name1 = record1.cleaned_name
        name2 = record2.cleaned_name

        if not name1 or not name2:
            return 0.0

        # 1. Name String Similarity Score
        if string_metric:
            # RapidFuzz Jaro-Winkler similarity (0-100 scale)
            name_score = string_metric.jaro_winkler_similarity(name1, name2) / 100.0
        else:
            # Fallback difflib SequenceMatcher ratio (raw and token-sorted)
            name_score = max(
                difflib.SequenceMatcher(None, name1, name2).ratio(),
                self._token_sort_ratio(name1, name2),
            )

        # 2. Address Boost
        address_boost = 0.0
        if record1.address and record2.address:
            addr1 = EntityNormalizer.clean_name(record1.address)
            addr2 = EntityNormalizer.clean_name(record2.address)
            if addr1 and addr2:
                if addr1 == addr2:
                    address_boost = 0.10  # Exact address match bonus
                elif string_metric:
                    if string_metric.jaro_winkler_similarity(addr1, addr2) > 85:
                        address_boost = 0.05
                elif self._token_sort_ratio(addr1, addr2) > 0.85:
                    address_boost = 0.05

        composite_score = min(1.0, name_score + address_boost)
        return round(composite_score, 4)

    def match_donors_to_officers(
        self,
        donors: List[EntityRecord],
        officers: List[EntityRecord]
    ) -> List[Dict[str, Any]]:
        """Matches a batch of campaign donors against corporate LLC officers."""
        matched_pairs = []

        logger.info(
            "Running Entity Resolution across %d donors and %d corporate officers...",
            len(donors), len(officers),
        )

        for donor in donors:
            for officer in officers:
                score = self.calculate_similarity(donor, officer)
                if score >= self.match_threshold:
                    matched_pairs.append({
                        "donor_id": donor.record_id,
                        "donor_raw_name": donor.raw_name,
                        "officer_id": officer.record_id,
                        "officer_raw_name": officer.raw_name,
                        "confidence_score": score,
                        "donor_address": donor.address,
                        "officer_address": officer.address
                    })

        logger.info(
            "Resolution complete: Found %d match links above %s threshold.",
            len(matched_pairs), self.match_threshold,
        )
        return matched_pairs
