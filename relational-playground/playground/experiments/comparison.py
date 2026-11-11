"""Side-by-side comparison. No winner: rank() raises, and rows come out in name order."""
from . import runner


def side_by_side(configs, output):
    rows = []
    for cfg in sorted(configs, key=lambda c: c["model"]):
        try:
            rec = runner.run(cfg)
            rows.append(dict(model=cfg["model"], run_id=cfg["run_id"], status=rec["status"],
                             output=rec["observations_and_predictions"]["final_state"].get(output, "MODEL HAS NO SUCH VARIABLE"),
                             limitations=rec["known_limitations"]))
        except Exception as e:
            rows.append(dict(model=cfg["model"], run_id=cfg["run_id"], status="MODEL FAILED", error="%s: %s" % (type(e).__name__, e)))
    return dict(output=output, rows=rows, note="no ranking; each row is read with its own applicability record")


def rank(*_a, **_k):
    raise RuntimeError("no automatic model ranking: read the applicability records")
