"""Layer F. Uncertainty matrix: one status, provenance and interval per value.

An unknown never becomes a number. Value.number() raises on any status that
holds no number; nothing in the playground supplies a default.

ADDITION 4 (EXPIRY). UNKNOWN and NOT MEASURED carry an expiry_condition: the
observation that would end the status. VOID is allowed and is counted as "no
exit defined". ABSENT_AT_SENSITIVITY(<value>) is the status for "looked for at
this sensitivity and not found": a bounded null, not a zero, so it holds no number.
"""
STATUSES = ("MEASURED", "ESTIMATED", "INFERRED", "ASSUMED", "UNKNOWN", "NOT MEASURED", "EXCLUDED BY DESIGN",
            "ABSENT_AT_SENSITIVITY")
NO_NUMBER = ("UNKNOWN", "NOT MEASURED", "EXCLUDED BY DESIGN", "ABSENT_AT_SENSITIVITY")
NEEDS_EXPIRY = ("UNKNOWN", "NOT MEASURED")     # ADDITION 4: these must say what would end them
VOID = "VOID"                                  # allowed; counted as "no exit defined"


class UnknownValue(ValueError):
    pass


class Value:
    def __init__(self, value, status, provenance, interval=None, expiry_condition=None, sensitivity=None):
        if status not in STATUSES:
            raise ValueError("status %r not in %r" % (status, STATUSES))
        if not provenance:
            raise ValueError("every value needs provenance")
        if status in NO_NUMBER and value is not None:
            raise ValueError("%s holds no number; got %r" % (status, value))
        if status not in NO_NUMBER and value is None:
            raise ValueError("%s needs a number" % status)
        if status in NEEDS_EXPIRY and not expiry_condition:
            raise ValueError("%s needs expiry_condition: what observation would end it (write %r if none is defined)" % (status, VOID))
        if status == "ABSENT_AT_SENSITIVITY" and sensitivity is None:
            raise ValueError("ABSENT_AT_SENSITIVITY needs the sensitivity it was looked for at")
        if status != "ABSENT_AT_SENSITIVITY" and sensitivity is not None:
            raise ValueError("sensitivity belongs to ABSENT_AT_SENSITIVITY only")
        self.value, self.status, self.provenance, self.interval = value, status, provenance, interval
        self.expiry_condition, self.sensitivity = expiry_condition, sensitivity

    def label(self):
        return "ABSENT_AT_SENSITIVITY(%s)" % self.sensitivity if self.status == "ABSENT_AT_SENSITIVITY" else self.status

    def number(self):
        if self.status in NO_NUMBER:
            raise UnknownValue("%s (%s): no number, and none is supplied" % (self.status, self.provenance))
        return self.value

    def as_dict(self):
        return dict(value=self.value, status=self.label(), provenance=self.provenance, interval=self.interval,
                    expiry_condition=self.expiry_condition)


class UncertaintyMatrix:
    """name -> Value. resolve() gives the numbers a model may use; it raises on an unknown."""

    def __init__(self, values):
        for k, v in values.items():
            if not isinstance(v, Value):
                raise TypeError("%s: wrap it in Value(value, status, provenance)" % k)
        self.values = dict(values)

    def resolve(self, names=None):
        return {k: self.values[k].number() for k in (names or self.values)}

    def counts(self):
        out = {s: 0 for s in STATUSES}
        for v in self.values.values():
            out[v.status] += 1
        return out

    def expiry_report(self):
        """Every UNKNOWN / NOT MEASURED with its exit; VOID exits are counted, not hidden."""
        rows = [dict(name=k, status=v.status, expiry_condition=v.expiry_condition)
                for k, v in sorted(self.values.items()) if v.status in NEEDS_EXPIRY]
        return dict(rows=rows, open_slots=len(rows), no_exit_defined=sum(1 for r in rows if r["expiry_condition"] == VOID))

    def propagate(self, fn, names):
        """Interval propagation by corner evaluation. Values without an interval are
        listed in 'no_interval' and enter as points."""
        import itertools
        lo_hi, missing = [], []
        for n in names:
            v = self.values[n]
            if v.interval is None:
                missing.append(n)
                lo_hi.append((v.number(),))
            else:
                lo_hi.append(tuple(v.interval))
        outs = [fn(dict(zip(names, c))) for c in itertools.product(*lo_hi)]
        return dict(low=min(outs), high=max(outs), corners=len(outs), no_interval=missing)

    def as_dict(self):
        return {k: v.as_dict() for k, v in self.values.items()}
