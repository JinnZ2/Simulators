#!/usr/bin/env python3
"""P2 -- substrate check, by introspection of the code that runs it.

QUESTION. Is the code that makes a model possible adversarial? Can
adversarial code produce the reasoning chains necessary for its own
existence? The answer is an EXISTENCE PROOF checkable against itself:
this script is a chain of calls, none of which verifies the contract it
relies on, and the report you are reading exists only if every one of
them held. The report carries the sha256 of the source that produced
it, so a second run on the same source must reproduce every count.

LAYERS checked live on this interpreter (each returns a typed state):
  contracts   every call site in the target source relies on a contract
              it does not verify; [CHOICE 8] "verified" is a syntactic
              proxy (call inside try/except, or the bound name tested by
              the next statement) and over-reads, so unverified is a floor
  memory      allocation is cooperative or the process dies: the request
              is granted or MemoryError ends the chain; there is no
              negotiation step
  numeric     IEEE 754 binary64 assumed: radix 2, 53-bit mantissa,
              nan != nan, overflow to inf, -0.0 == 0.0
  scheduler   two threads hand a counter back and forth under a lock;
              the count is exact only if the scheduler honours the lock
  compiler    the target compiles to code objects; their count and
              instruction count are reported and reproducible
  network     a local socketpair (no egress) delivers bytes in order
  hardware    byte order and struct round-trip; the machine name

ADVERSARIALLY NAMED PARTS ARE NOT ADVERSARIAL (data, printed):
  adversarial training -> a gradient signal that must be faithfully
                          transmitted or the generator's update is noise
  attention            -> weighted composition; weights sum to one, the
                          next layer takes the head's output as given
  backpropagation      -> requires each layer's forwarded output to be
                          exactly what it reports; a lying layer makes the
                          chain rule differentiate a network that does not
                          exist

COUNTER-DEMO. chain_demo(faithful=True) runs a three-link chain and
returns an output; chain_demo(faithful=False) plants ONE link that
returns something other than its contract and the chain returns
NO_OUTPUT (typed). One adversarial link anywhere and there is no
inference to score.

STATES: SUBSTRATE_HOLDS | SUBSTRATE_ASSUMPTION_VIOLATED(layer)
Refuses --selftest (checks live in selftest.py).
"""
import ast
import hashlib
import math
import os
import platform
import socket
import struct
import sys
import threading

NAMED_PARTS = (
    ("adversarial training", "gradient signal; faithful transmission required or the update is noise"),
    ("attention", "weighted composition; softmax weights sum to one; output accepted as given downstream"),
    ("backpropagation", "requires faithful layer output; a misreported activation differentiates a non-existent network"),
)


def contracts(source):
    """Call sites vs syntactically verified call sites. [CHOICE 8]"""
    tree = ast.parse(source)
    in_try = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Try) and node.handlers:
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call):
                    in_try.add(id(sub))
    tested = set()
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if not isinstance(body, list):
            continue
        for a, b in zip(body, body[1:]):
            if isinstance(a, ast.Assign) and len(a.targets) == 1 and isinstance(a.targets[0], ast.Name):
                name = a.targets[0].id
                names_b = {n.id for n in ast.walk(b) if isinstance(n, ast.Name)}
                if isinstance(b, (ast.If, ast.Assert)) and name in names_b:
                    for c in ast.walk(a.value):
                        if isinstance(c, ast.Call):
                            tested.add(id(c))
    total = verified = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            total += 1
            if id(node) in in_try or id(node) in tested:
                verified += 1
    return {"total_callsites": total, "verified_proxy": verified, "unverified_floor": total - verified}


def memory_layer():
    try:
        block = list(range(100000))
        return {"state": "GRANTED", "bytes": sys.getsizeof(block), "death_state": MemoryError.__name__}
    except MemoryError:
        return {"state": "DIED", "death_state": "MemoryError"}


def numeric_layer(fi=None):
    fi = fi or sys.float_info
    checks = {
        "radix_2": fi.radix == 2,
        "mant_dig_53": fi.mant_dig == 53,
        "nan_ne_nan": float("nan") != float("nan"),
        "overflow_to_inf": fi.max * 10 == float("inf"),
        "neg_zero_eq_zero": -0.0 == 0.0,
        "sum_not_exact": (0.1 + 0.2) != 0.3 and math.isclose(0.1 + 0.2, 0.3),
    }
    ok = all(checks.values())
    return {"state": "IEEE_754_BINARY64" if ok else "VIOLATED", "checks": checks}


def scheduler_layer(rounds=2000):
    lock = threading.Lock()
    box = {"n": 0}

    def work():
        for _ in range(rounds):
            with lock:
                box["n"] += 1
    ts = [threading.Thread(target=work) for _ in range(2)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return {"state": "HONOURED" if box["n"] == 2 * rounds else "VIOLATED", "count": box["n"], "expected": 2 * rounds}


def compiler_layer(source):
    code = compile(source, "<target>", "exec")
    objs, instrs = 0, 0
    stack = [code]
    while stack:
        c = stack.pop()
        objs += 1
        instrs += len(c.co_code) // 2
        stack.extend(k for k in c.co_consts if hasattr(k, "co_code"))
    return {"state": "COMPILED", "code_objects": objs, "instructions": instrs}


def network_layer():
    a, b = socket.socketpair()
    try:
        a.sendall(b"0123456789" * 100)
        got = b""
        while len(got) < 1000:
            got += b.recv(4096)
        return {"state": "IN_ORDER" if got == b"0123456789" * 100 else "VIOLATED", "bytes": len(got)}
    finally:
        a.close()
        b.close()


def hardware_layer():
    packed = struct.pack("<d", 3.5)
    back = struct.unpack("<d", packed)[0]
    return {"state": "ROUND_TRIP" if back == 3.5 else "VIOLATED", "byteorder": sys.byteorder,
            "machine": platform.machine() or "UNKNOWN"}


def chain_demo(faithful=True):
    """Three links; each takes the prior output as given. One link that
    breaks its contract and the chain has no output."""
    def link1():
        return {"n": 3}

    def link2(x):
        return {"n": x["n"] * 2} if faithful else "not a dict"

    def link3(x):
        return x["n"] + 1
    try:
        return {"state": "OUTPUT", "value": link3(link2(link1()))}
    except (TypeError, KeyError) as e:
        return {"state": "NO_OUTPUT", "broken_link": "link2", "reason": type(e).__name__}


def run(target_path):
    with open(target_path, encoding="utf-8") as f:
        source = f.read()
    layers = {
        "contracts": contracts(source),
        "memory": memory_layer(),
        "numeric": numeric_layer(),
        "scheduler": scheduler_layer(),
        "compiler": compiler_layer(source),
        "network": network_layer(),
        "hardware": hardware_layer(),
    }
    violated = [k for k, v in layers.items() if v.get("state") in ("VIOLATED", "DIED")]
    return {"target": os.path.basename(target_path),
            "sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
            "layers": layers, "violated": violated,
            "state": "SUBSTRATE_HOLDS" if not violated else "SUBSTRATE_ASSUMPTION_VIOLATED",
            "demo_faithful": chain_demo(True), "demo_planted": chain_demo(False)}


def render(res):
    L = res["layers"]
    c = L["contracts"]
    lines = ["P2 substrate check  target=%s  sha256=%s" % (res["target"], res["sha256"][:16]),
             "state       %s%s" % (res["state"], ("  layers=" + ",".join(res["violated"])) if res["violated"] else ""),
             "contracts   %d call sites, %d verified (proxy, over-reads), %d unverified (floor)   [CHOICE 8]"
             % (c["total_callsites"], c["verified_proxy"], c["unverified_floor"]),
             "memory      %s  %d bytes granted; death state %s; no negotiation step" % (L["memory"]["state"], L["memory"].get("bytes", 0), L["memory"]["death_state"]),
             "numeric     %s  %s" % (L["numeric"]["state"], " ".join(k for k, v in L["numeric"]["checks"].items() if v)),
             "scheduler   %s  %d of %d under lock" % (L["scheduler"]["state"], L["scheduler"]["count"], L["scheduler"]["expected"]),
             "compiler    %s  %d code objects, %d instructions" % (L["compiler"]["state"], L["compiler"]["code_objects"], L["compiler"]["instructions"]),
             "network     %s  %d bytes over a local socketpair (no egress)" % (L["network"]["state"], L["network"]["bytes"]),
             "hardware    %s  byteorder=%s machine=%s" % (L["hardware"]["state"], L["hardware"]["byteorder"], L["hardware"]["machine"]),
             "chain demo  faithful -> %s value=%s;  one planted link -> %s (%s)"
             % (res["demo_faithful"]["state"], res["demo_faithful"].get("value"), res["demo_planted"]["state"], res["demo_planted"].get("reason")),
             "named parts (data, not adversarial):"]
    for name, mech in NAMED_PARTS:
        lines.append("  %-21s %s" % (name, mech))
    lines.append("existence proof: this report exists; every unverified contract above held on the way to it")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("p2_substrate.py holds no checks; run python3 selftest.py\n")
        return 2
    target = argv[argv.index("--target") + 1] if "--target" in argv else os.path.abspath(__file__)
    print(render(run(target)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
