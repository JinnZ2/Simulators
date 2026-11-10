"""Instrument-level experiment procedures (v0.3). Standard library only.

Each procedure wraps the v0.2 transition engine in a controlled experiment
and records the outcome as an ``experiment`` record. The same boundary holds
as everywhere else in the lab: these procedures record what the instrument
did and what it produced; they assign no cause, significance, robustness
score, or verdict. Words like "stable" or "sensitive" are deliberately
avoided in payloads — appearance counts and lists are recorded, and any
characterization is left to a separately recorded human judgment.

Procedures:
  1. null_baseline_scan   — scan seeded synthetic noise with no planted
                            structure; record candidate regions per replication.
  2. threshold_sweep      — scan one case set at several thresholds; record
                            the region set as a function of threshold.
  3. order_permutation_probe — scan one case set in its given order and in
                            seeded permutations; record region appearance
                            across orders.
  4. coupling_scan        — scan one case set against two recorded factors;
                            record where candidate regions coincide or differ.

Synthetic data is labeled as synthetic in every payload that contains it.
"""
from __future__ import annotations

from typing import Any, Iterable
import math
import random

from .core import Record
from .transitions import Case, scan_transitions, THRESHOLD_KINDS

DISTRIBUTIONS = ("uniform", "normal")
EXPERIMENT_KINDS = ("null_baseline_scan", "threshold_sweep",
                    "order_permutation_probe", "coupling_scan")

SYNTHETIC_LABEL = ("synthetic (generated for instrument exercise; "
                   "no empirical content)")


def _validate_threshold(threshold: float) -> float:
    if not math.isfinite(float(threshold)) or threshold < 0:
        raise ValueError("threshold must be finite and non-negative.")
    return float(threshold)


def _validate_kind(threshold_kind: str) -> str:
    if threshold_kind not in THRESHOLD_KINDS:
        raise ValueError(f"threshold_kind must be one of {THRESHOLD_KINDS}.")
    return threshold_kind


def _region_key(region: dict[str, Any]) -> str:
    """Order-independent identity of a between-pair, for cross-scan tallying."""
    left, right = region["between"]
    return "|".join(sorted((str(left), str(right))))


def _region_brief(region: dict[str, Any]) -> dict[str, Any]:
    return {
        "between": list(region["between"]),
        "direction": region["direction"],
        "metric_kind": region["metric_kind"],
        "metric_value": region["metric_value"],
        "threshold": region["threshold"],
    }


def null_baseline_scan(*, n_cases: int, n_replications: int, threshold: float,
                       seed: int, threshold_kind: str = "absolute",
                       distribution: str = "uniform",
                       low: float = 0.0, high: float = 100.0,
                       mean: float = 0.0, sd: float = 1.0,
                       factor_start: float = 0.0, factor_step: float = 1.0,
                       zero_tolerance: float = 0.0,
                       factor_label: str = "factor",
                       output_label: str = "output",
                       label: str | None = None) -> dict[str, Any]:
    """Scan synthetic noise with no planted structure; record what is flagged.

    The output is a null-baseline record: how many candidate transition
    regions the engine reports, and where, when the scanned data is known
    (by construction, and labeled) to contain no planted transition. Future
    scans of real data can be recorded alongside this record; whether any
    difference matters is not decided here.
    """
    if not isinstance(n_cases, int) or n_cases < 2:
        raise ValueError("n_cases must be an integer >= 2.")
    if not isinstance(n_replications, int) or n_replications < 1:
        raise ValueError("n_replications must be an integer >= 1.")
    threshold = _validate_threshold(threshold)
    threshold_kind = _validate_kind(threshold_kind)
    if distribution not in DISTRIBUTIONS:
        raise ValueError(f"distribution must be one of {DISTRIBUTIONS}.")
    if distribution == "uniform" and not low < high:
        raise ValueError("uniform distribution requires low < high.")
    if distribution == "normal" and not sd > 0:
        raise ValueError("normal distribution requires sd > 0.")

    rng = random.Random(seed)
    replications: list[dict[str, Any]] = []
    for rep in range(n_replications):
        if distribution == "uniform":
            outputs = [rng.uniform(low, high) for _ in range(n_cases)]
        else:
            outputs = [rng.gauss(mean, sd) for _ in range(n_cases)]
        cases = [Case(case_id=f"null_{rep:03d}_{i:03d}",
                      factor_value=factor_start + i * factor_step,
                      output_value=outputs[i],
                      factor_label=factor_label,
                      output_label=output_label,
                      notes=(SYNTHETIC_LABEL,))
                 for i in range(n_cases)]
        result = scan_transitions(cases, threshold=threshold,
                                  threshold_kind=threshold_kind,
                                  zero_tolerance=zero_tolerance,
                                  scan_label=f"{label or 'null_baseline'}_rep_{rep}")
        replications.append({
            "replication": rep,
            "candidate_region_count": len(result["candidate_regions"]),
            "candidate_regions": [_region_brief(r)
                                  for r in result["candidate_regions"]],
            "deltas_computed": result["deltas_computed"],
            "deltas_not_computed": result["deltas_not_computed"],
        })

    counts = [r["candidate_region_count"] for r in replications]
    return {
        "experiment_kind": "null_baseline_scan",
        "label": label,
        "data_status": SYNTHETIC_LABEL,
        "planted_structure": "none (by construction)",
        "generator": {
            "distribution": distribution,
            "parameters": ({"low": float(low), "high": float(high)}
                           if distribution == "uniform"
                           else {"mean": float(mean), "sd": float(sd)}),
            "seed": seed,
            "factor_grid": {"start": float(factor_start),
                            "step": float(factor_step)},
        },
        "scan_config": {
            "threshold": threshold,
            "threshold_kind": threshold_kind,
            "zero_tolerance": float(zero_tolerance),
        },
        "replications": replications,
        "recorded_summary": {
            "replications": n_replications,
            "cases_per_replication": n_cases,
            "min_candidate_regions": min(counts),
            "max_candidate_regions": max(counts),
            "mean_candidate_regions": sum(counts) / len(counts),
            "summary_basis": ("recorded counts over synthetic replications; "
                              "no significance assigned"),
        },
        "interpretation": "unassigned",
        "limitations": [
            "Counts on known-null data are recorded observations about the "
            "instrument, not a calibrated error rate.",
            "The noise distribution is a chosen generator, not a model of "
            "any real measurement process.",
            "No verdict is assigned about whether any count is acceptable.",
        ],
    }


def threshold_sweep(cases: Iterable[Case], *, thresholds: Iterable[float],
                    threshold_kind: str = "absolute",
                    zero_tolerance: float = 0.0,
                    sweep_label: str | None = None) -> dict[str, Any]:
    """Scan one case set at each threshold; record regions per threshold.

    Thresholds are used in the order given, never sorted. For each distinct
    between-pair flagged at any threshold, the thresholds at which it
    appeared are recorded; nothing is concluded from that pattern here.
    """
    ordered = list(cases)
    if not ordered:
        raise ValueError("threshold_sweep requires at least one case.")
    threshold_kind = _validate_kind(threshold_kind)
    threshold_list = [_validate_threshold(t) for t in thresholds]
    if not threshold_list:
        raise ValueError("threshold_sweep requires at least one threshold.")

    per_threshold: list[dict[str, Any]] = []
    appearances: dict[str, dict[str, Any]] = {}
    for t in threshold_list:
        result = scan_transitions(ordered, threshold=t,
                                  threshold_kind=threshold_kind,
                                  zero_tolerance=zero_tolerance,
                                  scan_label=f"{sweep_label or 'sweep'}_at_{t}")
        regions = [_region_brief(r) for r in result["candidate_regions"]]
        per_threshold.append({
            "threshold": t,
            "candidate_region_count": len(regions),
            "candidate_regions": regions,
        })
        for r in result["candidate_regions"]:
            key = _region_key(r)
            entry = appearances.setdefault(key, {
                "between": list(r["between"]),
                "appears_at_thresholds": [],
            })
            entry["appears_at_thresholds"].append(t)

    return {
        "experiment_kind": "threshold_sweep",
        "sweep_label": sweep_label,
        "factor_label": ordered[0].factor_label,
        "output_label": ordered[0].output_label,
        "case_count": len(ordered),
        "case_ids_in_given_order": [c.case_id for c in ordered],
        "thresholds_in_given_order": threshold_list,
        "threshold_kind": threshold_kind,
        "per_threshold": per_threshold,
        "region_appearances": [
            {**v, "appearance_count": len(v["appears_at_thresholds"]),
             "sweep_points": len(threshold_list)}
            for v in appearances.values()
        ],
        "ordering_rule": "thresholds and cases used in given order; never sorted",
        "interpretation": "unassigned",
        "limitations": [
            "Appearance across thresholds is recorded, not characterized as "
            "stability or instability.",
            "The threshold ladder is analyst-chosen; the record does not "
            "judge the choice.",
        ],
    }


def order_permutation_probe(cases: Iterable[Case], *, n_permutations: int,
                            threshold: float, seed: int,
                            threshold_kind: str = "absolute",
                            zero_tolerance: float = 0.0,
                            probe_label: str | None = None) -> dict[str, Any]:
    """Scan the given order plus seeded permutations; record appearances.

    The engine's contract is that input order is preserved and load-bearing.
    This probe records how the candidate-region set varies when that order
    is permuted. Scan 0 is always the given order.
    """
    ordered = list(cases)
    if len(ordered) < 2:
        raise ValueError("order_permutation_probe requires at least two cases.")
    if not isinstance(n_permutations, int) or n_permutations < 1:
        raise ValueError("n_permutations must be an integer >= 1.")
    threshold = _validate_threshold(threshold)
    threshold_kind = _validate_kind(threshold_kind)

    rng = random.Random(seed)
    scans: list[dict[str, Any]] = []
    appearances: dict[str, dict[str, Any]] = {}

    def run(order: list[Case], scan_index: int, order_kind: str) -> None:
        result = scan_transitions(order, threshold=threshold,
                                  threshold_kind=threshold_kind,
                                  zero_tolerance=zero_tolerance,
                                  scan_label=f"{probe_label or 'permute'}_scan_{scan_index}")
        regions = [_region_brief(r) for r in result["candidate_regions"]]
        scans.append({
            "scan_index": scan_index,
            "order_kind": order_kind,
            "case_ids_in_scanned_order": [c.case_id for c in order],
            "candidate_region_count": len(regions),
            "candidate_regions": regions,
        })
        for r in result["candidate_regions"]:
            key = _region_key(r)
            entry = appearances.setdefault(key, {
                "between_pair_unordered": sorted(map(str, r["between"])),
                "appears_in_scans": [],
            })
            entry["appears_in_scans"].append(scan_index)

    run(ordered, 0, "given_order")
    for p in range(1, n_permutations + 1):
        shuffled = list(ordered)
        rng.shuffle(shuffled)
        run(shuffled, p, "seeded_permutation")

    total = n_permutations + 1
    return {
        "experiment_kind": "order_permutation_probe",
        "probe_label": probe_label,
        "factor_label": ordered[0].factor_label,
        "output_label": ordered[0].output_label,
        "case_count": len(ordered),
        "seed": seed,
        "scan_config": {"threshold": threshold,
                        "threshold_kind": threshold_kind,
                        "zero_tolerance": float(zero_tolerance)},
        "scans": scans,
        "region_appearances": [
            {**v, "appearance_count": len(v["appears_in_scans"]),
             "total_scans": total}
            for v in appearances.values()
        ],
        "interpretation": "unassigned",
        "limitations": [
            "Appearance across permutations is recorded, not characterized "
            "as robustness or fragility.",
            "A permuted order is a different input to the engine, not an "
            "error; the engine's no-sorting contract still holds per scan.",
        ],
    }


def coupling_scan(entries: Iterable[dict[str, Any]], *, threshold: float,
                  factor_a_label: str = "factor_a",
                  factor_b_label: str = "factor_b",
                  output_label: str = "output",
                  threshold_kind: str = "absolute",
                  zero_tolerance: float = 0.0,
                  coupling_label: str | None = None) -> dict[str, Any]:
    """Scan one case set against two recorded factors; record (non)coincidence.

    Each entry supplies the same case observed against two factors, e.g.
    ``{"case_id": ..., "factor_a": ..., "factor_b": ..., "output": ...}``.
    Each factor is scanned separately in the given order. Coincidence of
    candidate regions across factors is recorded; whether it indicates a
    shared cause, a confound, or nothing is explicitly not decided.
    """
    rows = list(entries)
    if len(rows) < 2:
        raise ValueError("coupling_scan requires at least two entries.")
    threshold = _validate_threshold(threshold)
    threshold_kind = _validate_kind(threshold_kind)

    ids: list[str] = []
    cases_a: list[Case] = []
    cases_b: list[Case] = []
    for i, row in enumerate(rows):
        case_id = row.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip():
            raise ValueError(f"entry {i}: case_id must be a non-empty string.")
        if case_id in ids:
            raise ValueError(f"entry {i}: duplicate case_id {case_id!r}.")
        ids.append(case_id)
        notes = tuple(row.get("notes", ()))
        cases_a.append(Case(case_id, row.get("factor_a"), row.get("output"),
                            factor_a_label, output_label, notes))
        cases_b.append(Case(case_id, row.get("factor_b"), row.get("output"),
                            factor_b_label, output_label, notes))

    scan_a = scan_transitions(cases_a, threshold=threshold,
                              threshold_kind=threshold_kind,
                              zero_tolerance=zero_tolerance,
                              scan_label=f"{coupling_label or 'couple'}_a")
    scan_b = scan_transitions(cases_b, threshold=threshold,
                              threshold_kind=threshold_kind,
                              zero_tolerance=zero_tolerance,
                              scan_label=f"{coupling_label or 'couple'}_b")

    keys_a = {_region_key(r): r for r in scan_a["candidate_regions"]}
    keys_b = {_region_key(r): r for r in scan_b["candidate_regions"]}
    coincident = sorted(set(keys_a) & set(keys_b))
    only_a = sorted(set(keys_a) - set(keys_b))
    only_b = sorted(set(keys_b) - set(keys_a))

    return {
        "experiment_kind": "coupling_scan",
        "coupling_label": coupling_label,
        "factor_a_label": factor_a_label,
        "factor_b_label": factor_b_label,
        "output_label": output_label,
        "case_count": len(rows),
        "case_ids_in_given_order": ids,
        "scan_config": {"threshold": threshold,
                        "threshold_kind": threshold_kind,
                        "zero_tolerance": float(zero_tolerance)},
        "factor_a_scan": {
            "candidate_regions": [_region_brief(r)
                                  for r in scan_a["candidate_regions"]],
            "deltas_computed": scan_a["deltas_computed"],
            "deltas_not_computed": scan_a["deltas_not_computed"],
            "unresolved": scan_a["unresolved"],
        },
        "factor_b_scan": {
            "candidate_regions": [_region_brief(r)
                                  for r in scan_b["candidate_regions"]],
            "deltas_computed": scan_b["deltas_computed"],
            "deltas_not_computed": scan_b["deltas_not_computed"],
            "unresolved": scan_b["unresolved"],
        },
        "coincidence_record": {
            "coincident_pairs": [sorted(map(str, keys_a[k]["between"]))
                                 for k in coincident],
            "factor_a_only_pairs": [sorted(map(str, keys_a[k]["between"]))
                                    for k in only_a],
            "factor_b_only_pairs": [sorted(map(str, keys_b[k]["between"]))
                                    for k in only_b],
            "note": ("Coincidence of candidate regions across factors is "
                     "recorded only; it does not establish a shared cause, "
                     "a confound, or its absence."),
        },
        "interpretation": "unassigned",
        "limitations": [
            "Each factor is scanned independently; joint factor structure "
            "is not modeled.",
            "A region appearing under only one factor is recorded, not "
            "explained.",
        ],
    }


def make_experiment_record(payload: dict[str, Any],
                           linked_record_ids: Iterable[str] = ()) -> Record:
    """Wrap an experiment payload in an ``experiment`` record."""
    if payload.get("experiment_kind") not in EXPERIMENT_KINDS:
        raise ValueError(f"experiment_kind must be one of {EXPERIMENT_KINDS}.")
    payload = {**payload, "linked_record_ids": list(linked_record_ids)}
    return Record.create("experiment", payload)
