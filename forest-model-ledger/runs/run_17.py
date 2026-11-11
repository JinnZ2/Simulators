"""run_17: parameter_recovery on the candidate anchor, run_11's trigger (card CC_003).

    python3 runs/run_17.py     # about a minute on 4 workers; reproduces samples/run_17.sample.txt

Question the tool asks: from run_11's nine outputs alone, can the pipeline get back a
parameter it was given? One parameter at a time, the rest at DEFAULTS. Synthetic data
at the true value (x1.0) on seeds 100-104; the fit on seeds 0-4 at each grid value.
Parameters chosen to span run_15's classes: dep (moved strongly in run_11), kT
(HIDDEN_IN_NOISE), uG (HIDDEN / ABSORBED pair), aG (ABSORBED), kill_G (INERT x1.1),
p_ign (INERT / UNRESOLVED).
"""
import functools, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import base
from ledger.toolkit import parameter_recovery as pr
from runs import run_11

GRID = [0.6, 0.8, 1.0, 1.2, 1.4]          # multiples of the DEFAULTS value [CHOICE]
PARAMS = ["dep", "kT", "uG", "aG", "kill_G", "p_ign"]
CLASS15 = dict(dep="(not in the 33: moved in run_11)", kT="HIDDEN_IN_NOISE", uG="HIDDEN x1.1 / ABSORBED x0.9",
               aG="ABSORBED", kill_G="INERT x1.1 / ABSORBED x0.9", p_ign="INERT x1.1 / UNRESOLVED x0.9")


def outputs_at(name, mult, seed):
    import warnings
    warnings.simplefilter("ignore")
    return run_11.outputs(base.simulate(seed=seed, params={name: base.DEFAULTS[name] * mult}))


def main():
    from concurrent.futures import ProcessPoolExecutor
    print(f"grid (x DEFAULTS) {GRID}; obs seeds 100-104; fit seeds 0-4; {pr.CHOICES} [CHOICE]")
    with ProcessPoolExecutor(4) as ex:
        for name in PARAMS:
            r = pr.recover(functools.partial(outputs_at, name), 1.0, GRID, range(100, 105), range(5), mapper=ex.map)
            chi = "  ".join(f"{g}:{r['chi2'][g]:8.1f}" for g in GRID)
            print(f"{name:7s} {r['verdict']:16s} theta_hat x{r['theta_hat']}  plausible {r['plausible']}   run_15: {CLASS15[name]}")
            print(f"        chi2 {chi}   outputs skipped (se 0): {r['skipped'] or '-'}")


if __name__ == "__main__":
    main()
