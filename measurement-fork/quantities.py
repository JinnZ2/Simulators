#!/usr/bin/env python3
"""
quantities.py -- what a quantity IS, and when two of them are the same one.

CC0-1.0. stdlib only.

Reconstructed from the call sites in conventional.py, coupling.py and
compare.py, which the drop shipped without this module. The contract is
fully determined by those call sites; the choices this file makes beyond
them are marked below.

THE ONE IDEA
------------
A quantity is not its name. It is the triple

    (base, object_of, normalizer)

and two quantities are the same quantity only when all three match. That is
the whole basis of compare.py's VOID RATIO cell: two arms can both report
"response_magnitude" and be measuring different things, because one is a
property of the organism and the other of the coupling, or because one is
per-unit-stimulus and the other is raw.

This is ../reasoning-gate/'s G-DIM moved one stage earlier. G-DIM voids a
ratio at report time when its operands turn out to belong to different
objects. Carrying object_of in the quantity itself means the mismatch is
visible at DESIGN time, before anyone runs anything -- which is the only
point at which it is cheap to fix.
"""

from __future__ import annotations


def quantity(base, object_of, normalizer=None):
    """
    A quantity's full identity.

      base        what is measured, as a name
      object_of   what it is a property OF -- organism, environment,
                  coupling, instrument. The load-bearing field.
      normalizer  what it is divided by, or None. A raw magnitude and a
                  magnitude-per-unit-stimulus are different quantities.
    """
    if not (isinstance(base, str) and base.strip()):
        raise ValueError("quantity needs a base name")
    if not (isinstance(object_of, str) and object_of.strip()):
        raise ValueError(
            "quantity %r declares no object_of. A number that does not say "
            "what it is a property of cannot be compared with anything."
            % base)
    return {
        "base": base.strip(),
        "object_of": object_of.strip(),
        "normalizer": normalizer.strip() if isinstance(normalizer, str)
        else normalizer,
    }


def probe(arm, pid, q, protocol, reads, blind_to):
    """
    One proposed measurement.

    `blind_to` is required and is not decoration. A probe that cannot say
    what it is blind to has not been thought through, and the blindness map
    is what makes the SOLE REACH cell readable -- an arm reaching a quantity
    alone is only interesting next to what the other arms could not see.
    """
    for name, val in (("protocol", protocol), ("reads", reads),
                      ("blind_to", blind_to)):
        if not (isinstance(val, str) and val.strip()):
            raise ValueError("probe %s: %r is empty" % (pid, name))
    return {
        "arm": arm,
        "pid": pid,
        "quantity": q,
        "protocol": protocol.strip(),
        "reads": reads.strip(),
        "blind_to": blind_to.strip(),
    }


def key(q):
    """Full identity. Same key == same quantity == directly comparable."""
    return (q["base"], q["object_of"], q["normalizer"])


def base_key(q):
    """Name only. Same base with different keys is the VOID RATIO cell."""
    return q["base"]


def render(q):
    """
    Human-readable, and deliberately verbose about object_of.

    [CHOICE] The drop's call sites do not fix this format. It is written to
    put object_of next to the name every time it is printed, because the
    failure this whole module exists to catch is a reader seeing two
    identical names and assuming one quantity.
    """
    text = q["base"]
    if q["normalizer"]:
        text += " / " + q["normalizer"]
    return "%s  [of %s]" % (text, q["object_of"])
