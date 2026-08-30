#!/usr/bin/env python3
# addendum_audit.py (bridge-impoundment) -- CC0, stdlib only,
# parses under 3.9
#
# Audit of the GAP 15 addendum. The author delivered two blocks with
# the instruction "add to the quantified table, plus a note";
# SOURCE_DROP_V2.md is the assembly -- v1 with the delivered fragment
# inserted at the end of the quantified section, after the SIGN CAVEAT
# and before the divider ahead of "The unstudied term". The placement
# is a [CHOICE]: the instruction names the section, not the byte
# offset, and this point is the least-disturbing one (the CITATION
# STATUS paragraph's "table rows above" keeps its referent). The
# assembly is verified as a PURE INSERTION: the fragment comes from
# the delivery sheet, appears once, and removing it reproduces v1
# byte-for-byte.

import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

MARKER = "---\n\n## The unstudied term"


def _read(name):
    return io.open(os.path.join(HERE, name), encoding="utf-8").read()


def fragment():
    delivery = _read("ADDENDUM_DELIVERY.md")
    part = delivery.split("GAP 15")[1]
    lines = part.splitlines()
    start = next(i for i, ln in enumerate(lines)
                 if ln.startswith("INSTRUMENTED CASCADE"))
    return "\n".join(lines[start:]).rstrip() + "\n"


def assembly():
    a, b, frag = _read("SOURCE_DROP.md"), _read("SOURCE_DROP_V2.md"), \
        fragment()
    return {"fragment_absent_from_v1": frag not in a,
            "fragment_once_in_v2": b.count(frag) == 1,
            "pure_insertion":
                b.replace(frag + "\n", "", 1) == a,
            "placed_in_quantified_section":
                (frag + "\n" + MARKER) in b,
            "placement_declared_choice": True}


def cascade_case():
    """Fjaerland 2004: a measured instance of the chained shape --
    with the configuration split applied symmetrically. A moraine dam
    is not a clogged bridge; what is measured is the RELEASE half
    (impoundment breach -> debris flow, post-event morphology), and
    the clog term is not in it -- checked mechanically: the word does
    not occur in the fragment. Mechanism kin, configuration differs,
    which is the sibling entry's own CONFIGURATION NOTE discipline
    applied to this folder's new source. The measured chain's two
    outputs (surge + debris load) are the release initiator's two
    load-bearing fields."""
    frag = fragment()
    one = " ".join(frag.split())
    return {"doi_carried": "10.1007/s10346-008-0118-3" in frag,
            "measured_instance_stated":
                "a MEASURED instance of the chained-process shape"
                in one,
            "release_half_only": "clog" not in frag.lower(),
            "chain_stated":
                "impoundment breach → debris flow" in one,
            "volume_carried": "240,000 m³" in frag}


def standing_record():
    """The NVE register carries its own search-exclusion finding: it
    serves English and never ranks on an English query, because the
    phenomenon indexes under jokullaup / skred and the institution
    under NVE. That is a query-vocabulary-bounded null -- an
    English-query absence bounded by its vocabulary, not evidence of
    record absence (the QA_004 / CT_005 discipline, stated here by
    the author about a national register) -- and 'long series = the
    instrument for a slow rate' names why a standing register beats
    event studies for a rate question."""
    frag = fragment()
    one = " ".join(frag.split())
    return {"register_url_carried":
                "glacier.nve.no/Glacier/viewer/GLOF/en/" in frag,
            "serves_english_stated": "serves English" in one,
            "vocabulary_exclusion_stated":
                "never ranks on an English query" in one
                and "jøkullaup / skred" in one,
            "slow_rate_instrument":
                "long series = the instrument for a slow rate" in one,
            "egress_note": "glacier.nve.no is not probed from here; "
                           "the register's content is carried at the "
                           "delivery's own description depth"}


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
    w("GAP 15 ADDENDUM -- ASSEMBLY AND CONTENT AUDIT")
    w("")
    asm = assembly()
    w("THE ASSEMBLY (a verified pure insertion)")
    for k in ("fragment_absent_from_v1", "fragment_once_in_v2",
              "pure_insertion", "placed_in_quantified_section"):
        w("  %-32s %s" % (k, asm[k]))
    for ln in _wrap(
            "The instruction names the section, not the byte offset; "
            "the placement after the SIGN CAVEAT is declared as the "
            "assembler's choice, picked so the CITATION STATUS "
            "paragraph's 'table rows above' keeps its referent."):
        w("  " + ln)
    w("")
    cc = cascade_case()
    w("THE INSTRUMENTED CASCADE CASE")
    for k in ("doi_carried", "measured_instance_stated",
              "release_half_only", "chain_stated", "volume_carried"):
        w("  %-32s %s" % (k, cc[k]))
    for ln in _wrap(
            "The configuration split applies symmetrically: a moraine "
            "dam is not a clogged bridge, what is measured is the "
            "release half, and the clog term does not occur in the "
            "fragment -- mechanism kin, configuration differs, the "
            "sibling entry's own CONFIGURATION NOTE discipline "
            "applied to this folder's new source. The measured "
            "chain's outputs are the release initiator's two "
            "load-bearing fields."):
        w("  " + ln)
    w("")
    sr = standing_record()
    w("THE STANDING RECORD")
    for k in ("register_url_carried", "serves_english_stated",
              "vocabulary_exclusion_stated", "slow_rate_instrument"):
        w("  %-32s %s" % (k, sr[k]))
    for ln in _wrap(
            "A register that serves English and never ranks on an "
            "English query is a query-vocabulary-bounded null: an "
            "English-language absence is bounded by its vocabulary, "
            "not evidence of record absence. " + sr["egress_note"]):
        w("  " + ln)
    w("")
    w("This module computes; it does not conclude. Findings are in")
    w("CLAIM_TABLE.md as BI_008..BI_010.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "addendum_audit.py has no checks of its own. The checks "
            "that exercise it live in selftest_bi.py.\n"
            "    python3 bridge-impoundment/selftest_bi.py\n")
        sys.exit(2)
    print(render())
