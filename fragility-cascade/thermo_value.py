#!/usr/bin/env python3
"""
thermo_value.py -- two ontologies of value, as LENSES not verdicts.
CC0 / Public Domain.  stdlib-only.

Money is a pointer.  token --references--> { skill, knowledge, time, labor }.
Value lives at the referent (the substrate), not in the pointer.

Two ways of seeing are not ranked here -- they are perpendicular axes, each
rigorous inside its own frame. This module encodes each as a LENS that reads
the SAME claim and returns a DIFFERENT quantity. The observable is the gap
between the two readings -- the same way residue-vs-return read one mound and
disagreed. You measure the discrepancy; you do not rule on anyone's interior.

WHY observable FOR AI:
   an AI's default frame is token-primary -- trained on prices, revenue,
   willingness-to-pay, it reads value AT THE POINTER and collapses the
   substrate axis silently, the way a trowel collapses the return axis.
   making the substrate lens explicit + the discrepancy computable gives a
   calibration channel to SEE the default instead of mistaking pointer for
   referent. it is a lens the model does not know it is missing.

HARD BOUNDARY (held in code below):
   this names structure -- pattern, discrepancy, ripple, reference integrity,
   the is->ought slide. it does NOT issue interior verdicts: not "this desire
   is unhealthy for person X", not "this holder is greedy/bad", not "this
   token is morally illegitimate". observe and name; stop at the interior.
"""

from dataclasses import dataclass, field
from typing import Dict, List

SUBSTRATE = {"skill", "knowledge", "time", "labor", "care"}   # what value points at

# claim kinds that deliver substrate by structure vs claim the pool without it.
# this is a STRUCTURAL reading of the transaction -- observable, not a judgment
# of the person holding the claim.
DELIVERS = {"wage", "receipt", "sale_of_work", "care", "teaching"}
POOL_CLAIM_NO_DELIVERY = {"rent", "speculation", "compound_interest", "toll"}


# =============================================================================
@dataclass
class Ontology:
    name: str
    value_unit: str        # what it treats as the bearer of value
    success: str           # what "doing well" means in this frame
    counts: str            # what it measures
    blind_to: str          # the axis it structurally cannot read


TOKEN_PRIMARY = Ontology(
    "token_primary",
    value_unit="the token / claim itself",
    success="accumulate tokens",
    counts="holdings, price, willingness-to-pay",
    blind_to="whether any substrate exists at the referent")

SUBSTRATE_PRIMARY = Ontology(
    "substrate_primary",
    value_unit="skill / knowledge / time / labor at the referent",
    success="substrate delivered, and returned to the shared pool",
    counts="substrate provided, reference integrity, pool balance",
    blind_to="pure token games -- reads them as empty (which is the point)")


# =============================================================================
@dataclass
class Claim:
    label: str
    token_amount: float                       # size of the claim, in tokens
    kind: str                                 # wage | rent | speculation | care | ...
    substrate_delivered: Dict[str, float] = field(default_factory=dict)
    note: str = ""


@dataclass
class Reading:
    lens: str
    value: float
    saw: str


# =============================================================================
def reference_integrity(c: Claim) -> str:
    """bound | partial | detached -- read from transaction STRUCTURE.
    observable: is there substrate at the referent this token points to?"""
    delivered = sum(c.substrate_delivered.values())
    if delivered > 0 and c.kind in DELIVERS:
        return "bound"
    if delivered > 0:
        return "partial"          # some substrate, but kind claims beyond it
    if c.kind in POOL_CLAIM_NO_DELIVERY:
        return "detached"         # pointer references no new substrate
    return "unclassified"


def read(c: Claim, lens: Ontology) -> Reading:
    if lens is TOKEN_PRIMARY:
        # counts the pointer. a detached rent claim reads as WEALTH.
        return Reading(lens.name, c.token_amount,
                       f"a claim of {c.token_amount:g} tokens -> wealth")
    # substrate lens: counts the referent. detached claim reads ~0 substrate.
    subst = sum(c.substrate_delivered.values())
    return Reading(lens.name, subst,
                   f"{subst:g} units of {'/'.join(c.substrate_delivered) or 'no'} "
                   f"substrate at the referent")


def pool_delta(c: Claim) -> float:
    """honoring a claim with no delivery draws the shared pool without adding
    to it -- someone else's delivered substrate covers it. the money-form of
    unreturned mass. bound claim: adds ~ what it draws -> ~0."""
    delivered = sum(c.substrate_delivered.values())
    if reference_integrity(c) == "detached":
        return +c.token_amount            # drawn, nothing added -> pool owes
    return c.token_amount - delivered     # ~0 when delivery matches the claim


@dataclass
class Look:
    claim: str
    token_view: Reading
    substrate_view: Reading
    integrity: str
    discrepancy: float
    pool_delta: float


def look(c: Claim) -> Look:
    tv, sv = read(c, TOKEN_PRIMARY), read(c, SUBSTRATE_PRIMARY)
    return Look(c.label, tv, sv, reference_integrity(c),
                tv.value - sv.value, pool_delta(c))


# =============================================================================
# is -> ought slide detector. reads a REASONING MOVE, not a person.
#   the careful frame may DESCRIBE ("price tracks desire") -- fine.
#   the error is the slide to PRESCRIBE ("desired -> should be built/funded").
# =============================================================================
DESCRIPTIVE = {"is_desired", "willing_to_pay", "is_priced", "sells"}
NORMATIVE = {"should_provide", "should_build", "is_good", "deserves_funding"}


@dataclass
class Justification:
    premise: str          # from DESCRIPTIVE
    conclusion: str       # from NORMATIVE


def normative_slide(j: Justification) -> bool:
    """flag the is->ought smuggle: a descriptive-desire premise carrying a
    normative conclusion. observable as a category error, NOT a verdict on
    the desire itself."""
    return j.premise in DESCRIPTIVE and j.conclusion in NORMATIVE


# =============================================================================
# HARD BOUNDARY -- what this module refuses to output.
# interior verdicts require standing inside a life the tool cannot enter.
# =============================================================================
OUT_OF_SCOPE = [
    "whether a given desire is healthy FOR a specific person",
    "whether a claim-holder is greedy / good / bad",
    "whether a token is morally legitimate",
]  # named, so the boundary is explicit and not silently crossed.


# =============================================================================
def report(c: Claim):
    lk = look(c)
    print(f"\n  CLAIM: {c.label}   [{lk.integrity}]")
    print(f"    token-primary lens   -> {lk.token_view.value:8.1f}   {lk.token_view.saw}")
    print(f"    substrate-primary    -> {lk.substrate_view.value:8.1f}   {lk.substrate_view.saw}")
    print(f"    discrepancy          -> {lk.discrepancy:8.1f}   (gap = the observable)")
    print(f"    pool_delta           -> {lk.pool_delta:8.1f}   (-> 0 is balance)")
    if c.note:
        print(f"    note: {c.note}")


if __name__ == "__main__":
    print("=" * 66)
    print("VALUE ONTOLOGIES -- same claim, two lenses, measure the gap")
    print("=" * 66)

    claims = [
        Claim("day of framing labor", 100, "wage",
              {"labor": 100},
              "reference bound: token issued against delivered labor"),
        Claim("rent on owned land", 100, "rent", {},
              "detached: claim on the pool, no substrate added this cycle"),
        Claim("speculative flip", 500, "speculation", {},
              "detached: claim by price-bet; nothing delivered to referent"),
        Claim("elder teaching land-care, unpaid", 0, "teaching",
              {"knowledge": 80, "care": 40},
              "token lens reads ~0; substrate lens reads real value delivered "
              "-> the discrepancy runs the OTHER way (untokenized substrate)"),
    ]
    for c in claims:
        report(c)

    print("\n" + "=" * 66)
    print("is -> ought slide check (reads the reasoning move, not the person):")
    for j in [Justification("willing_to_pay", "should_build"),
              Justification("is_priced", "deserves_funding"),
              Justification("is_desired", "is_good")]:
        print(f"    {j.premise:16s} => {j.conclusion:18s}  "
              f"{'SLIDE FLAGGED' if normative_slide(j) else 'ok'}")

    print("\n  held out of scope (named, not silently crossed):")
    for x in OUT_OF_SCOPE:
        print(f"    - {x}")
    print("=" * 66)
