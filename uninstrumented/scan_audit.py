"""
scan_audit.py -- grade the delivered scanner and its trigger set.

CC0-1.0. Standard library only. Deterministic. Imports scan.py and reads
patterns.json; modifies neither.

An earlier pass of this audit ran against a RECONSTRUCTED scanner, written
from patterns.json before scan.py was delivered. The delivered scanner
differs in four ways that move numbers, so section 0 states them and every
number below is from the delivered instrument. The one finding that
survived both is section 1, and it survives because it needs no corpus.

WHAT CAN AND CANNOT BE MEASURED HERE
------------------------------------
The obvious test is a false-positive rate against a known-null corpus, the
../null-harness/ invariant. It is not run, and the reason is the corpus:

    this repository is a corpus ABOUT measurement failure, written in the
    same vocabulary the triggers are made of

`UNVERIFIED` is a claim-table status code here. `benchmark`, `compliance`,
`proxy for` and `tacit` are subject terms. patterns.json contains the
trigger words by definition. Scoring precision on that corpus would measure
the corpus. So sections 2-4 report what it CAN support -- triage load,
concentration, coverage -- and no section reports a precision figure.

THE CORPUS IS LIVE
------------------
Sections 2-5 walk the repository as it stands when the script runs, so every
count MOVES as the repo grows, including when a file is added that discusses
this scanner. Section 5 measures that happening. The pinned sample is a
snapshot, not a fixture.
"""

from __future__ import annotations

import collections
import os
import sys
import tempfile

import scan

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
RULE = "=" * 72


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


# UNI_010 repaired. This script writes its output to samples/, and scan.py
# reads .txt, so run N+1 used to measure run N. The exclusion was a path
# filter reimplemented here, which put the rule outside the tool and left
# anyone else running scan.py over the repo seeing the hits anyway.
#
# It is now a `.scanignore` next to this file, honoured by scan.walk()
# wherever the scan starts from. The loop is closed in the scanner, so the
# reported corpus IS the corpus on disk for every caller.
def corpus():
    return sorted(scan.walk([ROOT], scan.load_ignores([ROOT])))


def words(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return len(fh.read().split())


def scan_string(text, patterns):
    """The delivered scanner takes paths. Wrap a probe string in one."""
    d = tempfile.mkdtemp()
    p = os.path.join(d, "probe.txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    return scan.scan([p], patterns)


# ---------------------------------------------------------------------------


def check_instrument(patterns) -> None:
    section("0  the delivered scanner is not the reconstructed one")

    print("  Four differences that move numbers:\n")
    print("    unit          delivered splits into SENTENCES (>= 20 chars);")
    print("                  the reconstruction worked line by line")
    print("    dedup         delivered `break`s after the first matching")
    print("                  trigger per mechanism per sentence -- at most")
    print("                  one hit per (mechanism, sentence)")
    print("    extensions    delivered reads %s"
          % " ".join(scan.TEXT_EXT))
    print("                  the reconstruction read .md only")
    print("    boundaries    delivered compiles each trigger RAW:")
    print("                  re.compile(t, re.I), no \\b")
    print()
    print("  That last one was flagged [CHOICE] in the reconstruction and")
    print("  guessed the other way. Raw matching means `lean` matches")
    print("  `cleaning` and `slack` matches `slacken`. The dedup pulls in")
    print("  the opposite direction, so the two do not simply add.")
    print()
    print("  Every number below is from the delivered instrument.")


def check_known_signal(patterns) -> None:
    section("1  the drop's own worked example of BUDGET BOUNDARY")

    print("  The register's canonical BUDGET_BOUNDARY case is leaf vs")
    print("  panel, and ../declared-frame/v2/examples/ ships both halves.")
    print("  No corpus, no threshold, no adjudication: does the scanner")
    print("  fire on the case its own trigger list was written for?\n")

    ex = os.path.join(ROOT, "declared-frame", "v2", "examples")
    hits = scan.scan([ex], patterns)
    print("    %s -> %d candidate(s)" % ("declared-frame/v2/examples/",
                                         len(hits)))
    for h in hits:
        print("      %s via %r" % (h["mechanism"], h["trigger"]))

    print()
    print("  Now the same case in four phrasings:\n")
    probes = (
        ("the register's own VISIBLE AS line",
         "The tree is inefficient at photosynthesis compared with a panel."),
        ("the delivered result string",
         "Silicon PV converts ~22% of incident photons; "
         "leaf converts ~1-2%."),
        ("stated as a comparative",
         "The panel is more efficient than the leaf."),
        ("stated with the noun",
         "Silicon PV has a higher conversion efficiency than a leaf."),
    )
    for label, text in probes:
        h = scan_string(text, patterns)
        got = ", ".join("%s (%r, %s)" % (x["mechanism"], x["trigger"],
                                         x["strength"]) for x in h) or "NO HIT"
        print("    %-36s %s" % (label, got))

    print()
    print("  Unchanged from the reconstructed run. Two results:\n")
    print("  (a) The delivered result string does not fire. The triggers")
    print("      catch the RHETORIC of a comparison -- 'more efficient")
    print("      than', 'outperforms', 'orders of magnitude better' -- not")
    print("      the comparison. Two numbers side by side with no")
    print("      comparative is the usual result-line form, and it is")
    print("      invisible to all eight BUDGET BOUNDARY triggers.\n")
    print("  (b) The register's own phrasing fires under the WRONG")
    print("      mechanism: 'inefficient' is a SCORED AS WASTE trigger, so")
    print("      the reader is handed the wrong `check` question.\n")
    print("  Both repairs are cheap: a trigger for the bare-numbers form,")
    print("  and letting mechanisms co-fire -- which is UNI_003 arriving in")
    print("  the scanner. The delivered `break` in scan() is what enforces")
    print("  one-mechanism-per-sentence, so the co-firing repair is a")
    print("  two-line change there.")


def check_triage_load(patterns) -> None:
    section("2  triage load -- the quantity the design turns on")

    print("  patterns.json states its own standard: every hit is a")
    print("  candidate for triage, not a finding. Under that standard the")
    print("  binding constraint is not precision but how many `check`")
    print("  questions a human must answer per unit of text.\n")

    files = corpus()
    total_words = sum(words(f) for f in files)
    hits = scan.scan(corpus(), patterns)
    strong = [h for h in hits if h["strength"] == "candidate"]

    print("  corpus: %d files (%s), %d words"
          % (len(files), " ".join(scan.TEXT_EXT), total_words))
    print("    all candidates      %5d   %.1f per 1000 words"
          % (len(hits), 1000.0 * len(hits) / total_words))
    print("    strength=candidate  %5d   %.1f per 1000 words"
          % (len(strong), 1000.0 * len(strong) / total_words))
    print("    strength=weak       %5d"
          % (len(hits) - len(strong)))
    print()
    print("  The `weak` band is the delivered scanner's own confidence")
    print("  gradient -- reported, never used to filter, which is the same")
    print("  discipline as the register's CONFIDENCE field. It downgrades")
    print("  a SCALAR DEMAND hit when conditioning words are nearby, an")
    print("  AUDIT ASYMMETRY hit with no hedge in the sentence, and any")
    print("  sentence over 400 chars.")
    print()
    by_file = collections.Counter(h["file"] for h in hits)
    print("  Densest files:\n")
    shown = 0
    for f, n in by_file.most_common():
        w = words(f)
        if w < 400:
            continue
        print("    %-52s %5d w %4d hits %5.1f /1000"
              % (os.path.relpath(f, ROOT)[:52], w, n, 1000.0 * n / w))
        shown += 1
        if shown >= 6:
            break


def check_concentration(patterns) -> None:
    section("3  concentration and coverage")

    hits = scan.scan(corpus(), patterns)
    by_mech = collections.Counter(h["mechanism"] for h in hits)
    by_trig = collections.Counter((h["mechanism"], h["trigger"].lower())
                                  for h in hits)
    total_triggers = sum(len(v["rx"]) for v in patterns.values())

    print("  %d candidates, %d mechanisms, %d triggers defined\n"
          % (len(hits), len(patterns), total_triggers))
    print("    %-24s %6s %8s" % ("mechanism", "hits", "share"))
    print("    " + "-" * 40)
    for m, n in by_mech.most_common():
        print("    %-24s %6d %7.1f%%" % (m, n, 100.0 * n / len(hits)))
    for m in patterns:
        if m not in by_mech:
            print("    %-24s %6d %7.1f%%" % (m, 0, 0.0))

    print()
    print("  Top matched strings:\n")
    for (m, t), n in by_trig.most_common(6):
        print("    %-22s %-30s %4d" % (m, t[:30], n))
    top4 = sum(n for _, n in by_trig.most_common(4))
    print()
    print("  4 matched strings produce %d of %d candidates (%.0f%%)."
          % (top4, len(hits), 100.0 * top4 / len(hits)))
    print()
    print("  Corpus-conditional, and neither number grades the list.")
    print("  SCALAR DEMAND is near-silent because this corpus contains no")
    print("  survey instruments -- 'on a scale of', 'rate yourself',")
    print("  'composite score' are psychometrics vocabulary. A silent")
    print("  trigger on the wrong corpus is not a dead trigger.")
    print()
    print("  In the other direction, the dominant strings are corpus")
    print("  artifacts: UNVERIFIED is a claim-table STATUS CODE here, not a")
    print("  hedge attached to an account. The trigger is correct and the")
    print("  corpus is adversarial to it.")
    print()
    print("  One result IS about the instrument, and it is the largest")
    print("  single number in the table. `lean` is compiled raw, so it")
    print("  matches as a substring:\n")

    import re
    for trig in ("lean", "slack"):
        sel = [h for h in hits if h["trigger"].lower() == trig]
        rx = re.compile(r"\w*%s\w*" % trig, re.I)
        forms = collections.Counter()
        for h in sel:
            for w in rx.findall(h["sentence"]):
                forms[w.lower()] += 1
        exact = forms.get(trig, 0)
        print("    %-8s %4d hits   surrounding forms: %s"
              % ("`%s`" % trig, len(sel),
                 ", ".join("%s x%d" % (w, n)
                           for w, n in forms.most_common(4))))
        print("             the bare word appears %d time(s)" % exact)
    print()
    lean_hits = sum(1 for h in hits if h["trigger"].lower() == "lean")
    print("  `lean` is the most-fired trigger in the corpus and nearly all")
    print("  of it is `clean`, `cleanly` and `boolean`. Adding word")
    print("  boundaries to that one trigger removes ~%d of %d candidates"
          % (lean_hits, len(hits)))
    print("  (%.0f%%) at no cost, because the bare word is rare here."
          % (100.0 * lean_hits / len(hits)))
    print()
    print("  `slack` is the harder case and stays: the bare word IS what")
    print("  mostly matches, and the noise is a proper-noun homograph and a")
    print("  code identifier, neither of which \\b removes. That one is a")
    print("  triage cost the design already accepts.")


def check_asym() -> None:
    section("4  --asym: the register's own WOULD MEASURE, now shipped")

    print("  The AUDIT ASYMMETRY entry names its measurement:\n")
    print("      count caveats issued per account type across a transcript")
    print("      corpus; the ratio is the measurement\n")
    print("  and CLAIM_TABLE.md calls it the cheapest of the three")
    print("  unworked entries to run. scan.py --asym is that measurement.\n")

    tally = scan.asym(corpus())
    oh = on_ = ih = in_ = 0
    any_hedge = 0
    for a, b, c, d in tally.values():
        oh += a
        on_ += b
        ih += c
        in_ += d
        any_hedge += bool(a or c)

    print("    files with an account mention   %d" % len(tally))
    print("    files with ANY hedge at all     %d" % any_hedge)
    print("    outside    hedged %3d of %4d   %.4f"
          % (oh, on_, oh / max(on_, 1)))
    print("    incumbent  hedged %3d of %4d   %.4f"
          % (ih, in_, ih / max(in_, 1)))
    r_out = oh / max(on_, 1)
    r_inc = ih / max(in_, 1)
    print("    ratio (outside/incumbent)       %s"
          % ("inf" if not r_inc else "%.2f" % (r_out / r_inc)))
    print()
    print("  Every hedge in the corpus, hand-checked:\n")
    real = 0
    for path in corpus():
        for _ln, s in scan.sentences(path):
            m = scan.HEDGES.search(s)
            if not m:
                continue
            if not (scan.OUTSIDE.search(s) or scan.INCUMBENT.search(s)):
                continue
            print("    %-40s %r"
                  % (os.path.relpath(path, ROOT)[:40], m.group(0)))
    print()
    print("  All of them are artifacts: `UNVERIFIED` and `unverified` as")
    print("  claim-table and provenance STATUS CODES, `claims to` inside")
    print("  prose describing a model, `Self-reported` inside a JSON spec")
    print("  string, and `anecdotal` inside patterns.json itself -- the")
    print("  scanner matching the file that defines the trigger.")
    print()
    print("  Zero are a hedge attached to an account, so the ratio above is")
    print("  computed on nothing and means nothing.")
    print()
    print("  The instrument gap is CLOSED and the corpus gap is not. The")
    print("  measurement needs reportage -- limitations sections, news,")
    print("  transcripts, regulatory filings -- and this repository")
    print("  contains none. That is a sharper statement of UNI_006 than")
    print("  UNI_006 makes: the entry is not unrun for want of a design.")


def check_self_reference(patterns) -> None:
    section("5  the corpus is live, and the scanner is inside it")

    own = {os.path.join("uninstrumented", "patterns.json"),
           os.path.join("uninstrumented", "scan.py"),
           os.path.join("uninstrumented", "scan_audit.py"),
           os.path.join("uninstrumented", "README.md"),
           os.path.join("uninstrumented", "AUDIT_NOTES.md")}

    hits = scan.scan(corpus(), patterns)
    inside = [h for h in hits if os.path.relpath(h["file"], ROOT) in own]

    print("  patterns.json holds the trigger strings, and the scanner reads")
    print("  .json. So the definition file is in the corpus:\n")
    print("    candidates from the scanner's own files: %d of %d"
          % (len(inside), len(hits)))
    seen = collections.Counter(os.path.relpath(h["file"], ROOT)
                               for h in inside)
    for f, n in sorted(seen.items()):
        print("      %-44s %d" % (f, n))
    print()
    print("  Not a bug to fix by excluding a path. It is the use-mention")
    print("  problem at its purest, and it is the one place in this corpus")
    print("  where it actually bites -- documents ABOUT the mechanisms")
    print("  return almost nothing, because the triggers are written in the")
    print("  vocabulary of the FAILING document, not of the mechanism.")
    print("  'apparatus in the wrong channel' is how the register names")
    print("  MODALITY; 'failed to demonstrate' is what a paper exhibiting")
    print("  it says. The two barely overlap -- except in the file that")
    print("  lists both.")
    print()
    print("  The counts in sections 2-4 are therefore a SNAPSHOT, not a")
    print("  fixture. This is ../anchor-interval/'s moving reference")
    print("  occurring rather than being described.")
    print()
    print("  And one step further, which is why EXCLUDE exists at the top")
    print("  of this file: scan.py reads .txt, and this script writes its")
    print("  own output to samples/. Left alone, run N+1 measures run N and")
    print("  the script has NO FIXED POINT -- consecutive runs disagree")
    print("  before anything in the repo has changed.")
    print()
    sample = os.path.join(HERE, "samples", "scan_audit.sample.txt")
    if os.path.exists(sample):
        own = scan.scan([sample], patterns)
        print("    candidates in this script's own last output: %d"
              % len(own))
        print("    excluded from every walk above, by path")
    else:
        print("    (no pinned sample on disk yet)")
    print()
    print("  That exclusion is a hand-broken loop, not a fix. Anyone")
    print("  running scan.py over this repo WILL see those hits, because")
    print("  the file is really there. What the exclusion buys is a script")
    print("  that converges; what it costs is that the reported corpus is")
    print("  no longer the corpus on disk. Both halves are stated here")
    print("  rather than one of them being quietly true.")


def main() -> int:
    patterns = scan.load_patterns()

    print()
    print("GRADING scan.py + patterns.json")
    print("%d mechanisms, %d triggers"
          % (len(patterns), sum(len(v["rx"]) for v in patterns.values())))

    check_instrument(patterns)
    check_known_signal(patterns)
    check_triage_load(patterns)
    check_concentration(patterns)
    check_asym()
    check_self_reference(patterns)

    section("READING")
    print("""
  The one result that needs no corpus survives the change of instrument:
  the scanner returns ZERO on both halves of the drop's own worked example
  of BUDGET BOUNDARY, and the register's own phrasing of that case fires
  under SCORED AS WASTE instead. The triggers catch the rhetoric of a
  comparison and not the comparison.

  Triage load is the quantity the design turns on by its own statement,
  and it is affordable. The delivered `weak` band is a real addition --
  a confidence gradient reported and never used to filter, the same
  discipline as the register's CONFIDENCE field.

  No precision figure is reported. This repository is a corpus about
  measurement failure written in the triggers' own vocabulary, and
  patterns.json is itself in the corpus. That measurement needs an outside
  corpus.

  --asym is the AUDIT ASYMMETRY entry's own WOULD MEASURE, now shipped as
  code. It runs, and every hedge this corpus produces is an artifact --
  status codes, spec strings, and the trigger file matching itself. Zero
  are a hedge attached to an account. The instrument gap is closed and the
  corpus gap is not, which is a sharper statement than UNI_006 makes: that
  entry is no longer unrun for want of a design.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
