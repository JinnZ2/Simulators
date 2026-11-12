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
  PROVISIONAL would read RESOLVED, but recheck_when names tools still in
              build: the evidence stands, the producing tool does not exist
              yet. Re-check when every named tool is built (Kavik, 2026-11-10)
  CURIOSITY   all five ruled_out; the card must name a branch

Slot states: void | supported | ruled_out | ABSENT_AT_SENSITIVITY(<value>).
  ABSENT_AT_SENSITIVITY is a scoped absence (work order 2026-11-10, item 1): a
  null result at a stated sensitivity, never a bare "absent". The value is
  required; "ABSENT_AT_SENSITIVITY" alone and "absent" are refused. For the
  reading it counts as ruled out WITHIN that sensitivity, and the detail lists
  every scoped slot so a reader cannot drop the scope.

expiry_condition (every slot, work order 2026-11-10, item 1): void, or
  {instrument_class, sensitivity, protocol, provenance}: the instrument whose
  null result would move a void slot to ABSENT_AT_SENSITIVITY(<sensitivity>).
  On a void slot, expiry_condition void = "no exit defined". Counted by the
  checker, not failed on (yet).

    python3 ledger/toolkit/coincidence_card.py            # read every card
"""
import glob, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE)
from tools import miniyaml

CAUSES = ["shared_constraint", "local_normal_form", "statistical_artifact", "numerical_artifact", "low_dim_projection"]
SLOTS = CAUSES + ["none_of_above"]
STATES = {"void", "supported", "ruled_out"}
SCOPED = re.compile(r"^ABSENT_AT_SENSITIVITY\((.+)\)$")
EXPIRY_KEYS = ["instrument_class", "sensitivity", "protocol", "provenance"]
FIELDS = ["id", "observation", "trigger", "slots", "reading_declared", "recheck_when", "branch", "runs", "open_issues"]


class CardError(ValueError):
    pass


def slot_state(s):
    """Return (state, sensitivity). state is one of STATES or ABSENT_AT_SENSITIVITY."""
    st = s.get("state")
    if st in STATES:
        return st, None
    m = SCOPED.match(st) if isinstance(st, str) else None
    if m and m.group(1).strip() and m.group(1).strip() != "void":
        return "ABSENT_AT_SENSITIVITY", m.group(1).strip()
    raise CardError(f"state {st!r}: not void / supported / ruled_out / ABSENT_AT_SENSITIVITY(<value>)")


def expiry(s):
    """Return 'none' (void), 'complete', or 'incomplete' (some part void). Raises on a malformed one."""
    e = s.get("expiry_condition", "MISSING")
    if e == "MISSING":
        raise CardError("expiry_condition dropped (write void)")
    if e == "void":
        return "none"
    if not isinstance(e, dict) or sorted(e) != sorted(EXPIRY_KEYS):
        raise CardError(f"expiry_condition must be void or exactly {EXPIRY_KEYS}")
    return "complete" if all(e[k] != "void" for k in EXPIRY_KEYS[:3]) else "incomplete"


def exits(card):
    """Per open (void) cause slot: its exit state. none_of_above is derived, never counted."""
    return {n: expiry(card["slots"][n]) for n in CAUSES if card["slots"][n].get("state") == "void"}


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
        try:
            slot_state(s)
            expiry(s)
        except CardError as e:
            raise CardError(f"{card['id']}: {name} {e}")
        if name == "none_of_above" and slot_state(s)[0] == "ABSENT_AT_SENSITIVITY":
            raise CardError(f"{card['id']}: none_of_above is derived; it cannot be scoped")
        if "evidence" not in s:
            raise CardError(f"{card['id']}: {name} evidence dropped")
        if s["state"] != "void" and s["evidence"] == "void":
            raise CardError(f"{card['id']}: {name} is {s['state']} with no evidence")
    full = {n: slot_state(slots[n]) for n in CAUSES}
    scoped = {n: v[1] for n, v in full.items() if v[0] == "ABSENT_AT_SENSITIVITY"}
    states = {n: ("ruled_out" if v[0] == "ABSENT_AT_SENSITIVITY" else v[0]) for n, v in full.items()}
    unrun = [n for n in CAUSES if states[n] == "void"]
    supported = [n for n in CAUSES if states[n] == "supported"]
    derived_none = "supported" if all(states[n] == "ruled_out" for n in CAUSES) else ("void" if unrun else "ruled_out")
    declared_none = slots["none_of_above"]["state"]
    if declared_none != derived_none:
        raise CardError(f"{card['id']}: none_of_above declared {declared_none}, derived {derived_none}")
    if unrun:
        return "OPEN", dict(unrun=unrun, supported=supported, **({"scoped": scoped} if scoped else {}))
    if derived_none == "supported":
        if card["branch"] == "void":
            raise CardError(f"{card['id']}: CURIOSITY needs its own branch")
        return "CURIOSITY", dict(branch=card["branch"], **({"scoped": scoped} if scoped else {}))
    rw = card["recheck_when"]
    if rw != "void":
        if not isinstance(rw, list) or not rw:
            raise CardError(f"{card['id']}: recheck_when must be void or a list of tool ids")
        return "PROVISIONAL", dict(supported=supported, awaiting=list(rw), **({"scoped": scoped} if scoped else {}))
    return "RESOLVED", dict(supported=supported, **({"scoped": scoped} if scoped else {}))


def load_all(root=HERE):
    return {os.path.basename(p)[:-5]: miniyaml.load(p)
            for p in sorted(glob.glob(os.path.join(root, "ledger", "toolkit", "cards", "*.yaml")))}


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("refused: the checks live in forest-model-ledger/tests/test_l0.py"); sys.exit(2)
    for cid, card in load_all().items():
        reading, detail = read(card)
        print(f"{cid:44s} {reading:11s} {detail}")
