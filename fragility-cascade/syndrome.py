"""
syndrome.py -- parity between peers, without reading content. v1 against SPEC.
CC0. stdlib only. imports clock, entrain, divlog.

    TRACE     vertical    module reading  vs  primary reference     (metrology)
    PARITY    horizontal  module reading  vs  peer module reading   (syndrome)
    PHASE     temporal    time since each module last re-read ref   (zeitgeber)

parity() reads two 12-char digests and two band labels. It never opens the
claim. It never picks a winner. RAISES on cross-target comparison (I2).

trace() would recompute a reading from primary. The spec's Reading holds
`inputs_digest` (the FINGERPRINT), not the raw inputs, so trace requires the
caller to supply the inputs it used. Missing inputs -> None with LOUD (I4).

mesh() runs every pairwise parity within a target, every trace where inputs
are supplied, and one phase check per peripheral. Flat list; no aggregation.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Iterable
import hashlib, json

import clock
import entrain
import divlog


# ------------------------------------------------------------------- reading

@dataclass
class Reading:
    module: str                    # who made the reading
    target: str                    # MUST be one of clock target names
    subject: str                   # claim id / mode name / anchor id
    band: Optional[str]            # FRESH / DECAYING / STALE / EXPIRED / UNDETERMINED
    governing: Optional[str]       # which clock channel governed, or None
    inputs_digest: str             # sha256[:12] of sorted (key, value) pairs
    as_of: str                     # when the reading was taken (explicit; I7)


def digest(inputs: dict) -> str:
    """
    Canonical fingerprint of the inputs a reading was computed from.
    Sorted keys; None rendered as the string "None" so a missing input is
    part of the fingerprint, not invisible. Two readings that both silently
    dropped the same field would collide if None were skipped; here they
    hash the same because the None is part of the canonical form -- exactly
    the shared-blindness case we want to be visible, not hidden.
    """
    canonical = [(k, "None" if inputs[k] is None else repr(inputs[k]))
                 for k in sorted(inputs.keys())]
    blob = json.dumps(canonical, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:12]


# ------------------------------------------------------------------ syndrome

KIND_SAME_INPUTS_DIFF_BAND  = "SAME_INPUTS_DIFF_BAND"    # real module disagreement
KIND_DIFF_INPUTS_DIFF_BAND  = "DIFF_INPUTS_DIFF_BAND"    # separate bucket
KIND_DIFF_INPUTS_SAME_BAND  = "DIFF_INPUTS_SAME_BAND"    # homoplasy analogue
KIND_MISSING                = "MISSING"                  # UNDETERMINED input
KIND_TRACE_DIVERGENCE       = "TRACE_DIVERGENCE"         # drift from primary
KIND_PHASE_DRIFTED          = "PHASE_DRIFTED"
KIND_PHASE_FREE_RUNNING     = "PHASE_FREE_RUNNING"
KIND_PHASE_NEVER            = "PHASE_NEVER"


@dataclass
class Syndrome:
    kind: str
    a: Reading
    b: Optional[Reading] = None    # None for TRACE and PHASE syndromes
    detail: str = ""
    loud: List[str] = field(default_factory=list)


# ------------------------------------------------------- horizontal: parity

def parity(a: Reading, b: Reading) -> Optional[Syndrome]:
    """
    Compare two peer readings. Digests + bands only -- never opens the claim.
    RAISES on cross-target comparison (I2) or subject mismatch.
    Returns None on trivial agreement (same digest AND same band); a Syndrome
    otherwise.
    """
    if a.target != b.target:
        raise ValueError(
            f"cross-target comparison forbidden (I2): "
            f"a.target={a.target!r} vs b.target={b.target!r} -- claim, "
            f"mode_sensitivity, and independence are separate meshes")
    if a.subject != b.subject:
        raise ValueError(
            f"subject mismatch: a.subject={a.subject!r} vs "
            f"b.subject={b.subject!r}")

    # I4: missing input goes LOUD + UNDETERMINED, never silent-agreement
    if a.band == "UNDETERMINED" or b.band == "UNDETERMINED":
        return Syndrome(
            KIND_MISSING, a, b,
            detail=f"a.band={a.band}, b.band={b.band}",
            loud=[f"one or both sides UNDETERMINED -- LOUD, no agreement "
                  "inferred from absence (I4)"])

    same_digest = (a.inputs_digest == b.inputs_digest)
    same_band = (a.band == b.band)

    if same_digest and same_band:
        return None

    if same_digest and not same_band:
        return Syndrome(
            KIND_SAME_INPUTS_DIFF_BAND, a, b,
            detail=f"digests match ({a.inputs_digest}); bands differ "
                   f"({a.band} vs {b.band})")

    if not same_digest and same_band:
        return Syndrome(
            KIND_DIFF_INPUTS_SAME_BAND, a, b,
            detail=f"agreement from different inputs ({a.inputs_digest} vs "
                   f"{b.inputs_digest}) -- homoplasy analogue; logged but not "
                   f"evidence of agreement")

    return Syndrome(
        KIND_DIFF_INPUTS_DIFF_BAND, a, b,
        detail=f"different inputs ({a.inputs_digest} vs {b.inputs_digest}); "
               f"different bands ({a.band} vs {b.band}); separate bucket -- "
               f"NOT module disagreement")


# ------------------------------------------------------- vertical: trace

def trace(r: Reading, now: str,
          inputs: Optional[Dict] = None) -> Optional[Syndrome]:
    """
    Vertical check: recompute the reading from primary and compare bands.

    The Reading holds only `inputs_digest` (the fingerprint), not the raw
    inputs. To recompute, the caller must supply `inputs` -- the same dict
    it hashed into `inputs_digest`. If not supplied, trace returns None with
    LOUD (I4): the check cannot be performed without them.

    On band mismatch, kind=TRACE_DIVERGENCE means the module's own copy of
    the logic (or its inputs) has drifted from the registry.
    """
    if inputs is None:
        return Syndrome(
            KIND_MISSING, r, None,
            detail="trace cannot recompute without raw inputs",
            loud=[f"trace('{r.module}/{r.subject}') called without inputs -- "
                  "LOUD, cannot compare against primary (I4)"])

    # verify the supplied inputs match the reading's declared digest --
    # otherwise the caller is comparing something OTHER than what the module
    # originally read, which is not what trace measures
    if digest(inputs) != r.inputs_digest:
        return Syndrome(
            KIND_MISSING, r, None,
            detail=f"supplied inputs digest != reading.inputs_digest",
            loud=[f"trace inputs' digest {digest(inputs)!r} does not match "
                  f"reading.inputs_digest {r.inputs_digest!r} -- supplied "
                  "inputs are not what was originally read"])

    o = clock.Observation(now=now, **inputs)
    d = clock.decay(o)
    primary_band = d.band.get(r.target, "UNDETERMINED")

    if primary_band == r.band:
        return None
    return Syndrome(
        KIND_TRACE_DIVERGENCE, r, None,
        detail=f"module band={r.band} vs primary band={primary_band} "
               f"(target={r.target})",
        loud=[f"module '{r.module}' band ({r.band}) diverges from primary "
              f"({primary_band}) on target '{r.target}' -- the module's own "
              "copy of the logic has drifted from the registry"])


# --------------------------------------------------------- temporal: mesh

def mesh(readings: List[Reading], now: str,
         inputs_by_reading: Optional[Dict[str, Dict]] = None
         ) -> List[Syndrome]:
    """
    The full mesh: every pairwise parity within a (target, subject) group,
    every trace where inputs are supplied, one phase per registered
    peripheral. Flat list. No aggregation, no counts-as-score (I1).

    inputs_by_reading is keyed by "{module}/{target}/{subject}" ->
    the raw inputs dict; used ONLY by trace (parity never opens content).
    """
    out: List[Syndrome] = []
    ibr = inputs_by_reading or {}

    # group by (target, subject) so parity never crosses targets (I2)
    groups: Dict[tuple, List[Reading]] = {}
    for r in readings:
        groups.setdefault((r.target, r.subject), []).append(r)

    for _, group in groups.items():
        for i, a in enumerate(group):
            for b in group[i + 1:]:
                s = parity(a, b)
                if s is not None:
                    out.append(s)
            key = f"{a.module}/{a.target}/{a.subject}"
            t = trace(a, now, inputs=ibr.get(key))
            if t is not None:
                out.append(t)

    # one phase check per module that has a registered peripheral
    seen_modules = {r.module for r in readings}
    for name in sorted(seen_modules):
        if name not in entrain.PERIPHERALS:
            continue
        ph = entrain.phase(name, now)
        if ph.name == entrain.PHASE_ENTRAINED:
            continue
        # DRIFTED / FREE_RUNNING / NEVER -> surface as a Syndrome, no Reading
        kind_map = {
            entrain.PHASE_DRIFTED: KIND_PHASE_DRIFTED,
            entrain.PHASE_FREE_RUNNING: KIND_PHASE_FREE_RUNNING,
            entrain.PHASE_NEVER: KIND_PHASE_NEVER,
        }
        placeholder = Reading(module=name, target="phase", subject=name,
                              band=None, governing=None, inputs_digest="",
                              as_of=now)
        out.append(Syndrome(
            kind_map[ph.name], placeholder, None,
            detail=f"phase.{ph.name} days_since={ph.days_since_entrained} "
                   f"interval={ph.interval}",
            loud=ph.loud))

    return out
