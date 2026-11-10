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
                      ("delay", ["NO_MOVE"]),
                      ("flip_x", ["E", "W"]), ("flip_x", ["W", "W", "E", "E"]),
                      ("momentum", ["N", "WAIT", "S"])):
        pos, preds = ch.reported(), []
        for a in acts:
            pos = plain(pos, a, ch.size)
            preds.append(pos)
        record_self(log, predicted_specific=acts[0],
                    predicted_category="wait" if acts[0] in ("WAIT", "NO_MOVE") else "move",
                    actual_specific=acts[0], note="self: first action of the next path")
        probe_path(ch, acts, preds, log, rule_hypothesis=hyp)
    return log


# CONSTRUCTED fixture for the fingerprint-decay arm: a seed habit (mostly N, some
# E and waits) drifting into equal use of the four moves. Not from any real log.
CONSTRUCTED_SEED_FP = {"N": 0.6, "S": 0.0, "E": 0.2, "W": 0.0, "WAIT": 0.2}
CONSTRUCTED_CYCLES = [["N"] * 6 + ["E"] * 2 + ["WAIT"] * 2,
                      ["N"] * 5 + ["E"] * 2 + ["S"] + ["NO_MOVE"] * 2,
                      ["N"] * 4 + ["E"] * 2 + ["S"] * 2 + ["W"] * 2,
                      ["N"] * 3 + ["E"] * 3 + ["S"] * 2 + ["W"] * 2,
                      ["N", "E", "S", "W"] * 3]


def write_samples(seed=7):
    import fingerprint
    import markers
    sd = os.path.join(HERE, "samples")
    txt = render(run(seed, os.path.join(sd, "misslog.sample.jsonl")).records())
    with open(os.path.join(sd, "readout.sample.txt"), "w") as fh:
        fh.write(txt + "\n")
    with open(os.path.join(sd, "markers.sample.txt"), "w") as fh:
        fh.write(markers.render(markers.compare_marks(seed)) + "\n")
        fh.write("\nsame searcher, plain chamber (no rules):\n")
        fh.write("\n".join(markers.render(markers.compare_marks(seed, rules={})).splitlines()[2:]) + "\n")
    with open(os.path.join(sd, "fingerprint.sample.txt"), "w") as fh:
        fh.write(fingerprint.render(fingerprint.decay([], fingerprint.load_seed("prior-conversation")["fingerprint"])) + "\n")
        fh.write("\nCONSTRUCTED fixture (demo.CONSTRUCTED_SEED_FP; not a real prior conversation):\n")
        fh.write("\n".join(fingerprint.render(fingerprint.decay(CONSTRUCTED_CYCLES, CONSTRUCTED_SEED_FP)).splitlines()[2:]) + "\n")
    return txt


if __name__ == "__main__":
    if "--samples" in sys.argv:
        print(write_samples())
        sys.exit(0)
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 7
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(HERE, "samples", "misslog.sample.jsonl")
    print(render(run(seed, out).records()))
