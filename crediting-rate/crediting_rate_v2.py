#!/usr/bin/env python3
# crediting_rate_v2.py -- DISPATCH L, revision 2. CC0, stdlib only, 3.9.
#
# Does attribution of an imported technique track CONTRIBUTION or LOANWORD
# VISIBILITY? A rate comparison across three visibility bins, with two hard
# gates in front of the comparison and four nulls behind it.
#
#   python3 crediting_rate_v2.py events.jsonl descriptions.jsonl \
#           depth.jsonl frame.json [seed]
#   python3 crediting_rate_v2.py --selftest
#   python3 crediting_rate_v2.py --choices
#
# WHAT CHANGED FROM v1, and why this is a separate module rather than an edit:
# v1 is delivered work and stays exactly as it is. The bins went from two to
# three, the blind moved from the bin to the item NAME, crediting became
# mechanical, and two returns were added. Those are not edits to a scorer,
# they are a different scorer, so it lands beside v1 under the repo's
# supersession convention and both stay inspectable.
#
# WHAT IS IMPORTED RATHER THAN COPIED: load_frame, ordering_state and
# outside come from crediting_rate.py; spearman comes from
# readout-count/readout_count.py. Five stale copies of one gate across three
# drops is what copying cost this tree last time.
#
# NOTHING HERE IS A MEASUREMENT. Every fixture is CONSTRUCTED and says so in
# its own header. No catalogue was consulted, no corpus declared, no
# description read from any reference work, and no statement is made about
# algebra, paper, sine, any tradition, or any person.

import hashlib
import io
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "readout-count"))

from crediting_rate import load_frame, ordering_state, outside   # noqa: E402
from readout_count import spearman                               # noqa: E402

PREDICTION = os.path.join(HERE, "PREDICTION_V2.md")
BRANCH_SET = os.path.join(HERE, "branch_set_v2.json")

# ---------------------------------------------------------------- vocabulary

# The order's three states plus its fourth, which is a bin and never an
# assignment. AMBIGUOUS items are carried, counted, and enter no rate.
VISIBLE = "visible"
TECHNICAL_ONLY = "technical_only"
NOT_RETAINED = "not_retained"
AMBIGUOUS = "ambiguous"
BINS = (VISIBLE, TECHNICAL_ONLY, NOT_RETAINED)
ALL_BINS = BINS + (AMBIGUOUS,)

# Visibility order, low to high. Used only for the correlation report, which
# is why it is an ordinal and not a score.
BIN_ORDINAL = {NOT_RETAINED: 0, TECHNICAL_ONLY: 1, VISIBLE: 2}

SIDES = ("technique_side", "language_side")

RETURNS = ("ETYMOLOGY_TRACKING", "CONTRIBUTION_TRACKING", "UNKNOWN_measurable",
           "DOMAIN_SPECIFIC", "BLOCKED", "FRAME_ASYMMETRIC", "CONTAMINATED_FRAME")

# The order's method layer is two pieces, F (branch set) and G (return
# envelope / enum), and they are in different states.
#
# F EXISTS, in another repository: JinnZ2/method-layer carries branch_set
# among its tools. That repository is outside this session's GitHub scope, so
# the fact is CARRIED from the operator and verified against nothing here.
# `branch_set_v2.json` is therefore an emission in F's shape pointing at a
# real consumer, not a stand-in for a missing build.
#
# G IS ABSENT. method-layer's five tools are branch_set,
# preference_free_rank, rank_detector, frame_probe and
# observer_position_control (carried, same provenance) and none of them is a
# return envelope. The order's instruction for that state is to define the
# enum locally and mark it, so RETURNS above is the local definition and this
# is the mark. It is declared rather than derived: nothing here searched
# method-layer, and a False would be a claim about a repository this session
# cannot read.
G_ABSENT = True
G_ABSENT_REASON = ("no return-envelope tool among method-layer's five "
                   "(branch_set, preference_free_rank, rank_detector, "
                   "frame_probe, observer_position_control); RETURNS is "
                   "defined locally")
METHOD_LAYER_TOOLS = ("branch_set", "preference_free_rank", "rank_detector",
                      "frame_probe", "observer_position_control")
F_LOCATION = "JinnZ2/method-layer (out of this session's GitHub scope; CARRIED)"

# ----------------------------------------------------------------- constants

# [CHOICE 1] items with attested ordering needed in each of the three bins
# before any gap is read. Carried from v1's MIN_PER_BIN; no basis beyond
# being stated.
MIN_PER_BIN = 3

# [CHOICE 2] N1 permutations and bootstrap draws. Carried from v1.
SHUFFLES = 2000

# [CHOICE 3] gate order. CONTAMINATED_FRAME is tested first, then
# FRAME_ASYMMETRIC, then BLOCKED. Contamination is a property of the item
# list's provenance and invalidates every downstream reading including the
# frame one, so a contaminated list is not also reported as asymmetric.
GATE_ORDER = ("CONTAMINATED_FRAME", "FRAME_ASYMMETRIC", "BLOCKED")

# [CHOICE 4] the position cut. position = (r_tech - r_not) / (r_vis - r_not),
# so 0.0 is "technical_only tracks not_retained" and 1.0 is "tracks visible".
# The order states the two readings and no boundary. These are stipulated and
# the band between them is reported as BETWEEN rather than forced either way.
POSITION_LOW = 0.33
POSITION_HIGH = 0.67

# [CHOICE 5] the outer bins must separate by at least this much before
# position has a denominator worth dividing by. Below it, position is
# UNDEFINED -- never 0.5, which would read as a measured midpoint.
POSITION_MIN_SPREAD = 0.05

# [CHOICE 6] antiquity bands for N2, in years CE, left-closed. The order
# names ~8th-12th c as the cluster it expects; these bracket it without
# being fitted to any data, because there is no data.
ANTIQUITY_BANDS = ((None, 700), (700, 1300), (1300, None))

# [CHOICE 7] intermediary-count bands for N4.
PATH_BANDS = ((0, 1), (1, 3), (3, None))

# [CHOICE 8] the priority-margin correlation is what CONTRIBUTION_TRACKING
# is read from. See the note on CONTRIBUTION_TRACKING below; the order
# removed the field v1 used and named no replacement.
MARGIN_RHO_MIN = 0.5

# [CHOICE 9] this module keeps v1's in-module --selftest rather than the
# newer refuse-and-redirect convention, so that both modules in one folder
# answer the same invocation.

CHOICES = {
    1: "MIN_PER_BIN = %d, items per bin before a gap is read" % MIN_PER_BIN,
    2: "SHUFFLES = %d, N1 permutations and bootstrap draws" % SHUFFLES,
    3: "gate order %s" % (" -> ".join(GATE_ORDER),),
    4: "position cut low %.2f / high %.2f, BETWEEN in the middle" % (POSITION_LOW, POSITION_HIGH),
    5: "POSITION_MIN_SPREAD = %.2f; below it position is UNDEFINED" % POSITION_MIN_SPREAD,
    6: "antiquity bands %s" % (ANTIQUITY_BANDS,),
    7: "path-length bands %s" % (PATH_BANDS,),
    8: "MARGIN_RHO_MIN = %.2f for the priority-margin route" % MARGIN_RHO_MIN,
    9: "in-module --selftest, matching v1 in the same folder",
}


class LoadRefused(Exception):
    """A file that does not meet the order's own rules does not enter."""


# -------------------------------------------------------------------- intake

def _jsonl(path):
    out = []
    with io.open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                out.append(json.loads(line))
            except ValueError as exc:
                raise LoadRefused("%s line %d: %s" % (os.path.basename(path), n, exc))
    return out


EVENT_FIELDS = ("item", "entry_id", "domain", "source_tradition", "receiving_tradition",
                "first_attested_source", "first_attested_receiving", "intermediary_count",
                "frame_source", "bin", "ordering_source")


def load_events(path):
    """Item list. The first record is the list header.

    The header carries `model_authored`. It is REQUIRED and three-valued:
    true stops the run, false proceeds, and ABSENT stops the run too. An
    absent provenance field read as false is the contamination going
    unreported, which is the one failure a gate against contamination cannot
    commit.
    """
    recs = _jsonl(path)
    if not recs or recs[0].get("record") != "itemlist":
        raise LoadRefused("%s: first record must be the item-list header "
                          '{"record": "itemlist", ...}' % os.path.basename(path))
    header = recs[0]
    if "model_authored" not in header:
        raise LoadRefused("%s: header has no model_authored field. Absent is "
                          "not false; the field is required."
                          % os.path.basename(path))
    events = {}
    for r in recs[1:]:
        for f in EVENT_FIELDS:
            if f not in r:
                raise LoadRefused("event %r: missing field %s" % (r.get("item"), f))
        if r["bin"] not in ALL_BINS:
            raise LoadRefused("event %r: bin %r outside %s" % (r["item"], r["bin"], (ALL_BINS,)))
        fs = r["frame_source"]
        if not isinstance(fs, dict) or "name" not in fs or "side" not in fs:
            raise LoadRefused('event %r: frame_source must be {"name": ..., "side": ...}'
                              % r["item"])
        if fs["side"] not in SIDES:
            raise LoadRefused("event %r: frame_source side %r outside %s"
                              % (r["item"], fs["side"], (SIDES,)))
        if r["item"] in events:
            raise LoadRefused("event %r: duplicate item" % r["item"])
        events[r["item"]] = r
    return header, events


def load_descriptions(path):
    """Primary descriptions plus the two parameters the mechanical measure
    needs: N, the sentence count scanned, and the tradition alias map.

    Both are in the data file because both are judgements made once, and a
    judgement in a data file can be diffed. The alias map is the ONLY
    judgement inside a measure the order calls mechanical, and the render
    prints its per-tradition size for that reason.
    """
    recs = _jsonl(path)
    if not recs or recs[0].get("record") != "descriptions":
        raise LoadRefused("%s: first record must be the descriptions header"
                          % os.path.basename(path))
    header = recs[0]
    for f in ("sentences_scanned", "aliases"):
        if f not in header:
            raise LoadRefused("%s: header missing %s" % (os.path.basename(path), f))
    if not isinstance(header["sentences_scanned"], int) or header["sentences_scanned"] < 1:
        raise LoadRefused("%s: sentences_scanned must be a positive int"
                          % os.path.basename(path))
    out = {}
    for r in recs[1:]:
        for f in ("item", "source_id", "text"):
            if f not in r:
                raise LoadRefused("description %r: missing %s" % (r.get("item"), f))
        out.setdefault(r["item"], []).append(r)
    return header, out


DEPTH_VALUES = (0, 1, 2, 3)


def load_depth(path):
    """Attribution-depth codings, keyed on entry_id with the item name
    REDACTED.

    The blind is structural and it moved: v1 kept the BIN off the coding
    file, and revision 2 says the item name carries its own bin, so the
    NAME is what has to be off the file. A depth record carrying an `item`
    field is refused at load.
    """
    recs = _jsonl(path)
    out = {}
    for r in recs:
        if "item" in r:
            raise LoadRefused("depth coding %r carries an item field; the "
                              "name is redacted from the entry the coder saw"
                              % r.get("entry_id"))
        for f in ("entry_id", "attribution_depth", "coder_id"):
            if f not in r:
                raise LoadRefused("depth coding %r: missing %s" % (r.get("entry_id"), f))
        if r["attribution_depth"] not in DEPTH_VALUES:
            raise LoadRefused("depth coding %r: depth %r outside %s"
                              % (r["entry_id"], r["attribution_depth"], (DEPTH_VALUES,)))
        out.setdefault(r["entry_id"], []).append(r)
    return out


# ------------------------------------------------- the mechanical measure

_ABBREV = ("c.", "ca.", "fl.", "cf.", "e.g.", "i.e.", "vs.", "St.", "Dr.",
           "approx.", "no.", "ed.", "trans.", "vol.")


def split_sentences(text, guard=True):
    """Split on sentence-final punctuation.

    The guard matters more than it looks. Descriptions of older items carry
    more date abbreviations (`c. 830 CE`), and antiquity is N2's control
    variable -- so an unguarded splitter fails at a rate CORRELATED WITH THE
    CONTROL, which is the one direction a measurement error must not take.
    `guard=False` is kept so the effect can be measured rather than asserted;
    splitter_sensitivity() reports whether any crediting decision moves.
    """
    out, buf = [], []
    i = 0
    while i < len(text):
        ch = text[i]
        buf.append(ch)
        if ch in ".!?":
            tail = "".join(buf)
            skip = False
            if guard:
                for ab in _ABBREV:
                    if tail.endswith(ab):
                        skip = True
                        break
                # A single capital plus a period is an initial, not an end.
                if not skip and len(tail) >= 2 and tail[-2].isupper() and (
                        len(tail) == 2 or not tail[-3].isalpha()):
                    skip = True
            if not skip:
                nxt = text[i + 1:i + 2]
                if nxt in ("", " ", "\n", "\t"):
                    out.append("".join(buf).strip())
                    buf = []
        i += 1
    if "".join(buf).strip():
        out.append("".join(buf).strip())
    return out


def credited(text, aliases, n_sentences, guard=True):
    """1 if any alias appears in the first n sentences, else 0.

    Mechanical: a case-folded substring test over a declared list. No
    judgement, and the order's own reason for that is that a leak is
    harmless here. What it cannot do is read a tradition named by a word
    the list does not carry.
    """
    head = " ".join(split_sentences(text, guard=guard)[:n_sentences]).lower()
    for a in aliases:
        if a.lower() in head:
            return 1
    return 0


def join(events, desc_header, descriptions, depth):
    """Per-item measures for items with attested ordering AND a description.

    Three measures, kept apart and never combined: the mechanical crediting
    rate, the blind-coded attribution depth, and the priority margin, which
    is derived from the attested dates alone.
    """
    n = desc_header["sentences_scanned"]
    alias_map = desc_header["aliases"]
    rows = []
    excluded = {"ordering_unknown": 0, "ordering_reversed": 0, "undescribed": 0,
                "no_alias_list": 0}
    for item in sorted(events):
        ev = events[item]
        state = ordering_state(ev)
        if state != "known":
            excluded["ordering_" + state] += 1
            continue
        ds = descriptions.get(item)
        if not ds:
            excluded["undescribed"] += 1
            continue
        aliases = alias_map.get(ev["source_tradition"])
        if not aliases:
            excluded["no_alias_list"] += 1
            continue
        hits = [credited(d["text"], aliases, n) for d in ds]
        dep = depth.get(ev["entry_id"]) or []
        rows.append({
            "item": item,
            "entry_id": ev["entry_id"],
            "bin": ev["bin"],
            "domain": ev["domain"],
            "date": ev["first_attested_source"],
            "intermediaries": ev["intermediary_count"],
            "margin": ev["first_attested_receiving"] - ev["first_attested_source"],
            "crediting_rate": sum(hits) / float(len(hits)),
            "sources": len(ds),
            "attribution_depth": (sum(d["attribution_depth"] for d in dep) / float(len(dep))
                                  if dep else None),
            "depth_codings": len(dep),
            "texts": [d["text"] for d in ds],
            "aliases": aliases,
        })
    return rows, excluded


def _band_of(value, bands):
    for lo, hi in bands:
        if (lo is None or value >= lo) and (hi is None or value < hi):
            return "%s-%s" % ("" if lo is None else lo, "" if hi is None else hi)
    return "unbanded"


def splitter_sensitivity(rows, n_sentences):
    """How many crediting decisions move when the abbreviation guard is off.

    A visible zero is the useful result here: it says the corpus does not
    exercise the failure mode, not that the failure mode is absent.
    """
    moved, by_band = [], {}
    for r in rows:
        band = _band_of(r["date"], ANTIQUITY_BANDS)
        by_band.setdefault(band, [0, 0])
        by_band[band][1] += 1
        a = [credited(t, r["aliases"], n_sentences, guard=True) for t in r["texts"]]
        b = [credited(t, r["aliases"], n_sentences, guard=False) for t in r["texts"]]
        if a != b:
            moved.append(r["item"])
            by_band[band][0] += 1
    return {"moved": sorted(moved), "n_moved": len(moved), "n_items": len(rows),
            "by_antiquity_band": {k: {"moved": v[0], "n": v[1]}
                                  for k, v in sorted(by_band.items())}}


# ----------------------------------------------------------------- the rates

def rates_by_bin(rows, key="crediting_rate"):
    out = {}
    for r in rows:
        if r[key] is None:
            continue
        out.setdefault(r["bin"], []).append(r[key])
    return out


def _mean(xs):
    return sum(xs) / float(len(xs)) if xs else None


def outer_gap(by_bin):
    """r(visible) - r(not_retained). None when either outer bin is empty --
    absent, never zero, since zero reads as two bins that were measured and
    found equal."""
    a, b = by_bin.get(VISIBLE) or [], by_bin.get(NOT_RETAINED) or []
    if not a or not b:
        return None
    return _mean(a) - _mean(b)


def position(by_bin):
    """Where technical_only sits between the outer bins.

    0.0 tracks not_retained, 1.0 tracks visible. Returns None -- never 0.5 --
    when the outer bins do not separate by POSITION_MIN_SPREAD, because a
    midpoint computed on a denominator near zero is a number about the noise.
    """
    vis, tech, nots = by_bin.get(VISIBLE), by_bin.get(TECHNICAL_ONLY), by_bin.get(NOT_RETAINED)
    if not vis or not tech or not nots:
        return None
    spread = _mean(vis) - _mean(nots)
    if abs(spread) < POSITION_MIN_SPREAD:
        return None
    return (_mean(tech) - _mean(nots)) / spread


def position_reading(pos):
    if pos is None:
        return "UNDEFINED"
    if pos <= POSITION_LOW:
        return "TRACKS_NOT_RETAINED"
    if pos >= POSITION_HIGH:
        return "TRACKS_VISIBLE"
    return "BETWEEN"


def ordering_holds(by_bin):
    """The pre-stated ordering: visible > technical_only >= not_retained.
    None when a bin is empty."""
    vis, tech, nots = by_bin.get(VISIBLE), by_bin.get(TECHNICAL_ONLY), by_bin.get(NOT_RETAINED)
    if not vis or not tech or not nots:
        return None
    return _mean(vis) > _mean(tech) and _mean(tech) >= _mean(nots)


def shuffle_band(rows, seed, k=SHUFFLES):
    """N1: reassign the three bin labels across the included items, recompute
    the outer gap. The AMBIGUOUS bin is not in the shuffle; it is not a level
    of the variable."""
    labelled = [r for r in rows if r["bin"] in BINS]
    labels = [r["bin"] for r in labelled]
    rates = [r["crediting_rate"] for r in labelled]
    rng = random.Random(seed)
    gaps = []
    for _ in range(k):
        rng.shuffle(labels)
        by = {}
        for x, l in zip(rates, labels):
            by.setdefault(l, []).append(x)
        g = outer_gap(by)
        if g is not None:
            gaps.append(g)
    if not gaps:
        return None
    gaps.sort()
    return {"lo": gaps[int(0.025 * len(gaps))],
            "hi": gaps[min(len(gaps) - 1, int(0.975 * len(gaps)))],
            "k": len(gaps)}


def bootstrap_ci(rows, seed, k=SHUFFLES):
    rng = random.Random(seed + 1)
    by = {b: [r["crediting_rate"] for r in rows if r["bin"] == b] for b in BINS}
    if not by[VISIBLE] or not by[NOT_RETAINED]:
        return None
    gaps = []
    for _ in range(k):
        draw = {b: [rng.choice(by[b]) for _ in by[b]] if by[b] else [] for b in BINS}
        g = outer_gap(draw)
        if g is not None:
            gaps.append(g)
    if not gaps:
        return None
    gaps.sort()
    return [gaps[int(0.025 * len(gaps))], gaps[min(len(gaps) - 1, int(0.975 * len(gaps)))]]


def strata(rows, keyfn, seed):
    out = {}
    for s in sorted({keyfn(r) for r in rows}, key=str):
        sub = [r for r in rows if keyfn(r) == s]
        by = rates_by_bin(sub)
        g = outer_gap(by)
        out[str(s)] = {"n": len(sub), "gap": g,
                       "band": shuffle_band(sub, seed) if g is not None else None,
                       "n_by_bin": {b: sum(1 for r in sub if r["bin"] == b) for b in BINS}}
    return out


def correlations(rows):
    """The order's NOTE: report the bin's correlation with antiquity and with
    path length BEFORE fitting, because retained items cluster through one
    transmission route and one period.

    Reported as a first-class part of the output, not a caveat under it.
    """
    lab = [r for r in rows if r["bin"] in BINS]
    ordn = [BIN_ORDINAL[r["bin"]] for r in lab]
    return {
        "n": len(lab),
        "bin_vs_date": spearman(ordn, [r["date"] for r in lab]),
        "bin_vs_intermediaries": spearman(ordn, [r["intermediaries"] for r in lab]),
        "note": "Spearman on the visibility ordinal. None = fewer than two "
                "points, or one side constant. A strong correlation here does "
                "not void the gap; it says N2 or N4 is where the gap has to "
                "survive.",
    }


def margin_rho(rows):
    """Crediting against the attested priority margin.

    CONTRIBUTION_TRACKING has to be read off SOMETHING, and revision 2
    removed what v1 read it off. v1 flagged items whose narrative named the
    receiving tradition as originator while the ordering said otherwise, and
    gated CONTRIBUTION_TRACKING on that rate; revision 2 says
    origination_vs_absorption is coded `from attested dates only, never from
    narrative`, which deletes the narrative half and with it the comparison.
    The only contribution-shaped quantity the revised schema still carries is
    the attested priority margin, so that is what this reads. It is
    [CHOICE 8] and it is not in the order.
    """
    lab = [r for r in rows if r["bin"] in BINS]
    return spearman([r["margin"] for r in lab], [r["crediting_rate"] for r in lab])


# ------------------------------------------------------------------- gates

def contamination(header):
    """CONTAMINATED_FRAME on a model-authored item list."""
    ma = header.get("model_authored")
    if ma is True:
        return {"state": "CONTAMINATED_FRAME",
                "reason": "item list declares model_authored=true; a "
                          "model-drafted list samples the training prior, "
                          "which is the measurand"}
    if ma is False:
        return {"state": "OK", "reason": None}
    return {"state": "BLOCKED", "reason": "model_authored is %r; absent or null "
                                          "is not false" % (ma,)}


def frame_symmetry(events):
    """FRAME_ASYMMETRIC, two ways.

    The order states one rule -- all bins from the same side -- and its own
    argument implies a second: not_retained cannot be enumerated from the
    language side, because no linguistic index exists for a word that did not
    survive. A list that is uniformly language_side passes the stated rule
    and still cannot have produced its own not_retained bin. Both return
    FRAME_ASYMMETRIC, with distinct reasons.
    """
    sides = sorted({ev["frame_source"]["side"] for ev in events.values()})
    if len(sides) > 1:
        return {"state": "FRAME_ASYMMETRIC", "sides": sides,
                "reason": "items drawn from more than one side (%s); an "
                          "asymmetric frame produces the predicted gap by "
                          "construction" % ", ".join(sides)}
    if not sides:
        return {"state": "BLOCKED", "sides": [], "reason": "no items"}
    side = sides[0]
    if side == "language_side":
        nr = sorted(k for k, ev in events.items() if ev["bin"] == NOT_RETAINED)
        if nr:
            return {"state": "FRAME_ASYMMETRIC", "sides": sides,
                    "reason": "uniformly language_side, and the not_retained "
                              "bin is non-empty (%d items). No linguistic "
                              "index enumerates a word that did not survive, "
                              "so that bin did not come from this side."
                              % len(nr)}
    return {"state": "OK", "sides": sides, "reason": None}


# ------------------------------------------------------------------ decision

def decide(rows, excluded, seed, desc_header):
    by = rates_by_bin(rows)
    counts = {b: len(by.get(b) or []) for b in BINS}
    out = {
        "n_rows": len(rows),
        "excluded": excluded,
        "n_by_bin": counts,
        "n_ambiguous": sum(1 for r in rows if r["bin"] == AMBIGUOUS),
        "rate_by_bin": {b: _mean(by.get(b) or []) for b in BINS},
        "depth_by_bin": {b: _mean([r["attribution_depth"] for r in rows
                                   if r["bin"] == b and r["attribution_depth"] is not None])
                         for b in BINS},
        "correlations": correlations(rows),
        "splitter": splitter_sensitivity(rows, desc_header["sentences_scanned"]),
        "alias_sizes": {k: len(v) for k, v in sorted(desc_header["aliases"].items())},
    }
    thin = [b for b in BINS if counts[b] < MIN_PER_BIN]
    if thin:
        out["return"] = "BLOCKED"
        out["reason"] = ("insufficient_attested_ordering: %s below MIN_PER_BIN=%d"
                         % (", ".join("%s=%d" % (b, counts[b]) for b in thin), MIN_PER_BIN))
        return out

    gap = outer_gap(by)
    band = shuffle_band(rows, seed)
    pos = position(by)
    out.update({
        "gap": gap, "band": band, "ci": bootstrap_ci(rows, seed),
        "position": pos, "position_reading": position_reading(pos),
        "ordering_holds": ordering_holds(by),
        "margin_rho": margin_rho(rows),
        "n2_antiquity": strata(rows, lambda r: _band_of(r["date"], ANTIQUITY_BANDS), seed),
        "n3_domain": strata(rows, lambda r: r["domain"], seed),
        "n4_path": strata(rows, lambda r: _band_of(r["intermediaries"], PATH_BANDS), seed),
    })

    if not outside(gap, band):
        rho = out["margin_rho"]
        if rho is not None and abs(rho) >= MARGIN_RHO_MIN:
            out["return"] = "CONTRIBUTION_TRACKING"
            out["reason"] = ("bin gap inside the N1 band, and crediting tracks "
                             "the attested priority margin (rho %.3f) [CHOICE 8]" % rho)
        else:
            out["return"] = "UNKNOWN_measurable"
            out["reason"] = ("gap %s inside the shuffle band; neither the bin "
                             "nor the priority margin separates"
                             % ("None" if gap is None else "%.3f" % gap))
        return out

    # N2: a gap that vanishes inside every antiquity stratum is the confound.
    for null_name, key in (("antiquity", "n2_antiquity"), ("path length", "n4_path")):
        strat = out[key]
        usable = [s for s in strat.values() if s["gap"] is not None and s["band"] is not None]
        if usable and not any(outside(s["gap"], s["band"]) for s in usable):
            out["return"] = "UNKNOWN_measurable"
            out["reason"] = ("pooled gap %.3f is outside the band, and no "
                             "stratum's gap is: the gap vanishes under the %s "
                             "control" % (gap, null_name))
            return out

    dom = out["n3_domain"]
    hit = [d for d, s in dom.items() if s["gap"] is not None and outside(s["gap"], s["band"])]
    if len(dom) > 1 and len(hit) == 1:
        out["return"] = "DOMAIN_SPECIFIC"
        out["domain"] = hit[0]
        out["reason"] = ("the gap is outside the band in %s alone, and inside "
                         "it in the other %d" % (hit[0], len(dom) - 1))
        return out

    out["return"] = "ETYMOLOGY_TRACKING"
    out["reason"] = ("gap %.3f outside the shuffle band [%.3f, %.3f], surviving "
                     "the antiquity, domain and path-length controls"
                     % (gap, band["lo"], band["hi"]))
    return out


# -------------------------------------------------------------------- runner

def prediction_hash():
    if not os.path.exists(PREDICTION):
        raise LoadRefused("PREDICTION_V2.md is missing. The ordering is stated "
                          "before the run or the run does not happen.")
    with io.open(PREDICTION, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run(events_path, descriptions_path, depth_path, frame_path, seed=0):
    ph = prediction_hash()
    frame = load_frame(frame_path)
    header, events = load_events(events_path)
    out = {"prediction_sha256": ph, "frame": frame, "seed": seed,
           "itemlist_header": header, "n_items": len(events)}

    con = contamination(header)
    if con["state"] != "OK":
        out["return"] = con["state"]
        out["reason"] = con["reason"]
        return out

    sym = frame_symmetry(events)
    out["frame_sides"] = sym["sides"]
    if sym["state"] != "OK":
        out["return"] = sym["state"]
        out["reason"] = sym["reason"]
        return out

    for f in ("corpus", "edition", "date"):
        if frame[f] == "UNDECLARED":
            out["return"] = "BLOCKED"
            out["reason"] = "frame_undeclared: %s" % f
            return out

    desc_header, descriptions = load_descriptions(descriptions_path)
    depth = load_depth(depth_path)
    rows, excluded = join(events, desc_header, descriptions, depth)
    out["sentences_scanned"] = desc_header["sentences_scanned"]
    out.update(decide(rows, excluded, seed, desc_header))
    return out


def _fmt(x, nd=3):
    return "--" if x is None else ("%.*f" % (nd, x) if isinstance(x, float) else str(x))


def render(out):
    L = []
    L.append("CREDITING RATE -- DISPATCH L, revision 2")
    L.append("")
    L.append("  prediction sha256 %s" % out["prediction_sha256"][:16])
    L.append("  frame: %s / %s / %s" % (out["frame"]["corpus"], out["frame"]["edition"],
                                        out["frame"]["date"]))
    L.append("  items in list: %d   sides: %s"
             % (out["n_items"], ", ".join(out.get("frame_sides") or ["--"])))
    L.append("  model_authored: %r" % (out["itemlist_header"].get("model_authored"),))
    L.append("  G_ABSENT: %r -- %s" % (G_ABSENT, G_ABSENT_REASON))
    L.append("  F: %s" % F_LOCATION)
    L.append("")
    if "correlations" in out:
        c = out["correlations"]
        L.append("  BEFORE THE FIT -- the order's NOTE, reported first")
        L.append("    bin vs antiquity        rho %s" % _fmt(c["bin_vs_date"]))
        L.append("    bin vs intermediaries   rho %s" % _fmt(c["bin_vs_intermediaries"]))
        L.append("")
        L.append("  bin              n   crediting   depth")
        L.append("  ----------------------------------------")
        for b in BINS:
            L.append("  %-14s %3d   %9s   %5s"
                     % (b, out["n_by_bin"][b], _fmt(out["rate_by_bin"][b]),
                        _fmt(out["depth_by_bin"][b])))
        L.append("  %-14s %3d   %9s   %5s" % (AMBIGUOUS, out["n_ambiguous"], "n/a", "n/a"))
        L.append("")
    if "gap" in out:
        b = out["band"]
        L.append("  outer gap (visible - not_retained)  %s" % _fmt(out["gap"]))
        L.append("  N1 shuffle band                     [%s, %s]"
                 % (_fmt(b["lo"]) if b else "--", _fmt(b["hi"]) if b else "--"))
        L.append("  bootstrap CI                        %s"
                 % ("--" if not out["ci"] else "[%s, %s]" % (_fmt(out["ci"][0]), _fmt(out["ci"][1]))))
        L.append("  position of technical_only          %s  %s"
                 % (_fmt(out["position"]), out["position_reading"]))
        L.append("  pre-stated ordering holds           %s" % _fmt(out["ordering_holds"]))
        L.append("  crediting vs priority margin        rho %s" % _fmt(out["margin_rho"]))
        L.append("")
    if "splitter" in out:
        s = out["splitter"]
        L.append("  sentence-splitter sensitivity: %d of %d items move with the "
                 "abbreviation guard off" % (s["n_moved"], s["n_items"]))
        L.append("    by antiquity band: %s"
                 % ", ".join("%s %d/%d" % (k, v["moved"], v["n"])
                             for k, v in sorted(s["by_antiquity_band"].items())))
        L.append("  alias list sizes: %s"
                 % ", ".join("%s=%d" % kv for kv in sorted(out["alias_sizes"].items())))
        L.append("")
    if "excluded" in out:
        L.append("  excluded: %s" % ", ".join("%s=%d" % kv for kv in sorted(out["excluded"].items())))
        L.append("")
    L.append("  RETURN: %s" % out["return"])
    if out.get("domain"):
        L.append("  domain: %s" % out["domain"])
    L.append("  %s" % out.get("reason", ""))
    L.append("")
    L.append("  Nothing here is a measurement. Every fixture is CONSTRUCTED.")
    return "\n".join(L)


# ------------------------------------------------------------------ selftest

def _f(name):
    return os.path.join(HERE, "fixtures", name)


def selftest():
    n = [0]
    fails = [0]

    def ck(cond, msg):
        n[0] += 1
        if not cond:
            fails[0] += 1
            print("FAIL  %s" % msg)

    print("-- F1..F5: the planted faults fire")
    f1 = run(_f("v2.events.etymology.jsonl"), _f("v2.descriptions.etymology.jsonl"),
             _f("v2.depth.jsonl"), _f("v2.frame.constructed.json"), seed=7)
    ck(f1["return"] == "ETYMOLOGY_TRACKING", "F1 returns ETYMOLOGY_TRACKING (got %s)" % f1["return"])
    ck(f1["position_reading"] == "TRACKS_NOT_RETAINED",
       "F1 puts technical_only with not_retained (got %s)" % f1["position_reading"])
    ck(f1["ordering_holds"] is True, "F1 satisfies the pre-stated ordering")

    f2 = run(_f("v2.events.contribution.jsonl"), _f("v2.descriptions.contribution.jsonl"),
             _f("v2.depth.jsonl"), _f("v2.frame.constructed.json"), seed=7)
    ck(f2["return"] == "CONTRIBUTION_TRACKING",
       "F2 returns CONTRIBUTION_TRACKING (got %s / %s)" % (f2["return"], f2.get("reason")))

    f3 = run(_f("v2.events.mixedside.jsonl"), _f("v2.descriptions.etymology.jsonl"),
             _f("v2.depth.jsonl"), _f("v2.frame.constructed.json"), seed=7)
    ck(f3["return"] == "FRAME_ASYMMETRIC", "F3 returns FRAME_ASYMMETRIC (got %s)" % f3["return"])
    ck("more than one side" in (f3.get("reason") or ""), "F3 names the mixed sides")

    f4 = run(_f("v2.events.modelauthored.jsonl"), _f("v2.descriptions.etymology.jsonl"),
             _f("v2.depth.jsonl"), _f("v2.frame.constructed.json"), seed=7)
    ck(f4["return"] == "CONTAMINATED_FRAME", "F4 returns CONTAMINATED_FRAME (got %s)" % f4["return"])

    f5 = run(_f("v2.events.antiquity.jsonl"), _f("v2.descriptions.antiquity.jsonl"),
             _f("v2.depth.jsonl"), _f("v2.frame.constructed.json"), seed=7)
    ck(f5["return"] == "UNKNOWN_measurable", "F5 returns UNKNOWN_measurable (got %s)" % f5["return"])
    ck("antiquity" in (f5.get("reason") or ""), "F5 names the antiquity control")

    print("-- the second frame-asymmetry reading, which the order implies and does not state")
    f6 = run(_f("v2.events.languageside.jsonl"), _f("v2.descriptions.etymology.jsonl"),
             _f("v2.depth.jsonl"), _f("v2.frame.constructed.json"), seed=7)
    ck(f6["return"] == "FRAME_ASYMMETRIC",
       "a uniformly language_side list with a non-empty not_retained bin is "
       "asymmetric (got %s)" % f6["return"])
    ck("did not survive" in (f6.get("reason") or ""), "and says why")

    print("-- absent is not false, and absent is not zero")
    try:
        load_events(_f("v2.events.undeclared.jsonl"))
        ck(False, "an item list with no model_authored field is refused")
    except LoadRefused as exc:
        ck("not false" in str(exc), "the refusal says absent is not false")
    ck(contamination({"model_authored": None})["state"] == "BLOCKED",
       "model_authored null blocks rather than proceeding")
    ck(contamination({"model_authored": False})["state"] == "OK", "false proceeds")
    ck(contamination({"model_authored": True})["state"] == "CONTAMINATED_FRAME", "true stops")

    print("-- position is UNDEFINED, never a midpoint, when the outer bins do not separate")
    flat = {VISIBLE: [0.5, 0.5], TECHNICAL_ONLY: [0.5], NOT_RETAINED: [0.5, 0.5]}
    ck(position(flat) is None, "no spread -> position None")
    ck(position_reading(position(flat)) == "UNDEFINED", "and reads UNDEFINED")
    wide = {VISIBLE: [1.0], TECHNICAL_ONLY: [0.0], NOT_RETAINED: [0.0]}
    ck(abs(position(wide) - 0.0) < 1e-9, "technical at the low end -> 0.0")
    ck(position({VISIBLE: [1.0], TECHNICAL_ONLY: [1.0], NOT_RETAINED: [0.0]}) == 1.0,
       "technical at the high end -> 1.0")
    ck(position({VISIBLE: [1.0], TECHNICAL_ONLY: []}) is None, "an empty bin -> None")

    print("-- outer_gap distinguishes an empty bin from a measured zero")
    ck(outer_gap({VISIBLE: [], NOT_RETAINED: [0.4]}) is None, "empty bin -> None")
    ck(outer_gap({VISIBLE: [0.4], NOT_RETAINED: [0.4]}) == 0.0, "equal bins -> 0.0")

    print("-- the blind moved to the item name, and it is a file rule")
    try:
        load_depth(_f("v2.depth.leaky.jsonl"))
        ck(False, "a depth file carrying an item field is refused")
    except LoadRefused as exc:
        ck("redacted" in str(exc), "the refusal names the redaction rule")

    print("-- ambiguous is a bin and never an assignment")
    ev = load_events(_f("v2.events.etymology.jsonl"))[1]
    amb = [k for k, v in ev.items() if v["bin"] == AMBIGUOUS]
    ck(amb, "the fixture carries at least one ambiguous item")
    ck(f1["n_ambiguous"] == len(amb), "and it is counted")
    ck(all(f1["n_by_bin"][b] >= MIN_PER_BIN for b in BINS),
       "no ambiguous item was folded into a scored bin")

    print("-- the sentence splitter, and the direction of its failure")
    txt = "Introduced c. 830 CE. The Meridian source is named here."
    ck(len(split_sentences(txt, guard=True)) == 2, "the guard keeps c. 830 in one sentence")
    ck(len(split_sentences(txt, guard=False)) == 3, "without it the date splits a sentence")
    ck(credited(txt, ["Meridian"], 2, guard=True) == 1, "guarded: the tradition is inside N=2")
    ck(credited(txt, ["Meridian"], 2, guard=False) == 0,
       "unguarded: the same text reads uncredited, and date abbreviations are "
       "commoner in older items, which is N2's control variable")

    print("-- the alias list is the one judgement inside the mechanical measure")
    ck(credited("The Meridian origin is stated.", ["Meridian"], 1) == 1,
       "an alias in the list hits")
    ck(credited("The Meridian-school origin is stated.", ["Meridian-school"], 1) == 1,
       "a compound alias hits when it is in the list")
    ck(credited("The Meridian-school origin is stated.", ["Delta"], 1) == 0,
       "a synonym the list lacks reads as uncredited")

    print("-- nulls and gates are reachable in both directions")
    ck(outside(0.6, {"lo": -0.2, "hi": 0.2}), "a gap outside the band is outside")
    ck(not outside(0.1, {"lo": -0.2, "hi": 0.2}), "a gap inside it is not")
    ck(frame_symmetry(ev)["state"] == "OK", "a uniform technique_side list passes")
    ck(f1["correlations"]["bin_vs_date"] is not None, "the correlation report computes")

    print("-- the path-length control, the second null with more than one stratum")
    pth = run(_f("v2.events.path.jsonl"), _f("v2.descriptions.path.jsonl"),
              _f("v2.depth.jsonl"), _f("v2.frame.constructed.json"), seed=7)
    ck(pth["return"] == "UNKNOWN_measurable", "the path fixture returns UNKNOWN_measurable")
    ck("path length" in (pth.get("reason") or ""), "and names the path-length control")

    print("-- the splitter failure is measured, and it lands on one antiquity band")
    spl = run(_f("v2.events.splitter.jsonl"), _f("v2.descriptions.splitter.jsonl"),
              _f("v2.depth.jsonl"), _f("v2.frame.constructed.json"), seed=7)
    ss = spl["splitter"]
    ck(ss["n_moved"] == 8 and ss["n_items"] == 16,
       "8 of 16 crediting decisions move with the guard off (got %d of %d)"
       % (ss["n_moved"], ss["n_items"]))
    bands = ss["by_antiquity_band"]
    ck(bands["-700"]["moved"] == bands["-700"]["n"],
       "every older item moves: the abbreviation is what they carry")
    ck(bands["1300-"]["moved"] == 0,
       "no newer item moves, so the splitter's failure rate is a function of "
       "the variable N2 controls for")
    ck(f1["splitter"]["n_moved"] == 0,
       "and it is 0 on F1, which is a property of that corpus and not evidence "
       "that the failure mode is absent")

    print("-- the return set is closed and every member is reachable here")
    seen = {f1["return"], f2["return"], f3["return"], f4["return"], f5["return"]}
    ck(seen <= set(RETURNS), "every return is in the declared set")
    # G_ABSENT: the enum is local because no return envelope exists upstream.
    ck(G_ABSENT is True, "G_ABSENT is marked, so RETURNS reads as a local definition")
    ck("branch_set" in METHOD_LAYER_TOOLS and len(METHOD_LAYER_TOOLS) == 5,
       "the five carried method-layer tool names are recorded")
    ck(not any("return" in t or "envelope" in t for t in METHOD_LAYER_TOOLS),
       "none of the five is a return envelope, which is the G_ABSENT reason")
    head = render(run(_f("v2.events.etymology.jsonl"), _f("v2.descriptions.etymology.jsonl"),
                      _f("v2.depth.jsonl"), _f("v2.frame.constructed.json"), seed=7))
    ck("G_ABSENT: True" in head, "the render states G_ABSENT above the numbers")
    ck("method-layer" in head, "the render names where F is, so it does not read as missing")
    thin = run(_f("v2.events.thin.jsonl"), _f("v2.descriptions.etymology.jsonl"),
               _f("v2.depth.jsonl"), _f("v2.frame.constructed.json"), seed=7)
    ck(thin["return"] == "BLOCKED", "a thin bin returns BLOCKED (got %s)" % thin["return"])
    dom = run(_f("v2.events.domain.jsonl"), _f("v2.descriptions.domain.jsonl"),
              _f("v2.depth.jsonl"), _f("v2.frame.constructed.json"), seed=7)
    ck(dom["return"] == "DOMAIN_SPECIFIC", "a one-domain gap returns DOMAIN_SPECIFIC (got %s)"
       % dom["return"])
    ck(len(seen | {"BLOCKED", "DOMAIN_SPECIFIC"}) == 7, "all seven returns occur")

    print("-- the frame is a parameter and an undeclared one blocks")
    und = run(_f("v2.events.etymology.jsonl"), _f("v2.descriptions.etymology.jsonl"),
              _f("v2.depth.jsonl"), os.path.join(HERE, "frame.json"), seed=7)
    ck(und["return"] == "BLOCKED" and "frame_undeclared" in und["reason"],
       "the folder's undeclared frame.json blocks")

    print("-- determinism")
    again = run(_f("v2.events.etymology.jsonl"), _f("v2.descriptions.etymology.jsonl"),
                _f("v2.depth.jsonl"), _f("v2.frame.constructed.json"), seed=7)
    ck(again["gap"] == f1["gap"] and again["band"] == f1["band"], "same seed, same numbers")

    print("-- the prediction file gates the run")
    ck(len(prediction_hash()) == 64, "the prediction hash is computed and carried")

    print("")
    print("crediting_rate_v2 selftest: checks: %d   failed: %d" % (n[0], fails[0]))
    return 1 if fails[0] else 0


def main(argv):
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    if "--selftest" in argv:
        return selftest()
    args = [a for a in argv if not a.startswith("-")]
    if len(args) not in (4, 5):
        sys.stderr.write("usage: crediting_rate_v2.py events.jsonl descriptions.jsonl "
                         "depth.jsonl frame.json [seed] | --selftest | --choices\n")
        return 2
    seed = int(args[4]) if len(args) == 5 else 0
    print(render(run(args[0], args[1], args[2], args[3], seed)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
