"""Layer D. Control matrix: what the experimenter holds, varies and perturbs.

Independent of the boundary layer: neither object reads the other.
"""
FIELDS = ("held_constant", "varied", "coupled", "perturbation_magnitude", "perturbation_duration",
          "recovery_conditions", "measurement_frequency", "instrument_sensitivity")

# ADDITION 6. Observer regimes: three separate fields, each declared on its own.
#   observer_perturbation  the act of measuring moves the system physically
#   observer_reactivity    the system behaves differently because it is being observed
#   observer_strategy      the system models the observer and acts on that model
# Each is dict(state=PRESENT | ABSENT | UNKNOWN, basis=...), or the string UNDECLARED.
# The reading of the three names is the building session's and is PROPOSED.
OBSERVER_FIELDS = ("observer_perturbation", "observer_reactivity", "observer_strategy")
OBSERVER_STATES = ("PRESENT", "ABSENT", "UNKNOWN")
UNDECLARED = "UNDECLARED"


class ControlMatrix:
    def __init__(self, **fields):
        missing = [f for f in FIELDS if f not in fields]
        if missing:
            raise ValueError("control fields %s dropped (write UNDECLARED)" % missing)
        self.fields = {f: fields[f] for f in FIELDS}
        self.observer = {}
        for f in OBSERVER_FIELDS:
            v = fields.get(f, UNDECLARED)
            if v != UNDECLARED and not (isinstance(v, dict) and v.get("state") in OBSERVER_STATES and v.get("basis")):
                raise ValueError("%s: dict(state in %r, basis=...) or %s" % (f, OBSERVER_STATES, UNDECLARED))
            self.observer[f] = v
        self.extra = {k: v for k, v in fields.items() if k not in FIELDS and k not in OBSERVER_FIELDS}

    def observer_undeclared(self):
        return [f for f in OBSERVER_FIELDS if self.observer[f] == UNDECLARED]

    def get(self, k, default=None):
        return self.fields.get(k, self.extra.get(k, default))

    def as_dict(self):
        d = dict(self.fields)
        d.update(self.observer)
        d.update(self.extra)
        return d
