"""Equation substitution interface.

    MODEL(state, environment, relationships, controls, parameters) -> ModelOutput

state         dict name -> number (plus an optional "_config" entry for non-numeric state)
environment   dict: forcing at this time, plus "t", "dt", "rng"
relationships RelationalMatrix or None
controls      ControlMatrix or None
parameters    dict name -> number, already resolved by the uncertainty layer

KIND "rate": state_changes are d/dt and the runner integrates them (RK4).
KIND "step": state_changes are the change over one step of length dt.
A model that cannot say something writes NOT_APPLICABLE; it does not leave the field out.
"""
NOT_APPLICABLE = "NOT_APPLICABLE"
REGISTRY = {}


class ModelOutput:
    FIELDS = ("state_changes", "energy_changes", "relationship_changes", "boundary_behavior",
              "configuration_changes", "uncertainty")

    def __init__(self, state_changes, energy_changes=NOT_APPLICABLE, relationship_changes=NOT_APPLICABLE,
                 boundary_behavior=NOT_APPLICABLE, configuration_changes=NOT_APPLICABLE,
                 uncertainty=NOT_APPLICABLE, transfers=(), new_config=None):
        self.state_changes = state_changes
        self.energy_changes = energy_changes
        self.relationship_changes = relationship_changes
        self.boundary_behavior = boundary_behavior
        self.configuration_changes = configuration_changes
        self.uncertainty = uncertainty
        self.transfers = list(transfers)     # (name, src, dst, rate); None = across the boundary
        self.new_config = new_config


def from_transfers(transfers, variables):
    """state_changes implied by a transfer list. A transfer names where the quantity
    comes from and where it goes; None is the outside."""
    d = {v: 0.0 for v in variables}
    for _name, src, dst, r in transfers:
        if src is not None:
            d[src] -= r
        if dst is not None:
            d[dst] += r
    return d


class Model:
    def __init__(self, name, family, version, fn, kind, requires=(), limitations=()):
        if kind not in ("rate", "step"):
            raise ValueError("kind must be rate or step")
        self.name, self.family, self.version, self.fn, self.kind = name, family, version, fn, kind
        self.requires, self.limitations = tuple(requires), tuple(limitations)
        self.event = None        # optional: event(state, environment, parameters) -> [(name, src, dst, amount)] or None

    def __call__(self, state, environment, relationships, controls, parameters):
        missing = [k for k in self.requires if k not in parameters]
        if missing:
            raise KeyError("%s: parameters %s not supplied; the model does not default them" % (self.name, missing))
        return self.fn(state, environment, relationships, controls, parameters)

    def ident(self):
        return dict(name=self.name, family=self.family, version=self.version, kind=self.kind)


def register(name, family, version, fn, kind="rate", requires=(), limitations=()):
    if name in REGISTRY:
        raise ValueError("model %s already registered; add a new name, keep both" % name)
    REGISTRY[name] = Model(name, family, version, fn, kind, requires, limitations)
    return REGISTRY[name]


def get(name):
    if name not in REGISTRY:
        raise KeyError("no model %r; registered: %s" % (name, sorted(REGISTRY)))
    return REGISTRY[name]


def load_all():
    from . import linear, nonlinear, network, energy, boundary, stochastic, percolation, branching  # noqa: F401
    return sorted(REGISTRY)
