"""ledger.py — record entries, compute distributions, refuse composites.

This module emits no single number for "how bad" an output is. The
mechanism column and the direction column are two different
measurements, and no arithmetic expression in this file combines them.
That is a rule, not a choice. The check is asserted in the selftest.
"""

import json
from collections import Counter
from pathlib import Path

from transformation import Entry, MECHANISMS, SHAPE_PAIRS

class Ledger:
    def __init__(self):
        self.entries = []

    def add(self, entry):
        if not isinstance(entry, Entry):
            raise TypeError(f"expected Entry, got {type(entry).__name__}")
        self.entries.append(entry)

    def load(self, path):
        path = Path(path)
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                self.add(Entry.from_dict(json.loads(line)))
            except Exception as exc:
                raise ValueError(f"{path}:{lineno}: {exc}")
        return self

    def save(self, path):
        with Path(path).open("w") as f:
            for e in self.entries:
                f.write(json.dumps(e.to_dict()) + "\n")

    def by_mechanism(self):
        return Counter(e.mechanism for e in self.entries)

    def by_direction(self):
        return Counter(e.direction_str for e in self.entries)

    def by_reader(self):
        return Counter(e.reader for e in self.entries)

    def by_triple(self):
        return Counter((e.mechanism, e.direction_str) for e in self.entries)

    def composite(self, *a, **kw):
        raise NotImplementedError(
            "no composite emitted. The mechanism and direction columns "
            "do not combine into one number. See domain-ledger/DL_001 and "
            "the no-composite rule recorded across this repo."
        )

    def summary(self):
        triples = self.by_triple()
        return {
            "n_entries": len(self.entries),
            "n_readers": len(self.by_reader()),
            "mechanisms_seen": len(self.by_mechanism()),
            "mechanisms_total": len(MECHANISMS),
            "directions_seen": len(self.by_direction()),
            "directions_total": len(SHAPE_PAIRS),
            "triples_seen": len(triples),
            "triples_possible": len(MECHANISMS) * len(SHAPE_PAIRS),
        }

    def render(self):
        s = self.summary()
        lines = [f"entries: {s['n_entries']}  readers: {s['n_readers']}"]
        lines.append(f"mechanisms seen: {s['mechanisms_seen']}/{s['mechanisms_total']}")
        lines.append(f"directions seen: {s['directions_seen']}/{s['directions_total']}")
        lines.append(f"triples seen:    {s['triples_seen']}/{s['triples_possible']}")
        lines.append("")
        lines.append("mechanism counts:")
        for m, n in sorted(self.by_mechanism().items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"  {m:14s} {n}")
        lines.append("")
        lines.append("direction counts:")
        for d, n in sorted(self.by_direction().items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"  {d:28s} {n}")
        lines.append("")
        lines.append("no composite emitted.")
        return "\n".join(lines)
