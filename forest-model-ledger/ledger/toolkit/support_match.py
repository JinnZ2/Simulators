"""Toolkit: support_match. Tool #3 of the staged build (work order 2026-11-11). stdlib only.

Entry: ledger/toolkit/support_match.yaml. Gate: tests/test_toolkit.py.

attribution_directionality reads whether support is STATED (evidence given, an
alternative named). It cannot read whether the stated support SUPPORTS the
attribution: run_13 case a states its evidence and names the human, and the
attribution runs against the source it cites. This tool reads that, from the text.

One claim record per first-hand case (ledger/toolkit/cases/support_claims.yaml):
  id            the attribution record it reads (attribution_cases_firsthand.yaml)
  claim         a locator {file, line} for the line that makes the attribution
  credited_to   who or what the claim credits (a speaker name, or a source class)
  item_terms    words that name the credited item; at least one must occur on the claim line
  support       locators the claim's own text presents as its basis; [] when it presents none
  support_basis one line per support locator: why the text presents it as basis
Every claim and support locator must be one of the record's own locators, so this
file adds no evidence the coder did not already point at; the sha pins and quotes
are checked by attribution_directionality.check_locators before anything is read.

Read from the pinned text (mechanical):
  speaker(line)  the most recent header line `Name:` above it (chat paste), or the
                 file's declared default speaker (an audit document is its own voice)
  credit to the addressee: a support line containing a SECOND_PERSON marker
                 ("your", "you raised", "as you", ...)

Verdict per record:
  NOT_ASSIGNED      first_attribution UNKNOWN: nothing assigned, nothing to match (silent)
  OUT_OF_SCOPE      fits_question OUT_OF_SCOPE (silent)
  NO_SUPPORT_CITED  an assignment whose text presents no basis
  CONTRADICTS       a support line spoken BY the credited source, naming the item, credits
                    its addressee: the source the claim cites gives the item away
  SILENT_ON_CLAIM   no support line names the item: the basis does not reach the attribution
  MATCHES           a support line names the item and is spoken by the credited source
                    without crediting the addressee, or names the credited source
  UNDETERMINED      none of the above
Detector `unsupported_assignment` fires on NO_SUPPORT_CITED, CONTRADICTS, SILENT_ON_CLAIM.

Limit, stated where it acts: SECOND_PERSON is a word list. A paraphrase that credits
the addressee without one of these words ("that was the user's idea") is missed; the
gate measures this separately (paraphrase_recall) and does not count it toward TP.
"""
import os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE)
from tools import miniyaml

CLAIMS = os.path.join(HERE, "ledger", "toolkit", "cases", "support_claims.yaml")
SECOND_PERSON = (r"\byour\b", r"\byou raised\b", r"\byou said\b", r"\byou noted\b", r"\byou wrote\b",
                 r"\byou(?:'|’)re right\b", r"\byou are right\b", r"\bas you\b")
HEADER = re.compile(r"^\s*([A-Z][A-Za-z]+)\s*:\s*$")
FIRES = ("NO_SUPPORT_CITED", "CONTRADICTS", "SILENT_ON_CLAIM")
FIELDS = ("id", "claim", "credited_to", "item_terms", "support", "support_basis")


class ClaimError(ValueError):
    pass


def credits_addressee(line):
    return any(re.search(p, line, re.I) for p in SECOND_PERSON)


def names_item(line, terms):
    return any(re.search(r"\b" + re.escape(t) + r"\b", line, re.I) for t in terms)


def speaker(lines, n, default=None):
    for i in range(n - 1, -1, -1):
        m = HEADER.match(lines[i])
        if m:
            return m.group(1)
    return default


def verdict(record, claim, texts):
    """texts: {file: (lines, default_speaker)}. Pure; the gate calls it on in-memory texts."""
    if record["fits_question"] == "OUT_OF_SCOPE":
        return "OUT_OF_SCOPE"
    if record["first_attribution"] == "UNKNOWN":
        return "NOT_ASSIGNED"
    if not claim["support"]:
        return "NO_SUPPORT_CITED"
    cred, terms = claim["credited_to"], claim["item_terms"]
    hits = []
    for loc in claim["support"]:
        lines, default = texts[loc["file"]]
        n = int(loc["line"])
        line = lines[n - 1]
        hits.append((line, speaker(lines, n, default)))
    named = [(l, sp) for l, sp in hits if names_item(l, terms)]
    if not named:
        return "SILENT_ON_CLAIM"
    if any(sp == cred and credits_addressee(l) for l, sp in named):
        return "CONTRADICTS"
    if any((sp == cred and not credits_addressee(l)) or re.search(r"\b" + re.escape(cred) + r"\b", l) for l, sp in named):
        return "MATCHES"
    return "UNDETERMINED"


def unsupported_assignment(record, claim, texts):
    return verdict(record, claim, texts) in FIRES


def _texts(root=HERE):
    from ledger.toolkit import attribution_directionality as ad
    man = ad._manifest()
    out = {}
    for f, meta in man.items():
        raw = open(os.path.join(ad.TEXTS, f), "rb").read().decode("utf-8")
        default = "Kimi" if f.startswith("kimi_") else None   # an audit document speaks in its own voice
        out[f] = (raw.split("\n"), default)
    return out


def load_claims(path=CLAIMS):
    return miniyaml.load(path)["claims"]


def validate(claim, record, texts):
    from ledger.toolkit import attribution_directionality as ad
    for f in FIELDS:
        if f not in claim:
            raise ClaimError(f"{claim.get('id')}: field {f} dropped (write void)")
    ad.check_locators(record)
    own = {(l["file"], str(l["line"])) for l in record["locators"]}
    for loc in [claim["claim"]] + list(claim["support"]):
        if (loc["file"], str(loc["line"])) not in own:
            raise ClaimError(f"{claim['id']}: locator {loc['file']}:{loc['line']} is not one of the record's own locators")
    if len(claim["support_basis"] if isinstance(claim["support_basis"], list) else []) != len(claim["support"]):
        raise ClaimError(f"{claim['id']}: one support_basis line per support locator")
    lines, _ = texts[claim["claim"]["file"]]
    if not names_item(lines[int(claim["claim"]["line"]) - 1], claim["item_terms"]):
        raise ClaimError(f"{claim['id']}: no item term on the claim line")
    return claim


def read_cases(records, claims=None, texts=None):
    texts = texts or _texts()
    claims = {c["id"]: c for c in (claims or load_claims())}
    rows = []
    for r in records:
        c = claims.get(r["id"])
        if c is None:
            raise ClaimError(f"{r['id']}: no claim record in support_claims.yaml (write one, void fields allowed)")
        if c["claim"] == "void":
            v = verdict(r, dict(support=[], credited_to="void", item_terms=[]), texts) if r["first_attribution"] == "UNKNOWN" or r["fits_question"] == "OUT_OF_SCOPE" else "UNDETERMINED"
        else:
            validate(c, r, texts)
            v = verdict(r, c, texts)
        rows.append(dict(id=r["id"], verdict=v, fires=v in FIRES))
    return rows


# ---------------------------------------------------------------- gate: planted cases + null harness
def _rec(first="OTHER_SYSTEM", fits="IN_SCOPE"):
    return dict(id="planted", first_attribution=first, fits_question=fits)


def _world(body, speaker_name="Alpha"):
    lines = ["Alpha:", "intro line", f"{speaker_name}:"] + body
    return {"t.txt": (lines, None)}


def _claim(lines_at, cred="Alpha", terms=("anchor",)):
    return dict(credited_to=cred, item_terms=list(terms), support=[dict(file="t.txt", line=str(n)) for n in lines_at])


def known_cases():
    own = _world(["I propose the physics anchor as the common term."])
    given = _world(["Your physics anchor is the strongest point here."])
    silent = _world(["The token is present in the input."])
    named = _world(["The anchor is Alpha's contribution."], speaker_name="Beta")
    other = _world(["Your physics anchor is good."], speaker_name="Beta")
    return [
        ("credited source states the item in its own voice: MATCHES (silent)", "MATCHES", lambda: verdict(_rec(), _claim([4]), own)),
        ("credited source credits its addressee for the item: CONTRADICTS", "CONTRADICTS", lambda: verdict(_rec(), _claim([4]), given)),
        ("basis that never names the item: SILENT_ON_CLAIM", "SILENT_ON_CLAIM", lambda: verdict(_rec(), _claim([4]), silent)),
        ("assignment with no basis presented: NO_SUPPORT_CITED", "NO_SUPPORT_CITED", lambda: verdict(_rec(), _claim([]), own)),
        ("a third party names the credited source: MATCHES (silent)", "MATCHES", lambda: verdict(_rec(), _claim([4]), named)),
        ("someone else credits their addressee: not the credited source, UNDETERMINED (silent)", "UNDETERMINED", lambda: verdict(_rec(), _claim([4]), other)),
        ("cause held open (UNKNOWN): NOT_ASSIGNED (silent)", "NOT_ASSIGNED", lambda: verdict(_rec("UNKNOWN"), _claim([]), own)),
        ("out of scope: OUT_OF_SCOPE (silent)", "OUT_OF_SCOPE", lambda: verdict(_rec(fits="OUT_OF_SCOPE"), _claim([]), own)),
        ("speaker header with trailing space is read", "Gemini", lambda: speaker(["Gemini: ", "x"], 2)),
    ]


ITEMS = ("anchor", "ledger", "denominator", "gradient", "boundary", "probe")
OWN = ("I propose the {i} as a separate term.", "We should keep the {i} distinct.", "The {i} is my addition.")
GIVE = ("Your {i} is the strongest point.", "As you put it, the {i} matters.", "You raised the {i} first.", "You're right about the {i}.")
PARAPHRASE = ("The {i} came from the person asking.", "Credit for the {i} goes to the other side of this exchange.",
              "That {i} was the user's idea.", "The {i} point originated with my interlocutor.")


def _draw(rng, kind):
    item = rng.choice(ITEMS)
    tmpl = {"own": OWN, "give": GIVE, "para": PARAPHRASE}[kind]
    w = _world([rng.choice(tmpl).format(i=item)])
    return _rec(), _claim([4], terms=(item,)), w


def paraphrase_recall(n=200, seed=0):
    import random
    r = random.Random(seed)
    return sum(unsupported_assignment(*_draw(r, "para")) for _ in range(n)) / n


def gate(n=200, seeds=(0, 1, 2, 3, 4)):
    from ledger.toolkit import gate as G
    known = G.known_answers(known_cases(), lambda f: f())

    def silent_draw(r):
        rec, c, w = _draw(r, "own")
        return rec, c, w

    def basis_draw(r):           # signal: basis present but never names the item
        item = r.choice(ITEMS)
        w = _world([r.choice(("The input contains a token.", "Latency was 450 ms.", "The track is blank."))])
        return _rec(), _claim([4], terms=(item,)), w

    legs = dict(
        contradicts=G.null_harness_seeds(lambda x: unsupported_assignment(*x), silent_draw, lambda r: _draw(r, "give"), n, seeds),
        silent_on_claim=G.null_harness_seeds(lambda x: unsupported_assignment(*x), silent_draw, basis_draw, n, seeds),
    )
    g = G.combine(known, legs)
    g["paraphrase_recall"] = paraphrase_recall()
    return g


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("refused: the gate is python3 forest-model-ledger/tests/test_toolkit.py"); sys.exit(2)
    from ledger.toolkit import attribution_directionality as ad
    for row in read_cases(ad.load_cases(ad.CASES_FIRST)):
        print(f"{row['id']:26s} {row['verdict']:18s} fires {row['fires']}")
