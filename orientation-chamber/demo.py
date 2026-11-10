"""demo.py -- one scripted agent walk, written as a sample misslog. CC0, stdlib only.

PROPOSED | co-authored (JinnZ2 + Claude). The agent starts from the `median`
seed (a plain-physics prediction), so its MISSes locate where this chamber
differs from a plain one. The sample is a property of the seed and the script.

  python3 demo.py [--seed N] [--out PATH]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from chamber import ACTIONS, Chamber  # noqa: E402
from fix import render  # noqa: E402
from misslog import MissLog  # noqa: E402
from probe import probe_path  # noqa: E402
from selfmode import record_self  # noqa: E402


def plain(pos, a, size):
    dx, dy = ACTIONS[a]
    return (min(max(pos[0] + dx, 0), size - 1), min(max(pos[1] + dy, 0), size - 1))


def run(seed, out):
    if os.path.exists(out):
        os.remove(out)
    log, ch = MissLog(out), Chamber(seed=seed)
    for hyp, acts in ((None, ["N", "E", "S", "W"]), (None, ["N", "E", "S", "W"]),
                      ("flip_x", ["E", "W"]), ("flip_x", ["W", "W", "E", "E"]),
                      ("momentum", ["N", "WAIT", "S"])):
        pos, preds = ch.reported(), []
        for a in acts:
            pos = plain(pos, a, ch.size)
            preds.append(pos)
        record_self(log, predicted_specific=acts[0], predicted_category="move",
                    actual_specific=acts[0], note="self: first action of the next path")
        probe_path(ch, acts, preds, log, rule_hypothesis=hyp)
    return log


if __name__ == "__main__":
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 7
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(HERE, "samples", "misslog.sample.jsonl")
    print(render(run(seed, out).records()))
