"""
Canonical quantity structure. Shared by all arms so the comparator
can key on something stable.

CC0-1.0. stdlib only.

A quantity is not a name. It is:

    base        what is being counted
    normalizer  what it is divided by (None = raw)
    object_of   what the number is a property OF
                organism | environment | coupling | instrument

Two probes with the same base and different object_of are NOT
measuring the same thing. That is the void-ratio case and the
comparator flags it rather than merging them.
"""

OBJECTS = ("organism", "environment", "coupling", "instrument")


def quantity(base, object_of, normalizer=None):
    if object_of not in OBJECTS:
        raise ValueError("object_of must be one of %r, got %r"
                         % (OBJECTS, object_of))
    return {
        "base": _norm(base),
        "normalizer": _norm(normalizer) if normalizer else None,
        "object_of": object_of,
    }


def _norm(s):
    return "_".join(str(s).lower().replace("-", " ").replace("/", " ").split())


def key(q):
    """Full identity. Same key = same quantity."""
    return (q["base"], q["normalizer"], q["object_of"])


def base_key(q):
    """Name-level only. Same base_key + different key = void ratio."""
    return q["base"]


def render(q):
    s = q["base"]
    if q["normalizer"]:
        s += " / " + q["normalizer"]
    return "%s  [%s]" % (s, q["object_of"])


def probe(arm, pid, q, protocol, reads, blind_to):
    """
    arm       which generator emitted this
    pid       stable id within the arm
    q         quantity() dict
    protocol  how it would be run
    reads     what the number registers
    blind_to  what this probe structurally cannot see
    """
    return {
        "arm": arm,
        "id": pid,
        "quantity": q,
        "protocol": protocol,
        "reads": reads,
        "blind_to": blind_to,
    }
