#!/usr/bin/env python3
# revision_audit.py (mining-increment) -- CC0, stdlib only,
# parses under 3.9
#
# Audit of SOURCE_DROP_V2.md -- the GAP 14 entry revised with MI_002
# folded back in. Both versions stay as delivered; this module edits
# neither. Three jobs: check the resolution of MI_002 against the new
# text (the repair took a stronger form than the audit suggested --
# the term got defined, not the headline hedged); check the two new
# devices (CONFIGURATION NOTE, READ CEILING) including the scaffold's
# compliance with the ceiling; and verify the invariant sections are
# byte-identical across the revision, so the scaffold's arithmetic
# stands on an unchanged specification.

import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import audit as A  # noqa: E402

RUN_DATE = "2026-08-30"


def _read(name):
    return io.open(os.path.join(HERE, name), encoding="utf-8").read()


def v1():
    return _read("SOURCE_DROP.md")


def v2():
    return _read("SOURCE_DROP_V2.md")


# --------------------------------------------- the MI_002 resolution

def mi002_resolution():
    """MI_002 keyed on one v1 sentence and the headline it
    contradicted. In v2 the sentence is gone, the carries are stated
    precisely, the headline's referent is defined one paragraph down,
    and the appendix is promoted to a primary source table."""
    a, b = v1(), v2()
    old_sentence = ("The connecting term is unstudied on both sides "
                    "of the silo boundary")
    return {
        "old_sentence_in_v1": old_sentence in " ".join(a.split()),
        "old_sentence_gone_from_v2":
            old_sentence not in " ".join(b.split()),
        "carries_stated_precisely":
            "The two carries stop one node short of each other"
            in b,
        "headline_unchanged":
            "**Knowledge state:** NOT_STUDIED (the coupling term)"
            in b,
        "referent_defined":
            "RESERVOIR POOL LOADING on a multi-dam" in " ".join(
                b.split()),
        "appendix_heading_gone":
            "WHAT THE CHINESE WORK HAS" not in b,
        "promoted_to_primary":
            "primary, not alternative" in b
            and "Entered as peer sources, primary" in b,
        "v1_still_carries_both": "WHAT THE CHINESE WORK HAS" in a
            and old_sentence in " ".join(a.split()),
    }


# ------------------------------------------------- the new devices

def configuration_note():
    """Mechanism transfers, configuration does not -- the FIRM/SOFT
    split (RCC_007's shape) arriving inside the author's own source
    table -- plus the source-ranking rule."""
    b = v2()
    one = " ".join(b.split())
    return {
        "mechanism_configuration_split":
            "transfers; the configuration does not" in one,
        "ranking_rule":
            "not a reason to rank these sources below an English one"
            in one,
        "language_geology_rule":
            "The language of the source carries no weight here; the "
            "geology of the basin carries all of it." in one,
    }


def read_ceiling():
    """A per-source read-depth declaration: the CWIM boundary-condition
    formulation -- the load-bearing content -- sits below the depth the
    entry was read at, declared as a capability limit on the audit
    rather than an open question about the work. The scaffold complies:
    no CWIM formulation appears in mining_increment.py, which is the
    ceiling being honored rather than silently exceeded."""
    b = v2()
    one = " ".join(b.split())
    src = _read("mining_increment.py")
    return {
        "section_present": "READ CEILING" in b,
        "declares_depth":
            "entered from English-language abstracts" in one,
        "names_the_invisible_content":
            "boundary-condition formulation" in one
            and "not visible at that depth" in one,
        "capability_limit_framing":
            "capability limit on the audit, not an open question "
            "about the work" in one,
        "scaffold_complies": "CWIM" not in src,
    }


# ------------------------------------------------ invariant sections

def _section(doc, start, end):
    return doc.split(start)[1].split(end)[0]

INVARIANTS = [
    ("subsurface table",
     "## What is already quantified (do not re-derive)", "\n---"),
    ("governing equations + provenance flag",
     "## Governing equations", "**CITATION STATUS"),
    ("citation status paragraph",
     "**CITATION STATUS", "**TRANSFER CAVEAT"),
    ("research question", "**Research question:**", "**Disciplines"),
    ("method", "**Method:**", "**Expected deliverable:**"),
    ("deliverable + falsifiers",
     "**Expected deliverable:**", "## Why this gap"),
]

CHANGED = [
    ("the split paragraph",
     "This split is the whole point of the gap", "---"),
    ("the transfer caveat", "**TRANSFER CAVEAT.**", "---"),
    ("why-different, first paragraph",
     "## Why this gap is different", "The omission of this gap"),
]


def invariants():
    a, b = v1(), v2()
    rows = []
    for name, start, end in INVARIANTS:
        same = _section(a, start, end) == _section(b, start, end)
        rows.append((name, same))
    changed = []
    for name, start, end in CHANGED:
        diff = _section(a, start, end) != _section(b, start, end)
        changed.append((name, diff))
    return {"identical": rows,
            "all_identical": all(s for _n, s in rows),
            "changed": changed,
            "all_changed": all(d for _n, d in changed)}


def flag_contained_v2():
    return A.provenance_flag(v2())


# ------------------------------------------------ the addendum (v3)

ADDENDUM_MARKER = "**CONFIGURATION NOTE — not a discount.**"


def v3():
    return _read("SOURCE_DROP_V3.md")


def addendum_fragment():
    delivery = _read("ADDENDUM_DELIVERY.md")
    part = delivery.split("GAP 15")[0]
    lines = part.splitlines()
    start = next(i for i, ln in enumerate(lines)
                 if ln.startswith("PORE-PRESSURE"))
    return "\n".join(lines[start:]).rstrip() + "\n"


def addendum():
    """The pore-pressure validation case, inserted per the delivered
    instruction ('insert before CONFIGURATION NOTE'). The assembly is
    verified as a pure insertion: the fragment comes from the delivery
    sheet, sits immediately before the instructed marker, and removing
    it reproduces v2 byte-for-byte. The content: u is the term that
    drops the factor of safety and is normally modeled; a u measured
    DURING a real event gives the modeled term a known answer to
    reproduce -- 'has not earned its place' otherwise -- routed to the
    transfer test of Method step 2, whose gate the scaffold already
    is."""
    frag = addendum_fragment()
    b, c = v2(), v3()
    one = " ".join(c.split())
    return {"fragment_absent_from_v2": frag not in b,
            "fragment_once_in_v3": c.count(frag) == 1,
            "pure_insertion": c.replace(frag + "\n", "", 1) == b,
            "placed_before_marker":
                (frag + "\n" + ADDENDUM_MARKER) in c,
            "doi_carried": "10.5194/hess-25-4147-2021" in c,
            "measured_during_stated":
                "recorded DURING a debris flow event" in one,
            "earned_its_place_rule":
                "has not earned its place in the FoS calculation"
                in one,
            "routed_to_step2":
                "the transfer test in Method step 2" in one}


# ---------------------------------------------------------- render

def _wrap(s, n=66):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return lines


def render():
    out = []
    w = out.append
    w("GAP 14 REVISION -- MI_002 FOLDED BACK, AUDITED")
    w("")
    w("Both versions stay as delivered; prior claims keep their")
    w("ratings on the text they rated. Dated %s." % RUN_DATE)
    w("")
    r = mi002_resolution()
    w("THE MI_002 RESOLUTION")
    for k in ("old_sentence_in_v1", "old_sentence_gone_from_v2",
              "carries_stated_precisely", "headline_unchanged",
              "referent_defined", "appendix_heading_gone",
              "promoted_to_primary", "v1_still_carries_both"):
        w("  %-28s %s" % (k, r[k]))
    for ln in _wrap(
            "The resolution took a stronger form than the audit's "
            "one-parenthetical suggestion: the headline stands and "
            "its referent is defined one paragraph down -- what no "
            "record carries is pool loading on a multi-dam surface "
            "chain, the two existing carries stopping one node short "
            "of each other -- while the sentence the finding keyed on "
            "is gone and the appendix is a primary source table."):
        w("  " + ln)
    w("")
    c = configuration_note()
    w("THE CONFIGURATION NOTE")
    for k, vv in c.items():
        w("  %-28s %s" % (k, vv))
    w("")
    rc = read_ceiling()
    w("THE READ CEILING")
    for k in ("section_present", "declares_depth",
              "names_the_invisible_content",
              "capability_limit_framing", "scaffold_complies"):
        w("  %-28s %s" % (k, rc[k]))
    for ln in _wrap(
            "A per-source read-depth declaration: the load-bearing "
            "content sits below the depth the entry was read at, and "
            "saying so is a statement about the audit's reach, not "
            "the work. The scaffold honors the ceiling -- no CWIM "
            "formulation appears in mining_increment.py."):
        w("  " + ln)
    w("")
    iv = invariants()
    w("INVARIANT SECTIONS (byte-identical across the revision)")
    for name, same in iv["identical"]:
        w("  %-38s %s" % (name, "identical" if same else "DIFFERS"))
    w("CHANGED SECTIONS (and they did change)")
    for name, diff in iv["changed"]:
        w("  %-38s %s" % (name, "changed" if diff else "UNCHANGED"))
    ad = addendum()
    w("THE ADDENDUM (v3: the pore-pressure validation case)")
    for k in ("fragment_absent_from_v2", "fragment_once_in_v3",
              "pure_insertion", "placed_before_marker", "doi_carried",
              "measured_during_stated", "earned_its_place_rule",
              "routed_to_step2"):
        w("  %-28s %s" % (k, ad[k]))
    for ln in _wrap(
            "Assembled per the delivered instruction as a verified "
            "pure insertion. The content adds the missing instrument "
            "class to the LEM coupling: u is the FoS-dropping term "
            "and normally modeled, and a u measured during a real "
            "event gives the modeled term a known answer to reproduce "
            "-- the known-answer standing rule arriving in the "
            "entry's own text, routed to the transfer test whose "
            "gate the scaffold already is."):
        w("  " + ln)
    w("")
    fc = flag_contained_v2()
    w("provenance flag contained on v2 as well: %s"
      % fc["all_contained"])
    for ln in _wrap(
            "A revision that changed the epistemics without touching "
            "the arithmetic: equations, flag, method, falsifiers and "
            "deliverable are byte-identical, so the scaffold stands "
            "unchanged on an unchanged specification -- which is what "
            "'the claim updates, never the instrument' looks like "
            "from the author's side."):
        w("  " + ln)
    w("")
    w("This module computes; it does not conclude. Findings are in")
    w("CLAIM_TABLE.md as MI_009..MI_014.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "revision_audit.py has no checks of its own. The checks "
            "that exercise it live in selftest_mi.py.\n"
            "    python3 mining-increment/selftest_mi.py\n")
        sys.exit(2)
    print(render())
