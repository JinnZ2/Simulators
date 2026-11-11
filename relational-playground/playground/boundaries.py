"""Layer C. Boundary matrix: the boundary is an experimental variable.

A boundary sorts nodes into interior / interface / exterior. It never touches
the observations. Nothing here picks a boundary: choose() raises.
"""
KINDS = ("fixed", "moving", "distributed", "dynamically generated")
ZONES = ("interior", "interface", "exterior")
FIELDS = ("location", "thickness", "permeability", "exchange_rates", "mobility", "uncertainty")


class BoundaryMatrix:
    def __init__(self, name, kind, zones, **fields):
        if kind not in KINDS:
            raise ValueError("kind %r not in %r" % (kind, KINDS))
        bad = {n: z for n, z in zones.items() if z not in ZONES}
        if bad:
            raise ValueError("zones must be one of %r: %r" % (ZONES, bad))
        missing = [f for f in FIELDS if f not in fields]
        if missing:
            raise ValueError("%s: fields %s dropped (write UNDECLARED)" % (name, missing))
        self.name, self.kind, self.zones = name, kind, dict(zones)
        self.fields = {f: fields[f] for f in FIELDS}

    def zone(self, node):
        if node not in self.zones:
            raise KeyError("%s: node %r has no zone; the boundary does not guess" % (self.name, node))
        return self.zones[node]

    def classify(self, relmatrix):
        """Sort relationships: included (both ends inside or interface), crossing, excluded."""
        inc, cross, exc = [], [], []
        for r in relmatrix.rels:
            a, b = self.zone(r.src) != "exterior", self.zone(r.dst) != "exterior"
            (inc if a and b else cross if a or b else exc).append(r)
        return dict(included=inc, crossing=cross, excluded=exc)

    def as_dict(self):
        return dict(name=self.name, kind=self.kind, zones=self.zones, fields=self.fields)


def compare(b1, b2, relmatrix):
    """Spec section 4: what changes when the boundary changes. Observations are not an input."""
    c1, c2 = b1.classify(relmatrix), b2.classify(relmatrix)
    key = lambda r: (r.src, r.dst, r.cls)
    nodes = sorted(set(b1.zones) | set(b2.zones))
    return dict(
        became_internal=[n for n in nodes if b1.zones.get(n) == "exterior" and b2.zones.get(n) in ("interior", "interface")],
        became_external=[n for n in nodes if b1.zones.get(n) in ("interior", "interface") and b2.zones.get(n) == "exterior"],
        relationships_dropped=sorted(set(map(key, c1["included"] + c1["crossing"])) - set(map(key, c2["included"] + c2["crossing"]))),
        relationships_new=sorted(set(map(key, c2["included"] + c2["crossing"])) - set(map(key, c1["included"] + c1["crossing"]))),
    )


def choose(*_a, **_k):
    raise RuntimeError("no automatic boundary selection: the boundary is declared by the experimenter")
