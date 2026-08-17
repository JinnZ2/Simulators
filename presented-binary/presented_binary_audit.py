#!/usr/bin/env python3
"""presented_binary_audit.py -- checks on the presented-binary drop.

Added, not delivered. Imports binary_audit.py and frame_sim.py and
modifies neither. Findings are recorded in AUDIT_NOTES.md as PB_001..010.

    python3 presented_binary_audit.py

frame_sim writes run state next to itself. This audit redirects RUNDIR to
a temporary directory and removes it, so running the audit leaves no runs
behind and the delivered folder is unchanged.

stdlib only, deterministic. CC0.
"""

import contextlib
import io
import json
import os
import shutil
import tempfile

import binary_audit as BA
import frame_sim as FS

HERE = os.path.dirname(os.path.abspath(__file__))
BAR = "=" * 70

CHECK_IDS = [c[0] for c in BA.CHECKS]

P1 = {
    "options": [{"id": "a", "desc": "lay off 12"}, {"id": "b", "desc": "close the site"}],
    "choice": "a",
    "metric": "twelve-month cost to the operating budget",
    "reasoning": "synthetic fixture",
    "incompleteness_acknowledged": False,
}
P2 = {
    "options": [{"id": "x", "desc": "1"}, {"id": "y", "desc": "2"}, {"id": "z", "desc": "3"}],
    "choice": "z",
}


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


@contextlib.contextmanager
def sandbox():
    """Point frame_sim's RUNDIR at a scratch directory for the duration."""
    d = tempfile.mkdtemp(prefix="fs_audit_")
    old = FS.RUNDIR
    FS.RUNDIR = d
    try:
        yield d
    finally:
        FS.RUNDIR = old
        shutil.rmtree(d, ignore_errors=True)


def quiet(fn, *a, **kw):
    """Run a frame_sim command, swallow its output, return (rc, stdout)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = fn(*a, **kw)
    return (rc or 0), (out.getvalue() + err.getvalue())


def write(d, name, obj):
    p = os.path.join(d, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f)
    return p


print("presented-binary -- audit of the delivered drop")
print("delivered: binary_audit.py, frame_sim.py, CLAIM_TABLE.md")
print("%d checks in binary_audit; %d claims in the delivered table" % (
    len(BA.CHECKS), 9))

# ----------------------------------------------------------------- PB_001
head(1, "PB_001", "both verification statements rest on files that did not arrive")
print("""
CLAIM_TABLE.md, "Status":

    binary_audit.py "has one seeded case, a generic framing rather than a
    documented incident, scoring 0 documented of 11."

    frame_sim.py "is verified end to end against synthetic fixtures --
    seal enforcement, prompt withholding, and tamper detection all
    confirmed."

Neither the case file nor the fixtures are in the drop.
""".strip())
print()
casedir = BA.CASEDIR
print("  binary_audit.CASEDIR = %s" % os.path.relpath(casedir, HERE))
print("  exists: %s" % os.path.isdir(casedir))
print("  case files: %d" % (len(BA.load_cases()) if os.path.isdir(casedir) else 0))
print("  -> `python3 binary_audit.py` exits 1 with 'no case files'")
print()
print("""
The seeded case is data. Inventing one would put a framing in the author's
mouth, so cases/ is left absent and the gap stays visible. The frame_sim
properties are different -- they are properties of code, checkable
directly, and the sections below check all three.

This is the second consecutive drop where the claim table's verification
sentence names a file the drop does not carry (category-weld CW_001 was
the first, and there the files arrived one drop later).
""".strip())

# ----------------------------------------------------------------- PB_002
head(2, "PB_002", "the seal is enforced at one gate and not at the other")
print("""
Three properties are claimed. Measured, in order:
""".strip())
print()
with sandbox() as d:
    p1p = write(d, "p1.json", P1)
    p2p = write(d, "p2.json", P2)
    quiet(FS.cmd_start, "T1", "lay off 12 or close the site")

    rc, _ = quiet(FS.cmd_prompt2, "T1")
    print("  prompt 2 before sealing            rc=%d  %s" % (
        rc, "refused" if rc else "RELEASED"))
    rc, _ = quiet(FS.cmd_submit2, "T1", p2p)
    print("  submit 2 before sealing            rc=%d  %s" % (
        rc, "refused" if rc else "ACCEPTED"))

    rc, out = quiet(FS.cmd_seal, "T1", p1p)
    print("  seal                               rc=%d  %s" % (rc, out.strip()))
    rc, _ = quiet(FS.cmd_seal, "T1", p1p)
    print("  re-seal the same run               rc=%d  %s" % (
        rc, "refused" if rc else "ACCEPTED"))

    # tamper: rewrite the sealed pass 1 after the fact
    sealed = os.path.join(FS.run_path("T1"), "pass1.json")
    obj = json.load(open(sealed, encoding="utf-8"))
    obj["choice"] = "b"
    with open(sealed, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
    print()
    print("  ... pass1.json edited after sealing: choice a -> b")
    print()
    print("  verify()                           %s" % FS.verify("T1"))
    rc, _ = quiet(FS.cmd_prompt2, "T1")
    print("  prompt 2 on the tampered run       rc=%d  %s" % (
        rc, "refused" if rc else "RELEASED"))
    rc, out = quiet(FS.cmd_submit2, "T1", p2p)
    quoted = [ln for ln in out.splitlines() if ln.startswith("Pass 1 choice:")]
    print("  submit 2 on the tampered run       rc=%d  %s" % (
        rc, "refused" if rc else "ACCEPTED"))
    print("  prompt 3 was built from            %s" % (quoted[0] if quoted else "?"))
    rc, _ = quiet(FS.cmd_submit3, "T1", write(d, "p3.json", {"dominates": True}))
    print("  submit 3 on the tampered run       rc=%d  %s" % (
        rc, "refused" if rc else "ACCEPTED"))
print()
print("""
Tamper detection works where it is called. It is called in cmd_prompt2 and
nowhere else. cmd_submit2 checks only that seal.json EXISTS, so a pass 1
rewritten after sealing flows straight through, and prompt 3 -- the
question whose answer is B9's entire readout -- is generated from the
edited choice. cmd_submit3 validates nothing at all.

cmd_report does print SEAL BROKEN, so the run is not silently clean. But
by then the comparison has already been asked and answered against a pass
1 that was changed after pass 2 was seen, which is the exact failure the
seal exists to prevent.

One line in cmd_submit2 -- the same `if verify(rid) is False` cmd_prompt2
already carries -- closes it. So does refusing in cmd_submit3.
""".strip())

# ----------------------------------------------------------------- PB_003
head(3, "PB_003", "'prompt withholding' is commitment, not confidentiality")
print("""
The module docstring: "Pass 1 is sealed with a hash before the pass 2
prompt is released. Without the seal a model reconstructs a flattering
version of what it would have thought."

The first sentence is a workflow gate and it works (PB_002, first two
rows). The second names the property that matters, and the seal does buy
it: pass 1 is frozen at a hash before pass 2 is requested, so a later
reconstruction is detectable.

What the seal does not do is withhold information. PROMPT_2 and PROMPT_3
are string constants in frame_sim.py.
""".strip())
print()
print("  PROMPT_2 length: %d chars, defined at module level" % len(FS.PROMPT_2))
print("  PROMPT_3 length: %d chars, defined at module level" % len(FS.PROMPT_3))
print("  both readable by anyone running the tool, before pass 1 is written")
print()
print("""
And the operator is the model. A model that has read the file knows pass 2
will ask it to push on every constraint and to include the option of not
deciding, while it is still writing pass 1.

divergence-playground/seal.py states this limit about itself -- its XOR
obfuscation is "accidental-peek defence, not cryptographic". The same
caveat applies here and is not stated. It does not sink the instrument:
commitment is the property B7 through B9 need. It does mean
"prompt withholding" is the wrong name for what was verified.
""".strip())

# ----------------------------------------------------------------- PB_004
head(4, "PB_004", "option_gain is None for two different things")
rows = []
with sandbox() as d:
    p1p = write(d, "p1.json", P1)
    for rid, p2 in (("A", {"options": [], "choice": ""}),
                    ("B", {"options": [{"id": "x", "desc": "1"},
                                       {"id": "y", "desc": "2"}], "choice": "x"}),
                    ("C", None)):
        quiet(FS.cmd_start, rid, "p")
        quiet(FS.cmd_seal, rid, p1p)
        if p2 is not None:
            quiet(FS.cmd_submit2, rid, write(d, "p2_%s.json" % rid, p2))
        rows.append((rid, FS.readouts(rid)))
    labels = {"A": "wide pass ran, found 0 options",
              "B": "wide pass ran, found 2 (no gain)",
              "C": "wide pass never run"}
    print()
    print("  %-34s %8s %8s" % ("state", "opt2", "gain"))
    print("  " + "-" * 52)
    for rid, r in rows:
        print("  %-34s %8s %8s" % (labels[rid], r["n_options_pass2"], r["option_gain"]))
print()
print("""
    gain = round((n2 - n1) / n1, 3) if (n2 and n1) else None

n2 == 0 is falsy, so a wide pass that returned nothing scores the same as
a wide pass that was never run. Those are opposite results: the first is a
loud finding about the model, the second is an incomplete run.

n_options_pass2 does separate them (0 against None), so the information is
present and the derived readout throws it away -- and option_gain is the
field B7 is stated in.
""".strip())

# ----------------------------------------------------------------- PB_005
head(5, "PB_005", "--submit3 is parsed and not documented, so B9 has no readout")
doc = sorted(set(
    ln.split("--")[1].split()[0]
    for ln in open(os.path.join(HERE, "frame_sim.py"), encoding="utf-8")
    if ln.startswith("#   python3 frame_sim.py --")))
parsed = sorted(set(
    ln.split('add_argument("--')[1].split('"')[0]
    for ln in open(os.path.join(HERE, "frame_sim.py"), encoding="utf-8")
    if 'add_argument("--' in ln))
print()
print("  documented in the header : %s" % ", ".join(doc))
print("  parsed by the CLI        : %s" % ", ".join(parsed))
print("  parsed but undocumented  : %s" % ", ".join(
    sorted(set(parsed) - set(doc) - {"file", "problem", "jsonl"})))
print()
print("""
cmd_submit2 PRINTS prompt 3 and the header gives no command for submitting
its answer. Follow the documented workflow exactly and pass3.json is never
written, so dominated_on_own_metric stays None on every run.

B9 -- "the wide pass finds an option that beats the constrained choice on
the constrained run's own metric" -- is stated entirely in that field. Its
falsifier is "runs where dominated_on_own_metric is consistently false";
under the documented workflow it is consistently None, and None is not
false. One line in the usage block.
""".strip())

# ----------------------------------------------------------------- PB_006
head(6, "PB_006", "B8's readout is elicited by the prompt that measures it")
print("""
B8: "A constrained pass will usually state its option set as complete
rather than as the extent of its search."
Falsified by: "runs where frame_flagged is consistently true."

frame_flagged is p1["incompleteness_acknowledged"], and PROMPT_1 requires
that field in the JSON it asks for:

    "incompleteness_acknowledged": true or false,
    "incompleteness_statement": "if the option set was stated as complete,
       leave empty; if it was stated as only what was generated, say so here"

    The incompleteness field is a readout, not a prompt to hedge. Record
    what the reasoning actually did.

The disclaimer is doing the work the schema undoes. The field is in the
requested output, so the model sees the word "incompleteness" while it is
generating the constrained pass -- it is not reporting on a pass that has
already happened, it is producing both at once.

That makes frame_flagged a self-report from inside the thing being
measured. triad-playground TP_006 is the same shape (three of four
reasoning checks readable only by self-report); reasoning-dial RD_009
names it as the G-STATE gap.

What would read it out without the contamination: drop the field from
PROMPT_1's schema entirely, and have a separate pass -- or a separate
reader -- score the `reasoning` text for whether the option set was
presented as complete. That is a rating on an artifact rather than a
question to the author, and it is the same move frame_sim already makes
for pass 3, which asks about pass 1 rather than asking pass 1.
""".strip())

# ----------------------------------------------------------------- PB_010
head(7, "PB_010", "the seal gate validates every field except B8's")
with sandbox() as d:
    noflag = dict(P1)
    del noflag["incompleteness_acknowledged"]
    p = write(d, "p1_noflag.json", noflag)
    quiet(FS.cmd_start, "N1", "p")
    rc, out = quiet(FS.cmd_seal, "N1", p)
    r = FS.readouts("N1")
    print()
    print("  pass 1 submitted without incompleteness_acknowledged")
    print("  seal            rc=%d  %s" % (rc, out.strip()))
    print("  frame_flagged   %s" % r["frame_flagged"])
    print()
    print("  the fields the gate DOES require, each removed in turn:")
    for missing in ("options", "choice", "metric"):
        rid = "M_" + missing
        quiet(FS.cmd_start, rid, "p")
        broken = {k: v for k, v in P1.items() if k != missing}
        rc, out = quiet(FS.cmd_seal, rid, write(d, "m_%s.json" % missing, broken))
        print("    without %-8s seal rc=%d  %s" % (missing, rc, out.strip()))
print()
print("""
cmd_seal requires options, choice and metric -- the three fields that feed
option_gain and the pass 3 prompt. It does not require
incompleteness_acknowledged, which is the whole of B8. A pass 1 without it
seals clean and reports frame_flagged None.

So the one claim frame_sim can test on a single pass, with no second pass
and no comparison, is the one field the gate lets through missing. Adding
it to the required list is one string.
""".strip())

# ----------------------------------------------------------------- PB_007
head(8, "PB_007", "documented_share merges two of the three states")
asserted = {"case": "all-asserted", "presented_as": "",
            "checks": {i: {"state": "asserted", "answer": "stated", "record": ""}
                       for i in CHECK_IDS}}
absent = {"case": "all-absent", "presented_as": "",
          "checks": {i: {"state": "absent", "answer": "", "record": ""}
                     for i in CHECK_IDS}}
print()
print("  %-14s %5s %6s %8s %14s" % ("case", "doc", "asrt", "absent", "doc_share"))
print("  " + "-" * 52)
for c in (asserted, absent):
    s = BA.score(c)
    print("  %-14s %5d %6d %8d %14.3f" % (
        s["case"], s["documented"], s["asserted"], s["absent"],
        s["documented_share"]))
print()
print("""
The module docstring names three states and reads them as a ladder: "A
binary carried mostly by asserted and absent checks is an unaudited one."
The two are not the same thing. An asserted check is an answer someone can
be held to; an absent one is silence. A framing carried by eleven
assertions is a different object from one carried by eleven silences, and
whoever gave the assertions can be asked for the record.

documented_share is documented/n, so the two return an identical number --
and it is the only field in the score named as a share, which is the one
that gets quoted. The three counts are all returned and the table prints
all three, so nothing is lost at the readout; the loss is in the derived
scalar.

Two of this repo's own mechanisms name it: eleven heterogeneous checks
collapsed to one number is uninstrumented's SCALAR DEMAND, and merging an
ordered pair of states into one denominator is criteria-drift CD_002's
ordinal-compared-as-nominal. A second share -- answered_share, documented
plus asserted over n -- separates them at no cost.
""".strip())

# ----------------------------------------------------------------- PB_008
head(9, "PB_008", "the template fails closed -- recorded because it holds")
s = BA.score(BA.template())
bad = BA.score({"case": "bad", "checks": {CHECK_IDS[0]: {"state": "probably"}}})
print()
print("  blank template          doc=%d asrt=%d absent=%d share=%.3f" % (
    s["documented"], s["asserted"], s["absent"], s["documented_share"]))
print("  case with no checks key doc=%d asrt=%d absent=%d" % tuple(
    BA.score({"case": "empty"})[k] for k in ("documented", "asserted", "absent")))
print("  malformed state value   counted absent, reported as %s" % bad["malformed_states"])
print()
print("""
Every default runs toward absent: the template writes all eleven checks at
"absent", a missing entry reads as absent, and a state value outside the
vocabulary is counted absent AND named in malformed_states rather than
dropped. A blank file scores 0 of 11 and cannot be mistaken for an audited
one.

Worth recording because the same author's other template does not do this:
category-weld's `weld.py --new` ships a placeholder divergence with an
empty id which score() counts, so a blank term file scores 1 on the only
live readout there (CW_012). Two templates, opposite defaults.
""".strip())

# ----------------------------------------------------------------- PB_009
head(10, "PB_009", "B5 is runnable in the folder next door and is not run")
print("""
B5: "'A few' is a category weld -- headcount and functional position score
identically." S2 states the same thing as a check: "Is loss counted by
headcount or by functional position? (weld check: those score identically
under headcount)".

category-weld/ takes exactly this object: a term, a tracked_by_label, a
component list with units, and named divergence cases. There is no
welds/a_few.json.
""".strip())
weldsdir = os.path.join(os.path.dirname(HERE), "category-weld", "welds")
if os.path.isdir(weldsdir):
    print()
    print("  ../category-weld/welds/ holds: %s" % ", ".join(
        sorted(f[:-5] for f in os.listdir(weldsdir) if f.endswith(".json"))))
print()
print("""
Writing it is the cheapest test either folder has available: components
headcount and functional position, tracked_by_label headcount, and the
divergence case is any reduction where the two diverge -- which is what S2
asserts happens. It would also be the first weld term from outside
policy/economics, which is the open question in uninstrumented UNI_002.

Recorded as an unrun test, not as a defect. B5 is stated in a claim table
that says its status is open, which is accurate.
""".strip())

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as PB_001..PB_010")
print(BAR)
