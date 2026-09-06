"""runrecord -- one record per run of every script in frame-instruments.

Built from the shared spec in README.md and the B1-B3 order. Appends to
runs/runs.jsonl. Record fields:
  run_id, utc, script, args_hash, seed, input_files (name+sha256),
  output_file, status, counts, notes
status is one of ok | void | error | empty.

RULE: a run that fails, voids, or returns nothing STILL WRITES ITS
RECORD, in the same form, by the same code path.  `Run` is a context
manager; the write happens in __exit__ on every path, including an
uncaught exception (recorded as status=error, then re-raised).

Command:  python3 runrecord.py [RUNS_DIR]   -- print the records
"""
import datetime
import hashlib
import json
import os
import sys

STATUSES = ("ok", "void", "error", "empty")
RECORD_FILE = "runs.jsonl"
DEFAULT_RUNS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs")
EXIT = {"ok": 0, "error": 1, "void": 2, "empty": 3}


def sha256_path(path):
    """sha256 of a file; for a directory, sha256 over sorted (relpath, filehash)."""
    h = hashlib.sha256()
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            dirs.sort()
            for name in sorted(files):
                full = os.path.join(root, name)
                rel = os.path.relpath(full, path)
                h.update(rel.encode("utf-8") + b"\0" + sha256_path(full).encode("ascii") + b"\n")
        return h.hexdigest()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def args_hash(args):
    canon = json.dumps(args, sort_keys=True, default=str)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:16]


def describe_inputs(paths):
    out = []
    for p in paths or []:
        if p is None:
            continue
        if os.path.exists(p):
            out.append({"name": os.path.basename(os.path.normpath(p)), "sha256": sha256_path(p)})
        else:
            out.append({"name": os.path.basename(os.path.normpath(p)), "sha256": None})
    return out


class Run(object):
    """Context manager. Scripts call run.set(status, counts, notes); the
    record is written in __exit__ regardless of how the block ends."""

    def __init__(self, script, args, seed, input_files, output_file, runs_dir=None):
        self.script = script
        self.args = dict(args or {})
        self.seed = seed
        self.input_files = list(input_files or [])
        self.output_file = output_file
        self.runs_dir = runs_dir or DEFAULT_RUNS_DIR
        self.status = "error"
        self.counts = {}
        self.notes = "run did not reach set()"
        self.record = None

    def set(self, status, counts=None, notes=""):
        if status not in STATUSES:
            raise ValueError("status must be one of %s, got %r" % (STATUSES, status))
        self.status = status
        self.counts = dict(counts or {})
        self.notes = notes
        return EXIT[status]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc is not None:
            self.status = "error"
            self.notes = "uncaught: %r" % (exc,)
        self.record = self._write()
        return False  # never swallow

    def _write(self):
        utc = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        inputs = describe_inputs(self.input_files)
        ah = args_hash(self.args)
        rid_src = "|".join([self.script, ah, str(self.seed), utc] + [i["sha256"] or "-" for i in inputs])
        rec = {
            "run_id": hashlib.sha256(rid_src.encode("utf-8")).hexdigest()[:16],
            "utc": utc,
            "script": self.script,
            "args_hash": ah,
            "seed": self.seed,
            "input_files": inputs,
            "output_file": self.output_file,
            "status": self.status,
            "counts": self.counts,
            "notes": self.notes,
        }
        os.makedirs(self.runs_dir, exist_ok=True)
        with open(os.path.join(self.runs_dir, RECORD_FILE), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
        return rec


def read_records(runs_dir=None):
    path = os.path.join(runs_dir or DEFAULT_RUNS_DIR, RECORD_FILE)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    runs_dir = argv[0] if argv else DEFAULT_RUNS_DIR
    recs = read_records(runs_dir)
    if not recs:
        print("no records in %s" % runs_dir)
        return 3
    print("%-16s %-20s %-18s %-6s %s" % ("run_id", "utc", "script", "status", "output_file"))
    for r in recs:
        print("%-16s %-20s %-18s %-6s %s" % (r["run_id"], r["utc"], r["script"], r["status"], r["output_file"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
