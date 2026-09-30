# SPDX-License-Identifier: CC0-1.0
"""WORK ORDER standing/A-6.3 (2026-09-30): verification split, lint labels, Part B status.

Landed verbatim as WORK_ORDER_A6.3_2026-09-30_verification-split.md and committed ALONE at
EXPECTED_COMMIT_A63 before this module existed.  Additive: A-1..A-6.2 modules are read by
import.  Two prior data rows move, both because the order names them: gate_state_a21.SOURCES21
W-1a / W-2a (item 8, the address leaves the text for a url field) and standing_a61.SOURCES_A61
CE-4e (item 3, a status note).

  0  Part B status: reported in the README and CLAIM_TABLE (RIN_151), not computed here
  1  repo files as sources: location repo:<commit>:<path> plus a remote clone url
  2  consistency is not verification: STORED_UNVERIFIED vs VERIFIED; only VERIFIED lets a
     row read MATCH; a verification record names who/what fetched, the date, the hash obtained
  3  CE-4e status note (coding rule GEOGRAPHIC, undeclared at issue)
  4  lint: a year-shaped number is FLAGGED and credited, a year only with date context
  5  lint: a number directly after a declared identifier token is a LABEL, never a count
  6  a declared alias map for id ranges (P-* -> profiles); no alias is inferred
  7  mutation test over every status gate: a gate whose output never moves is a FAIL
  8  W-1a, W-2a: address in the url field; no span, so no stored record

Nothing here read a web source.  The repo spans were stored from this session's local object
store and verified by a fetch of the same commit from the repository's remote into a fresh
repository (verification_store.json names the method).
"""
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import chains_a4 as C          # noqa: E402
import repairs_a31 as R        # noqa: E402
import sourcing_a62 as P       # noqa: E402
import standing_a61 as S61     # noqa: E402

EXPECTED_COMMIT_A63 = "ea0d379"
ORDER_FILE = "WORK_ORDER_A6.3_2026-09-30_verification-split.md"
REPO_STORE = os.path.join(HERE, "repo_span_store.json")
VERIFY_STORE = os.path.join(HERE, "verification_store.json")
CLONE_URL = "https://github.com/JinnZ2/Simulators"
REPO_PREFIX = "route-independence/"

# input states (item 2) and row states
CONSTRUCTED = P.CONSTRUCTED
NO_SPAN = "NO_SPAN"
INCONSISTENT = "INCONSISTENT"
STORED_UNVERIFIED = "STORED_UNVERIFIED"
VERIFIED = "VERIFIED"
VERIFICATION_MISMATCH = "VERIFICATION_MISMATCH"
WORKTREE_DRIFT = "WORKTREE_DRIFT"
INPUT_STATES = (VERIFIED, STORED_UNVERIFIED, NO_SPAN, CONSTRUCTED, INCONSISTENT, VERIFICATION_MISMATCH,
                WORKTREE_DRIFT)
MATCH = "MATCH"
UNVERIFIED_PASS = "UNVERIFIED_PASS"
VERIFICATION_FAILED = "VERIFICATION_FAILED"
UNSOURCED_PASS = P.UNSOURCED_PASS
CONSTRUCTED_PASS = P.CONSTRUCTED_PASS
UNFALSIFIABLE_AS_RUN = P.UNFALSIFIABLE_AS_RUN

REMOTE_FETCH, LOCAL_CHECKOUT, LOCAL_OBJECT_STORE = "REMOTE_FETCH", "LOCAL_CHECKOUT", "LOCAL_OBJECT_STORE"
COUNT, LABEL, YEAR = "COUNT", "LABEL", "YEAR"
YEAR_SHAPED = "YEAR_SHAPED"
WORD, BRACKET, ATTACHED = "WORD", "BRACKET", "ATTACHED"

CHOICES = {
    95: "repo location form (item 1): url 'repo:<40-hex commit>:<path from the repository root>' plus clone_url, "
        "an http(s) url of the repository remote; both are required, a short commit is refused because a remote "
        "fetch needs the full id; repo spans live in repo_span_store.json, so A-6.2's span_store.json and its "
        "render do not move when a repo span is stored",
    96: "consistency (item 2): a stored record is on file iff its location is an http(s) url or the [CHOICE 95] "
        "repo form, retrieval_date is an ISO date, span is non-empty and sha256 equals sha256(span utf-8); a record "
        "on file that fails any of the four reads INCONSISTENT, never STORED_UNVERIFIED",
    97: "verification (item 2): VERIFIED iff a verification record for the same source id and location carries "
        "hash_obtained equal to the stored sha256 and a method other than the one that stored the span; a record "
        "whose hash differs reads VERIFICATION_MISMATCH; no record reads STORED_UNVERIFIED; an http(s) location is "
        "not fetched here (egress allowlist) and so never leaves STORED_UNVERIFIED",
    98: "an IN_REPO input whose working-tree bytes differ from the stored span reads WORKTREE_DRIFT, since the row "
        "was computed from the working tree and the verified span would not be the bytes it read",
    99: "the A-6.3 gate over a raw MATCH: not enumerated or one aggregate case -> UNFALSIFIABLE_AS_RUN; any "
        "CONSTRUCTED input -> CONSTRUCTED_PASS (stays first, item 1); no input, or any NO_SPAN / INCONSISTENT -> "
        "UNSOURCED_PASS; any VERIFICATION_MISMATCH / WORKTREE_DRIFT -> VERIFICATION_FAILED; any STORED_UNVERIFIED "
        "-> UNVERIFIED_PASS; MATCH only when every input is VERIFIED; it replaces [CHOICE 87]",
    100: "verification method for a repo span: a fresh empty repository fetches the full commit id --depth 1 from "
         "the repository's configured remote, checks the path out and hashes the bytes read from the checkout "
         "(REMOTE_FETCH); if the fetch fails, a git worktree at the commit is used and recorded as LOCAL_CHECKOUT; "
         "the remote's address is not written to any record, clone_url names the repository",
    101: "year heuristic (item 4), replacing [CHOICE 30] here only: a 4-digit number in 1000..2999 is YEAR_SHAPED; "
         "it is a YEAR (not credited) iff the preceding word is a month name, 'in', 'since' or 'by', or it sits in "
         "a range ('-', en or em dash, or 'to') with another year-shaped number; otherwise it is a COUNT carrying "
         "the YEAR_SHAPED flag",
    102: "labels (item 5): a number whose preceding word is a WORD identifier in LABEL_IDENTIFIERS (case "
         "insensitive, a leading '[' stripped) is a LABEL and is never credited; ATTACHED identifiers (A-, RIN_, "
         "P-, E-A, CE-, FWO-) are already outside the count pattern (R._DIGITS refuses a digit after '-', '_' or "
         "a letter); 'section' and 'row' are carried from [CHOICE 30] and marked so",
    103: "alias map (item 6): an id or id range whose prefix is a key of ID_ALIASES reads as its declared noun "
         "before [CHOICE 90] agreement; an undeclared prefix is left as written and its row stays a FLAG",
    104: "mutation test (item 7): every gate in MUTATION_GATES is run over its declared input grid; for each "
         "argument, pairs differing in that argument only are counted and the ones whose output differs; a gate "
         "whose output is one value over the whole grid FAILs; an argument no single flip ever moves is reported "
         "DEAD, the gate not failed for it",
    105: "counts line: over the re-gated rows, each (row, input) reference is counted once in its input state, and "
         "each distinct source id once; both are printed with their unit",
}


class VerificationError(ValueError):
    pass


# ------------------------------------------------------------ 1: location ---

_REPO = re.compile(r"^repo:([0-9a-f]{40}):(\S+)$")


def location_form(url):
    if not isinstance(url, str) or not url:
        return "NONE"
    if P._URL.match(url):
        return "HTTP"
    if _REPO.match(url):
        return "REPO"
    if url.startswith("repo:"):
        return "REPO_MALFORMED"
    return "NO_SCHEME"


def consistent(rec):
    """[CHOICE 96] four fields plus, for the repo form, a clone url."""
    missing = []
    form = location_form(rec.get("url"))
    if form == "REPO":
        if not (isinstance(rec.get("clone_url"), str) and P._URL.match(rec["clone_url"])):
            missing.append("clone_url")
    elif form != "HTTP":
        missing.append("url")
    if not (isinstance(rec.get("retrieval_date"), str) and P._DATE.match(rec["retrieval_date"])):
        missing.append("retrieval_date")
    span = rec.get("span")
    span_ok = isinstance(span, str) and span.strip() != ""
    if not span_ok:
        missing.append("span")
    if not (span_ok and rec.get("sha256") == P.sha256_of(span)):
        missing.append("sha256")
    return {"ok": not missing, "missing": missing, "form": form}


def _load(path, key="records"):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)[key]


def _git(args, cwd=HERE):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)


def repo_record_a63(path, date=None):
    """[CHOICE 95] one repo span from the local object store, full commit id, clone url."""
    full = _git(["log", "-n", "1", "--format=%H", "--", path]).stdout.strip()
    if not re.match(r"^[0-9a-f]{40}$", full):
        raise VerificationError("%s has no commit" % path)
    body = _git(["show", "%s:./%s" % (full, path)]).stdout
    return {"source_id": path, "kind": P.IN_REPO, "url": "repo:%s:%s%s" % (full, REPO_PREFIX, path),
            "clone_url": CLONE_URL, "retrieval_date": date or datetime.date.today().isoformat(), "span": body,
            "sha256": P.sha256_of(body), "stored_by": LOCAL_OBJECT_STORE}


def store_repo(paths, store_path=REPO_STORE, date=None):
    recs = _load(store_path)
    have = set((r["source_id"], r["url"]) for r in recs)
    for p in paths:
        r = repo_record_a63(p, date)
        if (r["source_id"], r["url"]) not in have:
            recs.append(r)
    with open(store_path, "w", encoding="utf-8") as fh:
        json.dump({"note": "A-6.3 repo spans [CHOICE 95]; append-only", "records": recs}, fh, indent=1)
        fh.write("\n")
    return recs


# ---------------------------------------------------------- 2: verifying ---

def _fetch_bytes(commit, repo_path, method=REMOTE_FETCH):
    """[CHOICE 100]"""
    d = tempfile.mkdtemp()
    try:
        if method == REMOTE_FETCH:
            remote = _git(["remote", "get-url", "origin"]).stdout.strip()
            ok = (_git(["init", "-q"], d).returncode == 0 and _git(["remote", "add", "origin", remote], d).returncode == 0
                  and _git(["fetch", "-q", "--depth", "1", "origin", commit], d).returncode == 0
                  and _git(["checkout", "-q", "FETCH_HEAD", "--", repo_path], d).returncode == 0)
            if not ok:
                return None
            with open(os.path.join(d, repo_path), "rb") as fh:
                return fh.read()
        wt = os.path.join(d, "wt")
        if _git(["worktree", "add", "-q", "--detach", wt, commit]).returncode != 0:
            return None
        try:
            with open(os.path.join(wt, repo_path), "rb") as fh:
                return fh.read()
        finally:
            _git(["worktree", "remove", "--force", wt])
    finally:
        shutil.rmtree(d, ignore_errors=True)


def verify(rec, method=REMOTE_FETCH, date=None):
    """Item 2: an independent retrieval of the stored location.  Web locations are not fetched."""
    m = _REPO.match(rec.get("url") or "")
    if m is None:
        return None
    data = _fetch_bytes(m.group(1), m.group(2), method)
    if data is None and method == REMOTE_FETCH:
        method = LOCAL_CHECKOUT
        data = _fetch_bytes(m.group(1), m.group(2), method)
    if data is None:
        return None
    fetched_by = {REMOTE_FETCH: "git fetch --depth 1 of the commit from the repository remote into a fresh "
                                "repository, checkout, bytes read from the checkout (this session)",
                  LOCAL_CHECKOUT: "git worktree at the commit, bytes read from the checkout (this session)"}[method]
    got = hashlib.sha256(data).hexdigest()
    return {"source_id": rec["source_id"], "location": rec["url"], "method": method, "fetched_by": fetched_by,
            "date": date or datetime.date.today().isoformat(), "hash_obtained": got,
            "matches_stored": got == rec["sha256"]}


def record_verifications(recs, vstore_path=VERIFY_STORE, method=REMOTE_FETCH, date=None):
    out = _load(vstore_path)
    for r in recs:
        v = verify(r, method, date)
        if v is not None:
            out.append(v)
    with open(vstore_path, "w", encoding="utf-8") as fh:
        json.dump({"note": "A-6.3 verification records [CHOICE 97] [CHOICE 100]; append-only", "records": out},
                  fh, indent=1)
        fh.write("\n")
    return out


def _latest(recs, source_id):
    hits = [r for r in recs if r.get("source_id") == source_id]
    return sorted(hits, key=lambda r: r.get("retrieval_date") or "")[-1] if hits else None


def input_status(source_id, kind, stores=None, vrecs=None):
    """Item 2: one input's state.  stores = records on file (both span stores), vrecs = verifications."""
    if kind == CONSTRUCTED:
        return {"source_id": source_id, "kind": kind, "status": CONSTRUCTED, "form": None, "missing": []}
    stores = (P.load_store() + _load(REPO_STORE)) if stores is None else stores
    vrecs = _load(VERIFY_STORE) if vrecs is None else vrecs
    rec = _latest(stores, source_id)
    carried = P._carried_table().get(source_id, {}) if kind == P.CARRIED else {}
    if rec is None:
        return {"source_id": source_id, "kind": kind, "status": NO_SPAN, "missing": ["span", "sha256"],
                "form": location_form(carried.get("url")), "url": carried.get("url")}
    c = consistent(rec)
    base = {"source_id": source_id, "kind": kind, "form": c["form"], "missing": c["missing"], "url": rec.get("url")}
    if not c["ok"]:
        return dict(base, status=INCONSISTENT)
    if kind == P.IN_REPO:   # [CHOICE 98]
        live = os.path.join(HERE, source_id)
        if not os.path.exists(live) or hashlib.sha256(open(live, "rb").read()).hexdigest() != rec["sha256"]:
            return dict(base, status=WORKTREE_DRIFT)
    mine = [v for v in vrecs if v.get("source_id") == source_id and v.get("location") == rec.get("url")
            and v.get("method") != rec.get("stored_by")]
    if any(v.get("hash_obtained") == rec["sha256"] for v in mine):
        v = [v for v in mine if v.get("hash_obtained") == rec["sha256"]][-1]
        return dict(base, status=VERIFIED, verification=v)
    if mine:
        return dict(base, status=VERIFICATION_MISMATCH, verification=mine[-1])
    return dict(base, status=STORED_UNVERIFIED)


def gate_core(raw, statuses, enumerated=True, single_aggregate=False):
    """[CHOICE 99] only VERIFIED inputs let a row read MATCH."""
    if raw != MATCH:
        return raw
    if not enumerated or single_aggregate:
        return UNFALSIFIABLE_AS_RUN
    if CONSTRUCTED in statuses:
        return CONSTRUCTED_PASS
    if not statuses or any(s in (NO_SPAN, INCONSISTENT) for s in statuses):
        return UNSOURCED_PASS
    if any(s in (VERIFICATION_MISMATCH, WORKTREE_DRIFT) for s in statuses):
        return VERIFICATION_FAILED
    if STORED_UNVERIFIED in statuses:
        return UNVERIFIED_PASS
    return MATCH


def gate_a63(raw, inputs, enumerated=True, single_aggregate=False, stores=None, vrecs=None):
    return gate_core(raw, [input_status(s, k, stores, vrecs)["status"] for s, k in inputs], enumerated,
                     single_aggregate)


def rerun_a63(stores=None, vrecs=None):
    """Items 1 and 2: every row A-6.2 re-gated, read again under the split."""
    rows = []
    for r in P.rerun():
        agg = P.AGGREGATE_READING[r["row"]][0]
        st = [input_status(s, k, stores, vrecs) for s, k in r["inputs"]]
        rows.append({"row": r["row"], "module": r["module"], "raw": r["raw"], "a62": r["new"],
                     "a62_repo_address": r["repo_address"], "new": gate_core(r["raw"], [s["status"] for s in st],
                                                                            True, agg),
                     "inputs": r["inputs"], "sources": st})
    return rows


def counts(rows):
    """[CHOICE 105]"""
    refs = dict((s, 0) for s in INPUT_STATES)
    distinct = {}
    for r in rows:
        for s in r["sources"]:
            refs[s["status"]] += 1
            distinct[s["source_id"]] = s["status"]
    uniq = dict((s, 0) for s in INPUT_STATES)
    for v in distinct.values():
        uniq[v] += 1
    return {"references": refs, "distinct": uniq, "n_rows": len(rows), "n_refs": sum(refs.values()),
            "n_sources": len(distinct)}


def match_on_unverified(rows):
    return [r["row"] for r in rows if r["new"] == MATCH and any(s["status"] != VERIFIED for s in r["sources"])]


def placeholder_fixture(date="2026-09-30"):
    """RIN_150's placeholder: a constructed span at the declared LII url.  A-6.2 read MATCH on it."""
    span = "CONSTRUCTED TEST SPAN, not the regulation"
    rec = {"source_id": P.LII_ID, "url": P.LII_URL, "retrieval_date": date, "span": span,
           "sha256": P.sha256_of(span)}
    a62 = P.gate_a62("MATCH", [(P.LII_ID, P.CARRIED)], True, False, [rec])
    st = input_status(P.LII_ID, P.CARRIED, [rec], [])
    return {"a62": a62, "status": st["status"], "a63": gate_core("MATCH", [st["status"]]),
            "verify": verify(dict(rec, source_id=P.LII_ID))}


def fail_fixture():
    f = placeholder_fixture()
    return {"a62": f["a62"], "a63": f["a63"], "fires": f["a62"] == MATCH and f["a63"] != MATCH}


# ------------------------------------------------------------- 4 and 5: lint ---

MONTHS = ("january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
          "november", "december", "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov", "dec")
DATE_WORDS = ("in", "since", "by")
LABEL_IDENTIFIERS = (   # [CHOICE 102] identifier, form, source -- one line per identifier
    ("rule", WORD, "A-6.3 item 5"),
    ("item", WORD, "A-6.3 item 5"),
    ("step", WORD, "A-6.3 item 5"),
    ("CHOICE", BRACKET, "A-6.3 item 5"),
    ("A-", ATTACHED, "A-6.3 item 5"),
    ("RIN_", ATTACHED, "A-6.3 item 5"),
    ("P-", ATTACHED, "A-6.3 item 5"),
    ("E-A", ATTACHED, "A-6.3 item 5"),
    ("CE-", ATTACHED, "A-6.3 item 5"),
    ("FWO-", ATTACHED, "A-6.3 item 5"),
    ("section", WORD, "carried from [CHOICE 30]"),
    ("row", WORD, "carried from [CHOICE 30]"),
)
_WORD_IDS = tuple(i.lower() for i, f, _ in LABEL_IDENTIFIERS if f in (WORD, BRACKET))
_RANGE_AFTER = re.compile(r"^\s*(?:-|\u2013|\u2014|to)\s*[12]\d{3}\b")
_RANGE_BEFORE = re.compile(r"\b[12]\d{3}\s*(?:-|\u2013|\u2014|to)\s*$")


def _prev_word(text, pos):
    before = text[:pos].split()
    return before[-1].lower().lstrip("([\"'").rstrip(",:\"'") if before else ""


def classify_number(text, start, tok):
    """[CHOICE 101] [CHOICE 102] -> (kind, flag)"""
    prev = _prev_word(text, start)
    if prev in _WORD_IDS:
        return LABEL, None
    if tok.isdigit() and len(tok) == 4 and 1000 <= int(tok) <= 2999:
        after, before = text[start + len(tok):], text[:start]
        if prev in MONTHS or prev in DATE_WORDS or _RANGE_AFTER.match(after) or _RANGE_BEFORE.search(before):
            return YEAR, YEAR_SHAPED
        return COUNT, YEAR_SHAPED
    return COUNT, None


def count_tokens_a63(text):
    """The A-3.1 count tokens with items 4 and 5: every number classified, only COUNTs carry a unit."""
    found = [(m.start(1), m.group(1)) for m in R._DIGITS.finditer(text)]
    found += [(m.start(), m.group(1)) for m in R._WORDS.finditer(text)]
    found.sort()
    counted, dropped = [], []
    for pos, tok in found:
        kind, flag = classify_number(text, pos, tok)
        if kind != COUNT:
            dropped.append({"token": tok, "kind": kind, "flag": flag, "pos": pos, "context": text[pos:pos + 40]})
            continue
        rest = text[pos + len(tok):]
        window = [w for w in R._TOKEN.findall(rest)[:6] if w.lower() != "of" and not w.isdigit()
                  and w.lower() not in R.NUMBER_WORDS][:3]
        if any(w.lower() in R.UNITS for w in window):
            st, unit = R.OK, [w for w in window if w.lower() in R.UNITS][0]
        elif window:
            st, unit = R.UNIT_OUTSIDE_LIST, window[0]
        else:
            st, unit = R.NO_UNIT, None
        counted.append({"token": tok, "status": st, "unit": unit, "context": text[pos:pos + 40], "kind": COUNT,
                        "flag": flag, "pos": pos})
    return {"counted": counted, "dropped": dropped}


def attach_a63(text, aliases=None):
    """[CHOICE 78] nearest ownership and [CHOICE 90] agreement over the item 4/5 tokens, aliases per item 6."""
    aliases = ID_ALIASES if aliases is None else aliases
    toks = count_tokens_a63(text)["counted"]
    owner, flags = {}, []
    for m in P._ANN.finditer(text):
        unit = m.group(1).strip().lower()
        prev = [i for i, t in enumerate(toks) if t["pos"] + len(t["token"]) <= m.start()
                and m.start() - (t["pos"] + len(t["token"])) <= 80]
        if not prev:
            continue
        near = prev[-1]
        sig = P.agreement(dealias(text[toks[near]["pos"] + len(toks[near]["token"]):m.start()], aliases), unit)
        if sig in ("AGREE", "NO_NOUN"):
            owner[near] = unit
        else:
            flags.append({"unit": unit, "nearest": toks[near]["token"], "nearest_pos": toks[near]["pos"],
                          "context": text[toks[near]["pos"]:m.end()]})
    ann = [dict(t, owns=owner.get(i), annotated=(t["status"] == R.OK or i in owner)) for i, t in enumerate(toks)]
    return {"tokens": ann, "flags": flags,
            "identities": [(t["pos"], t["token"], (t["owns"] or t["unit"]).lower()) for t in ann if t["annotated"]]}


# ------------------------------------------------------------ 6: aliases ---

ID_ALIASES = (   # [CHOICE 103] prefix -> noun, one line per prefix; nothing inferred
    ("P-", "profiles"),
)


def dealias(between, aliases=None):
    aliases = ID_ALIASES if aliases is None else aliases
    for prefix, noun in aliases:
        pat = re.compile(r"(?<![A-Za-z0-9])%s\d+(?:\s*\.\.\s*%s\d+)?" % (re.escape(prefix), re.escape(prefix)))
        between = pat.sub(" %s " % noun, between)
    return between


def pins_a63(fname, aliases=None):
    text = C.expected_block(fname)
    a62 = P.pins(fname)
    new = attach_a63(text, aliases)
    dropped = count_tokens_a63(text)["dropped"]
    return {"file": fname, "a62_agree": a62["agree"], "a63": new["identities"], "flags": new["flags"],
            "a62_flags": a62["flags"], "dropped": dropped,
            "moved": (sorted(set(a62["agree"]) - set(new["identities"])),
                      sorted(set(new["identities"]) - set(a62["agree"])))}


LINT_FIXTURES = (   # item 4 and item 5 fixtures, as the order words them
    ("2036 paths", "2036", COUNT, True),
    ("since 1971", "1971", YEAR, False),
    ("rule 0 these rows", "0", LABEL, False),
)


def lint_fixture(text, token):
    r = count_tokens_a63(text)
    hit = [t for t in r["counted"] if t["token"] == token]
    drop = [t for t in r["dropped"] if t["token"] == token]
    return {"kind": hit[0]["kind"] if hit else (drop[0]["kind"] if drop else None), "credited": bool(hit),
            "flag": (hit or drop or [{}])[0].get("flag"),
            "a31_credited": any(t["token"] == token for t in R.count_tokens(text))}


def order_lint():
    text = open(os.path.join(HERE, ORDER_FILE), encoding="utf-8").read()
    a31 = R.count_tokens(text)
    new = count_tokens_a63(text)
    return {"a31": len(a31), "a31_ok": [t["context"][:16] for t in a31 if t["status"] == R.OK],
            "a63_counted": len(new["counted"]), "a63_ok": [t["context"][:16] for t in new["counted"] if t["status"] == R.OK],
            "labels": len([t for t in new["dropped"] if t["kind"] == LABEL]),
            "years": [t["token"] for t in new["dropped"] if t["kind"] == YEAR],
            "year_shaped_counted": [t["token"] for t in new["counted"] if t["flag"] == YEAR_SHAPED]}


# ------------------------------------------------------------ 7: mutation ---

_G_RAW = (MATCH, "UNMET_UNFALSIFIED", P.NOT_EVALUABLE)
_G_BOOL = (True, False)


def _grid_gate_core():
    stat = ((), (VERIFIED,), (STORED_UNVERIFIED,), (NO_SPAN,), (CONSTRUCTED,), (VERIFICATION_MISMATCH,),
            (VERIFIED, STORED_UNVERIFIED))
    return ("raw", _G_RAW), ("statuses", stat), ("enumerated", _G_BOOL), ("single_aggregate", _G_BOOL)


def _grid_gate_status():
    return ("raw", _G_RAW), ("input_grades", (("S",), ("K",), ("P",), (P.NOT_RECORDED,))), \
           ("falsifier_cases_enumerated", _G_BOOL)


_MUT_SPAN = "mutation span"
_MUT_STORE = [{"source_id": "X", "url": "https://example.org/x", "retrieval_date": "2026-09-30",
               "span": _MUT_SPAN, "sha256": P.sha256_of(_MUT_SPAN)}]


def _grid_gate_a62():
    return (("raw", _G_RAW), ("inputs", ((), (("X", P.CARRIED),), (("X", CONSTRUCTED),), (("Y", P.CARRIED),),
                                         (("gate_state.py", P.IN_REPO),))),
            ("enumerated", _G_BOOL), ("single_aggregate", _G_BOOL), ("store", (_MUT_STORE, [])),
            ("reading", (P.URL_RULE, P.REPO_ADDRESS)))


def _grid_consistent():
    good = {"url": "https://example.org/x", "retrieval_date": "2026-09-30", "span": "s", "sha256": P.sha256_of("s")}
    return (("rec", (good, dict(good, url="example.org/x"), dict(good, sha256="0" * 64), dict(good, span=""))),)


def _grid_input_status():
    rec = dict(_MUT_STORE[0])
    v_ok = {"source_id": "X", "location": rec["url"], "method": REMOTE_FETCH, "hash_obtained": rec["sha256"]}
    v_bad = dict(v_ok, hash_obtained="0" * 64)
    v_same = dict(v_ok, method=None)
    return (("source_id", ("X", "Y")), ("kind", (P.CARRIED, CONSTRUCTED)), ("stores", (_MUT_STORE, [])),
            ("vrecs", ([], [v_ok], [v_bad], [v_same])))


MUTATION_GATES = (   # [CHOICE 104] every status gate this module defines or reads, with its grid
    ("verification_a63.gate_core", lambda: gate_core, _grid_gate_core),
    ("verification_a63.input_status", lambda: input_status, _grid_input_status),
    ("verification_a63.consistent", lambda: (lambda rec: consistent(rec)["ok"]), _grid_consistent),
    ("sourcing_a62.gate_a62", lambda: P.gate_a62, _grid_gate_a62),
    ("standing_a61.gate_status", lambda: S61.gate_status, _grid_gate_status),
)
NOT_MUTATED = (   # functions with 'gate' or 'status' in the name, read here, not status gates
    ("verification_a63.gate_a63", "gate_core over input_status; both are in the list"),
    ("sourcing_a62.source_status", "a record, no single status; its status field is rule0, read by gate_a62"),
    ("sourcing_a62.erratum_sweep_ran_aggregate_condition", "reads a caller's source for a constant; not a gate"),
    ("verification_a63.gate_functions_named", "this list's own coverage check"),
)


def _cells(grid):
    import itertools
    names = [n for n, _ in grid]
    for combo in itertools.product(*[range(len(v)) for _, v in grid]):
        yield names, combo


def mutation(fn, grid):
    """[CHOICE 104]"""
    import itertools
    names = [n for n, _ in grid]
    vals = [v for _, v in grid]

    def call(idx):
        out = fn(**dict((names[i], vals[i][j]) for i, j in enumerate(idx)))
        return out["status"] if isinstance(out, dict) else out
    table = dict((idx, call(idx)) for idx in itertools.product(*[range(len(v)) for v in vals]))
    per_arg = {}
    for a, name in enumerate(names):
        pairs = moved = 0
        for idx, out in table.items():
            for j in range(len(vals[a])):
                if j <= idx[a]:
                    continue
                other = idx[:a] + (j,) + idx[a + 1:]
                pairs += 1
                moved += table[other] != out
        per_arg[name] = {"pairs": pairs, "moved": moved, "dead": moved == 0}
    outs = set(table.values())
    return {"cells": len(table), "outputs": sorted(outs, key=str), "constant": len(outs) == 1,
            "per_arg": per_arg, "verdict": "FAIL" if len(outs) == 1 else "PASS"}


def mutation_all(gates=None):
    return [dict(mutation(get(), grid()), gate=name) for name, get, grid in (gates or MUTATION_GATES)]


CONSTANT_GATE_FIXTURE = ("constant_gate", lambda: (lambda raw, statuses: MATCH),
                         lambda: (("raw", _G_RAW), ("statuses", ((), (VERIFIED,)))))


def gate_functions_named():
    """Every function with 'gate' or 'status' in its name in this module and the two it reads."""
    import ast
    out = []
    for mod, fname in (("verification_a63", __file__), ("sourcing_a62", P.__file__), ("standing_a61", S61.__file__)):
        tree = ast.parse(open(fname, encoding="utf-8").read())
        out += ["%s.%s" % (mod, n.name) for n in tree.body if isinstance(n, ast.FunctionDef)
                and not n.name.startswith("_") and ("gate" in n.name or "status" in n.name)]
    return out


# --------------------------------------------------------------- render ---

def render(out=None):
    out = sys.stdout if out is None else out
    wr = out.write
    rows = rerun_a63()
    cn = counts(rows)
    wr("A-6.3 verification split (work order landed verbatim at %s; web sources CARRIED, not read here)\n\n"
       % EXPECTED_COMMIT_A63)
    wr("0  Part B status: see README 'Work order standing/A-6.3' and RIN_151 (not computed here)\n\n")
    wr("what did not hold\n")
    wr("   item 8: W-1a, W-2a carry a url now and no span, so they read %s, not %s as item 8 words it\n"
       % (input_status("W-1a", P.CARRIED)["status"], STORED_UNVERIFIED))
    wr("   item 8: the moved url field carries no scheme: W-1a %s, W-2a %s (the scheme is left to the operator)\n"
       % (input_status("W-1a", P.CARRIED)["form"], input_status("W-2a", P.CARRIED)["form"]))
    fx = placeholder_fixture()
    wr("   RIN_150 placeholder: A-6.2 gate %s, A-6.3 input %s, gate %s (the fail fixture)\n\n"
       % (fx["a62"], fx["status"], fx["a63"]))
    wr("1-2  rows re-gated (A-6.2 gate -> A-6.3 gate) [CHOICE 99]\n")
    for r in rows:
        wr("   %-28s raw %-6s a62 %-22s -> %-22s\n" % (r["row"], r["raw"], r["a62"], r["new"]))
        for s in r["sources"]:
            if s["kind"] != CONSTRUCTED:
                v = s.get("verification")
                wr("      %-50s %-9s %-18s form %-9s%s\n"
                   % (s["source_id"][:50], s["kind"], s["status"], s["form"],
                      " via %s %s" % (v["method"], v["date"]) if v else ""))
    wr("   counts, references (unit: row inputs, n %d over %d rows): %s\n"
       % (cn["n_refs"], cn["n_rows"], " / ".join("%s %d" % (k, cn["references"][k]) for k in INPUT_STATES)))
    wr("   counts, distinct sources (unit: sources, n %d): %s\n"
       % (cn["n_sources"], " / ".join("%s %d" % (k, cn["distinct"][k]) for k in INPUT_STATES)))
    wr("   rows reading MATCH: %s; MATCH on a non-VERIFIED input: %s\n\n"
       % ([r["row"] for r in rows if r["new"] == MATCH], match_on_unverified(rows) or "none"))
    note = S61.SOURCES_A61["CE-4e"].get("status_note", "")
    wr("3  CE-4e status note on file (standing_a61.SOURCES_A61, %d chars): coding rule GEOGRAPHIC %s; origin "
       "the chat handover (Claude) %s\n\n" % (len(note), "coding rule = GEOGRAPHIC" in note,
                                             "chat handover (Claude)" in note))
    wr("4-5  lint fixtures [CHOICE 101] [CHOICE 102]\n")
    for text, tok, kind, credited in LINT_FIXTURES:
        f = lint_fixture(text, tok)
        wr("   %-20s token %-5s A-3.1 credited %-5s -> kind %-6s credited %-5s flag %s\n"
           % (repr(text), tok, f["a31_credited"], f["kind"], f["credited"], f["flag"]))
    ol = order_lint()
    wr("   this order: A-3.1 %d tokens, OK %s; A-6.3 %d counted, OK %s, %d labels, years %s, year-shaped counted %s\n\n"
       % (ol["a31"], ol["a31_ok"], ol["a63_counted"], ol["a63_ok"], ol["labels"], ol["years"],
          ol["year_shaped_counted"]))
    wr("5-6  identity pins A-4..A-6.1, A-6.2 agree rule -> A-6.3 (labels, years, alias map) [CHOICE 103]\n")
    for f in P.PIN_FILES:
        p = pins_a63(f)
        wr("   %-58s %d -> %d  removed %s added %s  flags %d -> %d\n"
           % (f, len(p["a62_agree"]), len(p["a63"]), p["moved"][0], p["moved"][1], len(p["a62_flags"]),
              len(p["flags"])))
    a6 = pins_a63(P.PIN_FILES[2])
    wr("   A-6 returns to %d credited counts (A-6.1 erratum read 3; A-6.2 agreement read %d)\n\n"
       % (len(a6["a63"]), len(a6["a62_agree"])))
    wr("7  mutation over every status gate [CHOICE 104]\n")
    for m in mutation_all():
        dead = [k for k, v in m["per_arg"].items() if v["dead"]]
        wr("   %-32s %-4s cells %3d outputs %d dead args %s\n"
           % (m["gate"], m["verdict"], m["cells"], len(m["outputs"]), dead or "none"))
    cg = mutation(CONSTANT_GATE_FIXTURE[1](), CONSTANT_GATE_FIXTURE[2]())
    wr("   fixture: a gate returning one value on every input reads %s\n\n" % cg["verdict"])
    wr("execution note: test_verification_a63.py prints the check count; samples/verification_a63.sample.txt is one "
       "render, pinned\n")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("verification_a63.py carries no selftest; run python3 test_verification_a63.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    if argv[:1] == ["store-repo"]:
        paths = sorted(set(p for r in P.ROW_INPUTS for p, k in r[2] if k == P.IN_REPO))
        recs = store_repo(paths)
        print("stored %d repo spans" % len(recs))
        return 0
    if argv[:1] == ["verify-repo"]:
        v = record_verifications(_load(REPO_STORE))
        print("%d verification records" % len(v))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
