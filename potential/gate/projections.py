"""projections.py — compute cut vertices across multiple θ projections.

Given a domain graph and a set of declared admissibilities, report per
θ: whether source connects to target, κ, and the cut-vertex set.

No composite across θ. Each θ is one reading. The reader sees which
projections contain a single-vertex cut and which do not; nothing is
ranked or averaged.
"""

from dataclasses import dataclass
from graph import Graph, Admissibility, project, TOKEN_NODE
from cut import cut_vertices, vertex_connectivity

# The declared admissibilities for these domains. Names are the labels
# the reader sees; kind sets are the filters applied to channels.
DEFAULT_THETAS = (
    Admissibility.of("physical", "physical"),
    Admissibility.of("legal", "legal"),
    Admissibility.of("practical", "practical"),
    Admissibility.of("legal+practical", "legal", "practical"),
    Admissibility.of("all", "physical", "legal", "practical"),
)

@dataclass
class Projection:
    theta: Admissibility
    connected: bool
    kappa: int
    cut_vertices: frozenset
    token_is_cut: bool
    token_in_cuts: bool

    def to_dict(self):
        return {
            "theta": self.theta.to_dict(),
            "connected": self.connected,
            "kappa": self.kappa,
            "cut_vertices": sorted(self.cut_vertices),
            "token_is_cut": self.token_is_cut,
            "token_in_cuts": self.token_in_cuts,
        }

def project_all(domain, thetas=DEFAULT_THETAS):
    out = {}
    for theta in thetas:
        g = project(domain, theta)
        if not g.nodes or domain.source not in g.nodes or domain.target not in g.nodes:
            out[theta.name] = Projection(
                theta=theta, connected=False, kappa=0,
                cut_vertices=frozenset(), token_is_cut=False, token_in_cuts=False,
            )
            continue
        kappa, cuts = cut_vertices(g)
        token_is_cut = (kappa == 1 and TOKEN_NODE in cuts)
        out[theta.name] = Projection(
            theta=theta,
            connected=(kappa > 0),
            kappa=kappa,
            cut_vertices=frozenset(cuts),
            token_is_cut=token_is_cut,
            token_in_cuts=(TOKEN_NODE in cuts),
        )
    return out

def render(domain_name, projections):
    lines = [f"domain: {domain_name}", ""]
    lines.append(f"{'theta':18s} {'conn':>5s} {'kappa':>5s} {'token_cut':>10s}  cuts")
    for name in sorted(projections):
        p = projections[name]
        conn = "yes" if p.connected else "no"
        tc = "yes" if p.token_is_cut else "no"
        cuts = ",".join(sorted(p.cut_vertices)) if p.cut_vertices else "-"
        lines.append(f"{name:18s} {conn:>5s} {p.kappa:>5d} {tc:>10s}  {cuts}")
    return "\n".join(lines)

def render_all(all_projections):
    lines = []
    for domain_name in sorted(all_projections):
        lines.append(render(domain_name, all_projections[domain_name]))
        lines.append("")
    return "\n".join(lines).rstrip()
