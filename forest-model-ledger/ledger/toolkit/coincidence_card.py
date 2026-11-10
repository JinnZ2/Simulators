"""Toolkit: coincidence_card. One card per observed coincidence: two things agree,
or one thing is flatter / smoother / more alike than expected.

Six slots. Each is void (not looked at), supported or ruled_out, and anything
but void needs evidence. Slots are not exclusive: a coincidence can have two
causes and the card then names both.

  shared_constraint     both sides obey one constraint, so they must agree
  local_normal_form     near a fixed point or threshold many systems look alike
  statistical_artifact  sampling, selection, too few draws
  numerical_artifact    roundoff, step size, grid, solver
  low_dim_projection    a scalar or low-dimensional readout hides the difference
  none_of_above         DERIVED, never declared: supported only when the five
                        above are all ruled_out. It is a curiosity and needs its
                        own branch.

Readings (closed set):
  OPEN        at least one of the five is void; the unrun slots are listed
  RESOLVED    all five looked at, at least one supported
  CURIOSITY   all five ruled_out; the card must name a branch

    python3 ledger/toolkit/coincidence_card.py            # read every card
"""
import glob, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE)
from tools import miniyaml

CAUSES = ["shared_constraint", "local_normal_form", "statistical_artifact", "numerical_artifact", "low_dim_projection"]
SLOTS = CAUSES + ["none_of_above"]
STATES = {"void", "supported", "ruled_out"}
FIELDS = ["id", "observation", "trigger", "slots", "reading_declared", "branch", "runs", "open_issues"]


class CardError(ValueError):
    pass


def read(card):
    """Return (reading, detail). Raises CardError on a malformed card."""
    for f in FIELDS:
        if f not in card:
            raise CardError(f"{card.get('id')}: field {f} dropped (write void)")
    slots = card["slots"]
    if sorted(slots) != sorted(SLOTS):
        raise CardError(f"{card['id']}: slots must be exactly {SLOTS}")
    for name in SLOTS:
        s = slots[name]
        if s.get("state") not in STATES:
            raise CardError(f"{card['id']}: {name} state {s.get('state')}")
        if "evidence" not in s:
            raise CardError(f"{card['id']}: {name} evidence dropped")
        if s["state"] != "void" and s["evidence"] == "void":
            raise CardError(f"{card['id']}: {name} is {s['state']} with no evidence")
    states = {n: slots[n]["state"] for n in CAUSES}
    unrun = [n for n in CAUSES if states[n] == "void"]
    supported = [n for n in CAUSES if states[n] == "supported"]
    derived_none = "supported" if all(states[n] == "ruled_out" for n in CAUSES) else ("void" if unrun else "ruled_out")
    declared_none = slots["none_of_above"]["state"]
    if declared_none != derived_none:
        raise CardError(f"{card['id']}: none_of_above declared {declared_none}, derived {derived_none}")
    if unrun:
        return "OPEN", dict(unrun=unrun, supported=supported)
    if derived_none == "supported":
        if card["branch"] == "void":
            raise CardError(f"{card['id']}: CURIOSITY needs its own branch")
        return "CURIOSITY", dict(branch=card["branch"])
    return "RESOLVED", dict(supported=supported)


def load_all(root=HERE):
    return {os.path.basename(p)[:-5]: miniyaml.load(p)
            for p in sorted(glob.glob(os.path.join(root, "ledger", "toolkit", "cards", "*.yaml")))}


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("refused: the checks live in forest-model-ledger/tests/test_l0.py"); sys.exit(2)
    for cid, card in load_all().items():
        reading, detail = read(card)
        print(f"{cid:44s} {reading:9s} {detail}")
