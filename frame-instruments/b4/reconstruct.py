"""B4.2 reconstruct.py -- one prompt file per (item, reconstructor).

Each file holds {"text_verbatim": ...} and NOTHING else. Built from the
validated items file alone. Layout enforces the boundary:

    OUT/<reconstructor_id>/<item_id>.jsonl

so a reconstructor receives one directory and nothing in it names any
other reconstructor, any requirement, any category, or any prior run.
After writing, every file is re-read and asserted to carry exactly the
one key.

Command: python3 reconstruct.py ITEMS_VALID.jsonl --reconstructors r1,r2,r3 --out PROMPTS_DIR
"""
import argparse
import json
import os
import sys

from common import (ITEM_FIELDS, Invalid, Run, check_fields, check_id,
                    finish, read_jsonl, raise_if)

ONLY_KEY = "text_verbatim"


def build_prompt(item):
    return {ONLY_KEY: item[ONLY_KEY]}


def emit(items, reconstructors, out_dir):
    probs = []
    for rid in reconstructors:
        probs += check_id(rid, "reconstructor")
    if len(set(reconstructors)) != len(reconstructors):
        probs.append("duplicate reconstructor ids")
    for n, it in enumerate(items, 1):
        probs += check_fields(it, ITEM_FIELDS, "item row %d" % n)
    raise_if(probs)
    written = []
    for rid in reconstructors:
        d = os.path.join(out_dir, rid)
        os.makedirs(d, exist_ok=True)
        for it in items:
            path = os.path.join(d, it["item_id"] + ".jsonl")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(build_prompt(it), sort_keys=True, ensure_ascii=False) + "\n")
            written.append(path)
    assert_boundary(written, {it["item_id"]: it[ONLY_KEY] for it in items})
    return written


def assert_boundary(paths, texts):
    """Re-read every emitted file: exactly one key, value equals the item text."""
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            lines = [ln for ln in fh.read().split("\n") if ln.strip()]
        if len(lines) != 1:
            raise AssertionError("%s: expected one line, found %d" % (p, len(lines)))
        obj = json.loads(lines[0])
        if set(obj) != {ONLY_KEY}:
            raise AssertionError("%s: keys %s, expected {%r}" % (p, sorted(obj), ONLY_KEY))
        item_id = os.path.splitext(os.path.basename(p))[0]
        if obj[ONLY_KEY] != texts[item_id]:
            raise AssertionError("%s: text differs from items file" % p)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("items")
    ap.add_argument("--reconstructors", required=True, help="comma-separated ids")
    ap.add_argument("--out", required=True)
    ap.add_argument("--runs", default=None)
    a = ap.parse_args(argv)
    rids = [r.strip() for r in a.reconstructors.split(",") if r.strip()]
    with Run("b4/reconstruct.py", vars(a), None, [a.items], a.out, a.runs) as run:
        try:
            items = read_jsonl(a.items)
            if not items or not rids:
                return finish(run, "empty", {"items": len(items), "reconstructors": len(rids)})
            written = emit(items, rids, a.out)
        except Invalid as e:
            return finish(run, "error", notes=str(e))
        return finish(run, "ok", {"items": len(items), "reconstructors": len(rids),
                                  "files": len(written), "keys_per_file": 1})


if __name__ == "__main__":
    sys.exit(main())
