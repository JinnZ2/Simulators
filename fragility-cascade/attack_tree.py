"""
attack_tree.py
-------------
The attack surface as a fractal, plus the growth law.

The Branching Principle: every leaf is a stem. "Counterfeit GPU" opens into
"TEE compromise" opens into "vendor backdoor" / "state coercion" opens into
specific agency operations opens into individual engineers with a price. The
recursion bottoms out only at human bodies and physical matter.

Two things live here:
  1. A typed, expandable tree so the map can be walked, extended, and never
     mistaken for complete (any leaf is expandable = surface is unbounded).
  2. surface_growth(): a toy law showing attackable paths grow super-linearly
     with intermediation depth L, while a possession asset (L=0) has a fixed,
     tiny surface.

Falsifiable claim: total attack surface grows at least polynomially in the number
of trust relationships. A defender must cover all of it; an attacker needs one
path. Refute by exhibiting a multi-intermediary value system whose exploitable
path count stays constant as intermediation depth rises.

CC0. stdlib only.
"""

from dataclasses import dataclass, field


@dataclass
class AttackNode:
    label: str
    children: list = field(default_factory=list)
    expandable: bool = True   # branching principle: a leaf is only unexpanded, never final

    def add(self, *labels):
        for l in labels:
            self.children.append(AttackNode(l))
        return self

    def leaves(self):
        if not self.children:
            yield self
        for c in self.children:
            yield from c.leaves()

    def walk(self, depth=0):
        mark = "" if self.children else ("  [expandable]" if self.expandable else "")
        yield f"{'  ' * depth}- {self.label}{mark}"
        for c in self.children:
            yield from c.walk(depth + 1)


def compcoin_tree():
    root = AttackNode("CompCoin surface")
    hw = AttackNode("hardware"); hw.add("counterfeit GPU", "supply-chain trojan", "physical DC destruction")
    net = AttackNode("provider/network"); net.add("Sybil provider farm", "reputation gaming", "oversubscription death spiral")
    bench = AttackNode("benchmark/proof"); bench.add("dieselgate", "proof forgery", "oracle manipulation")
    gov = AttackNode("governance/DAO"); gov.add("plutocratic capture", "emergency-powers abuse", "voter apathy oligarchy")
    res = AttackNode("physical reserve"); res.add("fractional-reserve deception", "jurisdictional arbitrage", "redemption bottleneck")
    econ = AttackNode("economic/market"); econ.add("landlord-tax cartel", "hidden rehypothecation", "front-running conversions")
    legal = AttackNode("legal/regulatory"); legal.add("regulatory capture", "reclassification risk", "sanctions weaponization")
    meta = AttackNode("meta-systemic"); meta.add("complexity collapse", "information-asymmetry tax", "too-big-to-fail moral hazard", "adversarial AI")
    root.children = [hw, net, bench, gov, res, econ, legal, meta]
    return root


def surface_growth(max_depth=6, branching=3):
    """
    Possession asset: L=0, surface ~ 1 (theft/degradation).
    Intermediated asset: each layer multiplies paths by `branching`.
    Cumulative exploitable paths through depth L = sum(branching**k).
    """
    print("depth L   cumulative exploitable paths   defender must cover / attacker needs")
    print("-" * 74)
    cum = 0
    for L in range(max_depth + 1):
        cum += branching ** L
        print(f"{L:>5}     {cum:>12,}                     all {cum:,} / any 1")


def report():
    tree = compcoin_tree()
    print("\n".join(tree.walk()))
    n_leaves = sum(1 for _ in tree.leaves())
    print(f"\nvisible leaves: {n_leaves}  -- and every one is a stem, not a floor.\n")
    surface_growth()
    print("\nA barrel of oil sits at L=0. Its surface is a fence and a lock.")


if __name__ == "__main__":
    report()
