"""Step 1 end to end: baselines, exports, both feeds, comparison, report.

    python3 playground-crossrun/run_all.py            # everything (~1 min)
    python3 playground-crossrun/run_all.py --no-baseline

STUDY_APERTURE_PATH points at a study-aperture checkout (default ../study-aperture
beside this repository). Each step is a separate process because both builds ship a
package named `playground`. The run ends by checking that neither playground's tracked
files changed.
"""
import os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "adapters"))
import common  # noqa: E402


def run(cmd, cwd, timeout=900):
    t = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout + p.stderr, time.time() - t


def baseline():
    suites = {}
    rc, out, dt = run([sys.executable, "-m", "playground.self_check"], common.SA_EXP)
    m = re.search(r"guards:\s+(\d+)/(\d+).*?defects:\s+(\d+)/(\d+) caught, (\d+)/(\d+) correctly classified.*?controls:\s+(\d+)/(\d+)",
                  out, re.S)
    ran = [int(x) for x in re.findall(r"^Ran (\d+) tests", out, re.M)]
    suites["study-aperture self_check: guards"] = "%s/%s" % (m.group(1), m.group(2)) if m else "UNPARSED"
    suites["study-aperture self_check: planted defects caught / classified"] = \
        "%s/%s caught, %s/%s correctly classified" % m.group(3, 4, 5, 6) if m else "UNPARSED"
    suites["study-aperture self_check: controls"] = "%s/%s" % (m.group(7), m.group(8)) if m else "UNPARSED"
    suites["study-aperture self_check: unit suites"] = "%d suites, %d tests, %s" % (
        len(ran), sum(ran), "COMBINED SELF-CHECK PASSED" if "COMBINED SELF-CHECK PASSED" in out else "FAILED")
    suites["study-aperture self_check: exit"] = rc
    rc2, out2, _ = run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], common.R257)
    m2 = re.search(r"Ran (\d+) tests", out2)
    suites["#257 relational-playground unittest"] = "%s tests, %s" % (m2.group(1) if m2 else "?", "OK" if out2.rstrip().endswith("OK") else "NOT OK")
    suites["#257 unittest exit"] = rc2
    return suites


def main():
    steps = []
    if "--no-baseline" not in sys.argv:
        b = baseline()
    else:
        b = common.load("baseline.json")["suites"] if os.path.exists(os.path.join(common.OUT, "baseline.json")) else {}
    common.dump("baseline.json", dict(suites=b, sa_rev=common.git_rev(common.SA_ROOT), sim_rev=common.git_rev(common.SIM_ROOT)))
    for script in ("export_perplexity.py", "export_257.py", "feed_into_perplexity.py", "feed_into_257.py", "compare.py"):
        rc, out, dt = run([sys.executable, os.path.join(HERE, "adapters", script)], HERE)
        steps.append((script, rc, out.strip().splitlines()[-1] if out.strip() else ""))
        if rc != 0:
            print(out)
            raise SystemExit("step %s failed" % script)
    for s in steps:
        print("%-26s rc=%d  %s" % s)
    dirty = common.git_dirty(common.SIM_ROOT, "relational-playground") + \
        common.git_dirty(common.SA_ROOT, "experimental/playground")
    print("originals untouched:", "YES" if not dirty else "NO -> %s" % dirty)
    return 0 if not dirty else 1


if __name__ == "__main__":
    raise SystemExit(main())
