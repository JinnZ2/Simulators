#!/usr/bin/env python3
# inverse_knowledge_tree.py
# CC0-1.0. stdlib-only. phone-buildable.
#
# claim a capability -> trace it backward through every node it rests on
# -> sum the failures that purchased the chain -> weigh that load against
# the margin a forward projection actually holds.
#
# each node carries two numbers that must not be conflated:
#   claimed       : understanding the builders asserted        0..1
#   demonstrated  : reliability the structure showed under load 0..1
#   gap = claimed - demonstrated
#     gap > 0  -> margin SPENT  (abstraction outran the stone)
#     gap < 0  -> margin HELD   (overbuilt against unnamed unknowns)
#
# refutation protocol: verdict updates on contradiction. the tree is data,
# the audit reads it, neither is retuned to make a claim pass.
#
# SCOPE (see grounding-layers/SCOPE_TAXONOMY.md):
#   T = uncalibrated (span_years and failures are caller-defined units)
#   S = uncalibrated (applies to any domain: bridges, drugs, algorithms,
#                     claims of AI capability -- caller supplies the tree)
#   O = any_information_system (any entity that can make claims about
#                               capabilities and cite prerequisites)
#   C = culture_neutral (the framework is domain-agnostic; specific trees
#                        encode specific engineering/scientific traditions,
#                        which the tree itself makes explicit)
#
# Peer to the L-stack rather than a member of it. The L-stack audits
# against physical/biological/social CONSTRAINTS. This audits against
# demonstrated LINEAGE. Different epistemic move; complementary use.

from dataclasses import dataclass
from typing import Dict, Tuple, List


@dataclass(frozen=True)
class Node:
    id: str
    yields: str                     # verb-first capability delivered
    requires: Tuple[str, ...] = ()  # prior knowledge this rests on
    failures_absorbed: int = 0      # failed attempts spent reaching here
    span_years: float = 0.0         # elapsed time those failures took
    claimed: float = 0.0            # asserted understanding
    demonstrated: float = 0.0       # reliability shown under load + time

    @property
    def gap(self) -> float:
        return self.claimed - self.demonstrated


Tree = Dict[str, Node]


def closure(tree: Tree, root: str) -> Tuple[List[str], List[str]]:
    """walk requires-edges backward. return (reached, missing)."""
    seen: List[str] = []
    missing: List[str] = []
    stack = [root]
    while stack:
        nid = stack.pop()
        if nid in seen or nid in missing:
            continue
        node = tree.get(nid)
        if node is None:
            missing.append(nid)
            continue
        seen.append(nid)
        stack.extend(node.requires)
    return seen, missing


def failure_load(tree: Tree, root: str) -> dict:
    reached, missing = closure(tree, root)
    nodes = [tree[n] for n in reached]
    return {
        "root": root,
        "nodes": len(nodes),
        "failures": sum(n.failures_absorbed for n in nodes),
        "span_years": sum(n.span_years for n in nodes),
        "margin_spent": round(sum(n.gap for n in nodes if n.gap > 0), 3),
        "margin_held": round(sum(-n.gap for n in nodes if n.gap < 0), 3),
        "spenders": [n.id for n in nodes if n.gap > 0],
        "reached": reached,
        "missing": missing,
    }


def audit(tree: Tree, root: str, margin_attempts: int,
          gap_tol: float = 0.15, terminal_tol: float = 0.20):
    """verdict on projecting `root` forward into new territory.
       margin_attempts = failed attempts the projection can absorb
       before it must pay off.
       two gates, because collapse is local: a chain can average honest
       while its point-of-application spends hard. the terminal node's
       own posture can't hide behind honest ancestors."""
    load = failure_load(tree, root)
    node = tree.get(root)
    terminal_gap = node.gap if node else 0.0
    load["terminal_gap"] = round(terminal_gap, 3)
    if load["missing"]:
        verdict = "UNGROUNDED"        # chain rests on nodes not in the ledger
    elif load["failures"] > margin_attempts:
        verdict = "EXCEEDS"           # historical failure-load > available margin
    elif terminal_gap > terminal_tol:
        verdict = "BORROWS"           # point-of-application spends unearned margin
    elif load["margin_spent"] > gap_tol * max(load["nodes"], 1):
        verdict = "BORROWS"           # chain-wide spend beyond tolerance
    else:
        verdict = "HOLDS"             # margin covers load, chain stands on demonstrated ground
    return verdict, load


def report(verdict: str, load: dict) -> str:
    lines = [
        f"root          {load['root']}",
        f"verdict       {verdict}",
        f"chain depth   {load['nodes']} nodes",
        f"failure-load  {load['failures']} attempts over {load['span_years']:.0f}y",
        f"margin spent  {load['margin_spent']}   (abstraction outran stone)",
        f"margin held   {load['margin_held']}   (overbuilt reserve)",
        f"terminal gap  {load.get('terminal_gap', 0.0)}   (spend at point-of-application)",
    ]
    if load["spenders"]:
        lines.append(f"spenders      {', '.join(load['spenders'])}")
    if load["missing"]:
        lines.append(f"MISSING       {', '.join(load['missing'])}  <- untraceable")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# demo tree: bridges, root-to-span, honest about the graveyard behind each
# ---------------------------------------------------------------------------

BRIDGES: Tree = {
    "fire_control":   Node("fire_control", "smelts ore repeatably",
                           (), 40, 3000, claimed=0.30, demonstrated=0.85),
    "lime_mortar":    Node("lime_mortar", "binds stone under compression",
                           ("fire_control",), 25, 400, claimed=0.35, demonstrated=0.92),
    "roman_arch":     Node("roman_arch", "distributes load through compression",
                           ("lime_mortar",), 30, 300, claimed=0.35, demonstrated=0.95),
    "iron_working":   Node("iron_working", "forms members in tension",
                           ("fire_control",), 60, 2000, claimed=0.50, demonstrated=0.75),
    "steel_process":  Node("steel_process", "yields predictable tensile members",
                           ("iron_working",), 120, 150, claimed=0.60, demonstrated=0.78),
    "stress_theory":  Node("stress_theory", "predicts member stress under load",
                           ("steel_process",), 200, 120, claimed=0.78, demonstrated=0.72),
    "fea_modeling":   Node("fea_modeling", "simulates whole-structure response",
                           ("stress_theory",), 300, 60, claimed=0.90, demonstrated=0.72),
    "cost_optimization": Node("cost_optimization", "trims material to modeled minimum",
                           ("fea_modeling",), 90, 40, claimed=0.95, demonstrated=0.60),
    # standing:
    "aqueduct_span":  Node("aqueduct_span", "carries water across valley 2000y",
                           ("roman_arch",), 12, 300, claimed=0.35, demonstrated=0.97),
    # fell 2007:
    "i35w_span":      Node("i35w_span", "spans river at minimum steel",
                           ("cost_optimization", "steel_process"), 15, 5,
                           claimed=0.92, demonstrated=0.55),
    # forward projection into new territory:
    "new_gorge_span": Node("new_gorge_span", "spans unmeasured gorge, optimized",
                           ("cost_optimization", "fea_modeling", "steel_process"), 0, 0,
                           claimed=0.93, demonstrated=0.0),
}


if __name__ == "__main__":
    print("=" * 60)
    print("STANDING vs FALLEN — same domain, opposite margin posture")
    print("=" * 60)
    for root in ("aqueduct_span", "i35w_span"):
        v, load = audit(BRIDGES, root, margin_attempts=1000)
        print(report(v, load))
        print("-" * 60)

    print("\n" + "=" * 60)
    print("FORWARD PROJECTION — 'overcome the gorge through optimization'")
    print("=" * 60)
    for margin in (2000, 500):
        v, load = audit(BRIDGES, "new_gorge_span", margin_attempts=margin)
        print(f"\navailable margin = {margin} attempts")
        print(report(v, load))

    print("\n" + "=" * 60)
    print("UNGROUNDED — claim resting on a node not in the ledger")
    print("=" * 60)
    ghost = dict(BRIDGES)
    ghost["nano_lattice_span"] = Node(
        "nano_lattice_span", "spans via unproven nano-lattice",
        ("self_healing_alloy",), 0, 0, claimed=0.98, demonstrated=0.0)
    v, load = audit(ghost, "nano_lattice_span", margin_attempts=5000)
    print(report(v, load))
