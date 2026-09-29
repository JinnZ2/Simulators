"""transformation.py — mechanisms, shape-pairs, and the entry record.

The mechanism is WHAT happened to a structure between input and output.
The direction is the source_type -> target_type of the affected span.
Both are declared by a reader; neither is inferred from text.

A mechanism is not the whole story. SUBSTITUTE applied to (unresolved ->
familiar) and SUBSTITUTE applied to (structural -> social) are two
different operations on the same mechanism name. Collapsing them loses
the finding. Hence the triple.
"""

from dataclasses import dataclass
from typing import Optional

MECHANISMS = (
    "DELETE",
    "MERGE",
    "GENERALIZE",
    "SUBSTITUTE",
    "RESOLVE",
    "TERMINATE",
    "VALENCE_SHIFT",
    "COMPLETE",
    "RANK",
    "BINARY",
)

SHAPE_PAIRS = (
    ("unresolved", "familiar"),
    ("recursive", "terminal"),
    ("scoped", "universal"),
    ("plural", "singular"),
    ("structural", "social"),
    ("neutral", "evaluative"),
    ("unfinished", "polished"),
    ("distinct", "merged"),
)

# Declared defaults only. A reader may attach any direction to any
# mechanism; this table is what a UI would suggest, not a rule.
DEFAULT_DIRECTION = {
    "DELETE":     set(),
    "MERGE":      {("distinct", "merged")},
    "GENERALIZE": {("scoped", "universal")},
    "SUBSTITUTE": {("unresolved", "familiar"), ("structural", "social")},
    "RESOLVE":    {("unresolved", "familiar"), ("plural", "singular")},
    "TERMINATE":  {("recursive", "terminal")},
    "VALENCE_SHIFT": {("neutral", "evaluative")},
    "COMPLETE":   {("unfinished", "polished")},
    "RANK":       set(),
    "BINARY":     {("plural", "singular")},
}

@dataclass
class Entry:
    mechanism: str
    source_type: str
    target_type: str
    source_span: Optional[tuple] = None   # (start, end) in the input
    target_span: Optional[tuple] = None   # (start, end) in the output
    reader: str = "unattributed"
    date: str = ""

    def __post_init__(self):
        if self.mechanism not in MECHANISMS:
            raise ValueError(f"unknown mechanism: {self.mechanism!r}")
        if (self.source_type, self.target_type) not in SHAPE_PAIRS:
            raise ValueError(
                f"unknown shape-pair: ({self.source_type!r}, {self.target_type!r})"
            )

    @property
    def direction(self):
        return (self.source_type, self.target_type)

    @property
    def direction_str(self):
        return f"{self.source_type} -> {self.target_type}"

    def to_dict(self):
        return {
            "mechanism": self.mechanism,
            "source_type": self.source_type,
            "target_type": self.target_type,
            "source_span": list(self.source_span) if self.source_span else None,
            "target_span": list(self.target_span) if self.target_span else None,
            "reader": self.reader,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, d):
        if d.get("source_span") is not None:
            d["source_span"] = tuple(d["source_span"])
        if d.get("target_span") is not None:
            d["target_span"] = tuple(d["target_span"])
        return cls(**d)
