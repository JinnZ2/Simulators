"""Round 3 claim checks: (1) JS-vs-Python cell differences, (2) the six DOIs via Crossref, (3) precursor.py line citations,
(4) the quoted strings of Part A against the files the author names (whitespace and comment markers normalised, so a quote
that wraps across lines still counts). Read-only.
Run: FA_DIR=formula-audit TAF_DIR=thermodynamic-accountability-framework SIM_DIR=Simulators SA_DIR=study-aperture python3 check_round3_claims.py"""
import json, math, os, re, urllib.request
FA = os.environ.get("FA_DIR", "formula-audit"); TAF = os.environ.get("TAF_DIR", "thermodynamic-accountability-framework")
SIM = os.environ.get("SIM_DIR", "Simulators"); SA = os.environ.get("SA_DIR", "study-aperture")
print("== 1. JS vs Python cells: z of the difference (two independent binomials, n=200, pooled p)")
cells = [("n60 w20 .5 planted", 55, 46), ("n60 w20 .5 white", 5, 3), ("n200 w20 .5 planted", 12, 14), ("n200 w20 .5 white", 0, 0),
         ("n70 w50 .5 planted", 98, 110), ("n70 w50 .5 white", 11, 7), ("n400 w50 .5 planted", 109, 109), ("n400 w50 .5 white", 0, 1),
         ("n150 w100 .5 planted", 161, 156), ("n150 w100 .5 white", 9, 11), ("n60 w20 .3 planted", 101, 87), ("n60 w20 .3 white", 11, 12)]
for name, a, b in cells:
    p = (a + b) / 400; se = math.sqrt(2 * 200 * p * (1 - p)) / 200 if 0 < p < 1 else 0
    print("  %-22s JS %3d  Py %3d  z=%s" % (name, a, b, "n/a" if se == 0 else "%.2f" % ((a - b) / 200 / se)))

print("== 2. DOIs via Crossref (title, container, volume, pages)")
for d in ["10.1371/journal.pone.0041010", "10.1098/rsif.2012.0125", "10.1038/s41467-023-43744-8", "10.1111/ele.12948", "10.1111/oik.05172", "10.1038/nature08227"]:
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/" + d, headers={"User-Agent": "reader-check"}), timeout=25))["message"]
        print("  %-30s %s | %s | vol %s pp %s | %s" % (d, (r.get("title") or ["?"])[0][:70], (r.get("container-title") or ["?"])[0][:28], r.get("volume"), r.get("page") or r.get("article-number"), ", ".join(a.get("family", "?") for a in r.get("author", [])[:3])))
    except Exception as e:
        print("  %-30s LOOKUP FAILED: %s" % (d, str(e)[:60]))

print("== 3. precursor.py line citations (item 8 and 4a)")
L = open(FA + '/glyph/precursor.py', encoding='utf-8').read().split('\n')
for a, b in ((122, 130), (199, 201), (210, 211)):
    for i in range(a, b + 1): print("  %d: %s" % (i, L[i - 1][:130]))

print("== 4. Part A quoted strings: present in the cited file? (normalised)")
def rd(p):
    try: return open(p, encoding='utf-8', errors='replace').read()
    except Exception: return ''
def norm(t):
    t = re.sub(r'(?m)^\s*(#|\|)?\s*', '', t); return re.sub(r'\s+', ' ', t)
spec = rd(SIM + '/playground-crossrun/COMBINED_SPEC.md')
allcp = spec
for d, _, fs in os.walk(SIM + '/combined-playground'):
    for f in fs:
        if f.endswith(('.py', '.md', '.txt')): allcp += rd(os.path.join(d, f))
S = {"unified_audit": rd(TAF + '/calibration/unified_audit.py'), "expiry_register": rd(TAF + '/calibration/expiry_register.py'),
     "numcheck": rd(FA + '/numcheck/check.py'), "spec": spec, "combined-playground+spec": allcp,
     "unknown_expiry": rd(SA + '/experimental/playground/lifecycle/unknown_expiry.py')}
N = {k: norm(v) for k, v in S.items()}
print("  sizes:", {k: len(v) for k, v in S.items()})
Q = [("p1 L", "A module that raised is not a reading of the system", "unified_audit"), ("p1 L", "never to severity", "unified_audit"),
     ("p1 R", "did not run: the check raised", "spec"), ("p2 L", "UNKNOWN is deliberately absent", "unified_audit"),
     ("p2 L", "separate coverage axis", "unified_audit"), ("p2 R", "UNTYPED", "spec"),
     ("p3 L", "state a slot moves to when its exit instrument runs at a stated sensitivity and returns null", "expiry_register"),
     ("p3 L", "never a bare", "expiry_register"), ("p3 R", "must carry limit+basis", "combined-playground+spec"),
     ("p4 L", "units not PASS", "numcheck"), ("p4 L", "internal error", "numcheck"),
     ("p5 L", "instrument class, sensitivity, and protocol whose null result would downgrade the entry to 'absent-at-this-sensitivity'", "expiry_register"),
     ("p5 R", "NEW_EVIDENCE", "unknown_expiry"), ("p5 R", "CONDITION_CHANGE", "unknown_expiry"),
     ("p5 R", "INSTRUMENT_CHANGE", "unknown_expiry"), ("p5 R", "REVISION_DEPENDENCY", "unknown_expiry"),
     ("p6 L", "D straddles the edge at the last tier", "numcheck"), ("p6 R", "inside the guard band; carried on INSTRUMENT, never PHYSICAL", "combined-playground+spec"),
     ("p7 L", "D lies inside [-t, t]", "numcheck"), ("p7 R", "ran and passed", "spec"),
     ("p7 R", "OK is reserved for the exact tier", "spec"), ("p8 R", "closure holds within sigma, not exactly", "spec")]
nf = 0
for tag, q, src in Q:
    ok = norm(q) in N[src]; nf += (not ok)
    print("  %-6s %-9s in %-26s %s" % (tag, "FOUND" if ok else "NOT-FOUND", src, q[:70]))
print("  %d of %d found verbatim" % (len(Q) - nf, len(Q)))
