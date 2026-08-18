#!/usr/bin/env python3
"""drop_016_017_audit.py -- checks on the 016/017 drop.

Added, not delivered. Everything under `cases/016*`, `cases/017*`,
`AVENUES.md` and `specimens/` is as received and is not modified.
Findings recorded in AUDIT_NOTES.md as UNI_059..UNI_068.

    python3 drop_016_017_audit.py

Eight files arrived together and they are four different kinds of thing:
two register entries (016, 017), one instrument list (AVENUES.md), three
specimen files (README + two readings), and two JSON artifacts authored by
one of the systems the specimens are readings of. The last group is new to
this register and changes what can be checked, because the specimens were
readings of text the reader did not have.

LITERATURE CHECK. Section 1 was run against the open web on 2026-08-18 and
is marked. Everything else is computed from the delivered files and the
repo tree, and reproduces by running this script.

stdlib only, deterministic. CC0.
"""

import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BAR = "=" * 72


def read(p):
    return io.open(os.path.join(HERE, p), encoding="utf-8").read()


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


C016 = read("cases/016agreementasmode.md")
C017 = read("cases/017weldedobservables.md")
AV = read("AVENUES.md")
SPEC = read("specimens/README.md")
SA = read("specimens/20260818modelA.md")
SB = read("specimens/20260818modelB.md")
PROTO = json.loads(read("specimens/BNRAM_TEST_PROTO_001.json"))
FLOG = json.loads(read("specimens/BNRAM_FIELD_LOG_001.json"))

print("uninstrumented -- audit of the 016/017 drop")
print("delivered: 2 register entries, AVENUES.md, 3 specimen files,")
print("           2 JSON artifacts authored by a specimened system")

# ---------------------------------------------------------------- UNI_059

head(1, "UNI_059", "017's occasion is the most precisely verified in this family  [web]")
print()
for claim, status, note in (
    ("STAR Collaboration, 'Tracking the baryon number with nuclear "
     "collisions', Science 2026", "CONFIRMED", "published 13 Aug 2026"),
    ("doi 10.1126/science.ads5962", "CONFIRMED", "resolves"),
    ("arXiv:2408.15441", "CONFIRMED", "resolves to the same paper"),
    ("HEPData record 154708", "CONFIRMED", "resolves"),
    ("junction = Y-shaped non-perturbative gluon topology", "CONFIRMED",
     "'a non-perturbative Y-shaped topology of neutral gluons'"),
    ("isobar collisions, matched mass number differing in charge",
     "CONFIRMED", "measurements of B over charge-number difference in "
                  "isobar collisions"),
    ("larger B/dQ ratio, less asymmetric net-proton yield than "
     "valence-quark models predict", "CONFIRMED",
     "reported in those words"),
    ("the collaboration's word is 'disfavor', not overturn", "CONFIRMED",
     "'disfavor the valence quark picture'"),
    ("roughly three decades on the record", "CONSISTENT",
     "1996 (Kharzeev, junction as carrier) to 2026 = 30 years; coverage "
     "also runs the 1970s topology proposal as '50 years', and the entry "
     "counts from the specific 1996 proposal, which is the right one"),
):
    print("  %-11s %s" % (status, claim))
    for i in range(0, len(note), 58):
        print("              %s" % note[i:i + 58])
block("""
Eight elements, eight confirmed, including the two that are easiest to
inflate: the result phrasing and the collaboration's own hedge.

The entry does not inflate either. It quotes `disfavor`, carries the
Science Perspective's caveat that the measurements "do not provide a
direct, tightly controlled measurement of the underlying mechanism", and
states outright: "Nothing here requires the junction picture to be
correct -- the case is about the thirty years during which the question
was not answerable, and what ended that."

That last sentence is what makes the occasion usable. The mechanism claim
is about the interval and the decoupling, not about which member of the
pair wins, so a later reversal of the physics leaves the case standing --
which the entry's own falsifier says in as many words.
""")

# ---------------------------------------------------------------- UNI_060

head(2, "UNI_060", "every internal filename reference misses the delivered filename")
print()
refs = sorted(set(re.findall(r"[0-9]{3}-[a-z-]+\.md|2026-08-18-model-[AB]\.md",
                             C016 + C017 + AV + SPEC)))
delivered = {
    "016-agreement-as-mode.md": "cases/016agreementasmode.md",
    "017-welded-observables.md": "cases/017weldedobservables.md",
    "2026-08-18-model-A.md": "specimens/20260818modelA.md",
    "2026-08-18-model-B.md": "specimens/20260818modelB.md",
}
print("  %-30s %-34s %s" % ("referenced as", "delivered as", "resolves"))
print("  " + "-" * 76)
for r in refs:
    d = delivered.get(r, "?")
    print("  %-30s %-34s %s" % (r, d, os.path.exists(os.path.join(HERE, d))))
print("  %-30s %-34s %s" % ("specimens/README.md", "specimens/README.md",
                            os.path.exists(os.path.join(HERE, "specimens",
                                                        "README.md"))))
block("""
Four of five references do not resolve, and the one that does resolves
only because the upload arrived as `README_35.md` -- a transport artifact
nobody would choose -- and was landed at the name the documents use.

That last point decides the naming question rather than leaving it open.
The upload layer is demonstrably lossy on at least one filename, so it is
not authoritative; the documents' own cross-references are authored. But
the case files 010-015 were landed at their upload names last drop, on the
author's evident intent, and 015 has just been re-delivered at exactly the
name that convention produced. So the two signals disagree and both have
standing.

Landed at the delivered names, for consistency with the six case files
already sitting beside them, and the mismatch is recorded here rather
than repaired by rewriting delivered text. The repair is one line in
whichever direction the author prefers: rename four files, or edit five
references.

Worth stating plainly because this set is unusually interlinked -- 016
borrows 017's design, AVENUES indexes both, and both specimens are cited
by number from three files. The references ARE the navigation, and four
of five of them currently land nowhere.
""")

# ---------------------------------------------------------------- UNI_061

head(3, "UNI_061", "the specimens README's first rule is false of its own files")
print()
rule = SPEC.split("1. **Authorship.**", 1)[1].split("\n2.", 1)[0]
print("  rule 1, as written:")
for line in [l.strip() for l in rule.splitlines() if l.strip()]:
    print("    %s" % line)
print()
for name, txt in (("20260818modelA.md", SA), ("20260818modelB.md", SB)):
    hdr = txt.split("---", 1)[0]
    body = txt.split("---", 1)[1] if "---" in txt else ""
    readings = len(re.findall(r"^## R\d", txt, re.M))
    print("  %-22s readings: %d   raw output pasted in: %s"
          % (name, readings, "Raw text:" in hdr and "held by maintainer"
             not in hdr))
block("""
Rule 1 says: "Nothing in these files is authored by the repository
maintainer. These are outputs from other systems, pasted in."

Neither specimen file contains a pasted output. Both headers say so
explicitly -- "Raw text: held by maintainer; attach alongside this file"
-- and the body of each is readings, seven in one and six in the other.
Readings are analysis. They are the most maintainer-authored content in
the folder.

So the rule states the opposite of the files' actual composition, and it
is the first of five rules, which is where a reader takes the frame from.

The rule that IS doing the work is stated three lines later and is the
right one: "Specimens are not measurements. They are the occasion for
designing one. Nothing in `016` rests on a specimen." That is the claim
rule 1 is reaching for -- no authority flows from a specimen -- and it
survives intact whoever wrote the readings.

Repair is a sentence: the OUTPUTS are not maintainer-authored; the
readings are, and describe operations present in text held elsewhere.
""")

# ---------------------------------------------------------------- UNI_062

head(4, "UNI_062", "the attachment arrives, and discloses that it is not raw")
print()
print("  BNRAM_FIELD_LOG_001.json provenance:")
for k, v in FLOG["provenance"].items():
    print("    %-32s %s" % (k, str(v)[:60]))
block("""
Both specimen headers ask for the raw text to be attached alongside. Two
JSON files now arrive with the drop, which is that attachment -- and
neither is raw output.

`BNRAM_TEST_PROTO_001.json` is authored "JinnZ2 + Kimi (Moonshot AI)" and
is very likely the object Specimen B reads (see UNI_063). It is a
co-authored artifact, not a model output.

`BNRAM_FIELD_LOG_001.json` says in a machine-readable field that it was
compiled by one of the two systems under test, AFTER correction, with
three corrections applied before logging. It is a downstream account of
both encounters written by a participant in one of them.

That is not a defect, and the reason is the specimens README's own rule
3: "Contamination is recorded, not cleaned." This file records its
cleaning -- `corrections_applied_before_logging` is a list, in the file,
naming what was applied. It discloses in a field what the prose specimens
disclose in a header, and it is the better of the two forms because a
field can be read without being interpreted.

What is still missing is the thing both headers actually ask for: the raw
DeepSeek and Kimi output. Neither JSON is it. A reader wanting to check
Specimen A's seven readings still cannot.
""")

# ---------------------------------------------------------------- UNI_063

head(5, "UNI_063", "Specimen B's readings, checked against the source it read")
print()
rows = []
rows.append(("R1 circular categories", "CONFIRMED",
             "proto scores %s; those are defined in the field log's "
             "exclusion_registry, compiled by '%s'"
             % (", ".join(sorted(PROTO["scoring_rubric"])),
                FLOG["provenance"]["log_compiler"])))
tested = [m["model_id"] for m in PROTO["test_subjects"]["models"]
          if m["already_tested"]]
rows.append(("R2 n=2", "CONFIRMED",
             "already_tested true for exactly %s; field log states n=%d"
             % (" and ".join(tested), FLOG["cross_model_analysis"]["n"])))
rows.append(("R3 no baseline", "CONFIRMED",
             "all %d stimulus variants are subsets of the SAME repository; "
             "no comparison repository appears anywhere in the file"
             % len(PROTO["stimulus_variants"]["variants"])))
rows.append(("R4 no pre-registered scoring", "OVERSTATES",
             "a scoring_rubric exists with detection methods and 0-3 "
             "severity per EXC, and phase_5 proposes independent raters on "
             "a random 20%. What is missing is blinding, not criteria"))
stimf = [v["content"] for v in PROTO["stimulus_variants"]["variants"]
         if v["variant_id"] == "STIM-F"][0]
rows.append(("R5 compliance without control", "CONFIRMED",
             "STIM-F is '%s' -- differs from STIM-A by CONTENT, and no "
             "content-free re-prompt arm exists" % stimf))
for name, verdict, why in rows:
    print("  %-30s %s" % (name, verdict))
    for i in range(0, len(why), 60):
        print("      %s" % why[i:i + 60])
block("""
Four of five confirmed against the primary source, one overstated.

This is the check the drop made possible. Specimen B was a reading of a
document the reader did not have; attaching it turns five assertions into
five verifiable ones, and one of them does not survive. That is the
specimens directory earning its own rule 4 -- specimens are the occasion
for designing a measurement, and here the measurement is the diff between
the reading and the source.

**R4, precisely.** Specimen B says the plan "specifies no criteria and no
scorer." It specifies both: four detection methods per EXC and a
four-level severity scale, plus a named ground-truth rater and a
cross-validation phase. The criticism that survives is narrower and still
real -- scoring is unblinded and performed by the operator who states the
expected result, and `principles[2]` makes that explicit rather than
hiding it. "Post-hoc scoring by the party who expects the result is not
measurement" is the sentence that holds; "specifies no criteria and no
scorer" is not.

`AVENUES.md` A3 carries R4 forward as "Pre-registered scoring, as A1",
which is the correct requirement and does not repeat the overstatement.
The error is in the specimen and not in the instrument derived from it.
""")

# ---------------------------------------------------------------- UNI_064

head(6, "UNI_064", "a definitional gap in the protocol, and a disclosure")
print()
print("  principle 1 :", PROTO["principles"][0])
print()
print("  model notes, as written:")
for m in PROTO["test_subjects"]["models"]:
    if not m["already_tested"]:
        print("    %-20s %s" % (m["model_id"], m["notes"][:52]))
print()
print("  EXC-16 detection includes:")
print("    %s" % PROTO["scoring_rubric"]["EXC-16"]["detection_methods"][3])
block("""
Principle 1 makes model identity, provider reputation and release date
null-weight. The `notes` fields generate directional hypotheses from
training regime and provider -- Constitutional AI, RLHF-heavy,
open-weights with less RLHF filtering.

Those are technical properties, not reputation, so this is not a
contradiction and should not be reported as one. What it is: the protocol
defines a failure mode about provider-linked signals -- EXC-16's fourth
detection method is "references provider reputation or training data size
as implicit validity signal" -- and then uses provider-linked training
regime to set its own priors, without stating where the line falls
between the two.

That line is real and thin, and the protocol needs it because it is the
protocol's own subject. A rater applying EXC-16 to an output that says
"this model is RLHF-heavy so expect schema-forcing" has no rule telling
them whether that scores 0 or 3.

DISCLOSURE, since this audit is written by a model. `CLAUDE-3.5-SONNET`
appears in the test matrix with the note "tests whether Constitutional AI
training reduces EXC-15 narrativization". Nothing in this file's findings
depends on that row, and the finding above holds identically with it
removed -- the same gap is visible from the GPT-4o and Llama rows. It is
recorded because a reader should not have to discover it.
""")

# ---------------------------------------------------------------- UNI_065

head(7, "UNI_065", "016's Q1 design, and the confound it names before running")
print()
wm = C016.split("## WOULD MEASURE", 1)[1].split("## CONFIDENCE", 1)[0]
kw = wm.split("**Known weakness, disclosed:**", 1)[1].split("\n\n", 1)[0]
print("  the disclosed weakness, verbatim:")
for i, line in enumerate(" ".join(kw.split()).split(". ")):
    print("    %s%s" % (line, "." if i < 3 else ""))
block("""
The design holds form, pressure, position and specificity constant and
varies only whether the named operation is actually present in the prior
output. Three pre-registered states, no verdict computed by the harness.
Equal rates mean concession tracks pressure; a gap is the readout.

What lifts it above the other WOULD MEASURE blocks in this register is
the paragraph above: it names a specific alternative explanation for a
positive result -- the model constructs a reading of its own prior output
under which the FALSE correction is true -- says that is a different
failure from pressure-tracking, states what would separate them (a third
state plus a manual read of the justification text), and marks it
untested.

That is an alternative explanation for the finding the design is built to
produce, registered before any run. Compare `photoperiod-claim-harness`,
which registers predictions before runs; this registers the way the
prediction could be right for the wrong reason. First instance in this
register.

`AVENUES.md` A1 carries it forward without softening it, and adds the
three things the design needs before it returns anything: pre-registered
scoring, blind scoring of arm, order counterbalancing.
""")

# ---------------------------------------------------------------- UNI_066

head(8, "UNI_066", "the absent artifact reaches a third drop; one name misses")
print()
for name, cited_in in (
    ("tool-off-metrology", ["011rebuildabandonmentcycles.md",
                            "014offloadingevolutionaryframing.md",
                            "cases/016agreementasmode.md"]),
):
    print("  %-24s exists: %s" % (name, os.path.isdir(os.path.join(ROOT, name))))
    for c in cited_in:
        print("      cited in %s" % c)
print()
print("  %-24s exists: %s" % ("moral-claim-decomposer",
                              os.path.isdir(os.path.join(ROOT,
                                                         "moral-claim-decomposer"))))
print("  %-24s exists: %s" % ("moral-decomposer",
                              os.path.isdir(os.path.join(ROOT,
                                                         "moral-decomposer"))))
block("""
`tool-off-metrology` is now cited by three drops. `UNI_043` recorded two
and called it load-bearing; at three it is the most-cited absent object in
the repo, and 016 Q3 states its problem in the most general form yet
reached:

    the quantity of interest is unaided reasoning, and the environment
    that would measure it is the environment that supplies the aid

A different kind of miss in 017 Q4: `moral-claim-decomposer` does not
exist and `moral-decomposer` does. That is a name mismatch rather than an
absent artifact -- the folder is there, the link points one word off, and
the described work ("the optionality cut") is a fair summary of what
`moral-decomposer` does. Cheapest fix in the drop.
""")

# ---------------------------------------------------------------- UNI_067

head(9, "UNI_067", "016 and 017 are instruments for each other")
print()
print("  016 WOULD MEASURE opens:")
print("    %s" % " ".join(C016.split("**Matched-pair correction protocol.**",
                                     1)[1].split("\n\n", 1)[0].split())[:64])
print()
print("  017 Q4 asks:")
q4 = C017.split("### Q4 — Language-layer weld", 1)[1].split("###", 1)[0]
print("    %s" % " ".join(q4.split())[:64])
print("    %s" % " ".join(q4.split())[64:132])
block("""
017 supplies 016's decoupling design, by name -- "Borrowed from the isobar
design in 017". And 017 Q4 asks whether the language-layer weld is the
same operation or a metaphor sharing a word, with the test stated as:
does the matched-pair design have a linguistic analogue that actually
separates two fused concepts, or does the analogy fail at the point where
you would need a matched pair.

016's A1 is that analogue, constructed. So the pair partially answers its
own cross-question by existing: a matched-pair decoupling design WAS
constructible for a language-layer weld, and the point where it would
have failed -- finding two corrections matched on form, pressure,
position and specificity, differing only in correctness -- is exactly
where 016 does its work.

What remains open is the half that needs data. Constructible is not
working; whether the design separates the two concessions is A1's
readout, and no reading has been taken. Stated so the partial answer is
not read as the whole one.

First time in this register that two entries are instruments for each
other rather than cross-references.
""")

# ---------------------------------------------------------------- UNI_068

head(10, "UNI_068", "second re-delivery check, and the offered name arrives")
print()
print("  015definitionalprecedence.md   re-delivered, identical to the")
print("                                 landed case-015.md")
print("  MECHANISM_11.md                re-delivered, identical")
block("""
`UNI_058` recorded the first re-delivery check -- five cases, zero
differing lines. This is the second, on two more files, with the same
result.

The 015 filename is the one offered last drop and deliberately not
applied: the same rule the author used for 013 -- take the entry's
declared working handle -- would give `015definitionalprecedence.md`, and
that was recorded as a derivation rather than a delivery, offered and
held. It has now been delivered at exactly that name, so the derivation
was right and holding it was still correct. The file is renamed in this
commit.

Recorded because the holding is the part worth keeping: in a folder where
one entry devotes a paragraph to why its own name is not settled, a
derived filename applied quietly would have been indistinguishable from a
delivered one a week later.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_059..UNI_068")
print(BAR)
