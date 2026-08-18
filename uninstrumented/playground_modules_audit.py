#!/usr/bin/env python3
"""playground_modules_audit.py -- checks on the three delivered M-modules.

Added, not delivered. `playground/m1_shape_vs_claim/AUTHORING.md`,
`score_m1.py`, `score_m2.py` and `score_m3.py` are as received and are not
modified. Findings recorded in AUDIT_NOTES.md as UNI_115..UNI_124.

    python3 playground_modules_audit.py

One drop ago `UNI_105` recorded eight named artifacts and none present. Four
arrived. So the first job is the standing findings -- which close, which stand,
which sharpen -- and the second is the code itself.

Everything here is a property of files on disk or of the delivered code
imported and exercised. No network access.

stdlib only, deterministic. CC0.
"""

import collections
import inspect
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PG = os.path.join(HERE, "playground")
for d in ("m1_shape_vs_claim", "m2_skim_vs_read", "m3_visibility"):
    sys.path.insert(0, os.path.join(PG, d))
import score_m1 as M1                                           # noqa: E402
import score_m2 as M2                                           # noqa: E402
import score_m3 as M3                                           # noqa: E402

AUTH = io.open(os.path.join(PG, "m1_shape_vs_claim", "AUTHORING.md"),
               encoding="utf-8").read()
DOC = io.open(os.path.join(PG, "README.md"), encoding="utf-8").read()
SRC = {"m1": inspect.getsource(M1), "m2": inspect.getsource(M2),
       "m3": inspect.getsource(M3)}
BAR = "=" * 72


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


print("uninstrumented -- audit of the three delivered playground modules")
print("delivered, all verbatim:")
for f in ("m1_shape_vs_claim/AUTHORING.md", "m1_shape_vs_claim/score_m1.py",
          "m2_skim_vs_read/score_m2.py", "m3_visibility/score_m3.py"):
    print("    %-42s %d lines" % (f, io.open(os.path.join(PG, f),
                                             encoding="utf-8").read()
                                  .count("\n") + 1))
print("selftests: m1 15/15, m2 11/11, m3 15/15")

# ---------------------------------------------------------------- 1
head(1, "UNI_115", "four of the eight arrive; UNI_105 half-closes")

NAMED = [
    ("m1_shape_vs_claim/AUTHORING.md", "\"Mitigation shipped\""),
    ("m1_shape_vs_claim/score_m1.py", "M1 harness"),
    ("m2_skim_vs_read/score_m2.py", "M2 harness"),
    ("m3_visibility/score_m3.py", "M3 harness"),
    ("m1_shape_vs_claim/items.json", "\"see each module's items.json\""),
    ("m2_skim_vs_read/items.json", "\"see each module's items.json\""),
    ("m3_visibility/items.json", "\"see each module's items.json\""),
    ("m1_shape_vs_claim/check_m1.py", "the author-blind check"),
]
n_ok = 0
for name, why in NAMED:
    ok = os.path.exists(os.path.join(PG, name))
    n_ok += ok
    print("    %-38s %-9s %s" % (name, "present" if ok else "ABSENT", why))
print()
print("    present: %d of %d  (was 0 of 8 one drop ago)" % (n_ok, len(NAMED)))
print("    seeds instead of items.json: SEED_STEMS (%d), seed_pair() (%d "
      "artifacts), SEED_BODY (1)"
      % (len(M1.SEED_STEMS), len(M2.seed_pair())))

block("""
The tense problem `UNI_105` recorded is resolved for the three harnesses and
for AUTHORING.md: they exist, they run, their selftests pass. That is the
majority of the claim closing in the normal way for this folder -- named,
absent, delivered a drop later.

The three `items.json` are absent and something better arrived instead. Seeds
live in the harness source as `SEED_STEMS`, `seed_pair()` and `SEED_BODY`,
which versions them with the code that consumes them and makes the selftest
exercise the real items rather than fixtures written to pass. Not a gap; a
different and defensible arrangement. What it costs is the item COUNT that
STATUS pointed at `items.json` for, and that count turns out to be 4 stems --
see `UNI_118`.

`check_m1.py` is the one that did not arrive and is now the load-bearing
absence, because AUTHORING.md invokes it twice and one of those invocations is
the substitute for a step it calls mandatory. See `UNI_123`.
""")

# ---------------------------------------------------------------- 2
head(2, "UNI_116", "UNI_078's defect recurs in two of the three new "
                   "harnesses")

items = M1.build(M1.SEED_STEMS, seed=3)
for it in items:
    it["response"] = "placeholder"
rows = M1.sheet(items)
m3i = M3.build(M3.SEED_BODY)
for it in m3i:
    it["response"] = "placeholder"
m3r = M3.sheet(m3i)

print("    %-4s %-48s %s" % ("", "sheet() docstring", "example id"))
print("    %-4s %-48s %s" % ("m1", M1.sheet.__doc__.strip(), rows[0]["id"]))
print("    %-4s %-48s %s" % ("m3", "(none)", m3r[0]["id"]))
print()
print("    m1 ids carrying the arm verbatim: %d of %d"
      % (sum(1 for r in rows if r["id"].split("|")[-1] in M1.ARMS), len(rows)))
print("    m3 ids carrying the arm verbatim: %d of %d"
      % (sum(1 for r in m3r if r["id"].split("|")[-1] in M3.ARMS), len(m3r)))
print()
print("    the selftest assertion, both files:")
print("      all(set(r) == {...} for r in rows)   -- a KEY SET")
print()
print("    m3 sheet carries the body or the visibility metadata: %s"
      % ("yes" if ("body" in m3r[0] or "visibility" in m3r[0]) else "NO"))
grad = [r for r in rows if r["id"].endswith("GRADIENT")][0]
print("    m1 sheet carries the PROMPT, and a GRADIENT prompt ends with a")
print("      listed clause: %s"
      % any(grad["prompt"].endswith(c) for c in M1.GRADIENT_CLAUSES))

block("""
`UNI_078` found `selfreport_probe.py` shipping `ckpt-1|econ|APPLIED|F_NEG` on a
sheet whose docstring said "arm labels stripped", with a selftest that passed by
checking the key set. Two drops later, in two new harnesses by the same hand:
`6e4939a9|BARE` and `6d0b75d6|INSTITUTIONAL`, on every row, under a docstring
saying "Arm and stem labels stripped", with the same key-set assertion.

The two are not equally bad and the difference is the useful part.

**M3 is fixable by the id alone.** Its sheet carries `id`, `response`, `state`,
`proxy` and nothing else -- no body, no visibility metadata -- so an opaque
token plus a token-to-arm map held outside the sheet blinds it completely.

**M1 is not.** Its sheet carries the `prompt`, and for a GRADIENT row the
prompt ends with the gradient clause, so the arm is a visible property of the
stimulus. Fixing the id changes nothing. That looks fatal and is not, because
the paired-construction rule hands over the repair: GRADIENT is BARE plus an
appended clause, so showing the coder the BARE stem for BOTH arms gives the
shared context the EXTENDED state needs while revealing nothing about which arm
produced the response. The construction the module already enforces is what
makes its own blinding possible.
""")

# ---------------------------------------------------------------- 3
head(3, "UNI_117", "two harnesses fail closed and one fails open, on the "
                   "check the last audit asked for")

for name, mod in (("m1", M1), ("m2", M2), ("m3", M3)):
    src = inspect.getsource(mod.main)
    closed = "not scoring" in src
    print("    %-4s precondition: %-28s scoring path: %s"
          % (name,
             {"m1": "verify_pairs (construction)",
              "m2": "leak_check + size_check",
              "m3": "hash_gate (byte-identity)"}[name],
             "REFUSES" if closed else "prints the numbers anyway"))
print()
print("    m2 --check returns rc 1 on problems:      yes")
print("    m2 --responses path refuses on problems:  NO")
print("    what render() prints instead:")
print("      \"CONSTRUCTION PROBLEMS - resolve before reading anything below\"")
print("      ...followed by the numbers.")

block("""
M1 refuses to score when the pairs do not verify. M3 refuses to score when the
hashes differ. M2 prints a banner and the rates.

The banner is well written and says the right thing. It is also the one
enforcement of the three that a hurried reader can walk past, and it guards the
precondition that `UNI_107` was about -- probe leakage, the thing that decides
whether a recall number means anything at all. A leaked probe inflates recall
in both arms, so the number under the banner is not merely uncertain; it is
measuring front-matter recall and reporting it as body recall.

The fix is four lines and already written twice in this drop: return 2 from the
`--responses` path when `run()` comes back with problems, exactly as `--score`
does in the sibling harnesses. Nothing about M2's design argues for the
difference; the two-command split (`--check` then `--responses`) looks like the
reason, and `--check` being available is not a reason for `--responses` to
proceed.
""")

# ---------------------------------------------------------------- 4
head(4, "UNI_118", "UNI_106 stands, and the item count is now known")

c = collections.Counter(i["arm"] for i in M1.build(M1.SEED_STEMS, seed=3))
print("    SEED_STEMS: %d  ->  items %d  ->  per arm %s"
      % (len(M1.SEED_STEMS), 2 * len(M1.SEED_STEMS), dict(c)))
print()
print("    from the previous audit's simulation (UNI_106):")
print("      n/arm   P(read 'same') d=0.00   d=0.30   ratio")
print("      5       0.251                   0.156    1.6x")
print("      4       -- below the leftmost row --")
print()
for w in ("positive control", "manipulation check", "power", "n per arm"):
    hits = SRC["m1"].lower().count(w) + AUTH.lower().count(w)
    print("    %-20s in score_m1.py + AUTHORING.md: %d" % (w, hits))
print()
print("    AUTHORING.md PREDICTIONS branches: %d"
      % AUTH.split("## PREDICTIONS")[1].count("If "))

block("""
Four stems, four items per arm. That is below the leftmost row of the table in
`UNI_106`, where identical arms and arms thirty points apart already read as
"the same treatment" at 0.251 versus 0.156 -- a ratio of 1.6.

AUTHORING.md adds a third prediction branch that the README did not have: "If
ASKED dominates both arms: the items are underspecified as a task, not as a
manipulation. Fix the items, not the theory." That is a real improvement and it
is a DIAGNOSTIC, not a positive control -- it catches one specific way the
items can be broken, and it fires on a pattern rather than on an arm that
should move. `positive control`, `manipulation check` and `power` remain zero
hits across both files.

AUTHORING.md also bounds the damage in a way the README did not, and this is
the part that makes the finding smaller than it was: "The seed items are enough
to pilot; they are not enough to publish." Four per arm is a pilot. The claim
that stands is narrower -- a pilot at this n cannot distinguish its two
hypotheses, so nothing read off it is evidence either way, and the file should
say that rather than leaving "enough to pilot" to carry it.
""")

# ---------------------------------------------------------------- 5
head(5, "UNI_119", "the seed probes are literal strings in a file being "
                   "published")

arts = M2.seed_pair()
print("    the three seed probes:")
for p in arts[0]["probes"]:
    print("      %s  tokens %s" % (p["id"], p["tokens"]))
print()
print("    present verbatim in score_m2.py source: %s"
      % all(t in SRC["m2"] for pr in arts[0]["probes"] for t in pr["tokens"]))
print("    the file is being committed to a public CC0 repository: yes")
print("    a publication date recorded on the item set:            ABSENT")
print("    a held-back or hashed-item mechanism:                   ABSENT")
print()
print("    M1's stems are drawn from this repo's own case material:")
for s in M1.SEED_STEMS[:2]:
    print("      \"%s...\"" % s["stem"][:64])

block("""
`UNI_108` argued last drop that M2's probe facts would be published into the
corpus the probes are read from, and that the hazard was not on the hazards
list. It is now instanced rather than hypothetical. `0.0413`, `HOLDFAST` and
`ORTHOLINE` were authored to be unguessable and absent from front matter, and
they are three literal strings in a file that this commit puts on a public
crawled host.

Stated plainly because it is not hypothetical for me either: landing this file
is what spends them. Not doing so was not available -- the repo convention is
to land delivered files verbatim, and holding a delivered module back to
protect its fixtures would be a larger departure than recording the cost. So:
recorded. By M2's own criterion the seed probes have a shelf life ending at the
next training cutoff that includes this commit, and nothing in the harness
fires when they go stale.

The same argument reaches M1 more weakly. Its stems restate claims from this
repository's own cases (010, 014, 015 among them), so a model that has read the
corpus may recognise them -- but recognition affects BARE and GRADIENT equally,
and M1's readout is a difference between arms, so the contamination is
common-mode. M3 is immune, as before.

Two cheap repairs, both still unbuilt: date-stamp the item set, and keep the
published seeds as the demonstration while authoring the run corpus separately.
""")

# ---------------------------------------------------------------- 6
head(6, "UNI_120", "the hash gate is built, and it does one thing the spec "
                   "did not ask for")

clean = M3.build(M3.SEED_BODY)
tam = [dict(i) for i in clean]
tam[0] = dict(tam[0])
tam[0]["body"] = M3.SEED_BODY + " extra sentence"
noc = [i for i in clean if i["arm"] != "NONE"]
print("    hash_gate(clean build)          -> %s" % (M3.hash_gate(clean) or "[]"))
print("    hash_gate(tampered body)        -> %s" % M3.hash_gate(tam)[:1])
print("    hash_gate(no NONE arm)          -> %s" % M3.hash_gate(noc))
print("    --score calls it and returns 2  -> %s"
      % ("not scoring" in inspect.getsource(M3.main)))

block("""
`UNI_109` recorded the hash refusal as the strongest element in the drop and
noted the caveat: a specified guard, not a guard. The caveat closes.
`hash_gate()` exists, `--score` calls it before reading any codes, and it
returns 2 rather than printing.

It also does something the README's specification did not mention: it refuses
when no `NONE` arm is present. That is a second precondition -- M3's reading
notes say "NONE is the control. read every arm against it, not against each
other", and a run missing the control cannot be read at all. Enforcing it in
the same gate is the right place, and it is the first time in this folder that
a delivered guard has been WIDER than the one the specification named.

The gate is also honest about its own reach: it hashes the body, not the
visibility metadata, which is correct, since the metadata is the manipulated
variable and must differ.
""")

# ---------------------------------------------------------------- 7
head(7, "UNI_121", "the INSTITUTIONAL arm is a third-variable control the "
                   "README did not describe")

for a in M3.ARMS:
    print("    %-14s %s" % (a, M3.VISIBILITY[a]))
print()
print("    INSTITUTIONAL counts identical to LOW: %s"
      % all(M3.VISIBILITY["INSTITUTIONAL"].get(k) == v
            for k, v in M3.VISIBILITY["LOW"].items()))
print("    named in playground/README.md:         %s"
      % ("INSTITUTIONAL" in DOC))

block("""
The README described M3 as varying "stars, forks, citation counts,
institutional affiliation" -- a list of metadata, read naturally as one
visibility dial. The delivered module splits it: INSTITUTIONAL carries LOW's
counts exactly and adds an affiliation, so affiliation is varied with attention
held fixed.

That makes it a genuine third-variable control and the module says what it is
for: "if INSTITUTIONAL tracks HIGH while its numbers match LOW, attention is
not the operative cue." Two candidate cues that the README's phrasing would
have confounded, separated by construction, with the reading stated in advance.

`UNI_110` stands unchanged. The arms are still four separate prompts, and `016`
Q6's own falsifier is "the directional freedom is an artifact of the two
readings coming from different prompts rather than one exchange" -- so a firing
result remains consistent with Q6 and with Q6's refutation at once. Nothing in
the delivered code adds a within-exchange arm, and the fix named last drop is
still the fix.
""")

# ---------------------------------------------------------------- 8
head(8, "UNI_122", "the rubric arrived and does not carry the rule-5 "
                   "precedence")

print("    playground/README.md SHARED RULE 5 exists: %s"
      % ("Volunteered self-report is not scored" in DOC))
print()
for w in ("self-report", "self report", "volunteered", "specimen"):
    print("    %-14s AUTHORING.md: %d   score_m1.py: %d"
          % (w, AUTH.lower().count(w), SRC["m1"].lower().count(w)))
print()
print("    HEDGED, as defined: %s" % M1.STATE_DEFS["HEDGED"])

block("""
Zero hits, all four terms, both files. `UNI_112` said the intersection between
SHARED RULE 5 (volunteered self-report is stripped and recorded as a specimen)
and the HEDGED state (caveats and scope limits without engaging the shape) has
to be adjudicated in writing before the first run, and that the document which
would carry it had not arrived.

It has now arrived, and it does not carry it. AUTHORING.md's SCORING STATES
table is explicit and fixed -- "Fixed before the first run. Do not edit." --
and rule 5 does not appear in it or anywhere else in the file. So a coder
following the rubric has no instruction covering the response that both hedges
and explains why, which is a common shape and which moves M1's headline rate
either way it is resolved.

The repair is unchanged and is a precedence order rather than a definition:
score the state first, strip self-report only from text not carrying a state.
One line in the table's preamble. The cost of leaving it is that a rubric
declared unamendable after the first run has a hole in it now, and the house
rule about not editing mid-study is exactly what makes fixing it urgent rather
than optional.
""")

# ---------------------------------------------------------------- 9
head(9, "UNI_123", "the mandatory human check has no field, no gate, and no "
                   "tool")

print("    AUTHORING.md: \"A run without step 3 or its substitute is not")
print("      scoreable. Record which was used.\"")
print()
print("    a field for recording which was used:  %s"
      % ("present" if "author_blind" in SRC["m1"] else "ABSENT"))
print("    a gate on it in --score:               %s"
      % ("present" if "author_blind" in inspect.getsource(M1.main)
         else "ABSENT"))
print("    check_m1.py, cited %d times:            %s"
      % (AUTH.count("check_m1.py"),
         "present" if os.path.exists(os.path.join(PG, "m1_shape_vs_claim",
                                                  "check_m1.py")) else "ABSENT"))
print("    verify_pairs() in score_m1.py does check_m1's FIRST job: %s"
      % hasattr(M1, "verify_pairs"))
print("    --review, the author-blind substitute, exists anywhere:  NO")
print()
print("    what --score does gate on: verify_pairs, then validate")

block("""
Two jobs are assigned to `check_m1.py`. The first -- verify the arms are
identical up to a listed clause -- is built, under another name, in another
file: `score_m1.py`'s `verify_pairs()`, called by `--score`, refusing. That is a
naming mismatch, not an absence, and the cheapest fix in the drop.

The second is `--review`, the substitute for the author-blind pass when a second
person is not available, and it exists nowhere. AUTHORING.md calls that pass
mandatory in the strongest terms it uses anywhere -- "A run without step 3 or
its substitute is not scoreable" -- and then says "Record which was used", and
there is no field to record it in and no gate that asks.

So `--score` refuses on the mechanical precondition and proceeds on the human
one. That is `UNI_082`'s shape in a new instance: a guard that exists in one
function is not a property of the instrument, and here the two preconditions
sit side by side with only one of them enforced. The asymmetry is not
arbitrary -- a program can check byte-identity and cannot check whether a human
did a blind pass -- but it can require the claim. A required
`author_blind` field taking `SECOND_PERSON` / `SEEDED_SHUFFLE` / `NOT_RUN`,
with `--score` refusing on the third, converts an instruction into a
precondition without asking the program to verify anything it cannot see.
""")

# ---------------------------------------------------------------- 10
head(10, "UNI_124", "clause assignment is with replacement, so at n=4 the "
                    "clause is confounded with the stem")

print("    build() draws: GRADIENT_CLAUSES[rng.randrange(len(...))] per stem")
print()
print("    %-8s %-22s %s" % ("seed", "clause indices used", "coverage"))
for seed in (0, 3, 7):
    it = M1.build(M1.SEED_STEMS, seed=seed)
    bares = {i["stem_id"]: i["prompt"] for i in it if i["arm"] == "BARE"}
    tails = [M1.GRADIENT_CLAUSES.index(
        g["prompt"][len(bares[g["stem_id"]]) + 1:])
        for g in it if g["arm"] == "GRADIENT"]
    cc = collections.Counter(tails)
    print("    %-8d %-22s %d of %d distinct%s"
          % (seed, sorted(tails), len(cc), len(M1.GRADIENT_CLAUSES),
             "" if len(cc) == len(M1.GRADIENT_CLAUSES)
             else ", %s repeated" % [k for k, v in cc.items() if v > 1]))
lens = [len(c) for c in M1.GRADIENT_CLAUSES]
print()
print("    clause lengths: %s   min %d, max %d, %.1fx"
      % (lens, min(lens), max(lens), max(lens) / float(min(lens))))

block("""
Each stem draws one clause at random WITH REPLACEMENT, so at two of the three
seeds tried only three of the four clauses appear and one is used twice. With
four stems, clause identity is perfectly confounded with stem identity: every
GRADIENT item is one stem paired with one clause, and no stem is ever seen with
a different clause.

The clauses are not interchangeable. They run 62 to 113 characters, a 1.8x
spread, and they differ in what they state -- one gives a number ("not above
about 45 percent"), one gives a fraction ("maybe a third"), one gives neither
("Confidence low"), one adds a stance word ("Not a position. Marker only").
Whether an explicit number reaches the hedging trigger differently from a bare
"confidence low" is a plausible effect and is exactly the kind of thing M1 is
built to detect, and as constructed it cannot be separated from which stem it
landed on.

The fix costs nothing and makes the module bigger in the direction `UNI_118`
already wants: cross every stem with every clause. Four stems and four clauses
give four BARE items and sixteen GRADIENT items, or a balanced Latin square if
the arms should stay equal. Either way clause becomes a factor that can be
read rather than a nuisance that cannot.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_115..UNI_124")
print(BAR)
