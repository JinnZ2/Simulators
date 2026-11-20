"""Read-only branch reclass, run 2026-11-20. Run from a directory of bare clones (<repo>.git,
git clone --bare --filter=blob:none). Writes reclass.json there. Pushes nothing, deletes nothing.
SAFE_BRANCHES_2026-11-20.tsv = the rows whose proof is not NONE, archive/* branches left out."""
import subprocess, sys, os, json
def g(d,*a,ok=(0,)):
    p=subprocess.run(["git","-C",d]+list(a),capture_output=True,text=True)
    return p.returncode,p.stdout.strip()
rows=[]; skipped=[]
for d in sorted(x for x in os.listdir(".") if x.endswith(".git")):
    repo=d[:-4]
    rc,head=g(d,"symbolic-ref","--short","HEAD")
    rc,dtip=g(d,"rev-parse","--verify","-q","refs/heads/"+head)
    if rc: skipped.append((repo,"no default branch tip")); continue
    rc,dtree=g(d,"rev-parse",dtip+"^{tree}")
    rc,refs=g(d,"for-each-ref","--format=%(objectname) %(refname:short)","refs/heads")
    br=[l.split(" ",1) for l in refs.splitlines()]
    archives={n:s for s,n in br if n.startswith("archive/")}
    for sha,name in br:
        if name==head: continue
        proof=""; detail=""
        if g(d,"merge-base","--is-ancestor",sha,dtip)[0]==0:
            proof="ancestor"
        else:
            am=[n for n,s in archives.items() if n!=name and (s==sha or g(d,"merge-base","--is-ancestor",sha,s)[0]==0)]
            rc,mt=g(d,"merge-tree","--write-tree",dtip,sha)
            if rc==0 and mt.split("\n")[0]==dtree:
                proof="content-proof"; detail="merge-tree(default,tip) == default tree"
            elif am:
                proof="archive-match"; detail=am[0]
        _,ahead=g(d,"rev-list","--count",dtip+".."+sha)
        rows.append((repo,name,sha,head,dtip[:12],proof or "NONE",ahead,detail))
json.dump({"rows":rows,"skipped":skipped},open("reclass.json","w"))
import collections
print(len(rows),collections.Counter(r[5] for r in rows),skipped)
