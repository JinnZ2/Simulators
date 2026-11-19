"""make_key_a1.py: builds scoring/key_v2_a1.json from scoring/key_v2.json, the rule, and the owner's rulings.

Every changed list is DERIVED, not typed: derive_specific.derive_all() reads the packet's sources (numcheck run on its corpus, the cplay
constructors run, the TAF code parsed) and returns, for each term, a list or two routes that disagree. Two owner rulings (2026-11-19) settle
the two terms whose routes disagree:
  taf cplay:CRASHED -> the instance is the Reading with status CRASHED     (route "Reading fields a rule requires for CRASHED")
  taf:UNKNOWN       -> undetermined; the packet stays unchanged            (no route chosen; the list is None)
The script then checks that the ONLY lists that move against key v2 are the expected four (T08, T09, T10, T12) and stops if any other moves.
Nothing else in key v2 changes: not clusters, labels, slots_carried, the pair list, or key_v2.json itself.

Run (from anywhere):  FORMULA_AUDIT_DIR=<formula-audit checkout holding the packet's numcheck/check.py>  python3 make_key_a1.py
"""
import hashlib, importlib.util, json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.abspath(os.path.join(HERE, ".."))
FA = os.environ.get("FORMULA_AUDIT_DIR")
spec = importlib.util.spec_from_file_location("derive_specific", os.path.join(BASE, "amendment_options", "derive", "derive_specific.py"))
DS = importlib.util.module_from_spec(spec); spec.loader.exec_module(DS)
sys.path.insert(0, os.path.join(BASE, "scoring"))
import score_v2 as SV

RULINGS = {  # term_id -> route chosen by the owner, or None for "undetermined"
    "cplay:CRASHED": "Reading fields a rule requires for CRASHED",
    "taf:UNKNOWN": None,
}
EXPECTED_MOVES = {"T08", "T09", "T10", "T12"}
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()

def build(check_all, out_path=None):
    kp = os.path.join(BASE, "scoring", "key_v2.json")
    key = json.load(open(kp, encoding="utf-8"))
    T, AX, CL = DS.load_cplay()
    D = DS.derive_all(check_all, T, AX, CL)
    new = json.loads(json.dumps(key))
    byid = {t["term_id"]: i for i, t in key["terms"].items()}
    moves = {}
    for tid, i in byid.items():
        d = D[tid]
        if tid in RULINGS:
            route = RULINGS[tid]
            lst = None if route is None else sorted(d["routes"][route], key=lambda x: d["routes"][route].index(x))
        else:
            lst = d["slots"]
        old = key["terms"][i]["slots_specific"]
        same = (lst is None and old is None) or (lst is not None and old is not None and set(lst) == set(old))
        if not same:
            moves[i] = (old, lst)
            new["terms"][i]["slots_specific"] = lst
    if set(moves) != EXPECTED_MOVES:
        sys.exit("unexpected set of moved lists: %s (expected %s)" % (sorted(moves), sorted(EXPECTED_MOVES)))
    note = {
        "T08": "a1: instance of CRASHED = the Reading with status CRASHED (owner ruling 2026-11-19); the fields a rule requires for CRASHED and for no other status (axes.py 59-60): exception, path.",
        "T09": "a1: undetermined (owner ruling 2026-11-19): the glossary defines UNKNOWN as a slot, the code builds a coverage entry, and the sources do not fix which is the instance; the packet is unchanged.",
        "T10": "a1: the rule (TAG + INDEPENDENCE) on the section record built in the one handler that assigns the GAP status: missing_path, error. exception_type is a function of error (unified_audit.py 486-488) and is dropped. slots_carried is not changed by a1.",
        "T12": "a1: the rule: reason is required by every non-verdict token (tokens.py), so it is not this term's alone; triggers is the parameter that is.",
    }
    for i, n in note.items():
        new["terms"][i]["derivation"] = new["terms"][i]["derivation"].rstrip() + " | " + n
    clusters = {i: t["cluster"] for i, t in new["terms"].items()}
    slots_spec = {i: t["slots_specific"] for i, t in new["terms"].items()}
    ts = SV.tiers_under(new, clusters, slots_spec, "specific")
    for p, t in zip(new["pairs"], ts): p["key_tier_specific"] = t
    new["meta"]["v"] = "2-a1"
    new["meta"]["key_v2_sha256"] = sha(kp)
    new["meta"]["scoring_rules"] = ["N1", "C1"]
    new["meta"]["a1_changes"] = sorted("%s.slots_specific" % i for i in moves) + ["pair key_tier_specific recomputed from the lists"]
    new["meta"]["a1_rulings"] = {"cplay:CRASHED": "instance = the Reading with status CRASHED", "taf:UNKNOWN": "undetermined; packet unchanged"}
    new["meta"]["a1_carried_statement"] = (
        "The key's slots_carried lists were derived from the record each term's source builds: for cplay terms by running the constructors and "
        "taking the record's fields (vars for plain objects, _fields for namedtuples); for numcheck and TAF terms by reading the record's keys "
        "in the source. Class attributes are not included. A reader who names a class attribute is scored as having an extra name.")
    text = json.dumps(new, indent=1, ensure_ascii=False)
    return new, moves, text

def main():
    pk = os.path.join(DS.SRC, "formula-audit", "numcheck", "check.py")
    if not FA or not os.path.exists(os.path.join(FA, "numcheck", "check.py")) or sha(pk) != sha(os.path.join(FA, "numcheck", "check.py")):
        sys.exit("FORMULA_AUDIT_DIR must hold a numcheck/check.py with the packet's sha256 (%s)" % sha(pk)[:16])
    sys.path.insert(0, FA)
    from numcheck.check import check_all
    new, moves, text = build(check_all)
    out = os.environ.get("KEY_A1_OUT", os.path.join(BASE, "scoring", "key_v2_a1.json"))
    open(out, "w", encoding="utf-8").write(text)
    print("wrote %s sha256 %s" % (out, hashlib.sha256(text.encode("utf-8")).hexdigest()))
    for i in sorted(moves): print("  %s %-28s %s -> %s" % (i, new["terms"][i]["term_id"], moves[i][0], moves[i][1]))
    print("pair tiers (specific): " + ", ".join("%s|%s %s" % (p["left"], p["right"], p["key_tier_specific"]) for p in new["pairs"]))

if __name__ == "__main__":
    main()
