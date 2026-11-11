"""Fetch the one open dataset this folder reads, at a pinned commit, and check its hash.

    python3 tools/fetch_data.py            # clone into data/raw/ (git-ignored), verify sha256
    python3 tools/fetch_data.py --check    # verify only; exit 3 if absent

Source: Thapa P. (2025), github.com/thapawan/MeanderClassification, MIT licence.
The bytes are NOT checked into this repository (third-party licence, 9.4 MB); only the
pin, the hash and the derived numbers are. A copy that does not match the hash is
reported as differing, never used. stdlib only; needs `git` on PATH.
"""
import hashlib, os, subprocess, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(HERE, "data", "raw", "MeanderClassification")
URL = "https://github.com/thapawan/MeanderClassification"
COMMIT = "0b9be85c58a527b113f72c9613cfbc8351a8ab60"
FILE = "Data/MeanderClass_Final_6_24_2025.csv"
SHA256 = "02aa78259f0844ea703ca904ee7dcf4fe22c2b22aaad1a4b405ee31235c4dd49"
PATH = os.path.join(RAW, FILE)


def state(path=PATH):
    if not os.path.exists(path):
        return "NOT_PRESENT"
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    return "PRESENT_MATCH" if h == SHA256 else "PRESENT_DIFFERS"


def fetch():
    if state() == "PRESENT_MATCH":
        return state()
    os.makedirs(RAW, exist_ok=True)
    env = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1")
    run = lambda *a: subprocess.run(["git", "-C", RAW, *a], check=True, env=env, capture_output=True)
    if not os.path.isdir(os.path.join(RAW, ".git")):
        run("init", "-q")
        run("remote", "add", "origin", URL)
    run("fetch", "-q", "--depth", "1", "origin", COMMIT)
    run("checkout", "-q", COMMIT)
    return state()


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("refused: tools/fetch_data.py has no selftest; run python3 tests/test_meander.py")
        sys.exit(2)
    s = state() if "--check" in sys.argv else fetch()
    print(f"{s}  {FILE}  sha256 {SHA256[:12]}...  commit {COMMIT[:12]}")
    sys.exit(0 if s == "PRESENT_MATCH" else 3)
