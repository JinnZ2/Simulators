# SPDX-License-Identifier: CC0-1.0
"""FWO-15 checks. Every fixture is CONSTRUCTED by the agent that wrote the
scorer, so the summary line reads REGRESSION, not validation."""

import ast
import importlib.util
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import enclosure_caveat_register as A   # noqa: E402
import coupling_gradient as B           # noqa: E402
import fwo15_fixtures as F              # noqa: E402

_checks = 0
_failed = 0
FAIL_FIXTURES = {}


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


def render_of(mod):
    buf = io.StringIO()
    mod.render(buf)
    return buf.getvalue()


def defined_names(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    return {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}


# ------------------------------------------------------------------ Build A ---
def t_register():
    for name, (frames, studies), want in [
        ("gap", F.GAP, "GAP_CONFIRMED"),
        ("no-gap", F.NO_GAP, "NO_GAP"),
        ("indeterminate", F.INDETERMINATE, "INDETERMINATE"),
        ("under-floor", F.UNDER_FLOOR, "UNMEASURED"),
    ]:
        r = A.run(frames, studies)
        for arm in A.ANIMAL_ARMS:
            check(r["comparisons"][arm]["branch"] == want,
                  "%s world, human vs %s reads %s (got %s)" % (name, arm, want, r["comparisons"][arm]["branch"]))
        check(r["refused"] == [], "%s world refuses nothing" % name)

    r = A.run(*F.SCOPE)
    c = r["comparisons"]["captive-animal"]
    check(c["branch"] == "SCOPE_LIMITED", "scope world reads SCOPE_LIMITED (got %s)" % c["branch"])
    check(c["gap_in"] == ["sub-A"] and c["no_gap_in"] == ["sub-B"], "scope world names sub-A gap, sub-B no gap")

    # ABSENT E4 never enters the denominator; the rate is per arm with n and frame.
    r = A.run(*F.GAP)
    h = r["arms"]["human"]
    check(h["e4"]["ABSENT"] == 3 and h["n_rate"] == 30 and h["n_studies"] == 33, "E4 ABSENT counted apart (3 of 33)")
    check(abs(h["rate"] - 2 / 30) < 1e-12, "human rate is YES/(YES+NO) = 2/30")
    check(r["frames"]["human"] == ["CONSTRUCTED frame h (human)"], "the human rate carries its frame")
    check(h["e2_modal"] == ["ABSENT"], "E2 ABSENT is the modal human value in the gap world")
    out = io.StringIO()
    A.render_result(r, out)
    check("reported as a FINDING" in out.getvalue(), "modal E2 ABSENT is rendered as a finding")
    check("frame:" in out.getvalue(), "every arm line is followed by its frame")

    # Two animal arms are never pooled [CHOICE 4].
    check(set(r["comparisons"]) == set(A.ANIMAL_ARMS), "one comparison per animal arm, none pooled")

    # caveat_rate and wilson.
    check(A.caveat_rate(0, 0) is None, "empty denominator is None, never 0")
    check(A.caveat_rate(0, 5) == 0.0, "a measured zero stays 0.0")
    check(A.wilson(0, 0) is None, "wilson on n=0 is None")
    lo, hi = A.wilson(5, 10)
    check(abs(lo - 0.2366) < 1e-3 and abs(hi - 0.7634) < 1e-3, "wilson(5,10) = [0.2366, 0.7634] by hand")

    # No corpus -> UNMEASURED everywhere, DESIGN_WRITTEN in the render.
    r0 = A.run([], [])
    check(all(r0["comparisons"][a]["branch"] == "UNMEASURED" for a in A.ANIMAL_ARMS), "no corpus reads UNMEASURED")
    check("DESIGN_WRITTEN" in render_of(A), "render states DESIGN_WRITTEN")

    # FAIL fixture: coded before frame, wrong arm, undeclared frame, missing field.
    frames, studies = F.FAIL_A
    r = A.run(frames, studies)
    reasons = " | ".join(r["refused"])
    check(len(r["refused"]) == 4, "FAIL fixture: all four built-to-fail studies refused (got %d)" % len(r["refused"]))
    check("before its frame was declared" in reasons, "coded-before-frame refused")
    check("disagrees with frame arm" in reasons, "wrong arm refused")
    check("never declared" in reasons, "undeclared frame refused")
    check("field E3 missing" in reasons, "missing field refused")
    check(r["arms"]["human"]["n_studies"] == 0, "nothing from the FAIL fixture enters a rate")
    FAIL_FIXTURES["enclosure_caveat_register"] = True


# ------------------------------------------------------------------ Build B ---
def t_coupling():
    res = B.run(F.CASES_B)
    held = dict(res["held"])
    check(held.get("undated") == "coupling instrument undated", "undated case HELD")
    check(held.get("dated-unsourced") == "coupling date stated without a source", "dated-unsourced case HELD")
    got = {r["population"]: r for r in res["entered"]}
    check(got["coincident"]["verdict"] == "CONFOUNDED_BEYOND_READ", "coincident confound reads CONFOUNDED_BEYOND_READ")
    check(got["visible"]["verdict"] == "VISIBLE", "declared visible shift with a distant confound reads VISIBLE")
    check(got["not-visible"]["verdict"] == "NOT_VISIBLE", "declared not-visible reads NOT_VISIBLE")
    check(got["none-declared"]["confounds_flag"] == "NONE_DECLARED", "empty confound list flagged NONE_DECLARED")
    check(got["missing-after"]["verdict"] == "NOT_EVALUABLE"
          and got["missing-after"]["would_read_if_filled"] == "VISIBLE", "missing after-record reads NOT_EVALUABLE first")
    check(all(r["control"].startswith("CONTROL: ") for r in res["entered"]), "every pre-coupling record labelled CONTROL")
    check(res["shared_dates"].get(("permit", 1990)) is not None
          and len(res["shared_dates"][("permit", 1990)]) == 6, "six entered cases share one treatment date")
    check(set(B.VERDICTS) >= {r["verdict"] for r in res["entered"]}, "verdicts drawn from the declared set")

    # FAIL fixture: no confound column, unnamed 'other', reading without basis.
    res = B.run(F.FAIL_B)
    check(len(res["rejected"]) == 3 and not res["entered"] and not res["held"], "FAIL fixture: three cases rejected")
    check(any("CONFOUNDS column missing" in r for r in res["rejected"]), "missing CONFOUNDS column rejected")
    check(any("must be named" in r for r in res["rejected"]), "unnamed 'other' confound rejected")
    check(any("basis" in r for r in res["rejected"]), "shift reading without a basis rejected")
    FAIL_FIXTURES["coupling_gradient"] = True

    # The seed run (EXPECTED E15.5 - E15.7, scored in CLAIM_TABLE).
    seed = B.run(B.SEEDS)
    check(len(seed["entered"]) == 1 and len(seed["held"]) == 4 and not seed["rejected"], "seeds: 1 entered, 4 held")
    check(all(why == "coupling instrument undated" for _, why in seed["held"]), "every held seed is held for an undated instrument")
    e = seed["entered"][0]
    check(e["verdict"] == "NOT_EVALUABLE" and e["would_read_if_filled"] == "CONFOUNDED_BEYOND_READ",
          "entered seed: NOT_EVALUABLE now, CONFOUNDED_BEYOND_READ if filled")
    check(B.SURVIVOR_LINE in render_of(B), "survivor filter printed in the render")


# ------------------------------------------------------------------ hygiene ---
CONVENTION = {"render", "main"}


def t_hygiene():
    lag = defined_names(os.path.join(HERE, "lag_count.py"))
    qs = defined_names(os.path.join(HERE, "question_space.py"))
    check(CONVENTION <= (lag | qs), "the exempted names are exactly ones FWO-11/FWO-9 also define")
    check(len(lag | qs) > len(CONVENTION), "the scope check still compares against more than the exemption")
    for m in (A, B):
        # render/main are the folder's CLI convention, shared by every module; the
        # first run fired on them and the narrowing is recorded as RIN_155.
        own = defined_names(os.path.join(HERE, m.__name__ + ".py")) - CONVENTION
        check(not (own & (lag | qs)), "%s rebuilds no FWO-11 / FWO-9 name (%s)" % (m.__name__, sorted(own & (lag | qs))))
        check("RECONSTRUCTED" in (m.__doc__ or ""), "%s docstring declares RECONSTRUCTED" % m.__name__)
        check("No political position is advanced" in (m.__doc__ or ""), "%s docstring carries the TERMS line" % m.__name__)
        r = render_of(m)
        check(r == render_of(m), "%s render deterministic" % m.__name__)
        check("RECONSTRUCTED" in r and "TERMS:" in r, "%s render states RECONSTRUCTED and TERMS" % m.__name__)
        p = subprocess.run([sys.executable, os.path.join(HERE, m.__name__ + ".py"), "--selftest"], capture_output=True)
        check(p.returncode == 2, "%s refuses --selftest with exit 2" % m.__name__)
        p = subprocess.run([sys.executable, os.path.join(HERE, m.__name__ + ".py")], capture_output=True)
        check(p.returncode == 0, "%s runs with exit 0" % m.__name__)
        p = subprocess.run([sys.executable, os.path.join(HERE, m.__name__ + ".py"), "--choices"], capture_output=True, text=True)
        check(p.returncode == 0 and p.stdout.count("[CHOICE") == len(m.CHOICES), "%s prints every CHOICE" % m.__name__)
        src = open(os.path.join(HERE, m.__name__ + ".py"), "rb").read()
        check(all(b < 128 for b in src), "%s is ASCII" % m.__name__)
        ast.parse(src.decode("ascii"), feature_version=(3, 8))
        check(True, "%s parses under 3.8" % m.__name__)
        for k in m.CHOICES:
            check(src.decode("ascii").count("[CHOICE %d]" % k) >= 1, "%s cites CHOICE %d inline" % (m.__name__, k))

    spec_path = os.path.join(HERE, "..", "sheet-structure-scan", "no_severity.py")
    if os.path.exists(spec_path):
        spec = importlib.util.spec_from_file_location("no_severity", spec_path)
        ns = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ns)
        for m in (A, B):
            ok, h = ns.check(render_of(m))
            check(ok, "%s render screens clean (%s)" % (m.__name__, [x[1] for x in h][:5]))
        check(not ns.check(render_of(A) + "\nthis cell is wrong\n")[0], "a planted word is caught by the screen")

    for m in (A, B):
        sample = os.path.join(HERE, "samples", m.__name__ + ".sample.txt")
        check(os.path.exists(sample) and open(sample, encoding="utf-8").read() == render_of(m),
              "%s sample matches a fresh render" % m.__name__)

    # EXPECTED precedes every module in history (key-holder rule 1).
    try:
        def first_add(path):
            out = subprocess.run(["git", "-C", HERE, "log", "--diff-filter=A", "--format=%H", "--", path],
                                 capture_output=True, text=True).stdout.split()
            return out[-1] if out else None
        exp = first_add("EXPECTED_FWO-15.md")
        if exp:
            files = subprocess.run(["git", "-C", HERE, "show", "--name-only", "--format=", exp],
                                   capture_output=True, text=True).stdout.split()
            check(not any(f.endswith(".py") for f in files), "the EXPECTED commit carries no module")
            for mod in ("enclosure_caveat_register.py", "coupling_gradient.py"):
                m = first_add(mod)
                if m:
                    anc = subprocess.run(["git", "-C", HERE, "merge-base", "--is-ancestor", exp, m]).returncode
                    check(anc == 0 and m != exp, "EXPECTED commit precedes %s" % mod)
    except OSError:
        pass


for fn in (t_register, t_coupling, t_hygiene):
    fn()

missing = [k for k in ("enclosure_caveat_register", "coupling_gradient") if not FAIL_FIXTURES.get(k)]
tag = "" if not missing else "  NO_FAIL_FIXTURE: %s" % ",".join(missing)
print("fwo-15: %d checks, %d failed; fail fixtures present on %d of 2 instruments; REGRESSION, not validation%s"
      % (_checks, _failed, 2 - len(missing), tag))
sys.exit(1 if _failed else 0)
