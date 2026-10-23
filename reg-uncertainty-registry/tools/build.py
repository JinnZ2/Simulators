#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
build.py -- the only writer of registry/.

    pinned source    bundle/source/current/*.csv (graded from), and
                     bundle/source/superseded/v1/*.csv (configuration history:
                     the v1 direction column is the verb coding, the v1 annex
                     carries the per-axis C_permit scores the v2 annex dropped)
    curation         tools/curation_core.py, curation_cases.py, curation_ncr.py
    ledger           tools/ledger.py over verification/
    grading          tools/grade.py
    numbers          tools/stats.py (statement values are computed, never typed)

Every CHANGE in curation_ncr.CHANGES is applied in order. A recode or retype
first asserts that the pinned source carries the CHANGE's `from` value; a
CHANGE whose `from` does not match fails the build, so the change log cannot
drift from the data. Output is deterministic (sorted keys, sorted lists) and
registry/MANIFEST.json pins every file written; validate.py rebuilds into a
scratch directory and compares bytes.

Usage
    python3 tools/build.py            write registry/
    python3 tools/build.py --check    build in memory, compare with registry/
Refuses --selftest (checks run in tools/validate.py --selftest). Stdlib only.
"""

import csv
import datetime
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reglib  # noqa: E402
import grade  # noqa: E402
import ledger as ledgermod  # noqa: E402
import curation_core as CORE  # noqa: E402
import curation_cases as CASES  # noqa: E402
import curation_ncr as NCRC  # noqa: E402

REGISTRY = "ACT-REGISTRY"
KIMI = "ACT-KIMI"
CUR = reglib.SRCDIR
OLD = reglib.OLDDIR


class BuildError(reglib.RegistryError):
    pass


# ---------------------------------------------------------------- helpers

def read_csv(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def claim(value, status, coder, source=None, basis=None, rationale=None,
          inference=None, contested=None, independence=None):
    c = {"value": value, "status": status, "coder": coder}
    if source:
        c["source"] = source
    if basis:
        c["basis"] = sorted(set(basis))
    if rationale:
        c["rationale"] = rationale
    if inference is not None:
        c["inference"] = inference
    if contested is not None:
        c["contested"] = contested
    if independence:
        c["independence"] = independence
    return c


def collapse(direction):
    if direction in ("go_ahead", "warn"):
        return "permissive"
    if direction in ("hold", "decline"):
        return "restrictive"
    return "not_determinable"


def group_of(bearer):
    return "diffuse" if bearer == "public" else "concentrated"


def short(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]


def host_kind(url):
    if not url or url == "none":
        return "none_given"
    for host, kind in NCRC.HOST_KIND:
        if host in url:
            return kind
    return "secondary"


def years_between(a, b):
    def parse(s):
        parts = [int(x) for x in s.split("-")]
        while len(parts) < 3:
            parts.append(1 if len(parts) == 2 else 7)
        return datetime.date(parts[0], parts[1] if len(parts) > 1 else 7,
                             parts[2])
    # year-only dates are read as mid-year (July 1); year-month as the 1st
    def p(s):
        bits = s.split("-")
        if len(bits) == 1:
            return datetime.date(int(bits[0]), 7, 1)
        if len(bits) == 2:
            return datetime.date(int(bits[0]), int(bits[1]), 1)
        return datetime.date(int(bits[0]), int(bits[1]), int(bits[2]))
    return round((p(b) - p(a)).days / 365.25, 2)


def file_verification(path):
    return {"state": reglib.citation_state("Y", 0, "Y", "MATCH"),
            "depth": "file", "reached": "Y", "queries": 0, "exists": "Y",
            "says": "MATCH", "found": "pinned file, read in full",
            "corrected_value": None, "ledger_row": None,
            "reason": "bundle file pinned by sha256 (bundle/MANIFEST.sha256)"}


def gap_verification(reason):
    return {"state": reglib.citation_state("N", 0, "?", "UNSEEN"),
            "depth": "none", "reached": "N", "queries": 0, "exists": "?",
            "says": "UNSEEN", "found": "", "corrected_value": None,
            "ledger_row": None, "reason": reason}


# ---------------------------------------------------------------- build

class Builder(object):
    def __init__(self):
        self.led = ledgermod.ledger()
        self.objects = {}
        self.edges = []
        self.changes_applied = {}

    # -------------------------------------------------- object store
    def add(self, obj):
        oid = obj["id"]
        if oid in self.objects:
            raise BuildError("duplicate id %s" % oid)
        self.objects[oid] = obj
        return obj

    def edge(self, a, b, etype, status, basis=None, kind=None, order=None,
             note=None):
        e = {"from": a, "to": b, "type": etype, "status": status}
        if basis:
            e["basis"] = sorted(set(basis))
        if kind:
            e["kind"] = kind
        if order is not None:
            e["order"] = order
        if note:
            e["note"] = note
        self.edges.append(e)

    def row(self, rid):
        if rid not in self.led:
            raise BuildError("ledger row %s cited but not in the ledger" % rid)
        return self.led[rid]

    def ev_id(self, rid):
        self.row(rid)
        return "EV-" + rid

    # -------------------------------------------------- sources + evidence
    def sources_and_evidence(self):
        pins = {r: w for r, w in reglib.bundle_manifest_entries()}
        for sid, label, path, superseded in NCRC.BUNDLE_SOURCES:
            full = os.path.join(reglib.FOLDER, path)
            sha = reglib.sha256_file(full)
            rel_b = os.path.relpath(full, reglib.BUNDLE)
            if not rel_b.startswith("..") and pins.get(rel_b) not in (None, sha):
                raise BuildError("%s does not match bundle manifest" % path)
            self.add({"id": sid, "type": "SOURCE", "cite": label, "url": None,
                      "path": path, "sha256": sha, "kind": "bundle_file",
                      "superseded": superseded, "rows": [],
                      "verification": file_verification(path)})
        # one SOURCE per cited URL; verification aggregated over its rows
        by_url = {}
        for rid, r in sorted(self.led.items()):
            if r["cite"] and r["cite"] != "none":
                by_url.setdefault(r["cite"], []).append(r)
        for url, rows in sorted(by_url.items()):
            states = [r["state"] for r in rows]
            if all(s == "VERIFIED" for s in states):
                st = "VERIFIED"
            elif "CORRECTED" in states:
                st = "CORRECTED"
            elif "NOT_FOUND" in states:
                st = "NOT_FOUND"
            else:
                st = "UNREACHABLE"
            sid = "SRC-U-" + short(url)
            best = rows[0]
            ver = ledgermod.verification_of(best)
            ver["state"] = st
            ver["reason"] = ("aggregate over %d ledger rows (%s): VERIFIED "
                             "only if every row is; else CORRECTED if any; "
                             "else NOT_FOUND if any; else UNREACHABLE"
                             % (len(rows), ", ".join(r["id"] for r in rows)))
            ver["ledger_row"] = None
            self.add({"id": sid, "type": "SOURCE", "cite": url, "url": url,
                      "path": None, "sha256": None, "kind": host_kind(url),
                      "superseded": False, "rows": [r["id"] for r in rows],
                      "verification": ver})
        self.url_source = {url: "SRC-U-" + short(url) for url in by_url}
        # one EVIDENCE per ledger row
        auth_kind = {}
        for aid, level, cit, title, lrow in CORE.AUTHORITIES:
            if lrow:
                auth_kind[lrow] = {"statute": "statute", "regulation": "regulation",
                                   "guidance": "regulation", "order": "regulation",
                                   "court_decision": "court_order",
                                   "international_instrument": "regulation"}[level]
        for rid, r in sorted(self.led.items()):
            kind = "record_fact"
            if rid in auth_kind:
                kind = auth_kind[rid]
            elif rid[0] == "H":
                kind = "absence"
            elif rid in ("V001", "V002", "V003", "V004", "V005", "V006", "V007", "V008"):
                kind = "population_statistic"
            elif r["rep"] == "Q":
                kind = "regulation"
            obj = {"id": "EV-" + rid, "type": "EVIDENCE", "kind": kind,
                   "statement": r["claim"],
                   "sources": ([self.url_source[r["cite"]]]
                               if r["cite"] in self.url_source else []),
                   "status": "PROPOSED" if rid[0] == "H" else "OBSERVED",
                   "verification": ledgermod.verification_of(r),
                   "rep": r["rep"], "section": r["sec"]}
            if rid in ("V080", "V081", "V082", "V083", "V084", "V085", "V086", "V087"):
                obj["rotation_pattern"] = "not_coded"
                obj["note"] = ("E01 evidence: the source codes exposure "
                               "ever/never or by duration, not by rotation "
                               "pattern (EA-05)")
            self.add(obj)
            for s in obj["sources"]:
                self.edge(obj["id"], s, "cites", "OBSERVED")
        # unlocated legacy inputs: gaps are nodes
        for uid, case, eclass, text, reason in CASES.UNLOCATED:
            self.add({"id": uid, "type": "EVIDENCE",
                      "kind": "absence" if eclass == "absence" else "unlocated_input",
                      "statement": text, "sources": [], "status": "PROPOSED",
                      "verification": gap_verification(reason),
                      "unlocated_reason": reason,
                      "evidence_class": ([eclass] if eclass != "absence" else [])})
            self.edge(uid, case, "supports", "PROPOSED",
                      note="input relied on, not located")
        # frames named and not loaded
        for fid, label, reason, rows in CASES.FRAMES_NOT_LOADED:
            self.add({"id": "EV-" + fid, "type": "EVIDENCE", "kind": "gap",
                      "statement": label, "sources": [], "status": "PROPOSED",
                      "verification": gap_verification(reason),
                      "note": "rows: " + (", ".join(rows) if rows else "none")})

    # -------------------------------------------------- statements
    def statements(self, values):
        for stid, src, needle, ncr, template in NCRC.STATEMENTS:
            path = os.path.join(reglib.FOLDER, self.objects[src]["path"])
            text = open(path, "r", encoding="utf-8").read()
            n = text.count(needle)
            if n != 1:
                raise BuildError("%s: needle occurs %d times in %s"
                                 % (stid, n, self.objects[src]["path"]))
            line = text[:text.index(needle)].count("\n") + 1
            value = template.format(**values)
            ver = {"state": reglib.citation_state("Y", 0, "Y", "DIFFERS"),
                   "depth": "file", "reached": "Y", "queries": 0, "exists": "Y",
                   "says": "DIFFERS", "found": needle,
                   "corrected_value": value, "ledger_row": None,
                   "reason": "corrected by %s; value computed by tools/stats.py"
                             % ncr}
            self.add({"id": stid, "type": "EVIDENCE", "kind": "statement",
                      "statement": needle, "sources": [src], "status": "OBSERVED",
                      "verification": ver, "registry_value": value,
                      "located": {"path": self.objects[src]["path"],
                                  "line": line}})
            self.edge(stid, src, "cites", "OBSERVED")

    # -------------------------------------------------- actors, authority
    def actors_authority(self):
        for aid, atype, name, role, dr, rows in CORE.ACTORS:
            for r in rows:
                self.row(r)
            self.add({"id": aid, "type": "ACTOR", "actor_type": atype,
                      "name": name, "role_at_time": role, "date_range": dr,
                      "basis": sorted(self.ev_id(r) for r in rows),
                      "status": "OBSERVED" if rows else "PROPOSED"})
        for aid, level, cit, title, lrow in CORE.AUTHORITIES:
            ver = (ledgermod.verification_of(self.row(lrow)) if lrow else
                   gap_verification("no ledger row: authority named by the "
                                    "registry, citation not searched"))
            obj = {"id": aid, "type": "AUTHORITY", "level": level,
                   "citation": cit, "title": title, "verification": ver}
            self.add(obj)
            if lrow:
                self.edge(self.ev_id(lrow), aid, "supports", "OBSERVED")
        for actor, auth, rows in CORE.FUNDING:
            self.edge(actor, auth, "funded_by", "OBSERVED" if rows else "PROPOSED",
                      basis=[self.ev_id(r) for r in rows])
        for child, parent in CORE.DELEGATION:
            self.edge(child, parent, "delegated_from", "PROPOSED")

    # -------------------------------------------------- cases
    def cases(self):
        cd = {r["id"]: r for r in read_csv(os.path.join(CUR, "coded_decisions_v3.csv"))}
        an = {r["id"]: r for r in read_csv(os.path.join(CUR, "annex_a_regrading_v2.csv"))}
        v1 = {r["id"]: r for r in read_csv(os.path.join(OLD, "v1", "coded_decisions.csv"))}
        v1a = {r["id"]: r for r in read_csv(os.path.join(OLD, "v1", "annex_a_regrading.csv"))}
        if set(cd) != set(an) or set(cd) != set(CASES.CASES) or set(cd) != set(CASES.EXTRA):
            raise BuildError("coded sample, annex and curation disagree on ids")
        self.source_rows = cd
        self.annex_rows = an
        for cid in sorted(cd):
            self.add(self.coded_case(cid, cd[cid], an[cid], v1.get(cid), v1a.get(cid)))
        for cid in sorted(CASES.NEW_CASES):
            nc = CASES.NEW_CASES[cid]
            if nc["frame"] == "C2":
                continue
            self.add(self.new_case(cid, nc))
        self.frame_c2()
        self.comparators()

    def common_links(self, cid, cur):
        for r in cur.get("rows", []):
            self.edge(self.ev_id(r), cid, "supports", "OBSERVED")
        for a in cur.get("decided", []):
            self.edge(cid, a, "decided_by", "PROPOSED")
        for a in cur.get("recommended", []):
            self.edge(cid, a, "recommended_by", "PROPOSED")
        for a in cur.get("overruled", []):
            self.edge(cid, a, "overruled", "PROPOSED")
        if cur.get("sponsor"):
            self.edge(cid, cur["sponsor"], "sponsored_by", "PROPOSED")
        fk = cur.get("forcing")
        if fk and fk[0] != "none":
            for r in fk[2]:
                self.edge(cid, self.ev_id(r), "forced_by", "PROPOSED", kind=fk[0])

    def chain(self, key, cid):
        ch = CORE.CHAINS.get(key, [])
        for i, aid in enumerate(ch):
            if aid not in self.objects:
                raise BuildError("%s: authority %s not defined" % (cid, aid))
            self.edge(cid, aid, "authorized_by", "PROPOSED", order=i)
        return list(ch)

    def coded_case(self, cid, s, a, v1, v1a):
        cur = CASES.CASES[cid]
        ex = CASES.EXTRA[cid]
        src = "SRC-K3-CSV"
        cl = {}
        def K(name, value, rationale=None):
            cl[name] = claim(value, "PROPOSED", KIMI, source=src, rationale=rationale,
                             independence="ORIGINATOR")
        K("direction", s["direction"], "relative to the bearer of the cost of caution (v2 Fix 4)")
        K("action_direction", s["action_direction"])
        K("outcome_direction", s["outcome_direction"])
        if v1 is not None:
            cl["direction_verb"] = claim(v1["direction"], "PROPOSED", KIMI,
                                         source="SRC-K1-CSV",
                                         rationale="v1 coded the agency's verb; superseded file, read as configuration history",
                                         independence="ORIGINATOR")
        else:
            cl["direction_verb"] = claim("no_action", "PROPOSED", REGISTRY,
                                         rationale="not in v1; a non-decision has no verb")
        cl["direction_rel_bearer"] = claim(collapse(s["direction"]), "DERIVED", REGISTRY,
                                           rationale="permissive = go_ahead|warn; invariant under Rule L and Rule S because the cost-bearer is defined as the bearer of the cost of caution")
        for f in ("cost_bearer", "cost_bearer_L", "cost_bearer_S", "cost_group",
                  "uncertainty", "mirror"):
            K(f, s[f])
        cl["cost_group_L"] = claim(group_of(s["cost_bearer_L"]), "DERIVED", REGISTRY)
        cl["cost_group_S"] = claim(group_of(s["cost_bearer_S"]), "DERIVED", REGISTRY)
        K("evidence_class", s["evidence_class"].split("+"))
        K("source_verified_flag", s["verified"], "S = sourced, K = K-flagged by the originator")
        K("statute_compelled", s["statute_compelled"])
        U, rule = grade.u_grade(s["uncertainty"], s["evidence_class"].split("+"))
        cl["U_grade"] = claim(U, "DERIVED", REGISTRY, rationale=rule)
        annex_r3 = a["status"].startswith("STATUTE")
        cl["forced_action"] = claim(annex_r3, "DERIVED", KIMI, source="SRC-K2-ANNEX",
                                    rationale="RUS-0.2 R3 on the agency's action, as the annex applies it (status STATUTE/JUDICIAL-EXCEPTION)")
        cl["forced_outcome"] = claim(annex_r3, "DERIVED", KIMI, source="SRC-K2-ANNEX",
                                     rationale="RUS-0.2 R3 on the legal outcome, as the annex applies it")
        fk = cur.get("forcing")
        cl["forcing_kind"] = claim(fk[0] if fk else "none", "PROPOSED", REGISTRY,
                                   basis=[self.ev_id(r) for r in (fk[2] if fk else [])])
        cl["r1"] = claim(cur["r1"][0], "PROPOSED", REGISTRY, rationale=cur["r1"][1])
        cl["r1_scope"] = claim(ex["r1_scope"], "PROPOSED", REGISTRY,
                               rationale="[CHOICE] RUS-0.3 R1 scope (NCR-N06)")
        cl["r5"] = claim(bool(cur.get("r5")), "PROPOSED", REGISTRY)
        r6 = ex.get("r6", (False, None, None))
        cl["r6_blocking"] = claim(r6[0], "PROPOSED", REGISTRY)
        cl["r6_cycles"] = claim(r6[1], "PROPOSED", REGISTRY)
        cl["r6_justification"] = claim(r6[2], "PROPOSED", REGISTRY)
        cl["r6b_loosening"] = claim(bool(ex.get("r6b")), "PROPOSED", REGISTRY)
        # consequence
        cp_axes = None
        if v1a is not None:
            pid = [int(v1a["P"]), int(v1a["I"]), int(v1a["D"])]
            if sum(pid) == int(a["Cp_score"]):
                cp_axes = pid
        cp = {"P": cp_axes[0] if cp_axes else None, "I": cp_axes[1] if cp_axes else None,
              "D": cp_axes[2] if cp_axes else None, "score": int(a["Cp_score"]),
              "grade": a["Cp"], "rationale": v1a["rationale"] if v1a else "not delivered",
              "status": "PROPOSED", "coder": KIMI,
              "axes_source": ("SRC-K1-ANNEX (RUS-0.1 consequence; sum equals the v2 C_permit score)"
                              if cp_axes else "not delivered (NCR-N01)")}
        if grade.band(cp["score"]) != cp["grade"]:
            raise BuildError("%s: C_permit %s bands %s, annex says %s"
                             % (cid, cp["score"], grade.band(cp["score"]), cp["grade"]))
        cr_src = {"P": None, "I": None, "D": None, "score": int(a["Cr_score"]),
                  "grade": a["Cr"], "rationale": a["Cr_rationale"], "status": "PROPOSED",
                  "coder": KIMI, "axes_source": "not delivered (NCR-N01)"}
        if grade.band(cr_src["score"]) != cr_src["grade"]:
            raise BuildError("%s: C_restrict band mismatch" % cid)
        pr, ir, dr, rat = cur["Cr"]
        cr_reg = {"P": pr, "I": ir, "D": dr, "score": pr + ir + dr,
                  "grade": grade.band(pr + ir + dr), "rationale": rat,
                  "status": "PROPOSED", "coder": REGISTRY,
                  "axes_source": "registry second coding (NCR-N01, CHG-N01-01)"}
        alt = ex["alt"]
        sub = {"claimed": alt[0], "named": alt[1], "grade": alt[2], "status": "PROPOSED"}
        if ex.get("substitution_note"):
            sub["note"] = ex["substitution_note"]
        cons = {"C_permit": cp, "C_restrict": {"source": cr_src, "registry": cr_reg,
                                                "substitution": sub}}
        annex = {"U": a["U"], "Cp_score": int(a["Cp_score"]), "Cr_score": int(a["Cr_score"]),
                 "gap": int(a["gap"]), "Cp": a["Cp"], "Cr": a["Cr"], "floor": a["floor"],
                 "actual": a["actual"], "deviation": int(a["deviation"]),
                 "status": a["status"]}
        tier = {"C4": "T1", "C3": "T2"}.get(cp["grade"], "T3")
        obj = {"id": cid, "type": "DECISION", "title": s["decision"], "year": int(s["year"]),
               "agency": s["agency"], "frame": ex["frame"], "in_sample": True,
               "source_row": cid, "curation_key": cid, "claims": cl,
               "consequence": cons, "annex": annex, "grades": {},
               "authority_chain": self.chain(cid, cid), "rigor_tier": tier,
               "version": 1, "note": s["note"]}
        if cur.get("stages"):
            obj["stages"] = [{"stage": st, "direction": d, "text": t,
                              "forcing": {"kind": f[0], "pushes": f[1]}}
                             for st, d, t, f in cur["stages"]]
        if cid == "E01":
            obj["exposure"] = {"axis": "rotation_pattern",
                               "values_in_sources": ["not_coded"],
                               "note": "no located source codes night work by rotation pattern (EA-05)"}
        self.common_links(cid, cur)
        for o in cur.get("outcomes", []):
            pass  # linked in outcomes()
        return obj

    def new_case(self, cid, nc):
        cl = {}
        R = lambda v, why=None: claim(v, "PROPOSED", REGISTRY, rationale=why)
        cl["direction"] = R(nc["action"])
        cl["action_direction"] = R(nc["action"])
        cl["outcome_direction"] = R(nc["outcome"])
        cl["direction_verb"] = R(nc["action"])
        cl["direction_rel_bearer"] = claim(collapse(nc["action"]), "DERIVED", REGISTRY)
        obj = {"id": cid, "type": nc["type"], "title": nc["decision"], "year": nc["year"],
               "agency": nc["agency"], "frame": nc["frame"], "in_sample": False,
               "source_row": None, "curation_key": cid, "claims": cl,
               "authority_chain": self.chain(cid, cid), "version": 1,
               "note": nc["note"]}
        if nc["frame"] == "R8":
            for f in ("cost_bearer_L", "cost_bearer_S", "uncertainty"):
                cl[f] = R(nc[f])
            cl["cost_bearer"] = R(nc["cost_bearer_S"])
            cl["cost_group"] = claim(group_of(nc["cost_bearer_S"]), "DERIVED", REGISTRY)
            cl["cost_group_L"] = claim(group_of(nc["cost_bearer_L"]), "DERIVED", REGISTRY)
            cl["cost_group_S"] = claim(group_of(nc["cost_bearer_S"]), "DERIVED", REGISTRY)
            ec = nc["evidence_class"].split("+")
            cl["evidence_class"] = R(ec)
            U, rule = grade.u_grade(nc["uncertainty"], ec)
            cl["U_grade"] = claim(U, "DERIVED", REGISTRY, rationale=rule)
            cl["forced_action"] = R(nc["forced"][0])
            cl["forced_outcome"] = R(nc["forced"][1])
            cl["forcing_kind"] = R("none")
            cl["statute_compelled"] = R("0")
            cl["r1"] = R("none")
            cl["r1_scope"] = R(nc["r1_scope"])
            cl["r5"] = R(False)
            cl["r6_blocking"] = R(nc["r6"][0])
            cl["r6_cycles"] = R(nc["r6"][1], "annual cycles held at the decision date")
            cl["r6_justification"] = R(nc["r6"][2])
            cl["r6b_loosening"] = R(False)
            p, i, d, rp = nc["Cp"]
            q, j, e, rr = nc["Cr_axes"]
            side = lambda P, I, D, why: {"P": P, "I": I, "D": D, "score": P + I + D,
                                         "grade": grade.band(P + I + D), "rationale": why,
                                         "status": "PROPOSED", "coder": REGISTRY,
                                         "axes_source": "registry coding (NCR-R8)"}
            alt = nc["alt"]
            obj["consequence"] = {"C_permit": side(p, i, d, rp),
                                  "C_restrict": {"source": side(q, j, e, rr), "registry": None,
                                                 "substitution": {"claimed": alt[0], "named": alt[1],
                                                                  "grade": alt[2], "status": "PROPOSED"}}}
            obj["grades"] = {}
            obj["rigor_tier"] = {"C4": "T1", "C3": "T2"}.get(grade.band(p + i + d), "T3")
            obj["single_failure"] = ["every field: one coder (ACT-REGISTRY); row selected on direction (NCR-R8)"]
        self.common_links(cid, nc)
        return obj

    def frame_c2(self):
        rows = read_csv(os.path.join(CUR, "epa_frame_2022.csv"))
        if len(rows) != 40:
            raise BuildError("epa_frame_2022.csv has %d rows, want 40" % len(rows))
        self.c2_key = {}
        for i, r in enumerate(rows, 1):
            cid = "C2-%02d" % i
            key = "C2:" + r["chemical"]
            if key in self.c2_key:
                raise BuildError("two frame rows for %s" % key)
            self.c2_key[key] = cid
            cl = {"direction": claim(r["direction"], "PROPOSED", KIMI, source="SRC-K2-FRAME",
                                     independence="ORIGINATOR"),
                  "decision_type": claim(r["decision_type"], "OBSERVED", KIMI, source="SRC-K2-FRAME"),
                  "cost_bearer": claim(r["cost_bearer"], "PROPOSED", KIMI, source="SRC-K2-FRAME"),
                  "notice": claim(r["notice"], "OBSERVED", KIMI, source="SRC-K2-FRAME")}
            cl["direction_rel_bearer"] = claim(collapse(r["direction"]), "DERIVED", REGISTRY)
            obj = {"id": cid, "type": "DECISION",
                   "title": "%s: %s" % (r["chemical"], r["decision_type"]),
                   "year": int(r["date"][:4]), "agency": "EPA-OPP", "frame": "C2",
                   "in_sample": False, "source_row": "epa_frame_2022.csv:%d" % (i + 1),
                   "curation_key": key, "claims": cl, "authority_chain": [],
                   "version": 1, "note": r["note"]}
            if r["chemical"] == "Pentachlorophenol":
                nc = CASES.NEW_CASES["PCP22"]
                obj["curation_key"] = "PCP22"
                obj["authority_chain"] = self.chain("PCP22", cid)
                obj["note"] = r["note"] + " || registry: " + nc["note"]
                cl["forcing_kind"] = claim("none", "PROPOSED", REGISTRY,
                                           rationale="no statute or court forcing located (NCR-R6)",
                                           basis=[self.ev_id("G001")])
                self.common_links(cid, nc)
            self.add(obj)

    def comparators(self):
        for mid, title, year, agency, us_case, pair, us_s, comp_s, rows in CASES.COMPARATORS:
            cl = {"pair": claim(pair, "PROPOSED", KIMI if us_s is not None else REGISTRY,
                                source="SRC-K1-REPORT" if us_s is not None else None)}
            if us_s is not None:
                cl["us_score"] = claim(us_s, "PROPOSED", KIMI, source="SRC-K1-REPORT",
                                       rationale="permissiveness 0 (ban) to 3 (go ahead), v1 section 6 table")
                cl["comparator_score"] = claim(comp_s, "PROPOSED", KIMI, source="SRC-K1-REPORT")
                cl["divergence"] = claim(abs(us_s - comp_s), "DERIVED", REGISTRY)
            self.add({"id": mid, "type": "DECISION", "title": title, "year": year,
                      "agency": agency, "frame": "M", "in_sample": False,
                      "source_row": None, "curation_key": mid, "claims": cl,
                      "authority_chain": [], "version": 1,
                      "note": "in the source's mirror table" if us_s is not None
                              else "added by the registry; not in the source's mirror table"})
            self.edge(us_case, mid, "mirrors", "PROPOSED", basis=[self.ev_id(r) for r in rows])
            for r in rows:
                self.edge(self.ev_id(r), mid, "supports", "OBSERVED")

    # -------------------------------------------------- outcomes, reversals
    def outcomes(self):
        for oid, text, date, kind, direction, rows, case in CASES.OUTCOMES:
            self.add({"id": oid, "type": "OUTCOME", "statement": text, "date": date,
                      "kind": kind, "direction": direction,
                      "basis": sorted(self.ev_id(r) for r in rows), "status": "OBSERVED",
                      "case": case})
            self.edge(oid, case, "supersedes" if kind in ("court", "legislature") else "closes",
                      "PROPOSED")

    def reversals(self):
        for (rid, frm, to, fd, td, init, itype, mech, d0, d1, drows, harm, hrows,
             note) in CASES.REVERSALS:
            to_case = to if to in self.objects else None
            if frm not in self.objects:
                raise BuildError("%s: from_case %s unknown" % (rid, frm))
            for r in drows + hrows:
                self.row(r)
            obj = {"id": rid, "type": "REVERSAL", "from_case": frm, "to": to,
                   "to_case": to_case, "from_direction": fd, "to_direction": td,
                   "initiator": init, "initiator_type": itype, "mechanism": mech,
                   "date_from": d0, "date_to": d1,
                   "date_basis": sorted(self.ev_id(r) for r in drows),
                   "time_to_reversal_years": years_between(d0, d1),
                   "harm_at_reversal": {"state": "FOUND" if harm else "NOT_FOUND",
                                        "value": harm,
                                        "basis": sorted(self.ev_id(r) for r in hrows)},
                   "alias_of": CASES.REVERSAL_ALIASES.get(rid),
                   "status": "PROPOSED", "coder": REGISTRY, "note": note}
            self.add(obj)
            self.edge(rid, frm, "reverses", "PROPOSED")
            if to_case:
                self.edge(rid, to_case, "reverses", "PROPOSED", kind="to")
            if init not in self.objects:
                raise BuildError("%s: initiator %s unknown" % (rid, init))
            for r in drows:
                self.edge(self.ev_id(r), rid, "supports", "OBSERVED")

    # -------------------------------------------------- conflicts
    def conflicts(self):
        have = set()
        for fid, actor, ctype, dec, rows, text, recusal in CASES.CONFLICTS:
            st = "FOUND" if any(self.row(r)["state"] in ("VERIFIED", "CORRECTED")
                                for r in rows) else "UNREACHABLE"
            self.add({"id": fid, "type": "CONFLICT", "actor_id": actor,
                      "conflict_type": ctype, "decision": dec, "record_state": st,
                      "statement": text, "recusal": recusal,
                      "basis": sorted(self.ev_id(r) for r in rows), "status": "PROPOSED"})
            self.edge(fid, actor, "conflict_of", "PROPOSED")
            self.edge(fid, dec, "concerns", "PROPOSED")
            if ctype == "disclosure_record":
                have.add(dec)
        # every decision-maker of every graded case without a located
        # disclosure record: NOT_FOUND is never 'no conflict'
        for cid in sorted(o["id"] for o in self.objects.values()
                          if o["type"] in ("DECISION", "NON_DECISION")
                          and o["frame"] in ("A", "B", "C", "D", "E", "R8")):
            if cid in have:
                continue
            fid = "CF-%s-DISCLOSURE" % cid
            self.add({"id": fid, "type": "CONFLICT", "actor_id": "ACT-UNKNOWN",
                      "conflict_type": "disclosure_record", "decision": cid,
                      "record_state": "UNREACHABLE",
                      "statement": "no disclosure record located for the decision-makers or advisers of %s; not searched (egress); this is NOT 'no conflict'" % cid,
                      "recusal": None, "basis": [], "status": "PROPOSED"})
            self.edge(fid, cid, "concerns", "PROPOSED")

    # -------------------------------------------------- substances, endpoints, absences
    def vocab_objects(self):
        subs, ends = set(), set()
        for d in list(CASES.CASES.values()) + list(CASES.NEW_CASES.values()):
            subs.update(d.get("sub", []))
            ends.update(d.get("end", []))
        for a in CASES.ABSENCES:
            subs.add(a[1])
            ends.add(a[2])
        gap = ("external id lookup not run: EPA CompTox (DTXSID) and the "
               "endpoint ontologies are not reachable from this container "
               "(DNS refuses the hosts); local id minted (verification/ids_input.txt "
               "lists the lookups owed)")
        for s in sorted(subs):
            self.add({"id": "SUB-" + s, "type": "SUBSTANCE", "name": s.replace("_", " "),
                      "ids": {}, "id_state": "LOCAL_ONLY", "gap": gap, "basis": []})
        for e in sorted(ends):
            self.add({"id": "END-" + e, "type": "ENDPOINT", "label": e.replace("_", " "),
                      "ids": {}, "id_state": "LOCAL_ONLY", "gap": gap, "basis": []})
        for aid, sub, end, state, decs, corpus, terms, rows, note in CASES.ABSENCES:
            for r in rows:
                self.row(r)
            ver = (ledgermod.verification_of(self.row(rows[0])) if rows
                   else gap_verification("no search row"))
            self.add({"id": aid, "type": "ENDPOINT_ABSENCE", "substance": "SUB-" + sub,
                      "endpoint": "END-" + end, "state": state, "status": "PROPOSED",
                      "corpus": corpus, "terms": terms,
                      "basis": sorted(self.ev_id(r) for r in rows), "decisions": decs,
                      "verification": ver, "note": note})
            for r in rows:
                self.edge(self.ev_id(r), aid, "supports", "OBSERVED")

    # -------------------------------------------------- grades
    def grade_all(self):
        import stats
        for obj in self.objects.values():
            if obj["type"] in ("DECISION", "NON_DECISION") and "consequence" in obj:
                obj["grades"] = stats.stored_grades(obj)

    # -------------------------------------------------- NCRs and CHANGES
    def apply_changes(self):
        """Apply curation_ncr.CHANGES in order. A recode asserts the claim
        carries the CHANGE's `from`; a retype asserts the type; every other
        kind asserts that what it names exists. Nothing is applied silently."""
        vocab = reglib.vocabulary()
        for seq, (chid, kind, obj, field, frm, to, reason, ncr, wo) in enumerate(NCRC.CHANGES, 1):
            target = self.c2_key.get(obj, obj)
            o = self.objects.get(target)
            if kind == "pin":
                applied = "pinned (bundle_pins.json, bundle/MANIFEST.sha256)"
            elif kind == "recode" and field == "id":
                if o is None or frm in self.objects:
                    raise BuildError("%s: id %s -> %s not as stated" % (chid, frm, to))
                applied = "one object, id %s (no object %s)" % (to, frm)
            elif kind == "recode":
                if o is None:
                    raise BuildError("%s: object %s not built" % (chid, obj))
                c = o["claims"].get(field)
                if c is None:
                    raise BuildError("%s: %s has no claim %s" % (chid, target, field))
                if c["value"] != frm:
                    raise BuildError("%s: source has %r for %s.%s, CHANGE says %r"
                                     % (chid, c["value"], target, field, frm))
                c.setdefault("history", []).append(
                    {"version": o["version"], "value": frm, "by": c["coder"], "change": None})
                o["version"] += 1
                c.update({"value": to, "coder": REGISTRY, "status": "PROPOSED",
                          "independence": "NOT_INDEPENDENT", "rationale": reason})
                c["history"].append({"version": o["version"], "value": to,
                                     "by": REGISTRY, "change": chid})
                if field == "direction":
                    o["claims"]["direction_rel_bearer"]["value"] = collapse(to)
                applied = "applied to %s.%s" % (target, field)
            elif kind == "retype":
                if o is None or o["type"] != frm:
                    raise BuildError("%s: %s is not %s" % (chid, obj, frm))
                o["type"] = to
                o["version"] += 1
                applied = "applied to %s" % target
            elif kind == "add_field" and obj == "*":
                key = field.split(".")[-1]
                present = [x for x in self.objects.values()
                           if x["type"] in ("DECISION", "NON_DECISION") and "consequence" in x]
                if key == "substitution":
                    ok = all("substitution" in x["consequence"]["C_restrict"] for x in present)
                else:
                    ok = all(x["consequence"]["C_restrict"]["registry"] is not None
                             for x in present if x.get("in_sample"))
                if not ok:
                    raise BuildError("%s: %s missing on a graded case" % (chid, field))
                applied = "present on all %d graded cases" % len(present)
            elif kind == "add_field":
                if o is None:
                    raise BuildError("%s: object %s not built" % (chid, obj))
                if field == "forcing":
                    c = o["claims"]["forcing_kind"]
                    if c["value"] != "none":
                        raise BuildError("%s: %s forcing already %s" % (chid, obj, c["value"]))
                    c.setdefault("history", []).append(
                        {"version": o["version"], "value": "none", "by": c["coder"], "change": None})
                    o["version"] += 1
                    c.update({"value": to, "inference": True, "rationale": reason})
                    c["history"].append({"version": o["version"], "value": to,
                                         "by": REGISTRY, "change": chid})
                else:
                    if field in o["claims"]:
                        raise BuildError("%s: %s already has %s" % (chid, obj, field))
                    o["claims"][field] = claim(to, "PROPOSED", REGISTRY, rationale=reason)
                    o["version"] += 1
                applied = "applied to %s.%s" % (obj, field)
            elif kind == "add_object":
                names = [obj] if obj not in ("REVERSAL", "PRIOR") else [
                    x.strip() for x in str(to).split(",")]
                missing = [x for x in names if x not in self.objects]
                if missing:
                    raise BuildError("%s: objects %s not built" % (chid, missing))
                applied = "present: %s" % ", ".join(names)
            elif kind == "add_vocab":
                applied = "vocabulary carries the additions (schema/vocabulary.json)"
            elif kind == "drop_vocab":
                if frm in vocab["object_types"]["values"]:
                    raise BuildError("%s: %s still in object_types" % (chid, frm))
                applied = "%s absent from object_types" % frm
            else:
                raise BuildError("%s: kind %s not handled" % (chid, kind))
            self.add({"id": chid, "type": "CHANGE", "seq": seq, "date": NCRC.DATE,
                      "kind": kind, "object": target, "field": field,
                      "from": frm, "to": to, "reason": reason, "ncr": ncr, "wo": wo,
                      "author": REGISTRY, "applied": applied})
            if ncr:
                self.edge(chid, ncr, "closes", "PROPOSED")
        # the curation's R3 flags and the change log must land on the same values
        for cid, ex in sorted(CASES.EXTRA.items()):
            got = (self.objects[cid]["claims"]["forced_action"]["value"],
                   self.objects[cid]["claims"]["forced_outcome"]["value"])
            if got != tuple(ex["forced"]):
                raise BuildError("%s: forced %s after CHANGES, curation says %s"
                                 % (cid, got, ex["forced"]))

    def ncrs(self):
        st_by = {}
        for stid, src, needle, ncr, template in NCRC.STATEMENTS:
            st_by.setdefault(ncr, []).append(stid)
        for (nid, origin, ref, items, evidence, finding, disp, reason, changes,
             state, tier, note) in NCRC.NCRS:
            audit = origin == "AUDIT_WO-REG-1"
            for r in evidence:
                self.row(r)
            self.add({"id": nid, "type": "NCR", "origin": origin, "ref": ref,
                      "finding": finding, "item": items,
                      "evidence": sorted(self.ev_id(r) for r in evidence),
                      "disposition": disp, "reason": reason, "changes": changes,
                      "statements": sorted(st_by.get(nid, [])),
                      "originator": REGISTRY if audit else "ACT-REVIEWER",
                      "adjudicator": REGISTRY,
                      "independence": "NOT_INDEPENDENT" if audit else "CONTAMINATED-BY-PRIOR",
                      "state": state, "rigor_tier": tier, "single_failure": audit,
                      "note": note})
            for it in items:
                tgt = self.c2_key.get(it, it)
                if tgt in self.objects and self.objects[tgt]["type"] in (
                        "DECISION", "NON_DECISION", "EVIDENCE", "REVERSAL", "SOURCE", "ACTOR"):
                    self.edge(nid, tgt, "concerns", "PROPOSED")
            for st in st_by.get(nid, []):
                self.edge(nid, st, "concerns", "PROPOSED")
            for r in evidence:
                self.edge(self.ev_id(r), nid, "supports", "OBSERVED")

    # -------------------------------------------------- run
    def run(self):
        import stats
        self.sources_and_evidence()
        self.actors_authority()
        self.add({"id": "ACT-UNKNOWN", "type": "ACTOR", "actor_type": "office",
                  "name": "decision-makers and advisers not individually identified",
                  "role_at_time": "placeholder for an unsearched disclosure record",
                  "date_range": "-", "basis": [], "status": "PROPOSED"})
        self.cases()
        self.outcomes()
        self.reversals()
        self.vocab_objects()
        self.conflicts()
        self.apply_changes()
        self.grade_all()
        values = stats.statement_values(self.objects)
        self.statements(values)
        self.ncrs()
        for e in self.edges:
            for end in (e["from"], e["to"]):
                if end not in self.objects:
                    raise BuildError("edge %s %s -> %s: %s unknown"
                                     % (e["type"], e["from"], e["to"], end))
        return self.render()

    def render(self):
        schema = reglib.load_json(reglib.SCHEMA)
        files = {}
        type_file = {}
        for relpath, t in schema["x-files"].items():
            if t == "case":
                type_file["DECISION"] = relpath
                type_file["NON_DECISION"] = relpath
            elif t != "EDGE":
                type_file[t] = relpath
            files[relpath] = []
        for oid in sorted(self.objects):
            o = self.objects[oid]
            files[type_file[o["type"]]].append(o)
        edges = sorted(self.edges, key=lambda e: (e["type"], e["from"], e["to"],
                                                  e.get("order", -1), e.get("kind", "")))
        files["registry/edges.json"] = edges
        return files


def serialize(obj):
    import json
    return json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def write(files, regdir=reglib.REGDIR):
    os.makedirs(regdir, exist_ok=True)
    man = {"_note": "sha256 of every registry file written by tools/build.py; "
                    "a file edited by hand fails reglib.check_manifest",
           "files": {}}
    for relpath, data in sorted(files.items()):
        text = serialize(data)
        path = os.path.join(os.path.dirname(regdir), relpath)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        man["files"][relpath] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    reglib.dump_json(man, os.path.join(regdir, "MANIFEST.json"))
    return man


def check(files, regdir=reglib.REGDIR):
    diffs = []
    for relpath, data in sorted(files.items()):
        path = os.path.join(os.path.dirname(regdir), relpath)
        want = serialize(data)
        got = open(path, "r", encoding="utf-8").read() if os.path.exists(path) else None
        if got != want:
            diffs.append(relpath)
    return diffs


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("build.py: checks run in tools/validate.py --selftest\n")
        return 2
    bad = reglib.check_pins()
    if bad:
        for p, w, g in bad:
            print("PIN MISMATCH %s want %s got %s" % (p, w[:12], g[:12]))
        return 1
    files = Builder().run()
    if "--check" in argv:
        diffs = check(files)
        print("build --check: %d of %d registry files differ%s"
              % (len(diffs), len(files), (": " + ", ".join(diffs)) if diffs else ""))
        return 1 if diffs else 0
    man = write(files)
    n = sum(len(v) for k, v in files.items() if not k.endswith("edges.json"))
    print("built %d objects, %d edges, %d files; MANIFEST pins %d"
          % (n, len(files["registry/edges.json"]), len(files), len(man["files"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
