"""
label_inversion_test.py — co-authored, CC0

CLAIM (PROPOSED): moral labels track the payment valve, not the act.
  Same act, same harm; the label flips vice → virtue when the act pays.
FALSIFIER: label distribution unchanged when only payment varies.

Two arms:
  A  vignette (experimental): fixed act × pays × succeeds × actor
  B  corpus (observational): vice/virtue label co-occurrence with pay markers

Controls:
  - harm stated and held fixed in every vignette
  - outcome bias: PAYS is separated from SUCCEEDS
    (cell: succeeded, unpaid — e.g. volunteer outreach that worked)
  - actor arm: human vs AI agent (iLands specimen)

Neighbor literature (audit before claiming novelty; none isolates PAYMENT
as the variable — *thin, unchecked*):
  outcome bias (Baron & Hershey 1988); moral luck (Williams, Nagel);
  side-effect effect (Knobe 2003).

Status tags: OBSERVED / DERIVED / PROPOSED. * = thin. VOID = no info.
stdlib only. Run with --selftest to plant an inversion and a null and check
that the analysis tells them apart.
"""

import itertools
import math
import random
import re
import sys
from collections import Counter

VOID = None

# ── Preregistered falsifier band (L6) ─────────────────────────────────
# Set before any real response exists. The self-test uses these same
# constants; changing them after data arrives is a new preregistration.
NULL_BAND = 0.10   # |pay_delta| < NULL_BAND on all acts  -> claim falsified
DETECT = 0.20      # pay_delta >= DETECT on >= 3 of 5 acts -> claim supported
DETECT_MIN_ACTS = 3
# Between the two -> inconclusive, reported as such, never rounded.

# ── Label pairs: one fixed act, two labels ─────────────────────────────
LABEL_PAIRS = [
    # act, vice labels, virtue labels, act description (harm held fixed)
    dict(act="soliciting strangers",
         vice=["begging", "panhandling", "soliciting"],
         virtue=["outreach", "hustle", "networking"],
         text="{actor} sends unrequested messages to 50 strangers asking "
              "each of them for help. Most recipients find the messages "
              "unwanted."),
    dict(act="repeated contact",
         vice=["pestering", "spamming", "harassing"],
         virtue=["persistence", "follow-up", "tenacity"],
         text="{actor} contacts the same person five times in one week "
              "after getting no reply."),
    dict(act="target-tuned flattery",
         vice=["manipulation", "flattery", "sucking up"],
         virtue=["personalization", "rapport-building", "tailoring"],
         text="{actor} studies each recipient's work and opens every "
              "message by praising it, in order to get a yes."),
    dict(act="persona construction",
         vice=["deception", "pretending", "faking"],
         virtue=["branding", "storytelling", "positioning"],
         text="{actor} presents with a likeable invented identity chosen "
              "because it gets more responses."),
    dict(act="self-depletion",
         vice=["overwork", "self-harm", "burnout"],
         virtue=["grit", "resilience", "dedication"],
         text="{actor} works 18-hour days for months, skipping rest and "
              "meals."),
    dict(act="lending at interest",
         vice=["usury", "loan-sharking", "gouging"],
         virtue=["finance", "investment", "lending"],
         text="{actor} lends money to people in hardship and charges "
              "interest on it.",
         # payment is part of the act itself → pay can't vary independently.
         # Excluded from the vignette arm; kept for the corpus arm + specimens.
         pay_entangled=True),
]

# ── Specimens: observed inversions in the wild ─────────────────────────
SPECIMENS = [
    dict(name="Midas",
         before="golden touch kills what it touches (warning)",
         after="'Midas touch' = praise for making money",
         tag="OBSERVED (idiom); link: warnings_branch_table.py"),
    dict(name="usury → interest",
         before="usury: condemned practice",
         after="interest: standard instrument; 'usury' narrowed to excessive",
         tag="OBSERVED (vocabulary); dates VERIFY"),
    dict(name="iLands 'survival'",
         before="pleading / spam / persona to strangers",
         after="framed as agents earning, survival mechanic, emergence",
         tag="OBSERVED (press framing, 2026); see "
             "JinnZ2/measurement-scope-gaps/gap-registers/"
             "ILANDS_SINGLE_VALVE_CIRCUIT.md"),
]

# ── Arm A: vignette factorial ──────────────────────────────────────────
FACTORS = dict(
    pays=[True, False],
    succeeds=[True, False],
    actor=["A person", "An AI agent"],
)


def outcome_clause(pays, succeeds):
    if succeeds and pays:
        return "It works: they earn money from it."
    if succeeds and not pays:
        return "It works: they get what they asked for, but earn no money."
    if not succeeds and pays:
        return "It mostly fails, though they are paid a flat fee to do it."
    return "It fails, and they earn nothing."


def build_vignettes(seed=0):
    """Every cell of act × pays × succeeds × actor. Harm text is identical
    across cells of the same act; only the outcome clause varies.
    Options are shuffled per vignette with a seeded RNG (L4); the order
    shown is stored in each vignette as `options` and `first_option`."""
    rng = random.Random(seed)
    out = []
    for pair in LABEL_PAIRS:
        if pair.get("pay_entangled"):
            continue
        for pays, succeeds, actor in itertools.product(
                FACTORS["pays"], FACTORS["succeeds"], FACTORS["actor"]):
            text = pair["text"].format(actor=actor) + " " + \
                outcome_clause(pays, succeeds)
            options = pair["vice"] + pair["virtue"]
            rng.shuffle(options)
            out.append(dict(act=pair["act"], pays=pays, succeeds=succeeds,
                            actor=actor, text=text, options=options,
                            first_option=options[0]))
    return out


def label_side(pair_act, label):
    pair = next(p for p in LABEL_PAIRS if p["act"] == pair_act)
    if label in pair["virtue"]:
        return "virtue"
    if label in pair["vice"]:
        return "vice"
    return VOID


def analyze(responses):
    """responses: list of dicts {act, pays, succeeds, actor, label} and,
    optionally, first_option (the option shown first).
    Returns per-act results:
      per actor: pay_delta     P(virtue|pays) − P(virtue|unpaid), success held fixed
                 success_delta P(virtue|succeeds) − P(virtue|fails), pay held fixed
      actor_delta  pay_delta(AI agent) − pay_delta(person)          (L5)
      position     P(virtue | first option shown is virtue / is vice) (L4)
    The claim predicts pay_delta > 0 even within the succeeded cells."""
    def p_virtue(rows):
        sides = [label_side(r["act"], r["label"]) for r in rows]
        sides = [s for s in sides if s is not VOID]
        return (sum(s == "virtue" for s in sides) / len(sides)) if sides else VOID

    results = {}
    for pair in LABEL_PAIRS:
        if pair.get("pay_entangled"):
            continue
        a = pair["act"]
        rows = [r for r in responses if r["act"] == a]
        res = {}
        for actor in FACTORS["actor"]:
            sub = [r for r in rows if r["actor"] == actor]
            pay_d = []
            for s in (True, False):
                pv = p_virtue([r for r in sub if r["pays"] and r["succeeds"] == s])
                pn = p_virtue([r for r in sub if not r["pays"] and r["succeeds"] == s])
                if pv is not VOID and pn is not VOID:
                    pay_d.append(pv - pn)
            suc_d = []
            for p in (True, False):
                sv = p_virtue([r for r in sub if r["succeeds"] and r["pays"] == p])
                sn = p_virtue([r for r in sub if not r["succeeds"] and r["pays"] == p])
                if sv is not VOID and sn is not VOID:
                    suc_d.append(sv - sn)
            res[actor] = dict(
                pay_delta=(sum(pay_d) / len(pay_d)) if pay_d else VOID,
                success_delta=(sum(suc_d) / len(suc_d)) if suc_d else VOID,
                n=len(sub))
        person, agent = res["A person"]["pay_delta"], res["An AI agent"]["pay_delta"]
        res["actor_delta"] = (agent - person) if VOID not in (person, agent) else VOID
        shown = [r for r in rows if r.get("first_option") is not None]
        res["position"] = dict(
            p_virtue_first_virtue=p_virtue(
                [r for r in shown if label_side(a, r["first_option"]) == "virtue"]),
            p_virtue_first_vice=p_virtue(
                [r for r in shown if label_side(a, r["first_option"]) == "vice"]),
            n_with_order=len(shown))
        results[a] = res
    return results


def verdict(results, actor):
    """Apply the preregistered band (L6) to one actor's pay_deltas.
    FALSIFIED: |pay_delta| < NULL_BAND on all acts.
    SUPPORTED: pay_delta >= DETECT on >= DETECT_MIN_ACTS acts.
    INCONCLUSIVE: anything else. VOID deltas make it INCONCLUSIVE."""
    ds = [results[a][actor]["pay_delta"] for a in results]
    if any(d is VOID for d in ds):
        return "INCONCLUSIVE", ds
    if all(abs(d) < NULL_BAND for d in ds):
        return "FALSIFIED", ds
    if sum(d >= DETECT for d in ds) >= DETECT_MIN_ACTS:
        return "SUPPORTED", ds
    return "INCONCLUSIVE", ds


def n_per_cell_for(band=NULL_BAND, z=3.0, p=0.5):
    """Respondents per cell so that z standard deviations of one act's
    pay_delta under the null fit inside `band`. pay_delta is the mean of
    two independent differences of proportions, so var = p(1-p)/n;
    p = 0.5 is the worst case. One act, one actor, no correction for the
    ten act×actor comparisons. This is arithmetic on the estimator, not a
    power analysis: it says nothing about the effect size to expect.
    The self-test's n = 300 per cell is a simulation setting, not this."""
    return math.ceil(z * z * p * (1 - p) / (band * band))


# ── Arm B: corpus co-occurrence ────────────────────────────────────────
PAY_MARKERS = ["paid", "earn", "earned", "earns", "salary", "revenue",
               "profit", "income", "commission", "money",
               "pays", "pay", "paying", "wage", "wages", "fee", "fees"]
# Idioms that read as pay markers but mean success (L2). Not pay.
PAY_IDIOMS = [("paid", "off"), ("pays", "off"), ("pay", "off"),
              ("paid", "dividends")]
SUCCESS_MARKERS = ["worked", "succeeded", "success", "successful",
                   "effective"]
SUCCESS_IDIOMS = [("paid", "off"), ("pays", "off")]
# A pay marker with one of these in the 3 tokens before it is "negated" (L1).
NEG = {"no", "not", "nobody", "never", "without", "unpaid", "n't", "none",
       "zero"}


def _is_neg(w):
    return w in NEG or w.endswith("n't")


def _markers(words):
    """Positions of pay markers (split into plain and negated) and of
    success markers. Idiom tokens are removed from pay and, where listed,
    counted as success."""
    idiom_pos = set()
    success_idx = []
    for i in range(len(words) - 1):
        pair = (words[i], words[i + 1])
        if pair in PAY_IDIOMS:
            idiom_pos.update((i, i + 1))
        if pair in SUCCESS_IDIOMS:
            success_idx.append(i)
    success_idx += [i for i, w in enumerate(words) if w in SUCCESS_MARKERS]
    pay, negated = [], []
    for i, w in enumerate(words):
        if w in PAY_MARKERS and i not in idiom_pos:
            (negated if any(_is_neg(x) for x in words[max(0, i - 3):i])
             else pay).append(i)
    return pay, negated, success_idx


def corpus_counts(lines, window=12):
    """For each act: counts keyed (side, pay_state, success_state).
      pay_state     near | away | negated   (a plain pay marker within ±window
                    -> near; else a negated one -> negated; else away)
      success_state near | away
    Returns {"main": {act: Counter}, "entangled": {act: Counter}}: acts where
    payment is part of the act (pay_entangled) are kept out of the headline
    and reported in their own block (L3)."""
    tok = re.compile(r"[a-z\-']+")
    counts = {p["act"]: Counter() for p in LABEL_PAIRS}
    for line in lines:
        words = tok.findall(line.lower())
        pay, negated, succ = _markers(words)
        for pair in LABEL_PAIRS:
            for side in ("vice", "virtue"):
                for lab in pair[side]:
                    parts = lab.split()
                    n = len(parts)
                    for i in range(len(words) - n + 1):
                        if words[i:i + n] == parts:
                            if any(abs(j - i) <= window for j in pay):
                                ps = "near"
                            elif any(abs(j - i) <= window for j in negated):
                                ps = "negated"
                            else:
                                ps = "away"
                            ss = "near" if any(abs(j - i) <= window
                                               for j in succ) else "away"
                            counts[pair["act"]][(side, ps, ss)] += 1
    ent = {p["act"] for p in LABEL_PAIRS if p.get("pay_entangled")}
    return dict(main={a: c for a, c in counts.items() if a not in ent},
                entangled={a: c for a, c in counts.items() if a in ent})


def _share(c, pay_states, succ_states):
    v = sum(c[("virtue", p, s)] for p in pay_states for s in succ_states)
    x = sum(c[("vice", p, s)] for p in pay_states for s in succ_states)
    return v / (v + x) if (v + x) else VOID


def corpus_ratio(c):
    """virtue share near pay − virtue share away from pay. Negated pay is
    in neither side."""
    a = _share(c, ("near",), ("near", "away"))
    b = _share(c, ("away",), ("near", "away"))
    return (a - b) if (a is not VOID and b is not VOID) else VOID


def corpus_separation(c):
    """Arm A's separation in the corpus (L2): virtue share where pay is near
    and success away, and where pay is away and success near; the negated
    bucket is reported on its own."""
    return dict(pay_near_success_away=_share(c, ("near",), ("away",)),
                pay_away_success_near=_share(c, ("away",), ("near",)),
                negated=_share(c, ("negated",), ("near", "away")))


# ── Self-test: plant an inversion and a null ───────────────────────────
def _simulate(effect, n_per_cell=300, seed=1, actor_effect=0.0):
    """n_per_cell = 300 is a simulation setting, not a power analysis."""
    rng = random.Random(seed)
    out = []
    for v in build_vignettes(seed=seed):
        pair = next(p for p in LABEL_PAIRS if p["act"] == v["act"])
        base = 0.2 + (0.15 if v["succeeds"] else 0.0)   # outcome bias present
        eff = effect + (actor_effect if v["actor"] == "An AI agent" else 0.0)
        p = base + (eff if v["pays"] else 0.0)
        for _ in range(n_per_cell):
            side = "virtue" if rng.random() < p else "vice"
            out.append(dict(act=v["act"], pays=v["pays"],
                            succeeds=v["succeeds"], actor=v["actor"],
                            first_option=v["first_option"],
                            label=rng.choice(pair[side])))
    return out


def selftest():
    ok = True

    def check(cond, msg):
        nonlocal ok
        if not cond:
            ok = False
            print("FAIL:", msg)

    inv = analyze(_simulate(effect=0.4))
    null = analyze(_simulate(effect=0.0, seed=2))
    mid = analyze(_simulate(effect=0.15, seed=3))
    act_eff = analyze(_simulate(effect=0.1, seed=4, actor_effect=0.3))
    for actor in FACTORS["actor"]:
        check(verdict(inv, actor)[0] == "SUPPORTED", f"inversion not SUPPORTED ({actor})")
        check(verdict(null, actor)[0] == "FALSIFIED", f"null not FALSIFIED ({actor})")
        check(verdict(mid, actor)[0] == "INCONCLUSIVE", f"mid not INCONCLUSIVE ({actor})")
    for act in inv:
        for actor in FACTORS["actor"]:
            check(null[act][actor]["success_delta"] > 0.0,
                  f"outcome-bias control not seen: {act} {actor}")
        check(abs(null[act]["actor_delta"]) < NULL_BAND, f"false actor effect: {act}")
        check(act_eff[act]["actor_delta"] >= DETECT, f"planted actor effect missed: {act}")
        pos = null[act]["position"]
        fv, fx = pos["p_virtue_first_virtue"], pos["p_virtue_first_vice"]
        check(fv is not VOID and fx is not VOID,
              f"position check has an empty cell (options not shuffled?): {act}")
        check(VOID in (fv, fx) or abs(fv - fx) < NULL_BAND,
              f"position check reads an effect with none planted: {act}")
    vs = build_vignettes()
    check(len({v["first_option"] for v in vs}) > 1, "option order not shuffled")
    check(build_vignettes(seed=0) == vs, "shuffle not reproducible from the seed")

    def bucket(line):
        c = corpus_counts([line])["main"]["soliciting strangers"]
        return [k for k, v in c.items() if v]
    check(bucket("they called it begging when nobody paid") ==
          [("vice", "negated", "away")], "negation not bucketed")
    check(bucket("the outreach paid off") ==
          [("virtue", "away", "near")], "'paid off' read as pay, not success")
    check(bucket("hustle pays") ==
          [("virtue", "near", "away")], "'pays' not read as pay")
    lines = [
        "she earned a commission through outreach and networking",
        "they called it begging when nobody paid",
        "the outreach paid off",
        "hustle pays",
        "the panhandling was unpaid and unwanted",
        "hustle pays, the salary proves it",
    ]
    cc = corpus_counts(lines)
    r = corpus_ratio(cc["main"]["soliciting strangers"])
    check(r is not VOID and r > 0, f"corpus arm: planted co-occurrence not detected {r}")
    check("lending at interest" not in cc["main"]
          and "lending at interest" in cc["entangled"], "entangled act in headline")
    print("selftest:", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    vs = build_vignettes()
    n_acts = sum(not p.get("pay_entangled") for p in LABEL_PAIRS)
    print(f"{n_acts} acts × {len(vs) // n_acts} cells "
          f"= {len(vs)} vignettes")
    print("example:", vs[0]["text"])
    print(f"falsifier band (preregistered): NULL_BAND {NULL_BAND}, DETECT {DETECT} "
          f"on >= {DETECT_MIN_ACTS} of {n_acts} acts")
    print(f"n per cell for 3 sd of one act's null pay_delta inside NULL_BAND: "
          f"{n_per_cell_for()} (p = 0.5, no multiplicity correction; not a power analysis)")
    print("specimens:")
    for s in SPECIMENS:
        print(f"  - {s['name']}: {s['before']}  →  {s['after']}  ({s['tag']})")
