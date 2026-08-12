"""Domain module registry for crossdomain_eval."""

from __future__ import annotations

from crossdomain_eval.domains import geometry, physics

#: Registry of domain name -> module.
DOMAINS: dict[str, object] = {
    "physics": physics,
    "geometry": geometry,
}
