"""Skilled-operator reserve line: spec and cost model (work order section 7).

Framed as resilience insurance: the premium is what the line costs net of
what it produces; the expected avoided loss is outage days x daily output
value x yearly outage probability x the share of that loss the line avoids.
All inputs come from the user. Nothing here is a finding.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .schema import ReserveInputs

SPEC = [
    "Runs live daily production, not drills.",
    "Operators see automation data and fault logs, and their fixes feed back "
    "into the maintenance record under their own names.",
    "Sized to keep the plant's critical output going by hand if the automated "
    "line or its software is down.",
]

POLICY_NOTE = (
    "PROPOSED: a policy frame like a strategic reserve (compare the Defense "
    "Production Act) could fund such lines. This is an analogy, not an "
    "existing program."
)

DEFAULT_AVOIDED_SHARE = 1.0   # ASSUMED when not given: line avoids the whole loss


@dataclass
class ReserveCost:
    wage_cost: Optional[float]
    output_value: Optional[float]
    premium: Optional[float]               # net yearly cost
    expected_avoided_loss: Optional[float]
    ratio: Optional[float]                 # avoided loss per unit premium
    missing: list[str] = field(default_factory=list)
    assumed: list[str] = field(default_factory=list)


def cost(inp: ReserveInputs) -> ReserveCost:
    missing, assumed = [], []
    wage = None
    if inp.size is not None and inp.wage_cost_per_operator_year is not None:
        wage = inp.size * inp.wage_cost_per_operator_year
    else:
        missing += [n for n in ("size", "wage_cost_per_operator_year")
                    if getattr(inp, n) is None]
    out = inp.reserve_output_value_per_year
    if out is None:
        missing.append("reserve_output_value_per_year")
    premium = wage - out if wage is not None and out is not None else None
    share = inp.share_of_outage_avoided
    if share is None:
        share = DEFAULT_AVOIDED_SHARE
        assumed.append(f"share_of_outage_avoided = {share} (ASSUMED)")
    loss_inputs = ("outage_days", "daily_output_value", "outage_probability_per_year")
    absent = [n for n in loss_inputs if getattr(inp, n) is None]
    missing += absent
    avoided = None
    if not absent:
        avoided = (inp.outage_days * inp.daily_output_value
                   * inp.outage_probability_per_year * share)
    ratio = avoided / premium if avoided is not None and premium and premium > 0 else None
    return ReserveCost(wage, out, premium, avoided, ratio, missing, assumed)
