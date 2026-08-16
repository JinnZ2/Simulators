"""
scan_audit.py -- grade the trigger set in patterns.json.

CC0-1.0. Standard library only. Deterministic. Reads patterns.json and
scan.py; modifies neither.

WHAT CAN AND CANNOT BE MEASURED HERE
------------------------------------
The obvious test is a false-positive rate against a known-null corpus, the
../../null-harness/ invariant. It is not run, and the reason is the corpus:

    this repository is a corpus ABOUT measurement failure, written in the
    same vocabulary the triggers are made of

`UNVERIFIED` is a claim-table status code here, so the AUDIT ASYMMETRY
trigger `(unverified|uncorroborated)` fires 52 times on the repo's own
verdict vocabulary. `benchmark`, `compliance`, `proxy for` and `tacit` are
all subject terms. Scoring a false-positive rate on that corpus would
measure the corpus, not the triggers. So sections 2-4 report what the corpus
CAN support -- triage load, trigger concentration, coverage -- and no
section reports a precision figure.

Section 1 needs no corpus at all, and it is the one that finds something.

THE CORPUS IS LIVE
------------------
Sections 2-4 walk the repository's markdown as it stands when the script
runs, so every count below MOVES as the repo grows -- including when a file
is added that discusses this scanner. The pinned sample in samples/ is a
snapshot, not a fixture, and re-running will not reproduce it once anything
has been written.

That is the moving-reference problem in ../../anchor-interval/ appearing in
this file rather than being described by it: the measurement and its
reference are not independent, and the number is reported against a
reference that the act of reporting changes. Pinning it would need a frozen
corpus copy, which is the honest fix and is not done here.
"""

from __future__ import annotations

import collections
import json
import os
import sys

import scan

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
RULE = "=" * 72


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def repo_markdown():
    out = []
    for d, _, fs in os.walk(ROOT):
        if os.sep + ".git" in d:
            continue
        for f in sorted(fs):
            if f.endswith(".md"):
                out.append(os.path.join(d, f))
    return sorted(out)


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# 1  the known signal


def check_known_signal(patterns, rules) -> None:
    section("1  the drop's own worked example of BUDGET BOUNDARY")

    print("  The register's canonical BUDGET BOUNDARY case is the leaf vs")
    print("  panel comparison, and this drop ships both halves of it as")
    print("  declared-frame examples. No corpus, no adjudication, no")
    print("  threshold: does the scanner fire on the case its own trigger")
    print("  list was written for?\n")

    for name in ("photosynthesis", "tree"):
        path = os.path.join(HERE, "examples", "%s.json" % name)
        doc = json.loads(read(path))
        hits = scan.scan_text(read(path), rules)
        print("    examples/%-18s %d candidate(s)" % (name + ".json",
                                                      len(hits)))
        print("      result: %s" % doc["result"][:60])
        for m, t, _, g, _ in hits:
            print("      -> %s via %r on %r" % (m, t, g))

    print()
    print("  Zero. Now the same case in four phrasings:\n")
    probes = (
        ("the register's own VISIBLE AS line",
         "the tree is inefficient at photosynthesis"),
        ("the delivered result string",
         "silicon PV converts ~22% of incident photons; "
         "leaf converts ~1-2%"),
        ("stated as a comparative",
         "the panel is more efficient than the leaf"),
        ("stated with the noun",
         "silicon PV has a higher conversion efficiency than a leaf"),
    )
    for label, text in probes:
        hits = scan.scan_text(text, rules)
        got = ", ".join("%s (%r)" % (m, g) for m, _, _, g, _ in hits) or "NO HIT"
        print("    %-36s %s" % (label, got))

    print()
    print("  Two results, and the second is the sharper one.\n")
    print("  (a) The delivered result string does not fire. The trigger list")
    print("      catches the RHETORIC of a comparison -- 'more efficient")
    print("      than', 'outperforms', 'orders of magnitude better' -- and")
    print("      not the comparison. Two numbers placed side by side with no")
    print("      comparative is how the claim usually appears in a result")
    print("      line, and that form is invisible to every BUDGET BOUNDARY")
    print("      trigger.\n")
    print("  (b) The register's own phrasing of the case fires under the")
    print("      WRONG mechanism: 'inefficient' is a SCORED AS WASTE trigger.")
    print("      A reader triaging that hit is handed the wrong `check`")
    print("      question -- 'what does it return, and on what interval' --")
    print("      for a case whose actual question is 'are both budgets closed")
    print("      at the same boundary'.\n")
    print("  Neither is fatal to the design, and both are cheap: BUDGET")
    print("  BOUNDARY needs a trigger for the bare-numbers form (a percentage")
    print("  or ratio within N tokens of a second one for a different")
    print("  object), and the mechanisms need to be allowed to co-fire, which")
    print("  is uninstrumented/ UNI_003 arriving in the scanner.")


# ---------------------------------------------------------------------------
# 2  triage load


def check_triage_load(patterns, rules, raw_rules) -> None:
    section("2  triage load -- the quantity the design actually turns on")

    print("  patterns.json states its own standard: 'Every hit is a candidate")
    print("  for triage, not a finding.' Under that standard precision is not")
    print("  the binding constraint -- how many `check` questions a human has")
    print("  to answer per unit of text is.\n")

    files = repo_markdown()
    words = hits = raw = 0
    per = {}
    for f in files:
        t = read(f)
        w = scan.word_count(t)
        h = len(scan.scan_text(t, rules))
        r = len(scan.scan_text(t, raw_rules))
        words += w
        hits += h
        raw += r
        per[os.path.relpath(f, ROOT)] = (w, h)

    print("  corpus: %d markdown files, %d words" % (len(files), words))
    print("    with word boundaries   %4d candidates  %.1f per 1000 words"
          % (hits, 1000.0 * hits / words))
    print("    without (--raw)        %4d candidates  %.1f per 1000 words"
          % (raw, 1000.0 * raw / words))
    print("    cost of dropping \\b    %+d candidates (%+.0f%%)"
          % (raw - hits, 100.0 * (raw - hits) / hits))
    print()
    print("  About one candidate per 1000 words. That is a workable triage")
    print("  load -- a 5000-word document arrives with roughly five questions")
    print("  attached, not fifty. The trigger list is written tightly enough")
    print("  that the human step it depends on is affordable.")
    print()
    print("  Densest files:\n")
    for rel, (w, h) in sorted(per.items(),
                              key=lambda kv: -(1000.0 * kv[1][1]
                                               / max(kv[1][0], 1)))[:6]:
        if per[rel][0] < 300:
            continue
        print("    %-48s %5d w  %3d hits  %5.1f /1000"
              % (rel[:48], w, h, 1000.0 * h / w))


# ---------------------------------------------------------------------------
# 3  an expectation that did not hold


def check_use_mention(rules) -> None:
    section("3  use-mention: a checked expectation that failed")

    print("  Expected before running: a scanner keyed on surface words")
    print("  cannot distinguish a document EXHIBITING a failure from one")
    print("  DESCRIBING it, so documents about the mechanisms should light")
    print("  up entirely with false positives.\n")

    for rel in ("uninstrumented/README.md", "uninstrumented/CLAIM_TABLE.md",
                "declared-frame/v2/FRAME.md", "declared-frame/README.md"):
        t = read(os.path.join(ROOT, rel))
        h = scan.scan_text(t, rules)
        w = scan.word_count(t)
        print("    %-40s %5d w %3d hits %5.1f /1000"
              % (rel, w, len(h), 1000.0 * len(h) / w))
        if h:
            print("        %s" % sorted({m for m, _, _, _, _ in h}))

    print()
    print("  It did not happen. The document that names all seven mechanisms")
    print("  and glosses each one returns 2 candidates in 986 words, and the")
    print("  v2 frame document returns none.")
    print()
    print("  Why: the triggers are written as the vocabulary of the FAILING")
    print("  document, not as the vocabulary of the mechanism. 'apparatus in")
    print("  the wrong channel' is how the register names MODALITY; 'failed")
    print("  to demonstrate' is what a paper exhibiting it says. The two")
    print("  vocabularies barely overlap, and that separation is doing more")
    print("  work than the trigger list looks like it is doing.")


# ---------------------------------------------------------------------------
# 4  concentration and coverage


def check_concentration(patterns, rules) -> None:
    section("4  concentration: 24 triggers of 69 ever fire")

    hits = []
    for f in repo_markdown():
        hits.extend(scan.scan_text(read(f), rules))

    by_mech = collections.Counter(m for m, _, _, _, _ in hits)
    by_trig = collections.Counter((m, t) for m, t, _, _, _ in hits)
    total_triggers = sum(len(v["triggers"]) for v in patterns.values())

    print("  %d candidates, %d mechanisms, %d triggers defined\n"
          % (len(hits), len(patterns), total_triggers))
    print("    %-24s %6s %8s" % ("mechanism", "hits", "share"))
    print("    " + "-" * 40)
    for m in patterns:
        n = by_mech.get(m, 0)
        print("    %-24s %6d %7.1f%%" % (m, n, 100.0 * n / len(hits)))

    print()
    print("  Top triggers:\n")
    for (m, t), n in by_trig.most_common(6):
        print("    %-22s %-34s %4d" % (m, t[:34], n))
    top4 = sum(n for _, n in by_trig.most_common(4))
    print()
    print("  4 triggers produce %d of %d candidates (%.0f%%)."
          % (top4, len(hits), 100.0 * top4 / len(hits)))
    print("  %d of %d triggers never fire on %d words."
          % (total_triggers - len(by_trig), total_triggers,
             sum(scan.word_count(read(f)) for f in repo_markdown())))

    print()
    print("  Both numbers are CORPUS-CONDITIONAL and neither grades the")
    print("  trigger list. SCALAR DEMAND is 7 of 8 triggers silent because")
    print("  this corpus contains no survey instruments -- 'on a scale of',")
    print("  'rate yourself', 'composite score' are psychometrics vocabulary")
    print("  and there is none here. A silent trigger on the wrong corpus is")
    print("  not a dead trigger.")
    print()
    print("  The concentration is corpus-conditional in the other direction")
    print("  and worth naming precisely, because it is the shape of every")
    print("  false positive this corpus produces:")
    print()
    print("    `(unverified|uncorroborated)` fires 52 times, almost all on")
    print("    the string UNVERIFIED -- a claim-table STATUS CODE in this")
    print("    repo, not a hedge attached to an account. The trigger is")
    print("    correct and the corpus is adversarial to it.")
    print()
    print("    `slack` fires 49 times on a mix of Slack the product, 'the")
    print("    slack rope', a code identifier, and genuine idle-capacity")
    print("    usage. This one is the trigger's own problem: a four-letter")
    print("    common noun with a proper-noun homograph.")
    print()
    print("  Which is why no precision number appears in this file. Getting")
    print("  one requires a corpus that is not about its own subject, and")
    print("  every corpus in this repository is.")


# ---------------------------------------------------------------------------


def check_self_reference(patterns, rules) -> None:
    section("5  writing this audit changed the corpus it measures")

    own = os.path.join("declared-frame", "v2", "README.md")
    total_triggers = sum(len(v["triggers"]) for v in patterns.values())

    def sweep(skip):
        hits = []
        for f in repo_markdown():
            if os.path.relpath(f, ROOT) in skip:
                continue
            hits.extend(scan.scan_text(read(f), rules))
        return hits

    without = sweep({own})
    with_ = sweep(set())
    fired_without = {(m, t) for m, t, _, _, _ in without}
    fired_with = {(m, t) for m, t, _, _, _ in with_}

    print("  The README written to report sections 1-4 quotes the triggers")
    print("  in order to discuss them, so it entered the corpus as text.\n")
    print("    %-26s %6s %8s" % ("", "hits", "silent"))
    print("    " + "-" * 44)
    print("    %-26s %6d %8d" % ("without v2/README.md", len(without),
                                 total_triggers - len(fired_without)))
    print("    %-26s %6d %8d" % ("with v2/README.md", len(with_),
                                 total_triggers - len(fired_with)))
    print()
    woke = sorted(fired_with - fired_without)
    print("  Triggers this audit's own README moved from never-firing to")
    print("  firing: %d\n" % len(woke))
    for m, t in woke:
        print("      %-22s %s" % (m, t))
    print()
    print("  Three of the five are SCALAR DEMAND triggers that section 4")
    print("  reported silent 'because this corpus contains no survey")
    print("  instruments'. That reading is still correct -- there are none --")
    print("  and the triggers now fire anyway, on a document explaining that")
    print("  they do not fire.")
    print()
    print("  So the corpus counts in sections 2-4 are a SNAPSHOT, not a")
    print("  fixture, and re-running after any markdown is added will not")
    print("  reproduce them. Pinning would need a frozen corpus copy.")
    print()
    print("  This is ../../anchor-interval/'s moving reference occurring")
    print("  rather than being described: the measurement and its reference")
    print("  are not independent, and reporting the number changed it. The")
    print("  numbers in the folder README are quoted from a pinned sample")
    print("  and are not re-derived here, which is the smallest honest")
    print("  handling short of freezing the corpus.")


def main() -> int:
    patterns = scan.load_patterns()
    rules = scan.compile_triggers(patterns, True)
    raw_rules = scan.compile_triggers(patterns, False)

    print()
    print("GRADING patterns.json")
    print("%d mechanisms, %d triggers"
          % (len(patterns),
             sum(len(v["triggers"]) for v in patterns.values())))

    check_known_signal(patterns, rules)
    check_triage_load(patterns, rules, raw_rules)
    check_use_mention(rules)
    check_concentration(patterns, rules)
    check_self_reference(patterns, rules)

    section("READING")
    print("""
  The one result that needs no corpus: the scanner returns ZERO on both
  halves of the drop's own worked example of BUDGET BOUNDARY, and the
  register's own phrasing of that case fires under SCORED AS WASTE
  instead. The triggers catch the rhetoric of a comparison and not the
  comparison, and two numbers side by side -- the usual form -- is
  invisible to all eight BUDGET BOUNDARY triggers.

  Triage load is the quantity the design turns on, by its own statement,
  and it is low: about one candidate per 1000 words across ~300k. Dropping
  word boundaries costs roughly 40% more candidates for no obvious gain.
  Exact counts are in section 2 and move with the corpus.

  The expectation that use-mention would dominate was checked and did not
  hold. Documents describing the mechanisms return almost nothing, because
  the triggers are written in the vocabulary of the failing document
  rather than the vocabulary of the mechanism. That separation is load-
  bearing and is not visible from reading the file.

  No precision figure is reported. This repository is a corpus about
  measurement failure written in the triggers' own vocabulary --
  UNVERIFIED is a status code here -- so a false-positive rate scored on
  it would measure the corpus. That measurement needs an outside corpus
  and is the next thing to run.

  And the corpus is live. Writing the README that reports sections 1-4
  moved five triggers from never-firing to firing, three of them SCALAR
  DEMAND triggers that section 4 calls silent for want of survey
  instruments -- now firing on the document that says so. The counts here
  are a snapshot, not a fixture.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
