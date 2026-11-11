"""Layer D. Control matrix: what the experimenter holds, varies and perturbs.

Independent of the boundary layer: neither object reads the other.
"""
FIELDS = ("held_constant", "varied", "coupled", "perturbation_magnitude", "perturbation_duration",
          "recovery_conditions", "measurement_frequency", "instrument_sensitivity")


class ControlMatrix:
    def __init__(self, **fields):
        missing = [f for f in FIELDS if f not in fields]
        if missing:
            raise ValueError("control fields %s dropped (write UNDECLARED)" % missing)
        self.fields = {f: fields[f] for f in FIELDS}
        self.extra = {k: v for k, v in fields.items() if k not in FIELDS}

    def get(self, k, default=None):
        return self.fields.get(k, self.extra.get(k, default))

    def as_dict(self):
        d = dict(self.fields)
        d.update(self.extra)
        return d
