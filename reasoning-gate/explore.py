# explore.py  — CC0-1.0, stdlib only
# widens a sim declaration. emits candidates, ranks NOTHING,
# refuses to converge. applies[] is yours to fill.
import json, sys

MOVES = {
 "instrument": [
  "change the sampling grid: finer, coarser, non-uniform, aligned to expected feature locations",
  "change the window/aperture and re-run: what moves is instrument, what stays is not",
  "change the estimator for the same quantity (fit vs local slope vs direct count)",
  "change sample size by 4x: which numbers move with N",
  "check dynamic range: is the floor a real floor or the noise of this apparatus",
  "run the apparatus on a case with a known answer",
 ],
 "statistic": [
  "name a second statistic that answers the same question by a different route",
  "name a statistic that would FAIL if the hypothesis were true",
  "state what this statistic is blind to by construction",
  "state what would change the number without changing the system",
 ],
 "physical": [
  "dimensional check: do both sides carry the same units and the same object",
  "limiting case: does it reduce correctly at the trivial limit",
  "order of magnitude from an independent route (back-of-envelope, different physics)",
  "published range for this quantity in this system: does it bracket the result",
  "what physical measurement outside this script could contradict it",
  "is the quantity a property of the modelled system, or of the code",
 ],
 "disposition": [
  "if this result had surprised me, what control would I have added? add it now",
  "what is the cheapest result to obtain here, and am I obtaining it",
  "which step is most fragile, and does it have the least scaffolding",
  "what did I stop testing once the first clean number appeared",
  "restate the live question: is this still the version being tested",
 ],
}

def explore(declaration, kinds=None, out=None, sim_id=None):
    """`declaration` may be a gate report or the declaration block inside
    one. sim_id lives at the top level of a report, not in the declaration,
    so accept it from either place."""
    kinds = kinds or list(MOVES)
    decl = declaration.get("declaration", declaration)
    sim_id = sim_id or declaration.get("sim_id") or decl.get("sim_id")
    cands = []
    for k in kinds:
        for i, m in enumerate(MOVES[k]):
            cands.append({"id": "%s-%02d" % (k[:4].upper(), i+1),
                          "kind": k, "probe": m,
                          "applies": None,      # yes | no | unclear
                          "note": ""})
    doc = {"sim": sim_id,
           "question": decl.get("question"),
           "statistic": decl.get("statistic"),
           "candidates": cands,
           "ordering": "arbitrary. not a ranking. not a shortest path."}
    if out:
        with open(out, "w") as fh:
            json.dump(doc, fh, indent=2)
    for c in cands:
        print("[ ] %-8s %s" % (c["id"], c["probe"]))
    print("\n%d candidates, unranked. fill applies= yes|no|unclear." % len(cands))
    return doc

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as fh:
            d = json.load(fh)
    else:
        d = {}
    explore(d, out="explore_%s.json" % (d.get("sim_id") or "x"))
