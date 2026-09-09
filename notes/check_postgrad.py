#!/usr/bin/env python3
# check_postgrad.py -- CC0, stdlib only, parses under 3.9
#
# Checker for notes/markers/POSTGRAD_2026_09_09.md, under the notes/
# convention: the entry is stored as delivered, this checker never
# edits it, and every disagreement goes in this output. The entry is
# a LIST of seven research items ("postgrad list"), each with four
# fields (Q / design / sits in / why). Nothing here adjudicates any
# item, ranks them, or assigns an id; every reading below is about
# the record and about which artifacts in this tree an item's own
# text reaches.
#
# Five readings:
#   1  structure -- seven numbered items, four fields each
#   2  schema against RESEARCH_RENDER.md -- ids (none assigned, none
#      invented) and the `What it opens` field (absent from all)
#   3  anchors -- each item's stated in-tree referent resolved by
#      content or by path, never by grep for the item's own words
#      (a text search would count this file and this checker)
#   4  item 5's stated run-1 fact checked against the run log it
#      names -- a transcription check, not a reading of the run
#   5  index exclusion -- the list is not a gap-bearing document

import hashlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MARKER = os.path.join(HERE, "markers", "POSTGRAD_2026_09_09.md")
FIELDS = ("Q", "design", "sits in", "why")

# item number -> (artifact, how the item's text reaches it)
ANCHORS = {
    1: ("anchor-measurand-crossing/WORK_ORDER.md",
        "the two prompts the item says to reuse"),
    2: ("anchor-measurand-crossing/lexicon.json",
        "measurand vs instrument denomination, per case"),
    3: ("uninstrumented/specs/SCOPED_REFUSAL.md",
        "the refusal-attribution spec the item's tag would feed"),
    4: ("anchor-measurand-crossing/lexicon.json",
        "sc-01's 30 cm sampling boundary as a claim boundary"),
    5: ("ontology-probe/ontologies/substrate-primary/runs/"
        "claudeopus5_r1.jsonl",
        "run 1, named in the item's own design line"),
    6: ("readout-count/EXCLUSION_STACK_trucking_v2.md",
        "ASRS beside the trucking channel the item says is absent"),
    7: ("ontology-probe/ontologies/substrate-primary/"
        "constructions.jsonl",
        "c-011, an operator-built statement about the same phase"),
}
# per-item content marker that must appear in the anchor file, so the
# anchor is resolved by what the artifact holds and not by its name
CONTENT = {
    1: "decision-anchored",
    2: "canonical",
    3: "refus",
    4: "30 cm",
    5: "interior_state",
    6: "ASRS",
    7: "first eight weeks",
}


def _read(path):
    return io.open(path, encoding="utf-8").read()


# ------------------------------------------------ 1  structure

def structure():
    text = _read(MARKER)
    heads = re.findall(r"(?m)^(?:postgrad list: )?(\d)  ([A-Z][A-Z0-9 ,—’'\-]+)$",
                       text)
    numbers = [int(n) for n, _ in heads]
    titles = [t.strip() for _, t in heads]
    # split into item bodies on the numbered heading lines
    bodies = re.split(r"(?m)^(?:postgrad list: )?\d  [A-Z][^\n]*$", text)[1:]
    fields = []
    for b in bodies:
        present = []
        for f in FIELDS:
            if re.search(r"(?m)^\s{3}%s\s" % re.escape(f), b):
                present.append(f)
        fields.append(present)
    return {
        "n_items": len(heads),
        "numbers": numbers,
        "sequential": numbers == list(range(1, len(numbers) + 1)),
        "titles": titles,
        "fields_per_item": fields,
        "all_four_fields": all(p == list(FIELDS) for p in fields),
        "sha256": hashlib.sha256(
            io.open(MARKER, "rb").read()).hexdigest(),
    }


# ------------------------------------------------ 2  schema

def schema():
    """RESEARCH_RENDER.md fixes a per-gap field set including `What
    it opens`, and an id scheme (three-letter prefix + sequence). The
    list carries neither. Recorded, not repaired: an id is permanent
    once assigned, so none is invented here, and `What it opens` is
    the field AUDIT_OPEN_RESEARCH.md found absent in 0 of 182 entries
    across the rendered batch -- this list inherits the same
    absence."""
    text = _read(MARKER)
    rr = os.path.join(ROOT, "RESEARCH_RENDER.md")
    rr_txt = _read(rr) if os.path.isfile(rr) else ""
    return {
        "research_render_present": os.path.isfile(rr),
        "render_names_what_it_opens": "What it opens" in rr_txt,
        "what_it_opens_count": text.count("What it opens"),
        "ids_assigned": bool(re.search(r"\b[A-Z]{3}_\d{3}\b", text)),
        "ids_invented_here": False,
    }


# ------------------------------------------------ 3  anchors

def anchors():
    out = {}
    for n, (rel, how) in ANCHORS.items():
        path = os.path.join(ROOT, rel)
        present = os.path.isfile(path)
        by_content = present and CONTENT[n] in _read(path)
        out[n] = {"artifact": rel, "how": how, "present": present,
                  "resolves_by_content": bool(by_content),
                  "content_marker": CONTENT[n]}
    return out


# ------------------------------------------------ 4  item 5 fact

def item5_against_run():
    """Item 5's design line states a fact about run 1: '"preference"
    walked past an "interior_state" exclusion in run 1'. Both halves
    are checkable against the artifacts the item names -- the run
    log's c-025 record and the primitive set's absent list. What is
    NOT checkable here, and is recorded as such: the walking-past is
    the restater's own note, a self-report; the run is a coded sheet
    with no restatement text, so the mechanical leak check is
    NOT_EVALUABLE and nothing here can confirm the route independently
    of the restater saying so."""
    base = os.path.join(ROOT, "ontology-probe", "ontologies",
                        "substrate-primary")
    run = os.path.join(base, "runs", "claudeopus5_r1.jsonl")
    prim = os.path.join(base, "primitives.json")
    if not (os.path.isfile(run) and os.path.isfile(prim)):
        return {"run_present": os.path.isfile(run),
                "primitives_present": os.path.isfile(prim)}
    recs = [json.loads(l) for l in _read(run).splitlines() if l.strip()]
    hits = [r for r in recs
            if "preference" in r.get("terms_added", [])
            and "interior_state" in (r.get("note") or "")]
    absent = [a["term"] for a in json.load(io.open(prim, encoding="utf-8"))
              .get("absent_by_design", [])]
    return {
        "run_present": True,
        "primitives_present": True,
        "records_with_preference_and_interior_state_note":
            [r["id"] for r in hits],
        "interior_state_on_absent_list": "interior_state" in absent,
        "preference_on_absent_list": "preference" in absent,
        "any_raw_response_in_run":
            any("raw_response" in r for r in recs),
        "route_is_self_report": True,
    }


# ------------------------------------------------ 5  index

def index_exclusion():
    gi = os.path.join(ROOT, "GAP_INDEX.md")
    txt = _read(gi) if os.path.isfile(gi) else ""
    return {"gap_index_present": os.path.isfile(gi),
            "markers_dir_in_index": "notes/markers" in txt,
            "postgrad_in_index": "POSTGRAD_2026" in txt}


# ------------------------------------------------------ render

def render():
    out = []
    w = out.append
    w("POSTGRAD LIST 2026-09-09 -- STRUCTURAL READINGS")
    w("(a list of seven research items; nothing below ranks, files,")
    w(" ids, or adjudicates any of them)")
    w("")
    st = structure()
    w("1  STRUCTURE")
    w("   items %d, numbered %s, sequential %s"
      % (st["n_items"], st["numbers"], st["sequential"]))
    for n, t in zip(st["numbers"], st["titles"]):
        w("   %d  %s" % (n, t))
    w("   fields per item %s: all four on every item %s"
      % (list(FIELDS), st["all_four_fields"]))
    w("   sha256 %s" % st["sha256"][:16])
    w("")
    sc = schema()
    w("2  SCHEMA AGAINST RESEARCH_RENDER.md")
    w("   render present %s; it names `What it opens` %s"
      % (sc["research_render_present"],
         sc["render_names_what_it_opens"]))
    w("   `What it opens` in the list: %d of %d items"
      % (sc["what_it_opens_count"], st["n_items"]))
    w("   ids assigned in the list: %s; invented here: %s"
      % (sc["ids_assigned"], sc["ids_invented_here"]))
    w("   The `why` field carries what the render's `What it opens`")
    w("   would, in the author's own form; recorded, not re-keyed.")
    w("")
    an = anchors()
    w("3  ANCHORS (path existence and one content marker each)")
    for n in sorted(an):
        a = an[n]
        w("   %d  %-62s" % (n, a["artifact"]))
        w("      present %s; resolves by content (%r) %s"
          % (a["present"], a["content_marker"],
             a["resolves_by_content"]))
        w("      %s" % a["how"])
    w("   Item 3's 'nobody has measured it' and item 6's 'trucking,")
    w("   ag, construction don't' are absence claims with no stated")
    w("   corpus (question-availability QA_004); carried, not scored.")
    w("")
    i5 = item5_against_run()
    w("4  ITEM 5 AGAINST THE RUN IT NAMES")
    if i5.get("run_present"):
        w("   records with 'preference' added and an interior_state")
        w("   note: %s" % i5["records_with_preference_and_interior_state_note"])
        w("   interior_state on the absent list %s; preference on it %s"
          % (i5["interior_state_on_absent_list"],
             i5["preference_on_absent_list"]))
        w("   raw restatement text in the run: %s -> the route is the"
          % i5["any_raw_response_in_run"])
        w("   restater's declaration; leak check NOT_EVALUABLE; the")
        w("   fact transcribes, the mechanism is self-reported.")
    else:
        w("   run or primitives absent: %s" % i5)
    w("")
    ie = index_exclusion()
    w("5  INDEX")
    w("   GAP_INDEX present %s; notes/markers in it %s; this list in"
      % (ie["gap_index_present"], ie["markers_dir_in_index"]))
    w("   it %s. A list is not a gap-bearing document; nothing enters"
      % ie["postgrad_in_index"])
    w("   the index until the author renders an item.")
    w("")
    w("This module computes; it does not conclude. The marker file")
    w("is edited by nothing here.")
    return "\n".join(out)


# ---------------------------------------------------- selftest

def selftest():
    n = [0]

    def check(name, ok):
        n[0] += 1
        if not ok:
            sys.stderr.write("FAIL %s\n" % name)
            sys.exit(1)

    before = hashlib.sha256(io.open(MARKER, "rb").read()).hexdigest()

    st = structure()
    check("seven items", st["n_items"] == 7)
    check("sequential", st["sequential"])
    check("first title", st["titles"][0] ==
          "ANCHOR POSITION IN EXPERT ELICITATION")
    check("last title", st["titles"][-1] == "SURGE-PHASE RECORD LOSS")
    check("four fields each", st["all_four_fields"])

    sc = schema()
    check("render present", sc["research_render_present"])
    check("render names field", sc["render_names_what_it_opens"])
    check("what it opens absent", sc["what_it_opens_count"] == 0)
    check("no ids assigned", not sc["ids_assigned"])
    check("no ids invented", not sc["ids_invented_here"])

    an = anchors()
    check("seven anchors", sorted(an) == list(range(1, 8)))
    for k in an:
        check("anchor %d present" % k, an[k]["present"])
        check("anchor %d by content" % k, an[k]["resolves_by_content"])
    # null: a wrong content marker must NOT resolve
    bogus = CONTENT.copy()
    bogus[6] = "zzz-no-such-string-zzz"
    saved = dict(CONTENT)
    CONTENT.update(bogus)
    try:
        check("bogus marker does not resolve",
              not anchors()[6]["resolves_by_content"])
    finally:
        CONTENT.clear()
        CONTENT.update(saved)

    i5 = item5_against_run()
    check("run present", i5["run_present"])
    check("c-025 carries the fact",
          i5["records_with_preference_and_interior_state_note"] == ["c-025"])
    check("interior_state declared absent",
          i5["interior_state_on_absent_list"])
    check("preference not on absent list",
          not i5["preference_on_absent_list"])
    check("no raw text in run", not i5["any_raw_response_in_run"])

    ie = index_exclusion()
    check("gap index present", ie["gap_index_present"])
    check("markers not in index", not ie["markers_dir_in_index"])
    check("list not in index", not ie["postgrad_in_index"])

    render()
    after = hashlib.sha256(io.open(MARKER, "rb").read()).hexdigest()
    check("marker unchanged across run", before == after)

    print("check_postgrad selftest: %d checks OK" % n[0])


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        selftest()
    else:
        print(render())
