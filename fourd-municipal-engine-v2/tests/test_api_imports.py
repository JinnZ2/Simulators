"""API smoke tests: import guards, route registration, /health (no DB)."""

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("psycopg2")

from fastapi.testclient import TestClient

from fourd_municipal_engine.api import app
from fourd_municipal_engine.api.main import app as main_app

EXPECTED_PATHS = [
    "/health",
    "/api/v1/envelopes/by-district/{zoning_district_id}",
    "/api/v1/envelopes/by-location",
    "/api/v1/sections/{section_id}/root-causes",
    "/api/v1/sections/{section_id}/citations",
    "/api/v1/fees/calculate",
    "/api/v1/audit/intent-compliance",
]


def test_app_object_exists():
    assert app is not None
    assert main_app is app


def test_routes_registered():
    paths = {route.path for route in app.routes}
    for path in EXPECTED_PATHS:
        assert path in paths, f"missing route: {path}"


def test_health_endpoint():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy", "service": "4D Ordinance API"}
