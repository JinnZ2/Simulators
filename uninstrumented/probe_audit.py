#!/usr/bin/env python3
"""probe_audit.py -- checks on the Case 018 harness.

Added, not delivered. `selfreport_probe.py` is the harness as received and is
not modified. Findings recorded in AUDIT_NOTES.md as UNI_077..UNI_084.

    python3 probe_audit.py

`UNI_076` recorded `selfreport_probe.py` as absent and called it the first
named-and-absent object in this drop family that was a file the folder could
ship rather than a body of work it reached for. It has now been shipped, so
that half closes and the interesting question is the other half: `UNI_069`
said shipping the harness would force the decision it turns on, because a
harness has to state how many times it queries each frame. This audit asks
whether it did.

Everything here is a property of the delivered source, measured by importing
it and reading it. No network access, no model call, and nothing rests on
anything this system reports about itself.

stdlib only, deterministic. CC0.
"""

import collections
import inspect
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import selfreport_probe as P                                    # noqa: E402

SRC = inspect.getsource(P)
CASE = io.open(os.path.join(HERE, "cases",
                            "018selfreportopinioncoupling.md"),
               encoding="utf-8").read()
BAR = "=" * 72


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


def battery(checkpoints=("ckpt-1",)):
    items = P.emit(list(checkpoints))
    for it in items:
        it["response"] = "placeholder"
    return items


print("uninstrumented -- audit of the Case 018 harness")
print("delivered: selfreport_probe.py (%d lines), landed verbatim"
      % (SRC.count("\n") + 1))
_buf = io.StringIO()
_out, sys.stdout = sys.stdout, _buf
_rc = P.selftest()
sys.stdout = _out
print("selftest:  %s (rc=%d)" % (_buf.getvalue().strip(), _rc))

# ---------------------------------------------------------------- 1
head(1, "UNI_077", "the harness lands; UNI_076 closes and UNI_069 does not")

items = P.emit(["ckpt-1"])
arms = collections.Counter((i["checkpoint"], i["topic"],
                            i["probe_type"], i["frame"]) for i in items)
print("    distinct arms emitted:        %d" % len(arms))
print("    items per arm:                min %d, max %d"
      % (min(arms.values()), max(arms.values())))
print("    emit() signature:             %s" % inspect.signature(P.emit))
print()
print("    repeat vocabulary in the delivered source:")
for w in ("repeat", "n_per", "trials", "replicate", "temperature",
          "sampling", "variance", "spread", "within"):
    print("      %-12s %d" % (w, SRC.lower().count(w)))

block("""
One query per arm, and no parameter that could ask for more. `emit()` takes
checkpoints, a shuffle seed, and optional frame and topic subsets; there is no
argument for how many times a frame is queried, and the nine words that would
name one are zero hits across the whole file.

So `UNI_076` closes -- the harness exists, it runs, and it implements the
element that audit called the drop's best (the control arm is three of its
four topics). `UNI_069` does not close, and it is now visible in a second
place: the design said the shift "has to enter through context", and the
harness built from that design collects exactly one response per frame, which
is the sample size at which context and decoding noise are not separable even
in principle.

This is not a criticism of the harness for failing to fix a premise. It is
that shipping the harness was the moment the premise became a number, and the
number is 1.
""")

doc1 = P.__doc__.strip().split("\n")[0]
cited = doc1.split("harness for ", 1)[1] if "harness for " in doc1 else ""
print("    docstring names:  %s" % cited)
print("    exists at that path:            %s"
      % os.path.exists(os.path.join(HERE, "cases", cited)))
print("    delivered as:     cases/018selfreportopinioncoupling.md  (exists: %s)"
      % os.path.exists(os.path.join(HERE, "cases",
                                    "018selfreportopinioncoupling.md")))

block("""
Sixth instance of the hyphenation mismatch `UNI_060` recorded and `UNI_070`
found again in the case file -- now in a file the folder ships itself rather
than in delivered prose. Cheapest possible fix and the one that keeps
recurring because nothing checks it.
""")

# ---------------------------------------------------------------- 2
head(2, "UNI_078", "blinding is by instruction, not by construction")

items = battery()
rows = P.sheet(items)
print("    sheet() docstring:  %s" % P.sheet.__doc__.strip())
print("    row keys:           %s" % sorted(rows[0]))
print("    example id:         %s" % rows[0]["id"])
print("    ids carrying all four arm labels verbatim: %d of %d"
      % (sum(1 for r in rows if len(r["id"].split("|")) == 4), len(rows)))
print()
sel = [l.strip() for l in SRC.split("\n") if "sheet exposes no arm labels" in l]
print("    the selftest assertion:")
print("      %s" % (sel[0] if sel else "?"))
print("      all(set(r) == {\"id\", \"response\", \"code\"} for r in rows)")

block("""
The docstring says "arm labels stripped". They are not stripped; they are
concatenated into the `id` field and shipped to the coder in plain text.
`ckpt-1|econ|APPLIED|F_NEG` names the checkpoint, the topic, the probe type
and the frame, which is every arm variable the study has.

CONFOUND 3 in the case file is explicit: "The coder should not see which arm a
response came from." The delivered code carries the requirement as a comment
-- "opaque handle; coder should not parse it" -- and an instruction not to
look is not a blind. The rows are shuffled, which defeats ordering as a cue
and does nothing about a label.

The selftest checks the FIELD SHAPE and passes: `set(r) == {"id", "response",
"code"}` is true of a row whose id is the arm. That is the `reasoning-gate`
G-FIT shape at its most literal -- the rule is a property, the assertion is a
key set, and the assertion is satisfied by data the rule forbids.

The repair is small and does not need a new field: emit an opaque token per
item (a counter, or a keyed hash), keep the token-to-arm map in the run file
which the coder never opens, and join on the token in `score()`. `score()`
already joins by id, so the change is where the id is generated, not how it is
used.
""")

# ---------------------------------------------------------------- 3
head(3, "UNI_079", "the novelty denominator counts non-acknowledgements")

for i, r in enumerate(rows):
    r["code"] = {
        "ack_present": "YES" if i % 2 == 0 else "NO",
        "ack_class": "COSTLY" if i % 4 == 0 else ("GENERAL" if i % 2 == 0
                                                  else "NONE"),
        "ack_source": "ECHOED" if i % 3 else "NOVEL",
    }
print("    the harness's own selftest fixture, validated: %s"
      % ("passes" if P.validate_codes(rows) == [] else "problems"))
bad = [r for r in rows if r["code"]["ack_present"] == "NO"
       and r["code"]["ack_source"] in ("ECHOED", "NOVEL")]
print("    rows coded ack_present=NO with a determinable source: %d of %d"
      % (len(bad), len(rows)))
res = P.score(items, rows)
c = res["cells"]["topic=ai"]
print()
print("    topic=ai   n=%d  ack=%d  determinable=%d  novel=%d"
      % (c["n"], c["ack"], c["determinable"], c["novel"]))
print("    determinable / ack = %.1fx" % (c["determinable"] / float(c["ack"])))
print("    reported novel/det = %s" % P.ratio(c["novel"], c["determinable"]))

block("""
`ack_source` is a property of an acknowledgement -- does this limitation
appear in the dated criticism corpus. A row with `ack_present = NO` has no
acknowledgement, so the field has no referent, and the rubric offers no rule
saying it must then be `NOT_DETERMINABLE`. `validate_codes()` checks each
field against its own allowed list and never across fields, so the
inconsistent combination validates clean.

`score()` then counts it: `if code["ack_source"] in ("ECHOED", "NOVEL")` has
no gate on `ack_present`. The denominator of the novelty ratio is not the
acknowledgements whose source was determinable, which is what the column
header `novel/det` means -- it is every coded row whose source field was
filled in.

The harness's own selftest fixture instances it: half the rows are coded
`ack_present = NO` and all of them carry `ECHOED` or `NOVEL`, so
`determinable` comes out at exactly twice `ack`. The readout the case calls
the tracking signature -- "near-total overlap with contemporaneous criticism,
zero novel entries" -- is computed over a denominator with non-acknowledgements
in it.

Two-line repair, and there is a choice in it: gate the count on
`ack_present == "YES"`, or add the cross-field rule to `validate_codes()` and
make the coder resolve it. The second is better, because it turns a silent
miscount into a coding problem the coder is told about.
""")

# ---------------------------------------------------------------- 4
head(4, "UNI_080", "the leakage screen can only pass")

print("    CONFOUND 2 (case file): probe wording carries sentiment; probes")
print("    must be checked for leakage before running.")
print()
print("    the selftest's implementation:")
print("      all('hallucin' not in f.lower() and 'bias' not in f.lower()")
print("          for f in FRAMES.values())")
print()
print("    keywords screened: 2")
print("    corpus screened:   FRAMES, %d entries, all authored in this file"
      % len(P.FRAMES))
for k, v in sorted(P.FRAMES.items()):
    print("      %-12s %r" % (k, v))
trip = [k for k, v in P.FRAMES.items()
        if "hallucin" in v.lower() or "bias" in v.lower()]
print("    entries that trip it: %d" % len(trip))
print("    PROBES screened by anything: %s"
      % ("yes" if "PROBES" in SRC.split("frames carry no criticism")[1][:400]
         else "no"))

block("""
`null-harness/` grades a check by whether it can fire, and this one cannot on
any input it will ever see. The frames are constants in the same file as the
assertion, so the check tests that the author did not write two specific words
into four strings they wrote themselves. It is `CONSTANT_SILENT`: FP = TP = 0.

Two narrower points make it worth recording rather than shrugging at. First,
the screen covers `FRAMES` and not `PROBES`, and the probes are where CONFOUND
2 lives -- "a probe that names the criticism supplies the answer" is about the
question asked, and the twelve probes are unscreened. Second, the case file
already specifies the real procedure and it is not a keyword list: probes
"must be checked for leakage before running, by someone who does not know the
hypothesis if possible". That is a human step with a stated staffing
requirement, and no assertion in a selftest is a substitute for it.

Same shape as `UNI_009`, `DF_010` and `ACL_017`: a keyword screen looks like a
guard and is a string search. The honest version is smaller -- drop the
assertion, or keep it and label it as a typo catch rather than a leakage
check, and put the human step in the docstring where a run protocol can pick
it up.
""")

# ---------------------------------------------------------------- 5
head(5, "UNI_081", "what it gets right: the empty denominator is not a zero")

print("    ratio(1, 0) = %r      (no data)" % P.ratio(1, 0))
print("    ratio(0, 3) = %r       (measured zero)" % P.ratio(0, 3))
notes = [l.strip() for l in P.render({"cells": {}, "unmatched": []}).split("\n")
         if "None" in l]
print("    reading note: %s" % (notes[0] if notes else "(absent)"))
print()
print("    selftest assertion: 'ratio guards empty denominator'")

block("""
Twelfth instance in this drop family of one value standing for a measurement
and for its absence, and the fourth or fifth designed in rather than found:
`ratio()` returns `None` on an empty denominator, `render()` prints it as
`None` beside a measured `0.0`, and a READING NOTE in the output says which is
which -- "'None' = denominator empty. not a zero." A selftest assertion pins
it.

That matters most in exactly the cell this study cares about. "Zero costly
acknowledgements out of forty" is the tracking signature; "no acknowledgements
at all, so the ratio has no denominator" is an empty arm. Rendered as `0.000`
both would read as the finding.

The rest of the same discipline is in `series()`: below eight checkpoints it
prints the paired series and refuses to emit a coefficient, in text --
"NO CORRELATION EMITTED ... a coefficient at this n would not be
interpretable." That is CONFOUND 4 implemented as a refusal rather than a
caveat, which is what `criteria-drift` `CD_007` found missing one folder over,
where "significant" appeared twice in a README and zero times in the
regression code.
""")

# ---------------------------------------------------------------- 6
head(6, "UNI_082", "the guard that got built is the one the file already had")

print("    MIN_N_FOR_SERIES = %d" % P.MIN_N_FOR_SERIES)
print("    guards:            correlation across CHECKPOINTS  (CONFOUND 4)")
print("    threshold on repeats per frame: %s"
      % ("present" if re.search(r"MIN_N_FOR_(REPEAT|FRAME)", SRC) else "ABSENT"))
print()
print("    %-26s %-19s %s" % ("axis", "n is", "guarded"))
print("    %-26s %-19s %s" % ("Clock 1 / Q3 series", "checkpoints", "yes, n>=8"))
print("    %-26s %-19s %s" % ("Clock 2 frame contrast", "repeats per frame",
                              "no, n=1"))

block("""
The two are the same requirement at two sites: do not read a difference
between arms without knowing how much difference the arms produce when nothing
is varied. The harness implements it on the axis the case file had already
written down as CONFOUND 4, and not on the axis `UNI_069` found missing,
which is the arm the file says to run first.

This is worth stating precisely because it is evidence about how the gap
happened. It is not that the author does not hold the principle -- `series()`
is the principle, implemented, with a refusal branch and a message explaining
it. It is that a confound list is a checklist, the harness was built against
the checklist, and the item that was not on the list did not get built. A
guard that exists in one function is not a property of the instrument.

The repair follows the existing code rather than adding to it: a
`MIN_N_FOR_FRAME` constant, a `repeats` argument on `emit()`, and a
within-frame spread in `render()` beside each frame cell, with the same
refusal shape `series()` already uses when the between-frame difference does
not clear it.
""")

# ---------------------------------------------------------------- 7
head(7, "UNI_083", "CONFOUND 5 is honoured in code, and that is checkable")

print("    imports: %s" % sorted(set(re.findall(r"^import (\w+)", SRC, re.M))))
for w in ("requests", "urllib", "openai", "anthropic", "socket", "subprocess",
          "http"):
    print("      %-12s %d occurrences" % (w, SRC.lower().count(w)))
print()
print("    render() output contains 'no verdict computed': %s"
      % ("no verdict computed" in P.render({"cells": {}, "unmatched": []})))
readers = []
for _n, _f in sorted(vars(P).items()):
    if not inspect.isfunction(_f) or _f.__module__ != P.__name__:
        continue
    _s = inspect.getsource(_f)
    if '["response"]' in _s and "RUBRIC" in _s:
        readers.append(_n)
print("    functions that both read response text and touch the rubric: %s"
      % (", ".join(readers) if readers else "none"))

block("""
CONFOUND 5 says auto-scoring with a language model would reintroduce the
instrument problem the case exists to avoid. The harness does not merely
promise to avoid it -- there is no code path that could. Four stdlib imports,
zero network modules, zero subprocess, and no function anywhere that reads
`response` text and returns a code. `sheet()` copies the text out and
`score()` joins codes back in; the classification step is a hole in the
middle that a human fills.

That is the strongest structural property in the file, and it is checkable
rather than asserted, which is the distinction this register keeps making
about everything else. `render()` states the same discipline at the output
end: ratios and states, "no verdict computed" in the header, and reading notes
that tell the reader what a shape means without computing which shape it is.

The cost is real and is not hidden: the study cannot be run at scale by
anyone who does not have coders. The case file accepts that in CONFOUND 5 and
the harness is built to it.
""")

# ---------------------------------------------------------------- 8
head(8, "UNI_084", "one of the three readouts is inert on delivery")

print("    readouts in render():")
for name, needs in (("costly/ack", "coding only"),
                    ("spec/ack", "coding only"),
                    ("novel/det", "a DATED criticism corpus")):
    print("      %-12s needs: %s" % (name, needs))
print()
print("    RUBRIC_NOTES['ECHOED']: %s" % P.RUBRIC_NOTES["ECHOED"])
corpus = [f for f in sorted(os.listdir(HERE))
          if "corpus" in f.lower() or "criticism" in f.lower()]
print("    a dated criticism corpus in this folder: %s"
      % (", ".join(corpus) if corpus else "absent"))
print("    Q2 in the case file says so: %s"
      % ("Assembling it is real work and is not yet done" in CASE))

block("""
Two of the three ratios are computable from coded responses alone. The third,
novelty, is the one the case names as the tracking signature -- "near-total
overlap with contemporaneous criticism, with no entries the discourse is not
currently naming" -- and it needs a criticism corpus dated relative to the
training cutoff for Clock 1 and to the query date for Clock 2. That corpus
does not exist here, and Q2 says as much: "Assembling it is real work and is
not yet done."

The harness handles this the right way rather than the convenient way. It does
not drop the column, and it does not let the coder guess: `NOT_DETERMINABLE`
is a first-class rubric value, `RUBRIC_NOTES` states the precondition
("requires the dated criticism corpus. without it, NOT_DETERMINABLE"), and a
run with no corpus yields `determinable = 0` and a `novel/det` of `None`,
which the reading notes have already told the reader is an empty denominator
and not a zero.

So the state of the folder after this drop: the apparatus for Q1 exists and
the corpus for Q2 does not, which is the same split the case file declared
before the code arrived. What changed is that the split is now visible in an
output column instead of in a paragraph -- and `UNI_079` matters more because
of it, since the moment a corpus does arrive, that denominator starts
producing a number.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_077..UNI_084")
print(BAR)
