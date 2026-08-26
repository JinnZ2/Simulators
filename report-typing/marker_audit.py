#!/usr/bin/env python3
"""Checks on the delivered `MARKER.md` and `reverse_arm_score.py`.

Both are imported or read; neither is modified.

This folder is the first named-and-absent artifact in the drop family
to arrive, so the first thing checked is the arrival itself -- who
named it, whether the marker's own back-reference list matches, and
what its cross-refs open in turn.

The rest is the scorer. Its design is right and its refusals are
declared, so what is checked is whether the code enforces what the
prose promises.

Nothing here tests the mechanism. Whether reports are typed by the
reporter's position is an empirical claim about institutions, no
transcript has been coded, and every literature pointer is
egress-blocked.

CC0. stdlib only. Parses under Python 3.9.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import reverse_arm_score as R  # noqa: E402

MARKER = os.path.join(HERE, "MARKER.md")

# Which of `score()`'s branches reads which declared value. Read from
# the source rather than retyped, so a new branch cannot go unnoticed.
def values_read():
    src = open(os.path.join(HERE, "reverse_arm_score.py"),
               encoding="utf-8").read()
    body = src.split("def score(")[1].split("def main(")[0]
    out = {}
    for field in R.SCOREABLES:
        got = set(re.findall(r'i\.get\("%s"\)\s*==\s*"([A-Z_]+)"' % field,
                             body))
        out[field] = got
    return out


def unread_values():
    read = values_read()
    return {k: sorted(set(spec["values"]) - read[k])
            for k, spec in R.SCOREABLES.items()}


def blindness_states():
    """What `receiver_blind` values actually drop an instance."""
    out = {}
    for v in (False, "False", "false", None, True, "True"):
        rows = R.score([{"reporter_seat": "disguised_exec",
                         "receiver_blind": v}])["by_seat"]
        out[repr(v)] = sum(s["n"] for s in rows.values())
    rows = R.score([{"reporter_seat": "disguised_exec"}])["by_seat"]
    out["<field absent>"] = sum(s["n"] for s in rows.values())
    return out


def gate_is_prose():
    """`contrast` and `verdict` -- computed, or literal?"""
    src = open(os.path.join(HERE, "reverse_arm_score.py"),
               encoding="utf-8").read()
    body = src.split("def score(")[1].split("def main(")[0]
    return {
        "contrast_literal": bool(re.search(r'"contrast":\s*UNCODED', body)),
        "verdict_literal": bool(re.search(r'"verdict":\s*UNCODED', body)),
        "double_coding_checked": "coder" in body.lower()
        and bool(re.search(r'if .*coder', body, re.I)),
        "both_arms_checked": bool(re.search(r'len\(by_seat\)', body)),
    }


def control_enforced():
    """CONTROL requires a floor-worker instance per exec instance."""
    only_exec = R.score([{"reporter_seat": "disguised_exec",
                          "receiver_blind": True}])
    return {
        "seats_present": sorted(only_exec["by_seat"]),
        "emits_a_result_with_one_arm": bool(only_exec["by_seat"]),
        "flags_the_missing_arm": "control" in json.dumps(only_exec).lower(),
    }


# ---- the arrival ---------------------------------------------------

# Two columns, not one. A folder that names this shape in authored
# prose is citing it; a folder whose only occurrences are in code, as
# an entry in a list of names being resolved, is CHECKING whether it
# exists. `question-availability` QA_007 is the finding that mention
# and existence are different columns; conflating them here would be
# that finding failing inside a checker written about it.
CITES = "cites"
CHECKS_ONLY = "checks_only"

PROSE_EXT = (".md",)
CODE_EXT = (".py",)
SKIP_DIRS = (".git", "__pycache__", "legacy")


def name_columns(name="report-typing", root=None, exclude=()):
    """folder -> CITES | CHECKS_ONLY, for every folder naming `name`.

    The split is structural: prose mention versus code-only mention.
    It is not a judgement about what the folder meant.
    """
    root = root or ROOT
    prose, code = set(), set()
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), root)
            top = rel.split(os.sep)[0]
            if top in exclude:
                continue
            if f.endswith(PROSE_EXT):
                bucket = prose
            elif f.endswith(CODE_EXT):
                bucket = code
            else:
                continue
            try:
                if name in open(os.path.join(dp, f), encoding="utf-8",
                                errors="replace").read():
                    bucket.add(top)
            except OSError:
                continue
    out = {}
    for t in sorted(prose | code):
        out[t] = CITES if t in prose else CHECKS_ONLY
    return out


def citing_folders(name="report-typing"):
    """Folders naming this shape in prose, excluding the folder itself
    and the two root index files, which this session writes."""
    cols = name_columns(name, exclude=(os.path.basename(HERE),
                                       "CLAUDE.md", "README.md"))
    return sorted(k for k, v in cols.items() if v == CITES)


def checking_folders(name="report-typing"):
    cols = name_columns(name, exclude=(os.path.basename(HERE),
                                       "CLAUDE.md", "README.md"))
    return sorted(k for k, v in cols.items() if v == CHECKS_ONLY)


def _column_null_test():
    """Known answer on a constructed tree, so the classifier is not
    graded against the corpus it is used on. Two folders, one prose
    mention and one code-only target list; nothing else in either."""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "a-marker"))
        os.makedirs(os.path.join(td, "a-checker"))
        os.makedirs(os.path.join(td, "a-silent"))
        with open(os.path.join(td, "a-marker", "MARKER.md"), "w") as fh:
            fh.write("see [[widget-shape]] for the routing argument\n")
        with open(os.path.join(td, "a-checker", "chk.py"), "w") as fh:
            fh.write('LINKS = ("widget-shape", "other")\n')
        with open(os.path.join(td, "a-silent", "n.md"), "w") as fh:
            fh.write("nothing relevant\n")
        cols = name_columns("widget-shape", root=td)
    return cols


def max_q_ordinal(folder="uninstrumented"):
    """Highest Qn found anywhere under `folder`. The marker cites Q7."""
    top = os.path.join(ROOT, folder)
    best = 0
    for dp, dn, fn in os.walk(top):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if not f.endswith((".md", ".py")):
                continue
            try:
                txt = open(os.path.join(dp, f), encoding="utf-8",
                           errors="replace").read()
            except OSError:
                continue
            for m in re.finditer(r"\bQ(\d+)\b", txt):
                best = max(best, int(m.group(1)))
    return best


def back_references():
    """Who the marker says references it."""
    txt = open(MARKER, encoding="utf-8").read()
    m = re.search(r"Referenced as the canonical shape by:\s*(.+?)\.\s*\n",
                  txt, re.S)
    if not m:
        return []
    return [x.strip() for x in re.split(r",|\n", m.group(1)) if x.strip()]


def cross_refs():
    """The CROSS-REFS block, and whether each resolves to a folder."""
    txt = open(MARKER, encoding="utf-8").read()
    m = re.search(r"## CROSS-REFS\n(.*)$", txt, re.S)
    if not m:
        return []
    out = []
    for ln in m.group(1).split("\n"):
        mm = re.match(r"^\s{4}([a-z][\w-]+)(.*)$", ln)
        if mm:
            name = mm.group(1)
            out.append({"name": name,
                        "resolves": os.path.isdir(os.path.join(ROOT, name)),
                        "note": mm.group(2).strip()[:40]})
    return out


def carried_not_branched():
    """Schema fields the scorer never reads, quantities the prose asks
    for that have no field, and whether any accumulator sums a value
    rather than counting an occurrence."""
    s = open(os.path.join(HERE, "reverse_arm_score.py"),
             encoding="utf-8").read()
    body = s.split("def score(")[1].split("def main(")[0]
    unread = [k for k in sorted(R.INSTANCE_SCHEMA)
              if k not in R.SCOREABLES and k != "receiver_blind"
              and ('"%s"' % k) not in body]
    asked = {
        "episode air order": any(w in R.INSTANCE_SCHEMA for w in
                                 ("air_order", "airdate", "order")),
        "network": "network" in R.INSTANCE_SCHEMA,
        # receiver suspicion IS expressible: the confound says
        # "code it, drop the instance", and receiver_blind=False is
        # exactly that switch. Not a gap; recorded as carried.
        "known-exec seat": "known_exec" in R.INSTANCE_SCHEMA[
            "reporter_seat"],
    }
    return {
        "unread_fields": unread,
        "asked_for_no_field": sorted(k for k, v in asked.items() if not v),
        "sums_a_value": bool(re.findall(r"\+=\s*(?!1\b)\S+", body)),
        "counters": sorted(set(re.findall(r'"(\w+)":\s*0', body))),
    }


def cli(args):
    p = subprocess.run([sys.executable,
                        os.path.join(HERE, "reverse_arm_score.py")] + args,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       timeout=60)
    return p.returncode, p.stdout.decode("utf8", "replace")


# ------------------------------------------------------------- report

def render():
    out = []
    out.append("REPORT-TYPING AUDIT")
    out.append("the marker is read and the scorer imported; neither is")
    out.append("modified")
    out.append("")
    out.append("Nothing here tests the mechanism. No transcript has been")
    out.append("coded and every literature pointer is egress-blocked.")
    out.append("")

    out.append("1. THE ARRIVAL")
    cit = citing_folders()
    che = checking_folders()
    br = back_references()
    out.append("   citing it in prose (%d): %s" % (len(cit), ", ".join(cit)))
    out.append("   only checking whether it existed (%d): %s"
               % (len(che), ", ".join(che) or "none"))
    out.append("   -- two columns, because a name in a cross-link")
    out.append("      checker's target list is not a citation. Pooling")
    out.append("      them is QA_007 failing inside a checker written")
    out.append("      about QA_007.")
    out.append("   the marker's own list (%d): %s" % (len(br), ", ".join(br)))
    missing = [c for c in cit if not any(c in b for b in br)]
    unmatched = [b for b in br
                 if not os.path.isdir(os.path.join(ROOT, b))]
    out.append("   citing but not listed: %s" % (missing or "none"))
    out.append("   listed but not a folder name: %s" % (unmatched or "none"))
    out.append("")

    out.append("2. WHAT THE MARKER'S OWN CROSS-REFS OPEN")
    for r in cross_refs():
        out.append("     %-26s %-5s %s" % (r["name"],
                                           "yes" if r["resolves"] else "NO",
                                           r["note"]))
    out.append("   uninstrumented resolves; the Q7 it cites does not.")
    out.append("   The highest question ordinal anywhere in that folder")
    out.append("   is Q%d, so the reference is one past the end, and R4"
               % max_q_ordinal())
    out.append("   rests on it.")
    out.append("")

    out.append("3. BLINDNESS IS THE DESIGN, AND THE CHECK IS `is False`")
    for k, n in blindness_states().items():
        out.append("     receiver_blind=%-16s instances counted: %d"
                   % (k, n))
    out.append("   The schema shows the field as the STRING")
    out.append("   \"True | False -- if False, DROP the instance\", so a")
    out.append("   coder following it writes strings, and the string")
    out.append("   \"False\" does not drop anything. A missing field does")
    out.append("   not either.")
    out.append("")

    out.append("4. DECLARED VALUES THE SCORER NEVER READS")
    uv = unread_values()
    for k in sorted(uv):
        spec = R.SCOREABLES[k]
        out.append("     %-18s %d of %d unread: %s"
                   % (k, len(uv[k]), len(spec["values"]),
                      ", ".join(uv[k])[:44]))
    out.append("")
    out.append("   d_exec_testimony is read on none of its five values,")
    out.append("   and its stated purpose is to distinguish the two")
    out.append("   available readings of the whole genre.")
    out.append("")
    out.append("   b_time_to_action's stated purpose is that the discount")
    out.append("   is a DELAY and refusal is the tail of the")
    out.append("   distribution, not the measurement. The scorer reads")
    out.append("   NEVER and nothing else, which is the tail.")
    out.append("")

    out.append("5. THE TWO-CONDITION GATE IS PROSE")
    g = gate_is_prose()
    for k in sorted(g):
        out.append("     %-24s %s" % (k, g[k]))
    out.append("   The note says contrast and verdict stay None until")
    out.append("   both arms have instances and a second coder has")
    out.append("   passed. Both are written as the literal UNCODED, so")
    out.append("   they are None whatever happens, and the two")
    out.append("   conditions are checked nowhere.")
    out.append("")

    out.append("6. THE CONTROL ARM IS REQUIRED AND NOT ENFORCED")
    ce = control_enforced()
    out.append("     one-arm input emits a result: %s"
               % ce["emits_a_result_with_one_arm"])
    out.append("     the missing arm is flagged:   %s"
               % ce["flags_the_missing_arm"])
    out.append("   CONTROL says a dismissal rate without the")
    out.append("   floor-worker rate in the same setting is")
    out.append("   uninterpretable. score() returns by_seat for whatever")
    out.append("   seats it was given.")
    out.append("")

    out.append("7. CLI")
    for args, label in ((["--schema"], "--schema"),
                        ([], "no argument"),
                        (["nosuch.json"], "missing file")):
        rc, o = cli(args)
        first = (o.strip().split("\n") or [""])[0]
        out.append("     %-18s rc=%-3s %s" % (label, rc, first[:40]))
    out.append("")

    out.append("8. STATED IN PROSE, NO FIELD OR NO BRANCH")
    cb = carried_not_branched()
    out.append("   schema fields the scorer never reads: %s"
               % ", ".join(cb["unread_fields"]))
    out.append("   -- `domain` is Instrument 2's sharp test (a report")
    out.append("      inside the reporter's prior expertise). It is")
    out.append("      codable and scored nowhere.")
    out.append("   quantities the prose asks for with no field: %s"
               % ", ".join(cb["asked_for_no_field"]))
    out.append("   -- CONFOUNDS/editing says code air order and network")
    out.append("      \"so it can be checked rather than assumed\".")
    out.append("   -- CONTROL's expected result names known-exec")
    out.append("      instances; reporter_seat declares two values and")
    out.append("      that is not one of them.")
    out.append("   every accumulator counts occurrences: %s"
               % (not cb["sums_a_value"]))
    out.append("   -- so b_time_to_action's integer beats are never")
    out.append("      summed, averaged, or binned. The delay its own")
    out.append("      `why` calls the measurement has no accumulator")
    out.append("      at all; only the NEVER tail has one.")
    out.append("")
    return "\n".join(out)


# ------------------------------------------------------------ selftest

def selftest():
    ok = [0]
    bad = []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    # -- 0. the classifier, on a constructed tree
    nt = _column_null_test()
    chk("a prose mention classifies as citing",
        nt.get("a-marker") == CITES)
    chk("a code-only target list classifies as checking",
        nt.get("a-checker") == CHECKS_ONLY)
    chk("a folder not naming it appears in neither column",
        "a-silent" not in nt)
    chk("the two columns are the only ones", set(nt.values())
        <= {CITES, CHECKS_ONLY})

    # -- 1. the arrival
    cit = citing_folders()
    che = checking_folders()
    chk("the columns are disjoint", not (set(cit) & set(che)))
    chk("some folder cites this shape in prose", len(cit) > 0)
    chk("some folder only checked whether it existed", len(che) > 0)
    br = back_references()
    chk("the marker's own list is shorter than the citing set",
        len(br) < len(cit))
    chk("at least one citing folder is not on that list",
        any(not any(c in b for b in br) for c in cit))
    chk("one listed name is not a folder",
        any(not os.path.isdir(os.path.join(ROOT, b)) for b in br))
    chk("each unmatched listed name has a folder with that prefix",
        all(any(d.startswith(b.split("-by-")[0])
                for d in os.listdir(ROOT))
            for b in br if not os.path.isdir(os.path.join(ROOT, b))))

    # -- 2. cross-refs
    cr = cross_refs()
    chk("seven cross-refs are extracted", len(cr) == 7)
    unresolved = [r["name"] for r in cr if not r["resolves"]]
    chk("three do not resolve", len(unresolved) == 3)
    chk("merit-anchoring is one", "merit-anchoring" in unresolved)
    chk("uninstrumented does resolve",
        any(r["name"] == "uninstrumented" and r["resolves"] for r in cr))

    # -- the Q7 reference. Not just absent: the highest question
    #    ordinal anywhere in that folder is Q6, so the marker cites
    #    one past the end.
    chk("no Q7 anywhere in uninstrumented", max_q_ordinal() < 7)
    chk("Q6 does exist, so the numbering is real", max_q_ordinal() == 6)
    chk("R4 rests on the reference",
        "direct instance of Q7" in open(MARKER, encoding="utf-8").read())

    # -- 3. blindness
    bs = blindness_states()
    chk("boolean False drops the instance", bs["False"] == 0)
    chk("the string 'False' does not", bs["'False'"] == 1)
    chk("a missing field does not", bs["<field absent>"] == 1)
    chk("None does not", bs["None"] == 1)
    chk("the schema shows the field as a string",
        isinstance(R.INSTANCE_SCHEMA["receiver_blind"], str))
    chk("and the string it shows contains False",
        "False" in R.INSTANCE_SCHEMA["receiver_blind"])

    # -- 4. unread values
    uv = unread_values()
    chk("d_exec_testimony is read on no value",
        len(uv["d_exec_testimony"]) == len(
            R.SCOREABLES["d_exec_testimony"]["values"]))
    chk("b_time_to_action reads only the tail",
        uv["b_time_to_action"] == ["NOT_STATED", "integer beats"])
    chk("its stated purpose names the distribution",
        "distribution" in R.SCOREABLES["b_time_to_action"]["why"])
    chk("a_prior_filing reads one of four",
        len(uv["a_prior_filing"]) == 3)
    chk("c_attribution reads two of four",
        len(uv["c_attribution"]) == 2)
    chk("values_read is derived from the source, not typed",
        values_read()["c_attribution"] == {"EXEC_INSIGHT",
                                           "WORKER_WHO_SAID_IT"})

    # -- 5. the gate
    g = gate_is_prose()
    chk("contrast is a literal", g["contrast_literal"])
    chk("verdict is a literal", g["verdict_literal"])
    chk("no double-coding condition is checked",
        not g["double_coding_checked"])
    chk("no both-arms condition is checked", not g["both_arms_checked"])
    r = R.score([{"reporter_seat": "disguised_exec", "receiver_blind": True},
                 {"reporter_seat": "floor_worker", "receiver_blind": True}])
    chk("two arms still give a None contrast", r["contrast"] is None)
    chk("and a None verdict", r["verdict"] is None)
    chk("the note states the two conditions",
        "second coder" in r["note"] and "both arms" in r["note"])

    # -- 6. the control
    ce = control_enforced()
    chk("a one-arm input still emits a result",
        ce["emits_a_result_with_one_arm"])
    chk("the missing arm is not flagged", not ce["flags_the_missing_arm"])
    chk("CONTROL states the requirement",
        "For every disguised-exec" in R.CONTROL["requirement"])
    chk("and states its own falsifier", "R1 fails" in R.CONTROL["falsifier"])

    # -- 7. CLI
    rc, o = cli(["--schema"])
    chk("--schema exits 0 and emits JSON", rc == 0 and o.strip()[0] == "{")
    chk("the schema carries all four blocks",
        set(json.loads(o)) == {"instance", "scoreables", "control",
                               "confounds"})
    rc, o = cli([])
    chk("no argument emits the schema rather than nothing", rc == 0
        and "instance" in json.loads(o))
    rc, o = cli(["nosuch_xyz.json"])
    chk("a missing file raises rather than reporting",
        rc != 0 and "FileNotFoundError" in o)

    # -- what the marker gets right, asserted so it cannot quietly go
    txt = open(MARKER, encoding="utf-8").read()
    chk("the one-observer note is labelled an observation",
        "not a scored count" in txt)
    chk("the convenience sample states direction not rate",
        "direction not rate" in txt)
    chk("the marker declares itself under exploration",
        "not a position under defense" in txt)
    chk("it ships falsifiers", txt.count("→") >= 4
        or "## FALSIFIERS" in txt)
    chk("the confounds block names the editing bias by arm",
        "biases the FORWARD arm heavily" in R.CONFOUNDS["editing"])

    # -- 8. carried, not branched
    cb = carried_not_branched()
    chk("domain is in the schema", "domain" in R.INSTANCE_SCHEMA)
    chk("and the scorer never reads it", "domain" in cb["unread_fields"])
    chk("Instrument 2 names domain as the sharp test",
        "original domain" in open(MARKER, encoding="utf-8").read())
    chk("air order has no field",
        "episode air order" in cb["asked_for_no_field"])
    chk("network has no field", "network" in cb["asked_for_no_field"])
    chk("the confound asks for both",
        "air order and network" in R.CONFOUNDS["editing"])
    chk("known-exec is not a declared seat",
        "known-exec seat" in cb["asked_for_no_field"])
    chk("receiver suspicion IS expressible and is not listed",
        "receiver suspicion" not in cb["asked_for_no_field"])
    chk("the drop switch it uses is the one branch that works",
        R.score([{"reporter_seat": "x",
                  "receiver_blind": False}])["by_seat"] == {})
    chk("and the control's expected result needs it",
        "known-exec" in R.CONTROL["expected_if_marker_holds"])
    chk("no accumulator sums a value", not cb["sums_a_value"])
    chk("five counters, all occurrences", len(cb["counters"]) == 5)
    chk("integer beats is a declared value",
        "integer beats" in R.SCOREABLES["b_time_to_action"]["values"])

    out = render()
    chk("render names all eight sections",
        all(("%d." % i) in out for i in range(1, 9)))

    # -- the emitted report carries no severity or interpretation
    #    language. Exemption list is empty; both arms run so the
    #    screen is not silent by construction.
    sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
    import no_severity  # noqa: E402
    chk("the report is clean with no exemption",
        not no_severity.hits(out))
    chk("a planted violation is caught",
        bool(no_severity.hits(out + "\nthis marker is broken\n")))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for b in bad:
        print("  FAILED", b)
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
