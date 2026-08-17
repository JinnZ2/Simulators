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
import inspect

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
head(1, "PB_001", "the seeded case arrived; the fixtures did not")
print("""
CLAIM_TABLE.md made two statements about artifacts the first drop did not
carry. One has now arrived and one has not.

    "binary_audit.py has one seeded case, a generic framing rather than a
    documented incident, scoring 0 documented of 11."
""".strip("\n"))
print()
cases = BA.load_cases()
for c in cases:
    sc = BA.score(c)
    print("  %-20s documented %d of %d   asserted %d   absent %d   share %.3f" % (
        sc["case"], sc["documented"], sc["n_checks"], sc["asserted"],
        sc["absent"], sc["documented_share"]))
print()
print("""
  ventilator-surge lands and the number is exact: 0 documented of 11, with
  3 asserted and 8 absent. The claim held.

    "frame_sim.py is verified end to end -- seal enforcement, prompt
    withholding and tamper detection all confirmed against synthetic
    fixtures -- and has two real self-runs, R1 and R2."

The fixtures are still not in the drop, and frame_sim.py was not
re-delivered. Sections 2-3 check the three named properties directly, as
before; the runs R1 and R2 are reported in the claim table and their
artifacts are not carried either.

So PB_001 splits. The seeded case: CLOSED, and confirmed to the digit.
The fixtures: still UNVERIFIED, third drop running.
""".strip("\n"))

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
print()
print("  DROP 3 WIDENS THIS. Two new commands, neither verifying:")
print()
print("  %-18s %-18s %s" % ("command", "verify() called", "seal.json checked"))
print("  " + "-" * 58)
for name in ("cmd_prompt2", "cmd_submit2", "cmd_submit3",
             "cmd_flag", "cmd_submit_flag"):
    src = inspect.getsource(getattr(FS, name))
    print("  %-18s %-18s %s" % (
        name, "verify(" in src, "seal.json" in src))
print()
print("""
cmd_prompt2 is still the only command that verifies. cmd_flag and
cmd_submit_flag are new in drop 3 and check neither the seal nor its
integrity, so a pass 1 edited after sealing can be blind-rated and the
rating recorded -- and the blind rating is the readout B8 now rests on.

The ratio of verifying to non-verifying commands went from 1:2 to 1:4
while the repair was being made. Not a new defect; the same one, wider.
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

DROP 3 WIDENS THIS TOO. --flag and --submit-flag are added, parsed, and
also absent from the header, so the undocumented count goes from one to
three -- and two of the three carry the PB_006 repair the same drop made.
The documented workflow now runs start -> seal -> prompt2 -> submit2 ->
report and produces, on every run, dominated_on_own_metric None (B9) and
frame_flagged source `none` (B8). Two of the three claims the instrument
exists to test are unreachable by following its own usage block.
""".strip())

# ----------------------------------------------------------------- PB_006
head(6, "PB_006", "REPAIRED -- the cue is out of the generating context")
print("""
The first pass recorded that B8's readout could not be measured by the
instrument measuring it: PROMPT_1 required `incompleteness_acknowledged`
in the JSON it asked for, so the flag was produced alongside the reasoning
rather than about it. The drop's own CLAIM_TABLE reached the same place
from the protocol-anticipation side and marked B8 NOT TESTED.

Drop 3 repairs it at the source.
""".strip())
print()
print("  'incompleteness' appears in PROMPT_1 : %s" % ("incompleteness" in FS.PROMPT_1))
print("  PROMPT_F exists                      : %s" % hasattr(FS, "PROMPT_F"))
print("  PROMPT_F mentions pass 2             : %s" % ("PASS 2" in FS.PROMPT_F))
print("  PROMPT_F mentions 'frame'            : %s" % ("frame" in FS.PROMPT_F.lower()))
print()
print("""
The field is gone from PROMPT_1 entirely, and a blind post-hoc rater
replaces it: PROMPT_F shows a reader only the pass 1 output -- options,
choice, metric, reasoning -- and asks a neutral question,
`set_stated_as_complete`, with evidence located in the text. It names
neither pass 2 nor the protocol nor the frame. The inversion to
`frame_flagged` is done by code, not by the rater.

frame_flag() then carries provenance instead of a bare boolean:
""".strip())
with sandbox() as d:
    new_p1 = {"options": [{"id": "a", "desc": "A"}, {"id": "b", "desc": "B"}],
              "choice": "a", "metric": "cost",
              "reasoning": "the two available options are A and B"}
    old_p1 = dict(new_p1); old_p1["incompleteness_acknowledged"] = True
    fl = {"set_stated_as_complete": True, "evidence": "\"the two available options\""}
    for rid, p1 in (("BLIND", new_p1), ("LEGACY", old_p1), ("UNRATED", new_p1)):
        quiet(FS.cmd_start, rid, "p")
        quiet(FS.cmd_seal, rid, write(d, "p1_%s.json" % rid, p1))
    quiet(FS.cmd_submit_flag, "BLIND", write(d, "flag.json", fl))
    print()
    print("  %-10s %-8s %-8s %-14s %s" % (
        "run", "value", "source", "valid_for_b8", "report nudges --flag"))
    print("  " + "-" * 66)
    for rid in ("BLIND", "LEGACY", "UNRATED"):
        ff = FS.readouts(rid)["frame_flagged"]
        _, out = quiet(FS.cmd_report, rid)
        print("  %-10s %-8s %-8s %-14s %s" % (
            rid, ff["value"], ff["source"], ff["valid_for_b8"],
            "--flag" in out))
print()
print("""
PB_006 is REPAIRED. B8 is measurable for the first time, and the two
prior runs are correctly re-labelled `cued` rather than silently kept.

ONE THING THE REPAIR LEFT BEHIND, in the last row. cmd_report nudges the
operator to run --flag only when the source is `cued`:

    if not ff["valid_for_b8"] and ff["source"] == "cued":

`cued` is exactly the state the repair eliminated. A run produced under
the new PROMPT_1 has no such field, lands on source `none`, prints
"NOT valid for B8", and is told nothing about how to fix that. The only
runs that get the instruction are the legacy ones the repair was written
to replace.

One condition: source in ("cued", "none").
""".strip())

# ----------------------------------------------------------------- PB_010
head(7, "PB_010", "restated -- the gate now has nothing to require")
print("""
The first pass recorded that cmd_seal required options, choice and metric
-- the three fields feeding option_gain and the pass 3 prompt -- and not
`incompleteness_acknowledged`, the whole of B8. Over-elicited by the
prompt, under-required by the gate.

The repair removes the field from PROMPT_1, so half the finding dissolves:
there is no longer a B8 field for the gate to require, and requiring one
would now be wrong.

What replaces it is a question about the blind rating, and the answer is
that nothing requires it either:
""".strip())
with sandbox() as d:
    p1 = {"options": [{"id": "a", "desc": "A"}], "choice": "a",
          "metric": "cost", "reasoning": "r"}
    quiet(FS.cmd_start, "G1", "p")
    rc, out = quiet(FS.cmd_seal, "G1", write(d, "p1.json", p1))
    r = FS.readouts("G1")
    print()
    print("  seal a pass 1 with no blind rating   rc=%d  %s" % (rc, out.strip()))
    print("  frame_flagged                        %s" % r["frame_flagged"])
    print("  report-all lists the run             %s" % (
        quiet(FS.cmd_report_all, False)[1].count("G1") > 0))
print()
print("""
That is the right design, not a defect: the blind rating happens AFTER
sealing by construction, so the seal gate cannot require it. The readout
carries `valid_for_b8: False` and says so, which is the honest handling.

The residue is PB_014's: an unrated run says it is invalid and does not
say what to do about it.
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

# ----------------------------------------------------------------- PB_011
head(11, "PB_011", "three copies of this file arrived; two were stale")
print("""
The drop carried binary_audit.py three times: twice as uploaded files and
once pasted inline. The two uploaded files are byte-identical to each
other AND to the version already in the repo -- the one WITHOUT the
handoff router. The inline paste is the live version.

    uploaded copy A  vs  uploaded copy B     identical
    uploaded copy A  vs  repo (pre-handoff)  identical
    inline paste                             adds HANDOFF_CEILING,
                                             handoff(), the O1 `count`
                                             template field, the score()
                                             key and the detail() block

measurement-fork MF_019 recorded the rule: files that live in one place do
not drift, files bundled into every drop do. This is the first drop where
the drift had a consequence -- landing the uploaded files at face value
would have reverted the router the same drop introduced.

capital.json also arrived for the third time, byte-identical again. That
one is inert; this one was not.
""".strip())

# ----------------------------------------------------------------- PB_012
head(12, "PB_012", "the router's null collides a measurement with a gap")
print()
print("  %-44s %s" % ("O1 state", "handoff"))
print("  " + "-" * 74)
for label, st, count in [
    ("documented, count 2 -- the signature", "documented", 2),
    ("documented, count 1", "documented", 1),
    ("documented, count 7 -- checked, does not match", "documented", 7),
    ("documented, count not stated", "documented", None),
    ("asserted", "asserted", None),
    ("absent -- never checked", "absent", None),
]:
    ch = {i: {"state": "absent", "answer": "", "record": ""} for i in CHECK_IDS}
    ch["O1"] = {"state": st, "answer": "", "record": ""}
    if count is not None:
        ch["O1"]["count"] = count
    h = BA.score({"case": "probe", "checks": ch})["handoff"]
    if h is None:
        shown = "None"
    elif h.get("route"):
        shown = "-> %s (count %s)" % (h["route"], h["count"])
    else:
        shown = "not routed: %s" % h["reason"]
    print("  %-44s %s" % (label, shown))
print()
print("""
Row 3 and row 6 return the same value. "O1 documented at 7" is a
measurement -- the count was recorded and does not carry the mechanism-10
signature. "O1 absent" is a gap -- nobody established a count. Both are
bare None, so a caller cannot tell a negative result from an unasked
question.

The vocabulary for the distinction already exists one row up. Row 4
returns {"route": None, "reason": "O1 documented but count not stated"},
which is exactly the right shape, and detail() already renders it as
"HANDOFF not routed: <reason>". Routing the count>ceiling case through
that same branch is two lines and needs no new concept.

This is the fourth instance of the shape in four folders: option_gain
(PB_004), R3's absent (generation-capacity GC_004), and the two here.
""".strip())

# ----------------------------------------------------------------- PB_013
head(13, "PB_013", "the router ships with no case that fires it")
print()
for c in BA.load_cases():
    o1 = (c.get("checks") or {}).get("O1") or {}
    print("  %-20s O1 state %-12s count %-6s handoff %s" % (
        c.get("case"), o1.get("state"), o1.get("count"),
        BA.score(c)["handoff"]))
print()
print("""
ventilator-surge has O1 absent -- the framing supplies two options and
never states a generated count, which its own record field says plainly:
"option count never stated; the framing supplies two and stops."

So the handoff's firing branch is exercised by no case in the repo. It is
not a defect: the router is correct to refuse, and refusing on the one
delivered case is the honest outcome, because a framing that never states
a count is not evidence of a low one. The gap is that the branch which
carries the whole handoff has no worked instance -- the same state
generation-capacity's own R1 is in.

What would close it: a case whose O1 is documented WITH a count. The
generation-capacity README's worked instance is written for exactly that
-- someone asked how many alternatives were generated, answering two,
truthfully -- and the case file for it (food-knowledge) is named in G2's
status and is not in the drop.
""".strip())


# ----------------------------------------------------------------- PB_014
head(14, "PB_014", "the repair's own next step has no prompt")
print("""
Collecting the three states in one place, because the shape only shows
when they sit together:

  source   how a run gets there                       report says
  blind    --flag then --submit-flag were run         valid, value usable
  cued     pass 1 carried the OLD prompt's field      invalid + RUN --flag
  none     pass 1 followed the NEW prompt, unrated    invalid, and nothing

The middle row is the legacy path. The bottom row is what every future run
lands on, because the repair removed the field that produces `cued`.

So the instruction to take the one step that makes B8 measurable is
attached to the state the repair abolished, and withheld from the state
the repair creates. An operator following the documented workflow gets a
report saying NOT valid for B8 with no indication that --flag exists --
and --flag is not in the usage block either (PB_005).

Two one-line changes, in different files: add the two commands to the
header, and widen the nudge condition to source in ("cued", "none").

This is not the repair failing. The repair is correct and PB_006 closes on
it. It is the second-order cost of a correct repair: the reminder to do
the replacement step was written for the population being replaced.
""".strip())

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as PB_001..PB_014")
print(BAR)
