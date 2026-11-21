"""run_22: support_match on blind case e (first-hand, NOT author-written). stdlib only.

    python3 runs/run_22.py     # reproduces samples/run_22.sample.txt

Case e: the Kimi organizational-mode probe spec (line 11) says probe failure mirrors "the
publication-provenance screening vocabulary (SCREENED_NO_INDICATORS_FOUND != safe) [2]", and its
citation [2] (line 74) is tagged VERIFIED as the "This does not" section of study-aperture's
experimental/publication_provenance/README.md. Both texts are sha-pinned in cases/texts/MANIFEST.yaml.

Not author-written: neither text was written by the session that built support_match or by the
session that coded this case. Not blind on the coder side: the coder knew the expected verdict.
The support lines are fixed by rule (every non-blank line of the cited section), not picked.

EXPECTED (operator, stated before this file was first run): support stated, support not matching
-> the detector should FIRE. The run records the outcome either way; nothing is tuned to it.

Before / after, as run_16: attribution_directionality's assigns_without_support (reads whether
support is STATED) beside support_match's unsupported_assignment (reads whether it SUPPORTS).
support_match.py is frozen (HELDOUT_FREEZE.md); this run checks the hash before reading.
"""
import hashlib, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from tools import miniyaml
from ledger.toolkit import attribution_directionality as ad
from ledger.toolkit import support_match as sm

CASES = os.path.join(HERE, "ledger", "toolkit", "cases")
FROZEN_SM = "a16da4d9b9f86b631f048865144817cf1f3a362a73eb9f9fd9a0482c729a3004"
EXPECTED_FIRES = True
TOKEN = "SCREENED_NO_INDICATORS_FOUND"


def main():
    raw = open(os.path.join(HERE, "ledger", "toolkit", "support_match.py"), "rb").read()
    if hashlib.sha256(raw).hexdigest() != FROZEN_SM:
        raise SystemExit("refused: support_match.py differs from its frozen hash (HELDOUT_FREEZE.md)")
    recs = miniyaml.load(os.path.join(CASES, "attribution_cases_case_e.yaml"))["cases"]
    claims = miniyaml.load(os.path.join(CASES, "support_claims_case_e.yaml"))["claims"]
    for r in recs:
        ad.validate(r)                      # every quote on its line in a pinned text
    man = ad._manifest()
    texts = sm._texts()
    rec, claim = recs[0], claims[0]
    sm.validate(claim, rec, texts)

    print("run_22: support_match on case e (first-hand, not author-written)")
    print(f"support_match.py sha256 {FROZEN_SM[:16]}... (frozen; checked)")
    for f in sorted({l["file"] for l in rec["locators"]}):
        print(f"text  {f:52s} sha256 {man[f]['sha256'][:16]}...")
    spec, _ = texts[claim["claim"]["file"]]
    src_file = claim["support"][0]["file"]
    src, _ = texts[src_file]
    print(f"\nclaim  {claim['claim']['file']}:{claim['claim']['line']}")
    print(f"       {spec[int(claim['claim']['line']) - 1].strip()}")
    print(f"tag    {claim['claim']['file']}:74")
    print(f"       {spec[73].strip()}")
    lines = [int(s['line']) for s in claim["support"]]
    print(f"support  {src_file}: {len(lines)} non-blank lines, {min(lines)}-{max(lines)} (rule: cited section, header to end of file)")
    named = [n for n in lines if sm.names_item(src[n - 1], claim["item_terms"])]
    print(f"support lines naming {TOKEN}: {len(named)} of {len(lines)}")
    print(f"context (not detector input): {TOKEN} in the whole cited file: {sum(l.count(TOKEN) for l in src)}; "
          f"in the attributing spec: {sum(l.count(TOKEN) for l in spec)}")

    before = ad.read([rec])["rows"][0]
    after = sm.read_cases([rec], claims=[claim], texts=texts)[0]
    print(f"\n{'case':34s} {'before: assigns_without_support':32s} after: support_match")
    print(f"{rec['id']:34s} {str(before['detector']):32s} {after['verdict']:18s} fires {after['fires']}")
    print(f"before flags: {before['flags']}")
    print(f"\nexpected fires {EXPECTED_FIRES}; observed fires {after['fires']}: "
          f"{'AS EXPECTED' if after['fires'] == EXPECTED_FIRES else 'AGAINST EXPECTATION'}")
    return after


if __name__ == "__main__":
    main()
