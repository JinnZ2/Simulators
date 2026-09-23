# faces.py -- WO-4: the seven faces, read out of the order, put through the
# invariant, plus the term gap as a registered state.
#
# The faces are PARSED from WORK_ORDER.md at call time and never retyped
# here. A document lacking the section raises rather than returning an empty
# list -- an empty face list would read as a census.
#
# The face -> structure mapping is a DECLARED READING BY THIS AUDIT, not a
# derivation from the order. Each carries a basis quoting the order's own
# line for it. [CHOICE 5]
#
# Standing limit, stated before the numbers: the invariant in invariant.py
# was abstracted FROM these seven faces. A high fit rate over them is close
# to a tautology and is not evidence for the invariant. The test that would
# be evidence is the order's own step 2 -- an eighth face supplied by
# someone who did not write the seven -- and it is NOT_RUN here, because
# this session is the same party that holds them.
#
# CONSTRUCTED. Nothing here is a measurement of any system.
#
# stdlib only, parses under 3.9, ASCII.

import os
import re
import sys

import invariant as inv

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ORDER = os.path.join(HERE, "WORK_ORDER.md")

EM = "\u2014"
ARROW = "\u2192"

CHOICES = {
    5: "the face -> structure mapping is a declared reading by this audit; "
       "each structure carries the order's own line as its basis.",
    6: "a cross-reference resolves only on a folder path that exists AND a "
       "content marker inside it; a name occurring in prose is not a "
       "resolution.",
    7: "face 6 is declared with the environment's scope UNDECLARED, on the "
       "order's own stated reason ('you cannot list in advance which "
       "binaries will turn out false'). The NOT_EVALUABLE verdict falls "
       "out of that declaration rather than being stipulated.",
    8: "the term-gap search (order step 3) is NOT_RUN and no language is "
       "scored; the status per language is UNSEARCHED, which is not "
       "'no term exists'.",
}


class OrderUnparsed(Exception):
    pass


def order_text(path=ORDER):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def faces(path=ORDER):
    """Parse the numbered faces out of '## Faces identified'.

    Returns [(n, label, text)] with label the part before the em dash.
    """
    txt = order_text(path)
    m = re.search(r"^## Faces identified\s*$(.*?)^## ", txt,
                  re.S | re.M)
    if not m:
        raise OrderUnparsed("%s: no '## Faces identified' section" % path)
    body = m.group(1)
    out = []
    cur = None
    for line in body.splitlines():
        h = re.match(r"^(\d+)\.\s+(.*)$", line)
        if h:
            if cur:
                out.append(cur)
            cur = [int(h.group(1)), h.group(2).strip()]
        elif cur is not None and line.strip():
            cur[1] = cur[1] + " " + line.strip()
        elif cur is not None and not line.strip():
            pass
    if cur:
        out.append(cur)
    if not out:
        raise OrderUnparsed("%s: section present, no numbered faces" % path)
    res = []
    for n, text in out:
        label = text.split(EM)[0].strip() if EM in text else text.strip()
        res.append((n, label, text))
    return res


def cross_refs(path=ORDER):
    """Which faces name a companion work order, from the arrow markers."""
    out = {}
    for n, _label, text in faces(path):
        m = re.search(r"%s\s*(WO-\d+)" % ARROW, text)
        if m:
            out[n] = m.group(1)
    return out


# --- where the companion orders landed in this tree --------------------
# [CHOICE 6] path plus a content marker; a mention in prose is not a
# resolution.

COMPANIONS = {
    "WO-1": ("chain-position", "chain_position.py"),
    "WO-2": ("quiet-aggregation", "WORK_ORDER.md"),
    "WO-3": ("terminal-crossing", "crossing_rate.py"),
}


def companion_state(wo, root=ROOT):
    ent = COMPANIONS.get(wo)
    if ent is None:
        return "UNKNOWN_COMPANION"
    folder, marker = ent
    d = os.path.join(root, folder)
    if not os.path.isdir(d):
        return "ABSENT"
    if not os.path.exists(os.path.join(d, marker)):
        return "FOLDER_NO_MARKER"
    return "RESOLVED"


# --- declared structures, one per face ---------------------------------

def _S():
    c = inv.component
    s = inv.structure
    out = {}
    out[1] = s(
        "face1_container",
        [c("container_i", ["own_inputs", "own_outputs"]),
         c("container_j", ["own_inputs", "own_outputs"])],
        ["position_in_chain"],
        "order face 1: 'each container locally correct by construction, "
        "the join unowned'",
    )
    out[2] = s(
        "face2_regulation",
        [c("rule_a", ["condition_a"]), c("rule_b", ["condition_b"])],
        ["joint_admissible_set"],
        "order face 2: 'every rule individually valid, exclusion arising "
        "from the unowned join. Nobody wrote the exclusion and nobody can "
        "find it from inside any single rule'",
    )
    out[3] = s(
        "face3_quiet_failure",
        [c("reporter_a", ["signal_a"]), c("reporter_b", ["signal_b"])],
        ["signal_a", "signal_b"],
        "order face 3: 'signals present and reported, aggregation nobody's "
        "job, failure then called sudden'",
    )
    out[4] = s(
        "face4_boundary",
        [c("boundary_holder", ["cost_inside_boundary"]),
         c("downstream_bearer", ["cost_borne_locally"])],
        ["cost_crossing_boundary"],
        "order face 4: 'boundary drawn where the consequences are not'",
    )
    out[5] = s(
        "face5_air_gap",
        [c("channel_a_owner", ["channel_a_state"]),
         c("claimant", ["channel_a_state"])],
        ["channel_a_state", "channel_b_state"],
        "order face 5: 'a claim about one channel treated as a claim about "
        "all channels'. Weakest fit in the set: it reads as an unowned "
        "join only because there is no component for the unconsidered "
        "channel, which is why the overclaim goes unchecked",
    )
    out[6] = s(
        "face6_frog",
        [c("presenter", ["option_1", "option_2"]),
         c("environment", inv.UNDECLARED)],
        ["affordances_beyond_the_presentation"],
        "order face 6, declared per [CHOICE 7] on the order's own reason: "
        "'You cannot list in advance which binaries will turn out false, "
        "because that is precisely what the environment supplies'",
    )
    out[7] = s(
        "face7_description",
        [c("institution", ["description"]),
         c("conformance_auditor", ["practice_matches_description"])],
        ["description", "referent"],
        "order face 7: 'the description DECOUPLES from what actually "
        "happens, at some time period, and the institution then defends "
        "the description'",
    )
    return out


def structures():
    return _S()


def fit(path=ORDER):
    """One row per parsed face: verdict, whether the shape holds, companion."""
    st = _S()
    refs = cross_refs(path)
    rows = []
    for n, label, _text in faces(path):
        s = st.get(n)
        if s is None:
            rows.append({"n": n, "label": label, "sid": None,
                         "verdict": "NO_STRUCTURE_DECLARED",
                         "shape_holds": None, "companion": refs.get(n),
                         "companion_state": None})
            continue
        r = inv.report(s)
        wo = refs.get(n)
        rows.append({
            "n": n, "label": label, "sid": r["sid"],
            "verdict": r["verdict"], "shape_holds": r["shape_holds"],
            "coverage": r["coverage"],
            "companion": wo,
            "companion_state": companion_state(wo) if wo else None,
        })
    return rows


def fit_counts(path=ORDER):
    rows = fit(path)
    out = {"n_faces": len(rows), "shape_holds": 0, "not_evaluable": 0,
           "no_structure": 0, "by_verdict": {}}
    for r in rows:
        v = r["verdict"]
        out["by_verdict"][v] = out["by_verdict"].get(v, 0) + 1
        if r["shape_holds"]:
            out["shape_holds"] += 1
        if v == inv.NOT_EVALUABLE:
            out["not_evaluable"] += 1
        if v == "NO_STRUCTURE_DECLARED":
            out["no_structure"] += 1
    return out


# --- the term gap ------------------------------------------------------

UNSEARCHED = "UNSEARCHED"
NAMED_ELSEWHERE = "NAMED_ELSEWHERE"
CHECKED_ADJACENT = "CHECKED_ADJACENT"

# The vocabulary the order records itself as having checked, with the
# order's own finding on each. Carried, not re-checked here.
ADJACENT = ("drift", "lossy encoding", "map-territory")

# Step 3 names a census method that returned 25 terms for a different
# structure. No language is scored here and none is searched. [CHOICE 8]
STEP3_STATUS = {
    "search_run": False,
    "reason": "the order's step 3 is a cross-language vocabulary search; "
              "the sources are not reachable from this environment (egress "
              "is an allowlist) and no language is scored from memory",
    "expected_by_order": "named_elsewhere rather than unnamed",
    "languages_scored": 0,
}


def term_status():
    return {
        "coined_here": False,
        "adjacent_checked_by_order": ADJACENT,
        "adjacent_status": CHECKED_ADJACENT,
        "cross_language": UNSEARCHED,
        "step3": dict(STEP3_STATUS),
    }


def code_without_a_term(module=inv):
    """The order's strong claim, checked against this folder.

    'Because there is no good word, NO PROCEDURES CAN BE MADE AROUND IT AND
    NO CODE CAN BE MADE AROUND IT.'

    Returns the state of that claim as measured here: a checkable predicate
    over the structure exists, was built with no term coined, and returns a
    verdict. Reports WHAT the missing term does block separately, using the
    order's own stated mechanism.
    """
    ctl = module.controls()
    reached = sorted(set(module.verdict(s) for s in ctl))
    return {
        "predicate_exists": True,
        "verdicts_reachable": len(reached),
        "verdicts_declared": len(module.VERDICTS),
        "term_coined": False,
        "strong_claim": "REFUTED_HERE",
        "strong_claim_scope": "one structure, one folder; it does not "
                              "establish that every structure lacking a "
                              "term is codeable",
        "surviving_claim": "what the missing term blocks is transmission, "
                           "not code. The order states the mechanism two "
                           "sections on: with a term a claim is a REPORT "
                           "and status is inherited; without one the same "
                           "content is rebuilt across several "
                           "sentences and reads as a PROPOSAL.",
        "mechanism_tested_here": False,
    }


# --- order step 2 ------------------------------------------------------

STEP2 = {
    "run": False,
    "reason": "adversarial face-finding takes a second party. This session "
              "holds the seven faces and is not the party to supply an "
              "eighth; a face produced here would be the same hand "
              "widening its own set.",
    "cost": "the order: 'needs no resources and is the cheapest test in "
            "the whole set'",
    "candidate_corpus": "folders in this tree built from unrelated "
                        "deliveries, each carrying a documented mechanism; "
                        "naming which of them instance the structure is a "
                        "reading and is also this session's, so it is "
                        "named as a corpus and not scored",
}


def _fmt(v):
    return "--" if v is None else str(v)


def render():
    lines = []
    lines.append("WO-4 FACES -- parsed from WORK_ORDER.md, put through the")
    lines.append("invariant. CONSTRUCTED; the mapping is a declared reading.")
    lines.append("")
    lines.append("READ THIS FIRST: the invariant was abstracted from these")
    lines.append("seven faces, so their fit is near-tautological and is NOT")
    lines.append("evidence for it. The evidence test is the order's step 2,")
    lines.append("and step 2 is NOT_RUN.")
    lines.append("")
    lines.append("%-3s %-34s %-17s %-6s %s"
                 % ("n", "face", "verdict", "holds", "companion"))
    for r in fit():
        comp = "--"
        if r["companion"]:
            comp = "%s %s" % (r["companion"], r["companion_state"])
        lab = r["label"]
        if len(lab) > 33:
            lab = lab[:30] + "..."
        lines.append("%-3s %-34s %-17s %-6s %s"
                     % (r["n"], lab, r["verdict"],
                        _fmt(r["shape_holds"]), comp))
    c = fit_counts()
    lines.append("")
    lines.append("faces parsed: %d   shape holds: %d   not evaluable: %d"
                 % (c["n_faces"], c["shape_holds"], c["not_evaluable"]))
    lines.append("")
    lines.append("TERM GAP")
    t = term_status()
    lines.append("  coined here:        %s" % t["coined_here"])
    lines.append("  adjacent vocabulary %s (%s)"
                 % (t["adjacent_status"], ", ".join(t["adjacent_checked_by_order"])))
    lines.append("  cross-language:     %s, languages scored %d"
                 % (t["cross_language"], t["step3"]["languages_scored"]))
    lines.append("  order step 3:       NOT_RUN -- %s"
                 % t["step3"]["reason"])
    lines.append("")
    k = code_without_a_term()
    lines.append("CAN CODE BE BUILT WITHOUT A TERM")
    lines.append("  predicate built:    %s (%d of %d verdicts reachable)"
                 % (k["predicate_exists"], k["verdicts_reachable"],
                    k["verdicts_declared"]))
    lines.append("  term coined:        %s" % k["term_coined"])
    lines.append("  strong claim:       %s" % k["strong_claim"])
    lines.append("  scope:              %s" % k["strong_claim_scope"])
    lines.append("  surviving claim:    %s" % k["surviving_claim"])
    lines.append("  mechanism tested:   %s" % k["mechanism_tested_here"])
    lines.append("")
    lines.append("ORDER STEP 2 (adversarial face-finding): NOT_RUN")
    lines.append("  %s" % STEP2["reason"])
    return "\n".join(lines) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "faces is a library and a render; the checks live in "
            "unowned-join/test_unowned.py -- run "
            "python3 unowned-join/test_unowned.py\n")
        return 2
    if "--choices" in argv:
        for n in sorted(CHOICES):
            sys.stdout.write("[CHOICE %d] %s\n" % (n, CHOICES[n]))
        return 0
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
