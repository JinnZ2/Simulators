#!/usr/bin/env python3
"""
reading.py -- what a reader commits.  stdlib only, CC0.

A Reading is one reader's independent answer to a Fork.  Four fields:

    verdict     which branch of the fork the reader picks.  categorical.
                axis 1 of spread (weakest signal).

    mechanism   the causal chain the reader believes generates the data.
                represented as a list of edges (src, relation, dst) so
                two readings that name the same chain in different prose
                still compare equal on the DAG.  axis 2 of spread.

    collapse    the experiment the reader proposes to resolve the fork.
                represented as a canonical dict:
                    {"vary": [param, ...], "observe": "quantity",
                     "criterion": "what would decide it"}
                two readings that propose the same experiment agree on
                axis 3 of spread -- operationally near-identical whatever
                they said in prose.  axis 3 is the STRONG axis.

    confidence  self-report in [0, 1].  purely diagnostic; not aggregated.

Reader identity is a separate string (`reader_id`) attached at commit
time by seal.py, not stored inside the Reading itself.
"""

import json
from dataclasses import dataclass, field, asdict
from typing import List, Tuple, Dict


@dataclass
class Reading:
    verdict: str
    mechanism: List[Tuple[str, str, str]]     # (src, relation, dst) edges
    collapse: Dict[str, object]                # {vary, observe, criterion}
    confidence: float = 0.5
    notes: str = ""

    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"confidence in [0,1], got {self.confidence}")
        if not isinstance(self.mechanism, list):
            raise TypeError("mechanism must be a list of 3-tuples")
        for e in self.mechanism:
            if not (isinstance(e, (list, tuple)) and len(e) == 3):
                raise TypeError(f"mechanism edge must be (src, rel, dst); got {e!r}")
        for key in ("vary", "observe", "criterion"):
            if key not in self.collapse:
                raise KeyError(f"collapse must have '{key}' field")

    # normalized comparable payload -- what seal.py hashes
    def canonical(self) -> str:
        return json.dumps({
            "verdict": self.verdict,
            "mechanism": sorted(tuple(e) for e in self.mechanism),
            "collapse": {"vary": sorted(self.collapse["vary"]),
                         "observe": self.collapse["observe"],
                         "criterion": self.collapse["criterion"]},
            "confidence": self.confidence,
            "notes": self.notes,
        }, sort_keys=True, ensure_ascii=False)

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def from_json(cls, s: str) -> "Reading":
        d = json.loads(s)
        # rehydrate mechanism edges as tuples
        d["mechanism"] = [tuple(e) for e in d.get("mechanism", [])]
        return cls(**d)


# --- self-test ------------------------------------------------------------

def _t_construct_and_json_roundtrip():
    r = Reading(
        verdict="basis_echo",
        mechanism=[("basis", "contains", "z/(1+z)"),
                   ("target", "is_defined_as", "CPL")],
        collapse={"vary": ["basis_library"], "observe": "proposed_form",
                  "criterion": "does_form_change_when_z_over_1plusz_removed"},
        confidence=0.9)
    r2 = Reading.from_json(r.to_json())
    assert r2.verdict == r.verdict
    assert r2.mechanism == r.mechanism


def _t_canonical_is_ordering_stable():
    r_a = Reading(
        verdict="X",
        mechanism=[("a", "r", "b"), ("c", "r", "d")],
        collapse={"vary": ["p1", "p2"], "observe": "q", "criterion": "c"})
    r_b = Reading(
        verdict="X",
        mechanism=[("c", "r", "d"), ("a", "r", "b")],
        collapse={"vary": ["p2", "p1"], "observe": "q", "criterion": "c"})
    assert r_a.canonical() == r_b.canonical(), "order in edges/vary should not matter"


def _t_reject_bad_mechanism():
    try:
        Reading(verdict="X", mechanism=[("only_two", "elements")],
                collapse={"vary": [], "observe": "", "criterion": ""})
    except TypeError:
        return
    raise AssertionError


def _t_reject_missing_collapse_key():
    try:
        Reading(verdict="X", mechanism=[], collapse={"vary": []})
    except KeyError:
        return
    raise AssertionError


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn(); print("ok", name)
    print("all pass")


if __name__ == "__main__":
    _run()
