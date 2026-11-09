#!/usr/bin/env python3
"""null_calibration.py -- cutoff-attribution wrapped as f(data) -> verdict and
run through null-harness. CC0. Co-authored (JinnZ2 + Claude), 2026-11-09.

ILLUSTRATIVE. Every control is a synthetic cut whose source is planted by this
file, so a pass is a regression result about the classifier's wiring, not
evidence about any real voice channel.

  python3 cutoff-attribution/null_calibration.py            the report
  python3 cutoff-attribution/selftest_null.py               the checks

verdict(data) = the single source cutoff-attribution separates by evidence, or
"NONE" when it separates none (status ESTIMATED without a single OBSERVED
candidate, or UNRESOLVED). NONE is the correct verdict for the UNRESOLVED
control.

Controls (one generator per candidate, plus UNRESOLVED), each drawn with a
null-harness numpy RNG:
  planted     a flagged log event for the candidate's hop, inside the window,
              that hop passing a known-reference check; jittered timing.
  distractors on every draw, an event for a DIFFERENT random hop that is NOT
              reference-checked, and unflagged measurements (rtt_ms, noise_db,
              asr_confidence). Neither should be read as a source.
  UNRESOLVED  distractors only; no checked hop carries an event.
Also run:
  hop_unchecked      the planted event through an UNCHECKED hop; correct NONE.
  sensor_collision   TASK_PAUSE and AMBIENT_NOISE both planted on the checked
                     sensor hop; two OBSERVED candidates do not separate, so
                     correct NONE.
  measurement_only   NETWORK_LAG is the true source but the only trace is an
                     unflagged rtt_ms spike. The tool reads unflagged
                     measurements as no evidence, so it is expected to MISS
                     (verdict NONE against true NETWORK_LAG). This row is the
                     cost of the gating rule, kept on the matrix.
The diagonal on the plain rows is close to true by construction: the planted
event is exactly the evidence the rules accept.

Note 2026-11-09 (FINDER ROUND 4): three-outcome scoring, beside the matrix.
  CORRECT_NAME     the verdict names a true source.
  CORRECT_ABSTAIN  the verdict is NONE, the cut status is UNRESOLVED, and a true
                   source is in the candidate set.
  WRONG            anything else: a non-true source named, or an abstention
                   that misses either condition. WRONG is split by reason in the
                   render (abstain with status ESTIMATED / abstain with the true
                   source dropped / named a non-true source); the split is a
                   readout, the three outcomes are the score.
  True sources: the planted source on every planted row (hop_unchecked
  included, where NONE is the gating-correct verdict); "UNRESOLVED" on the
  UNRESOLVED control; TASK_PAUSE and AMBIENT_NOISE on sensor_collision.

Readouts:
  confusion matrix   true source x assigned verdict, counts over N draws.
  forced-attribution rate
                     share of draws whose correct verdict is NONE that were
                     assigned a source anyway (UNRESOLVED and hop_unchecked).
  per-candidate gate null_harness.bake_off with gate "assigned == candidate",
                     negative control UNRESOLVED, positive control the
                     candidate's planted generator; verdict by
                     null_harness._verdict (imported, not copied).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "null-harness"))
import cutoff_attribution as ca  # noqa: E402
import null_harness as nh  # noqa: E402  (requires numpy, as null-harness does)

SOURCES = [c for c in ca.CANDIDATES if c != "UNRESOLVED"]
PLANT = {"NETWORK_LAG": "network_drop", "ENDPOINTING": "endpoint_fired", "TASK_PAUSE": "task_event",
         "AMBIENT_NOISE": "noise_db", "TRANSCRIPTION": "asr_error", "MODEL_READ": "model_interrupt"}
MEASURED = {"noise_db"}  # measurement kinds count only with flag: true
CUT_T = 2.0
N_DRAWS = 300


def _base(rng):
    return [{"t_start": 0.0, "t_end": CUT_T, "speaker": "user", "text": "the left axle reads"},
            {"t_start": CUT_T + float(rng.uniform(0.7, 1.2)), "t_end": 4.0, "speaker": "model", "text": "Go on."}]


def _distractors(rng, exclude_hop):
    hops = [h for h in sorted(set(ca.HOP_OF.values())) if h != exclude_hop]
    h = hops[int(rng.integers(len(hops)))]
    src = [k for k, v in ca.HOP_OF.items() if v == h][0]
    ev = {"t": CUT_T + float(rng.uniform(-1.5, 1.5)), "kind": PLANT[src]}
    if PLANT[src] in MEASURED:
        ev["flag"] = True
    return [ev, {"t": CUT_T + float(rng.uniform(-1, 1)), "kind": "rtt_ms"},
            {"t": CUT_T + float(rng.uniform(-1, 1)), "kind": "asr_confidence"}]


def gen(source, checked=True):
    def g(rng):
        hop = ca.HOP_OF.get(source)
        log = _distractors(rng, hop)
        refs = []
        if source != "UNRESOLVED":
            ev = {"t": CUT_T + float(rng.uniform(-1.5, 1.5)), "kind": PLANT[source]}
            if PLANT[source] in MEASURED:
                ev["flag"] = True
            log.append(ev)
            if checked:
                refs.append({"hop": hop, "injected": "ref", "observed": "ref"})
        return {"segments": _base(rng), "cut_marks": [{"t": CUT_T}], "signal_log": log,
                "reference_checks": refs}
    return g


def gen_collision(rng):
    d = gen("TASK_PAUSE")(rng)
    d["signal_log"].append({"t": CUT_T + float(rng.uniform(-1.5, 1.5)), "kind": "noise_db", "flag": True})
    return d


def gen_measurement_only(rng):
    return {"segments": _base(rng), "cut_marks": [{"t": CUT_T}],
            "signal_log": [{"t": CUT_T + float(rng.uniform(-1, 1)), "kind": "rtt_ms", "value": 900}],
            "reference_checks": [{"hop": "transmission", "injected": "ref", "observed": "ref"}]}


# Note 2026-11-09 (round 7): controls DESIGNED to identify under noise. Each
# plants one flagged event of the source's kind on the source's hop, inside the
# window (jitter up to +/-1.9 s against WINDOW_S 2.0), with that hop
# reference-checked; around it, k distractor events on other (unchecked) hops,
# unflagged measurements, and one event of a same-hop kind (or the source's own
# kind) placed OUTSIDE the window. The data carries no field naming the source:
# the rule set sees only the log, so the label is hidden from it (asserted in
# selftest_null.py). Identifiable by design: exactly one checked-hop event
# inside the window.
NOISE_K = (3, 6)


def gen_noisy(source, k):
    def g(rng):
        hop = ca.HOP_OF[source]
        log = []
        for _ in range(k):
            log.append(_distractors(rng, hop)[0])
        for _ in range(k):
            log.append({"t": CUT_T + float(rng.uniform(-2, 2)),
                        "kind": ("rtt_ms", "asr_confidence")[int(rng.integers(2))]})
        same = [x for x, h in ca.HOP_OF.items() if h == hop and x != source and x in PLANT]
        oth = same[0] if same else source
        sign = 1.0 if rng.uniform() < 0.5 else -1.0
        out = {"t": CUT_T + sign * float(rng.uniform(ca.WINDOW_S + 0.2, ca.WINDOW_S + 1.0)), "kind": PLANT[oth]}
        ev = {"t": CUT_T + float(rng.uniform(-1.9, 1.9)), "kind": PLANT[source]}
        for e in (out, ev):
            if e["kind"] in MEASURED:
                e["flag"] = True
        log += [out, ev]
        order = rng.permutation(len(log))
        return {"segments": _base(rng), "cut_marks": [{"t": CUT_T}],
                "signal_log": [log[int(i)] for i in order],
                "reference_checks": [{"hop": hop, "injected": "ref", "observed": "ref"}]}
    return g


def noise_cases():
    return [("%s/noise_k%d" % (src, k), gen_noisy(src, k), {src}) for k in NOISE_K for src in SOURCES]


def retained(data, source):
    """True if `source` is in the candidate set of the cut (kept, not assigned)."""
    return any(source in c["candidate_set"] for c in ca.attribute(data)["cuts"])


def verdict(data):
    cuts = ca.attribute(data)["cuts"]
    sep = [c["separated_by_evidence"] for c in cuts if c["separated_by_evidence"]]
    return sep[0] if len(sep) == 1 else "NONE"


OUTCOMES = ("CORRECT_NAME", "CORRECT_ABSTAIN", "WRONG")


def score_draw(data, true_set):
    """(outcome, reason) for one draw. One cut per draw in these controls."""
    cut = ca.attribute(data)["cuts"][0]
    v = verdict(data)
    if v != "NONE":
        return ("CORRECT_NAME", "named") if v in true_set else ("WRONG", "named_non_true")
    kept = any(t in cut["candidate_set"] for t in true_set)
    if kept and cut["status"] == "UNRESOLVED":
        return "CORRECT_ABSTAIN", "abstained"
    if not kept:
        return "WRONG", "abstain_true_dropped"
    return "WRONG", "abstain_status_" + cut["status"]


def _cases():
    cases = [(s, gen(s), {s}) for s in SOURCES] + [("UNRESOLVED", gen("UNRESOLVED"), {"UNRESOLVED"})]
    cases += [("%s/hop_unchecked" % s, gen(s, checked=False), {s}) for s in SOURCES]
    cases += [("sensor_collision", gen_collision, {"TASK_PAUSE", "AMBIENT_NOISE"}),
              ("NETWORK_LAG/measurement_only", gen_measurement_only, {"NETWORK_LAG"})]
    return cases


def three_outcome(n=N_DRAWS, seed=42):
    """Per row: counts of CORRECT_NAME / CORRECT_ABSTAIN / WRONG, and WRONG reasons.
    Same generators and seeds as confusion(), so the draws are the same."""
    rows = {}
    for k, (label, g, true_set) in enumerate(_cases()):
        rng = nh.np.random.default_rng(seed + k)
        cnt = dict((o, 0) for o in OUTCOMES)
        why = {}
        for _ in range(n):
            o, r = score_draw(g(rng), true_set)
            cnt[o] += 1
            if o == "WRONG":
                why[r] = why.get(r, 0) + 1
        rows[label] = {"true": sorted(true_set), "counts": cnt, "wrong_reasons": why}
    return rows


# Note 2026-11-09 (round 6): whether each control's planted evidence was
# DESIGNED to identify its source. Set by the planted design (the generator
# docstrings above), never by the tool's output. Declared data.
DESIGNED_IDENTIFIABLE = dict(
    [(s, (True, "flagged event on the source's hop, hop reference-checked")) for s in SOURCES]
    + [("UNRESOLVED", (False, "no source planted; distractors only"))]
    + [("%s/hop_unchecked" % s, (False, "planted event on a hop with no reference check; NONE is gating-correct"))
       for s in SOURCES]
    + [("sensor_collision", (False, "two sources planted on one checked hop; designed not to separate")),
       ("NETWORK_LAG/measurement_only", (False, "only an unflagged rtt_ms trace; designed as the expected miss"))]
    + [("%s/noise_k%d" % (src, k), (True, "planted on a checked hop inside the window; %d distractors, "
        "one same-hop event outside the window; label hidden" % k)) for k in NOISE_K for src in SOURCES])


def pick_options(t3=None):
    """Totals under each round-6 option. A readout: none is adopted here.
    A = rescore ESTIMATED abstentions on non-identifiable rows -> CORRECT_ABSTAIN.
    B = ESTIMATED abstentions on identifiable rows -> MISSED_IDENTIFIABLE.
    AB = both."""
    t3 = t3 or three_outcome()
    out = {}
    for opt in ("current", "A", "B", "AB"):
        tot = {"CORRECT_NAME": 0, "CORRECT_ABSTAIN": 0, "WRONG": 0, "MISSED_IDENTIFIABLE": 0}
        for label, r in t3.items():
            ident = DESIGNED_IDENTIFIABLE[label][0]
            est = r["wrong_reasons"].get("abstain_status_ESTIMATED", 0)
            tot["CORRECT_NAME"] += r["counts"]["CORRECT_NAME"]
            tot["CORRECT_ABSTAIN"] += r["counts"]["CORRECT_ABSTAIN"]
            wrong = r["counts"]["WRONG"]
            if opt in ("A", "AB") and not ident:
                tot["CORRECT_ABSTAIN"] += est
                wrong -= est
            elif opt in ("B", "AB") and ident:
                tot["MISSED_IDENTIFIABLE"] += est
                wrong -= est
            tot["WRONG"] += wrong
        out[opt] = tot
    return out


# Note 2026-11-09 (round 7): adopted scoring, the owner's pick "both".
#   CORRECT_NAME          the verdict names a true source.
#   MISSED_IDENTIFIABLE   NONE on a control designed to identify its source.
#   CORRECT_ABSTAIN       NONE on a control not designed to identify, true
#                         source kept in the candidate set (status UNRESOLVED
#                         or ESTIMATED; the round-4 status condition dropped).
#   WRONG                 a non-true source named, or NONE with the true
#                         source dropped from the candidate set.
# The round-4 three-outcome table is still printed, as a correction specimen.
ADOPTED = ("CORRECT_NAME", "CORRECT_ABSTAIN", "MISSED_IDENTIFIABLE", "WRONG")


def score_adopted(data, true_set, identifiable):
    cut = ca.attribute(data)["cuts"][0]
    v = verdict(data)
    if v != "NONE":
        return ("CORRECT_NAME", "named") if v in true_set else ("WRONG", "named_non_true")
    if identifiable:
        return "MISSED_IDENTIFIABLE", "abstain_status_" + cut["status"]
    if not any(t in cut["candidate_set"] for t in true_set):
        return "WRONG", "abstain_true_dropped"
    return "CORRECT_ABSTAIN", "abstain_status_" + cut["status"]


def adopted(n=N_DRAWS, seed=42):
    """Adopted score over the round-4 controls (same seeds, same draws) and the
    round-7 noise controls (seeds continue after them)."""
    rows = {}
    for k, (label, g, true_set) in enumerate(_cases() + noise_cases()):
        rng = nh.np.random.default_rng(seed + k)
        cnt = dict((o, 0) for o in ADOPTED)
        why = {}
        for _ in range(n):
            o, r = score_adopted(g(rng), true_set, DESIGNED_IDENTIFIABLE[label][0])
            cnt[o] += 1
            why[o + ":" + r] = why.get(o + ":" + r, 0) + 1
        rows[label] = {"true": sorted(true_set), "counts": cnt, "reasons": why}
    return rows


def confusion(n=N_DRAWS, seed=42):
    rows = {}
    cases = [(s, gen(s), s) for s in SOURCES] + [("UNRESOLVED", gen("UNRESOLVED"), "NONE")]
    cases += [("%s/hop_unchecked" % s, gen(s, checked=False), "NONE") for s in SOURCES]
    cases += [("sensor_collision", gen_collision, "NONE"),
              ("NETWORK_LAG/measurement_only", gen_measurement_only, "NETWORK_LAG")]
    for k, (label, g, correct) in enumerate(cases):
        rng = nh.np.random.default_rng(seed + k)
        cnt, kept = {}, 0
        for _ in range(n):
            d = g(rng)
            v = verdict(d)
            cnt[v] = cnt.get(v, 0) + 1
            if correct != "NONE" and v == "NONE" and retained(d, correct):
                kept += 1
        rows[label] = {"correct": correct, "counts": cnt, "retained_in_set": kept}
    none_rows = [r for r in rows.values() if r["correct"] == "NONE"]
    denom = n * len(none_rows)
    forced = sum(n - r["counts"].get("NONE", 0) for r in none_rows)
    return rows, forced, denom


def missed(rows):
    """Draws whose correct verdict is a source but were assigned NONE."""
    return sum(r["counts"].get("NONE", 0) for r in rows.values() if r["correct"] != "NONE")


# Note 2026-11-09 (ICSC v0.2 section 4.1 G1, test T30): the controls below
# were written to the rule set they test, so the output's validity is
# CONDITIONAL(same_author). It shows wiring, not validity.
# Note 2026-11-09 (round 6): label renamed CONDITIONAL(same_author) ->
# CONDITIONAL(circular_control) on the operator's order; the old label is kept
# as VALIDITY_OLD so a reader of earlier output can map it. Meaning unchanged.
VALIDITY_OLD = "CONDITIONAL(same_author)"
VALIDITY = "CONDITIONAL(circular_control)"
VALIDITY_LINE = ("validity = %s: controls were authored to the rule set under test "
                 "(ICSC v0.2 T30); this shows wiring, not validity" % VALIDITY)


def gates(n=N_DRAWS, seed=42):
    out = {}
    for s in SOURCES:
        r = nh.bake_off(lambda d, s=s: verdict(d) == s, gen("UNRESOLVED"), gen(s), n_draws=n, seed=seed)
        out[s] = r
    return out


def render(n=N_DRAWS):
    rows, forced, denom = confusion(n)
    cols = SOURCES + ["NONE"]
    L = ["cutoff-attribution null calibration -- ILLUSTRATIVE (synthetic planted sources, %d draws per row)" % n,
         "verdict = single source separated by evidence, else NONE",
         VALIDITY_LINE, "",
         "confusion matrix (rows: true source / control; columns: assigned)",
         "%-28s %s" % ("", " ".join("%7s" % c[:7] for c in cols))]
    for label, r in rows.items():
        L.append("%-28s %s   correct=%s" % (label, " ".join("%7d" % r["counts"].get(c, 0) for c in cols), r["correct"]))
    L += ["", "forced-attribution rate (source assigned where NONE was correct): %d / %d = %.4f"
          % (forced, denom, forced / denom),
          "missed attribution (NONE where a source was planted): %d draws" % missed(rows),
          "  of which the planted source is still in the candidate set: %d draws"
          % sum(r.get("retained_in_set", 0) for r in rows.values()), "", "per-candidate gate (null_harness.bake_off, neg = UNRESOLVED control)"]
    for s, r in gates(n).items():
        L.append("  %-14s FP=%.3f TP=%.3f  %s" % (s, r["FP"], r["TP"], r["verdict"]))
    t3 = three_outcome(n)
    L += ["", "three-outcome score (Note 2026-11-09, round 4; same draws as the matrix)",
          "%-28s %13s %15s %7s   wrong by reason" % ("", "CORRECT_NAME", "CORRECT_ABSTAIN", "WRONG")]
    tot = dict((o, 0) for o in OUTCOMES)
    for label, r in t3.items():
        for o in OUTCOMES:
            tot[o] += r["counts"][o]
        why = ", ".join("%s %d" % kv for kv in sorted(r["wrong_reasons"].items())) or "-"
        L.append("%-28s %13d %15d %7d   %s" % (label, r["counts"]["CORRECT_NAME"],
                                              r["counts"]["CORRECT_ABSTAIN"], r["counts"]["WRONG"], why))
    L.append("%-28s %13d %15d %7d" % ("total", tot["CORRECT_NAME"], tot["CORRECT_ABSTAIN"], tot["WRONG"]))
    L += ["", "round 6: designed identifiability per control (set by the planted design, not the tool)"]
    for label, r in t3.items():
        ident, basis = DESIGNED_IDENTIFIABLE[label]
        L.append("  %-28s %-5s ESTIMATED %3d  %s" % (label, "yes" if ident else "no",
                 r["wrong_reasons"].get("abstain_status_ESTIMATED", 0), basis))
    L += ["", "round 6 pick options (readout; superseded by the round 7 pick: both, below)",
          "  %-8s %13s %15s %7s %20s" % ("option", "CORRECT_NAME", "CORRECT_ABSTAIN", "WRONG", "MISSED_IDENTIFIABLE")]
    for opt, tt in pick_options(t3).items():
        L.append("  %-8s %13d %15d %7d %20d" % (opt, tt["CORRECT_NAME"], tt["CORRECT_ABSTAIN"],
                                               tt["WRONG"], tt["MISSED_IDENTIFIABLE"]))
    ad = adopted(n)
    L += ["", "ADOPTED SCORE (Note 2026-11-09, round 7, owner's pick: both)",
          "%-28s %13s %15s %20s %7s" % ("", "CORRECT_NAME", "CORRECT_ABSTAIN", "MISSED_IDENTIFIABLE", "WRONG")]
    tot = dict((o, 0) for o in ADOPTED)
    ntot = dict((o, 0) for o in ADOPTED)
    for label, r in ad.items():
        for o in ADOPTED:
            tot[o] += r["counts"][o]
            if "/noise_k" in label:
                ntot[o] += r["counts"][o]
        L.append("%-28s %13d %15d %20d %7d" % (label, r["counts"]["CORRECT_NAME"], r["counts"]["CORRECT_ABSTAIN"],
                                                r["counts"]["MISSED_IDENTIFIABLE"], r["counts"]["WRONG"]))
    L.append("%-28s %13d %15d %20d %7d" % ("total (all controls)", tot["CORRECT_NAME"], tot["CORRECT_ABSTAIN"],
                                            tot["MISSED_IDENTIFIABLE"], tot["WRONG"]))
    L.append("%-28s %13d %15d %20d %7d" % ("noise controls only", ntot["CORRECT_NAME"], ntot["CORRECT_ABSTAIN"],
                                            ntot["MISSED_IDENTIFIABLE"], ntot["WRONG"]))
    L += ["", "Scope: the controls test the evidence-gating rules this file plants against. A real",
          "channel can produce cues the generators never draw (overlapping hops, mislabelled",
          "logs, a reference check that passes while the hop fails on other inputs)."]
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("null_calibration.py refuses --selftest; run: python3 cutoff-attribution/selftest_null.py")
        sys.exit(2)
    print(render())
