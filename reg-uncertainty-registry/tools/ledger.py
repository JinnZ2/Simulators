#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
ledger.py -- the verification ledger: every checkable claim, its search
result if one was run, and its state.

    claims    verification/claims.txt (V rows), batch_e.txt (E, authority),
              batch_f.txt (F, actors and conflicts), batch_g.txt (G, the
              consolidated bundle's new inputs), batch_h.txt (H, absence
              searches). Format: id | rep | sec | cite | claim. A row id
              appears in exactly one claims file (batch_a..d are the V rows
              as dispatched to agents; claims.txt is their union and wins).
    results   verification/results_*.txt, read in name order, a later file
              overriding an earlier one for the same id. Format:
              id | reached | queries | exists | says | found | depth | note
    state     tools/check_citations.citation_state(reached, queries,
              exists, says), imported through reglib and never copied:
              derived, never declared.

A claim with no result row was not searched in this session. It is
recorded reached=N, queries=0, exists=?, says=UNSEEN, depth=none, so the
four-state rule returns UNREACHABLE with the reason stated; it is never
silently dropped and never read as NOT_FOUND (NOT_FOUND needs two empty
searches or a different object at the citation).

Library and CLI; the CLI prints the table and the counts. Refuses
--selftest (checks run in tools/validate.py --selftest). Stdlib only.
"""

import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reglib  # noqa: E402

VDIR = os.path.join(reglib.FOLDER, "verification")
CLAIM_FILES = [("claims.txt", "V"), ("batch_e.txt", "E"), ("batch_f.txt", "F"),
               ("batch_g.txt", "G"), ("batch_h.txt", "H")]
NOT_SEARCHED = ("not searched in this session: the container's DNS refuses "
                "publisher hosts (WebFetch fails) and the search agents hit "
                "their session limit; WebSearch from the main session was "
                "spent on load-bearing rows")


def _rows(path):
    out = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            out.append([p.strip() for p in line.split("|")])
    return out


def claims(vdir=VDIR):
    out = {}
    for fname, prefix in CLAIM_FILES:
        path = os.path.join(vdir, fname)
        for parts in _rows(path):
            rid = parts[0]
            if not rid.startswith(prefix):
                raise reglib.RegistryError("%s: row %s outside prefix %s"
                                           % (fname, rid, prefix))
            if rid in out:
                raise reglib.RegistryError("claim %s in two claims files" % rid)
            if len(parts) < 5:
                raise reglib.RegistryError("%s: row %s has %d fields"
                                           % (fname, rid, len(parts)))
            out[rid] = {"id": rid, "rep": parts[1], "sec": parts[2],
                        "cite": parts[3], "claim": " | ".join(parts[4:]),
                        "file": fname}
    return out


def results(vdir=VDIR):
    out = {}
    for path in sorted(glob.glob(os.path.join(vdir, "results_*.txt"))):
        for parts in _rows(path):
            if len(parts) < 8:
                raise reglib.RegistryError("%s: row %s has %d fields"
                                           % (os.path.basename(path), parts[0],
                                              len(parts)))
            rid = parts[0]
            out[rid] = {"reached": parts[1], "queries": int(parts[2]),
                        "exists": parts[3], "says": parts[4],
                        "found": parts[5], "depth": parts[6],
                        "note": " | ".join(parts[7:]),
                        "result_file": os.path.basename(path)}
    return out


def ledger(vdir=VDIR):
    cl = claims(vdir)
    rs = results(vdir)
    orphans = sorted(set(rs) - set(cl))
    if orphans:
        raise reglib.RegistryError("results with no claim row: %s"
                                   % ", ".join(orphans))
    out = {}
    for rid, c in cl.items():
        r = rs.get(rid)
        row = dict(c)
        if r is None:
            row.update({"reached": "N", "queries": 0, "exists": "?",
                        "says": "UNSEEN", "found": "", "depth": "none",
                        "note": NOT_SEARCHED, "result_file": None})
        else:
            row.update(r)
        row["state"] = reglib.citation_state(row["reached"], row["queries"],
                                             row["exists"], row["says"])
        row["corrected_value"] = (row["note"] if row["state"] == "CORRECTED"
                                  else None)
        out[rid] = row
    return out


def verification_of(row):
    """The registry's verification object for one ledger row."""
    return {"state": row["state"], "depth": row["depth"],
            "reached": row["reached"], "queries": row["queries"],
            "exists": row["exists"], "says": row["says"],
            "found": row["found"], "corrected_value": row["corrected_value"],
            "ledger_row": row["id"], "reason": row["note"]}


def counts(led):
    tab = {}
    for row in led.values():
        p = row["id"][0]
        tab.setdefault(p, {}).setdefault(row["state"], 0)
        tab[p][row["state"]] += 1
    return tab


def render(led):
    states = ("VERIFIED", "CORRECTED", "NOT_FOUND", "UNREACHABLE")
    out = ["ledger  %d claim rows, %d searched"
           % (len(led), sum(1 for r in led.values() if r["result_file"]))]
    tab = counts(led)
    out.append("prefix  " + "  ".join("%11s" % s for s in states) + "  total")
    for p in sorted(tab):
        out.append("%-6s  " % p + "  ".join("%11d" % tab[p].get(s, 0)
                                             for s in states)
                   + "  %5d" % sum(tab[p].values()))
    tot = {s: sum(tab[p].get(s, 0) for p in tab) for s in states}
    out.append("all     " + "  ".join("%11d" % tot[s] for s in states)
               + "  %5d" % len(led))
    out.append("")
    for rid in sorted(led):
        r = led[rid]
        if r["state"] in ("CORRECTED", "NOT_FOUND"):
            out.append("%-5s %-9s %s" % (rid, r["state"], r["note"][:110]))
    return out


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("ledger.py: checks run in reg-uncertainty-registry/tools/validate.py "
                         "--selftest\n")
        return 2
    print("\n".join(render(ledger())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
