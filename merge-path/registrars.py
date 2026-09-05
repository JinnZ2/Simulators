#!/usr/bin/env python3
"""registrars.py -- the shared Registrar model and the registry, one
source of truth for both directions (convert_out, convert_in).

Added over the work order's file list (§6) deliberately, with the reason
stated per §1's "extend if a better case is found": the registry is
shared by both converters, and putting it here keeps it a single source
of truth and avoids a convert_in <-> convert_out import cycle.

CRITICAL egress fact. The work order's §1 requires fetching each
registrar's own specification before mapping. In this environment the
egress proxy is an allowlist: every registrar spec host answered 403 to
CONNECT (probed 2026-09-05T03:30Z: nanopub.net, clinicaltrials.gov,
w3.org among them; the proxy logs the refusals in recentRelayFailures).
So NO spec was fetched, and per §7 every real registrar here is marked
`verified=False`: its atomic-record fields are NOT transcribed from a
spec and NOT fabricated from memory, its converter is NOT-IMPLEMENTED
with that reason, and anything derived from it inherits UNVERIFIED. The
work order's own §1 summaries are carried as candidates only, in the
docs, marked UNVERIFIED -- and §1 itself says do not work from summaries.

What IS implemented and tested is the MACHINERY: the identity registrar
(our format to our format) and a set of MOCK registrars that are
declared test doubles, constructed to exercise each residual class. No
mock is a claim about any real registrar. Stdlib only, parses under 3.9.
"""

from dataclasses import dataclass, field
from typing import Dict, List

# The atomic fields of the falsifier / branch-record format (our format).
FALSIFIER_FIELDS = ("claim", "falsifier", "measured_as", "scope_transform", "branch_record")


class ConversionFailure(Exception):
    """Raised when a conversion cannot be completed honestly -- an ADDED
    target field with no stated origin (§3, S4)."""


class VerdictError(Exception):
    """Raised when a NO-MERGE verdict carries no breaks_at (§0, S5)."""

# Egress-refusal stamp, recorded once, inherited by every real registrar.
EGRESS_REFUSED = ("spec not fetched: egress proxy answered 403 to CONNECT "
                  "(probed 2026-09-05T03:30Z); UNVERIFIED, nothing derived rests on it")


@dataclass
class Slot:
    """How one falsifier field maps into a target registrar slot.
    meaning='different' marks a COERCED mapping (a field written into a
    slot that means something else) -- the dangerous one."""
    target_name: str
    meaning: str = "same"        # "same" | "different"
    flatten: bool = False        # a dict collapsed to a string (recoverable)


@dataclass
class Registrar:
    name: str
    verified: bool               # was the spec fetched and read?
    implemented: bool            # is a converter built?
    spec_url: str = ""
    reason: str = ""             # why not implemented (if so)
    is_mock: bool = False        # a declared test double, not a real registrar
    slots: Dict[str, Slot] = field(default_factory=dict)     # falsifier field -> Slot
    requires: List[str] = field(default_factory=list)        # target fields the registrar demands
    added_origins: Dict[str, str] = field(default_factory=dict)  # required field -> stated origin


# ---------------------------------------------------------------------------
# REAL registrars: all UNVERIFIED (spec unfetched), all NOT-IMPLEMENTED.
# The spec_url is where a fetch would go; it is an identifier, not a fact
# about the record shape. No fields are transcribed here.
# ---------------------------------------------------------------------------
REGISTRARS: Dict[str, Registrar] = {
    "nanopublications": Registrar(
        "nanopublications", verified=False, implemented=False,
        spec_url="https://nanopub.net/ (RDF; W3C provenance PROV-O https://www.w3.org/TR/prov-o/)",
        reason=EGRESS_REFUSED),
    "orkg": Registrar(
        "orkg", verified=False, implemented=False,
        spec_url="https://orkg.org/ (Open Research Knowledge Graph)",
        reason=EGRESS_REFUSED),
    "ro_crate": Registrar(
        "ro_crate", verified=False, implemented=False,
        spec_url="https://www.researchobject.org/ro-crate/",
        reason=EGRESS_REFUSED),
    "clinicaltrials_gov": Registrar(
        "clinicaltrials_gov", verified=False, implemented=False,
        spec_url="https://clinicaltrials.gov/ (FDAAA 801; PRS data element definitions)",
        reason=EGRESS_REFUSED),
    "cipm_cmc": Registrar(
        "cipm_cmc", verified=False, implemented=False,
        spec_url="https://www.bipm.org/ (CIPM MRA; CMC entries in the KCDB)",
        reason=EGRESS_REFUSED),
    "proof_assistant": Registrar(
        "proof_assistant", verified=False, implemented=False,
        spec_url="https://leanprover-community.github.io/ (mathlib) / https://coq.inria.fr/",
        reason=EGRESS_REFUSED),
    "osf_prereg": Registrar(
        "osf_prereg", verified=False, implemented=False,
        spec_url="https://osf.io/prereg/ (OSF preregistration)",
        reason=EGRESS_REFUSED),
}


# ---------------------------------------------------------------------------
# MOCK registrars: declared test doubles for the machinery. Each is built
# to exercise one residual class. None is a claim about any real registrar.
# ---------------------------------------------------------------------------
def identity_registrar() -> Registrar:
    """Our format to our format: every field has a same-meaning slot. The
    S1 lossless round trip runs on this."""
    return Registrar(
        "MOCK_identity", verified=True, implemented=True, is_mock=True,
        slots={f: Slot(f, meaning="same") for f in FALSIFIER_FIELDS})


def drops_branch_registrar() -> Registrar:
    """Has no slot for the branch_record: converting OUT drops it (S2)."""
    return Registrar(
        "MOCK_drops_branch", verified=True, implemented=True, is_mock=True,
        slots={f: Slot(f, meaning="same") for f in FALSIFIER_FIELDS if f != "branch_record"})


def coerces_falsifier_registrar() -> Registrar:
    """Writes the falsifier into a slot declared to mean 'outcome_measure'
    -- a different meaning (S3, COERCED)."""
    s = {f: Slot(f, meaning="same") for f in FALSIFIER_FIELDS}
    s["falsifier"] = Slot("outcome_measure", meaning="different")
    return Registrar("MOCK_coerces_falsifier", verified=True, implemented=True, is_mock=True, slots=s)


def requires_id_registrar(with_origin: bool) -> Registrar:
    """Requires a 'registration_id' the source did not have (S4, ADDED).
    with_origin=False makes the ADDED field originless -> a hard failure."""
    r = Registrar(
        "MOCK_requires_id", verified=True, implemented=True, is_mock=True,
        slots={f: Slot(f, meaning="same") for f in FALSIFIER_FIELDS},
        requires=["registration_id"])
    if with_origin:
        r.added_origins = {"registration_id": "assigned by the registrar at submission"}
    return r


def flattens_measured_registrar() -> Registrar:
    """Collapses measured_as (a dict) to a string slot -- FLATTENED,
    recoverable by a human."""
    s = {f: Slot(f, meaning="same") for f in FALSIFIER_FIELDS}
    s["measured_as"] = Slot("measure_text", meaning="same", flatten=True)
    return Registrar("MOCK_flattens_measured", verified=True, implemented=True, is_mock=True, slots=s)
