"""graph.py — nodes, channels, and admissibility-indexed graphs.

A domain graph has:
  - nodes: named states
  - channels: transitions, each with a set of KINDS and a token flag
  - source node and target node

Kinds is a subset of {physical, legal, practical}. An admissibility
predicate θ selects a subset; G_θ keeps only channels whose kinds
include every kind in θ.

A channel marked requires_token=True is split into two edges with a
TOKEN node in between: src -> TOKEN and TOKEN -> dst. Removing TOKEN
disconnects the channel and any path that used it.

No node is privileged. No channel is ranked. Tokens are marked, not
scored. The graph reports topology; what the topology means is the
reader's.
"""

from dataclasses import dataclass, field
from typing import FrozenSet, Optional

KINDS = ("physical", "legal", "practical")

TOKEN_NODE = "__TOKEN__"

@dataclass(frozen=True)
class Channel:
    src: str
    dst: str
    kinds: frozenset
    requires_token: bool = False
    label: str = ""

    def __post_init__(self):
        for k in self.kinds:
            if k not in KINDS:
                raise ValueError(f"unknown kind: {k!r}")
        if not self.src or not self.dst:
            raise ValueError("channel requires src and dst")

    def to_dict(self):
        return {
            "src": self.src, "dst": self.dst,
            "kinds": sorted(self.kinds),
            "requires_token": self.requires_token,
            "label": self.label,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            src=d["src"], dst=d["dst"],
            kinds=frozenset(d["kinds"]),
            requires_token=d.get("requires_token", False),
            label=d.get("label", ""),
        )


class Graph:
    def __init__(self, name, source, target):
        self.name = name
        self.source = source
        self.target = target
        self.nodes = set()
        self.channels = []

    def add_channel(self, ch):
        self.nodes.add(ch.src)
        self.nodes.add(ch.dst)
        if ch.requires_token:
            self.nodes.add(TOKEN_NODE)
        self.channels.append(ch)

    def edges(self):
        """Return {(u, v): set(labels)} for the graph WITHOUT splitting."""
        out = {}
        for ch in self.channels:
            if ch.requires_token:
                out.setdefault((ch.src, TOKEN_NODE), set()).add(ch.label)
                out.setdefault((TOKEN_NODE, ch.dst), set()).add(ch.label)
            else:
                out.setdefault((ch.src, ch.dst), set()).add(ch.label)
        return out

    def to_dict(self):
        return {
            "name": self.name,
            "source": self.source,
            "target": self.target,
            "channels": [c.to_dict() for c in self.channels],
        }

    @classmethod
    def from_dict(cls, d):
        g = cls(d["name"], d["source"], d["target"])
        for c in d["channels"]:
            g.add_channel(Channel.from_dict(c))
        return g


@dataclass(frozen=True)
class Admissibility:
    """A declared predicate. kinds is the required set."""
    name: str
    kinds: frozenset

    def __post_init__(self):
        for k in self.kinds:
            if k not in KINDS:
                raise ValueError(f"unknown kind in admissibility: {k!r}")

    @classmethod
    def of(cls, name, *kinds):
        return cls(name=name, kinds=frozenset(kinds))

    def to_dict(self):
        return {"name": self.name, "kinds": sorted(self.kinds)}

    @classmethod
    def from_dict(cls, d):
        return cls(name=d["name"], kinds=frozenset(d["kinds"]))


def project(graph, admissibility):
    """Return a new Graph keeping only channels whose kinds ⊇ θ.kinds."""
    g = Graph(
        name=f"{graph.name}[{admissibility.name}]",
        source=graph.source,
        target=graph.target,
    )
    for ch in graph.channels:
        if admissibility.kinds.issubset(ch.kinds):
            g.add_channel(ch)
    return g
