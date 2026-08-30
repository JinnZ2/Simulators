#!/usr/bin/env python3
# knowledge_state.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# The epistemic state vocabulary for variables that are physically relevant
# but not yet quantified. See SCOPE_BOUNDARY.md for the rationale.
#
# VALID STATES:
#   UNKNOWN_ATM     — mechanism known, no current value
#   UNDER_STUDY     — data collection in progress, provisional
#   NOT_STUDIED     — mechanism recognized, never measured here
#   UNDEFINED       — no agreed definition or measurement protocol
#
# INVALID STATE (rejected):
#   INSTITUTIONAL_EXCLUSION — not a valid epistemic state.
#     If a variable physically influences the system, excluding it because
#     of ownership boundaries is a scope error, not a knowledge state.

# The four valid states
UNKNOWN_ATM = "UNKNOWN_ATM"
UNDER_STUDY = "UNDER_STUDY"
NOT_STUDIED = "NOT_STUDIED"
UNDEFINED = "UNDEFINED"

VALID_STATES = (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)

# The rejected state — present for explicit refusal
INSTITUTIONAL_EXCLUSION = "INSTITUTIONAL_EXCLUSION"


def is_valid(state):
    """True iff the state is a valid epistemic state."""
    return state in VALID_STATES


def validate(state, variable_name=""):
    """Raise ValueError if the state is not valid.

    If the state is INSTITUTIONAL_EXCLUSION, the error message explains
    why it is rejected."""
    if state == INSTITUTIONAL_EXCLUSION:
        raise ValueError(
            "INSTITUTIONAL_EXCLUSION is not a valid epistemic state for %s. "
            "If this variable physically influences the system, excluding it "
            "because of ownership boundaries is a scope error, not a knowledge "
            "state. Use UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, or UNDEFINED "
            "instead. See SCOPE_BOUNDARY.md." % variable_name)
    if not is_valid(state):
        raise ValueError(
            "%r is not a valid epistemic state. Valid states: %s"
            % (state, ", ".join(VALID_STATES)))
    return True


def render_state(state, description=""):
    """A human-readable rendering of a knowledge state."""
    if state == UNKNOWN_ATM:
        return "UNKNOWN_ATM — mechanism known, no current value available"
    if state == UNDER_STUDY:
        return "UNDER_STUDY — data collection in progress, value provisional"
    if state == NOT_STUDIED:
        return "NOT_STUDIED — mechanism recognized, never measured for this system"
    if state == UNDEFINED:
        return "UNDEFINED — no agreed definition or measurement protocol"
    return "%s — %s" % (state, description)


def render():
    out = []
    w = out.append
    w("KNOWLEDGE STATE VOCABULARY")
    w("")
    w("Valid epistemic states for physically relevant but unquantified variables:")
    for s in VALID_STATES:
        w("  %s" % render_state(s))
    w("")
    w("Rejected state:")
    w("  %s — NOT VALID. If a variable physically influences the system,"
      % INSTITUTIONAL_EXCLUSION)
    w("    excluding it because of ownership boundaries is a scope error,")
    w("    not a knowledge state. See SCOPE_BOUNDARY.md.")
    w("")
    w("Usage: every variable in the spec that is physically relevant but")
    w("not yet quantified carries one of the valid states. The state is")
    w("recorded as data, not commentary, and names what would be needed")
    w("to move it to a quantified state.")
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "knowledge_state.py has no checks of its own. The checks that "
            "exercise it live in selftest_ccc.py.\n"
            "    python3 columbia-chain-cascade/selftest_ccc.py\n")
        sys.exit(2)
    print(render())
