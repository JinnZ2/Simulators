"""build_packet.py: assemble a blind study-review packet for a new reader, from the files at the current commit.

  python3 build_packet.py grok 2026-11-19     -> studies/packets/grok_2026-11-19/
                                                   packet/ (the files), packet.txt (paste form), packet.zip,
                                                   MANIFEST_PRIVATE.json (not given to the reader)
  python3 build_packet.py grok 2026-11-19 --check   rebuilds in memory and fails if any output would change

The packet is the study material (M01 / M02 criteria, schemas, condition notes D0-D3), the v2 brief and terms, and the
source excerpts the studies cite, with original line numbers kept. Excluded: the keys and the amendment, the M01 coding and
reports, the arms report, studies/confusion/, PREREG, every reader response. Repository and project names, repo paths,
commit ids, reader names and two sentences that state a key list or a reading result are redacted by the explicit list
REDACT below; every replacement is counted per file in the private manifest. A leak scan fails the build if any banned
string survives. Stdlib only.
"""
import hashlib, io, json, os, re, subprocess, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(HERE))           # blind-reader-void12/
REPO = os.path.dirname(BASE)
SRC = "reader_packet_v2/sources"
P1, P2, P3 = SRC + "/Simulators/combined-playground", SRC + "/formula-audit", SRC + "/thermodynamic-accountability-framework"

# (packet name, repo path, kind, line ranges or None for the whole file)
FILES = [
    ("TASK.md", None, "task", None),
    ("brief/READER_BRIEF.md", "reader_packet_v2/READER_BRIEF.md", "text", None),
    ("brief/terms.json", "reader_packet_v2/terms.json", "terms", None),
    ("studies/M01_CRITERIA.md", "studies/M01_CRITERIA.md", "text", None),
    ("studies/M01_SCHEMA.json", "studies/M01_SCHEMA.json", "text", None),
    ("studies/M01_EXTENSION.md", "studies/M01_EXTENSION.md", "text", None),
    ("studies/M02_CRITERIA.md", "studies/M02_CRITERIA.md", "text", None),
    ("studies/M02_SCHEMA.json", "studies/M02_SCHEMA.json", "text", None),
    ("studies/conditions/D0.md", None, "d0", None),
    ("studies/conditions/M01_D1.md", "studies/instructions/M01_D1.md", "text", None),
    ("studies/conditions/M02_D1.md", "studies/instructions/M02_D1.md", "text", None),
    ("studies/conditions/M02_D2.md", "studies/instructions/M02_D2.md", "text", None),
    ("studies/conditions/M02_D3.md", "studies/instructions/M02_D3.md", "text", None),
    ("sources/P1/cplay/tokens.py", P1 + "/cplay/tokens.py", "excerpt", None),
    ("sources/P1/cplay/axes.py", P1 + "/cplay/axes.py", "excerpt", None),
    ("sources/P1/cplay/closure.py", P1 + "/cplay/closure.py", "excerpt", [(284, 336)]),
    ("sources/P1/playground-crossrun/COMBINED_SPEC.md", SRC + "/Simulators/playground-crossrun/COMBINED_SPEC.lines_1-390.md", "excerpt", [(35, 96), (122, 145)]),
    ("sources/P2/numcheck/check.py", P2 + "/numcheck/check.py", "excerpt", [(1, 53), (110, 119), (188, 240), (296, 305), (415, 440), (443, 557)]),
    ("sources/P3/calibration/unified_audit.py", P3 + "/calibration/unified_audit.py", "excerpt", [(93, 101), (209, 236), (331, 372), (479, 496)]),
    ("sources/P3/calibration/expiry_register.py", P3 + "/calibration/expiry_register.py", "excerpt", [(51, 60), (216, 235)]),
    ("sources/P3/docs/glossary.md", P3 + "/docs/glossary.md", "excerpt", [(122, 142)]),
    ("CONFUSION_REQUEST.md", None, "confusion", None),
]
# packet v2 (P1, P3): the response template is added; the spec excerpt keeps the file name terms.json points to
FILES_V2 = [f for f in FILES if f[0] != "CONFUSION_REQUEST.md"]
FILES_V2 = [(("sources/P1/playground-crossrun/COMBINED_SPEC.lines_1-390.md",) + f[1:]) if f[0].endswith("COMBINED_SPEC.md") else f for f in FILES_V2]
FILES_V2.insert(3, ("brief/response_template.json", "reader_packet_v2/response_template.json", "text", None))
FILES_V2.append(("CONFUSION_REQUEST.md", None, "confusion", None))

# Applied in order to every file. Each entry: (pattern, replacement, why).
REDACT = [
    (r"`2026-11-18_claude-v2-A`, `2026-11-19_kimi-v2-A`, `2026-11-19_gpt6-v2`", "[three reading folders, names withheld]", "reader names"),
    (r"\(all three filed readers list covers_effect\)", "([a result from the filed readings, withheld])", "a reading result"),
    (r"key v2's carried list is the coverage entry's six fields, and whether the section record also counts is open \(`KEY_V2_AMENDMENT_1\.md` section 6\.1\)",
     "[the comparison key's list for this term, withheld]; whether the section record also counts is open", "key content"),
    (r"variant A for the first two, null for GPT-6 \(not stated\)", "variants as filed", "reader names"),
    (r"`?KEY_V2_AMENDMENT_1\.md`?(,? sections? \d+(\.\d+)?(-\d+)?)?", "[an excluded file]", "excluded file"),
    (r"`?amendment_options/[^\s`)]*`?", "[an excluded file]", "excluded file"),
    (r"`?derive_specific_output\.txt`?", "[an excluded file]", "excluded file"),
    (r"`?key_v2(_a1)?\.json`?", "[an excluded file]", "excluded file"),
    (r"`?as_received/[^\s`)]*`?", "[an excluded file]", "excluded file"),
    (r"\(Manus's 12-record run\)", "(a 12-record run by another session)", "a session name"),
    (r"\bManus\b", "[another session]", "a session name"),
    (r"\bKavik\b", "[a person]", "a person's name"),
    (r"chat-side Claude", "[another session]", "a session name"),
    (r"Claude Code session", "[the coding session]", "a session name"),
    (r"the GPT-6 reader's", "a reader's", "reader names"),
    (r"the GPT-6 reader\b", "a reader", "reader names"),
    (r"(the )?\[the pre-registration file, excluded\] status note on amendment 1", "a status note in an excluded file", "excluded file"),
    (r"the drafter of a superseded amendment", "the drafter of a superseded draft", "excluded change"),
    (r"\"the amendment is proposed and not merged\"", "\"[an excluded change] is not in force\"", "excluded change"),
    (r"\bamendment 1\b", "[an excluded change]", "excluded change"),
    (r"\binstructions/", "conditions/", "packet folder name"),
    (r"\bGPT-6\b|\bgpt6\b|\bGPT\b", "[a reader]", "reader names"),
    (r"\b[Cc]laude\b", "[a reader]", "reader names"),
    (r"\b[Kk]imi audit\b", "[an external] audit", "a reader / author name"),
    (r"\b[Kk]imi\b", "[a reader]", "reader names"),
    (r"\bkey a1('s)?\b", r"the comparison key\1", "key name"),
    (r"\bkey v2('s)?\b", r"the comparison key\1", "key name"),
    (r"\"key_a1\"", "\"comparison_key\"", "key name"),
    (r"`?\bPREREG(\.md)?\b`?", "[the pre-registration file, excluded]", "excluded file"),
    (r"\b[0-9a-f]{7,64}\b", "[commit]", "commit id"),
    (r"reader_packet_v2/sources/Simulators/combined-playground", "sources/P1", "repo path"),
    (r"reader_packet_v2/sources/formula-audit", "sources/P2", "repo path"),
    (r"reader_packet_v2/sources/thermodynamic-accountability-framework", "sources/P3", "repo path"),
    (r"Simulators/combined-playground", "P1", "repo name"),
    (r"\bthermodynamic-accountability-framework\b", "P3", "repo name"),
    (r"\bformula-audit\b", "P2", "repo name"),
    (r"\bSimulators\b", "P1", "repo name"),
    (r"\bJinnZ2\b", "[owner]", "owner account"),
    (r"\bTAF\b", "P3", "project name"),
    (r"\btaf:", "p3:", "project name"),
    (r"\btaf\b", "p3", "project name"),
    (r"`?readings/[^\s`]*`?", "[readings folder]", "readings path"),
]
REDACT_V2 = [
    (r"- \*\*routes\*\*: 2 for T08 and T09 \(the two terms with disagreeing routes in \[an excluded file\]\), 1 otherwise\.",
     "- **routes**: the number of source routes to the term's instance that give different lists, set by the coder from a derivation not included here.", "P6: a value from an excluded file"),
    (r" \(2 for T08 and T09\)", "", "P6: a value from an excluded file"),
    (r"\[the comparison key's list for this term, withheld\]; whether the section record also counts is open\.", "which of the two a reader counts is what the study records.", "P6: a decision state from an excluded file"),
    (r"answer to T10's open carried question", "answer to a real term", "P6: a decision state from an excluded file"),
    (r"T09 \(the case where readers already chose different records: coverage entries vs register rows\)", "T09", "P6: a result of filed readings"),
    (r"\"\[an excluded change\] is not in force\"\s+\[an excluded change\] is in force \(\[the pre-registration file, excluded\] status note, this date\);\n\s+the file's line 3 is stale and left as written",
     "[row withheld: it concerns the status of a file not included]", "P6: a decision from an excluded file"),
    (r"\[an excluded file\]|\[a proposal file, excluded\]|\[an excluded change\]|\[the pre-registration file, excluded\]", "(not included)", "P5: pointer to a file not included"),
    (r"\[readings folder\]", "the readings folder (not included)", "P5: pointer to a folder not included"),
]
LATE = [(r"(the )?\[the pre-registration file, excluded\] status note on \[an excluded change\]", "a status note in an excluded file", "excluded file")]
BANNED = [r"\bamendment\b", r"claude", r"kimi", r"\bgpt", r"manus", r"kavik", r"simulators", r"jinnz2", r"thermodynamic", r"formula-audit",
          r"\btaf\b", r"key_v2", r"key a1", r"key_a1", r"amendment_options", r"\b[0-9a-f]{7,64}\b",
          r"readings/", r"github", r"\bgrok\b"]
ALLOW = {"CONFUSION_REQUEST.md": [r"\bgrok\b"]}     # the reader's own name, in its own Reader slot
BANNED_CASE = [r"PREREG"]     # the file name; the cplay source has a class and attribute `prereg`, which is source content

def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True, check=True).stdout.strip()

def read(rel):
    return open(os.path.join(BASE, rel), encoding="utf-8").read()

def redact(text, counts, version=1):
    for pat, rep, why in REDACT + LATE + (REDACT_V2 if version == 2 else []):
        text, n = re.subn(pat, rep, text)
        if n: counts[pat] = counts.get(pat, 0) + n
    return text

def excerpt(rel, ranges, name):
    lines = read(rel).split("\n")
    rs = ranges or [(1, len(lines) - (1 if lines[-1] == "" else 0))]
    out = ["# Excerpt of %s, original line numbers kept (lines %s of %d). Lines not shown are omitted, not empty."
           % (name.split("/", 1)[1], ", ".join("%d-%d" % r for r in rs), len(lines) - (1 if lines[-1] == "" else 0)), ""]
    for a, b in rs:
        out += ["%5d| %s" % (i, lines[i - 1]) for i in range(a, b + 1)] + ["  ...", ""]
    return "\n".join(out[:-2]) + "\n"

def terms():
    t = json.loads(read("reader_packet_v2/terms.json"))
    for x in t["terms"]:
        s = x["source"]
        x["source"] = {"path": s["served_as"], "anchor": s["anchor"]}
    return json.dumps(t, indent=1, ensure_ascii=False) + "\n"

def task(label, version=1):
    return f"""# Task

You are asked to do one reading task and return one thing.

**Setup.** Use a new conversation with no memory, no project knowledge, no connected repositories and no repository link or URL, and web search and code tools off if you can turn them off. Work only from the files below. If you use anything else, say so at the top of your answer.

**What the files are.** Two small studies, M01 and M02, are designed to measure how readers apply one reading brief. They are given here so you can read them as a reader who would have to apply them:

- `brief/READER_BRIEF.md` and `brief/terms.json`: the reading brief and its 15 terms (this is condition D0).
- `studies/`: the two studies' criteria and schemas, and `studies/conditions/`: the extra notes some readers get (D1-D3).
- `sources/`: excerpts of the source files the studies cite. Line numbers are the originals; lines not shown are omitted. P1, P2, P3 are three projects.

Some documents mention files that are not included here, or text marked as withheld. Treat those as unavailable; if you needed one, say so in your answer.
{V2_RULES if version == 2 else ""}
**Task.** Read the studies and condition notes against the brief and the source excerpts. Do not fill in the brief's response template and do not group the terms; this task is not a reading of the brief. Your answer is the confusion inventory described in `CONFUSION_REQUEST.md`: every point where you were unsure, guessed, stopped, or needed evidence not in these files.

**Label.** Write `{label}` at the top of your answer, with the model name your app shows (or "unknown AI model") and today's UTC date. Also say which tools were on, and whether memory or project knowledge was on.
"""

V2_RULES = """
**Your condition.** This task places you under no condition. You are not doing a reading of the brief; read D0, D1, D2 and D3 as material, the way a study designer would. Where a study says what a reader under a condition would do, judge whether its text lets you tell.

**Excerpt rule.** The source files are excerpts. Each starts with a header naming its line ranges; lines outside them are omitted, not empty. An answer that would need an omitted line is bounded by the excerpt, not by you: record it as a row ("needed evidence not in these files"), say which lines you would need, and do not guess their content. The response template (`brief/response_template.json`) is included so the brief's output format can be read; do not fill it in.
"""

def d0():
    return ("# Condition D0\n\nThe brief and terms in `brief/`, unchanged, with no extra note. D1, D2 and D3 are the brief plus the note "
            "of that name in this folder; a reader in a study gets exactly one condition.\n")

def confusion(reader, version=1):
    return f"""# Confusion request

Reader: {reader}      Read: <the files of this packet>

For every point where you were unsure, guessed, stopped, or needed evidence unavailable in these files, give one row:

```text
id | term or passage | what was missing | what you did (guessed / stopped / read X as Y) | file and lines | resolves with
```

- "What you did" is required: include every guess or interpretation, even if later evidence showed it was right.
- Leave a cell void when you do not know; do not omit the row.
- One row per point; do not merge separate uncertainties.
- If you find no confusion, write "none found" and list everything you read.
- Do not resolve a row by guessing what another reader would say.
- The inventory is a record of reading, not a score.
""" + (ATTEST if version == 2 else "")

# packet v2 (added 2026-11-19, owner's item 5): the reader attestation block of CONFUSION_TEMPLATE.md
ATTEST = """
Put this block at the head of your inventory. "unknown" is an answer; leave nothing blank.

```text
Reader attestation
prior exposure, before this task:
  the packet (these files, or an earlier version of them)          yes / no / unknown
  the key (any comparison key, or any score)                       yes / no / unknown
  the repository these files come from (any part)                  yes / no / unknown
  other readers' records (readings, confusion records)             yes / no / unknown
memory from other conversations                                   on / off / unknown
tools used in this task                                            <list, or "none">
```
"""

def build(reader, date, version=1):
    label = "R-%s-a" % date      # hyphens kept, so the label cannot read as a commit id
    commit = git("rev-parse", "HEAD")
    files, manifest_files, counts_all = [], [], {}
    for name, rel, kind, ranges in (FILES_V2 if version == 2 else FILES):
        counts = {}
        if kind == "task": text = task(label, version)
        elif kind == "d0": text = d0()
        elif kind == "confusion": text = confusion(reader, version)
        elif kind == "terms": text = terms()
        elif kind == "excerpt": text = excerpt(rel, ranges, name)
        else: text = read(rel)
        text = text if kind in ("task", "confusion", "d0") else redact(text, counts, version)
        files.append((name, text))
        manifest_files.append({"packet_file": name, "source": (rel and "blind-reader-void12/%s@%s" % (rel, commit)),
                               "source_sha256": rel and hashlib.sha256(open(os.path.join(BASE, rel), "rb").read()).hexdigest(),
                               "lines": ranges, "kind": kind, "redactions": counts,
                               "packet_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()})
        for k, v in counts.items(): counts_all[k] = counts_all.get(k, 0) + v
    leaks = []
    for name, text in files:
        for pat in BANNED:
            if pat in ALLOW.get(name, []): continue
            for m in re.finditer(pat, text, re.I):
                leaks.append("%s: %r near %r" % (name, m.group(0), text[max(0, m.start() - 30):m.end() + 30]))
        for pat in BANNED_CASE:
            for m in re.finditer(pat, text):
                leaks.append("%s: %r near %r" % (name, m.group(0), text[max(0, m.start() - 30):m.end() + 30]))
    paste = "\n".join("=== FILE %d === %s\n\n%s" % (i + 1, n, t) for i, (n, t) in enumerate(files))
    zbuf = io.BytesIO()
    with zipfile.ZipFile(zbuf, "w", zipfile.ZIP_DEFLATED) as z:
        for n, t in files:
            zi = zipfile.ZipInfo("packet/" + n, date_time=(2026, 1, 1, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, t.encode("utf-8"))
    manifest = {
        "private": "NOT given to the reader. Maps each packet file to its source path@commit.",
        "reader": reader, "packet_version": version, "status": "SENT" if version == 1 else "DRAFT (not sent)",
        "reader_label_in_packet": label, "built_at_commit": commit, "date_utc": date,
        "condition": {
            "blind_to": ["the comparison key's lists and derivation (keys and amendment excluded)", "the M01 coding and reports",
                         "the arms report", "every confusion record", "the pre-registration file", "every reader response",
                         "reader names, repository and project names, commit ids"],
            "not_blind_to": ["the study designs (M01 / M02 criteria, schemas, extension)",
                             "the condition notes D1-D3, including M01_D1, which states the comparison key's own slot rule "
                             "(TAG and INDEPENDENCE): after this packet the reader is not a fresh D0 reader of the v2 brief"],
            "prior_exposure": None, "channel": None, "observer": None,
            "note": "prior_exposure, channel (paste or zip) and observer are null until filled from the reader's answer and the owner's record"},
        "files": manifest_files, "redaction_counts_total": counts_all,
        "redaction_rules": [{"pattern": p, "replacement": r, "why": w} for p, r, w in REDACT + LATE + (REDACT_V2 if version == 2 else [])],
        "leak_scan": {"banned_patterns_case_insensitive": BANNED, "banned_case_sensitive": BANNED_CASE, "allowed": ALLOW, "hits": leaks},
        "sizes": {"packet_txt_chars": len(paste), "packet_txt_bytes": len(paste.encode("utf-8")), "zip_bytes": len(zbuf.getvalue())},
    }
    return files, paste, zbuf.getvalue(), manifest, leaks

def main():
    reader, date = sys.argv[1], sys.argv[2]
    version = 2 if "--v2" in sys.argv else 1
    files, paste, zbytes, manifest, leaks = build(reader.capitalize(), date, version)
    out = os.path.join(HERE, "%s_%s%s" % (reader.lower(), date, "_v2" if version == 2 else ""))
    if version == 2:
        import difflib
        v1dir = os.path.join(HERE, "%s_%s" % (reader.lower(), date), "packet")
        v1 = {os.path.relpath(os.path.join(d, f), v1dir): open(os.path.join(d, f), encoding="utf-8").read()
              for d, _, fs in os.walk(v1dir) for f in fs}
        v2 = dict(files); diff, rows = [], []
        for n in sorted(set(v1) | set(v2)):
            a, b = v1.get(n), v2.get(n)
            rows.append({"file": n, "v1": a and hashlib.sha256(a.encode()).hexdigest(), "v2": b and hashlib.sha256(b.encode()).hexdigest(),
                         "change": "added" if a is None else "removed" if b is None else "same" if a == b else "changed"})
            if a != b:
                diff += difflib.unified_diff((a or "").splitlines(True), (b or "").splitlines(True), "v1/" + n, "v2/" + n)
        manifest["diff_from_v1"] = {"files": rows, "diff_file": "v1_to_v2.diff",
                                    "fixes": {"P1": "response template added", "P2": "condition stated in TASK.md (none: a review task)",
                                              "P3": "spec excerpt named as terms.json points to it", "P4": "excerpt rule stated in TASK.md",
                                              "P5": "pointers to files not included neutralized", "P6": "six answer-bearing sentences neutralized"},
                                    "added": {"2026-11-19": "reader attestation block in CONFUSION_REQUEST.md (owner's item 5; not a v1 defect)"},
                                    "send_constraint": "not to be sent into the conversation that produced R-2026-11-19-a: that reader has since read the repository (grok_2026-11-19/SENT_RECORD.json, later_2026-11-19)"}
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "v1_to_v2.diff"), "w", encoding="utf-8").writelines(diff)
    if leaks:
        print("LEAK SCAN FAILED:"); print("\n".join("  " + l for l in leaks)); sys.exit(1)
    if "--check" in sys.argv:
        old = json.load(open(os.path.join(out, "MANIFEST_PRIVATE.json"), encoding="utf-8"))
        same = [f["packet_sha256"] for f in old["files"]] == [f["packet_sha256"] for f in manifest["files"]]
        print("build --check: " + ("identical packet" if same else "PACKET WOULD CHANGE")); sys.exit(0 if same else 1)
    for n, t in files:
        p = os.path.join(out, "packet", n); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(t)
    open(os.path.join(out, "packet.txt"), "w", encoding="utf-8").write(paste)
    open(os.path.join(out, "packet.zip"), "wb").write(zbytes)
    manifest["sizes"]["fits_100k_chars"] = manifest["sizes"]["packet_txt_chars"] <= 100000
    json.dump(manifest, open(os.path.join(out, "MANIFEST_PRIVATE.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(manifest["sizes"]), "files:", len(files), "redactions:", sum(manifest["redaction_counts_total"].values()), "leaks: 0")

if __name__ == "__main__":
    main()
