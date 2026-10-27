"""
gating_diagnostic.py  -- CC0, stdlib only. Co-authored.

Notation tool: compare coordination systems on five axes that decide
whether a claim is anchored to something external. Marks; does not judge.

Every value carries STATUS (MEASURED | ESTIMATED | UNKNOWN | GAP) and SOURCE.
GAP = no stable anchor identified. Data, not failure.
Schema is separate from examples. Examples are PROPOSED instances, not verdicts;
replace or refute them with evidence.

USAGE
  python gating_diagnostic.py                 # compare example instances
  python gating_diagnostic.py --claim "..."   # print question template
  python gating_diagnostic.py --selftest
"""
from dataclasses import dataclass, field
import sys, textwrap

STATUSES = ("MEASURED", "ESTIMATED", "UNKNOWN", "GAP")
AXES = {
    "anchor": "What invariant forces revision of this claim?",
    "bound": "What external limit cannot be exceeded by relabeling?",
    "coupling": "Does consequence reach the party that decided?",
    "update": "What forces revision, on what timescale?",
    "error_visibility": "Can the system detect its own decoupling?",
}

@dataclass
class Entry:
    value: str
    status: str = "GAP"
    source: str = ""          # who/what supports it; empty -> flagged
    def __post_init__(self):
        if self.status not in STATUSES:
            raise ValueError(f"status must be one of {STATUSES}")

@dataclass
class System:
    name: str
    instance_of: str          # concrete object + period; avoids welded labels
    axes: dict                # axis -> Entry
    notes: list = field(default_factory=list)
    def validate(self):
        missing = [a for a in AXES if a not in self.axes]
        unsourced = [a for a, e in self.axes.items()
                     if e.status in ("MEASURED", "ESTIMATED") and not e.source]
        return {"missing_axes": missing, "unsourced_claims": unsourced}

@dataclass
class Abstention:
    """A non-audit is a read. Falsifiable only with these fields filled."""
    date: str
    actor: str
    decision_point: str
    abstention_type: str      # declined_to_audit | no_assessment_possible
                              # | chose_neutrality | deferred | did_not_reach
    available_at_time: str
    would_have_counted_as: str = "GAP"
    review_trigger: str = "GAP"
    def defects(self):
        out = []
        if self.would_have_counted_as == "GAP":
            out.append("not reasoned, defaulted (would_have_counted_as empty)")
        if self.review_trigger == "GAP":
            out.append("closer, not binding (review_trigger empty)")
        return out

ABSTENTIONS = []
def record_abstention(a: Abstention):
    ABSTENTIONS.append(a)
    return a.defects()

def question_template(claim: str) -> dict:
    """Not a classifier. Returns the questions; reader supplies evidence."""
    return {"claim": claim,
            **{a: Entry(f"? {q}", "GAP") for a, q in AXES.items()},
            "if_not_audited": "record_abstention(...) with available_at_time, "
                              "would_have_counted_as, review_trigger"}

def compare(a: System, b: System, width=44):
    w = lambda s: textwrap.wrap(s, width) or [""]
    print(f"\n{'AXIS':<17}| {a.name:<{width}} | {b.name}")
    print(f"{'':<17}| {a.instance_of[:width]:<{width}} | {b.instance_of[:width]}")
    print("-" * (21 + 2 * width))
    for axis in AXES:
        ea, eb = a.axes.get(axis, Entry("")), b.axes.get(axis, Entry(""))
        la = w(f"[{ea.status}] {ea.value}") + [f"src: {ea.source or 'NONE'}"]
        lb = w(f"[{eb.status}] {eb.value}") + [f"src: {eb.source or 'NONE'}"]
        for i in range(max(len(la), len(lb))):
            print(f"{axis if i == 0 else '':<17}| "
                  f"{(la[i] if i < len(la) else ''):<{width}} | "
                  f"{lb[i] if i < len(lb) else ''}")
        print()
    for s in (a, b):
        v = s.validate()
        print(f"{s.name}: missing={v['missing_axes']} unsourced={v['unsourced_claims']}")
        for n in s.notes:
            print("  - " + n)

# ---------------- EXAMPLE INSTANCES (PROPOSED; refute with evidence) -------
EX_PHYSICS = System(
    name="EXAMPLE: physics-anchored",
    instance_of="structural engineering, current practice",
    axes={
        "anchor": Entry("conserved quantities (energy, mass, charge)", "MEASURED",
                        "conservation laws"),
        "bound": Entry("thermodynamic limits; material yield strength", "MEASURED",
                       "standard engineering references"),
        "coupling": Entry("tight: structure fails under load", "ESTIMATED",
                          "failure investigation record"),
        "update": Entry("failure contradicts design -> codes revise", "ESTIMATED",
                        "building-code revision history"),
        "error_visibility": Entry("external consequence on its own schedule",
                                  "ESTIMATED", "proposed (DeepSeek draft)"),
    },
    notes=["Institutional layer (review, funding) is NOT physics-anchored."],
)
EX_TOKEN = System(
    name="EXAMPLE: token-anchored",
    instance_of="fiat credit system, specify country + period",
    axes={
        "anchor": Entry("no stable invariant identified; double-entry balances "
                        "ledger to itself, not to world", "GAP",
                        "proposed (DeepSeek draft)"),
        "bound": Entry("leverage multiplies claims without physical limit",
                       "UNKNOWN", ""),
        "coupling": Entry("loose: costs displaced to non-deciders", "ESTIMATED",
                          "externality literature; cite"),
        "update": Entry("slow, partial; regime change breaks estimates",
                        "ESTIMATED", "Lucas critique"),
        "error_visibility": Entry("internally consistent, externally wrong",
                                  "UNKNOWN", ""),
    },
    notes=["Coupling of other sectors to the token is contingent, built.",
           "Specify instance; one label over changing objects is a weld."],
)

def selftest():
    assert EX_PHYSICS.validate()["missing_axes"] == []
    assert "bound" not in EX_TOKEN.validate()["unsourced_claims"]  # UNKNOWN ok
    try: Entry("x", "TRUE"); raise AssertionError
    except ValueError: pass
    d = record_abstention(Abstention("2026-10-25", "x", "y",
                                     "deferred", "dataset Z"))
    assert len(d) == 2
    t = question_template("c")
    assert all(t[a].status == "GAP" for a in AXES)
    print("selftest ok")

if __name__ == "__main__":
    if "--selftest" in sys.argv: selftest()
    elif len(sys.argv) > 2 and sys.argv[1] == "--claim":
        t = question_template(" ".join(sys.argv[2:]))
        print("\nCLAIM:", t.pop("claim"))
        for k, v in t.items():
            print(f"  {k:<17}: {v.value if isinstance(v, Entry) else v}")
    else:
        compare(EX_PHYSICS, EX_TOKEN)
