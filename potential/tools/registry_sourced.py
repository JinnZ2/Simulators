"""registry_sourced.py — the registry with verified spans.

`registry.RegEntry` carries `source_span` and `target_span` as
(start, end) tuples supplied by the caller. Nothing checks that those
offsets point at the text the entry claims to be about, and nothing
checks that the source text exists at that offset in any document the
loader can see.

This module adds both checks. An entry may carry a `SliceRef`, which is
a span plus the literal text it is supposed to bound plus a document
identifier. Verification slices the document at the offsets and
requires the slice to equal the stored text.

Three states, kept apart:
    VERIFIED   the slice reproduces the stored text
    REFUSED    the slice does not reproduce it (the offsets are wrong)
    UNVERIFIED the document was not supplied (the offsets are untested)

`REFUSED` and `UNVERIFIED` are different findings. A refusal says the
locator is wrong; an absent document says the locator is untested.
Collapsing them would read a silence as a contradiction.

Note on the sourced primitive: if `tools/sourced.py` exposes a span
type with the same semantics, `SliceRef.verify` should import and
delegate to it. The adapter would be a single function; the discipline
- slice, compare, three states - is the same either way.
"""

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from registry import Registry, RegEntry, MECHANISMS, SHAPE_PAIRS

# --- the sourced primitive --------------------------------------------

@dataclass
class SliceRef:
    """A span plus the text it is supposed to bound, plus a doc id."""
    doc: str
    start: int
    end: int
    text: str

    def __post_init__(self):
        if self.start < 0 or self.end < self.start:
            raise ValueError(f"invalid span ({self.start}, {self.end})")
        if not self.doc or not self.doc.strip():
            raise ValueError("SliceRef requires a document identifier")
        if self.text is None:
            raise ValueError("SliceRef requires a text value (may be empty)")

    def to_dict(self):
        return {"doc": self.doc, "start": self.start, "end": self.end, "text": self.text}

    @classmethod
    def from_dict(cls, d):
        return cls(doc=d["doc"], start=d["start"], end=d["end"], text=d["text"])

    def verify(self, doc_bytes):
        """Slice doc_bytes at [start:end] and compare to self.text."""
        if self.end > len(doc_bytes):
            return "REFUSED"
        sliced = doc_bytes[self.start:self.end].decode("utf-8", errors="replace")
        return "VERIFIED" if sliced == self.text else "REFUSED"

    def boundary_clean(self, doc_bytes, word_chars=b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"):
        """True if start and end fall on a token boundary or on doc edge.
        One narrow form of a false locator: a fixed-width column falling
        inside a token. Consistent-with-text is not the same as aligned."""
        n = len(doc_bytes)
        if self.start > 0 and self.start < n and doc_bytes[self.start - 1] in word_chars and doc_bytes[self.start] in word_chars:
            return False
        if self.end > 0 and self.end < n and doc_bytes[self.end - 1] in word_chars and doc_bytes[self.end] in word_chars:
            return False
        return True


# --- the entry ---------------------------------------------------------

@dataclass
class SourcedRegEntry(RegEntry):
    source_slice: Optional[SliceRef] = None
    target_slice: Optional[SliceRef] = None

    def to_dict(self):
        d = super().to_dict()
        d["source_slice"] = self.source_slice.to_dict() if self.source_slice else None
        d["target_slice"] = self.target_slice.to_dict() if self.target_slice else None
        return d

    @classmethod
    def from_dict(cls, d):
        d = dict(d)
        src = d.pop("source_slice", None)
        tgt = d.pop("target_slice", None)
        base = RegEntry.from_dict({k: v for k, v in d.items() if k in RegEntry.__dataclass_fields__})
        return cls(
            folder=base.folder,
            mechanism=base.mechanism,
            source_type=base.source_type,
            target_type=base.target_type,
            source_span=base.source_span,
            target_span=base.target_span,
            reader=base.reader,
            date=base.date,
            source_slice=SliceRef.from_dict(src) if src else None,
            target_slice=SliceRef.from_dict(tgt) if tgt else None,
        )


# --- the registry ------------------------------------------------------

@dataclass
class VerifyReport:
    verified: int = 0
    refused: int = 0
    unverified: int = 0
    no_slice: int = 0
    refused_entries: list = None
    unverified_docs: set = None

    def __post_init__(self):
        if self.refused_entries is None:
            self.refused_entries = []
        if self.unverified_docs is None:
            self.unverified_docs = set()

    def render(self):
        lines = [
            f"verified:   {self.verified}",
            f"refused:    {self.refused}",
            f"unverified: {self.unverified}",
            f"no slice:   {self.no_slice}",
        ]
        if self.refused_entries:
            lines.append("")
            lines.append("refused slices:")
            for e in self.refused_entries:
                lines.append(f"  {e}")
        if self.unverified_docs:
            lines.append("")
            lines.append("documents not supplied (spans untested):")
            for d in sorted(self.unverified_docs):
                lines.append(f"  {d}")
        return "\n".join(lines)


class SourcedRegistry(Registry):
    """A Registry whose entries may carry verified SliceRefs."""

    def add(self, entry):
        if not isinstance(entry, (RegEntry, SourcedRegEntry)):
            raise TypeError(f"expected RegEntry or SourcedRegEntry, got {type(entry).__name__}")
        super().add(entry)

    def load(self, path):
        path = Path(path)
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                self.add(SourcedRegEntry.from_dict(json.loads(line)))
            except Exception as exc:
                raise ValueError(f"{path}:{lineno}: {exc}")
        return self

    def verify(self, docs):
        """docs maps doc id -> bytes. Missing doc -> UNVERIFIED, not pass."""
        r = VerifyReport()
        for e in self.entries:
            for label, sr in (("source", e.source_slice), ("target", e.target_slice)):
                if sr is None:
                    continue
                if sr.doc not in docs:
                    r.unverified += 1
                    r.unverified_docs.add(sr.doc)
                    continue
                state = sr.verify(docs[sr.doc])
                if state == "VERIFIED":
                    r.verified += 1
                else:
                    r.refused += 1
                    r.refused_entries.append(
                        f"{label} slice in folder={e.folder} reader={e.reader} "
                        f"doc={sr.doc}[{sr.start}:{sr.end}]"
                    )
            if e.source_slice is None and e.target_slice is None:
                r.no_slice += 1
        return r


# --- CLI / selftest ----------------------------------------------------

def _selftest():
    checks = 0
    def check(cond, msg):
        nonlocal checks
        checks += 1
        if not cond:
            raise AssertionError(msg)

    # SliceRef validates
    try:
        SliceRef(doc="d", start=5, end=3, text="x")
        check(False, "should reject end < start")
    except ValueError:
        check(True, "rejected end < start")

    try:
        SliceRef(doc="", start=0, end=0, text="")
        check(False, "should reject empty doc")
    except ValueError:
        check(True, "rejected empty doc")

    # verify against real bytes
    doc = b"the cat sat on the mat"
    s = SliceRef(doc="d", start=4, end=7, text="cat")
    check(s.verify(doc) == "VERIFIED", "correct slice not verified")

    wrong = SliceRef(doc="d", start=4, end=7, text="dog")
    check(wrong.verify(doc) == "REFUSED", "wrong text not refused")

    oob = SliceRef(doc="d", start=100, end=103, text="xyz")
    check(oob.verify(doc) == "REFUSED", "out-of-range slice should be refused, not crash")

    # boundary check
    inside = SliceRef(doc="d", start=5, end=6, text="a")  # 'a' inside "cat"
    check(inside.boundary_clean(doc) is False, "mid-token boundary not flagged")
    at_edge = SliceRef(doc="d", start=4, end=7, text="cat")
    check(at_edge.boundary_clean(doc) is True, "clean boundary flagged")

    # three states distinct
    e1 = SourcedRegEntry(
        folder="f", mechanism="DELETE", source_type="unresolved", target_type="familiar",
        source_slice=SliceRef(doc="alpha.txt", start=4, end=7, text="cat"),
    )
    e2 = SourcedRegEntry(
        folder="f", mechanism="DELETE", source_type="unresolved", target_type="familiar",
        source_slice=SliceRef(doc="beta.txt", start=0, end=3, text="WRONG"),
    )
    e3 = SourcedRegEntry(
        folder="f", mechanism="DELETE", source_type="unresolved", target_type="familiar",
        source_slice=SliceRef(doc="gamma.txt", start=0, end=3, text="xyz"),
    )

    reg = SourcedRegistry()
    reg.add(e1); reg.add(e2); reg.add(e3)

    report = reg.verify({
        "alpha.txt": b"the cat sat",
        "beta.txt":  b"the cat sat",  # slice says WRONG
        # gamma.txt missing
    })
    check(report.verified == 1, f"expected 1 verified, got {report.verified}")
    check(report.refused == 1, f"expected 1 refused, got {report.refused}")
    check(report.unverified == 1, f"expected 1 unverified, got {report.unverified}")
    check(report.verified != report.unverified, "verified and unverified must be distinct")
    check("gamma.txt" in report.unverified_docs, "unverified doc not named")
    check(any("beta.txt" in s for s in report.refused_entries), "refused entry not named")

    # round trip preserves slices
    d = e1.to_dict()
    e1b = SourcedRegEntry.from_dict(d)
    check(e1b.source_slice is not None, "slice lost on roundtrip")
    check(e1b.source_slice.text == "cat", "slice text lost")

    # an entry with no slice is 'no slice', not a refusal
    e4 = SourcedRegEntry(
        folder="f", mechanism="DELETE", source_type="unresolved", target_type="familiar",
    )
    reg2 = SourcedRegistry(); reg2.add(e4)
    r2 = reg2.verify({})
    check(r2.no_slice == 1, "unsliced entry counted wrong")
    check(r2.refused == 0, "unsliced entry miscounted as refusal")
    check(r2.unverified == 0, "unsliced entry miscounted as unverified")

    # the base registry's refusals are inherited
    for method in ("composite", "rank_folders", "verdict_on"):
        try:
            getattr(reg, method)("x")
            check(False, f"{method} should have raised on SourcedRegistry")
        except NotImplementedError:
            check(True, f"{method} refused on SourcedRegistry")

    print(f"checks: {checks}")
    print("PASS")
    return 0

def _main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    if argv[1] == "--selftest":
        return _selftest()
    if argv[1] == "verify":
        if len(argv) != 4:
            print("usage: registry_sourced.py verify <registry.jsonl> <docs_dir>")
            return 2
        reg = SourcedRegistry().load(argv[2])
        docs = {}
        for p in Path(argv[3]).iterdir():
            if p.is_file():
                docs[p.name] = p.read_bytes()
        print(reg.verify(docs).render())
        return 0
    print(f"unknown command: {argv[1]}")
    return 2

if __name__ == "__main__":
    sys.exit(_main(sys.argv))
