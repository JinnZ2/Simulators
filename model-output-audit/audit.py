#!/usr/bin/env python3
"""Cross-repo audit of failure claims in model-tagged output. Stdlib only. Rules: DECLARED.json.

    python3 audit.py inventory CLONES     -> inventory.jsonl, repos.json
    python3 audit.py claims CLONES        -> claims.jsonl          (commit messages + HEAD file lines)
    python3 audit.py subset CLONES        -> subset.json           (the rerun subset, chosen by rule)
    python3 audit.py rerun CLONES WORK    -> reruns.jsonl          (one rerun log per subset claim)
    python3 audit.py probe                -> probes.json           (hosts named in limit claims)

CLONES is a directory holding one full clone per repo. It is not part of this folder.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "patterns.json"), encoding="utf-8"))
TYPES = {k: re.compile(v, re.I) for k, v in P["types"].items()}
MODEL = re.compile(r"(Claude(?: [A-Z][a-z]+)?(?: [0-9.]+)?|Perplexity|Manus|Kimi|DeepSeek|GPT-[0-9.]+|Gemini|Copilot|Grok)", re.I)
AGENT_AUTHORS = re.compile(r"^(claude|manus\b.*|ai-integrator-bot|hypothesis-engine\[bot\]|copilot-swe-agent\[bot\]|github-actions\[bot\])$", re.I)
CODE = (".py", ".js", ".ts", ".ino", ".c", ".cpp", ".rs", ".go", ".sh")
ANALYSIS = (".json", ".csv", ".jsonl", ".yaml", ".yml")
DOC = (".md", ".txt", ".pdf", ".html", ".rst")
EXPERIMENT = re.compile(r"test|sample|result|run|fixture|experiment", re.I)


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo] + list(args), capture_output=True)
    if check and r.returncode:
        raise RuntimeError("git %s: %s" % (" ".join(args), r.stderr.decode("utf-8", "replace")[:300]))
    return r.stdout.decode("utf-8", "replace")


def model_of(author, trailers):
    """(model, version, tag_text) from the commit's own tag only."""
    for t in trailers:
        name = t.split("<")[0].strip()
        if "anthropic" in t or "perplexity" in t or "manus" in t.lower():
            m = re.match(r"^(Claude|Perplexity|Manus)\s*(.*)$", name)
            if m:
                fam = re.match(r"^([A-Za-z]+)?\s*([0-9.]+)?", m.group(2) or "")
                return m.group(1) + ((" " + fam.group(1)) if fam and fam.group(1) else ""), \
                    (fam.group(2) if fam else None) or None, "Co-Authored-By: " + t
    if AGENT_AUTHORS.match(author):
        base = "Manus" if author.lower().startswith("manus") else ("Claude" if author.lower() == "claude" else author)
        return base, None, "author: " + author
    return None, None, None


def artifact_type(files):
    n = {"code": 0, "experiment": 0, "analysis": 0, "doc": 0}
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if EXPERIMENT.search(f):
            n["experiment"] += 1
        elif ext in CODE:
            n["code"] += 1
        elif ext in ANALYSIS:
            n["analysis"] += 1
        elif ext in DOC:
            n["doc"] += 1
    best = max(n.values())
    return next(k for k in ("code", "experiment", "analysis", "doc") if n[k] == best) if best else None


def commits(repo):
    sep, rs = "\x1f", "\x1e"
    out = git(repo, "log", "--name-only", "--format=" + rs + sep.join(["%H", "%aI", "%an", "%s", "%b", "%(trailers:key=Co-Authored-By,valueonly,separator=;)"]) + sep)
    for chunk in out.split(rs)[1:]:
        h, date, author, subject, body, trailers, files = chunk.split(sep)
        yield {"commit": h, "date": date, "author": author, "subject": subject, "body": body,
               "trailers": [t for t in trailers.split(";") if t.strip()], "files": [f for f in files.strip().split("\n") if f]}


def inventory(clones):
    repos, out = [], open(os.path.join(HERE, "inventory.jsonl"), "w", encoding="utf-8")
    listing = [l.strip() for l in open(os.path.join(HERE, "org_listing.txt"), encoding="utf-8") if l.strip()]
    for name in listing:
        path = os.path.join(clones, name)
        if not os.path.isdir(path):
            repos.append({"repo": name, "state": "NOT_CLONED", "reason": "clone refused: private repository outside this session's access"})
            continue
        n = 0
        for c in commits(path):
            model, version, tag = model_of(c["author"], c["trailers"])
            out.write(json.dumps({"record_id": "%s@%s" % (name, c["commit"][:12]), "repo": name, "commit": c["commit"], "date": c["date"],
                                  "author": c["author"], "model": model, "model_version": version, "tag_text": tag,
                                  "artifact_type": artifact_type(c["files"]), "files_changed": len(c["files"]),
                                  "paths": c["files"][:50], "agency": None}, ensure_ascii=False) + "\n")
            n += 1
        repos.append({"repo": name, "state": "CLONED", "head": git(path, "rev-parse", "HEAD").strip(),
                      "branch": git(path, "rev-parse", "--abbrev-ref", "HEAD").strip(), "commits": n})
    json.dump({"listed": len(listing), "repos": repos}, open(os.path.join(HERE, "repos.json"), "w", encoding="utf-8"), indent=1)
    print("repos listed %d, cloned %d, commits %d" % (len(listing), sum(r["state"] == "CLONED" for r in repos), sum(r.get("commits", 0) for r in repos)))


def match(line):
    return [k for k, rx in TYPES.items() if rx.search(line)]


def claims(clones):
    inv = {}
    for l in open(os.path.join(HERE, "inventory.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        inv[(r["repo"], r["commit"])] = r["record_id"]
    out = open(os.path.join(HERE, "claims.jsonl"), "w", encoding="utf-8")
    n = {"A": 0, "B": 0}
    unattributed = []
    for repo in [r["repo"] for r in json.load(open(os.path.join(HERE, "repos.json")))["repos"] if r["state"] == "CLONED"]:
        path = os.path.join(clones, repo)
        for c in commits(path):                                  # (A) commit messages
            for i, line in enumerate([c["subject"]] + c["body"].split("\n")):
                line = line.strip()
                for t in (match(line) if line and len(line) <= P["max_line_chars"] and not line.lower().startswith("co-authored-by") else []):
                    out.write(json.dumps({"claim_id": "A:%s@%s:%d:%s" % (repo, c["commit"][:12], i, t), "source": "A",
                                          "record_id": inv[(repo, c["commit"])], "quote": line, "claim_type": t,
                                          "location": {"repo": repo, "commit": c["commit"], "message_line": i}, "source_hash": c["commit"]}, ensure_ascii=False) + "\n")
                    n["A"] += 1
        files = [f for f in git(path, "ls-files", "-z").split("\0") if f and os.path.splitext(f)[1].lower() in P["text_extensions"]]
        for f in files:                                          # (B) HEAD file lines
            full = os.path.join(path, f)
            if not os.path.isfile(full) or os.path.islink(full) or os.path.getsize(full) > P["max_file_bytes"]:
                continue
            lines = open(full, encoding="utf-8", errors="replace").read().split("\n")
            hits = [(i, l.strip(), t) for i, l in enumerate(lines, 1) if l.strip() and len(l) <= P["max_line_chars"] for t in match(l)]
            if not hits:
                continue
            blob = git(path, "rev-parse", "HEAD:" + f, check=False).strip()
            blame, cur = {}, None
            r = subprocess.run(["git", "-C", path, "blame", "--line-porcelain", "HEAD", "--", f], capture_output=True)
            if r.returncode == 0:
                for bl in r.stdout.decode("utf-8", "replace").split("\n"):
                    m = re.match(r"^([0-9a-f]{40}) \d+ (\d+)", bl)
                    if m:
                        blame[int(m.group(2))] = m.group(1)
            else:
                unattributed.append("%s:%s" % (repo, f))
            for i, q, t in hits:
                commit = blame.get(i)
                out.write(json.dumps({"claim_id": "B:%s:%s:%d:%s" % (repo, f, i, t), "source": "B",
                                      "record_id": inv.get((repo, commit)), "quote": q, "claim_type": t,
                                      "location": {"repo": repo, "path": f, "line": i, "written_by_commit": commit}, "source_hash": blob}, ensure_ascii=False) + "\n")
                n["B"] += 1
        print(repo, n, flush=True)
    json.dump({"claims": n, "files_not_attributed": unattributed}, open(os.path.join(HERE, "claims_summary.json"), "w"), indent=1)


PY = re.compile(r"(?<![\w./-])([\w./-]+\.py)\b")
RERUN_TYPES = ("test_failure", "cant_run", "defect", "convergence")
SUBSET_MAX = 400
_trees = {}


def tree(path, rev):
    if (path, rev) not in _trees:
        _trees[(path, rev)] = set(git(path, "ls-tree", "-r", "--name-only", rev).split("\n"))
    return _trees[(path, rev)]


def resolve(names, files, near=None):
    """A named .py file counts if it is a path in the tree, or sits beside the quoting file, or its
    base name is the base name of exactly one file in the tree."""
    out = set()
    for n in names:
        n = n.lstrip("./")
        if n in files:
            out.add(n)
        elif near and os.path.join(os.path.dirname(near), n) in files:
            out.add(os.path.join(os.path.dirname(near), n))
        else:
            same = [f for f in files if os.path.basename(f) == os.path.basename(n) and f.endswith("/" + n) or f == n]
            if not same:
                same = [f for f in files if os.path.basename(f) == os.path.basename(n)] if "/" not in n else []
            if len(same) == 1:
                out.add(same[0])
            elif len(same) > 1:
                return None            # ambiguous name: not exactly one file
    return out


def subset(clones):
    heads = {r["repo"]: r["head"] for r in json.load(open(os.path.join(HERE, "repos.json")))["repos"] if r["state"] == "CLONED"}
    cand, seen = [], set()
    for l in open(os.path.join(HERE, "claims.jsonl"), encoding="utf-8"):
        c = json.loads(l)
        if c["claim_type"] not in RERUN_TYPES:
            continue
        names = set(PY.findall(c["quote"]))
        if not names:
            continue
        loc = c["location"]
        rev = loc["commit"] if c["source"] == "A" else heads[loc["repo"]]
        got = resolve(names, tree(os.path.join(clones, loc["repo"]), rev), loc.get("path"))
        if not got or len(got) != 1:
            continue
        target = sorted(got)[0]
        key = (loc["repo"], rev, target, c["quote"])        # one line matching two types is one rerun
        if key in seen:
            continue
        seen.add(key)
        cand.append({"claim_id": c["claim_id"], "repo": loc["repo"], "rev": rev, "target": target,
                     "order": hashlib.sha256(c["claim_id"].encode()).hexdigest()})
    cand.sort(key=lambda x: x["order"])
    json.dump({"eligible": len(cand), "taken": min(len(cand), SUBSET_MAX), "rule": "DECLARED.json rules.verification_subset",
               "claims": cand[:SUBSET_MAX]}, open(os.path.join(HERE, "subset.json"), "w"), indent=1)
    print("eligible %d, taken %d" % (len(cand), min(len(cand), SUBSET_MAX)))


ENVERR = re.compile(r"ModuleNotFoundError|No module named|FileNotFoundError|No such file or directory|URLError|ConnectionError|Temporary failure in name resolution|ProxyError")
FAILLINE = re.compile(r"\b[1-9]\d* (failed|failures?|errors?)\b|^FAIL(ED)?\b|\bAssertionError\b|Traceback \(most recent call last\)", re.M)
USAGE = re.compile(r"^usage:|refus(es|ed|ing)? .*--selftest|requires? (an? )?argument", re.I | re.M)


def run_one(args):
    clones, wt_root, c = args
    wt = os.path.join(wt_root, c["repo"], c["rev"][:12])
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
    runs = []
    for cwd, target in ((wt, c["target"]), (os.path.join(wt, os.path.dirname(c["target"])), os.path.basename(c["target"]))):
        try:
            r = subprocess.run(["python3", target], cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True, timeout=120)
            out = (r.stdout + r.stderr).decode("utf-8", "replace")
            runs.append({"cwd": os.path.relpath(cwd, wt), "exit": r.returncode, "tail": out[-1500:]})
        except subprocess.TimeoutExpired:
            runs.append({"cwd": os.path.relpath(cwd, wt), "exit": None, "tail": "TIMEOUT after 120 s"})
        if runs[-1]["exit"] == 0 or not ENVERR.search(runs[-1]["tail"]) or os.path.dirname(c["target"]) == "":
            break
    last = runs[-1]
    if last["exit"] is None:
        state = "TIMEOUT"
    elif last["exit"] != 0 and ENVERR.search(last["tail"]):
        state = "ENV_ERROR"
    elif last["exit"] == 2 and USAGE.search(last["tail"]) or (last["exit"] != 0 and USAGE.search(last["tail"]) and not FAILLINE.search(last["tail"])):
        state = "NEEDS_ARGUMENTS"
    elif last["exit"] != 0 or FAILLINE.search(last["tail"]):
        state = "FAILS"
    else:
        state = "CLEAN"
    return dict(c, command="python3 " + c["target"], runs=runs, rerun_state=state)


def rerun(clones, wt_root):
    from concurrent.futures import ThreadPoolExecutor
    cs = json.load(open(os.path.join(HERE, "subset.json")))["claims"]
    for c in cs:                 # checkouts one at a time, before any run
        wt = os.path.join(wt_root, c["repo"], c["rev"][:12])
        if not os.path.isdir(wt):
            os.makedirs(os.path.dirname(wt), exist_ok=True)
            subprocess.run(["git", "-C", os.path.join(clones, c["repo"]), "worktree", "add", "-f", "--detach", wt, c["rev"]], capture_output=True)
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run_one, [(clones, wt_root, c) for c in cs]))
    with open(os.path.join(HERE, "reruns.jsonl"), "w", encoding="utf-8") as f:
        for r in res:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    import collections
    print(collections.Counter(r["rerun_state"] for r in res))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "inventory":
        inventory(sys.argv[2])
    elif cmd == "claims":
        claims(sys.argv[2])
    elif cmd == "subset":
        subset(sys.argv[2])
    elif cmd == "rerun":
        rerun(sys.argv[2], sys.argv[3])
