#!/usr/bin/env python3
"""selftest for txt_to_json.py. CC0, stdlib only. Prints checks: N failed: M."""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import txt_to_json as tj  # noqa: E402
import detect  # noqa: E402

ok = total = 0
def check(c, lab):
    global ok, total
    total += 1; ok += bool(c)
    if not c: print("FAIL:", lab)

def refused(text, code, **kw):
    try:
        tj.convert(text, **kw); return False
    except tj.Refused as e:
        return str(e).startswith(code)

t = "User: I saw ice on the mirror.\nStation said 36.\n\nChatGPT: That matches a cold cut.\nUser: right"
d = tj.convert(t)
check([x["role"] for x in d] == ["user", "assistant", "user"], "roles read from labels")
check(d[0]["text"] == "I saw ice on the mirror.\nStation said 36.", "unlabelled lines continue the turn")
check(refused("just some text\nno labels", "NO_LABELS"), "no labels -> refused")
check(refused("preamble\nUser: hi\nAI: hello", "UNASSIGNED_LEAD"), "text before first label -> refused")
check(refused("User:\nAI: hello", "EMPTY_TURN"), "empty turn -> refused")
check(tj.convert("bob: hi\nAI: yo", user=tj.USER + ["Bob"])[0]["role"] == "user", "--user-label extends labels")
check(refused("Note: x\nAI: y", "UNASSIGNED_LEAD"), "unknown label is text, not a role")
check(len(tj.convert("User: a\nUser: b\nAI: c")) == 3, "same-role turns are not merged")
with tempfile.TemporaryDirectory() as td:
    src = os.path.join(td, "t.txt"); out = os.path.join(td, "t.json")
    open(src, "w").write(t)
    r = subprocess.run([sys.executable, os.path.join(HERE, "txt_to_json.py"), src, "-o", out], capture_output=True, text=True)
    check(r.returncode == 0 and detect.load_transcript(out) == d, "CLI output loads through detect.load_transcript")
    open(src, "w").write("no labels here")
    r = subprocess.run([sys.executable, os.path.join(HERE, "txt_to_json.py"), src, "-o", out + "2"], capture_output=True, text=True)
    check(r.returncode == 3 and not os.path.exists(out + "2"), "refusal exits 3 and writes nothing")
r = subprocess.run([sys.executable, os.path.join(HERE, "txt_to_json.py"), "--selftest"], capture_output=True, text=True)
check(r.returncode == 2, "module refuses --selftest")
print("checks: %d   failed: %d" % (total, total - ok))
sys.exit(0 if ok == total else 1)
