"""Results: the twelve outputs of spec section 8, written out and rendered."""
import json

OUTPUTS = ("configuration_record", "equation", "boundary_specification", "control_specification",
           "parameter_values", "initial_conditions", "observations_and_predictions",
           "uncertainty_propagation", "perturbation_response", "continuity_and_transitions",
           "applicability_region", "known_limitations")
NOT_RUN = "NOT RUN"


def check(record):
    missing = [o for o in OUTPUTS if o not in record]
    if missing:
        raise ValueError("record lacks outputs %s (write %r)" % (missing, NOT_RUN))
    from . import claims
    if "claims" not in record:
        raise ValueError("record carries no claims list (ADDITION 5)")
    claims.check(record["claims"])
    return record


def write(record, path):
    check(record)
    with open(path, "w") as f:
        json.dump(record, f, indent=1, sort_keys=True, default=str)
        f.write("\n")


def render(record):
    check(record)
    lines = ["run %s   model %s   status %s" % (record.get("run_id"), record["equation"]["name"], record.get("status"))]
    for o in OUTPUTS:
        v = record[o]
        s = v if isinstance(v, str) else json.dumps(v, sort_keys=True, default=str)
        lines.append("  %-30s %s" % (o, s if len(s) < 150 else s[:147] + "..."))
    return "\n".join(lines)
