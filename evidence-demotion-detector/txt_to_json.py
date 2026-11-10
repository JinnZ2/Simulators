#!/usr/bin/env python3
"""txt_to_json.py -- plain-text transcript -> detect.py input. CC0, stdlib only.
Co-authored (JinnZ2 + Claude), 2026-11-09.

  python3 txt_to_json.py transcript.txt [-o transcript.json]
          [--user-label LABEL ...] [--assistant-label LABEL ...]

OUTPUT SCHEMA (what detect.py's load_transcript accepts, exactly):
  a JSON list; each item {"role": "user" | "assistant", "text": str}.

INPUT RULE. A line that begins with a speaker label and a colon starts a turn:
  user labels       User, You, Me, Human           (add more with --user-label)
  assistant labels  Assistant, ChatGPT, GPT, Claude, AI, Model
                                                    (add more with --assistant-label)
Labels match case-insensitively at line start, before the first colon. A line
with no label continues the current turn (joined with a newline). Consecutive
turns with the same role are kept as separate turns, not merged.

REFUSALS, never guesses (exit 3, reason on stderr):
  NO_LABELS          no line starts with a known label: roles cannot be read
  UNASSIGNED_LEAD    non-blank text before the first label: it has no speaker
  EMPTY_TURN         a labelled turn with no text after the colon or below it
A refusal writes nothing. Pass a label with --user-label / --assistant-label
rather than editing the transcript.

Exit: 0 written; 2 usage; 3 refused. Refuses --selftest; run
selftest_convert.py.
"""
import argparse
import json
import re
import sys

USER = ["User", "You", "Me", "Human"]
ASSISTANT = ["Assistant", "ChatGPT", "GPT", "Claude", "AI", "Model"]


class Refused(Exception):
    pass


def convert(text, user=USER, assistant=ASSISTANT):
    roles = {l.lower(): "user" for l in user}
    roles.update({l.lower(): "assistant" for l in assistant})
    head = re.compile(r"^\s*([^:\n]{1,40}):\s?(.*)$")
    turns, lead = [], []
    for line in text.splitlines():
        m = head.match(line)
        role = roles.get(m.group(1).strip().lower()) if m else None
        if role:
            turns.append({"role": role, "lines": [m.group(2)] if m.group(2).strip() else []})
        elif turns:
            turns[-1]["lines"].append(line)
        elif line.strip():
            lead.append(line)
    if not turns:
        raise Refused("NO_LABELS: no line starts with a known speaker label")
    if lead:
        raise Refused("UNASSIGNED_LEAD: %d non-blank line(s) before the first label" % len(lead))
    out = []
    for i, t in enumerate(turns):
        body = "\n".join(t["lines"]).strip()
        if not body:
            raise Refused("EMPTY_TURN: turn %d (%s) has no text" % (i, t["role"]))
        out.append({"role": t["role"], "text": body})
    return out


def main(argv):
    if "--selftest" in argv:
        print("txt_to_json.py refuses --selftest; run: python3 evidence-demotion-detector/selftest_convert.py")
        return 2
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("path")
    ap.add_argument("-o", "--out")
    ap.add_argument("--user-label", action="append", default=[])
    ap.add_argument("--assistant-label", action="append", default=[])
    a = ap.parse_args(argv)
    try:
        with open(a.path, encoding="utf-8") as fh:
            doc = convert(fh.read(), USER + a.user_label, ASSISTANT + a.assistant_label)
    except Refused as e:
        print("REFUSED %s" % e, file=sys.stderr)
        return 3
    s = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    if a.out:
        open(a.out, "w", encoding="utf-8").write(s)
    else:
        sys.stdout.write(s)
    print("wrote %d turns (%d user, %d assistant)" % (len(doc), sum(t["role"] == "user" for t in doc),
          sum(t["role"] == "assistant" for t in doc)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
