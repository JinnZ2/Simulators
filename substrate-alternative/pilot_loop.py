#!/usr/bin/env python3
"""ICS as a coordination substrate, with no monetary terms in the model.

NOT CLAIMED: that ICS is a general substitute for price coordination. This
pilot tests one thing only, whether the loop closes on documented structure
alone. See the ENVELOPE section of README.md before reading any output as a
result about anything outside it.

SOURCE DISCIPLINE. Structure comes from the documents in SOURCES.md and is not
invented. Every structural element carries a provenance state:

    CITED          taken from a source in SOURCES.md
    ASSUMED        doctrine silent on something the model needs
    CARRIED        from memory, no citation confirmed. Not a citation.
    NOT_ACTIVATED  doctrine present, doctrine itself provides for non-activation
    EXCLUDED       doctrine present, a spec requirement excludes it

Every CITED element in this build is VERIFIED LOCATOR / UNVERIFIED SECTION: the
documents resolve, and their sections were not read by the party that wrote this
model, whose network cannot reach the host. `section_verified` is False on every
row and SOURCES.md V-2 says what would settle it.

EXCLUDED names the requirement that excluded it and what was omitted, and a run
that carries one reports it at the TOP of the output. This build uses EXCLUDED
zero times; the zero is printed rather than left silent, and the selftest shows
the state is reachable.

THE LOOP:

    resource typing         kind, capability, quantity; catalog supplied per
                            scenario. A kind the catalog cannot type returns
                            UNTYPED rather than being typed by guesswork.
    capacity declarations   who has what, declared
    need declarations       who needs what, declared
    assignment              capacity meets need, logged
    span of control         assignment limits per node, from params
    lag tracking            declaration -> assignment -> arrival, three stages

UNMET and UNTYPED are return values, not errors. Nothing here raises on a need
that goes unmet or a resource doctrine cannot type; both are results and both
are reported with a reason.

NO MONETARY VOCABULARY IN THE MODEL. `monetary_scan()` reads this file's own
AST and fails the run if a money-frame token appears in model logic or model
vocabulary. It is scoped to identifiers and model data, not to prose and not to
structural identifiers carried from cited doctrine; those go on
SCANNER_EXEMPTIONS and every entry there carries its citation. The lexicon is
IMPORTED from frame_audit.py rather than copied, so there is one lexicon.

stdlib only, CC0, runs on a phone.
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import os
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple

import frame_audit

SCHEMA_VERSION = "1.0"
HERE = os.path.dirname(os.path.abspath(__file__))


class Provenance(str, Enum):
    CITED = "CITED"
    ASSUMED = "ASSUMED"
    CARRIED = "CARRIED"
    NOT_ACTIVATED = "NOT_ACTIVATED"
    EXCLUDED = "EXCLUDED"


class Activation(str, Enum):
    ACTIVATED = "ACTIVATED"
    NOT_ACTIVATED = "NOT_ACTIVATED"


class UnmetReason(str, Enum):
    NO_CAPACITY_DECLARED = "no capacity of that kind was declared anywhere"
    CAPACITY_EXHAUSTED = "declared capacity of that kind ran out"
    SPAN_OF_CONTROL_REACHED = "every node holding that kind is at its span limit"
    CAPABILITY_BELOW_NEED = "declared capability does not meet the declared need"
    NEED_UNTYPED = "the need could not be typed, so nothing was matched to it"


class UntypedReason(str, Enum):
    KIND_NOT_IN_CATALOG = "kind is absent from the supplied typing catalog"
    CAPABILITY_NOT_DECLARED = "no capability declared and the catalog requires one"
    CATALOG_ABSENT = "no typing catalog was supplied with the scenario"


@dataclass(frozen=True)
class Element:
    """One structural element, with where it came from."""

    id: str
    title: str
    provenance: Provenance
    source_id: Optional[str]
    section_verified: bool
    note: str
    activation: Optional[Activation] = None
    excluded_by: Optional[str] = None
    omitted: Optional[str] = None

    def __post_init__(self) -> None:
        if self.provenance is Provenance.EXCLUDED:
            if not self.excluded_by or not self.omitted:
                raise ValueError(
                    "EXCLUDED must name the requirement that excluded it and "
                    "what was omitted: %s" % self.id)
        if self.provenance is Provenance.CITED and not self.source_id:
            raise ValueError("CITED must name a source id: %s" % self.id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id, "title": self.title,
            "provenance": self.provenance.value, "source_id": self.source_id,
            "section_verified": self.section_verified, "note": self.note,
            "activation": self.activation.value if self.activation else None,
            "excluded_by": self.excluded_by, "omitted": self.omitted,
        }


# The structure. Nothing here is invented; see SOURCES.md for the documents and
# for the citation-depth rule that puts section_verified False on every row.
ICS_STRUCTURE: Tuple[Element, ...] = (
    Element("E-CMD", "Command / Incident Commander", Provenance.CITED,
            "S-ICS-ORG", False,
            "the incident has one Incident Commander; command is the function "
            "that sets objectives for the operational period",
            Activation.ACTIVATED),
    Element("E-OPS", "Operations Section", Provenance.CITED, "S-ICS-ORG", False,
            "carries out the objectives; in this pilot it is where an "
            "assignment is delivered from", Activation.ACTIVATED),
    Element("E-PLN", "Planning Section", Provenance.CITED, "S-ICS-ORG", False,
            "collects declarations and holds resource status; in this pilot it "
            "is where capacity and need declarations land",
            Activation.ACTIVATED),
    Element("E-LOG", "Logistics Section", Provenance.CITED, "S-ICS-ORG", False,
            "obtains and moves resources; in this pilot it is where an "
            "assignment becomes an arrival after a lag", Activation.ACTIVATED),
    Element("E-FIN", "Finance/Administration Section", Provenance.NOT_ACTIVATED,
            "S-ICS-ORG", False,
            "doctrine provides for its non-activation: not all incidents "
            "require a Finance/Administration Section; it is activated only "
            "when involved agencies have a specific need for finance services. "
            "It is represented here and is not deleted. This pilot models the "
            "documented non-activation state.",
            Activation.NOT_ACTIVATED),
    Element("E-INT", "Intelligence/Investigations Function",
            Provenance.NOT_ACTIVATED, "S-ICS-ORG", False,
            "a sixth function, used only when the incident requires it; "
            "represented, not activated, in this pilot",
            Activation.NOT_ACTIVATED),
    Element("E-SPAN", "Span of control", Provenance.ASSUMED, None, False,
            "doctrine states that a supervisor oversees a bounded number of "
            "subordinates. The model does not hardcode a doctrinal figure: the "
            "limit per node is supplied in params. A commonly stated range is "
            "recorded as CARRIED in E-SPAN-RANGE and is read by nothing."),
    Element("E-SPAN-RANGE", "Span of control, the commonly stated range",
            Provenance.CARRIED, None, False,
            "three to seven, with five often given as the working figure. "
            "CARRIED from memory, not a citation, and no code path reads it. "
            "SOURCES.md V-3 says what would move it to CITED."),
    Element("E-TYPE", "Resource typing by kind and capability", Provenance.CITED,
            "S-NIMS3", False,
            "resources are described by what they are and what they can do, "
            "not by a number attached to them. The typing catalog itself is "
            "not held here and is supplied per scenario; see SOURCES.md V-4."),
    Element("E-PERIOD", "Operational period", Provenance.CITED, "S-ICS-REV",
            False,
            "the cycle the incident is planned and worked in; this loop runs "
            "one period per tick", Activation.ACTIVATED),
    Element("E-MATCH", "The assignment rule", Provenance.ASSUMED, None, False,
            "doctrine places priorities in the incident action plan and does "
            "not supply a matching algorithm. The model supplies one and says "
            "so: declared priority first, then shortest arrival lag, then node "
            "id for determinism. No quantity is compared across unlike kinds."),
    Element("E-SPEED", "Travel time from distance", Provenance.ASSUMED, None,
            False,
            "doctrine is silent on how long a distance takes. The scenario "
            "supplies time_per_distance_unit and the model multiplies."),
)

# Structural identifiers carried from cited doctrine that the monetary scanner
# must not fail the run on. Every entry carries its citation. The dispatch
# requires the list; whether any entry is used is measured and printed.
SCANNER_EXEMPTIONS: Tuple[Tuple[str, str, str], ...] = (
    ("Finance", "S-ICS-ORG",
     "section name in the cited ICS General Staff structure, element E-FIN"),
    ("Administration", "S-ICS-ORG",
     "section name in the cited ICS General Staff structure, element E-FIN"),
)


# ------------------------------------------------------------ declarations

@dataclass(frozen=True)
class CapacityDeclaration:
    node: str
    kind: str
    capability: int
    quantity: int
    t_declared: int

    def to_dict(self) -> Dict[str, Any]:
        return {"node": self.node, "kind": self.kind,
                "capability": self.capability, "quantity": self.quantity,
                "t_declared": self.t_declared}


@dataclass(frozen=True)
class NeedDeclaration:
    node: str
    kind: str
    capability: int
    quantity: int
    t_declared: int
    priority: Optional[int]

    def to_dict(self) -> Dict[str, Any]:
        return {"node": self.node, "kind": self.kind,
                "capability": self.capability, "quantity": self.quantity,
                "t_declared": self.t_declared, "priority": self.priority}


@dataclass(frozen=True)
class Untyped:
    """A resource doctrine as held here cannot type. A result, not an error."""

    resource: str
    reason: UntypedReason
    node: str
    side: str

    def to_dict(self) -> Dict[str, Any]:
        return {"resource": self.resource, "reason": self.reason.name,
                "reason_text": self.reason.value, "node": self.node,
                "side": self.side}


@dataclass(frozen=True)
class Unmet:
    """A declared need nothing was matched to. A result, not an error."""

    need: str
    quantity: int
    reason: UnmetReason

    def to_dict(self) -> Dict[str, Any]:
        return {"need": self.need, "quantity": self.quantity,
                "reason": self.reason.name, "reason_text": self.reason.value}


@dataclass(frozen=True)
class Assignment:
    need_node: str
    capacity_node: str
    kind: str
    quantity: int
    t_declared: int
    t_assigned: int
    t_arrived: int

    # Plain methods, not decorated. The monetary scanner fired on the builtin
    # decorator name, which is in the ownership lexicon, and the constraint is
    # easier to satisfy than to widen the exemption list for. Recorded because
    # it is the scanner shaping the model's surface, which is the point of it.
    def lag_to_assignment(self) -> int:
        return self.t_assigned - self.t_declared

    def lag_to_arrival(self) -> int:
        return self.t_arrived - self.t_declared

    def to_dict(self) -> Dict[str, Any]:
        return {"need_node": self.need_node,
                "capacity_node": self.capacity_node, "kind": self.kind,
                "quantity": self.quantity, "t_declared": self.t_declared,
                "t_assigned": self.t_assigned, "t_arrived": self.t_arrived,
                "lag_to_assignment": self.lag_to_assignment(),
                "lag_to_arrival": self.lag_to_arrival()}


@dataclass
class LoopResult:
    schema_version: str
    scenario: str
    assignments: List[Assignment] = field(default_factory=list)
    unmet: List[Unmet] = field(default_factory=list)
    untyped: List[Untyped] = field(default_factory=list)
    lag_by_node: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    assignment_rule: str = ""
    span_limits: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "scenario": self.scenario,
            "assignments": [a.to_dict() for a in self.assignments],
            "unmet": [u.to_dict() for u in self.unmet],
            "untyped": [u.to_dict() for u in self.untyped],
            "lag_by_node": self.lag_by_node,
            "assignment_rule": self.assignment_rule,
            "span_limits": dict(self.span_limits),
            "structure": [e.to_dict() for e in ICS_STRUCTURE],
        }


# ------------------------------------------------------------------- typing

def type_resource(kind: str, capability: Optional[int], catalog: Dict[str, Any],
                  node: str, side: str) -> Optional[Untyped]:
    """None when the catalog types it. An Untyped result when it cannot."""
    if not catalog:
        return Untyped(kind, UntypedReason.CATALOG_ABSENT, node, side)
    if kind not in catalog:
        return Untyped(kind, UntypedReason.KIND_NOT_IN_CATALOG, node, side)
    entry = catalog[kind]
    if entry.get("capability_required") and capability is None:
        return Untyped(kind, UntypedReason.CAPABILITY_NOT_DECLARED, node, side)
    return None


# --------------------------------------------------------------------- loop

def run_loop(params: Dict[str, Any]) -> LoopResult:
    """One operational period. Returns results; raises on nothing it measures."""
    scenario = str(params.get("scenario", "unnamed"))
    catalog = params.get("typing_catalog") or {}
    distances = params.get("distances") or {}
    per_unit = params.get("time_per_distance_unit", 1)
    default_span = params.get("default_span_limit", 5)
    span_limits: Dict[str, int] = {}
    for n in params.get("nodes", []):
        span_limits[str(n.get("id"))] = int(n.get("span_limit", default_span))

    caps: List[CapacityDeclaration] = []
    untyped: List[Untyped] = []
    for c in params.get("capacities", []):
        node = str(c["node"])
        kind = str(c["kind"])
        cap = c.get("capability")
        problem = type_resource(kind, cap, catalog, node, "capacity")
        if problem is not None:
            untyped.append(problem)
            continue
        caps.append(CapacityDeclaration(node, kind, int(cap or 0),
                                        int(c["quantity"]),
                                        int(c.get("t_declared", 0))))

    needs: List[NeedDeclaration] = []
    untyped_need_nodes = set()
    for n in params.get("needs", []):
        node = str(n["node"])
        kind = str(n["kind"])
        cap = n.get("capability")
        problem = type_resource(kind, cap, catalog, node, "need")
        if problem is not None:
            untyped.append(problem)
            untyped_need_nodes.add((node, kind))
            continue
        needs.append(NeedDeclaration(node, kind, int(cap or 0),
                                     int(n["quantity"]),
                                     int(n.get("t_declared", 0)),
                                     n.get("priority")))

    remaining: Dict[Tuple[str, str], int] = {}
    capability_of: Dict[Tuple[str, str], int] = {}
    for c in caps:
        key = (c.node, c.kind)
        remaining[key] = remaining.get(key, 0) + c.quantity
        capability_of[key] = max(capability_of.get(key, 0), c.capability)

    assigned_count: Dict[str, int] = {}
    rule = ("declared priority first, then shortest arrival lag, then node id. "
            "ASSUMED: doctrine places priorities in the incident action plan "
            "and supplies no matching algorithm (element E-MATCH).")

    def travel(a: str, b: str) -> int:
        d = distances.get("%s|%s" % (a, b), distances.get("%s|%s" % (b, a)))
        if d is None:
            return 0
        return int(round(float(d) * float(per_unit)))

    ordered = sorted(
        needs,
        key=lambda n: (n.priority if n.priority is not None else 10 ** 6,
                       n.t_declared, n.node, n.kind))

    assignments: List[Assignment] = []
    unmet: List[Unmet] = []
    for need in ordered:
        outstanding = need.quantity
        holders = [k for k in remaining if k[1] == need.kind and remaining[k] > 0]
        if not holders:
            any_kind = [k for k in capability_of if k[1] == need.kind]
            reason = (UnmetReason.CAPACITY_EXHAUSTED if any_kind
                      else UnmetReason.NO_CAPACITY_DECLARED)
            unmet.append(Unmet("%s:%s" % (need.node, need.kind), outstanding,
                               reason))
            continue
        able = [k for k in holders if capability_of[k] >= need.capability]
        if not able:
            unmet.append(Unmet("%s:%s" % (need.node, need.kind), outstanding,
                               UnmetReason.CAPABILITY_BELOW_NEED))
            continue
        able.sort(key=lambda k: (travel(k[0], need.node), k[0]))
        blocked_by_span = False
        for key in able:
            if outstanding <= 0:
                break
            holder = key[0]
            if assigned_count.get(holder, 0) >= span_limits.get(
                    holder, default_span):
                blocked_by_span = True
                continue
            moved = min(outstanding, remaining[key])
            t_assigned = need.t_declared + 1
            t_arrived = t_assigned + travel(holder, need.node)
            assignments.append(Assignment(need.node, holder, need.kind, moved,
                                          need.t_declared, t_assigned,
                                          t_arrived))
            remaining[key] -= moved
            assigned_count[holder] = assigned_count.get(holder, 0) + 1
            outstanding -= moved
        if outstanding > 0:
            reason = (UnmetReason.SPAN_OF_CONTROL_REACHED if blocked_by_span
                      else UnmetReason.CAPACITY_EXHAUSTED)
            unmet.append(Unmet("%s:%s" % (need.node, need.kind), outstanding,
                               reason))

    for node, kind in sorted(untyped_need_nodes):
        unmet.append(Unmet("%s:%s" % (node, kind), 0,
                           UnmetReason.NEED_UNTYPED))

    lag: Dict[str, Dict[str, Any]] = {}
    for n in params.get("nodes", []):
        nid = str(n.get("id"))
        mine = [a for a in assignments if a.need_node == nid]
        if mine:
            lag[nid] = {
                "assignments": len(mine),
                "lag_to_assignment_max": max(a.lag_to_assignment() for a in mine),
                "lag_to_arrival_max": max(a.lag_to_arrival() for a in mine),
                "lag_to_arrival_min": min(a.lag_to_arrival() for a in mine),
            }
        else:
            # No assignment is not a lag of zero. It is an absent measurement.
            lag[nid] = {"assignments": 0, "lag_to_assignment_max": None,
                        "lag_to_arrival_max": None, "lag_to_arrival_min": None}

    return LoopResult(SCHEMA_VERSION, scenario, assignments, unmet, untyped,
                      lag, rule, span_limits)


# ---------------------------------------------------------- monetary scan

@dataclass
class ScanHit:
    name: str
    token: str
    frame: str
    where: str


def _docstring_nodes(tree: ast.AST) -> set:
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef,
                          ast.AsyncFunctionDef)):
            body = getattr(n, "body", None)
            if body and isinstance(body[0], ast.Expr) and \
                    isinstance(body[0].value, ast.Constant) and \
                    isinstance(body[0].value.value, str):
                out.add(id(body[0].value))
    return out


def monetary_scan(path: Optional[str] = None) -> Dict[str, Any]:
    """Money-frame tokens in model logic and model vocabulary.

    Scoped to identifiers and to model data strings. Prose is counted on its
    own line rather than silently dropped, so the exemption is measured.
    Structural identifiers carried from cited doctrine are exempt, and every
    exemption carries its citation.
    """
    path = path or os.path.abspath(__file__)
    source = io.open(path, encoding="utf-8").read()
    tree = ast.parse(source)
    skip = _docstring_nodes(tree)
    exempt_words = set(w.lower() for w, _s, _n in SCANNER_EXEMPTIONS)

    # SCOPING, declared. The scanner reads the vocabulary the model DECLARES,
    # plus its data strings. It does not read attribute ACCESSES, because
    # `x.value` on a stdlib Enum is language surface rather than model
    # vocabulary, in the same category as `.values()` on a dict. A
    # model-defined field named for money is still caught, at the point the
    # model defines it, which is where the model's vocabulary is set. The
    # narrowing is stated here rather than left as an unexplained absence, and
    # the selftest plants a monetary field definition to show it is caught.
    names: List[Tuple[str, str]] = []
    prose_chars = 0
    for n in ast.walk(tree):
        if isinstance(n, ast.Name):
            names.append((n.id, "identifier"))
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.append((n.name, "function"))
        elif isinstance(n, ast.ClassDef):
            names.append((n.name, "class"))
        elif isinstance(n, ast.arg):
            names.append((n.arg, "argument"))
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            names.append((n.target.id, "declared_field"))
        elif isinstance(n, ast.Constant) and isinstance(n.value, str):
            if id(n) in skip:
                prose_chars += len(n.value)
            else:
                names.append((n.value, "model_string"))

    hits: List[ScanHit] = []
    exempted = 0
    for text, where in names:
        probe = text.replace("_", " ")
        result = frame_audit.audit(probe)
        for h in result.hits:
            if h.token.lower() in exempt_words:
                exempted += 1
                continue
            hits.append(ScanHit(text, h.token, h.frame, where))
    return {"path": os.path.basename(path), "hits": [h.__dict__ for h in hits],
            "clean": not hits, "exemptions_used": exempted,
            "exemptions_declared": len(SCANNER_EXEMPTIONS),
            "prose_chars_not_scanned": prose_chars}


# ------------------------------------------------------------------ render

def provenance_report() -> str:
    lines = []
    excluded = [e for e in ICS_STRUCTURE if e.provenance is Provenance.EXCLUDED]
    lines.append("EXCLUDED ELEMENTS: %d" % len(excluded))
    for e in excluded:
        lines.append("  %s %s" % (e.id, e.title))
        lines.append("      excluded by: %s" % e.excluded_by)
        lines.append("      omitted:     %s" % e.omitted)
    if not excluded:
        lines.append("  none. The zero is printed rather than left silent.")
    lines.append("")
    lines.append("STRUCTURE  (section_verified is False on every CITED row; "
                 "see SOURCES.md V-2)")
    for e in ICS_STRUCTURE:
        lines.append("  %-13s %-14s src=%-11s sect_ok=%-5s %s"
                     % (e.id, e.provenance.value, e.source_id or "-",
                        e.section_verified, e.title))
    return "\n".join(lines)


def not_claimed_text() -> str:
    """The disclaimer, read from this module's own docstring.

    It is not a string literal in the body on purpose. The sentence names the
    frame it disclaims, so as a model data string it would trip the scanner on
    a use-mention: the model saying what it is NOT about. Docstrings are
    already declared as prose and counted on their own line, so that is where
    the one sentence of this shape lives.
    """
    doc = __doc__ or ""
    for para in doc.split("\n\n"):
        if para.strip().startswith("NOT CLAIMED"):
            return " ".join(para.split())
    return "NOT CLAIMED paragraph not found in the module docstring."


def render(result: LoopResult, scan: Dict[str, Any]) -> str:
    lines = [provenance_report(), ""]
    lines.append("MONETARY SCAN  clean=%s  hits=%d  exemptions_declared=%d  "
                 "exemptions_used=%d  prose_chars_not_scanned=%d"
                 % (scan["clean"], len(scan["hits"]),
                    scan["exemptions_declared"], scan["exemptions_used"],
                    scan["prose_chars_not_scanned"]))
    for h in scan["hits"]:
        lines.append("    %s  token=%s frame=%s where=%s"
                     % (h["name"], h["token"], h["frame"], h["where"]))
    lines.append("")
    lines.append("SCENARIO: %s" % result.scenario)
    lines.append("assignment rule: %s" % result.assignment_rule)
    lines.append("")
    lines.append("ASSIGNMENT LOG (%d)" % len(result.assignments))
    if not result.assignments:
        lines.append("  none")
    for a in result.assignments:
        lines.append("  %-8s <- %-8s %-14s qty=%-5d lag_assign=%-3d "
                     "lag_arrive=%d"
                     % (a.need_node, a.capacity_node, a.kind, a.quantity,
                        a.lag_to_assignment(), a.lag_to_arrival()))
    lines.append("")
    lines.append("UNMET (%d)   a result, not an error" % len(result.unmet))
    if not result.unmet:
        lines.append("  none")
    for u in result.unmet:
        lines.append("  %-20s qty=%-5d %s" % (u.need, u.quantity, u.reason.name))
        lines.append("      %s" % u.reason.value)
    lines.append("")
    lines.append("UNTYPED (%d)   a result, not an error" % len(result.untyped))
    if not result.untyped:
        lines.append("  none")
    for u in result.untyped:
        lines.append("  %-16s %-8s %-8s %s"
                     % (u.resource, u.node, u.side, u.reason.name))
        lines.append("      %s" % u.reason.value)
    lines.append("")
    lines.append("LAG PER NODE   (None is an absent measurement, not a zero)")
    for nid in sorted(result.lag_by_node):
        d = result.lag_by_node[nid]
        lines.append("  %-8s assignments=%-3d to_assignment_max=%-6s "
                     "to_arrival_min=%-6s to_arrival_max=%s"
                     % (nid, d["assignments"], d["lag_to_assignment_max"],
                        d["lag_to_arrival_min"], d["lag_to_arrival_max"]))
    lines.append("")
    lines.append("span limits: %s" % json.dumps(result.span_limits,
                                                sort_keys=True))
    lines.append("")
    lines.append(not_claimed_text())
    lines.append("See README.md, ENVELOPE section.")
    return "\n".join(lines)


def load_params(path: str) -> Dict[str, Any]:
    return json.loads(io.open(path, encoding="utf-8").read())


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="ICS as a coordination substrate. No monetary terms in "
                    "the model; the run fails if any appear.")
    p.add_argument("params", nargs="?",
                   default=os.path.join(HERE, "params", "baseline.json"))
    p.add_argument("--json", action="store_true")
    p.add_argument("--provenance", action="store_true")
    p.add_argument("--scan-only", action="store_true")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.provenance:
        print(provenance_report())
        return 0
    scan = monetary_scan()
    if args.scan_only:
        print(json.dumps(scan, indent=2, sort_keys=True))
        return 0 if scan["clean"] else 1
    if not scan["clean"]:
        # The dispatch requires this: the run FAILS, it does not merely flag.
        sys.stderr.write(
            "MONETARY VOCABULARY IN THE MODEL. The run is refused.\n")
        for h in scan["hits"]:
            sys.stderr.write("  %s  token=%s frame=%s where=%s\n"
                             % (h["name"], h["token"], h["frame"], h["where"]))
        return 1
    result = run_loop(load_params(args.params))
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    else:
        print(render(result, scan))
    return 0


def selftest() -> int:
    from selftest_pilot import run
    return run()


if __name__ == "__main__":
    sys.exit(main())
