# SPDX-License-Identifier: CC0-1.0
"""
Checks for sense_as_match.py. Plain script, no pytest, no network.

    python3 sense-as-match/test_sense.py

Every path the work order names is covered, in the order it names them:
known -> KNOWN; definite novel -> NEW; plastic -> UNCOALESCED (not forced);
uncoalesced + evidence -> collapses; NEGATIVE: uncoalesced never returns
KNOWN by nearest neighbour; same shape via two channels -> same state.
Expected verdicts live HERE. Exits 1 on any failure.

The module is loaded by file path under its own name: the repo root carries
a different file called sense_as_match.py, and an import by bare name would
read whichever directory came first on sys.path (frame-instruments FI_001).
"""

from __future__ import annotations

import ast
import importlib.util
import math
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "sense_as_match.py")
_spec = importlib.util.spec_from_file_location("sense_as_match_folder", PATH)
sam = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = sam      # dataclasses resolve annotations here
_spec.loader.exec_module(sam)

FAILED = []
TOTAL = [0]


def check(name, condition, detail=""):
    TOTAL[0] += 1
    print("%-6s %s%s" % ("ok" if condition else "FAIL", name,
                         "" if condition else "   <- %s" % (detail,)))
    if not condition:
        FAILED.append(name)


# ---------------------------------------------------------------- patterns
# Every pattern below is CONSTRUCTED. Nothing is a reading from a sensor.

def sine(n, period=31.4, offset=0.0, gain=1.0, phase=0.0):
    return [offset + gain * math.sin(2 * math.pi * i / period + phase)
            for i in range(n)]


def ramp(n, offset=0.0, gain=1.0):
    return [offset + gain * i for i in range(n)]


def square(n, period=20, offset=0.0, gain=1.0):
    return [offset + gain * (1.0 if (i // (period // 2)) % 2 == 0 else -1.0)
            for i in range(n)]


def mix(a, b, w):
    """(1-w)*a + w*b, sample by sample; both already the same length."""
    return [(1 - w) * x + w * y for x, y in zip(a, b)]


def held_set(params=None):
    ks = sam.KnownSet(params)
    ks.add(sine(60), name="SINE")
    ks.add(ramp(40), name="RAMP")
    return ks


def split_set(params=None):
    """SINE and LAG (the same sine 0.9 rad later) are 0.847 apart, so a
    pattern halfway between them sits inside both radii."""
    ks = held_set(params)
    ks.add(sine(60, phase=0.9), name="LAG")
    return ks


def inc(obs, **channel):
    return sam.Incoming(list(obs), dict(channel))


# ------------------------------------------------------- reduction / distance
print("== the reduction takes out offset, gain and sampling, and keeps sign ==")

base = sine(60)
moved = sine(240, period=31.4 * 4, offset=500.0, gain=37.0)   # same form
# Not 0: linear resampling to LENGTH 32 interpolates differently from 60
# and from 240 points. Measured 0.082 (r = 0.9967); the bound is 0.1.
check("offset + gain + 4x sampling leave distance < 0.1 (resampling residue)",
      sam.shape_distance(base, moved) < 0.1,
      sam.shape_distance(base, moved))
check("a mirror image is distance 2 (r = -1)  [GAP 3]",
      abs(sam.shape_distance(base, [-x for x in base]) - 2.0) < 1e-9,
      sam.shape_distance(base, [-x for x in base]))
check("identical shapes are distance 0",
      sam.shape_distance(base, base) == 0.0)
rr = sam.reduce_shape(base)
check("a reduced shape has mean 0 and population sd 1",
      abs(sum(rr) / len(rr)) < 1e-12
      and abs(math.sqrt(sum(x * x for x in rr) / len(rr)) - 1) < 1e-12)
check("a flat pattern does not reduce: None, never a zero shape  [GAP 1]",
      sam.reduce_shape([5.0] * 30) is None)
check("one reading does not reduce", sam.reduce_shape([1.0]) is None)
check("a non-finite reading does not reduce",
      sam.reduce_shape([1.0, float("nan"), 2.0]) is None)
check("booleans are refused as readings",
      sam.reduce_shape([True, False, True, False]) is None)
check("distance to an unreducible pattern is None",
      sam.shape_distance(base, [3.0] * 10) is None)
check("spread of one shape is None, never 0  [CHOICE 7]",
      sam.spread([rr]) is None)
check("RADIUS 0.5 corresponds to r = 0.875  [CHOICE 2]",
      abs(math.sqrt(2 * (1 - 0.875)) - 0.5) < 1e-12)


# --------------------------------------------------------------- KNOWN
print("== known -> KNOWN ==")

ks = held_set()
r = sam.match(inc([sine(100, period=52.3, offset=3, gain=10),
                   sine(80, period=41.9, offset=-2, gain=0.4),
                   sine(60)], sensor="A"), ks)
check("three sine observations return KNOWN", r["state"] == sam.KNOWN, r)
check("... and name the held shape", r["shape"] == "SINE", r["shape"])
check("... with no `between`", r["between"] is None)
check("... and no pending field", r["pending"] is None)
check("... and field share 1.0 on SINE", r["field"] == {"SINE": 1.0},
      r["field"])
check("a KNOWN match registers nothing", sorted(ks.shapes) == ["RAMP", "SINE"])


# --------------------------------------------------------------- NEW
print("== definite novel -> NEW ==")

ks = held_set()
r = sam.match(inc([square(80), square(160, period=40, offset=9, gain=3)],
                  sensor="B"), ks)
check("two square waves return NEW", r["state"] == sam.NEW, r)
check("... registered under a fresh name",
      r["shape"] in ks.shapes and r["shape"] not in ("SINE", "RAMP"),
      r["shape"])
check("... the held set grew by exactly one", len(ks.shapes) == 3)
check("... and the registered shape is the square",
      sam.distance(ks.shapes[r["shape"]],
                   sam.reduce_shape(square(80), ks.params.length)) < 0.05)
r2 = sam.match(inc([square(120, period=30), square(40, period=10)]), ks)
check("the same square arriving again now returns KNOWN on the new name",
      r2["state"] == sam.KNOWN and r2["shape"] == r["shape"], r2)


# --------------------------------------------------------------- UNCOALESCED
print("== plastic -> UNCOALESCED (not forced) ==")

# Halfway between SINE and LAG, so inside both radii.
mid = sine(60, phase=0.45)
ks = split_set()
d_s = sam.distance(sam.reduce_shape(mid), ks.shapes["SINE"])
d_l = sam.distance(sam.reduce_shape(mid), ks.shapes["LAG"])
r = sam.match(inc([mid, mid]), ks)
check("a pattern inside both radii is split, not given to the nearer "
      "(d_sine %.4f, d_lag %.4f)" % (d_s, d_l),
      r["state"] == sam.UNCOALESCED, r)
check("... shape is None: the nearest is not reported  [CHOICE 8]",
      r["shape"] is None)
check("... between names both candidates",
      set(r["between"] or []) == {"SINE", "LAG"}, r["between"])
check("... with the field split 0.5 / 0.5  [CHOICE 3]",
      r["field"] == {"SINE": 0.5, "LAG": 0.5}, r["field"])
check("... and carries a pending field to update",
      r["pending"] is not None)
check("... and registers nothing", len(ks.shapes) == 3)

# Novel but not definite: two different novel shapes.
ks = held_set()
r = sam.match(inc([square(80), sine(60, period=8.0)]), ks)
check("two different novel patterns are UNCOALESCED, not NEW",
      r["state"] == sam.UNCOALESCED, r)
check("... reason names definiteness", "not definite" in r["reason"],
      r["reason"])
check("... and nothing is registered", len(ks.shapes) == 2)

# MIN_OBS: one observation of a held shape.
ks = held_set()
r = sam.match(inc([sine(60)]), ks)
check("one observation of a held shape is UNCOALESCED under MIN_OBS 2 "
      "[CHOICE 6]", r["state"] == sam.UNCOALESCED, r)
check("... with the whole field on SINE, still not collapsed",
      r["field"] == {"SINE": 1.0} and r["shape"] is None)

ks1 = held_set(sam.Params(min_obs=1))
r = sam.match(inc([sine(60)]), ks1)
check("MIN_OBS 1 lets one observation of a held shape be KNOWN",
      r["state"] == sam.KNOWN and r["shape"] == "SINE", r)
r = sam.match(inc([square(80)]), ks1)
check("MIN_OBS 1 still cannot make NEW from one observation (no spread)",
      r["state"] == sam.UNCOALESCED and "not definite" in r["reason"], r)

# GAP 1: flat observations are counted and excluded.
ks = held_set()
r = sam.match(inc([[4.0] * 30, [4.0] * 30]), ks)
check("only flat observations: UNCOALESCED, reason 'no reducible'",
      r["state"] == sam.UNCOALESCED and "no reducible" in r["reason"], r)
check("... n_unreducible 2, n_obs 0", r["n_unreducible"] == 2
      and r["n_obs"] == 0)
r = sam.match(inc([[4.0] * 30, sine(60), sine(90, period=47.1)]), ks)
check("a flat observation beside two sines is excluded, not counted against",
      r["state"] == sam.KNOWN and r["n_unreducible"] == 1, r)
try:
    ks.add([1.0] * 20)
    check("a flat pattern cannot be held", False, "added")
except ValueError:
    check("a flat pattern cannot be held", True)


# --------------------------------------------------------------- collapse
print("== uncoalesced + evidence -> collapses ==")

# (a) one observation, MIN_OBS 2 -> evidence on the same held shape -> KNOWN
ks = held_set()
r0 = sam.match(inc([sine(60)], sensor="A"), ks)
r1 = sam.update(r0, [sine(70, period=36.6)], ks, channel={"sensor": "C"})
check("UNCOALESCED (MIN_OBS) + one more sine collapses to KNOWN",
      r0["state"] == sam.UNCOALESCED and r1["state"] == sam.KNOWN
      and r1["shape"] == "SINE", (r0["state"], r1))

# (b) the field crosses COLLAPSE by accumulation
ks = held_set()
far = square(80)
r0 = sam.match(inc([sine(60), far]), ks)
check("one sine + one novel: field 0.5 / 0.5, UNCOALESCED",
      r0["state"] == sam.UNCOALESCED
      and r0["field"] == {"SINE": 0.5, "NEW": 0.5}, r0["field"])
r1 = sam.update(r0, [sine(60)], ks)
check("+1 sine: share 0.667 < 0.8, still UNCOALESCED (field updated)",
      r1["state"] == sam.UNCOALESCED
      and abs(r1["field"]["SINE"] - 2 / 3) < 1e-12, r1["field"])
r2 = sam.update(r1, [sine(60), sine(60)], ks)
check("+2 more: share 0.8 >= COLLAPSE, KNOWN", r2["state"] == sam.KNOWN
      and r2["shape"] == "SINE" and abs(r2["field"]["SINE"] - 0.8) < 1e-12,
      r2)

# (c) novel-not-definite + agreeing evidence -> NEW
ks = held_set()
r0 = sam.match(inc([square(80)]), ks)
r1 = sam.update(r0, [square(120, period=30)], ks)
check("one square (UNCOALESCED) + a second square collapses to NEW",
      r0["state"] == sam.UNCOALESCED and r1["state"] == sam.NEW, r1)
check("... and only then is a shape registered", len(ks.shapes) == 3)

# (d) channel enters the audit trail and nothing else
ks = held_set()
r0 = sam.match(inc([sine(60)], sensor="A"), ks)
r1 = sam.update(r0, [sine(60)], ks, channel={"sensor": "Z"})
check("the update's channel is appended to the audit trail",
      r1["audit"]["channel"]["trail"] == [{"sensor": "A"}, {"sensor": "Z"}],
      r1["audit"])
for bad in (r1,):
    try:
        sam.update(bad, [sine(60)], ks)
        check("update refuses a collapsed result", False, "no raise")
    except ValueError:
        check("update refuses a collapsed result", True)


# --------------------------------------------------------------- NEGATIVE
print("== NEGATIVE: uncoalesced never returns KNOWN by nearest neighbour ==")

# A pattern whose nearest held shape is SINE but which is outside RADIUS.
ks = held_set()
near_miss = None
for w in [i / 100.0 for i in range(1, 100)]:
    cand = mix(sine(60), square(60, period=31), w)
    d = {k: sam.distance(sam.reduce_shape(cand), h)
         for k, h in ks.shapes.items()}
    if min(d, key=d.get) == "SINE" and 0.5 < d["SINE"] < 0.7:
        near_miss = (w, cand, d)
        break
check("a near miss exists (nearest SINE, outside RADIUS)",
      near_miss is not None)
w, cand, d = near_miss
r = sam.match(inc([cand, mix(sine(60), square(60, period=29), w)]), ks)
check("near-miss observations (nearest SINE at %.3f) are not KNOWN SINE"
      % d["SINE"], not (r["state"] == sam.KNOWN), r)
check("... their weight sits on NEW, not on the nearest held shape",
      r["field"].get("SINE", 0.0) == 0.0 and "NEW" in r["field"], r["field"])

# The split case, accumulated: evidence that stays split never collapses.
ks = split_set()
r = sam.match(inc([mid, mid]), ks)
for k in range(6):
    r = sam.update(r, [mid], ks)
    if r["state"] != sam.UNCOALESCED:
        break
check("evidence that keeps splitting never collapses (8 observations)",
      r["state"] == sam.UNCOALESCED and r["shape"] is None, r["state"])

# Randomised sweep against a nearest-neighbour classifier. The negative is
# only worth something if nearest neighbour WOULD have answered in the
# cases this instrument holds open: count those, and require > 0.
rng = random.Random(20261005)
ks = held_set()
nn_would_answer = 0
violations = []
for trial in range(400):
    a = rng.uniform(0, 1)
    obs = []
    for _ in range(rng.randint(2, 4)):
        pat = mix(sine(60, phase=rng.uniform(-0.3, 0.3)),
                  [x / 30.0 for x in ramp(60)], a)
        pat = [x + rng.gauss(0, rng.uniform(0, 0.6)) for x in pat]
        obs.append(pat)
    shapes = [sam.reduce_shape(o, ks.params.length) for o in obs]
    shapes = [s for s in shapes if s is not None]
    nn = [min(ks.shapes, key=lambda k: sam.distance(s, ks.shapes[k]))
          for s in shapes]
    r = sam.match(inc(obs), ks)
    if r["state"] == sam.UNCOALESCED and len(set(nn)) == 1:
        nn_would_answer += 1
    if r["state"] == sam.KNOWN:
        within = sum(1 for s in shapes
                     if sam.distance(s, ks.shapes[r["shape"]])
                     <= ks.params.radius)
        if within / len(shapes) < ks.params.collapse:
            violations.append((trial, r["field"]))
    for name in list(ks.shapes):               # keep the held set fixed
        if name not in ("SINE", "RAMP"):
            del ks.shapes[name]
check("sweep: nearest neighbour would have answered in %d UNCOALESCED cases "
      "(the negative is not vacuous)" % nn_would_answer, nn_would_answer > 0)
check("sweep: every KNOWN has >= COLLAPSE of its observations inside RADIUS "
      "of the named shape (0 violations of 400)", violations == [],
      violations[:3])


# ------------------------------------------------------------ two channels
print("== same shape via two channels -> same state ==")


def run_both(obs_a, obs_b, ch_a, ch_b, make=None):
    make = make or held_set
    ka, kb = make(), make()
    return sam.match(inc(obs_a, **ch_a), ka), sam.match(inc(obs_b, **ch_b), kb)


ra, rb = run_both(
    [sine(60), sine(60, period=31.0)],
    [sine(400, period=31.4 * 400 / 60, offset=-80, gain=0.002),
     sine(400, period=31.0 * 400 / 60, offset=1e4, gain=5e3)],
    {"sensor": "accelerometer", "units": "m/s^2", "rate_hz": 60},
    {"sensor": "strain_gauge", "units": "ue", "rate_hz": 400,
     "calibrated": False})
check("KNOWN via two channels: same state, same shape",
      (ra["state"], ra["shape"]) == (rb["state"], rb["shape"]) == (sam.KNOWN,
                                                                   "SINE"),
      (ra["state"], ra["shape"], rb["state"], rb["shape"]))

ra, rb = run_both([square(80), square(160, period=40)],
                  [square(320, period=80, offset=2, gain=0.1),
                   square(640, period=160, offset=-7, gain=40)],
                  {"sensor": "A"}, {"sensor": "B", "inverted": "unknown"})
check("NEW via two channels: same state", ra["state"] == rb["state"]
      == sam.NEW, (ra["state"], rb["state"]))

ra, rb = run_both([mid, mid],
                  [[3 + 9 * x for x in mid], [3 + 9 * x for x in mid]],
                  {"sensor": "A"}, {"sensor": "B"}, make=split_set)
check("UNCOALESCED via two channels: same state, same between, same field",
      ra["state"] == rb["state"] == sam.UNCOALESCED
      and ra["between"] == rb["between"] and ra["field"] == rb["field"],
      (ra, rb))

# Same observations, any channel dict: identical result except audit.
ks_x, ks_y = split_set(), split_set()
obs = [sine(60), mid, square(80)]
rx = sam.match(inc(obs, sensor="X", trusted=True, weight=1e9), ks_x)
ry = sam.match(inc(obs, sensor="Y", trusted=False, nearest="RAMP"), ks_y)
strip = lambda d: {k: v for k, v in d.items() if k not in ("audit", "pending")}
check("identical observations under two channel dicts return identical "
      "results apart from audit", strip(rx) == strip(ry), (rx, ry))
check("... and the channel is carried in audit",
      rx["audit"]["channel"]["sensor"] == "X")

# Structural: the deciding functions never name the channel.
src = open(PATH).read()
tree = ast.parse(src)
DECIDERS = ("_field", "_novel", "_decide")
names_used = {}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in DECIDERS:
        used = set()
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name):
                used.add(sub.id)
            elif isinstance(sub, ast.Attribute):
                used.add(sub.attr)
            elif isinstance(sub, ast.arg):
                used.add(sub.arg)
            elif isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                used.add(sub.value)
        names_used[node.name] = used
check("all three deciding functions found in the AST",
      sorted(names_used) == sorted(DECIDERS), sorted(names_used))
FORBIDDEN = {"channel", "audit", "incoming", "Incoming", "pending", "trail"}
leaks = {k: sorted(v & FORBIDDEN) for k, v in names_used.items()
         if v & FORBIDDEN}
check("no deciding function names channel / audit / incoming / pending",
      leaks == {}, leaks)

# The AST scan fires on a plant, so its silence above means something.
plant = ast.parse("def _decide(shapes, held, params):\n"
                  "    return incoming.channel\n")
hits = set()
for sub in ast.walk(plant):
    if isinstance(sub, ast.Name):
        hits.add(sub.id)
    elif isinstance(sub, ast.Attribute):
        hits.add(sub.attr)
check("the AST scan fires on a planted channel read", hits & FORBIDDEN,
      hits)


# ------------------------------------------------------------- params / CLI
print("== params and CLI ==")

for kw, why in (({"collapse": 0.5}, "COLLAPSE 0.5 would let a tie collapse"),
                ({"collapse": 1.2}, "COLLAPSE above 1"),
                ({"radius": 0.0}, "RADIUS 0"),
                ({"min_obs": 0}, "MIN_OBS 0"),
                ({"spread": 0.0}, "SPREAD 0"),
                ({"length": 2}, "LENGTH 2")):
    try:
        sam.Params(**kw)
        check("Params refuses %s" % why, False, kw)
    except ValueError:
        check("Params refuses %s" % why, True)

ks = held_set()
for bad in ("NEW", "SINE"):
    try:
        ks.add(sine(60, period=9.0), name=bad)
        check("a held name %r is refused" % bad, False)
    except ValueError:
        check("a held name %r is refused" % bad, True)

p = subprocess.run([sys.executable, PATH, "--selftest"],
                   capture_output=True, text=True)
check("--selftest is refused (exit 2) and names test_sense.py",
      p.returncode == 2 and "test_sense.py" in p.stderr,
      (p.returncode, p.stderr))
p = subprocess.run([sys.executable, PATH, "--choices"],
                   capture_output=True, text=True)
check("--choices prints all %d choices" % len(sam.CHOICES),
      p.returncode == 0 and all("[CHOICE %d]" % k in p.stdout
                                for k in sam.CHOICES))
check("every [CHOICE n] is cited in the source outside CHOICES",
      all(src.count("[CHOICE %d]" % k) >= 1 for k in sam.CHOICES)
      and all(("[CHOICE %d]" % k) in src.split("CHOICES = {")[0]
              + src.split("# --------------------------------------------"
                          "------------------- match ----")[1]
              for k in (3, 4, 6, 7, 8)))
check("every [GAP n] declared in the docstring",
      all(("%d  " % k) in sam.__doc__ for k in (1, 2, 3, 4, 5)))
check("every [GAP n] that takes effect in code is cited where it does",
      all(("[GAP %d]" % k) in src.split('\"\"\"', 2)[2]
          for k in (1, 4, 5)))


print()
print("checks: %d   failed: %d" % (TOTAL[0], len(FAILED)))
if FAILED:
    for f in FAILED:
        print("  FAILED:", f)
    sys.exit(1)
