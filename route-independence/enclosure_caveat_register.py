# SPDX-License-Identifier: CC0-1.0
"""FWO-15 Build A -- enclosure caveat register.

STATUS: RECONSTRUCTED 2026-10-04. The original 2026-09-27 spec text was not
recovered; the order (WORK_ORDER_FWO-15_2026-10-04.md) was rebuilt from a
memory object that is not in this tree. If the original surfaces it
SUPERSEDES the order and this module is re-scored against it.

TERMS: "enclosure", "captive" and "domesticated" are used in their
animal-science external-validity sense. No political position is advanced.

QUESTION (order's): does human behavioral literature declare the
resource-gating condition of its sample the way captive-animal literature
declares housing and provision?

State: DESIGN_WRITTEN. No corpus is in hand, so this ships the schema, the
scorer and fixtures. A real run reads two JSON files (frames, coded studies)
and returns the same branches; on no input it returns UNMEASURED.

Not rebuilt here (order's SCOPE): the lag count is FWO-11 lag_count.py and
question selection is FWO-9 question_space.py.

Every [CHOICE n] below is this build's, not the order's, and is printed by
--choices.
  [CHOICE 1] caveat rate = YES / (YES + NO). E4 ABSENT is counted and printed
             apart and never enters the denominator. Empty denominator -> None.
  [CHOICE 2] floor: an arm (or sub-literature) is evaluable only with at
             least FLOOR studies carrying E4 in {YES, NO}.
  [CHOICE 3] "<<" = human Wilson-95 upper bound below the animal Wilson-95
             lower bound. Overlap with |difference| <= MARGIN reads NO_GAP;
             overlap with a larger difference reads INDETERMINATE.
  [CHOICE 4] the two animal arms are compared to the human arm separately
             and never pooled.
  [CHOICE 5] E5 (arm) and the frame id may not be ABSENT: a study with no arm
             cannot enter a per-arm rate.
  [CHOICE 6] SCOPE_LIMITED fires when evaluable human sub-literatures split
             between GAP_CONFIRMED and NO_GAP, or when the pooled human arm is
             not GAP_CONFIRMED while at least one sub-literature is.
"""

import json
import math
import sys

ABSENT = "ABSENT"
ARMS = ("human", "captive-animal", "production-animal")
ANIMAL_ARMS = ("captive-animal", "production-animal")
E2_VALUES = ("token-gated", "mixed", "direct", ABSENT)
E4_VALUES = ("YES", "NO", ABSENT)
FIELDS = ("E1", "E2", "E3", "E4", "E5")
FLOOR = 20
MARGIN = 0.10
Z95 = 1.96

CHOICES = {
    1: "caveat rate = YES/(YES+NO); E4 ABSENT counted apart; empty denominator -> None",
    2: "floor: %d studies with E4 in {YES, NO} per arm or sub-literature" % FLOOR,
    3: "'<<' = human Wilson-95 upper < animal Wilson-95 lower; overlap with |diff| <= %.2f "
       "is NO_GAP; larger overlapping difference is INDETERMINATE" % MARGIN,
    4: "captive-animal and production-animal arms are compared to the human arm separately",
    5: "E5 and frame_id may not be ABSENT",
    6: "SCOPE_LIMITED when evaluable human sub-literatures split, or pooled is not "
       "GAP_CONFIRMED while a sub-literature is",
}

BRANCHES = ("GAP_CONFIRMED", "NO_GAP", "INDETERMINATE", "SCOPE_LIMITED", "UNMEASURED")

PRIOR_ART_NOTE = (
    "prior art (RUN, search snippets only): the cross-cultural market-integration\n"
    "studies measured the share of purchased calories as a covariate of fairness\n"
    "(food leg of the provision regime); see FWO-15_PRIOR_ART.md"
)


class Refused(ValueError):
    """A frame or study that the order's rules do not let into a rate."""


def _date_key(s):
    if not isinstance(s, str) or len(s) < 4:
        raise Refused("date must be an ISO string, got %r" % (s,))
    return s


def validate_frame(frame):
    for k in ("frame_id", "arm", "description", "declared_at"):
        if k not in frame or frame[k] in (None, "", ABSENT):
            raise Refused("frame missing %s" % k)
    if frame["arm"] not in ARMS:
        raise Refused("frame arm %r not in %s" % (frame["arm"], ARMS))
    _date_key(frame["declared_at"])
    return frame


def validate_study(study, frames):
    """Refuse a study the rules do not admit. Returns the study unchanged."""
    fid = study.get("frame_id")
    if fid in (None, "", ABSENT):
        raise Refused("study %s: no frame_id [CHOICE 5]" % study.get("study_id"))
    if fid not in frames:
        raise Refused("study %s: frame %r was never declared" % (study.get("study_id"), fid))
    frame = frames[fid]
    for f in FIELDS:
        if f not in study:
            raise Refused("study %s: field %s missing (write ABSENT, not nothing)" % (study.get("study_id"), f))
    if study["E5"] == ABSENT:
        raise Refused("study %s: E5 ABSENT [CHOICE 5]" % study.get("study_id"))
    if study["E5"] not in ARMS:
        raise Refused("study %s: E5 %r not an arm" % (study.get("study_id"), study["E5"]))
    if study["E5"] != frame["arm"]:
        raise Refused("study %s: E5 %s disagrees with frame arm %s" % (study.get("study_id"), study["E5"], frame["arm"]))
    if study["E2"] not in E2_VALUES:
        raise Refused("study %s: E2 %r not in %s" % (study.get("study_id"), study["E2"], E2_VALUES))
    if study["E4"] not in E4_VALUES:
        raise Refused("study %s: E4 %r not in %s" % (study.get("study_id"), study["E4"], E4_VALUES))
    coded = _date_key(study.get("coded_at"))
    if coded < frame["declared_at"]:
        raise Refused("study %s: coded %s before its frame was declared %s (order: frame BEFORE coding)"
                      % (study.get("study_id"), coded, frame["declared_at"]))
    return study


def caveat_rate(yes, no):
    """YES / (YES + NO). None when the denominator is empty, never 0."""
    d = yes + no
    if d == 0:
        return None
    return yes / d


def wilson(k, n, z=Z95):
    """Wilson score interval; None for n == 0."""
    if n == 0:
        return None
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centre - half), min(1.0, centre + half))


def summarize(studies):
    """Counts for one group of studies (one arm, or one sub-literature)."""
    e4 = {v: 0 for v in E4_VALUES}
    e2 = {v: 0 for v in E2_VALUES}
    for s in studies:
        e4[s["E4"]] += 1
        e2[s["E2"]] += 1
    yes, no = e4["YES"], e4["NO"]
    n_rate = yes + no
    modal = None
    if studies:
        top = max(e2.values())
        modal = sorted(v for v in E2_VALUES if e2[v] == top)
    return {
        "n_studies": len(studies),
        "e4": e4,
        "e2": e2,
        "e2_modal": modal,
        "n_rate": n_rate,
        "rate": caveat_rate(yes, no),
        "interval": wilson(yes, n_rate),
        "evaluable": n_rate >= FLOOR,
    }


def compare(human, animal):
    """One human summary against one animal summary. Returns a branch."""
    if not human["evaluable"] or not animal["evaluable"]:
        return "UNMEASURED"
    hi_h = human["interval"][1]
    lo_a = animal["interval"][0]
    if hi_h < lo_a:
        return "GAP_CONFIRMED"
    if abs(animal["rate"] - human["rate"]) <= MARGIN:
        return "NO_GAP"
    return "INDETERMINATE"


def run(frames_list, studies):
    """Score a coded corpus. Never raises on content; refusals are returned."""
    frames = {}
    refused = []
    for f in frames_list:
        try:
            validate_frame(f)
            frames[f["frame_id"]] = f
        except Refused as e:
            refused.append(str(e))
    admitted = []
    for s in studies:
        try:
            admitted.append(validate_study(s, frames))
        except Refused as e:
            refused.append(str(e))
    by_arm = {a: [s for s in admitted if s["E5"] == a] for a in ARMS}
    arms = {a: summarize(by_arm[a]) for a in ARMS}
    arm_frames = {a: sorted({frames[s["frame_id"]]["description"] for s in by_arm[a]}) for a in ARMS}
    subs = {}
    for s in by_arm["human"]:
        subs.setdefault(s.get("sub_literature", "UNNAMED"), []).append(s)
    sub_sum = {k: summarize(v) for k, v in sorted(subs.items())}
    out = {"arms": arms, "frames": arm_frames, "refused": refused, "comparisons": {}}
    for a in ANIMAL_ARMS:
        pooled = compare(arms["human"], arms[a])
        per_sub = {k: compare(v, arms[a]) for k, v in sub_sum.items()}
        gap = sorted(k for k, v in per_sub.items() if v == "GAP_CONFIRMED")
        nogap = sorted(k for k, v in per_sub.items() if v == "NO_GAP")
        branch = pooled
        if pooled != "UNMEASURED":
            if gap and nogap:
                branch = "SCOPE_LIMITED"
            elif pooled != "GAP_CONFIRMED" and gap:
                branch = "SCOPE_LIMITED"
        out["comparisons"][a] = {
            "pooled": pooled,
            "branch": branch,
            "sub_literatures": per_sub,
            "gap_in": gap,
            "no_gap_in": nogap,
        }
    return out


def _fmt_rate(s):
    if s["rate"] is None:
        return "rate None (empty denominator)"
    lo, hi = s["interval"]
    return "rate %.3f  Wilson95 [%.3f, %.3f]" % (s["rate"], lo, hi)


def render_result(res, out):
    w = out.write
    for a in ARMS:
        s = res["arms"][a]
        w("  arm %-18s n=%d  E4 YES/NO/ABSENT = %d/%d/%d  %s%s\n"
          % (a, s["n_studies"], s["e4"]["YES"], s["e4"]["NO"], s["e4"]["ABSENT"], _fmt_rate(s),
             "" if s["evaluable"] else "  [below floor %d -> UNMEASURED]" % FLOOR))
        w("      frame: %s\n" % ("; ".join(res["frames"][a]) or "NONE DECLARED"))
        if s["n_studies"]:
            w("      E2 distribution %s  modal %s\n" % (
                ", ".join("%s=%d" % (k, s["e2"][k]) for k in E2_VALUES), "/".join(s["e2_modal"])))
            if a == "human" and ABSENT in s["e2_modal"]:
                w("      E2 = ABSENT is the modal human value; reported as a FINDING, not missing data\n")
    for a in ANIMAL_ARMS:
        c = res["comparisons"][a]
        w("  human vs %-17s pooled %-14s branch %s\n" % (a, c["pooled"], c["branch"]))
        if c["gap_in"] or c["no_gap_in"]:
            w("      gap in %s; no gap in %s\n" % (c["gap_in"] or "none", c["no_gap_in"] or "none"))
    if res["refused"]:
        w("  refused %d:\n" % len(res["refused"]))
        for r in res["refused"]:
            w("    - %s\n" % r)


def render(out=None):
    out = out or sys.stdout
    w = out.write
    w("FWO-15 Build A -- enclosure caveat register\n")
    w("STATUS RECONSTRUCTED 2026-10-04; DESIGN_WRITTEN (no corpus in hand)\n")
    w("TERMS: enclosure / captive / domesticated in the animal-science external-validity sense\n\n")
    w("schema per study (each field value or ABSENT):\n")
    w("  E1 population sampled\n")
    w("  E2 provision regime declared: %s\n" % " | ".join(E2_VALUES))
    w("  E3 generalization target stated (\"humans\", \"adults\", named population, ABSENT)\n")
    w("  E4 external-validity caveat re provision regime: %s\n" % " | ".join(E4_VALUES))
    w("  E5 arm: %s\n\n" % " | ".join(ARMS))
    w("real run: no corpus\n")
    res = run([], [])
    render_result(res, out)
    w("\n%s\n" % PRIOR_ART_NOTE)
    w("not rebuilt: lag count -> FWO-11 lag_count.py; question selection -> FWO-9 question_space.py\n")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("enclosure_caveat_register: checks live in test_fwo15.py; run python3 test_fwo15.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    if "--frames" in argv and "--corpus" in argv:
        frames = json.load(open(argv[argv.index("--frames") + 1], encoding="utf-8"))
        studies = json.load(open(argv[argv.index("--corpus") + 1], encoding="utf-8"))
        render_result(run(frames, studies), sys.stdout)
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
