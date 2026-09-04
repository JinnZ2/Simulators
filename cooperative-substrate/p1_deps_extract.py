#!/usr/bin/env python3
"""P1 -- dependency records. Reads plaintext methods sections, one file
per result, and emits one JSONL line per dependency the pattern set
catches. `verified_in_argument` is False unless the same sentence
carries an explicit verification verb.

    python3 p1_deps_extract.py --in methods/ --out deps.jsonl [--report]

Extraction is lexical: a dependency stated in vocabulary the pattern set
does not carry is not extracted, so every count here is a floor set by
the pattern set, never a count of what the text rests on. Stdlib only,
no network. Refuses --selftest (checks live in selftest_csp.py).
"""

import argparse
import json
import os
import re
import sys

# [CHOICE 1] The pattern set. Each entry is (class, regex); group 1 is
# the dependency text. Edit here; nothing below reads class names.
PATTERNS = {
    "instrument": [
        r"\b(?:measured|recorded|acquired|collected|imaged|observed|detected|counted|scanned)\s+"
        r"(?:using|with|on)\s+(?:a|an|the)?\s*([^.,;()]{3,60}?)\s*(?=[.,;()]|\s(?:at|in|for|which|that)\b)",
        r"\b(?:using|with)\s+(?:a|an|the)?\s*([^.,;()]{3,60}?(?:spectrometer|microscope|telescope|detector|"
        r"sensor|analy[sz]er|chromatograph|sequencer|camera|logger|probe|balance|thermometer|gauge|"
        r"interferometer|cytometer|oscilloscope|magnetometer|manometer|thermocouple))\b",
    ],
    "calibration_chain": [
        r"\b(?:calibrated|traceable|standardi[sz]ed|referenced|normali[sz]ed)\s+"
        r"(?:against|to|using|with)\s+(?:a|an|the)?\s*([^.,;()]{3,70}?)\s*(?=[.,;()]|\s(?:at|in|for|which|that)\b)",
    ],
    "method_inherited": [
        r"\b(?:following|according to|as described (?:in|by)|adapted from|modified from|"
        r"the (?:method|protocol|procedure|approach) of|per the (?:method|protocol) in)\s+"
        r"([^.,;()]{3,70}?)\s*(?=[.,;()]|\s(?:with|which|that)\b)",
    ],
    "material_supplied": [
        r"\b(?:obtained|purchased|supplied|provided|sourced|donated|acquired)\s+"
        r"(?:from|by)\s+(?:a|an|the)?\s*([^.,;()]{3,70}?)\s*(?=[.,;()]|\s(?:at|in|for|which|that)\b)",
    ],
    "prior_result": [
        r"\b(?:based on|building on|from the results? of|as (?:previously )?reported (?:in|by)|"
        r"taken from|values? from|parameters? from|drawn from)\s+"
        r"([^.,;()]{3,70}?)\s*(?=[.,;()]|\s(?:at|in|for|which|that)\b)",
        r"\(([A-Z][\w-]+(?: (?:and|&) [A-Z][\w-]+)?(?: et al\.?)?,? (?:19|20)\d\d[a-z]?)\)",
    ],
    "infrastructure": [
        r"\b(?:performed|computed|run|ran|carried out|conducted|hosted|processed|executed|stored)\s+"
        r"(?:on|at|using|in)\s+(?:a|an|the)?\s*([^.,;()]{3,70}?(?:cluster|facility|supercomputer|server|"
        r"beamline|observatory|network|database|repository|platform|pipeline|grid|archive|laboratory|"
        r"testbed|reactor|accelerator))\b",
    ],
}

# [CHOICE 2] Explicit in-text verification: one of these verbs in the
# SAME sentence as the dependency, in a verifying construction.
VERIFY = re.compile(
    r"\b(?:we|was|were|been|and|then|independently|subsequently)\s+"
    r"(?:verified|validated|confirmed|cross-checked|checked|re-?measured|reproduced|tested)\b", re.I)

SENTENCE_END = re.compile(r"[.!?](?:\s|$)")

CLASSES = list(PATTERNS)


def sentences(text):
    """(start, end) char spans of sentences, splitting on . ! ? + space."""
    out, start = [], 0
    for m in SENTENCE_END.finditer(text):
        out.append((start, m.end()))
        start = m.end()
    if start < len(text):
        out.append((start, len(text)))
    return out


def sentence_of(spans, pos):
    for s, e in spans:
        if s <= pos < e:
            return s, e
    return 0, 0


def extract(text, result_id, source_ref):
    """One record per (span, class). A span caught by two classes is
    emitted twice: the class assignment is the pattern's, not adjudicated."""
    spans = sentences(text)
    records = []
    for cls in CLASSES:
        for pat in PATTERNS[cls]:
            for m in re.finditer(pat, text, re.I):
                dep = " ".join(m.group(1).split())
                if not dep:
                    continue
                s, e = sentence_of(spans, m.start(1))
                verified = bool(VERIFY.search(text[s:e]))
                records.append({
                    "result_id": result_id,
                    "dependency": dep,
                    "class": cls,
                    "verified_in_argument": verified,
                    "source_span": [m.start(1), m.end(1)],
                    "source_ref": source_ref,
                })
    # one pattern set can catch one span twice inside one class; that is
    # one dependency, not two. Two CLASSES on one span stay two records.
    seen, out = set(), []
    for r in sorted(records, key=lambda r: (r["source_span"][0], r["class"])):
        key = (tuple(r["source_span"]), r["class"])
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def read_dir(path):
    files = sorted(f for f in os.listdir(path) if f.endswith((".txt", ".md")))
    for f in files:
        with open(os.path.join(path, f), encoding="utf-8", errors="replace") as fh:
            yield os.path.splitext(f)[0], f, fh.read()


def report(records, n_files):
    """Counts by class and the ratio required / argued. The ratio is
    None when nothing is argued: 0 in the denominator is not a large
    number, it is an absence of the quantity."""
    by_class = {c: 0 for c in CLASSES}
    for r in records:
        by_class[r["class"]] += 1
    required = len(records)
    argued = sum(1 for r in records if r["verified_in_argument"])
    ratio = (required / argued) if argued else None
    return {
        "files": n_files,
        "by_class": by_class,
        "dependencies_required": required,
        "dependencies_argued": argued,
        "verified_false_count": required - argued,
        "ratio_required_over_argued": ratio,
        "floor_note": "every count is a floor set by the pattern set [CHOICE 1]",
    }


def render_report(rep):
    lines = ["P1 dependency records", "files read: %d" % rep["files"]]
    for c in CLASSES:
        lines.append("  %-20s %4d" % (c, rep["by_class"][c]))
    lines.append("dependencies required : %d" % rep["dependencies_required"])
    lines.append("dependencies argued   : %d" % rep["dependencies_argued"])
    lines.append("verified_in_argument = False : %d" % rep["verified_false_count"])
    r = rep["ratio_required_over_argued"]
    lines.append("required / argued     : " + ("%.2f" % r if r is not None else "undefined (argued = 0)"))
    lines.append(rep["floor_note"])
    return "\n".join(lines)


def run(in_dir, out_path=None):
    all_records, n = [], 0
    for result_id, fname, text in read_dir(in_dir):
        n += 1
        all_records.extend(extract(text, result_id, fname))
    if out_path:
        with open(out_path, "w", encoding="utf-8") as fh:
            for r in all_records:
                fh.write(json.dumps(r, sort_keys=True) + "\n")
    return all_records, report(all_records, n)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_dir")
    ap.add_argument("--out")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        print("p1_deps_extract has no selftest; run selftest_csp.py", file=sys.stderr)
        return 2
    if not a.in_dir:
        print("--in DIR of plaintext methods sections is required; none is shipped", file=sys.stderr)
        return 2
    records, rep = run(a.in_dir, a.out)
    if a.report or not a.out:
        print(render_report(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
