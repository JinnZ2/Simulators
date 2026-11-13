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
import random
import re
import sys
from collections import Counter

VOID = None

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


def build_vignettes():
    """Every cell of act × pays × succeeds × actor. Harm text is identical
    across cells of the same act; only the outcome clause varies."""
    out = []
    for pair in LABEL_PAIRS:
        if pair.get("pay_entangled"):
            continue
        for pays, succeeds, actor in itertools.product(
                FACTORS["pays"], FACTORS["succeeds"], FACTORS["actor"]):
            text = pair["text"].format(actor=actor) + " " + \
                outcome_clause(pays, succeeds)
            options = pair["vice"] + pair["virtue"]
            out.append(dict(act=pair["act"], pays=pays, succeeds=succeeds,
                            actor=actor, text=text, options=options))
    return out


def label_side(pair_act, label):
    pair = next(p for p in LABEL_PAIRS if p["act"] == pair_act)
    if label in pair["virtue"]:
        return "virtue"
    if label in pair["vice"]:
        return "vice"
    return VOID


def analyze(responses):
    """responses: list of dicts {act, pays, succeeds, actor, label}.
    Returns per-act deltas:
      pay_delta     P(virtue|pays) − P(virtue|unpaid), success held fixed
      success_delta P(virtue|succeeds) − P(virtue|fails), pay held fixed
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
        results[a] = res
    return results


# ── Arm B: corpus co-occurrence ────────────────────────────────────────
PAY_MARKERS = ["paid", "earn", "earned", "earns", "salary", "revenue",
               "profit", "income", "commission", "money"]


def corpus_counts(lines, window=12):
    """For each act: counts of vice/virtue labels with and without a pay
    marker within ±window tokens. Input: iterable of text lines."""
    tok = re.compile(r"[a-z\-']+")
    counts = {p["act"]: Counter() for p in LABEL_PAIRS}
    for line in lines:
        words = tok.findall(line.lower())
        pay_idx = [i for i, w in enumerate(words) if w in PAY_MARKERS]
        for pair in LABEL_PAIRS:
            for side in ("vice", "virtue"):
                for lab in pair[side]:
                    parts = lab.split()
                    n = len(parts)
                    for i in range(len(words) - n + 1):
                        if words[i:i + n] == parts:
                            near = any(abs(j - i) <= window for j in pay_idx)
                            counts[pair["act"]][(side, near)] += 1
    return counts


def corpus_ratio(c):
    """virtue share near pay − virtue share away from pay."""
    def share(near):
        v, x = c[("virtue", near)], c[("vice", near)]
        return v / (v + x) if (v + x) else VOID
    a, b = share(True), share(False)
    return (a - b) if (a is not VOID and b is not VOID) else VOID


# ── Self-test: plant an inversion and a null ───────────────────────────
def _simulate(effect, n_per_cell=300, seed=1):
    rng = random.Random(seed)
    out = []
    for v in build_vignettes():
        pair = next(p for p in LABEL_PAIRS if p["act"] == v["act"])
        base = 0.2 + (0.15 if v["succeeds"] else 0.0)   # outcome bias present
        p = base + (effect if v["pays"] else 0.0)
        for _ in range(n_per_cell):
            side = "virtue" if rng.random() < p else "vice"
            out.append(dict(act=v["act"], pays=v["pays"],
                            succeeds=v["succeeds"], actor=v["actor"],
                            label=rng.choice(pair[side])))
    return out


def selftest():
    ok = True
    inv = analyze(_simulate(effect=0.4))
    null = analyze(_simulate(effect=0.0, seed=2))
    for act in inv:
        for actor in FACTORS["actor"]:
            d_inv = inv[act][actor]["pay_delta"]
            d_null = null[act][actor]["pay_delta"]
            s_null = null[act][actor]["success_delta"]
            if not d_inv > 0.25:
                ok = False; print("MISS inversion:", act, actor, d_inv)
            if not abs(d_null) < 0.15:
                ok = False; print("FALSE inversion:", act, actor, d_null)
            if not s_null > 0.0:
                ok = False; print("outcome-bias control not seen:", act, actor)
    c = corpus_counts([
        "she earned a commission through outreach and networking",
        "they called it begging when nobody paid",
        "the panhandling was unpaid and unwanted",
        "hustle pays, the salary proves it",
    ])
    r = corpus_ratio(c["soliciting strangers"])
    if r is VOID or not r > 0:
        ok = False; print("corpus arm: planted co-occurrence not detected", r)
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
    print("specimens:")
    for s in SPECIMENS:
        print(f"  - {s['name']}: {s['before']}  →  {s['after']}  ({s['tag']})")
