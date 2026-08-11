"""Tests for the MunicipalCodeTranslator."""
from fourd_municipal_engine.translator.core import MunicipalCodeTranslator

ORDINANCE_TEXT = (
    "Purpose: to protect wetlands and water quality from stormwater runoff.\n"
    "\n"
    "Section 1. Pursuant to Section 12.4, the applicant shall obtain a permit "
    "prior to commencing any land disturbance. A fee of $250.00 shall be paid "
    "at the time of application, plus $1,000 for the review bond."
)


def test_jargon_replacement_shall_to_must():
    result = MunicipalCodeTranslator().translate(ORDINANCE_TEXT)
    assert "shall" not in result.plain_english_summary.lower()
    assert "must" in result.plain_english_summary


def test_jargon_replacement_pursuant_to_under():
    result = MunicipalCodeTranslator().translate(ORDINANCE_TEXT)
    summary = result.plain_english_summary
    assert "pursuant to" not in summary.lower()
    # case-preserving replacement ("Pursuant to" -> "Under")
    assert "under section 12.4" in summary.lower()


def test_flat_fees_extracted():
    result = MunicipalCodeTranslator().translate(ORDINANCE_TEXT)
    amounts = [fee.amount for fee in result.fees]
    assert 250.0 in amounts
    assert 1000.0 in amounts


def test_stated_intent_extracted_from_purpose_block():
    result = MunicipalCodeTranslator().translate(ORDINANCE_TEXT)
    assert result.stated_intent
    assert "wetlands" in result.stated_intent.lower()


def test_citation_attached():
    result = MunicipalCodeTranslator().translate(
        ORDINANCE_TEXT, citation="Section 12.4"
    )
    assert result.section_citation == "Section 12.4"
