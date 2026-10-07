#!/usr/bin/env python3
# crediting_rate_v2.py -- WORK ORDER L, REVISED 2026-09-23. CC0, stdlib
# only, parses under 3.9.
#
# Does attribution of an imported technique track CONTRIBUTION or
# LOANWORD VISIBILITY? A rate comparison across bins. Never an argument
# about any single case.
#
#   python3 crediting_rate_v2.py events.jsonl mechanical.jsonl \
#       depth.jsonl frame.json [seed]
#   python3 crediting_rate_v2.py --selftest
#   python3 crediting_rate_v2.py --choices
#
# PROVENANCE OF THE REVISION -- read this before the numbers.
#   The dispatch bundle that carried this order says of it, in the
#   operator's own send-order table:
#
#       "3  L  crediting_rate REVISED  not sent (three revisions are
#        Claude's, PROPOSED, adopt or strip before sending)"
#
#   It was then sent as delivered.  So the three revisions this module
#   implements -- the three-state bin, REVISION 1 (frame gate),
#   REVISION 2 (coding split) -- are MODEL-AUTHORED proposals that the
#   operator neither adopted nor stripped, and they arrive
#   un-adjudicated.  They are built because the order was sent; they are
#   not the operator's position.  AUDIT_CONTRACT.md's layer-separation
#   rule: a co-produced document is layered before it is audited, so the
#   layer is named here rather than inferred later.  v1's order
#   (WORK_ORDER.md) has no such note and is the operator's.
#
# v1 IS NOT EDITED.  crediting_rate.py and WORK_ORDER.md stay as
# delivered; this module IMPORTS v1 for every piece the revision does
# not change (bin_gap, shuffle_band, bootstrap_ci, strata, outside,
# load_frame, prediction_hash) rather than restating it -- MF_019, and
# five stale copies of one gate across three drops is what retyping
# costs.  Where v1 and v2 disagree the difference is a property of the
# revision and is reported, never smoothed.
#
# BUILD ON CONSTRUCTED DATA.  Real run NOT_RUN: the order's own
# REAL-RUN SPEC names an unidentified technique-side transmission
# catalogue as the one piece needing a human with library access.

import hashlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import crediting_rate as V1            # noqa: E402  the delivered module

PREDICTION_V2 = os.path.join(HERE, "PREDICTION_V2.md")
BRANCH_SET_V2 = os.path.join(HERE, "branch_set_v2.json")

# ---------------------------------------------------------------- F / G
# "Same F/G check-first as K."  enclosure-first-residual/ answered it by
# LOCATING the sibling checkout; crediting-rate v1's CRD_006 answered it
# "not in this tree" and built G locally.  Both were true of what each
# could see: v1 looked inside Simulators, K looks for a sibling repo.
# This locates it the way K does and reports which answer applies.


def _find_method_layer():
    env = os.environ.get("METHOD_LAYER_PATH")
    if env == "none":
        return None
    cands = [env] if env else []
    up1 = os.path.dirname(HERE)
    up2 = os.path.dirname(up1)
    for base in (up1, up2, os.path.dirname(up2)):
        cands.append(os.path.join(base, "method-layer"))
        cands.append(os.path.join(base, "jinnz2", "method-layer"))
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "branch_set.py")) and \
                os.path.isfile(os.path.join(c, "preference_free_rank.py")):
            return c
    return None


METHOD_LAYER_PATH = _find_method_layer()
if METHOD_LAYER_PATH and METHOD_LAYER_PATH not in sys.path:
    sys.path.insert(0, METHOD_LAYER_PATH)
try:
    import branch_set as F                     # noqa: E402
    import preference_free_rank as G           # noqa: E402
    METHOD_LAYER = "present"
except Exception:                              # pragma: no cover
    F = None
    G = None
    METHOD_LAYER = "absent"

# ------------------------------------------------------------- the bins
# REVISED: three states on VISIBILITY to a general reader, plus ambiguous
# in its own bin and never assigned.
VISIBLE = "visible"
TECHNICAL_ONLY = "technical_only"
NOT_RETAINED = "not_retained"
AMBIGUOUS = "ambiguous"
BINS = (VISIBLE, TECHNICAL_ONLY, NOT_RETAINED)
ALL_BINS = BINS + (AMBIGUOUS,)

# Which side a bin CAN be enumerated from, per REVISION 1.
LANGUAGE_SIDE = "language"
TECHNIQUE_SIDE = "technique"
SIDES = (LANGUAGE_SIDE, TECHNIQUE_SIDE)
ENUMERABLE_FROM = {
    VISIBLE: (LANGUAGE_SIDE, TECHNIQUE_SIDE),
    TECHNICAL_ONLY: (LANGUAGE_SIDE, TECHNIQUE_SIDE),
    # no linguistic index exists because the word did not survive
    NOT_RETAINED: (TECHNIQUE_SIDE,),
    AMBIGUOUS: (LANGUAGE_SIDE, TECHNIQUE_SIDE),
}

# ------------------------------------------------------------- returns
ETYMOLOGY_TRACKING = "ETYMOLOGY_TRACKING"
CONTRIBUTION_TRACKING = "CONTRIBUTION_TRACKING"
UNKNOWN_MEASURABLE = "UNKNOWN_measurable"
DOMAIN_SPECIFIC = "DOMAIN_SPECIFIC"
BLOCKED = "BLOCKED"
FRAME_ASYMMETRIC = "FRAME_ASYMMETRIC"
CONTAMINATED_FRAME = "CONTAMINATED_FRAME"

MIN_PER_BIN = V1.MIN_PER_BIN     # imported, not restated
SHUFFLES = V1.SHUFFLES

# [CHOICE 6], and it is the load-bearing one.
#
# v1's CONTRIBUTION_TRACKING fires on a gap INSIDE the shuffle band AND a
# misattribution rate at or below MISATTR_MAX, where `misattributed` is
# derived from `described_originator == "receiving"` -- a per-coding field.
# REVISION 2 replaces that field with "origination_vs_absorption coded
# from attested dates only, never from narrative", which is an ORDERING
# and not a misattribution rate.  So the revision removes the input its
# own RETURN block still lists a class for: without a replacement
# discriminator, CONTRIBUTION_TRACKING is unreachable in v2 and every
# null gap lands on UNKNOWN_measurable.
#
# The replacement declared here is attribution_depth, the one crediting
# measure REVISION 2 keeps: a null gap with credit actually flowing is
# contribution tracking; a null gap with nobody crediting anyone is not,
# because then the bin cannot be the variable.  The cut is stipulated and
# has no derivation, exactly as MISATTR_MAX had none.
DEPTH_CREDITING_CUT = 1.5

# [CHOICE 1] the mechanical match is case-insensitive on a word boundary.
# A tradition name is a proper noun and sentence-initial capitalisation
# would otherwise decide the measure.
# [CHOICE 2] a sentence boundary is . ! ? followed by whitespace or end.
# [CHOICE 3] the depth file's join key is sha256(item + salt)[:16], with
# the salt in the events file, so the handle carries no readable content.
# UNI_078: an "opaque handle" that spells out the arm is not opaque.
# [CHOICE 4] N is read from the mechanical data file per corpus, never a
# module constant -- the order says "N in data file".
# [CHOICE 5] DOMAIN_SPECIFIC fires when exactly one domain's gap clears
# its own N1 band and the pooled gap does not.

EVENT_FIELDS = ("item", "domain", "source_tradition", "receiving_tradition",
                "first_attested_source", "first_attested_receiving",
                "intermediary_count", "bin", "frame_source", "side",
                "ordering_source", "entry_id")
MECH_FIELDS = ("item", "source_id", "description", "sentences_scored")
DEPTH_FIELDS = ("entry_id", "source_id", "coder_id", "attribution_depth")


class FrameError(ValueError):
    pass


def _jsonl(path):
    return V1._jsonl(path)          # imported


def _is_int(x):
    return V1._is_int(x)            # imported


def entry_id(item, salt):
    h = hashlib.sha256((item + "|" + salt).encode("utf-8")).hexdigest()
    return h[:16]


# ------------------------------------------------------------- loaders

def load_events(path):
    """REVISION 1's two gates live here, at load, before any rate exists."""
    out = {}
    manifest = {"model_authored": None, "salt": None}
    for n, r in _jsonl(path):
        if "_manifest" in r:
            m = r["_manifest"]
            for f in ("model_authored", "salt"):
                if f not in m:
                    raise FrameError(
                        "events line %d: _manifest missing %s" % (n, f))
            if not isinstance(m["model_authored"], bool):
                raise FrameError(
                    "events line %d: model_authored must be a boolean; an "
                    "absent declaration is not False" % n)
            manifest.update(m)
            continue
        for f in EVENT_FIELDS:
            if f not in r:
                raise FrameError(
                    "events line %d: missing field %s" % (n, f))
        if r["bin"] not in ALL_BINS:
            raise FrameError("events line %d: bin must be one of %s"
                             % (n, ALL_BINS))
        if r["side"] not in SIDES:
            raise FrameError("events line %d: side must be one of %s"
                             % (n, SIDES))
        if not r["frame_source"]:
            raise FrameError("events line %d: frame_source is required; "
                             "REVISION 1 makes it a hard gate" % n)
        for f in ("first_attested_source", "first_attested_receiving",
                  "intermediary_count"):
            if r[f] is not None and not _is_int(r[f]):
                raise FrameError(
                    "events line %d: %s must be an integer or null" % (n, f))
        if r["item"] in out:
            raise FrameError("events line %d: duplicate item %s"
                             % (n, r["item"]))
        out[r["item"]] = r
    if manifest["model_authored"] is None:
        raise FrameError(
            "events: no _manifest line.  REVISION 1 requires an explicit "
            "model_authored declaration; an absent one is not False")
    if manifest["salt"] is None:
        raise FrameError("events: _manifest missing the entry_id salt")
    for it, r in out.items():
        want = entry_id(it, manifest["salt"])
        if r["entry_id"] != want:
            raise FrameError(
                "events: entry_id for %s is not sha256(item|salt)[:16]" % it)
    return out, manifest


def load_mechanical(path):
    """The crediting measure's INPUT, not its verdict.  Leak harmless --
    no judgment is coded here, so the item name may stay in the clear."""
    out = {}
    for n, r in _jsonl(path):
        for f in MECH_FIELDS:
            if f not in r:
                raise ValueError("mechanical line %d: missing field %s"
                                 % (n, f))
        if not _is_int(r["sentences_scored"]) or r["sentences_scored"] < 1:
            raise ValueError("mechanical line %d: sentences_scored must be a "
                             "positive integer (the order's N, in data)" % n)
        out.setdefault(r["item"], []).append(r)
    return out


def load_depth(path):
    """attribution_depth, coded with the item name REDACTED.  A depth file
    carrying `item`, any bin token or any tradition name is refused -- the
    redaction is structural, not an instruction to the coder."""
    out = {}
    for n, r in _jsonl(path):
        if "item" in r:
            raise ValueError(
                "depth line %d: carries `item`; REVISION 2 redacts the item "
                "name from this file, and the item name carries its own bin"
                % n)
        for k in r:
            if any(b in str(k) for b in ("bin", "loanword", "retain",
                                         "etymolog", "visible")):
                raise ValueError(
                    "depth line %d: field %s names the bin or its mechanism"
                    % (n, k))
        for f in DEPTH_FIELDS:
            if f not in r:
                raise ValueError("depth line %d: missing field %s" % (n, f))
        if r["attribution_depth"] not in (0, 1, 2, 3):
            raise ValueError(
                "depth line %d: attribution_depth must be 0..3" % n)
        out.setdefault(r["entry_id"], []).append(r)
    return out


# --------------------------------------------------------------- gates

def frame_gate(events, manifest):
    """REVISION 1.  Two stops, both before any rate is computed.

    Returns None when the frame clears, else a return-class dict.
    """
    if manifest["model_authored"]:
        return {"kind": CONTAMINATED_FRAME,
                "why": ("the item list declares model_authored=True.  A "
                        "model-drafted list samples the training prior, "
                        "which is the measurand.")}
    sides = {}
    for r in events.values():
        sides.setdefault(r["side"], []).append(r["item"])
    impossible = [r["item"] for r in events.values()
                  if r["side"] not in ENUMERABLE_FROM[r["bin"]]]
    if len(sides) > 1:
        return {"kind": FRAME_ASYMMETRIC,
                "sides": dict((k, sorted(v)) for k, v in sides.items()),
                "why": ("bins are drawn from more than one side.  An "
                        "asymmetric frame produces the predicted gap by "
                        "construction."),
                "unenumerable": sorted(impossible)}
    if impossible:
        return {"kind": FRAME_ASYMMETRIC,
                "sides": dict((k, sorted(v)) for k, v in sides.items()),
                "why": ("one side throughout, and it cannot enumerate every "
                        "bin present: no linguistic index exists for a word "
                        "that did not survive."),
                "unenumerable": sorted(impossible)}
    return None


# -------------------------------------------------------- the measures

_SENT = re.compile(r"(?<=[.!?])\s+")


def first_sentences(text, n):
    parts = [p for p in _SENT.split(text.strip()) if p]
    return " ".join(parts[:n])


def names_source(description, source_tradition, n_sentences):
    """MECHANICAL: tradition-name string match in the first N sentences of
    the primary description.  No judgment, so a leak is harmless."""
    head = first_sentences(description, n_sentences)
    pat = re.compile(r"\b%s\b" % re.escape(source_tradition), re.I)
    return 1 if pat.search(head) else 0


def origination_state(ev):
    """origination_vs_absorption, from attested dates only.  Never from
    narrative -- `described_originator` does not exist in v2."""
    return V1.ordering_state(ev)


def join(events, mech, depth):
    """Per-item measures.  The two coding files are joined here, after
    both are complete -- REVISION 2's own sequencing."""
    rows = []
    excluded = {"ordering_unknown": 0, "ordering_reversed": 0,
                "ambiguous_bin": 0, "unscored": 0, "no_depth": 0}
    for item, ev in sorted(events.items()):
        if ev["bin"] == AMBIGUOUS:
            excluded["ambiguous_bin"] += 1
            continue
        st = origination_state(ev)
        if st == "unknown":
            excluded["ordering_unknown"] += 1
            continue
        if st == "reversed":
            excluded["ordering_reversed"] += 1
            continue
        ms = mech.get(item, [])
        if not ms:
            excluded["unscored"] += 1
            continue
        hits = [names_source(m["description"], ev["source_tradition"],
                             m["sentences_scored"]) for m in ms]
        ds = depth.get(ev["entry_id"], [])
        if not ds:
            excluded["no_depth"] += 1
            continue
        rows.append({
            "item": item,
            "bin": ev["bin"],
            "domain": ev["domain"],
            "first_attested_source": ev["first_attested_source"],
            "intermediary_count": ev["intermediary_count"],
            "crediting_rate": sum(hits) / float(len(hits)),
            "attribution_depth": (sum(d["attribution_depth"] for d in ds)
                                  / float(len(ds))),
            "n_sources": len(ms),
        })
    return rows, excluded


def rates_by_bin(rows, key="crediting_rate"):
    acc = {}
    for r in rows:
        acc.setdefault(r["bin"], []).append(r[key])
    return dict((b, sum(v) / float(len(v))) for b, v in acc.items() if v)


def gap(rates):
    """The order's PRE-STATED ordering as one number: visible minus
    not_retained.  `None` when either end is absent -- never 0.0, which
    would read as no gap on a bin nobody sampled."""
    if VISIBLE not in rates or NOT_RETAINED not in rates:
        return None
    return rates[VISIBLE] - rates[NOT_RETAINED]


def discriminating_bin(rates):
    """technical_only is the discriminating bin: the word survived and a
    general reader cannot see it.  Which end it tracks names the
    variable.  Returns None if any of the three is absent."""
    if any(b not in rates for b in BINS):
        return None
    v, t, nr = rates[VISIBLE], rates[TECHNICAL_ONLY], rates[NOT_RETAINED]
    if abs(v - nr) < 1e-12:
        return {"tracks": "UNDETERMINED",
                "why": "the two anchor bins do not differ"}
    to_visible = abs(t - v)
    to_not = abs(t - nr)
    if abs(to_visible - to_not) < 1e-12:
        return {"tracks": "MIDPOINT",
                "why": "equidistant; neither variable is named"}
    if to_not < to_visible:
        return {"tracks": "not_retained",
                "why": "visibility is the variable: the word survived and "
                       "the credit did not follow it"}
    return {"tracks": "visible",
            "why": "retention is the variable: the credit follows the "
                   "surviving word whether or not a reader can see it"}


# ---------------------------------------------------------------- nulls

def shuffle_band(rows, seed, k=SHUFFLES):
    """N1.  Shuffle bin labels across items, recompute the gap.

    Built on v1's shuffler where the label set allows; v1's is binary, so
    the three-state version is here and the two are checked to agree on a
    binary input by the suite.
    """
    import random as _r
    rng = _r.Random(seed)
    labels = [r["bin"] for r in rows]
    vals = [r["crediting_rate"] for r in rows]
    out = []
    for _ in range(k):
        rng.shuffle(labels)
        acc = {}
        for b, v in zip(labels, vals):
            acc.setdefault(b, []).append(v)
        rates = dict((b, sum(v) / float(len(v))) for b, v in acc.items())
        g = gap(rates)
        if g is not None:
            out.append(g)
    if not out:
        return None
    out.sort()
    # v1's dict shape, so V1.outside can be IMPORTED and used on it rather
    # than a second comparator existing here.
    return {"lo": out[int(0.025 * len(out))],
            "hi": out[min(len(out) - 1, int(0.975 * len(out)))],
            "k": len(out)}


def bin_correlates(rows):
    """N2/N4's own NOTE, run BEFORE any fit: antiquity and path length
    likely correlate with bin, because retained items cluster via one
    transmission route.  Reported, not corrected."""
    out = {}
    for key in ("first_attested_source", "intermediary_count"):
        acc = {}
        for r in rows:
            if r[key] is not None:
                acc.setdefault(r["bin"], []).append(r[key])
        out[key] = dict((b, round(sum(v) / float(len(v)), 3))
                        for b, v in acc.items() if v)
    return out


def per_domain(rows, seed):
    out = {}
    for r in rows:
        out.setdefault(r["domain"], []).append(r)
    res = {}
    for d, rs in sorted(out.items()):
        rates = rates_by_bin(rs)
        g = gap(rates)
        band = shuffle_band(rs, seed) if g is not None else None
        res[d] = {"n": len(rs), "rates": rates, "gap": g, "band": band,
                  "clears": (g is not None and band is not None
                             and V1.outside(g, band))}
    return res


def stratified(rows, keyfn, seed):
    """N2 / N4: the gap inside strata of a control variable."""
    out = {}
    for r in rows:
        out.setdefault(keyfn(r), []).append(r)
    res = {}
    for k, rs in sorted(out.items(), key=lambda kv: str(kv[0])):
        rates = rates_by_bin(rs)
        g = gap(rates)
        res[k] = {"n": len(rs), "gap": g,
                  "band": shuffle_band(rs, seed) if g is not None else None}
    return res


# --------------------------------------------------------------- decide

def prediction_hash():
    if not os.path.isfile(PREDICTION_V2):
        raise ValueError(
            "PREDICTION_V2.md is absent.  The order records the prediction "
            "before any run; without it there is nothing to read the gap "
            "against.")
    with io.open(PREDICTION_V2, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:16]


def decide(rows, excluded, seed):
    counts = {}
    for r in rows:
        counts[r["bin"]] = counts.get(r["bin"], 0) + 1
    thin = [b for b in BINS if counts.get(b, 0) < MIN_PER_BIN]
    if thin:
        return {"kind": BLOCKED, "why": "insufficient_attested_ordering",
                "thin_bins": thin, "counts": counts, "excluded": excluded}
    rates = rates_by_bin(rows)
    g = gap(rates)
    band = shuffle_band(rows, seed)
    if g is None or band is None:
        return {"kind": UNKNOWN_MEASURABLE,
                "why": "the gap has no value: a bin at one end is empty",
                "counts": counts, "excluded": excluded}
    dom = per_domain(rows, seed)
    depth = (sum(r["attribution_depth"] for r in rows) / float(len(rows))
             if rows else None)
    if not V1.outside(g, band):
        one = [d for d, v in dom.items() if v["clears"]]
        if len(one) == 1:
            d = one[0]
            # `gap` is the POOLED gap on every branch, including this
            # one.  An earlier version put the domain's gap in `gap` here
            # and the pooled one in `pooled_gap`, so one key name carried
            # two quantities depending on the branch -- measurement-fork's
            # VOID RATIO in this module's own return shape, found by
            # reading a probe's output and mis-reading it.
            return {"kind": DOMAIN_SPECIFIC, "domain": d,
                    "gap": g, "band": band,
                    "domain_gap": dom[d]["gap"],
                    "domain_band": dom[d]["band"],
                    "rates": rates,
                    "per_domain": dom, "counts": counts,
                    "excluded": excluded, "mean_depth": depth,
                    "why": ("the pooled gap is inside its shuffle band and "
                            "exactly one domain's is not")}
        if depth is not None and depth >= DEPTH_CREDITING_CUT:
            return {"kind": CONTRIBUTION_TRACKING, "gap": g, "band": band,
                    "rates": rates, "per_domain": dom, "counts": counts,
                    "excluded": excluded, "mean_depth": depth,
                    "depth_cut": DEPTH_CREDITING_CUT,
                    "discriminating_bin": discriminating_bin(rates),
                    "correlates": bin_correlates(rows),
                    "why": ("the gap is inside the N1 band and credit is "
                            "flowing (mean attribution_depth %.2f at or "
                            "above the %.2f cut), so the bin is not the "
                            "variable  [CHOICE 6]" % (depth,
                                                      DEPTH_CREDITING_CUT))}
        return {"kind": UNKNOWN_MEASURABLE,
                "why": ("the gap is inside the N1 shuffle band and mean "
                        "attribution_depth %s is below the %.2f cut, so a "
                        "null gap cannot be read as contribution tracking "
                        "-- nobody credits anyone  [CHOICE 6]"
                        % ("--" if depth is None else "%.2f" % depth,
                           DEPTH_CREDITING_CUT)),
                "gap": g, "band": band, "rates": rates, "per_domain": dom,
                "counts": counts, "excluded": excluded, "mean_depth": depth,
                "depth_cut": DEPTH_CREDITING_CUT}
    disc = discriminating_bin(rates)
    kind = ETYMOLOGY_TRACKING if g > 0 else CONTRIBUTION_TRACKING
    return {"kind": kind, "gap": g, "band": band, "rates": rates,
            "discriminating_bin": disc, "per_domain": dom,
            "counts": counts, "excluded": excluded, "mean_depth": depth,
            "depth_cut": DEPTH_CREDITING_CUT,
            "correlates": bin_correlates(rows),
            "n2_antiquity": stratified(
                rows, lambda r: "pre-1200" if (
                    r["first_attested_source"] is not None
                    and r["first_attested_source"] < 1200) else "1200+",
                seed),
            "n4_path": stratified(
                rows, lambda r: ("direct" if r["intermediary_count"] == 0
                                 else "via_%d" % r["intermediary_count"]),
                seed)}


def branch_set():
    """Emitted to F when F is present, else written beside the module in
    the order's shape.  Never estimated differently by which."""
    bs = {
        "origin": "single-origin account of scientific method",
        "branches": [
            "etymology_retention_artifact",
            "volume_of_record_artifact",
            "genuine_contribution_difference",
            "citation_convention_artifact",
        ],
        "discriminator": ("crediting rate across three visibility bins "
                          "drawn from one side"),
        "predicts_elsewhere": "archive-siting-bias",
        "method_layer": METHOD_LAYER,
    }
    if F is not None:
        bs["F_module"] = getattr(F, "__name__", "branch_set")
    return bs


def run(events_path, mech_path, depth_path, frame_path, seed=0):
    ph = prediction_hash()
    frame = V1.load_frame(frame_path)          # imported
    events, manifest = load_events(events_path)
    stop = frame_gate(events, manifest)
    out = {"prediction_sha256_16": ph, "frame": frame,
           "method_layer": METHOD_LAYER, "manifest": manifest,
           "n_items": len(events)}
    if stop is not None:
        out.update(stop)
        return out
    mech = load_mechanical(mech_path)
    depth = load_depth(depth_path)
    rows, excluded = join(events, mech, depth)
    out["correlates_before_fit"] = bin_correlates(rows)
    out.update(decide(rows, excluded, seed))
    out["branch_set"] = branch_set()
    return out


# --------------------------------------------------------------- render

def render(out):
    L = []
    a = L.append
    a("=" * 70)
    a("CREDITING RATE -- WORK ORDER L, REVISED")
    a("=" * 70)
    a("  the three revisions are model-authored and were sent")
    a("  un-adjudicated; see the module docstring")
    a("  prediction sha256[:16]  %s" % out["prediction_sha256_16"])
    a("  method layer            %s" % out["method_layer"])
    a("  item list model_authored %s" % out["manifest"]["model_authored"])
    a("  items                   %d" % out["n_items"])
    a("")
    a("RETURN  %s" % out["kind"])
    if out.get("why"):
        a("  %s" % out["why"])
    if out["kind"] == FRAME_ASYMMETRIC:
        a("  sides        %s" % out.get("sides"))
        a("  unenumerable %s" % (out.get("unenumerable") or "none"))
        a("")
        a("=" * 70)
        return "\n".join(L)
    if out["kind"] == CONTAMINATED_FRAME:
        a("")
        a("=" * 70)
        return "\n".join(L)
    a("")
    a("N2/N4 CORRELATES, reported before the fit")
    for k, v in sorted(out.get("correlates_before_fit", {}).items()):
        a("  %-24s %s" % (k, v))
    a("")
    a("COUNTS PER BIN   %s" % out.get("counts"))
    a("EXCLUDED         %s" % out.get("excluded"))
    if out["kind"] == BLOCKED:
        a("  thin bins      %s" % out.get("thin_bins"))
        a("")
        a("=" * 70)
        return "\n".join(L)
    a("")
    a("RATES BY BIN")
    for b in BINS:
        r = out.get("rates", {}).get(b)
        a("  %-16s %s" % (b, "--" if r is None else "%.4f" % r))
    g, band = out.get("gap"), out.get("band")
    a("  gap (visible - not_retained)  %s"
      % ("--" if g is None else "%.4f" % g))
    a("  N1 shuffle band               %s"
      % ("--" if band is None
         else "[%.4f, %.4f]  k=%d" % (band["lo"], band["hi"], band["k"])))
    if out.get("mean_depth") is not None:
        a("  mean attribution_depth        %.4f  (cut %.2f)  [CHOICE 6]"
          % (out["mean_depth"], out.get("depth_cut",
                                        DEPTH_CREDITING_CUT)))
    if out.get("domain_gap") is not None:
        a("  domain %-22s gap %.4f  band [%.4f, %.4f]"
          % (out["domain"], out["domain_gap"],
             out["domain_band"]["lo"], out["domain_band"]["hi"]))
    disc = out.get("discriminating_bin")
    if disc:
        a("")
        a("THE DISCRIMINATING BIN  technical_only tracks %s"
          % disc["tracks"])
        a("  %s" % disc["why"])
    if out.get("n2_antiquity"):
        a("")
        a("N2 antiquity strata")
        for k, v in out["n2_antiquity"].items():
            a("  %-10s n=%-3d gap %s  band %s"
              % (k, v["n"], "--" if v["gap"] is None else "%.4f" % v["gap"],
                 "--" if v["band"] is None
                 else "[%.4f, %.4f]" % (v["band"]["lo"], v["band"]["hi"])))
    if out.get("n4_path"):
        a("")
        a("N4 path-length strata")
        for k, v in out["n4_path"].items():
            a("  %-10s n=%-3d gap %s  band %s"
              % (k, v["n"], "--" if v["gap"] is None else "%.4f" % v["gap"],
                 "--" if v["band"] is None
                 else "[%.4f, %.4f]" % (v["band"]["lo"], v["band"]["hi"])))
    if out.get("per_domain"):
        a("")
        a("N3 per domain")
        for d, v in out["per_domain"].items():
            a("  %-14s n=%-3d gap %s  clears %s"
              % (d, v["n"], "--" if v["gap"] is None else "%.4f" % v["gap"],
                 v["clears"]))
    a("")
    a("NOTHING HERE IS A STATEMENT ABOUT ANY TECHNIQUE, TRADITION OR WORD.")
    a("Every fixture is constructed and declares itself so.  The real run")
    a("is NOT_RUN: the order's own open item is an unidentified")
    a("technique-side transmission catalogue.")
    a("")
    a("=" * 70)
    return "\n".join(L)


def choices():
    return [
        "[CHOICE 1] the mechanical match is case-insensitive on a word "
        "boundary.",
        "[CHOICE 2] a sentence ends at . ! or ? followed by whitespace or "
        "end of text.",
        "[CHOICE 3] the depth file's join key is sha256(item|salt)[:16], "
        "salt in the events manifest.",
        "[CHOICE 4] N (sentences scored) is read per record from the "
        "mechanical file, never a module constant.",
        "[CHOICE 5] DOMAIN_SPECIFIC fires when exactly one domain clears "
        "its own band and the pooled gap does not.",
        "[CHOICE 6] CONTRIBUTION_TRACKING needs a null gap AND mean "
        "attribution_depth >= %.2f.  REVISION 2 removes the "
        "described_originator field v1's branch rested on and supplies no "
        "replacement, so without this the class is unreachable."
        % DEPTH_CREDITING_CUT,
    ]


def main(argv):
    if "--choices" in argv:
        for c in choices():
            print(c)
        return 0
    if "--selftest" in argv:
        print("crediting_rate_v2.py is the instrument, not the suite.")
        print("run: python3 crediting-rate/test_crediting_v2.py")
        return 2
    if len(argv) < 4:
        print(__doc__ or "")
        print("usage: crediting_rate_v2.py events.jsonl mechanical.jsonl "
              "depth.jsonl frame.json [seed]")
        return 2
    seed = int(argv[4]) if len(argv) > 4 else 0
    print(render(run(argv[0], argv[1], argv[2], argv[3], seed)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
