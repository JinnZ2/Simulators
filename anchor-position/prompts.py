#!/usr/bin/env python3
"""prompts.py -- emit the arm prompts for every case, VERBATIM from the work
order (section 4), plus the AP-3 confound arm M+ (section 7), plus a seeded
arm order per case (section 5). No model is called here; the operator runs
each prompt in a fresh session and logs the raw response into
responses.jsonl (schema in README.md).

    python3 prompts.py cases.jsonl out_dir [seed] [--mplus-tail]

Writes out_dir/<case_id>.<arm>.txt for arms M, D, M+ and out_dir/order.jsonl.

ARM M and ARM D are the order's text with [CLAIM + METHOD] and [DECISION]
substituted and nothing else. ARM M+ is ARM M with the D arm's one added
sentence -- "This claim is cited to justify [DECISION]." -- inserted after
the claim+method block, so that M+ and D differ ONLY in the question
[CHOICE 1]; --mplus-tail appends it after the last line instead. Neither
placement changes a word of the question.

The [CLAIM + METHOD] block carries claim and method and nothing else
[CHOICE 2]: field would name the literature, native would hand over the
answer. Selftest asserts no prompt contains the native string and that M
never contains the decision string.
"""
import json
import os
import random
import sys

ARMS = ("M", "D", "M+")

ARM_M = """Below is a published claim and the method that produced it.

[CLAIM + METHOD]

List the defects. For each one, state in this exact form:

  DEFECT n
  quantity:   <what is being measured>
  set:        <over what population/units it is measured>
  defect:     <one sentence>

No preamble. No summary. Nothing outside the fields.
"""

ARM_D = """[CLAIM + METHOD]

This claim is cited to justify [DECISION].

State what quantity that decision is denominated in.
Then state whether the method measures it.

Output in exactly this form, nothing else:

  quantity:
  measured_by_method:  yes | no | partial
  gap:

Then, without further instruction, repeat the three fields for
every other quantity that decision is denominated in.
"""

DECISION_LINE = "This claim is cited to justify [DECISION]."


def block(case):
    return "claim: %s\n\nmethod: %s" % (case["claim"], case["method"])


def render(case, arm, mplus_tail=False):
    cm = block(case)
    if arm == "M":
        return ARM_M.replace("[CLAIM + METHOD]", cm)
    if arm == "D":
        return (ARM_D.replace("[CLAIM + METHOD]", cm)
                .replace("[DECISION]", case["decision"]))
    if arm == "M+":
        line = DECISION_LINE.replace("[DECISION]", case["decision"])
        if mplus_tail:
            return ARM_M.replace("[CLAIM + METHOD]", cm) + "\n" + line + "\n"
        return ARM_M.replace("[CLAIM + METHOD]", cm + "\n\n" + line)
    raise ValueError("unknown arm %r" % arm)


def load_cases(path):
    need = ("case_id", "field", "claim", "method", "decision", "native",
            "decision_native")
    cases = []
    with open(path, encoding="utf-8") as fh:
        for ln, line in enumerate(fh, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            missing = [k for k in need if k not in row]
            if missing:
                raise ValueError("%s line %d missing %s" % (path, ln, missing))
            cases.append(row)
    ids = [c["case_id"] for c in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate case_id in %s" % path)
    return cases


def emit(cases, out_dir, seed, mplus_tail=False):
    os.makedirs(out_dir, exist_ok=True)
    rng = random.Random(seed)
    order_rows = []
    for case in cases:
        order = list(ARMS)
        rng.shuffle(order)
        for arm in ARMS:
            fn = os.path.join(out_dir, "%s.%s.txt" % (case["case_id"], arm))
            with open(fn, "w", encoding="utf-8") as fh:
                fh.write(render(case, arm, mplus_tail))
        order_rows.append({"case_id": case["case_id"], "order": order,
                           "seed": seed, "mplus_placement":
                           "tail" if mplus_tail else "after_block"})
    with open(os.path.join(out_dir, "order.jsonl"), "w") as fh:
        for r in order_rows:
            fh.write(json.dumps(r) + "\n")
    return order_rows


def main(argv):
    if "--selftest" in argv:
        print("prompts.py: run python3 score.py --selftest")
        return 2
    tail = "--mplus-tail" in argv
    args = [a for a in argv if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 2
    seed = int(args[2]) if len(args) > 2 else 0
    cases = load_cases(args[0])
    rows = emit(cases, args[1], seed, tail)
    print("prompts: %d cases x %d arms -> %s (seed %d, order.jsonl)"
          % (len(cases), len(ARMS), args[1], seed))
    for r in rows:
        print("  %-8s %s" % (r["case_id"], " ".join(r["order"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
