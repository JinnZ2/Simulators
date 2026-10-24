from pathlib import Path

import pytest

from floor_resilience.schema import build_site, load_site

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "example_site.yaml"


@pytest.fixture(scope="session")
def example():
    site, gaps = load_site(EXAMPLE)
    return site


@pytest.fixture
def make():
    """Build a Site from a dict; asserts no load gaps unless allowed."""
    def _make(raw, allow_gaps=False):
        site, gaps = build_site(raw)
        if not allow_gaps:
            assert gaps == [], gaps
        return site
    return _make
