"""ADDITION 8. Coincidence card: opened whenever two equation families agree.

Agreement between families is an observation to be explained, not support for
either. Two existing instruments are wired in, neither copied:

  divergence-playground/coincidence.py   loaded by path. It holds four generators,
      C1 same object two shadows, C2 trials factor, C3 elastic target, C4 real
      common cause. The work order names C1-C6; that file has C1-C4, so C5 and
      C6 are recorded here as NOT IN THE SOURCE FILE and are not invented.
  forest-model-ledger coincidence_card   its six slots and its reading rule
      (OPEN / RESOLVED / PROVISIONAL / CURIOSITY, none_of_above derived, never
      declared). That module reads YAML through the ledger's own loader, so the
      rule is restated here and the slot names are kept identical.

Nothing sets a slot automatically. The C tests return evidence; a person reads
it and sets the slot with set_slot().
"""
import importlib.util, os

CAUSES = ("shared_constraint", "local_normal_form", "statistical_artifact", "numerical_artifact", "low_dim_projection")
SLOTS = CAUSES + ("none_of_above",)
STATES = ("void", "supported", "ruled_out")
C_TESTS = ("C1", "C2", "C3", "C4", "C5", "C6")
NOT_IN_SOURCE = "NOT IN THE SOURCE FILE (divergence-playground/coincidence.py holds C1-C4)"
_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "divergence-playground", "coincidence.py")


def source():
    """The divergence-playground module, or None when the sibling folder is not there."""
    path = os.path.abspath(_SRC)
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location("_divergence_coincidence", path)
    mod = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[spec.name] = mod            # dataclasses resolve their module by name
    spec.loader.exec_module(mod)
    return mod


def open_card(card_id, observation, trigger):
    return dict(id=card_id, observation=observation, trigger=trigger,
                slots={s: dict(state="void", evidence="void") for s in SLOTS},
                c_tests={c: (NOT_IN_SOURCE if c in ("C5", "C6") else "NOT RUN") for c in C_TESTS},
                recheck_when="void", branch="void")


def set_slot(card, slot, state, evidence):
    if slot not in CAUSES:
        raise ValueError("slot %r: none_of_above is derived, the others are %r" % (slot, CAUSES))
    if state not in STATES:
        raise ValueError("state %r not in %r" % (state, STATES))
    if state != "void" and (not evidence or evidence == "void"):
        raise ValueError("%s set to %s needs evidence" % (slot, state))
    card["slots"][slot] = dict(state=state, evidence=evidence)
    return card


def read(card):
    """Same rule as forest-model-ledger/ledger/toolkit/coincidence_card.py::read."""
    st = {n: card["slots"][n]["state"] for n in CAUSES}
    unrun = [n for n in CAUSES if st[n] == "void"]
    supported = [n for n in CAUSES if st[n] == "supported"]
    if unrun:
        return "OPEN", dict(unrun=unrun, supported=supported)
    if all(st[n] == "ruled_out" for n in CAUSES):
        card["slots"]["none_of_above"] = dict(state="supported", evidence="derived: all five causes ruled out")
        if card["branch"] == "void":
            raise ValueError("%s: CURIOSITY needs its own branch" % card["id"])
        return "CURIOSITY", dict(branch=card["branch"])
    card["slots"]["none_of_above"] = dict(state="ruled_out", evidence="derived: a named cause is supported")
    if card["recheck_when"] != "void":
        return "PROVISIONAL", dict(supported=supported, awaiting=list(card["recheck_when"]))
    return "RESOLVED", dict(supported=supported)


def run_c1(card, name_a, value_a, name_b, value_b, map_expr, map_fn, tolerance):
    src = source()
    card["c_tests"]["C1"] = src.C1Test(name_a, value_a, name_b, value_b, map_expr, map_fn, tolerance).run() if src else "SOURCE FILE NOT FOUND"
    return card["c_tests"]["C1"]


def run_c2(card, p_local, n_trials):
    src = source()
    card["c_tests"]["C2"] = src.c2_trials_factor(p_local, n_trials) if src else "SOURCE FILE NOT FOUND"
    return card["c_tests"]["C2"]


def run_c3(card, observed, target, pre_window, declared_at):
    if not declared_at:
        raise ValueError("C3 needs declared_at: when the window was fixed, before the number was seen")
    src = source()
    card["c_tests"]["C3"] = src.C3Test(observed, target, pre_window, declared_at).run() if src else "SOURCE FILE NOT FOUND"
    return card["c_tests"]["C3"]


def run_c4(card, cause, prediction, predicted_value, predicted_uncertainty, pre_registered_at, observed_value=None):
    src = source()
    card["c_tests"]["C4"] = (src.C4Test(cause, prediction, predicted_value, predicted_uncertainty, pre_registered_at).run(observed_value)
                             if src else "SOURCE FILE NOT FOUND")
    return card["c_tests"]["C4"]


def on_agreement(rows, window, declared_at):
    """rows: [dict(model, family, output)]. window: the agreement half-width, fixed
    before the outputs were seen. Returns one OPEN card per cross-family pair that
    agrees inside it. Same-family agreement opens nothing."""
    if window is None or not declared_at:
        return dict(state="NOT CHECKED", reason="no pre-declared agreement window; a window set after the fact is void (C3)")
    cards = []
    ok = [r for r in rows if isinstance(r.get("output"), (int, float))]
    for i in range(len(ok)):
        for j in range(i + 1, len(ok)):
            a, b = ok[i], ok[j]
            if a["family"] != b["family"] and abs(a["output"] - b["output"]) <= window:
                c = open_card("CC_%s_%s" % (a["model"], b["model"]),
                              "%s (%s) and %s (%s) agree: %r vs %r" % (a["model"], a["family"], b["model"], b["family"], a["output"], b["output"]),
                              "cross-family agreement inside the pre-declared window %r (%s)" % (window, declared_at))
                run_c3(c, a["output"], b["output"], window, declared_at)
                cards.append(c)
    return dict(state="CHECKED", window=window, declared_at=declared_at, cards=cards,
                readings=[(c["id"], read(c)[0]) for c in cards])
