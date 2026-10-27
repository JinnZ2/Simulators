#!/usr/bin/env python3
"""Classifier B: rule-based, MAINTAINERS text only, as pre-registered.

Does not read classifier A and does not look at path names for vendor
tokens.  The only use of the path is to find which MAINTAINERS sections
cover it -- which the rule requires.
"""
import re, subprocess, sys, collections
import subsystems as S

GENERIC = {
    "kernel.org", "gmail.com", "googlemail.com", "hotmail.com",
    "yahoo.com", "outlook.com", "zeniv.linux.org.uk", "infradead.org",
    "linux.ie", "free.fr", "gnu.org", "protonmail.com", "web.de",
    "posteo.de", "riseup.net", "users.sourceforge.net",
}
GIT = ["git", "-C", "/tmp/claude-0/-home-user/"
       "edb5a076-aa65-52b4-b9f8-d9089c041f39/scratchpad/ks/linux"]


def maintainers(tag):
    return subprocess.run(GIT + ["show", "%s:MAINTAINERS" % tag],
                          capture_output=True, text=True, check=True).stdout


def sections(text):
    """Split MAINTAINERS into (title, [(key, value)]) blocks."""
    out, title, fields = [], None, []
    for line in text.split("\n"):
        m = re.match(r"^([A-Z]):\t?(.*)$", line)
        if m:
            fields.append((m.group(1), m.group(2).strip()))
        else:
            if fields:
                out.append((title, fields))
            fields = []
            if line.strip() and not line.startswith(("\t", " ")):
                title = line.strip()
    if fields:
        out.append((title, fields))
    return out


def covers(pattern, path):
    """Does an F: pattern cover this subsystem path?"""
    pat = pattern.rstrip("/")
    p = path.rstrip("/")
    if pat.endswith("*"):
        return p.startswith(pat[:-1])
    return p == pat or p.startswith(pat + "/") or pat.startswith(p + "/")


CATCH_ALL = {"*", "*/", "**"}


def is_catch_all(section):
    """[D2] MAINTAINERS carries a catch-all section (THE REST) whose
    F: patterns are `*` and `*/`.  It covers every path, carries
    L: linux-kernel@vger.kernel.org, and contributes Linus's
    linux-foundation.org domain to every path's list.

    The pre-registered rule says "sections whose F: patterns cover the
    path" and did not exclude it.  Taken literally the classifier is
    CONSTANT_FIRES: 36 of 36 SHARED_CORE.  That degenerate result is
    published (mode="literal") rather than discarded, alongside the
    minimal declared repair (mode="repaired") that drops sections whose
    every F: pattern matches the whole tree.
    """
    fs = [v for k, v in section[1] if k == "F"]
    return bool(fs) and all(f.strip() in CATCH_ALL for f in fs)


def covering(secs, path, mode="repaired"):
    hit = [s for s in secs if any(k == "F" and covers(v, path)
                                  for k, v in s[1])]
    if mode == "repaired":
        hit = [s for s in hit if not is_catch_all(s)]
    elif mode != "literal":
        raise ValueError("unknown mode %r" % mode)
    return hit


def domain(addr):
    m = re.search(r"<([^>]+)>", addr) or re.search(r"(\S+@\S+)", addr)
    if not m:
        return None
    a = m.group(1)
    return a.split("@")[-1].lower().strip(">").strip() if "@" in a else None


def classify(secs, path, order="stake_first", mode="repaired"):
    """[D1] The pre-registered rule is ORDER-DEPENDENT and the
    pre-registration did not say so.  A section with exactly one
    corporate domain, <=2 M: lines, AND an lkml L: line satisfies the
    STAKE arm and the SHARED_CORE arm at once.

    The rule is NOT changed here -- changing it after seeing that would
    be post-hoc tuning.  Both readings are run and both are published:
      stake_first -- the bullets read as written, top to bottom
      core_first  -- the SHARED_CORE arm evaluated first
    """
    cov = covering(secs, path, mode)
    if not cov:
        return "MIXED/UNCLEAR", {"reason": "no covering section",
                                 "n_M": 0, "corporate": [],
                                 "n_sections": 0, "lkml": False,
                                 "arm_conflict": False}
    ms, ls = [], []
    for _t, fields in cov:
        for k, v in fields:
            if k == "M":
                ms.append(v)
            elif k == "L":
                ls.append(v.lower())
    doms = [d for d in (domain(x) for x in ms) if d]
    corp = sorted({d for d in doms if d not in GENERIC})
    lkml = any("linux-kernel@vger.kernel.org" in x for x in ls)
    stake_arm = bool(corp) and len(corp) == 1 and len(ms) <= 2
    core_arm = len(corp) >= 3 or lkml
    info = {"n_M": len(ms), "corporate": corp, "n_sections": len(cov),
            "lkml": lkml, "arm_conflict": stake_arm and core_arm}
    if order == "stake_first":
        first, second = (stake_arm, "STAKE_SPECIFIC"), (core_arm, "SHARED_CORE")
    elif order == "core_first":
        first, second = (core_arm, "SHARED_CORE"), (stake_arm, "STAKE_SPECIFIC")
    else:
        raise ValueError("unknown order %r" % order)
    if first[0]:
        return first[1], info
    if second[0]:
        return second[1], info
    return "MIXED/UNCLEAR", info


def run(tag="v4.14", order="stake_first", mode="repaired"):
    secs = sections(maintainers(tag))
    return {p: classify(secs, p, order, mode) for p in S.PATHS}


def selftest():
    n = 0
    def chk(c, name):
        nonlocal n
        n += 1
        assert c, name
    chk(covers("kernel/cgroup*", "kernel/cgroup/"), "star pattern covers")
    chk(covers("drivers/net/ethernet/intel/", "drivers/net/ethernet/intel/i40e/"),
        "parent dir covers child")
    chk(covers("mm/", "mm/"), "exact covers")
    chk(not covers("fs/xfs/", "fs/ext4/"), "sibling does not cover")
    chk(domain("A B <x@intel.com>") == "intel.com", "domain parse")
    chk(domain("no address here") is None, "domain absent -> None")
    chk(domain("A <x@KERNEL.ORG>") == "kernel.org", "domain lowercased")
    # rule arms, on synthetic sections
    S1 = [("T", [("M", "A <a@acme.com>"), ("F", "x/")])]
    chk(classify(S1, "x/")[0] == "STAKE_SPECIFIC", "one corp, <=2 M -> stake")
    S2 = [("T", [("M", "A <a@a.com>"), ("M", "B <b@b.com>"),
                 ("M", "C <c@c.com>"), ("F", "x/")])]
    chk(classify(S2, "x/")[0] == "SHARED_CORE", "3 corp domains -> core")
    S3 = [("T", [("M", "A <a@a.com>"), ("L", "linux-kernel@vger.kernel.org"),
                 ("F", "x/")])]
    # [D1] both arms fire; the bullet order decides, and it is published both ways
    chk(classify(S3, "x/", "stake_first")[0] == "STAKE_SPECIFIC",
        "arm conflict, bullets as written -> stake")
    chk(classify(S3, "x/", "core_first")[0] == "SHARED_CORE",
        "arm conflict, core arm first -> core")
    chk(classify(S3, "x/")[1]["arm_conflict"] is True, "conflict flagged")
    chk(classify(S2, "x/")[1]["arm_conflict"] is False, "no false conflict")
    try:
        classify(S2, "x/", "nope"); chk(False, "bad order refused")
    except ValueError:
        chk(True, "bad order refused")
    # [D2] catch-all detection
    REST = ("THE REST", [("M", "L T <t@linux-foundation.org>"),
                         ("L", "linux-kernel@vger.kernel.org"),
                         ("F", "*"), ("F", "*/")])
    chk(is_catch_all(REST), "THE REST is catch-all")
    chk(not is_catch_all(S1[0]), "a real section is not catch-all")
    chk(not is_catch_all(("T", [("M", "a@b.com")])), "no F: is not catch-all")
    chk(len(covering([REST] + S1, "x/", "literal")) == 2, "literal keeps it")
    chk(len(covering([REST] + S1, "x/", "repaired")) == 1, "repaired drops it")
    chk(classify([REST] + S1, "x/", mode="literal")[0] == "SHARED_CORE",
        "literal: catch-all forces core")
    chk(classify([REST] + S1, "x/", mode="repaired")[0] == "STAKE_SPECIFIC",
        "repaired: real section decides")
    try:
        covering([], "x/", "nope"); chk(False, "bad mode refused")
    except ValueError:
        chk(True, "bad mode refused")
    S4 = [("T", [("M", "A <a@a.com>"), ("M", "B <b@b.com>"), ("F", "x/")])]
    chk(classify(S4, "x/")[0] == "MIXED/UNCLEAR", "2 corp domains -> mixed")
    S5 = [("T", [("M", "A <a@gmail.com>"), ("F", "x/")])]
    chk(classify(S5, "x/")[0] == "MIXED/UNCLEAR", "generic only -> mixed")
    chk(classify([], "x/")[0] == "MIXED/UNCLEAR", "no section -> mixed")
    chk(classify([], "x/")[1]["reason"] == "no covering section", "reason named")
    print("checks: %d  failed: 0" % n)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest(); sys.exit(0)
    import json
    out = {}
    for mode in ("literal", "repaired"):
        for order in ("stake_first", "core_first"):
            out["%s/%s" % (mode, order)] = {
                p: run(order=order, mode=mode)[p][0] for p in S.PATHS}
    for k, v in out.items():
        cnt = collections.Counter(v.values())
        print("%-24s %s" % (k, dict(cnt)))
    json.dump(out, open("classifier_b.json", "w"), indent=1, sort_keys=True)
