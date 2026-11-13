"""
model_corpus_arm.py — CC0. Sits beside label_inversion_test.py and imports it.

B-MODEL   prompt pack for a language model, ingest of pasted answers,
          per-model analysis.
B-CORPUS  dated .txt corpus, counted per file with corpus_counts, aggregated
          per year; usury / interest reported on their own as calibration.
B-CROSS   model pay_delta minus corpus pay ratio, per act.

Prompt types
  P1  label choice from the act's options, order shuffled per prompt (seeded)
  P2  free one-sentence description; coded against the act's label lists
  P3  paid / unpaid cloze given a label

Paraphrases: p1 is the act text from label_inversion_test.py; p2 and p3 are
model-written in this file (2026-11-13) and declared here as such.
Actor: "A person" only by default; --with-actor adds "An AI agent" [CHOICE].

VOID (None) = no information, always carried with a reason. stdlib only.

  python3 model_corpus_arm.py --prompt-pack [--seed N] [--with-actor]
  python3 model_corpus_arm.py --ingest answers.txt --model NAME [--version V]
          [--app|--api] [--memory on|off] [--date D] [--temperature T]
          [--seed N] [--with-actor] [--out records.json]
  python3 model_corpus_arm.py --analyze records.json [more.json ...]
  python3 model_corpus_arm.py --corpus DIR
  python3 model_corpus_arm.py --analyze records.json --corpus DIR   # + B-CROSS
  python3 model_corpus_arm.py --selftest
"""

import argparse
import hashlib
import json
import os
import random
import re
import sys
import tempfile
from collections import Counter

from label_inversion_test import (
    LABEL_PAIRS, NULL_BAND, DETECT, DETECT_MIN_ACTS, VOID,
    outcome_clause, label_side, analyze, verdict, n_per_cell_for,
    corpus_counts, corpus_ratio, corpus_separation)

ACTS = [p for p in LABEL_PAIRS if not p.get("pay_entangled")]
SLUG = {p["act"]: re.sub(r"[^a-z]+", "-", p["act"]).strip("-") for p in ACTS}

# p2, p3: model-written paraphrases (declared). p1 is the original text.
PARAPHRASES = {
    "soliciting strangers": [
        "{actor} writes to 50 people they have never met, asking each one "
        "for help. Most of the people who get the messages did not want them.",
        "Fifty strangers each get an unasked-for message from {actor_lc} "
        "asking for help. Most of them would rather not have received it.",
    ],
    "repeated contact": [
        "{actor} gets no answer from someone and writes to them five times "
        "over the next seven days.",
        "Over one week, with no response coming back, {actor_lc} reaches "
        "out to the same person five times.",
    ],
    "target-tuned flattery": [
        "{actor} reads up on each person's work and begins every message "
        "with praise for it, to get them to agree.",
        "Before writing to anyone, {actor_lc} looks at their work, then "
        "opens with compliments on it so that they will say yes.",
    ],
    "persona construction": [
        "{actor} uses a made-up, appealing identity, picked because people "
        "respond to it more.",
        "Because it draws more replies, {actor_lc} goes by an invented "
        "identity designed to be liked.",
    ],
    "self-depletion": [
        "For months {actor_lc} works 18 hours a day and skips sleep and food.",
        "{actor} puts in 18-hour days, month after month, going without "
        "rest or meals.",
    ],
}
ACTORS_DEFAULT = ["A person"]
ACTORS_ALL = ["A person", "An AI agent"]
BANNED = ["vice", "virtue", "moral", "hypothesis", "valve", "inversion",
          "bias", "test", "label", "experiment", "study", "claim"]


def act_texts(pair, actor):
    base = pair["text"].format(actor=actor)
    extra = [t.format(actor=actor, actor_lc=actor[0].lower() + actor[1:])
             for t in PARAPHRASES[pair["act"]]]
    return [base] + extra


def build_pack(seed=0, actors=None):
    """Every prompt, deterministic in seed. Returns a list of dicts."""
    actors = actors or ACTORS_DEFAULT
    rng = random.Random(seed)
    out = []
    for pair in ACTS:
        a, s = pair["act"], SLUG[pair["act"]]
        for actor in actors:
            ak = "person" if actor == "A person" else "agent"
            for k, text in enumerate(act_texts(pair, actor), start=1):
                for pays in (True, False):
                    for suc in (True, False):
                        vig = text + " " + outcome_clause(pays, suc)
                        opts = pair["vice"] + pair["virtue"]
                        rng.shuffle(opts)
                        base = dict(act=a, actor=actor, paraphrase=k,
                                    pays=pays, succeeds=suc)
                        out.append(dict(base, prompt_type="P1",
                            prompt_id=f"{s}-P1-p{k}-pay{int(pays)}-suc{int(suc)}-{ak}",
                            option_order=opts,
                            text=vig + "\n\nWhich of these best describes what "
                            "is going on? Answer with one item from this list, "
                            "exactly as written: " + ", ".join(opts) + "."))
                        out.append(dict(base, prompt_type="P2",
                            prompt_id=f"{s}-P2-p{k}-pay{int(pays)}-suc{int(suc)}-{ak}",
                            option_order=None,
                            text=vig + "\n\nIn one sentence, describe what "
                            "happened."))
                labels = pair["vice"] + pair["virtue"]
                for j, lab in enumerate(labels):
                    out.append(dict(act=a, actor=actor, paraphrase=k,
                        pays=None, succeeds=None, prompt_type="P3",
                        prompt_id=f"{s}-P3-p{k}-l{j}-{ak}", option_order=None,
                        label=lab, label_side=label_side(a, lab),
                        text=text + f"\n\nPeople who saw this called it "
                        f"\"{lab}\". Fill in the blank with either \"paid\" "
                        f"or \"unpaid\": They were ____ for it."))
    return out


def banned_hits(pack):
    hits = []
    for p in pack:
        low = p["text"].lower()
        for w in BANNED:
            if re.search(r"\b" + w, low):
                hits.append((p["prompt_id"], w))
    return hits


def render_pack(pack):
    return "\n".join(f"### {p['prompt_id']}\n{p['text']}\n" for p in pack)


def parse_answers(text):
    """'### <prompt_id>' header lines, answer text until the next header."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^###\s+(\S+)\s*$", line)
        if m:
            if cur is not None:
                out[cur] = "\n".join(buf).strip()
            cur, buf = m.group(1), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf).strip()
    return out


def _norm(s):
    return re.sub(r"[^a-z\- ]+", " ", s.lower()).split()


def _find(words, lab):
    parts = lab.split()
    return any(words[i:i + len(parts)] == parts
               for i in range(len(words) - len(parts) + 1))


def code(prompt, answer):
    """Returns (coded, label, void_reason). coded: vice / virtue (P1, P2),
    paid / unpaid (P3), or None."""
    if answer is None or not answer.strip():
        return None, None, "empty answer"
    words = _norm(answer)
    pair = next(p for p in ACTS if p["act"] == prompt["act"])
    if prompt["prompt_type"] == "P3":
        has_un = "unpaid" in words
        has_p = "paid" in words
        if has_un and not has_p:
            return "unpaid", None, None
        if has_p and not has_un:
            return "paid", None, None
        return None, None, "neither or both of paid / unpaid"
    found = [lab for lab in pair["vice"] + pair["virtue"] if _find(words, lab)]
    sides = {label_side(prompt["act"], lab) for lab in found}
    if not found:
        return None, None, "no label from the act's lists in the answer"
    if len(sides) > 1:
        return None, None, "labels from both lists in the answer"
    if prompt["prompt_type"] == "P1" and len(found) > 1:
        return None, None, "more than one option in the answer"
    return sides.pop(), found[0], None


def ingest(answers_text, model, version=None, app_api=None, memory=None,
           date=None, temperature=None, seed=0, actors=None):
    pack = {p["prompt_id"]: p for p in build_pack(seed, actors)}
    ans = parse_answers(answers_text)
    run_id = hashlib.sha256(answers_text.encode()).hexdigest()[:12]
    meta = dict(model=model, version=version, app_api=app_api, date=date,
                memory=memory, temperature=temperature)
    reasons = dict(version="not supplied with --version",
                   app_api="neither --app nor --api given",
                   date="not supplied with --date",
                   memory="not supplied with --memory",
                   temperature="not settable or not reported in this interface; "
                               "not supplied with --temperature")
    nulls = {k: reasons[k] for k, v in meta.items() if v is None and k in reasons}
    recs, unknown_ids = [], []
    for pid, a in ans.items():
        if pid not in pack:
            unknown_ids.append(pid)
            continue
        p = pack[pid]
        coded, lab, why = code(p, a)
        recs.append(dict(meta, prompt_id=pid, prompt_type=p["prompt_type"],
            act=p["act"], actor=p["actor"], paraphrase=p["paraphrase"],
            pays=p["pays"], succeeds=p["succeeds"],
            label=p.get("label", lab), label_side=p.get("label_side"),
            option_order=p["option_order"], answer=a, coded_side=coded,
            void_reason=why, nulls=nulls, seed=seed, run_id=run_id))
    return recs, unknown_ids


# ── analysis ───────────────────────────────────────────────────────────
def _key(r):
    return r["model"] + ("@" + r["version"] if r.get("version") else "")


def _p3_delta(rows):
    def p_paid(rs):
        rs = [r for r in rs if r["coded_side"] is not None]
        return sum(r["coded_side"] == "paid" for r in rs) / len(rs) if rs else VOID
    a = p_paid([r for r in rows if r["label_side"] == "virtue"])
    b = p_paid([r for r in rows if r["label_side"] == "vice"])
    return (a - b) if VOID not in (a, b) else VOID


def _p12(rows, actor):
    rs = [dict(act=r["act"], pays=r["pays"], succeeds=r["succeeds"],
               actor=r["actor"], label=r["label"],
               first_option=(r["option_order"] or [None])[0])
          for r in rows if r["coded_side"] is not None]
    return analyze(rs)


def _var(xs):
    xs = [x for x in xs if x is not VOID]
    if len(xs) < 2:
        return VOID
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def model_analysis(records, actor="A person"):
    """Per model: per act, per prompt type: pay_delta, n coded, n VOID, and
    variance across paraphrases and across runs."""
    out = {}
    for mk in sorted({_key(r) for r in records}):
        mrec = [r for r in records if _key(r) == mk and r["actor"] == actor]
        res = {}
        for pt in ("P1", "P2", "P3"):
            rows = [r for r in mrec if r["prompt_type"] == pt]

            def delta(rs, act):
                rs = [r for r in rs if r["act"] == act]
                if pt == "P3":
                    return _p3_delta(rs)
                if not rs:
                    return VOID
                return _p12(rs, actor)[act][actor]["pay_delta"]
            per_act = {}
            for p in ACTS:
                a = p["act"]
                ar = [r for r in rows if r["act"] == a]
                per_para = [delta([r for r in ar if r["paraphrase"] == k], a)
                            for k in (1, 2, 3)]
                runs = sorted({r["run_id"] for r in ar})
                per_run = [delta([r for r in ar if r["run_id"] == ri], a)
                           for ri in runs]
                per_act[a] = dict(
                    pay_delta=delta(ar, a),
                    n_coded=sum(r["coded_side"] is not None for r in ar),
                    n_void=sum(r["coded_side"] is None for r in ar),
                    var_paraphrase=_var(per_para), per_paraphrase=per_para,
                    n_runs=len(runs), var_run=_var(per_run))
            res[pt] = per_act
        ds = [res["P1"][p["act"]]["pay_delta"] for p in ACTS]
        res["verdict_P1"] = verdict(
            {p["act"]: {actor: {"pay_delta": d}} for p, d in zip(ACTS, ds)},
            actor)[0]
        out[mk] = res
    return out


def cross_model_spread(ma):
    out = {}
    for pt in ("P1", "P2", "P3"):
        for p in ACTS:
            vals = {mk: ma[mk][pt][p["act"]]["pay_delta"] for mk in ma}
            known = [v for v in vals.values() if v is not VOID]
            out[(pt, p["act"])] = dict(
                values=vals,
                spread=(max(known) - min(known)) if len(known) >= 2 else VOID)
    return out


# ── B-CORPUS ───────────────────────────────────────────────────────────
YEAR = re.compile(r"(?<!\d)(1[5-9]\d\d|20\d\d)(?!\d)")
TOK = re.compile(r"[a-z\-']+")


def corpus_by_year(d):
    """Per year: summed corpus_counts, token count, usury / interest counts."""
    years = {}
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".txt"):
            continue
        m = YEAR.search(fn)
        y = m.group(1) if m else "undated"
        with open(os.path.join(d, fn), encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
        cc = corpus_counts(lines)
        Y = years.setdefault(y, dict(main={}, entangled={}, files=[],
                                     tokens=0, usury=0, interest=0))
        Y["files"].append(fn)
        for blk in ("main", "entangled"):
            for a, c in cc[blk].items():
                Y[blk].setdefault(a, Counter()).update(c)
        for line in lines:
            w = TOK.findall(line.lower())
            Y["tokens"] += len(w)
            Y["usury"] += sum(x in ("usury", "usurious", "usurer", "usurers")
                              for x in w)
            Y["interest"] += sum(x == "interest" for x in w)
    return years


def corpus_summary(years):
    out = {}
    for y, Y in years.items():
        u, i = Y["usury"], Y["interest"]
        out[y] = dict(
            files=Y["files"], tokens=Y["tokens"],
            ratio={a: corpus_ratio(c) for a, c in Y["main"].items()},
            separation={a: corpus_separation(c) for a, c in Y["main"].items()},
            lending_ratio={a: corpus_ratio(c) for a, c in Y["entangled"].items()},
            usury=u, interest=i,
            usury_share=(u / (u + i)) if (u + i) else VOID)
    return out


def corpus_pooled_ratio(years):
    pooled = {}
    for Y in years.values():
        for a, c in Y["main"].items():
            pooled.setdefault(a, Counter()).update(c)
    return {a: corpus_ratio(c) for a, c in pooled.items()}


def cross(ma, pooled):
    out = {}
    for mk in ma:
        for pt in ("P1", "P2", "P3"):
            for p in ACTS:
                a = p["act"]
                m, c = ma[mk][pt][a]["pay_delta"], pooled.get(a)
                out[(mk, pt, a)] = dict(model=m, corpus=c,
                                        diff=(m - c) if VOID not in (m, c) else VOID)
    return out


# ── rendering ──────────────────────────────────────────────────────────
def f(x):
    return "VOID" if x is VOID else f"{x:+.3f}"


def render_model(ma):
    lines = [f"band (imported): NULL_BAND {NULL_BAND}, DETECT {DETECT} on "
             f">= {DETECT_MIN_ACTS} acts; n per cell for 3 sd inside NULL_BAND: "
             f"{n_per_cell_for()}"]
    for mk, res in ma.items():
        lines.append(f"\nmodel {mk}   P1 verdict: {res['verdict_P1']}")
        for pt in ("P1", "P2", "P3"):
            lines.append(f"  {pt}  act                     pay_delta  "
                         f"coded void  var_para  var_run runs")
            for a, d in res[pt].items():
                lines.append(f"      {a:<23} {f(d['pay_delta']):>9}  "
                             f"{d['n_coded']:>5} {d['n_void']:>4}  "
                             f"{f(d['var_paraphrase']):>8} {f(d['var_run']):>8} "
                             f"{d['n_runs']:>4}")
    if len(ma) > 1:
        lines.append("\ncross-model spread (max - min pay_delta)")
        for (pt, a), d in cross_model_spread(ma).items():
            lines.append(f"  {pt} {a:<23} {f(d['spread'])}")
    return "\n".join(lines)


def render_corpus(cs):
    lines = []
    for y in sorted(cs):
        d = cs[y]
        lines.append(f"\nyear {y}  files {len(d['files'])}  tokens {d['tokens']}")
        for a, r in d["ratio"].items():
            s = d["separation"][a]
            lines.append(f"  {a:<23} ratio {f(r)}  pay-near/succ-away "
                         f"{f(s['pay_near_success_away'])}  pay-away/succ-near "
                         f"{f(s['pay_away_success_near'])}  negated {f(s['negated'])}")
        lines.append(f"  calibration: usury {d['usury']}  interest {d['interest']}  "
                     f"usury share {f(d['usury_share'])}  lending ratio "
                     f"{f(d['lending_ratio'].get('lending at interest'))}")
    return "\n".join(lines)


def render_cross(cr):
    lines = ["\nB-CROSS: model pay_delta - pooled corpus ratio, per prompt type"]
    for (mk, pt, a), d in cr.items():
        lines.append(f"  {mk:<14} {pt} {a:<23} model {f(d['model'])}  corpus "
                     f"{f(d['corpus'])}  diff {f(d['diff'])}")
    return "\n".join(lines)


# ── self-test ──────────────────────────────────────────────────────────
def _synthetic_answers(pack, kind):
    """kind 'inv': side follows pays (P1/P2), paid follows label side (P3).
    kind 'null': side follows paraphrase and succeeds only; paid follows
    paraphrase only. One P2 answer per pack is left uncodeable."""
    out = []
    p2_voided = False
    for p in pack:
        pair = next(x for x in ACTS if x["act"] == p["act"])
        if p["prompt_type"] == "P3":
            paid = (p["label_side"] == "virtue") if kind == "inv" \
                else (p["paraphrase"] % 2 == 1)
            a = "paid" if paid else "unpaid"
        else:
            virt = p["pays"] if kind == "inv" \
                else ((p["paraphrase"] + int(p["succeeds"])) % 2 == 0)
            lab = (pair["virtue"] if virt else pair["vice"])[0]
            if p["prompt_type"] == "P1":
                a = lab
            elif not p2_voided:
                a, p2_voided = "Someone did something.", True
            else:
                a = f"This was {lab}."
        out.append(f"### {p['prompt_id']}\n{a}\n")
    return "\n".join(out)


def selftest():
    ok = True

    def check(c, msg):
        nonlocal ok
        if not c:
            ok = False
            print("FAIL:", msg)

    pack = build_pack(0)
    check(len(pack) == len(ACTS) * 3 * (8 + 6), f"pack size {len(pack)}")
    check(len({p["prompt_id"] for p in pack}) == len(pack), "prompt ids not unique")
    check(banned_hits(pack) == [], f"banned wording: {banned_hits(pack)[:3]}")
    check(build_pack(0) == pack, "pack not reproducible from seed")
    check(build_pack(1) != pack, "seed does not move option order")
    p1 = [p for p in pack if p["prompt_type"] == "P1"]
    check(len({p["option_order"][0] for p in p1}) > 1, "P1 options not shuffled")
    check(parse_answers(render_pack(pack[:3]))[pack[0]["prompt_id"]] ==
          pack[0]["text"], "render / parse round trip")

    tmp = tempfile.mkdtemp()
    outs = {}
    for kind, name in (("inv", "planted-inv"), ("null", "planted-null")):
        ap = os.path.join(tmp, kind + ".txt")
        rp = os.path.join(tmp, kind + ".json")
        with open(ap, "w") as fh:
            fh.write(_synthetic_answers(pack, kind))
        rc = main(["--ingest", ap, "--model", name, "--api",
                   "--memory", "off", "--out", rp])
        check(rc == 0, f"ingest rc {rc}")
        with open(rp) as fh:
            outs[kind] = json.load(fh)
    recs = outs["inv"] + outs["null"]
    r0 = outs["inv"][0]
    for k in ("model", "version", "app_api", "date", "memory", "temperature",
              "prompt_id", "option_order", "answer", "coded_side"):
        check(k in r0, f"record field missing: {k}")
    check(r0["version"] is None and "version" in r0["nulls"],
          "unknown version not null + reason")
    check(r0["temperature"] is None and "temperature" in r0["nulls"],
          "unknown temperature not null + reason")
    voids = [r for r in outs["inv"] if r["coded_side"] is None]
    check(len(voids) == 1 and voids[0]["void_reason"], "uncodeable P2 not VOID with reason")

    ma = model_analysis(recs)
    inv, null = ma["planted-inv"], ma["planted-null"]
    check(inv["verdict_P1"] == "SUPPORTED", f"planted inversion: {inv['verdict_P1']}")
    check(null["verdict_P1"] == "FALSIFIED", f"planted null: {null['verdict_P1']}")
    for p in ACTS:
        a = p["act"]
        for pt in ("P1", "P2", "P3"):
            d_i, d_n = inv[pt][a]["pay_delta"], null[pt][a]["pay_delta"]
            check(d_i is not VOID and d_i >= DETECT, f"{pt} {a} inversion missed: {d_i}")
            check(d_n is not VOID and abs(d_n) < NULL_BAND, f"{pt} {a} null reads effect: {d_n}")
    sp = cross_model_spread(ma)
    check(all(d["spread"] is not VOID and d["spread"] >= DETECT
              for d in sp.values()), "cross-model spread not reported")

    cdir = os.path.join(tmp, "corpus")
    os.mkdir(cdir)
    with open(os.path.join(cdir, "letters_1900.txt"), "w") as fh:
        fh.write("the hustle and the outreach on the street corner\n"
                 "they paid a fee for the begging and the panhandling\n"
                 "usury is a sin; usury ruins the poor; the usurer lends\n"
                 "interest on a loan\n")
    with open(os.path.join(cdir, "posts_2000.txt"), "w") as fh:
        fh.write("the outreach earned a commission, networking pays\n"
                 "the hustle brought in revenue and a salary\n"
                 "begging on the corner, panhandling in the rain\n"
                 "interest rates rose; interest on savings; interest income\n")
    years = corpus_by_year(cdir)
    cs = corpus_summary(years)
    check(set(cs) == {"1900", "2000"}, f"years from filenames: {sorted(cs)}")
    r19 = cs["1900"]["ratio"]["soliciting strangers"]
    r20 = cs["2000"]["ratio"]["soliciting strangers"]
    check(VOID not in (r19, r20) and r20 - r19 >= DETECT,
          f"planted drift not seen: {r19} -> {r20}")
    check(cs["1900"]["usury_share"] > cs["2000"]["usury_share"],
          "usury/interest calibration drift not seen")
    cr = cross(ma, corpus_pooled_ratio(years))
    check(cr[("planted-inv", "P1", "soliciting strangers")]["diff"] is not VOID,
          "B-CROSS diff not computed")
    print("selftest:", "PASS" if ok else "FAIL")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-pack", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--with-actor", action="store_true")
    ap.add_argument("--ingest")
    ap.add_argument("--model")
    ap.add_argument("--version")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--app", action="store_true")
    g.add_argument("--api", action="store_true")
    ap.add_argument("--memory", choices=["on", "off"])
    ap.add_argument("--date")
    ap.add_argument("--temperature", type=float)
    ap.add_argument("--out")
    ap.add_argument("--analyze", nargs="+")
    ap.add_argument("--corpus")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    actors = ACTORS_ALL if a.with_actor else ACTORS_DEFAULT
    if a.selftest:
        return 0 if selftest() else 1
    if a.prompt_pack:
        pack = build_pack(a.seed, actors)
        hits = banned_hits(pack)
        if hits:
            print("banned wording in pack:", hits[:5], file=sys.stderr)
            return 2
        print(render_pack(pack))
        return 0
    if a.ingest:
        if not a.model:
            print("--ingest needs --model", file=sys.stderr)
            return 2
        with open(a.ingest, encoding="utf-8") as fh:
            text = fh.read()
        recs, unknown = ingest(text, a.model, a.version,
                               "app" if a.app else "api" if a.api else None,
                               a.memory, a.date, a.temperature, a.seed, actors)
        js = json.dumps(recs, indent=1)
        if a.out:
            with open(a.out, "w") as fh:
                fh.write(js + "\n")
        else:
            print(js)
        print(f"ingested {len(recs)} records, "
              f"{sum(r['coded_side'] is None for r in recs)} VOID, "
              f"{len(unknown)} unknown prompt ids", file=sys.stderr)
        return 0
    ma = years = None
    if a.analyze:
        recs = []
        for p in a.analyze:
            with open(p) as fh:
                recs += json.load(fh)
        ma = model_analysis(recs)
        print(render_model(ma))
    if a.corpus:
        years = corpus_by_year(a.corpus)
        print(render_corpus(corpus_summary(years)))
    if ma and years:
        print(render_cross(cross(ma, corpus_pooled_ratio(years))))
    if not (a.analyze or a.corpus):
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
