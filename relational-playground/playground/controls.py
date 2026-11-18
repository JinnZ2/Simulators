"""Layer D. Control matrix: what the experimenter holds, varies and perturbs.

Independent of the boundary layer: neither object reads the other.
"""
FIELDS = ("held_constant", "varied", "coupled", "perturbation_magnitude", "perturbation_duration",
          "recovery_conditions", "measurement_frequency", "instrument_sensitivity")

# ADDITION 6. Observer regimes: three separate fields, each declared on its own.
# Definitions: DEFINED 2026-11-11 (chat side; source: Kimi audit, confound C4, 2026-11-10).
#   observer_perturbation  the instrument physically disturbs the system (crystal, rock)
#                          -> answered by metrology and a perturbation budget
#   observer_reactivity    the system changes behaviour because it is observed, without
#                          modelling the observer (animal, plant)
#                          -> answered by blinding, habituation, remote sensing
#   observer_strategy      the system models the evaluation and adjusts to it (AI)
#                          -> answered by hidden evaluations, mechanistic readouts
# Each is dict(state=PRESENT | ABSENT | UNKNOWN, basis=...), or the string UNDECLARED.
OBSERVER_DEFINITIONS = {
    "observer_perturbation": dict(means="the instrument physically disturbs the system", examples="crystal, rock",
                                  answered_by="metrology; perturbation budget"),
    "observer_reactivity": dict(means="the system changes behaviour because it is observed, without modelling the observer",
                                examples="animal, plant", answered_by="blinding; habituation; remote sensing"),
    "observer_strategy": dict(means="the system models the evaluation and adjusts to it", examples="AI",
                              answered_by="hidden evaluations; mechanistic readouts"),
}
OBSERVER_DEFINITION_STATUS = "DEFINED 2026-11-11 (chat side; source: Kimi audit confound C4, 2026-11-10)"
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
