"""Layer A. System definition. Every field is written; an empty one is refused."""
FIELDS = ("state_variables", "internal_organization", "energy_exchanges", "material_exchanges",
          "information_exchanges", "environmental_dependencies", "timescales")
UNDECLARED = "UNDECLARED"


class SystemDefinition:
    def __init__(self, name, boundaries=None, **fields):
        missing = [f for f in FIELDS if f not in fields]
        if missing:
            raise ValueError("%s: fields %s dropped (write %s)" % (name, missing, UNDECLARED))
        self.name = name
        self.fields = {f: fields[f] for f in FIELDS}
        self.boundaries = dict(boundaries or {})      # name -> BoundaryMatrix; several may coexist

    def add_boundary(self, boundary):
        if boundary.name in self.boundaries:
            raise ValueError("boundary %s exists; keep both under different names" % boundary.name)
        self.boundaries[boundary.name] = boundary

    def undeclared(self):
        return [f for f in FIELDS if self.fields[f] == UNDECLARED]

    def as_dict(self):
        return dict(name=self.name, fields=self.fields, boundaries=sorted(self.boundaries))
