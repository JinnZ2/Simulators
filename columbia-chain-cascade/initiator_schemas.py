#!/usr/bin/env python3
# initiator_schemas.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# Modules A-E are declared in SOURCE_DROP.md as initiators and named by
# gaps 5-9 as the consumers of their deliverables -- and they existed as
# section headers, not code (CCA_016). This file is the drop-in those
# five gaps lacked: the COLUMN LIST each deliverable carries, a loader
# that refuses a file with the wrong columns, and the one interface
# every initiator shares (CCC_007: each writes only a hydrograph; the
# routing engine downstream is identical).
#
# No physics. No default value for any column. A schema says what a
# row must NAME, not what it must equal; every row carries the
# knowledge_state the repo runs on.

import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import knowledge_state  # noqa: E402

# Every table shares these leading columns. A node is named by the
# delivered node list (eap_coverage_v2.NODES); a knowledge_state is one
# of knowledge_state.VALID_STATES; `source` and `would_move_it` are the
# what-would-move-it discipline as columns, so no row can be a bare
# number.
COMMON = ("node", "knowledge_state", "source", "would_move_it")

SCHEMAS = {
    # Gap 5 -> Module A, single-structure breach
    "breach_params.csv": COMMON + (
        "dam_type",            # earthfill / concrete gravity / arch / ...
        "height_m", "crest_length_m", "storage_m3",
        "breach_width_m_froehlich", "breach_width_m_xuzhang",
        "breach_side_slope", "time_to_failure_h_froehlich",
        "time_to_failure_h_xuzhang",
        "initial_condition",   # sunny-day | flood-pool
        "height_sensitivity_pct_per_10pct",
    ),
    # Gap 6 -> Module B, seismic ground motion
    "seismic_params.csv": COMMON + (
        "pga_g", "pgv_cm_s", "sa_at_dam_period_g", "vs30_m_s",
        "site_class", "aftershock_delay_days_p50",
        "aftershock_delay_days_p90", "damage_state_carry_forward",
    ),
    # Gap 7 -> Module C, atmospheric-river inflow
    "hydro_params.csv": COMMON + (
        "ar_event_id", "ar_scale", "peak_inflow_m3_s",
        "time_to_peak_h", "volume_m3", "gate_capacity_m3_s",
        "partial_opening_sufficient",   # True | False | UNMEASURED
        "cmip6_adjusted_peak_m3_s",
    ),
    # Gap 8 -> Module D, cyber / control
    "cyber_params.yaml": COMMON + (
        "scada_trust_state",     # binary | degraded | adversarial
        "gates_open_fraction", "duration_h",
        "manual_override_p50_min", "manual_override_p90_min",
        "compound_factor_vs_normal_ops",
    ),
    # Gap 9 -> Module E, compound
    "compound_matrix.csv": COMMON + (
        "initiator_pair",        # B+D | C+D | B+C+D
        "interaction_type",      # simultaneous | sequential | delayed
        "delay_h", "interaction_factor",
        "interaction_factor_tolerance",   # the falsifier needs a band
        "elicitation_or_measured",
    ),
}

GAP_OF = {"breach_params.csv": 5, "seismic_params.csv": 6,
          "hydro_params.csv": 7, "cyber_params.yaml": 8,
          "compound_matrix.csv": 9}


def schema(name):
    if name not in SCHEMAS:
        raise KeyError("no schema for %r; have %s"
                       % (name, sorted(SCHEMAS)))
    return SCHEMAS[name]


def validate_rows(name, rows):
    """rows: list of dicts. Refuses on a missing column, an extra column,
    or a row whose knowledge_state is not a valid state. Returns the
    row count; never fills a value in."""
    cols = set(schema(name))
    for i, r in enumerate(rows):
        have = set(r)
        missing = cols - have
        extra = have - cols
        if missing or extra:
            raise ValueError("row %d: missing %s extra %s"
                             % (i, sorted(missing), sorted(extra)))
        knowledge_state.validate(r["knowledge_state"],
                                 "%s row %d" % (name, i))
    return len(rows)


def load_csv(name, path):
    with io.open(path, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    validate_rows(name, rows)
    return rows


def hydrograph_interface():
    """What every initiator writes, and nothing else (CCC_007). The
    same key set bridge-impoundment's release initiator carries."""
    return ("peak_flow", "time_to_peak", "volume", "debris_load",
            "provenance")


def render():
    out = []
    w = out.append
    w("INITIATOR SCHEMAS -- the drop-in gaps 5-9 lacked")
    w("")
    for name in sorted(SCHEMAS, key=lambda n: GAP_OF[n]):
        w("Gap %d -> %s   (%d columns)"
          % (GAP_OF[name], name, len(SCHEMAS[name])))
        for c in SCHEMAS[name]:
            w("    %s" % c)
        w("")
    w("every initiator writes exactly: %s" % ", ".join(hydrograph_interface()))
    w("")
    w("A schema names what a row carries; it sets no value. Every row")
    w("carries a knowledge_state, a source, and what would move it, so a")
    w("bare number cannot enter. The loader refuses a file with a missing")
    w("or extra column rather than reading what it can.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write("initiator_schemas.py has no checks of its own; "
                         "they live in selftest_kill.py.\n")
        sys.exit(2)
    print(render())
