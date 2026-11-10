#!/usr/bin/env python3
"""channel_chain.py -- a reading record that carries the chain it came through.

CC0. Stdlib only, parses under 3.8. Co-authored (JinnZ2 + Claude), 2026-11-09,
built to WORK ORDER TOOL FINDER Amendment A1 (precision + channel chain) and A2
(reuse Cross-Domain-Toolkit SubstrateReading fields).

No reading here is direct. Every reading passes through a chain of hops:

    sensor -> encoding -> transmission -> decoding -> inference

and a deviation at any hop changes what is "seen". A reading record therefore
carries, per hop:
  - the known deviation sources at that hop (declared by the tool),
  - a known-reference check: a known input injected at that hop and whether
    it came out as expected.
        CHECKED        injected == observed
        CHECK_FAILED   injected and observed differ (the hop deviates)
        UNVERIFIED_HOP no reference check was run for this hop

`chain_class()` of a record is never DIRECT. It is
        VIA_CHECKED_CHAIN    every hop the reading passed through was CHECKED
        VIA_UNVERIFIED_HOP   at least one hop is UNVERIFIED_HOP (named)
        VIA_FAILED_HOP       at least one hop is CHECK_FAILED (named)
A CHECKED chain is still a chain: it says the hops reproduced known inputs on
the checks run, not that this reading is correct.

Record fields: the field names of Cross-Domain-Toolkit
`multi_substrate_calibration.substrate.SubstrateReading` (value,
native_confidence, role, modality, units, correlation_group, timestamp,
provenance), plus `chain`. When a sibling checkout of Cross-Domain-Toolkit is
present (../cross-domain-toolkit, or CROSS_DOMAIN_TOOLKIT_PATH), the field
names are read from that dataclass at import time and compared with the mirror
below; `fields_source()` reports which happened. The record is a plain dict, so
a reading's `value` may be a label (a verdict, a cut status) where
SubstrateReading carries a float. That widening is stated, not hidden: the
toolkit's determinacy gate would refuse such a record, and should.
"""
import os
import sys

HOPS = ("sensor", "encoding", "transmission", "decoding", "inference")
CHECK_STATES = ("CHECKED", "CHECK_FAILED", "UNVERIFIED_HOP")
CHAIN_CLASSES = ("VIA_CHECKED_CHAIN", "VIA_UNVERIFIED_HOP", "VIA_FAILED_HOP")

# Mirror of SubstrateReading's field names, in declaration order. A copy,
# checked against the source whenever the source is reachable.
SUBSTRATE_FIELDS_MIRROR = ("value", "native_confidence", "role", "modality", "units",
                           "correlation_group", "timestamp", "provenance")


def _toolkit_dir():
    env = os.environ.get("CROSS_DOMAIN_TOOLKIT_PATH")
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cand = env or os.path.join(os.path.dirname(here), "cross-domain-toolkit")
    return cand if os.path.isfile(os.path.join(cand, "multi_substrate_calibration", "substrate.py")) else None


def fields_source():
    """('IMPORTED', fields) when read from the toolkit; ('MIRROR', fields) when
    no checkout is reachable; raises if the two disagree (drift)."""
    d = _toolkit_dir()
    if d is None:
        return "MIRROR", SUBSTRATE_FIELDS_MIRROR
    import dataclasses
    sys.path.insert(0, d)
    try:
        from multi_substrate_calibration.substrate import SubstrateReading
    finally:
        sys.path.remove(d)
    got = tuple(f.name for f in dataclasses.fields(SubstrateReading))
    if got != SUBSTRATE_FIELDS_MIRROR:
        raise RuntimeError("SubstrateReading fields drifted: toolkit %s vs mirror %s"
                           % (got, SUBSTRATE_FIELDS_MIRROR))
    return "IMPORTED", got


def reference_check(injected, observed):
    """Compare a known input with what came out. None observed = not run."""
    if observed is None:
        return "UNVERIFIED_HOP"
    return "CHECKED" if observed == injected else "CHECK_FAILED"


def hop(name, deviation_sources, injected=None, observed=None, note=None):
    if name not in HOPS:
        raise ValueError("unknown hop %r; hops are %s" % (name, HOPS))
    state = "UNVERIFIED_HOP" if injected is None else reference_check(injected, observed)
    return {"hop": name, "deviation_sources": list(deviation_sources),
            "reference": None if injected is None else {"injected": injected, "observed": observed},
            "check": state, "note": note}


def reading(value, modality, units, chain, native_confidence=0.0, role="ground",
            correlation_group="", timestamp=None, provenance=None):
    """A record with SubstrateReading's field names plus `chain`.
    native_confidence defaults to 0.0: nothing here claims confidence it did
    not measure."""
    _, names = fields_source()
    rec = dict(zip(names, (value, native_confidence, role, modality, units,
                           correlation_group, timestamp, provenance or {})))
    rec["chain"] = list(chain)
    rec["chain_class"] = chain_class(rec["chain"])
    rec["unverified_hops"] = [h["hop"] for h in rec["chain"] if h["check"] == "UNVERIFIED_HOP"]
    rec["failed_hops"] = [h["hop"] for h in rec["chain"] if h["check"] == "CHECK_FAILED"]
    return rec


def chain_class(chain):
    if not chain:
        return "VIA_UNVERIFIED_HOP"   # an empty chain is unknown, never direct
    if any(h["check"] == "CHECK_FAILED" for h in chain):
        return "VIA_FAILED_HOP"
    if any(h["check"] == "UNVERIFIED_HOP" for h in chain):
        return "VIA_UNVERIFIED_HOP"
    return "VIA_CHECKED_CHAIN"


def render_chain(chain):
    return " -> ".join("%s[%s]" % (h["hop"], h["check"]) for h in chain)


def _checks():
    out = []
    def c(cond, label):
        out.append((bool(cond), label))
    c(reference_check("x", "x") == "CHECKED", "equal reference -> CHECKED")
    c(reference_check("x", "y") == "CHECK_FAILED", "differing reference -> CHECK_FAILED")
    c(reference_check("x", None) == "UNVERIFIED_HOP", "no observation -> UNVERIFIED_HOP")
    ch = [hop("sensor", ["noise"], "a", "a"), hop("decoding", ["asr"])]
    c(chain_class(ch) == "VIA_UNVERIFIED_HOP", "one unchecked hop -> VIA_UNVERIFIED_HOP")
    ch2 = [hop("sensor", [], "a", "a"), hop("decoding", [], "b", "c")]
    c(chain_class(ch2) == "VIA_FAILED_HOP", "failed hop dominates")
    c(chain_class([hop("sensor", [], "a", "a")]) == "VIA_CHECKED_CHAIN", "all checked")
    c(chain_class([]) == "VIA_UNVERIFIED_HOP", "empty chain is not direct")
    c("DIRECT" not in CHAIN_CLASSES, "no DIRECT class exists")
    try:
        hop("retina", [])
        c(False, "unknown hop refused")
    except ValueError:
        c(True, "unknown hop refused")
    src, names = fields_source()
    c(names == SUBSTRATE_FIELDS_MIRROR, "fields from %s match the mirror" % src)
    r = reading("SAID", "text", "label", ch)
    c(set(SUBSTRATE_FIELDS_MIRROR) <= set(r) and r["unverified_hops"] == ["decoding"],
      "reading carries SubstrateReading fields and names the unverified hop")
    c(r["native_confidence"] == 0.0, "no unmeasured confidence")
    return out, src


def main(argv):
    if "--selftest" in argv:
        res, src = _checks()
        for ok, lab in res:
            if not ok:
                print("FAIL:", lab)
        print("fields source: %s" % src)
        print("checks: %d   failed: %d" % (len(res), sum(1 for ok, _ in res if not ok)))
        return 0 if all(ok for ok, _ in res) else 1
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
