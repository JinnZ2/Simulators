"""Shared plumbing for the cross-run. Imports neither playground.

Both builds ship a top-level package named `playground`, so one process can
load only one of them. Every adapter therefore runs in its own process, and
the two sides exchange plain JSON through out/ (the same rule study-aperture
uses between its parent and its lab: explicit JSON, never shared state).
"""
import json, math, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
SIM_ROOT = os.path.dirname(FOLDER)
OUT = os.path.join(FOLDER, "out")
R257 = os.path.join(SIM_ROOT, "relational-playground")
SA_ROOT = os.path.abspath(os.environ.get("STUDY_APERTURE_PATH", os.path.join(SIM_ROOT, "..", "study-aperture")))
SA_EXP = os.path.join(SA_ROOT, "experimental")


def git_rev(path):
    try:
        return subprocess.check_output(["git", "-C", path, "rev-parse", "HEAD"], text=True).strip()
    except Exception as e:
        return "UNKNOWN (%s)" % type(e).__name__


def git_dirty(path, sub):
    """Lines of `git status --porcelain` under sub; empty means the original is untouched."""
    try:
        out = subprocess.check_output(["git", "-C", path, "status", "--porcelain", "--", sub], text=True)
        return [l for l in out.splitlines() if "__pycache__" not in l]
    except Exception as e:
        return ["UNKNOWN (%s)" % type(e).__name__]


def clean(x):
    """JSON-safe: inf / nan become strings so they survive the exchange."""
    if isinstance(x, float) and (math.isinf(x) or math.isnan(x)):
        return repr(x)
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    return x


def unclean(x):
    if x in ("inf", "-inf", "nan"):
        return float(x)
    if isinstance(x, dict):
        return {k: unclean(v) for k, v in x.items()}
    if isinstance(x, list):
        return [unclean(v) for v in x]
    return x


def dump(name, obj):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(clean(obj), f, indent=1, sort_keys=True)
        f.write("\n")


def load(name):
    with open(os.path.join(OUT, name)) as f:
        return unclean(json.load(f))
