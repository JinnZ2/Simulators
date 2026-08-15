#!/usr/bin/env python3
"""
make_docs.py - render GUARDS.md from guards.json.

CC0-1.0. Stdlib only. guards.json is the single source of truth;
GUARDS.md is generated, never hand-edited.

    python3 make_docs.py [guards.json] [GUARDS.md]
"""

import json
import sys

STAGE_ORDER = ["pre", "mid", "post"]
STAGE_TITLE = {
    "pre": "PRE - before the sim executes",
    "mid": "MID - while quantities are emitted",
    "post": "POST - at report assembly",
}


def _stages(guard):
    """`stage` may be a single string or a list -- a guard can fire twice."""
    st = guard.get("stage", [])
    return [st] if isinstance(st, str) else list(st)


def render(reg):
    out = []
    out.append("# GUARDS")
    out.append("")
    out.append("Generated from `guards.json`. Do not hand-edit.")
    out.append("")
    out.append("License: %s" % reg.get("license", "CC0-1.0"))
    out.append("")
    out.append("Default is deny. A sim that does not declare gets no")
    out.append("output; an untagged quantity is not recorded; a ratio")
    out.append("across unlike objects is void; a claim without named")
    out.append("support does not enter the conclusion.")
    out.append("")
    out.append("Origin: %s" % reg.get("origin", ""))
    out.append("")

    out.append("## Layers")
    out.append("")
    out.append("```")
    for layer in reg.get("layers", []):
        out.append("%-11s %s" % (layer, reg["layer_meaning"][layer]))
    out.append("```")
    out.append("")
    out.append("No promotion between layers without an explicit,")
    out.append("justified step.")
    out.append("")

    for stage in STAGE_ORDER:
        guards = [g for g in reg["guards"] if stage in _stages(g)]
        if not guards:
            continue
        out.append("## %s" % STAGE_TITLE[stage])
        out.append("")
        for g in guards:
            out.append("### %s - %s" % (g["id"], g["name"]))
            out.append("")
            if len(_stages(g)) > 1:
                out.append("Also fires at: %s"
                           % ", ".join(x for x in _stages(g) if x != stage))
                out.append("")
            out.append("```")
            out.append("rule    %s" % _wrap(g["rule"], 8))
            out.append("denies  %s" % _wrap(g["fail_message"], 8))
            out.append("because %s" % _wrap(g["rationale"], 8))
            out.append("```")
            if g.get("examples"):
                out.append("")
                for ex in g["examples"]:
                    out.append("- %s" % ex)
            out.append("")

    out.append("## Reading the log")
    out.append("")
    out.append("```")
    out.append("gate_<SIM>.json")
    out.append("  declaration               what was promised before the run")
    out.append("  expected / observed       the divergence, logged either way")
    out.append("  generator_level_quantities  numbers that are properties of")
    out.append("                            the code, not of any system")
    out.append("  voided_ratios             computed, then refused")
    out.append("  claims[].status           supported | unsupported | qualified")
    out.append("  findings                  guards that fired in non-strict mode")
    out.append("```")
    out.append("")
    return "\n".join(out)


def _wrap(text, indent, width=64):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    pad = "\n" + " " * indent
    return pad.join(lines)


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "guards.json"
    dst = sys.argv[2] if len(sys.argv) > 2 else "GUARDS.md"
    with open(src) as fh:
        reg = json.load(fh)
    with open(dst, "w") as fh:
        fh.write(render(reg))
    print("wrote %s from %s" % (dst, src))
