#!/usr/bin/env python3
"""
make_checklist.py - render CHECKLIST.md from triad.json.

CC0-1.0. Stdlib only. triad.json is the single source of truth;
CHECKLIST.md is generated, never hand-edited. Same arrangement as
../reasoning-gate/make_docs.py.

    python3 make_checklist.py [triad.json] [CHECKLIST.md]
"""

import json
import sys

READABLE_MARK = {
    "always": "[readable]",
    "usually": "[readable]",
    "sometimes": "[partial ]",
    "self-report only": "[DECLARED]",
}


def _wrap(text, indent, width=66):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return ("\n" + " " * indent).join(lines)


def render(spec):
    out = []
    out.append("# INTERIOR CALIBRATION CHECKLIST")
    out.append("")
    out.append("Generated from `triad.json`. Do not hand-edit.")
    out.append("")
    out.append("License: %s" % spec.get("license", "CC0-1.0"))
    out.append("")
    out.append(_wrap(spec["principle"], 0))
    out.append("")
    out.append("Origin: %s" % _wrap(spec.get("origin", ""), 8))
    out.append("")

    out.append("## The three agents")
    out.append("")
    out.append("```")
    for a in spec["agents"]:
        out.append("%-11s %s" % (a, _wrap(spec["agent_meaning"][a], 12)))
    out.append("```")
    out.append("")

    out.append("## Dials")
    out.append("")
    out.append("Each agent carries its own dial. The dial is a vector, not a")
    out.append("scalar.")
    out.append("")
    for a in spec["agents"]:
        out.append("### %s" % a)
        out.append("")
        out.append("```")
        for level in ("low", "medium", "high"):
            out.append("%-8s %s" % (level, spec["dials"][a][level]))
        out.append("```")
        out.append("")

    out.append("## Pre-run checklist")
    out.append("")
    out.append("Tick each box before the run. A box you cannot read is not a")
    out.append("box you tick -- mark it `?` and carry the flag forward into")
    out.append("the pedigree.")
    out.append("")
    for a in spec["agents"]:
        out.append("### %s" % a)
        out.append("")
        for c in spec["calibration_checks"][a]:
            mark = READABLE_MARK.get(c.get("readable", ""), "[        ]")
            out.append("- [ ] `%s` %s %s" % (c["id"], mark,
                                             _wrap(c["check"], 6)))
            if c.get("note"):
                out.append("      > %s" % _wrap(c["note"], 8))
        out.append("")

    out.append("**On readability.** %s" % _wrap(spec["readability_note"], 0))
    out.append("")

    out.append("## Shadow protocol")
    out.append("")
    sp = spec["shadow_protocol"]
    out.append("```")
    out.append("purpose   %s" % _wrap(sp["purpose"], 10))
    out.append("design    %s" % _wrap(sp["design"], 10))
    out.append("sealing   %s" % _wrap(sp["sealing"], 10))
    out.append("null      %s" % _wrap(sp["null_required"], 10))
    out.append("blind to  %s" % _wrap(sp["blind_spot"], 10))
    out.append("```")
    out.append("")
    for key in ("design_note", "sealing_note"):
        out.append("> %s" % _wrap(sp[key], 2))
        out.append("")

    if "panel_independence" in sp:
        pi = sp["panel_independence"]
        out.append("### Panel independence")
        out.append("")
        out.append("```")
        out.append("rule    %s" % _wrap(pi["rule"], 8))
        out.append("N_eff   %s" % _wrap(pi["n_eff"], 8))
        out.append("```")
        out.append("")
        for key in ("why", "v1_gap", "without_a_human",
                    "what_a_human_still_uniquely_supplies"):
            out.append("> **%s** — %s"
                       % (key.replace("_", " "), _wrap(pi[key], 2)))
            out.append("")

    if "consensus_denominator" in sp:
        cd = sp["consensus_denominator"]
        out.append("### Consensus denominator")
        out.append("")
        out.append("```")
        out.append("v1 says   %s" % _wrap(cd["v1_rule"], 10))
        out.append("verdict   %s" % _wrap(cd["verdict"], 10))
        out.append("use       %s" % _wrap(cd["correct_denominator"], 10))
        out.append("```")
        out.append("")
        out.append("> %s" % _wrap(cd["why"], 2))
        out.append("")

    out.append("## Skip conditions")
    out.append("")
    sc = spec["skip_conditions"]
    out.append("```")
    out.append("rule   %s" % _wrap(sc["rule"], 7))
    out.append("test   %s" % _wrap(sc["test"], 7))
    out.append("```")
    out.append("")
    out.append("> %s" % _wrap(sc["note"], 2))
    out.append("")

    out.append("## Pedigree")
    out.append("")
    pf = spec["pedigree_fields"]
    out.append("Every number carries the chain that produced it.")
    out.append("")
    out.append("```")
    out.append("required  %s" % _wrap(", ".join(pf["required"]), 10))
    out.append("layer     %s" % pf["layer"])
    out.append("```")
    out.append("")
    out.append("> %s" % _wrap(pf["layer_note"], 2))
    out.append("")

    if spec.get("gate_mapping_note"):
        out.append("## Gate mapping")
        out.append("")
        out.append("> %s" % _wrap(spec["gate_mapping_note"], 2))
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "triad.json"
    dst = sys.argv[2] if len(sys.argv) > 2 else "CHECKLIST.md"
    with open(src) as fh:
        spec = json.load(fh)
    with open(dst, "w") as fh:
        fh.write(render(spec))
    print("wrote %s from %s" % (dst, src))
