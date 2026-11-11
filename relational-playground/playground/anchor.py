"""ADDITION 2. Anchor loop: ANCHOR -> BRANCH (one change) -> RETURN (diff against the anchor).

The anchor record has the fields of forest-model-ledger/ledger/anchors/ANCHOR_run9.yaml
(id, status, run, seed, params, scope, code with sha256, tests, known_errors,
open_issues) and is stored as JSON. Run statuses follow that ledger's
STATUS_MAP (COMPLETE | INCOMPLETE | REPORTED).

An anchor is 'candidate' until all four tests read PASS:
  budgets_close_within_noise_rule, holds_across_seeds,
  holds_when_each_assumption_nudged, independent_budgets_close_together
"""
import json
from .reporting import provenance
from .experiments import runner
from .experiments.sensitivity import _with_param
from .environment import Environment

TESTS = ("budgets_close_within_noise_rule", "holds_across_seeds",
         "holds_when_each_assumption_nudged", "independent_budgets_close_together")
STATES = ("PASS", "PARTIAL", "FAIL", "NOT RUN")
RUN_STATUSES = ("COMPLETE", "INCOMPLETE", "REPORTED")


class AnchorError(ValueError):
    pass


def freeze(anchor_id, cfg, code_paths, scope, known_errors=(), open_issues=()):
    rec = runner.run(cfg, code_paths)
    return dict(id=anchor_id, status="candidate", run=cfg["run_id"], seed=cfg["environment"].seed,
                params=cfg["parameters"].as_dict(), initial=cfg["initial"].as_dict(), scope=scope,
                config_sha256=rec["provenance"]["config_sha256"], code=rec["provenance"]["code"],
                final_state=rec["observations_and_predictions"]["final_state"], l0_budgets=rec["l0_budgets"],
                run_status=rec["status"],
                tests={t: dict(state="NOT RUN", evidence="void") for t in TESTS},
                known_errors=list(known_errors), open_issues=list(open_issues))


def verify(anchor, cfg, code_paths):
    """Re-run the anchor configuration. Returns the list of differences; empty means it still holds."""
    rec = runner.run(cfg, code_paths)
    diffs = []
    if rec["provenance"]["config_sha256"] != anchor["config_sha256"]:
        diffs.append("configuration hash moved")
    for path, h in anchor["code"].items():
        if rec["provenance"]["code"].get(path) != h:
            diffs.append("code moved: %s" % path)
    if rec["observations_and_predictions"]["final_state"] != anchor["final_state"]:
        diffs.append("final state not bit-identical")
    return diffs


def branch(cfg, branch_id, parameter=None, value=None, **config_change):
    """One change only: one parameter, or one configuration field."""
    n = (1 if parameter is not None else 0) + len(config_change)
    if n != 1:
        raise AnchorError("a branch changes ONE thing; got %d" % n)
    if parameter is not None:
        return _with_param(cfg, parameter, value).with_changes(run_id=branch_id), "parameter %s -> %r" % (parameter, value)
    k = next(iter(config_change))
    return cfg.with_changes(run_id=branch_id, **config_change), "config field %s" % k


def return_diff(anchor, branch_record, change):
    """RETURN: what moved against the anchor, variable by variable. No verdict on which is better."""
    a, b = anchor["final_state"], branch_record["observations_and_predictions"]["final_state"]
    rows = [dict(variable=k, anchor=a.get(k), branch=b.get(k),
                 delta=(b[k] - a[k]) if k in a and k in b else "NOT COMPARABLE") for k in sorted(set(a) | set(b))]
    return dict(anchor=anchor["id"], branch=branch_record["run_id"], change=change, branch_status=branch_record["status"],
                built_on="anchor status %s" % anchor["status"], rows=rows,
                budgets=[dict(budget=r["budget"], verdict=r["verdict"]) for r in branch_record["l0_budgets"]])


def run_tests(anchor, cfg, code_paths, seeds, nudge_names, rel_step=0.05):
    """Fill the four anchor tests from runs. A test that could not be run stays NOT RUN."""
    t = {}
    live = [r for r in anchor["l0_budgets"] if r["verdict"] != "VOID"]
    with_sigma = [r for r in live if r["sigma_meas"] is not None]
    closed = all(r["verdict"] in ("CLOSED", "NOISE") for r in live) and bool(live)
    t["budgets_close_within_noise_rule"] = dict(
        state="FAIL" if not closed else "PASS" if len(with_sigma) == len(live) else "PARTIAL",
        evidence="%d LIVE budget(s) closed at numerical tolerance; sigma_meas stated for %d of %d" % (len(live), len(with_sigma), len(live)))
    stat = []
    for s in seeds:
        env = cfg["environment"]
        stat.append(runner.run(cfg.with_changes(environment=Environment(s, env.forcing, env.label), run_id="%s+seed%d" % (cfg["run_id"], s)), code_paths)["status"])
    t["holds_across_seeds"] = dict(state="PASS" if stat and all(x == "COMPLETE" for x in stat) else "FAIL" if stat else "NOT RUN",
                                   evidence="seeds %s: %d of %d COMPLETE" % (list(seeds), stat.count("COMPLETE"), len(stat)))
    nudged, bad, skipped = 0, [], []
    for n in sorted(cfg["parameters"].values):
        v = cfg["parameters"].values[n].value
        if n not in nudge_names or not isinstance(v, (int, float)) or isinstance(v, bool) or v == 0:
            skipped.append(n)
            continue
        for sgn in (+1, -1):
            nudged += 1
            try:
                if runner.run(_with_param(cfg, n, v * (1 + sgn * rel_step)), code_paths)["status"] != "COMPLETE":
                    bad.append((n, sgn))
            except Exception as e:
                bad.append((n, sgn, type(e).__name__))
    t["holds_when_each_assumption_nudged"] = dict(
        state="NOT RUN" if not nudged else "FAIL" if bad else "PARTIAL" if skipped else "PASS",
        evidence="%d nudges, %d did not close %s; not nudged: %s" % (nudged, len(bad), bad, skipped))
    t["independent_budgets_close_together"] = dict(
        state="PASS" if len(live) == len(anchor["l0_budgets"]) and closed else "PARTIAL" if closed else "FAIL",
        evidence="%d of %d budgets LIVE; the rest VOID" % (len(live), len(anchor["l0_budgets"])))
    anchor = dict(anchor, tests=t)
    anchor["status"] = "anchor" if all(v["state"] == "PASS" for v in t.values()) else "candidate"
    return anchor


def save(anchor, path):
    with open(path, "w") as f:
        json.dump(anchor, f, indent=1, sort_keys=True, default=str)
        f.write("\n")


def load(path):
    with open(path) as f:
        a = json.load(f)
    for k in ("id", "status", "run", "seed", "params", "scope", "code", "tests", "known_errors", "open_issues"):
        if k not in a:
            raise AnchorError("anchor record lacks %s" % k)
    return a
