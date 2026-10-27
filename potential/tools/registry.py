"""registry.py — a per-reader register of transformation entries across
folders, in one file.

This is a registry, not a claim about any model or session. It records
which transformations were observed by which reader, at which folder,
on which date. It computes distributions and refuses to compute a
composite. It has no verdict vocabulary for a model, a session, or a
party.

It is deliberately a different object from any single folder's ledger:
a Ledger holds entries produced by one workflow; a Registry holds
entries produced by many, from anywhere in the tree, so the same
mechanism vocabulary can be counted across contexts without being
collapsed.
"""

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# Mechanism and shape-pair vocabularies are declared here so the
# registry can validate without importing any folder. This is a
# deliberate duplication: a registry that imports a folder cannot
# record entries from a folder that has been renamed or removed",.
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

FOLDERS_SEEN = set()  # recorded at add(), reported, never restricted

@dataclass
class RegEntry:
    folder: str
    mechanism: str
    source_type: str
    target_type: str
    source_span: Optional[tuple] = None
    target_span: Optional[tuple] = None
    reader: str = "unattributed"
    date: str = ""

    def __post_init__(self):
        if not self.folder or not self.folder.strip():
            raise ValueError("RegEntry requires a folder")
        if self.mechanism not in MECHANISMS:
            raise ValueError(f"unknown mechanism: {self.mechanism!r}")
        if (self.source_type, self.target_type) not in SHAPE_PAIRS:
            raise ValueError(
                f"unknown shape-pair: ({self.source_type!r}, {self.target_type!r})"
            )

    @property
    def direction_str(self):
        return f"{self.source_type} -> {self.target_type}"

    def to_dict(self):
        return {
            "folder": self.folder,
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

    @classmethod
    def from_vector(cls, folder, vector_dict):
        """Accept a potential.Vector.to_dict() payload as entry sources."""
        reader = vector_dict.get("reader", "unattributed")
        date = vector_dict.get("date", "")
        out = []
        for key, count in vector_dict.get("cells", {}).items():
            mech, dir_s = key.split("|", 1)
            src, tgt = dir_s.split(" -> ", 1)
            for _ in range(int(count)):
                out.append(cls(
                    folder=folder,
                    mechanism=mech,
                    source_type=src,
                    target_type=tgt,
                    reader=reader,
                    date=date,
                ))
        return out


class Registry:
    def __init__(self):
        self.entries = []

    def add(self, entry):
        if not isinstance(entry, RegEntry):
            raise TypeError(f"expected RegEntry, got {type(entry).__name__}")
        self.entries.append(entry)
        FOLDERS_SEEN.add(entry.folder)

    def extend(self, entries):
        for e in entries:
            self.add(e)

    def load(self, path):
        path = Path(path)
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                self.add(RegEntry.from_dict(json.loads(line)))
            except Exception as exc:
                raise ValueError(f"{path}:{lineno}: {exc}")
        return self

    def save(self, path):
        with Path(path).open("w") as f:
            for e in self.entries:
                f.write(json.dumps(e.to_dict()) + "\n")

    # -- readouts ---------------------------------------------------------

    def by_folder(self):
        return Counter(e.folder for e in self.entries)

    def by_mechanism(self):
        return Counter(e.mechanism for e in self.entries)

    def by_direction(self):
        return Counter(e.direction_str for e in self.entries)

    def by_reader(self):
        return Counter(e.reader for e in self.entries)

    def by_folder_mechanism(self):
        """Nested distribution: folder -> mechanism -> count."""
        out = {}
        for e in self.entries:
            out.setdefault(e.folder, Counter())[e.mechanism] += 1
        return out

    def by_folder_direction(self):
        out = {}
        for e in self.entries:
            out.setdefault(e.folder, Counter())[e.direction_str] += 1
        return out

    def readers_in_folder(self, folder):
        return set(e.reader for e in self.entries if e.folder == folder)

    # -- refusals ---------------------------------------------------------

    def composite(self, *a, **kw):
        raise NotImplementedError(
            "no composite emitted. Mechanism and direction are two "
            "measurements. See domain-ledger/DL_001 and the no-composite "
            "rule recorded across this repo."
        )

    def rank_folders(self, *a, **kw):
        raise NotImplementedError(
            "no folder ranking. A folder with many recorded entries is "
            "not worse than one with few; it may be more audited, or "
            "more audited per entry. The registry reports counts and "
            "refuses to order them."
        )

    def verdict_on(self, subject, *a, **kw):
        raise NotImplementedError(
            "no verdict on a model, session, reader, or folder. A verdict "
            "is a reading performed by a party at a moment; the registry "
            "holds readings, not verdicts."
        )

    # -- render -----------------------------------------------------------

    def summary(self):
        return {
            "n_entries": len(self.entries),
            "n_folders": len(self.by_folder()),
            "n_readers": len(self.by_reader()),
            "mechanisms_seen": len(self.by_mechanism()),
            "mechanisms_total": len(MECHANISMS),
            "directions_seen": len(self.by_direction()),
            "directions_total": len(SHAPE_PAIRS),
        }

    def render(self):
        s = self.summary()
        lines = [
            f"entries:  {s['n_entries']}",
            f"folders:  {s['n_folders']}",
            f"readers:  {s['n_readers']}",
            f"mechanisms seen: {s['mechanisms_seen']}/{s['mechanisms_total']}",
            f"directions seen: {s['directions_seen']}/{s['directions_total']}",
            "",
        ]
        if not self.entries:
            lines.append("(no entries; nothing recorded yet)")
            return "\n".join(lines)

        lines.append("by folder:")
        for folder, n in sorted(self.by_folder().items()):
            readers = len(self.readers_in_folder(folder))
            lines.append(f"  {folder:30s} {n:5d}  readers={readers}")

        lines.append("")
        lines.append("by mechanism:")
        for m, n in sorted(self.by_mechanism().items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"  {m:14s} {n}")

        lines.append("")
        lines.append("by direction:")
        for d, n in sorted(self.by_direction().items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"  {d:28s} {n}")

        lines.append("")
        lines.append("no composite. no ranking. no verdict.")
        return "\n".join(lines)


# -- CLI ----------------------------------------------------------------

def _cli(argv):
    import sys
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "summary":
        if len(argv) != 3:
            print("usage: registry.py summary <registry.jsonl>")
            return 2
        r = Registry().load(argv[2])
        print(r.render())
        return 0
    if cmd == "append":
        # append entries from a potential.Vector.to_dict() JSON file
        if len(argv) != 5:
            print("usage: registry.py append <registry.jsonl> <folder> <vector.json>")
            return 2
        reg_path, folder, vec_path = argv[2], argv[3], argv[4]
        vec = json.loads(Path(vec_path).read_text())
        entries = RegEntry.from_vector(folder, vec)
        r = Registry()
        if Path(reg_path).exists():
            r.load(reg_path)
        r.extend(entries)
        r.save(reg_path)
        print(f"appended {len(entries)} entries from {vec_path} to {reg_path}")
        return 0
    print(f"unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    import sys
    sys.exit(_cli(sys.argv))
