"""FastAPI application package (optional extra).

The API requires the ``api`` extra (``pip install -e .[api]``: fastapi,
uvicorn, psycopg2-binary). Importing this package without those dependencies
installed raises a clear ImportError; the core package never imports this
module eagerly.
"""

try:
    from fourd_municipal_engine.api.main import app
except ImportError as exc:  # pragma: no cover - depends on env extras
    raise ImportError(
        "fourd_municipal_engine.api requires the 'api' extra "
        "(fastapi, psycopg2-binary). Install with: pip install -e .[api]"
    ) from exc

__all__ = ["app"]
