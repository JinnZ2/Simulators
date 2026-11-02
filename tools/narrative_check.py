#!/usr/bin/env python3
"""
narrative_check.py -- flag structural moves in a pitch, transcript, article or own draft.

STATUS: PROPOSED instrument, co-authored. CC0. stdlib only.
Home: JinnZ2/Simulators tools/ (moved 2026-11-02 from AI-Consciousness-Sensors healing/);
mirrored byte-identical in JinnZ2/method-layer tools/.
Doc: NARRATIVE_CHECK.md. Reports STRUCTURE, never whether a claim is true or any side's position.
A flag means "check this part separately," not "this is false."

Detection is by the reader's judgment (human or model); there is no keyword matcher on purpose --
one would misfire on irony and quotation (see Gaps in the doc).

USAGE
  python3 narrative_check.py              render the origin-case report
  python3 narrative_check.py --markers    list the markers with questions and false positives
  python3 narrative_check.py --selftest
"""
from dataclasses import dataclass, field
import sys


@dataclass
class Marker:
    key: str
    question: str          # what the AI asks of the text
    signal: str            # observable pattern
    false_positive: str    # when the flag is innocent


MARKERS = [
    Marker("stakes_inflation",
           "Are stakes raised to survival/civilizational level before evidence is given?",
           "last line of defense, everyone dies, only X stands between us and Y",
           "genuine emergencies with cited data"),
    Marker("true_carrier",
           "Is one verifiable true claim placed next to unverified ones so trust transfers?",
           "accurate detail followed by claims the detail does not support",
           "all adjacent claims independently sourced"),
    Marker("provenance_stripped",
           "Do numbers or facts arrive without source, method, or scope?",
           "exact percentages, 'studies show', 'experts agree', no citation",
           "common knowledge with low stakes"),
    Marker("model_as_measurement",
           "Is a projection or worst-case model stated as an observed fact?",
           "'will die', 'would collapse' with numbers and no modeled-scenario label",
           "projection clearly labeled with assumptions"),
    Marker("unstated_bridge",
           "Does the conclusion need a step the text never states?",
           "land can't feed people -> therefore armed defense is needed",
           "step is genuinely obvious and uncontested"),
    Marker("causal_timing",
           "Is an effect pinned on a cause that came after it, or on a convenient event?",
           "deer/beaver collapse attributed to Depression; overharvest came earlier",
           "multiple real causes overlapping in time"),
    Marker("counter_case_omitted",
           "Are known cases that went the other way left out?",
           "collapse predicted; mutual-aid outcomes (Gary IN, Puerto Rico) absent",
           "short format with counter-cases acknowledged elsewhere"),
    Marker("special_knowledge",
           "Does the speaker claim to see what the population cannot?",
           "'most people don't know', 'they won't tell you', superior insight",
           "specialist with checkable credentials and sources"),
    Marker("in_out_group",
           "Are listeners sorted into those who get it vs. those who don't?",
           "sheep/awake, us/them, like-minded community as the solution",
           "descriptive grouping with no loyalty ask"),
    Marker("homogeneity_push",
           "Is differing knowledge framed as threat rather than resource?",
           "dissent = enemy; like-minded = safe",
           "exclusion of demonstrably bad-faith actors"),
    Marker("public_record_unchecked",
           "Is a physical claim (building, tunnel, construction, land use) checkable against public records nobody consulted?",
           "basement/tunnel/facility claims with no permit, zoning, plan, or inspection record cited (Pizzagate: claimed basement, building had none). Cross-reference underground layers: gas, electrical, fiber, water/sewer, prior construction problems, post-storm repair records; documentation is densest where past events (e.g. Sandy damage) forced it. Independent record sources with no stake in the narrative: insurance catastrophe (CAT) surveys, caving/speleological surveys, seismic preparedness assessments (e.g. distant-fault secondary effects such as New Madrid on DC's unstable fill/swamp ground)",
           "record genuinely unavailable or sealed, and said so"),
    Marker("join_ask",
           "Does the structure end in follow/buy/join/subscribe?",
           "get on board, follow me, prepare with my product",
           "ask is separate from and after independent evidence"),
]
STATUSES = ("OBSERVED", "DERIVED", "PROPOSED")


@dataclass
class Flag:
    key: str
    excerpt: str
    status: str   # OBSERVED (in text) | DERIVED (inferred from structure) | PROPOSED
    note: str = ""


@dataclass
class Report:
    flags: list = field(default_factory=list)

    def add(self, key, excerpt, status="OBSERVED", note=""):
        assert key in {m.key for m in MARKERS}, key
        assert status in STATUSES, status
        self.flags.append(Flag(key, excerpt, status, note))

    def render(self):
        lines = ["STRUCTURE REPORT (not a truth verdict)"]
        for f in self.flags:
            lines.append(f"- [{f.status}] {f.key}: \"{f.excerpt}\" {f.note}".rstrip())
        lines.append("Next: check each flagged part separately; source attached or marked unknown.")
        return "\n".join(lines)


def origin_case():
    r = Report()
    r.add("stakes_inflation", "last armed society before one world government")
    r.add("model_as_measurement", "90 days without power, 25-50% die",
          note="likely EMP-commission worst case; Maria record ~0.1%")
    r.add("causal_timing", "deer gone in the Depression",
          note="low point predates it, market hunting")
    r.add("true_carrier", "most can't live off the land")
    r.add("join_ask", "get on board with his thoughts")
    return r


def selftest():
    out = origin_case().render()
    checks = [
        ("12 markers, each with a false-positive case", len(MARKERS) == 12 and all(m.false_positive for m in MARKERS)),
        ("public_record_unchecked sits right before join_ask",
         [m.key for m in MARKERS][-2:] == ["public_record_unchecked", "join_ask"]),
        ("report header says it is not a truth verdict", out.startswith("STRUCTURE REPORT (not a truth verdict)")),
        ("origin case fires 5 markers", len(origin_case().flags) == 5),
        ("report hands checking back", out.rstrip().endswith("source attached or marked unknown.")),
        ("report carries no verdict words", not any(w in out.lower() for w in ("false.", "true.", "debunked", "liar"))),
    ]
    for bad_key, bad_status in (("not_a_marker", "OBSERVED"), ("join_ask", "CERTAIN")):
        try:
            Report().add(bad_key, "x", bad_status)
            checks.append(("rejects %s / %s" % (bad_key, bad_status), False))
        except AssertionError:
            checks.append(("rejects %s / %s" % (bad_key, bad_status), True))
    bad = [n for n, ok in checks if not ok]
    print("narrative_check --selftest: %d/%d" % (len(checks) - len(bad), len(checks)))
    for n in bad:
        print("  FAIL:", n)
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--markers" in sys.argv:
        for m in MARKERS:
            print(f"[{m.key}] {m.question}\n  signal: {m.signal}\n  innocent when: {m.false_positive}\n")
        sys.exit(0)
    print(origin_case().render())
