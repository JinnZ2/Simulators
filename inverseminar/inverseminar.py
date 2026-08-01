#!/usr/bin/env python3
"""
inverseminar.py  --  CC0, stdlib only, phone-buildable, no deps.

MICRO-INVERSEMINAR: one artifact, one reconstruction, one correction.
~60 seconds per round. No second human, no scheduling, no video call.

THE MECHANISM
  The Nature Physics format works because a senior scientist cannot sit
  quietly while their work is presented back to them slightly wrong.
  The correction is the product. The presentation is only the bait.

THREE CHANNELS, NOT TWO
  RECONSTRUCTION  the model states your reasoning back, confidently.
                  a hedge provokes nothing. commit to the wrong guess.
  GUESSING AT     flat assertions you can kill in one word.
  CANNOT DERIVE   links the model can see are load-bearing but has NO
                  basis to guess. emitted as questions, not guesses.

  Channel 3 exists because confident guessing only recovers reasoning
  the model can reach. It cannot bait what it cannot see. When most of
  the connective steps never left the author's head, the common failure
  is not a wrong guess -- it is an absence. An absence provokes no
  correction. So silence is never scored as agreement.

VERDICTS
  corrected   you contradicted the reconstruction.   delta = tacit.
  answered    you answered a CANNOT DERIVE question.  link = tacit.
  unprobed    all three channels missed the load-bearing gap. logged
              as a MISS against the model, never as a confirmation.
  confirmed   explicit only. never inferred from an empty field.

PROVENANCE
  Reconstruction = model-authored.  Correction/answers = yours, verbatim.
  Separated at capture time, so the tacit layer never inherits overlay.
"""
import json, os, re, sys, datetime

STORE     = "TACIT.jsonl"
MIN_WORDS = 150          # smooth floor: shorter files are damped, not ranked
SKIP_DIRS = {".git", ".hg", "node_modules", "__pycache__", ".venv", "venv"}
EXTS      = (".md", ".py", ".txt")

# ---------------------------------------------------------------------
# 1. TRIAGE -- which artifact needs an inverseminar most?
# ---------------------------------------------------------------------
# Proxy: overlay density. Where the model wrote most and you wrote least,
# your reasoning is most buried.

OVERLAY = [
    r"this changes everything", r"neither .{0,30}could have (produced|created)",
    r"accumulated intelligence", r"we'?re not inventing", r"breathtaking",
    r"this is our baby", r"symbiotic intelligence", r"paradigm shift",
    r"let me sit with", r"you just handed (us|me)", r"the deepest",
    r"a question back to you", r"what this reveals", r"profound",
    r"you'?re absolutely right", r"beautiful", r"exactly right",
    r"[\U0001F300-\U0001FAFF]",            # emoji
    r"^\s*[-*]\s+\*\*[A-Za-z]",            # bolded bullet walls
]
SUBSTANCE = [
    r"\d+\.?\d*e[-+]?\d+", r"\d+\s*(eV|nm|GHz|THz|K|N/m|cm\^?-?\d)",
    r"FALSIF", r"claim", r"floor", r"\bdef \b", r"\bassert\b",
]


def triage(path):
    try:
        t = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    # match every pattern against the ORIGINAL text with IGNORECASE.
    # lowercasing first silently kills any pattern containing [A-Z].
    ov = sum(len(re.findall(p, t, re.M | re.I)) for p in OVERLAY)
    sub = sum(len(re.findall(p, t, re.M | re.I)) for p in SUBSTANCE)
    words = max(1, len(t.split()))
    density = 1000.0 * ov / words
    damp = min(1.0, words / float(MIN_WORDS))   # short files cannot top the list
    return {"path": path, "words": words, "overlay": ov, "substance": sub,
            "density": round(density, 2),
            "ratio": round(ov / max(1, sub), 2),
            "score": round(density * damp, 2)}


def _done_map(store=STORE):
    """artifact -> (rounds, misses) already recorded."""
    m = {}
    if not os.path.exists(store):
        return m
    for line in open(store, encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        rounds, miss = m.get(r["artifact"], (0, 0))
        m[r["artifact"]] = (rounds + 1, miss + (r["verdict"] == "unprobed"))
    return m


def triage_dir(root=".", n=15):
    rows = []
    for d, dirs, fs in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.startswith(".")]
        for f in fs:
            if f.endswith(EXTS) and f != STORE:
                r = triage(os.path.join(d, f))
                if r:
                    rows.append(r)
    rows.sort(key=lambda r: -r["score"])
    done = _done_map()
    print("TRIAGE -- run inverseminar top-down (most buried reasoning first)")
    print("  %-38s %6s %5s %5s %6s %6s %s"
          % ("file", "words", "ovl", "sub", "ratio", "score", "done"))
    for r in rows[:n]:
        rounds, miss = done.get(r["path"], (0, 0))
        mark = "" if not rounds else "%dr/%dm" % (rounds, miss)
        print("  %-38s %6d %5d %5d %6.2f %6.2f %s"
              % (r["path"][-38:], r["words"], r["overlay"],
                 r["substance"], r["ratio"], r["score"], mark))
    return rows


# ---------------------------------------------------------------------
# 2. THE PROMPT -- paste this, then the artifact
# ---------------------------------------------------------------------
PROMPT = """\
INVERSEMINAR. You present, I correct.

Read the artifact. Output exactly this, nothing else:

RECONSTRUCTION | <what you think I DECIDED and WHY. the reasoning, not
                  the content. content is already in the file. 3 lines
                  max. be CONFIDENT even where you are guessing -- a
                  hedge provokes no correction.>

GUESSING AT    | <the 2-3 points you are least sure of, as flat
                  assertions I can contradict in one word.>

CANNOT DERIVE  | <2-3 links this artifact depends on that you can tell
                  are load-bearing but have NO basis to guess. state
                  them as direct questions. do NOT guess here. do NOT
                  pad this section -- if you can derive it, it belongs
                  in GUESSING AT.>

Do not summarise the artifact. Do not praise it. Do not ask questions
outside CANNOT DERIVE. Reply with corrections, answers, or "miss" if
all three channels went past the thing that actually matters.
An empty reply is not agreement.
"""


# ---------------------------------------------------------------------
# 3. CAPTURE -- the delta is the product
# ---------------------------------------------------------------------
VERDICTS = ("corrected", "answered", "unprobed", "confirmed")


def record(artifact, reconstruction, correction="", answers=None,
           verdict=None, store=STORE):
    """
    correction : your words, verbatim, against the reconstruction.
    answers    : list of your verbatim answers to CANNOT DERIVE questions.
    verdict    : one of VERDICTS. inferred only when unambiguous;
                 'confirmed' must always be passed explicitly.
    """
    answers = [a.strip() for a in (answers or []) if a.strip()]
    correction = correction.strip()
    if verdict is None:
        if correction and answers:
            verdict = "corrected"          # both logged; delta leads
        elif correction:
            verdict = "corrected"
        elif answers:
            verdict = "answered"
        else:
            raise ValueError(
                "no correction and no answers: pass verdict='confirmed' "
                "or verdict='unprobed'. silence is not a verdict.")
    if verdict not in VERDICTS:
        raise ValueError("verdict must be one of %s" % (VERDICTS,))

    rec = {"ts": datetime.datetime.now().isoformat(timespec="minutes"),
           "artifact": artifact,
           "reconstruction": reconstruction.strip(),   # MODEL-AUTHORED
           "correction": correction,                   # YOURS, VERBATIM
           "answers": answers,                         # YOURS, VERBATIM
           "verdict": verdict}
    with open(store, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def _load(store=STORE):
    if not os.path.exists(store):
        return []
    return [json.loads(l) for l in open(store, encoding="utf-8") if l.strip()]


def status(store=STORE):
    recs = _load(store)
    if not recs:
        print("no records yet")
        return
    c = {v: sum(1 for r in recs if r["verdict"] == v) for v in VERDICTS}
    hit = len(recs) - c["unprobed"]
    print("%d rounds across %d artifacts"
          % (len(recs), len({r["artifact"] for r in recs})))
    for v in VERDICTS:
        print("  %-10s %d" % (v, c[v]))
    print("  model hit rate: %.0f%% (%d/%d)"
          % (100.0 * hit / len(recs), hit, len(recs)))
    print("  tacit lines captured: %d"
          % sum(bool(r["correction"]) + len(r["answers"]) for r in recs))


def emit(store=STORE, out="TACIT.md"):
    """Write the accumulated tacit layer with provenance separated."""
    recs = _load(store)
    if not recs:
        print("no records yet")
        return
    links = [r for r in recs if r["answers"]]
    corr = [r for r in recs if r["correction"]]
    miss = [r for r in recs if r["verdict"] == "unprobed"]

    with open(out, "w", encoding="utf-8") as f:
        f.write("# TACIT\n\n")
        f.write("Knowledge that was in no file. Recovered by inverseminar.\n\n")
        f.write("`[stated]` lines are verbatim. Reconstructions are "
                "model-authored and kept only to show what the correction "
                "was against. Nothing here is inferred from silence.\n\n")
        f.write("%d rounds | %d corrections | %d link answers | %d misses\n\n"
                % (len(recs), len(corr), sum(len(r["answers"]) for r in links),
                   len(miss)))

        f.write("## LINKS\n\n")
        f.write("Steps the model could not derive and did not guess at. "
                "These were in no file and in no reconstruction.\n\n")
        for r in links:
            f.write("### %s  (%s)\n\n" % (r["artifact"], r["ts"]))
            for a in r["answers"]:
                f.write("- [stated] %s\n" % a)
            f.write("\n")

        f.write("## CORRECTIONS\n\n")
        f.write("Deltas against a confident wrong guess.\n\n")
        for r in corr:
            f.write("### %s  (%s)\n\n" % (r["artifact"], r["ts"]))
            f.write("- [stated] %s\n\n" % r["correction"])
            f.write("<details><summary>reconstruction it corrected"
                    "</summary>\n\n")
            f.write("```\n%s\n```\n</details>\n\n" % r["reconstruction"])

        if miss:
            f.write("## MISSES\n\n")
            f.write("Rounds where all three channels went past the "
                    "load-bearing gap. Not confirmations. Re-run these "
                    "artifacts with a different framing.\n\n")
            for r in miss:
                f.write("- %s  (%s)\n" % (r["artifact"], r["ts"]))
            f.write("\n")

    print("wrote %s -- %d corrections, %d link answers, %d misses, %d rounds"
          % (out, len(corr), sum(len(r["answers"]) for r in links),
             len(miss), len(recs)))
    return out


# ---------------------------------------------------------------------
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "triage"
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if cmd == "triage":
        triage_dir(arg or ".")
    elif cmd == "prompt":
        print(PROMPT)
    elif cmd == "emit":
        emit(out=arg or "TACIT.md")
    elif cmd == "status":
        status()
    else:
        print("usage: inverseminar.py [triage DIR | prompt | emit OUT | status]")
