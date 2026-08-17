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


DEFAULT_SWEEP = "regime.variable"
MIN_SWEEP_LEVELS = 2


def probe(arm, pid, q, protocol, reads, blind_to,
          sweep=DEFAULT_SWEEP, levels=MIN_SWEEP_LEVELS, point_reason=None):
    """
    arm       which generator emitted this
    pid       stable id within the arm
    q         quantity() dict
    protocol  how it would be run
    reads     what the number registers
    sweep     which spec variable this must be run ACROSS. Defaults to
              the spec's regime variable. Pass sweep=None for a point
              probe, and then point_reason is required.
    levels    how many settings of that variable. Minimum 2.

    MF_017: this field did not exist, so 0 of 17 measuring probes could
    declare a sweep -- one schema gap, not seventeen oversights. It is
    load-bearing rather than tidy because the spec's own falsifiers are
    statements about a GRADIENT ("ratio flat across the provisioning
    gradient"), and a probe run at one setting of the control parameter
    cannot participate in a claim about one. The generator could not emit
    a design capable of failing its own falsifier.
    blind_to  what this probe structurally cannot see
    """
    if sweep is None:
        if not (isinstance(point_reason, str) and point_reason.strip()):
            raise ValueError(
                "probe %r declares sweep=None and must give point_reason: "
                "a probe run at one setting cannot participate in a claim "
                "about a gradient, so saying so is the declaration." % pid)
    elif int(levels) < MIN_SWEEP_LEVELS:
        raise ValueError(
            "probe %r declares %d sweep level(s); minimum is %d"
            % (pid, levels, MIN_SWEEP_LEVELS))
    return {
        "arm": arm,
        "id": pid,
        "quantity": q,
        "protocol": protocol,
        "reads": reads,
        "blind_to": blind_to,
        "sweep": None if sweep is None else (sweep, int(levels)),
        "point_reason": point_reason,
    }


def resolve_sweep(p, spec):
    """The declared sweep variable, with DEFAULT_SWEEP resolved against
    the spec's regime. Returns (variable, levels) or None for a point."""
    if not p.get("sweep"):
        return None
    var, levels = p["sweep"]
    if var == DEFAULT_SWEEP:
        var = (spec.get("regime") or {}).get("variable", "")
    return (_norm(var), levels)
