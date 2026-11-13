#!/usr/bin/env python3
"""Check concept_map.json and collisions.json; render CONCEPT_MAP.md and COLLISIONS.md from them.

    python3 check_concept_map.py            check: every path exists, MD matches JSON
    python3 check_concept_map.py --write    rewrite CONCEPT_MAP.md from the JSON
    python3 check_concept_map.py --strict   also fail when another repo's checkout is absent
    python3 check_concept_map.py --selftest plant defects, show each check fires

A location is {repo, ref, path, role, builder, note}. Simulators paths with ref null
are read from this working tree. Other repos are read with `git cat-file -e ref:path`
from a sibling checkout (../<repo>, ../jinnz2/<repo>, or $CONCEPT_MAP_REPOS/<repo>).
No checkout: NOT_CHECKED, never OK. A pinned `tip` that no longer matches the ref is STALE.
Collision evidence is a URL or note (not checked) or {repo, path, ref}, shown as repo:path@ref and
checked: the ref must resolve (archive/* branches like any other), sit exactly at `tip` if given, contain `tip_contains` if given, hold the path, and match `sha256` if given.
No code is moved by this file. Stdlib only.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
JSON, MD = os.path.join(HERE, "concept_map.json"), os.path.join(HERE, "CONCEPT_MAP.md")
CJSON, CMD = os.path.join(HERE, "collisions.json"), os.path.join(HERE, "COLLISIONS.md")
COMMIT_ROLES = ("origin", "rename", "other", "VOID")
FORM_LABELS = (("a", "a. first model trailer"), ("b", "b. first Claude-Session keyed trailer"),
               ("c", "c. first bare session URL"), ("d", "d. first non-Claude model trailer"))
CFIELDS = ("date", "concept", "agents", "collided", "found", "resolution", "evidence")
ROLES = ("canonical", "candidate", "copy", "nearest")
PENDING = "pending cross-run"


def checkout(repo):
    roots = [os.path.join(HERE, ".."), os.path.join(HERE, "..", "jinnz2")]
    if os.environ.get("CONCEPT_MAP_REPOS"):
        roots.insert(0, os.environ["CONCEPT_MAP_REPOS"])
    for r in roots:
        d = os.path.join(r, repo)
        if os.path.isdir(os.path.join(d, ".git")):
            return d
    return None


def git(d, *a):
    p = subprocess.run(["git", "-C", d] + list(a), capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


def check_location(loc, here=HERE):
    """-> (state, detail); state in OK / MISSING / STALE / NOT_CHECKED."""
    repo, ref, path = loc["repo"], loc.get("ref"), loc["path"]
    if repo == "Simulators" and not ref:
        return ("OK", "") if os.path.exists(os.path.join(here, path)) else ("MISSING", "not in this tree")
    d = here if repo == "Simulators" else checkout(repo)
    if d is None:
        return "NOT_CHECKED", "no checkout of %s" % repo
    if not ref:
        return "MISSING", "a path in another repo needs a ref"
    rc, tip = git(d, "rev-parse", "--short=7", ref)
    if rc:
        return "NOT_CHECKED", "ref %s not fetched in %s" % (ref, d)
    if loc.get("tip") and not tip.startswith(loc["tip"][:7]):
        return "STALE", "%s is now %s, row pinned %s" % (ref, tip, loc["tip"])
    rc, _ = git(d, "cat-file", "-e", "%s:%s" % (ref, path.rstrip("/")))
    return ("OK", "") if rc == 0 else ("MISSING", "not at %s" % ref)


def row_problems(row):
    out, locs = [], row.get("locations", [])
    for k in ("concept", "home", "status", "decided_by", "locations"):
        if k not in row:
            out.append("field %s absent" % k)
    for l in locs:
        if l.get("role") not in ROLES:
            out.append("role %r not in %s" % (l.get("role"), ROLES))
        if not l.get("builder"):
            out.append("%s: builder absent (write 'not recorded')" % l.get("path"))
    n = {r: sum(1 for l in locs if l.get("role") == r) for r in ROLES}
    home = row.get("home")
    if home == "CANONICAL" and (n["canonical"] != 1 or row.get("decided_by") == PENDING):
        out.append("CANONICAL needs exactly one canonical location and a decision that is not pending")
    if home == "CANDIDATE" and (n["candidate"] < 2 or n["canonical"]):
        out.append("CANDIDATE needs two or more candidate locations and no canonical one")
    if home == "SINGLE" and (n["candidate"] + n["canonical"] != 1):
        out.append("SINGLE needs exactly one home location")
    if home == "NOT_LOCATED" and (n["candidate"] or n["canonical"] or not row.get("searched")):
        out.append("NOT_LOCATED needs no home location and a stated search")
    if home not in ("CANONICAL", "CANDIDATE", "SINGLE", "NOT_LOCATED"):
        out.append("home %r unknown" % home)
    return out


def where(l):
    return "%s%s:%s" % (l["repo"], "@" + l["ref"] if l.get("ref") else "", l["path"])


def render(data):
    o = ["# CONCEPT_MAP", "",
         "Generated from `concept_map.json` by `check_concept_map.py --write`. Edit the JSON, not this file.",
         "One block per concept. No code is moved. As of %s." % data["as_of"], "",
         "home: CANONICAL (decided), CANDIDATE (two or more homes, undecided), SINGLE (one copy), NOT_LOCATED.", ""]
    for r in data["rows"]:
        o += ["## %s" % r["concept"], "", "- home: %s" % r["home"], "- status: %s" % r["status"],
              "- decided by: %s" % r["decided_by"]]
        if r.get("searched"):
            o.append("- searched: %s" % r["searched"])
        if r.get("note"):
            o.append("- note: %s" % r["note"])
        if r["locations"]:
            o += ["", "| role | where | builder | note |", "|---|---|---|---|"]
            for l in r["locations"]:
                o.append("| %s | `%s` | %s | %s |" % (l["role"], where(l), l["builder"], l.get("note", "")))
        o.append("")
    return "\n".join(o)


def render_collisions(data):
    o = ["# COLLISIONS", "",
         "Generated from `collisions.json` by `check_concept_map.py --write`. Edit the JSON, not this file.",
         "One block per multi-agent collision. Rows are kept, not resolved away; a resolved row stays.",
         "As of %s." % data["as_of"], ""]
    for r in data["rows"]:
        o += ["## %s  %s" % (r["date"], r["concept"]), "", "- agents: %s" % r["agents"],
              "- what collided: %s" % r["collided"], "- how found: %s" % r["found"],
              "- resolution: %s" % r["resolution"]]
        if r.get("note"):
            o.append("- note: %s" % r["note"])
        o += ["- evidence: " + "; ".join(ev_text(e) for e in r["evidence"])]
        for sd in r.get("sides", []):
            if sd["commits"] == "VOID":
                o.append("- side %s: model VOID; session VOID; date VOID (%s)" % (sd["label"], sd["void_reason"]))
                continue
            cs = sd["commits"]
            ds = sorted(c["date"] for c in cs)
            o.append("- side %s (%s, %d commit%s, %s .. %s): model %s; session %s" % (
                sd["label"], sd["repo"], len(cs), "" if len(cs) == 1 else "s", ds[0], ds[-1],
                " | ".join(sorted({c["model"] for c in cs})), " | ".join(sorted({c["session"] for c in cs}))))
            o.append("  - commits: " + ", ".join("%s %s" % (c["sha"], c["role"]) for c in cs))
            for c in cs:
                if c["role"] != "VOID":
                    o.append("  - %s role %s: %s" % (c["sha"], c["role"], c["role_basis"]))
            vr = sorted({(k, c[k + "_void_reason"]) for c in cs for k in ("model", "session", "role") if c.get(k + "_void_reason")})
            for k, why in vr:
                o.append("  - %s VOID: %s" % (k, why))
        o.append("")
    if "marking_start" in data:
        o += ["## MARKING START", "", "Per repo, four forms, none picked. Before a form's first commit: that field VOID (not inferred from date or style).", ""]
        for m in data["marking_start"]:
            fm = m.get("forms") or {}
            for k, label in FORM_LABELS:
                v = fm.get(k) or {}
                if v.get("sha") in (None, "", "VOID"):
                    o.append("- %s, %s: VOID (%s)" % (m["repo"], label, v.get("void_reason") or "MISSING"))
                else:
                    extra = "; ".join("%s %s" % (x, v[x]) for x in ("agent", "model", "author") if v.get(x))
                    o.append("- %s, %s: `%s` %s%s" % (m["repo"], label, v["sha"], v.get("date") or "DATE MISSING", ("; " + extra) if extra else ""))
            o.append("  - %d commits on main before line a" % m["commits_before_on_main"])
            if m.get("note"):
                o.append("  - note: %s" % m["note"])
        o += ["", "Untrailered commits (no Co-Authored-By trailer) after line a:", "",
              "| repo | main tip | merge | non-merge web-UI | non-merge other | total |", "|---|---|---|---|---|---|"]
        for m in data["marking_start"]:
            u = m["untrailered_after_start"]
            o.append("| %s | `%s` | %d | %d | %d | %d |" % (m["repo"], u["main_tip"], u["merge"], u["web_ui"], u["other"], u["total"]))
        uc = data.get("untrailered_claude_simulators")
        if uc:
            o += ["", "Untrailered, non-merge, Claude-committed commits, %s, after %s (main tip %s):" % (uc["repo"], uc["after"], uc["main_tip"]), "",
                  "| hash | date | subject | bare claude.ai/code URL |", "|---|---|---|---|"]
            for c in uc["commits"]:
                o.append("| `%s` | %s | %s | %s |" % (c["sha"], c["date"], c["subject"].replace("|", "\\|"), c["bare_url"]))
            o += ["", "- rule: %s" % uc["rule"], "- bare URL: %s" % uc["bare_url_rule"],
                  "- count %d; date range %s .. %s" % (uc["count"], uc["first"], uc["last"]),
                  "- per month (UTC): " + ", ".join("%s %d" % (k, v) for k, v in uc["per_month_utc"].items())]
        o += ["", "- note: %s" % data["marking_note"], ""]
    if "conditions" in data:
        o += ["## CONDITIONS (as of %s)" % data["conditions"]["as_of"], "", "These affect how to read the record.", ""]
        o += ["- %s" % c for c in data["conditions"]["items"]] + [""]
    if "marking_start" in data:
        o += ["## SUMMARY", ""] + summary_lines(data) + [""]
    return "\n".join(o)


def side_marked(sd):
    return sd["commits"] != "VOID" and bool(sd["commits"]) and all(
        c["model"] != "VOID" for c in sd["commits"])


def summary_lines(data):
    """Counts only rows where EVERY side carries a trailer. No interpretation."""
    both = [r for r in data["rows"] if r.get("sides") and all(side_marked(s) for s in r["sides"])]
    out_rows = [r["concept"] for r in data["rows"] if r not in both]
    differ, same = [], []
    for r in both:
        ms = [frozenset(c["model"] for c in s["commits"]) for s in r["sides"]]
        (same if len(set(ms)) == 1 else differ).append(r)
    same_diff_session = [r for r in same if len({frozenset(c["session"] for c in s["commits"]) for s in r["sides"]}) > 1]
    same_same_session = [r for r in same if r not in same_diff_session]
    pairs = dict(differ=0, same_diff=0, same_same=0)
    for r in both:
        ss = r["sides"]
        for i in range(len(ss)):
            for j in range(i + 1, len(ss)):
                mi = {c["model"] for c in ss[i]["commits"]}; mj = {c["model"] for c in ss[j]["commits"]}
                si = {c["session"] for c in ss[i]["commits"]}; sj = {c["session"] for c in ss[j]["commits"]}
                pairs["differ" if mi != mj else ("same_diff" if si != sj else "same_same")] += 1
    names = lambda rs: ", ".join(r["concept"] for r in rs) or "none"
    return ["- rows counted (every side carries a trailer): %d of %d; not counted: %s" % (len(both), len(data["rows"]), ", ".join(out_rows) or "none"),
            "- models differ: %d (%s)" % (len(differ), names(differ)),
            "- same model, different session: %d (%s)" % (len(same_diff_session), names(same_diff_session)),
            "- same model, same session: %d (%s)" % (len(same_same_session), names(same_same_session)),
            "- by side pair over counted rows: models differ %d, same model different session %d, same model same session %d" % (
                pairs["differ"], pairs["same_diff"], pairs["same_same"]),
            "- no interpretation until n is larger."]


def ev_text(e):
    if isinstance(e, str):
        return e
    return "`%s:%s%s`" % (e["repo"], e["path"], "@" + e["ref"] if e.get("ref") else "")


def check_evidence(e, here=HERE):
    """Evidence written as path@branch-or-commit. -> (state, detail).
    A ref that no longer resolves in a present checkout is GONE: cleanup cannot orphan evidence silently."""
    repo, ref, path = e["repo"], e.get("ref"), e["path"]
    d = here if repo == "Simulators" else checkout(repo)
    if d is None:
        return "NOT_CHECKED", "no checkout of %s" % repo
    if not ref:
        return ("OK", "") if os.path.exists(os.path.join(d, path)) else ("MISSING", "not in the working tree")
    rc, _ = git(d, "rev-parse", "--verify", "--quiet", ref + "^{commit}")
    if rc:
        return "GONE", "ref %s does not resolve (deleted, or not fetched: git fetch origin)" % ref
    if e.get("tip"):
        _, now = git(d, "rev-parse", ref + "^{commit}")
        if not now.startswith(e["tip"]):
            return "GONE", "%s moved to %s, pinned %s" % (ref, now[:7], e["tip"][:7])
    if e.get("tip_contains"):
        rc, _ = git(d, "merge-base", "--is-ancestor", e["tip_contains"], ref)
        if rc:
            return "GONE", "%s no longer contains %s" % (ref, e["tip_contains"])
    rc, _ = git(d, "cat-file", "-e", "%s:%s" % (ref, path))
    if rc:
        return "MISSING", "not at %s" % ref
    if e.get("sha256"):
        import hashlib
        blob = subprocess.run(["git", "-C", d, "show", "%s:%s" % (ref, path)], capture_output=True).stdout
        if hashlib.sha256(blob).hexdigest() != e["sha256"]:
            return "CHANGED", "sha256 differs from the pinned value"
    return "OK", ""


def collision_evidence(data, strict=False, quiet=False):
    fails, ok, nc = [], 0, 0
    for r in data["rows"]:
        for e in r.get("evidence") or []:
            if isinstance(e, str):
                continue
            st, why = check_evidence(e)
            if st == "OK":
                ok += 1
            elif st == "NOT_CHECKED":
                nc += 1
                if not quiet:
                    print("NOT_CHECKED  %s: %s (%s)" % (r["concept"], ev_text(e), why))
                if strict:
                    fails.append("NOT_CHECKED under --strict: %s" % ev_text(e))
            else:
                fails.append("%s: evidence %s %s (%s)" % (r["concept"], st, ev_text(e), why))
    return fails, ok, nc


def collision_problems(data, md_text):
    out = []
    for i, r in enumerate(data["rows"]):
        for k in CFIELDS:
            if not r.get(k):
                out.append("collision %d (%s): field %s empty (write OPEN or NOT LOCATED)" % (i + 1, r.get("concept"), k))
        for j, sd in enumerate(r.get("sides", [])):
            if sd.get("commits") == "VOID":
                if not sd.get("void_reason"):
                    out.append("collision %d side %d: commits VOID with no void_reason" % (i + 1, j + 1))
                continue
            if not sd.get("commits"):
                out.append("collision %d side %d: no commits (write VOID with a void_reason)" % (i + 1, j + 1))
            for c in sd.get("commits") or []:
                for k in ("sha", "date", "model", "session", "role"):
                    if not c.get(k):
                        out.append("collision %d side %d %s: field %s empty (write VOID)" % (i + 1, j + 1, c.get("sha"), k))
                if c.get("role") and c["role"] not in COMMIT_ROLES:
                    out.append("collision %d side %d %s: role %r not in %s" % (i + 1, j + 1, c.get("sha"), c["role"], COMMIT_ROLES))
                if c.get("role") not in (None, "", "VOID") and not c.get("role_basis"):
                    out.append("collision %d side %d %s: role with no role_basis" % (i + 1, j + 1, c.get("sha")))
                for k in ("model", "session", "role"):
                    if c.get(k) == "VOID" and not c.get(k + "_void_reason"):
                        out.append("collision %d side %d %s: %s VOID with no %s_void_reason" % (i + 1, j + 1, c.get("sha"), k, k))
    for m in data.get("marking_start", []):
        for k, label in FORM_LABELS:
            v = (m.get("forms") or {}).get(k)
            if not v or not v.get("sha"):
                out.append("marking_start %s: form %s missing (write VOID with a void_reason)" % (m["repo"], k))
            elif v["sha"] == "VOID" and not v.get("void_reason"):
                out.append("marking_start %s: form %s VOID with no void_reason" % (m["repo"], k))
            elif v["sha"] != "VOID" and not v.get("date"):
                out.append("marking_start %s: form %s has no date" % (m["repo"], k))
    uc = data.get("untrailered_claude_simulators")
    if not uc:
        out.append("untrailered_claude_simulators: block missing")
    else:
        cs = uc.get("commits") or []
        if not cs:
            out.append("untrailered_claude_simulators: no commits")
        for c in cs:
            for k in ("sha", "date", "subject", "bare_url"):
                if not c.get(k):
                    out.append("untrailered_claude_simulators %s: field %s empty" % (c.get("sha"), k))
            if c.get("bare_url") not in ("yes", "no"):
                out.append("untrailered_claude_simulators %s: bare_url %r is not yes/no" % (c.get("sha"), c.get("bare_url")))
        if uc.get("count") != len(cs):
            out.append("untrailered_claude_simulators: count %s != %d commits listed" % (uc.get("count"), len(cs)))
        ds = sorted(c["date"] for c in cs if c.get("date"))
        if ds and (uc.get("first"), uc.get("last")) != (ds[0], ds[-1]):
            out.append("untrailered_claude_simulators: date range does not match the commits")
        from datetime import datetime, timezone
        pm = {}
        for c in cs:
            if c.get("date"):
                m = datetime.fromisoformat(c["date"]).astimezone(timezone.utc).strftime("%Y-%m")
                pm[m] = pm.get(m, 0) + 1
        if pm != dict(uc.get("per_month_utc") or {}):
            out.append("untrailered_claude_simulators: per-month counts do not match the commits")
    if md_text != render_collisions(data):
        out.append("COLLISIONS.md does not match collisions.json (run --write)")
    return out


def run(data, md_text, strict=False, here=HERE, quiet=False):
    fails, notchecked, ok = [], [], 0
    for r in data["rows"]:
        for p in row_problems(r):
            fails.append("%s: %s" % (r.get("concept"), p))
        for l in r.get("locations", []):
            st, why = check_location(l, here)
            if st == "OK":
                ok += 1
            elif st == "NOT_CHECKED":
                notchecked.append("%s: %s (%s)" % (r["concept"], where(l), why))
            else:
                fails.append("%s: %s %s (%s)" % (r["concept"], st, where(l), why))
    if md_text != render(data):
        fails.append("CONCEPT_MAP.md does not match concept_map.json (run --write)")
    if strict:
        fails += ["NOT_CHECKED under --strict: " + x for x in notchecked]
    if not quiet:
        for x in notchecked:
            print("NOT_CHECKED  " + x)
        for x in fails:
            print("FAIL  " + x)
        print("rows %d   paths OK %d   NOT_CHECKED %d   failed %d" % (len(data["rows"]), ok, len(notchecked), len(fails)))
    return fails, notchecked


def selftest(data):
    import copy
    base, n, bad = render(data), 0, 0

    def expect(name, d, text, word):
        nonlocal n, bad
        f, _ = run(d, text, quiet=True)
        hit = any(word in x for x in f)
        n += 1
        bad += 0 if hit else 1
        print("%s  %s" % ("fires " if hit else "SILENT", name))
    d = copy.deepcopy(data); d["rows"][0]["locations"][0]["path"] = "no/such/path.py"
    d["rows"][0]["locations"][0]["repo"], d["rows"][0]["locations"][0]["ref"] = "Simulators", None
    expect("missing path", d, render(d), "MISSING")
    expect("MD out of date", data, base + "x", "does not match")
    d = copy.deepcopy(data); d["rows"][0]["home"] = "CANONICAL"
    expect("canonical with no decision", d, render(d), "CANONICAL needs")
    d = copy.deepcopy(data); d["rows"][0]["locations"][0]["builder"] = ""
    expect("builder absent", d, render(d), "builder absent")
    d = copy.deepcopy(data)
    nl = [r for r in d["rows"] if r["home"] == "NOT_LOCATED"][0]; nl["searched"] = ""
    expect("NOT_LOCATED with no search", d, render(d), "NOT_LOCATED needs")
    d = copy.deepcopy(data)
    pinned = [l for r in d["rows"] for l in r["locations"] if l.get("tip")]
    if pinned and check_location(pinned[0])[0] == "OK":
        pinned[0]["tip"] = "0000000"
        expect("pinned tip moved", d, render(d), "STALE")
    else:
        print("NOT_RUN  pinned tip moved (no checkout holding a pinned ref)")
    import copy as _c
    cd = json.load(open(CJSON, encoding="utf-8"))
    for name, mut in (("collision field empty", lambda d: d["rows"][0].update(resolution="")),
                      ("COLLISIONS.md out of date", lambda d: d["rows"].pop()),
                      ("side model empty", lambda d: d["rows"][0]["sides"][0]["commits"][0].update(model="")),
                      ("VOID side with no reason", lambda d: d["rows"][-1]["sides"][0].update(void_reason="")),
                      ("role blank", lambda d: d["rows"][0]["sides"][0]["commits"][0].update(role="")),
                      ("role outside vocabulary", lambda d: d["rows"][0]["sides"][0]["commits"][0].update(role="author")),
                      ("role VOID with no reason", lambda d: d["rows"][1]["sides"][0]["commits"][0].pop("role_void_reason")),
                      ("marking form missing", lambda d: d["marking_start"][0]["forms"].pop("c")),
                      ("marking form VOID with no reason", lambda d: d["marking_start"][0]["forms"]["c"].pop("void_reason")),
                      ("marking form with no date", lambda d: d["marking_start"][0]["forms"]["a"].pop("date")),
                      ("untrailered table missing", lambda d: d.pop("untrailered_claude_simulators")),
                      ("untrailered bare_url not yes/no", lambda d: d["untrailered_claude_simulators"]["commits"][0].update(bare_url="")),
                      ("untrailered count differs", lambda d: d["untrailered_claude_simulators"].update(count=31)),
                      ("untrailered month counts differ", lambda d: d["untrailered_claude_simulators"]["per_month_utc"].update({"2026-08": 30})),
                      ("untrailered date range differs", lambda d: d["untrailered_claude_simulators"].update(last="2026-08-24T00:00:00+00:00")),
                      ("session VOID with no reason", lambda d: d["rows"][1]["sides"][0]["commits"][0].pop("session_void_reason"))):
        d = _c.deepcopy(cd); base_md = render_collisions(cd); mut(d)
        hit = bool(collision_problems(d, base_md if "out of date" in name else render_collisions(d)))
        n += 1; bad += 0 if hit else 1
        print("%s  %s" % ("fires " if hit else "SILENT", name))
    pinned_ev = [e for r in cd["rows"] for e in r["evidence"] if isinstance(e, dict) and e.get("ref")]
    live = [e for e in pinned_ev if check_evidence(e)[0] == "OK"]
    if live:
        for name, mut, word in (("evidence ref deleted", lambda e: e.update(ref="origin/no-such-branch"), "GONE"),
                                ("evidence path removed", lambda e: e.update(path="no/such/file"), "MISSING"),
                                ("archive branch moved", lambda e: e.update(tip="0" * 40), "GONE"),
                                ("branch lost the pinned commit", lambda e: e.update(tip_contains="0" * 40), "GONE")):
            e = dict(live[0]); mut(e)
            hit = check_evidence(e)[0] == word
            n += 1; bad += 0 if hit else 1
            print("%s  %s" % ("fires " if hit else "SILENT", name))
        sh = [e for e in live if e.get("sha256")]
        if sh:
            e = dict(sh[0]); e["sha256"] = "0" * 64
            hit = check_evidence(e)[0] == "CHANGED"
            n += 1; bad += 0 if hit else 1
            print("%s  %s" % ("fires " if hit else "SILENT", "pinned sha256 differs"))
    else:
        print("NOT_RUN  evidence plants (no checkout holding an evidence ref)")
    print("planted %d   silent %d" % (n, bad))
    return bad


if __name__ == "__main__":
    data = json.load(open(JSON, encoding="utf-8"))
    cdata = json.load(open(CJSON, encoding="utf-8"))
    if "--write" in sys.argv:
        open(MD, "w", encoding="utf-8").write(render(data))
        open(CMD, "w", encoding="utf-8").write(render_collisions(cdata))
    if "--selftest" in sys.argv:
        sys.exit(1 if selftest(data) else 0)
    md = open(MD, encoding="utf-8").read() if os.path.exists(MD) else ""
    f, _ = run(data, md, strict="--strict" in sys.argv)
    cf = collision_problems(cdata, open(CMD, encoding="utf-8").read() if os.path.exists(CMD) else "")
    ef, eok, enc = collision_evidence(cdata, strict="--strict" in sys.argv)
    cf += ef
    for x in cf:
        print("FAIL  " + x)
    print("collisions %d   evidence paths OK %d   NOT_CHECKED %d   failed %d" % (len(cdata["rows"]), eok, enc, len(cf)))
    sys.exit(1 if f or cf else 0)
