"""Software-layer knockout (work order section 6b).

Graph: function -> machines -> software layers, and layer -> layers it
depends on. Take one layer down; everything that depends on it, directly or
through other layers, goes down too. Report which machines and functions
stop, which degrade, and whether a person can bridge the gap.

A "hidden chain" is a machine whose own listed layers do not include the
downed layer but which stops anyway because one of them calls it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from importlib import resources
from typing import Optional

import yaml

from ..schema import Site


@dataclass
class MachineHit:
    machine: str
    status: str                 # STOPS | DEGRADED | BRIDGED_LOCAL | OK
    via: list[str]              # downed layers it touches
    hidden_chain: bool


@dataclass
class FunctionHit:
    function: str
    status: str                 # STOPS | BRIDGED | DEGRADED | OK
    bridge: Optional[str]
    because: list[str]


@dataclass
class Knockout:
    layer: str
    down: list[str]             # the layer plus everything depending on it
    machines: list[MachineHit] = field(default_factory=list)
    functions: list[FunctionHit] = field(default_factory=list)
    unknown_layers: list[str] = field(default_factory=list)

    @property
    def hidden_chains(self) -> list[str]:
        return [m.machine for m in self.machines if m.hidden_chain]


def downstream(site: Site, layer: str) -> list[str]:
    """The layer and every layer that depends on it, transitively."""
    deps = {l.id: set(l.depends_on) for l in site.software_layers}
    down, changed = {layer}, True
    while changed:
        changed = False
        for lid, ds in deps.items():
            if lid not in down and ds & down:
                down.add(lid)
                changed = True
    return sorted(down)


def knockout(site: Site, layer: str) -> Knockout:
    down = set(downstream(site, layer))
    known = {l.id for l in site.software_layers}
    ko = Knockout(layer, sorted(down))
    status_of: dict[str, str] = {}
    for m in site.machines:
        ko.unknown_layers += [l for l in m.software_layers
                              if l not in known and l not in ko.unknown_layers]
        via = [l for l in m.software_layers if l in down]
        if not via:
            st = "OK"
        elif m.manual_mode == "full":
            st = "BRIDGED_LOCAL"
        elif m.manual_mode == "partial":
            st = "DEGRADED"
        else:
            st = "STOPS"   # manual_mode none or not recorded: assume no bypass
        hidden = bool(via) and layer not in m.software_layers
        status_of[m.id] = st
        ko.machines.append(MachineHit(m.id, st, via, hidden))
    for f in site.functions:
        because = [l for l in f.layers if l in down]
        because += [f"machine {mid}" for mid in f.machines
                    if status_of.get(mid) == "STOPS"]
        degraded = [mid for mid in f.machines
                    if status_of.get(mid) in ("DEGRADED", "BRIDGED_LOCAL")]
        if because:
            st = "BRIDGED" if f.bridge else "STOPS"
        elif degraded:
            st = "DEGRADED"
            because = [f"machine {mid} on manual" for mid in degraded]
        else:
            st = "OK"
        ko.functions.append(FunctionHit(f.id, st, f.bridge, because))
    return ko


def all_knockouts(site: Site) -> list[Knockout]:
    return [knockout(site, l.id) for l in site.software_layers]


def bridge_share(kos: list[Knockout]) -> Optional[float]:
    """Share of hit functions that a person can keep going."""
    hit = [f for k in kos for f in k.functions if f.status in ("STOPS", "BRIDGED")]
    if not hit:
        return None
    return sum(f.status == "BRIDGED" for f in hit) / len(hit)


# --- PHP2Shell worked example ---------------------------------------------
def load_php2shell() -> dict:
    text = resources.files("floor_resilience").joinpath(
        "data/php2shell.yaml").read_text(encoding="utf-8")
    return yaml.safe_load(text)


def _ver(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in v.split(".") if x.isdigit())


def php_patch_status(version: Optional[str], facts: dict) -> str:
    if not version:
        return "PHP version not recorded: cannot say whether a patch exists"
    parts = _ver(version)
    if len(parts) < 2:
        return f"PHP version '{version}' not readable"
    branch = f"{parts[0]}.{parts[1]}"
    if parts[:2] < _ver(facts["no_upstream_patch_below"]):
        return (f"PHP {version}: no patch from the PHP project for this branch; "
                "needs a vendor backport or a move to 8.2+. Plan for this layer "
                "staying down.")
    fixed = facts["fixed_versions"].get(branch)
    if fixed is None:
        return f"PHP {version}: branch {branch} not in the fixed list; check php.net"
    if parts >= _ver(fixed):
        return f"PHP {version}: at or above the fixed release {fixed}"
    return f"PHP {version}: patch exists, upgrade to {fixed} or later"


@dataclass
class PhpScenario:
    facts: dict
    cases: list[tuple[str, str, Knockout]]   # (layer id, patch status, knockout)


def php2shell_scenario(site: Site) -> PhpScenario:
    facts = load_php2shell()
    cases = []
    for l in site.software_layers:
        if l.kind and "php" in l.kind.lower():
            cases.append((l.id, php_patch_status(l.version, facts), knockout(site, l.id)))
    return PhpScenario(facts, cases)
