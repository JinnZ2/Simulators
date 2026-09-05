
import json, glob, sys, collections

FOLDERS = set(l.strip() for l in open("/mnt/agents/output/survey/folders.txt") if l.strip())
REQ = {"folder","claim_id","source_file","falsifier_text","status","measured_as","scope_transform","downgrade_reason","notes"}
LEGAL = {"MEASURED","SCOPE-DIFFERENT","MISSING","UNKNOWN"}
errors, records = [], []

for path in sorted(glob.glob("/mnt/agents/output/survey/batches/batch_[0-7].jsonl")):
    for ln, line in enumerate(open(path), 1):
        line = line.strip()
        if not line: continue
        try: r = json.loads(line)
        except Exception as e:
            errors.append(f"{path}:{ln} bad JSON {e}"); continue
        missing_keys = REQ - set(r)
        if missing_keys: errors.append(f"{path}:{ln} missing keys {missing_keys}"); continue
        if r["status"] not in LEGAL: errors.append(f"{path}:{ln} illegal status {r['status']}")
        if r["folder"] not in FOLDERS: errors.append(f"{path}:{ln} unknown folder {r['folder']}")
        if r["status"]=="MEASURED":
            ma = r["measured_as"]
            if not isinstance(ma, dict) or not all(ma.get(k) for k in ("quantity","units","how_obtained")):
                errors.append(f"{path}:{ln} MEASURED w/o complete measured_as [{r['folder']}/{r['claim_id']}]")
        if r["status"]=="SCOPE-DIFFERENT":
            st = r["scope_transform"]
            if not isinstance(st, dict) or not all(st.get(k) for k in ("reference","maps_to","breaks_at")):
                errors.append(f"{path}:{ln} SCOPE-DIFFERENT w/o complete transform [{r['folder']}/{r['claim_id']}]")
        records.append(r)

covered = set(r["folder"] for r in records)
uncovered = FOLDERS - covered
print("records:", len(records), "| folders covered:", len(covered), "/", len(FOLDERS))
print("uncovered:", uncovered if uncovered else "none")
print("status counts:", dict(collections.Counter(r["status"] for r in records)))
print("ERRORS:", len(errors))
for e in errors[:40]: print(" -", e)
