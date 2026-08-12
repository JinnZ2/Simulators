"""Entity resolution tests — MUST pass stdlib-only (difflib fallback)."""

from fourd_municipal_engine.integrity import (
    EntityRecord,
    EntityNormalizer,
    EntityResolutionMatcher,
)


def _record(rid, raw, address=None, etype="DONOR"):
    return EntityRecord(rid, raw, EntityNormalizer.clean_name(raw), address, etype)


def test_clean_name_strips_corporate_suffixes_and_punctuation():
    assert EntityNormalizer.clean_name("Apex Holdings LLC") == "apex"
    assert EntityNormalizer.clean_name("Acme, Inc.") == "acme"
    assert EntityNormalizer.clean_name("O'Brien & Partners, LLP") == "o brien"


def test_clean_name_empty():
    assert EntityNormalizer.clean_name("") == ""


def test_parse_person_name_last_comma_first():
    first, last = EntityNormalizer.parse_person_name("Smith, Arthur")
    assert (first, last) == ("arthur", "smith")


def test_parse_person_name_first_last():
    first, last = EntityNormalizer.parse_person_name("Arthur Smith")
    assert (first, last) == ("arthur", "smith")


def test_parse_person_name_single_and_empty():
    assert EntityNormalizer.parse_person_name("Madonna") == ("madonna", "")
    assert EntityNormalizer.parse_person_name("") == ("", "")


def test_identical_names_similarity_at_least_099():
    matcher = EntityResolutionMatcher()
    r1 = _record("A", "Arthur Smith")
    r2 = _record("B", "Arthur Smith")
    assert matcher.calculate_similarity(r1, r2) >= 0.99


def test_address_boost_raises_score():
    matcher = EntityResolutionMatcher()
    a = _record("A", "Smith, Arthur C.", "100 Congress Ave, Austin TX")
    b = _record("B", "Arthur Smith", "100 Congress Ave, Austin TX")
    c = _record("C", "Arthur Smith", "999 Nowhere Blvd, El Paso TX")
    d = _record("D", "Arthur Smith")
    with_boost = matcher.calculate_similarity(a, b)
    without_boost = matcher.calculate_similarity(a, c)
    no_address = matcher.calculate_similarity(a, d)
    assert with_boost > without_boost
    assert with_boost > no_address
    assert without_boost == no_address


def test_empty_cleaned_name_scores_zero():
    matcher = EntityResolutionMatcher()
    r1 = _record("A", "Arthur Smith")
    r2 = EntityRecord("B", "", "", None)
    assert matcher.calculate_similarity(r1, r2) == 0.0


def test_match_donors_to_officers_finds_arthur_smith():
    """Sample data from the source harness; threshold 0.85 (stdlib path)."""
    donors = [
        _record("D-101", "Smith, Arthur C.", "100 Congress Ave, Austin TX"),
        _record("D-102", "Jane Doe", "500 W 2nd St, Austin TX"),
        _record("D-103", "Apex Holdings LLC", "1200 Sixth St, Austin TX"),
    ]
    officers = [
        _record("O-501", "Arthur Smith", "100 Congress Ave, Ste 400, Austin TX", "CORPORATE_OFFICER"),
        _record("O-502", "Jane A. Doe", "701 Brazos St, Austin TX", "CORPORATE_OFFICER"),
        _record("O-503", "Robert Johnson", "1200 Sixth St, Austin TX", "CORPORATE_OFFICER"),
    ]

    matcher = EntityResolutionMatcher(match_threshold=0.85)
    results = matcher.match_donors_to_officers(donors, officers)

    links = {(m["donor_id"], m["officer_id"]) for m in results}
    assert ("D-101", "O-501") in links
    for m in results:
        assert m["confidence_score"] >= 0.85
        assert set(m) == {
            "donor_id", "donor_raw_name", "officer_id", "officer_raw_name",
            "confidence_score", "donor_address", "officer_address",
        }
