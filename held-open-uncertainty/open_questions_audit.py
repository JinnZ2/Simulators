#!/usr/bin/env python3
"""open_questions_audit.py -- checks on OPEN_QUESTIONS.md.

Added, not delivered. OPEN_QUESTIONS.md is the drop as received and is not
modified. Findings are recorded in AUDIT_NOTES.md as HO_001..HO_006.

    python3 open_questions_audit.py

The drop is one prose file. It is a question list, not a claim table: nine
entries, each with a declared state, and several flagged as the model's
inference rather than the author's position. Every check here is against
the repo tree or against the file's own internal consistency. Nothing here
resolves a question the file holds open.

stdlib only, deterministic. CC0.
"""

import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BAR = "=" * 70

DOC = io.open(os.path.join(HERE, "OPEN_QUESTIONS.md"), encoding="utf-8").read()


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


def sections():
    out = {}
    cur = None
    for line in DOC.splitlines():
        m = re.match(r"^## (Q\d) — (.*)$", line)
        if m:
            cur = m.group(1)
            out[cur] = {"title": m.group(2), "lines": []}
        elif cur:
            out[cur]["lines"].append(line)
    return out


S = sections()

print("held-open-uncertainty -- audit of OPEN_QUESTIONS.md")
print("delivered: OPEN_QUESTIONS.md")
print("not delivered: any instrument, any run, any claim table")
print("sections: %d" % len(S))

# ---------------------------------------------------------------- HO_001

head(1, "HO_001", "provenance is separated per entry, and it costs the author")
rows = []
for q in sorted(S):
    body = "\n".join(S[q]["lines"])
    m = re.search(r"\*\*State: (.*?)\*\*", body, re.S)
    state = " ".join(m.group(1).split()) if m else "(none)"
    who = ("Claude" if "Claude's" in body or "Claude asserted" in body
           else "user" if "user's position" in body
           else "-")
    rows.append((q, who, state[:52]))
print()
print("  %-4s %-8s %s" % ("q", "whose", "declared state"))
print("  " + "-" * 66)
for r in rows:
    print("  %-4s %-8s %s" % r)
block("""
Every entry declares a state before it argues, and three declare whose
position it is. Two are marked the user's, one is marked Claude's -- and
that one carries the harder line:

    Status: no study located. Claude asserted this earlier in
    conversation with more confidence than it had earned.

That is a retraction inside the artifact that carries the claim, in the
entry the claim lives in, rather than as a note elsewhere. Q2 does the
same thing more quietly: its reading is flagged as inference and then
graded -- "Absence of the question is weak evidence for the structural
argument -- and it is absence, not a result."

`uninstrumented` UNI_005 is the rule being followed: a reached-but-badly
quantity has a blindness map, an excluded one does not, and absence is not
a reading. Here the author applies it to their own file's strongest
rhetorical move -- the fact that nobody asks the question -- and downgrades
it.
""")

# ---------------------------------------------------------------- HO_002

head(2, "HO_002", "Q4 and Q5 are runnable here, on apparatus already in the tree")
probe = os.path.join(ROOT, "voice-attractor-probe", "voice_attractor_probe.py")
src = io.open(probe, encoding="utf-8").read()
have = [(n, ("%s" % n) in src) for n in
        ("NEUTRAL_TASKS", "JITTER", "call_model_stub", "run_probe_session",
         "def extract")]
print()
print("  voice-attractor-probe/voice_attractor_probe.py")
for n, ok in have:
    print("    %-20s %s" % (n, ok))
block("""
Q4 asks for: one shape presented at a stated confidence with an explicit
action queue attached, the number varied and nothing else, and a count of
whether the response supplies a resolution. Q5 adds a second count on the
same runs -- does the named unrouted item survive in the response.

That is the `voice-attractor-probe` skeleton with a different perturbation
axis. The folder already holds a task list held constant, a jitter list
that varies what should not matter, a feature extractor that counts a
property of the response text, and a pluggable adapter with a stub so the
pipeline runs with no model attached. Swapping JITTER for a stated-
confidence ladder and FEATURES for resolution-supplied / queue-survived is
a new probe file, not a new harness.

The design also passes the check the harness exists to enforce. Q4 varies
only the number, so the high-confidence arm is the control, and Q5's queue
count has a reachable both-ways outcome -- which is what keeps it off
`null-harness`'s CONSTANT_SILENT. Q4's stated prediction is the sharper
half: resolution-supplying rises as the number falls EVEN WHEN the queue
is fully specified in the input. That conditional is what separates "the
model is answering an underspecified request" from "the number is being
read as a state of the person", and it is stated before any run.

What the file does not say is which model, how many repetitions, or what
counts as supplying a resolution. The last is the same problem Q3 names
about itself -- "requires a construction definition first, which is the
hard part and is not specified" -- and it applies to Q4 and Q5 too.
""")

# ---------------------------------------------------------------- HO_003

head(3, "HO_003", "Q8 is already implemented one folder over")
block("""
Q8's resolution:

    Action is taken on the strongest decision points against the most
    stable anchors, while the unknowns are held open as a separate
    readout. Two registers running simultaneously -- which is the same
    structure as reporting a confidence gradient and a comfort threshold
    independently rather than resolving them into one number.

`domain-ledger/ledger.py` returns four ratios and deliberately does not
combine them, printing each column's denominator underneath.
`domain-ledger/anchor.py` goes further and its selftest asserts the
refusal by name -- "no composite emitted". DL_001 and DL_010 recorded that
as the one scorer in the family that declines the single-headline-number
reduction.

So Q8 is not a proposal in this repo. It is the architecture two shipped
modules already have, described from the operating side rather than the
assessment side. That is worth stating because it changes what Q8 needs:
not an implementation, but a case where the one-register reading and the
two-register reading give different answers on the same material.

Q8's closing line supplies the shape of one -- "the confidence map and the
operating procedure are one document" -- and no document in the repo is
both. `constraint-assembly`'s grade-stop is an operating record with no
confidence readout; `domain-ledger`'s shapes are confidence readouts with
no procedure.
""")

# ---------------------------------------------------------------- HO_004

head(4, "HO_004", "Q6's routing claim, checked against what landed")
block("""
Q6 says of itself: "Now partly routed -- see Q7. Module at
`../constraint-assembly/`."

`partly` is doing real work and is accurate. The module records the
operation -- classes, components, rejections with grounds, a fail-closed
composition test -- and it does not measure the thing Q6 says is unasked.
Q6's claim is that nobody measures GENERATION of a composite from parts
held across unrelated domains under a fixed budget. A case file records
that a generation happened, as recalled afterward by the party who did it.

The module's own README says the same thing in stronger terms and puts it
last: recognition-primed selection and genuine construction look identical
in a single-instance retrospective record, and no case in the folder
establishes the difference (CA_013).

So the honest reading of the route is: Q6 has a place to put cases and a
vocabulary to write them in, and the measurement it names remains
unbuilt. Q6 says "partly routed" rather than "routed", which is the
correct word, and it is the third consecutive folder in this family to get
its own status word right.
""")

# ---------------------------------------------------------------- HO_005

head(5, "HO_005", "the literature entries are unverifiable as delivered")
cites = re.findall(r"(Ellsberg|recognition-primed|naturalistic|calibration|"
                   r"semantic-similarity|token-level entropy)", DOC)
print()
print("  named literatures      : %d mentions" % len(cites))
print("  citations, links, DOIs : %d" % len(re.findall(r"https?://|doi:|\[\d+\]", DOC)))
print("  named authors          : Ellsberg")
block("""
Q1 and Q2 are the two entries that carry the file's empirical weight --
Q1 states the human side IS measured and runs against the assumption, Q2
states the model side is not. Both describe literatures in enough detail
to be checked (recognition-primed decision work on operators under time
pressure; token-level entropy, semantic-similarity methods, self-verbalised
confidence, calibration, faithful hedging) and neither carries a citation.

This is the same status as ANC_010, CD_009 and RD_015, and it is recorded
the same way: UNVERIFIED is a gap, not a negative verdict. Nothing else in
this audit rests on a literature fact.

Q1's distinction is the part worth preserving whatever the sourcing turns
out to be, because it is a claim about two literatures being different
questions rather than about either one's result:

    ambiguity aversion measures preference between known and unknown
    probabilities in gambles. It does not measure whether holding a
    variable open impedes acting.

And the gap it names -- whether ambiguity-aversion results get cited as
evidence about action capacity -- is a citation-tracing question, which is
the one question in the file answerable with no new instrument and no
model access at all.
""")

# ---------------------------------------------------------------- HO_006

head(6, "HO_006", "the file's own subject is a thing it can be checked against")
q5 = "\n".join(S["Q5"]["lines"])
dmg = re.search(r"Damage case:(.*?)\n\n", q5, re.S)
print()
print("  Q5 names the damage case:")
print("    %s" % " ".join(dmg.group(1).split()))
# an entry counts as holding a queue item if it names something unbuilt,
# unrun, unmeasured or unspecified in its own declared state or body.
UNBUILT = ("unmeasured", "not specified", "no study located", "not taken",
           "unbuilt", "not yet searched", "unasked", "Route:", "not closed")
q_open = [q for q in sorted(S)
          if any(w.lower() in "\n".join(S[q]["lines"]).lower() for w in UNBUILT)]
print("  entries naming an unbuilt instrument or an unrun search: %d of %d"
      % (len(q_open), len(S)))
print("    %s" % ", ".join(q_open))
block("""
Q5's damage case is that a model reads a held-open shape as a request for
resolution, supplies one, and deletes the queue.

This file is a held-open shape with an explicit queue: nine entries, six
of them declaring an unbuilt instrument or an unrun search (counted
above). So the drop is
self-testing in a narrow and checkable way -- whether a response to it
supplies resolutions or preserves the queue is observable on this artifact
without building anything.

Recorded because it is a real property of the drop and not because it
settles Q5. It does not: n=1, no control arm, and the reader knows what is
being measured, which is exactly the condition Q4's design avoids by
varying only the number. `triad-playground` TP_004 is the same failure --
an experiment whose subject can see the manipulation measures compliance
with it.

What this artifact CAN supply is the material for the real run. Q4 needs a
shape at a stated confidence with an action queue attached, and
`domain-ledger/shapes/hierarchy-cut-generation.json` is one: asserted
coverage 0.61, thirty domains, zero read, and the unread list IS the
queue. The number is already in the file and varying it is an edit.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as HO_001..HO_006")
print(BAR)
