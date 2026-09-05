# SPDX-License-Identifier: CC0-1.0
"""
Rule 2 -- categorizations are parallel views, never canonical.

A view is a mapping from base entries to labels. Any number of views sit
side by side; none is privileged, none is required. Adding a view is
additive and never rewrites a base entry; retiring a view removes the
mapping and leaves the base intact. This is the part that breaks from the
human-facing convention -- a reader who can hold one categorization needs
the dataset to pick, a reader who can hold twelve does not, and picking
costs information that cannot be recovered later.

Stdlib only. Parses under Python 3.9. CC0.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


class ViewNotFound(Exception):
    pass


@dataclass
class View:
    view_id: str
    view_name: str            # e.g. NAICS_2017, ONET_taskclass, metabolic_class
    authoring_frame: str      # whose question this view answers
    effective_span: Tuple[str, str]   # (from, to); ("", "") = open
    mapping: Dict[str, str] = field(default_factory=dict)  # entry_id -> label

    def label(self, entry_id: str) -> Optional[str]:
        return self.mapping.get(entry_id)


class ViewRegistry:
    """Holds views side by side. No view is canonical; there is no
    `default_view`, and `labels_for` returns every view's label for an
    entry so no single frame is picked on the reader's behalf."""

    def __init__(self):
        self._views: Dict[str, View] = {}

    def add_view(self, view: View) -> None:
        """Additive. Adding a view touches no base entry -- it stores a
        mapping keyed by entry_id and nothing else."""
        self._views[view.view_id] = view

    def retire_view(self, view_id: str) -> None:
        """Removes the mapping; the base entries it referenced are
        untouched (this registry holds no base entries to touch)."""
        self._views.pop(view_id, None)

    def get(self, view_id: str) -> View:
        if view_id not in self._views:
            raise ViewNotFound(view_id)
        return self._views[view_id]

    def view_ids(self) -> List[str]:
        return sorted(self._views)

    def labels_for(self, entry_id: str) -> Dict[str, Optional[str]]:
        """Every view's label for one entry, side by side. None where a view
        does not map the entry -- an entry outside a view's frame, not an
        error."""
        return {vid: self._views[vid].label(entry_id)
                for vid in self.view_ids()}

    def group_by(self, view_id: str, entry_ids: List[str]
                 ) -> Dict[Optional[str], List[str]]:
        """Group entry_ids by their label under one view. Entries the view
        does not map fall under the None group (out of this view's frame),
        kept rather than dropped."""
        view = self.get(view_id)
        out: Dict[Optional[str], List[str]] = {}
        for eid in entry_ids:
            out.setdefault(view.label(eid), []).append(eid)
        return out


if __name__ == "__main__":
    import sys as _s
    _s.stderr.write("views.py is a library; its checks live in "
                    "machine-record-format/selftest_mrf.py.\n")
    _s.exit(2)
