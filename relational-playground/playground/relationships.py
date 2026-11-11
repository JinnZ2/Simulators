"""Layer B. Relational matrix. Directed edges; a reverse edge exists only if written."""
CLASSES = ("energy transfer", "matter transfer", "information transfer", "causal interaction",
           "structural dependency", "feedback", "regulatory interaction", "unknown relationship")


class Relationship:
    def __init__(self, src, dst, cls, strength=None, note=""):
        if cls not in CLASSES:
            raise ValueError("class %r not in %r" % (cls, CLASSES))
        self.src, self.dst, self.cls, self.strength, self.note = src, dst, cls, strength, note

    def as_dict(self):
        s = self.strength.as_dict() if hasattr(self.strength, "as_dict") else self.strength
        return dict(src=self.src, dst=self.dst, cls=self.cls, strength=s, note=self.note)


class RelationalMatrix:
    def __init__(self, relationships=()):
        self.rels = list(relationships)

    def add(self, rel):
        self.rels.append(rel)

    def nodes(self):
        return sorted({r.src for r in self.rels} | {r.dst for r in self.rels})

    def out_edges(self, node, cls=None):
        return [r for r in self.rels if r.src == node and (cls is None or r.cls == cls)]

    def reciprocal(self, rel):
        """True only if the reverse edge of the same class was written."""
        return any(r.src == rel.dst and r.dst == rel.src and r.cls == rel.cls for r in self.rels)

    def adjacency(self, cls=None):
        """{src: {dst: strength number}}; raises if a strength is unknown."""
        a = {}
        for r in self.rels:
            if cls is not None and r.cls != cls:
                continue
            s = r.strength.number() if hasattr(r.strength, "number") else r.strength
            if s is None:
                raise ValueError("%s->%s has no strength; none is supplied" % (r.src, r.dst))
            a.setdefault(r.src, {})[r.dst] = s
        return a

    def as_dict(self):
        return [r.as_dict() for r in self.rels]
