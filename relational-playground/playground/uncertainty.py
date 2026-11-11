"""Layer F. Uncertainty matrix: one status, provenance and interval per value.

An unknown never becomes a number. Value.number() raises on any status that
holds no number; nothing in the playground supplies a default.
"""
STATUSES = ("MEASURED", "ESTIMATED", "INFERRED", "ASSUMED", "UNKNOWN", "NOT MEASURED", "EXCLUDED BY DESIGN")
NO_NUMBER = ("UNKNOWN", "NOT MEASURED", "EXCLUDED BY DESIGN")


class UnknownValue(ValueError):
    pass


class Value:
    def __init__(self, value, status, provenance, interval=None):
        if status not in STATUSES:
            raise ValueError("status %r not in %r" % (status, STATUSES))
        if not provenance:
            raise ValueError("every value needs provenance")
        if status in NO_NUMBER and value is not None:
            raise ValueError("%s holds no number; got %r" % (status, value))
        if status not in NO_NUMBER and value is None:
            raise ValueError("%s needs a number" % status)
        self.value, self.status, self.provenance, self.interval = value, status, provenance, interval

    def number(self):
        if self.status in NO_NUMBER:
            raise UnknownValue("%s (%s): no number, and none is supplied" % (self.status, self.provenance))
        return self.value

    def as_dict(self):
        return dict(value=self.value, status=self.status, provenance=self.provenance, interval=self.interval)


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
