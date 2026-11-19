"""DRAFT, not merged: per-folder fields proposed for concept_map.json (see CONCEPT_MAP_SCHEMA_DRAFT.md).

Writes folder_fields.draft.json beside this file. Computes only the fields a script can derive and says how;
every other field is null (not recorded). Nothing is written to concept_map.json.
Run from anywhere: python3 folder_fields_draft.py [--check]
"""
import ast, json, os, sys, warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(HERE, "folder_fields.draft.json")
STD = set(sys.stdlib_module_names)
RULES = {
    "deps": "top-level imports (ast, absolute only) in the folder's .py files, minus stdlib and minus any module name defined as a .py file or package anywhere in the repo, so the list mixes third-party packages with modules imported but not present in this tree (e.g. a cross-repo source file); 'stdlib' when none; an import inside try/except is still counted",
    "claim_table": "'yes' if a file whose name starts with CLAIM (CLAIM_TABLE, CLAIMS) is anywhere in the folder, else 'no'; 'void' is not assigned by the script (its meaning is the owner's)",
    "refutation_protocol": "'yes' if the token REFUTATION_PROTOCOL occurs in a .md/.py/.json file of the folder, else 'no' (a mention, not a check that the protocol is followed)",
    "self_exclusion": "the folder holding this draft (blind-reader-void12/studies/drafts/) is not scanned: it names the tokens it counts, so scanning it would count itself",
    "selftest": "'yes' if the string --selftest occurs in a .py file of the folder, else 'no' (a mention; refusals of --selftest also count; nothing is run)",
}
NULL_FIELDS = ["purpose", "read_first", "first_file"]

def local_modules():
    names = set()
    for r, ds, fs in os.walk(ROOT):
        ds[:] = [d for d in ds if not d.startswith(".")]
        names |= {f[:-3] for f in fs if f.endswith(".py")}
        names |= {d for d in ds if os.path.exists(os.path.join(r, d, "__init__.py"))}
    return names

def folder(d, local):
    deps, ct, rp, st, parse_fail = set(), "no", "no", "no", []
    for r, ds, fs in os.walk(os.path.join(ROOT, d)):
        ds[:] = [x for x in ds if not x.startswith(".")]
        if os.path.abspath(r) == HERE: continue      # this draft names the tokens it counts; scanning it would count itself
        for f in fs:
            p = os.path.join(r, f)
            if f.startswith("CLAIM"): ct = "yes"
            if not f.endswith((".md", ".py", ".json")): continue
            txt = open(p, encoding="utf-8", errors="ignore").read()
            if "REFUTATION_PROTOCOL" in txt: rp = "yes"
            if not f.endswith(".py"): continue
            if "--selftest" in txt: st = "yes"
            try: tree = ast.parse(txt)
            except SyntaxError: parse_fail.append(os.path.relpath(p, ROOT)); continue
            for n in ast.walk(tree):
                mods = [a.name for a in n.names] if isinstance(n, ast.Import) else \
                       [n.module] if isinstance(n, ast.ImportFrom) and n.level == 0 and n.module else []
                for m in mods:
                    top = m.split(".")[0]
                    if top not in STD and top not in local: deps.add(top)
    v = {k: None for k in NULL_FIELDS}
    v.update({"deps": sorted(deps) or "stdlib", "claim_table": ct, "refutation_protocol": rp, "selftest": st,
              "residue_register_ref": "blind-reader-void12/studies/RESIDUE_REGISTER.md" if d == "blind-reader-void12" else None,
              "provenance": {"deps": "SCRIPT_DERIVED", "claim_table": "SCRIPT_DERIVED", "refutation_protocol": "SCRIPT_DERIVED",
                             "selftest": "SCRIPT_DERIVED", "residue_register_ref": "CODER_INFERRED" if d == "blind-reader-void12" else None,
                             "purpose": None, "read_first": None, "first_file": None}})
    if parse_fail: v["parse_failures"] = parse_fail
    return v

def build():
    local = local_modules()
    dirs = sorted(x for x in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, x)) and not x.startswith("."))
    return {"status": "DRAFT, not merged into concept_map.json", "rules": RULES,
            "null_means": "not recorded; no default", "folders": {d: folder(d, local) for d in dirs}}

if __name__ == "__main__":
    data = json.dumps(build(), indent=1, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        same = os.path.exists(OUT) and open(OUT, encoding="utf-8").read() == data
        print("folder_fields --check: " + ("identical" if same else "WOULD CHANGE")); sys.exit(0 if same else 1)
    open(OUT, "w", encoding="utf-8").write(data)
    d = json.loads(data)["folders"]
    print("folders", len(d), "| non-stdlib", sum(v["deps"] != "stdlib" for v in d.values()),
          "| claim_table yes", sum(v["claim_table"] == "yes" for v in d.values()),
          "| refutation_protocol yes", sum(v["refutation_protocol"] == "yes" for v in d.values()),
          "| selftest yes", sum(v["selftest"] == "yes" for v in d.values()))
