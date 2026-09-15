#!/usr/bin/env python3
"""frame_audit -- locate money-frame assumptions in text.

LOCATE ONLY.  This module proposes nothing.  There is no
replacement field, no suggestion, no rewrite, no score and no
verdict on the text.  A hit is a LOCATION, not a defect.  That
is enforced structurally rather than promised: test_substrate.py
walks this module's AST and fails if an identifier from the
proposal vocabulary (suggest / replace / instead / alternative /
rewrite / recommend / improve / fix / better) appears anywhere in
it, and plants one to show the scan is not silent.

THE LIMIT, STATED HERE RATHER THAN AT THE BOTTOM
    This is a WORD LIST.  Any paraphrase steps around it.
    "what it costs" is caught.  "what it takes from you before
    you may have it" is not, and carries the same frame.  So a
    zero from this module is a property of THE REGISTRY, never
    evidence that a text is frame-free.  The registry's coverage
    is the measurement; the text is only the sample.

THREE COUNTS, KEPT APART
    Many money-frame words carry a live non-money sense in the
    same corpus this was written in: `value` (absolute value),
    `property` (a property of a system), `cost` (a cost function),
    `budget` (an energy budget), `competition` (an ecological
    interaction), `efficiency` (a measured ratio).  Each such
    entry carries a stated reason and is counted APART, never
    silently included and never silently dropped -- the module
    locates, it does not adjudicate which sense is live.  A
    single collapsed count is the failure this split exists to
    prevent.

CC0.  Standard library only.  Parses under Python 3.9.
"""

import bisect
import collections
import re
import sys

FRAMES = (
    "OWNERSHIP",
    "PRICE",
    "TRANSACTION",
    "SCARCITY_AS_GIVEN",
    "VALUE_AS_PRICE",
)

CHOICES = {
    1: "Longest match wins at a position.  The registry is sorted "
       "by descending surface length before the alternation is "
       "built, so `cost-effective` is one VALUE_AS_PRICE hit and "
       "not a PRICE hit plus a loose word.  The alternative "
       "(count both) double-counts one utterance.",
    2: "A sentence ends at . ! or ? followed by whitespace.  "
       "Abbreviations over-split.  The sentence index is a "
       "locator for a reader, not a linguistic claim.",
    3: "A multi-frame phrase is filed under one frame by a "
       "declared reading: `supply and demand`, `market forces` "
       "and `free market` are SCARCITY_AS_GIVEN, because what "
       "they assert is the allocation premise, not a single "
       "price or a single exchange.",
    4: "`finance` / `financial` / `fiscal` / `compensation` are "
       "filed under PRICE, on the reading that what they name is "
       "money-quantity handling.  They could as defensibly sit "
       "under TRANSACTION.  The assignment is visible here so it "
       "can be disagreed with rather than inferred from output.",
    5: "A surface form may appear under exactly one frame.  A "
       "duplicate raises at load rather than being counted "
       "twice or silently taking the first frame.",
}

Hit = collections.namedtuple(
    "Hit",
    "surface entry frame sentence_index char_start char_end "
    "sentence sense_ambiguous ambiguity_reason",
)

_AMB_PROPERTY = "a property of a system (physics, mathematics)"
_AMB_COST = "a cost function; the compute or energy cost of an operation"
_AMB_VALUE = "absolute value; a value in a field; values as commitments"
_AMB_BUDGET = "an energy budget, a compute budget, a token budget"
_AMB_MARGIN = "a margin of error; a page margin"
_AMB_TRADE = "a trade as a craft; trade winds"
_AMB_EXCHANGE = "heat exchange; an exchange of letters"
_AMB_CONTRACT = "to contract; a muscle contracts"
_AMB_MARKET = "a marketplace of ideas; a farmers market as a place"
_AMB_CONSUMER = "an ecological consumer is a trophic position"
_AMB_COMPETE = "ecological competition is a measured interaction"
_AMB_EFF = "thermodynamic efficiency is a measured ratio"
_AMB_TRADEOFF = "a physical trade-off is a real constraint"
_AMB_TITLE = "the title of a document"
_AMB_STAKE = "a stake driven into the ground"
_AMB_EQUITY = "equity in the sense of fairness"
_AMB_QUOTE = "to quote a passage"
_AMB_CHARGE = "electric charge; to charge a battery"
_AMB_DEAL = "to deal with something"
_AMB_CLIENT = "a client in a client-server system"
_AMB_MINE = "a mine as an excavation"
_AMB_RATE = "a rate as a quantity per unit time"
_AMB_CLAIM = "a claim as an assertion under test"

REGISTRY = (
    # Frame assignment for a multi-frame phrase is a declared
    # reading -- [CHOICE 3].  The filing of `finance` and its
    # neighbours under PRICE is [CHOICE 4].
    # ---- OWNERSHIP --------------------------------------------
    ("own", "OWNERSHIP", None),
    ("owns", "OWNERSHIP", None),
    ("owned", "OWNERSHIP", None),
    ("owning", "OWNERSHIP", None),
    ("owner", "OWNERSHIP", None),
    ("owners", "OWNERSHIP", None),
    ("ownership", "OWNERSHIP", None),
    ("private property", "OWNERSHIP", None),
    ("intellectual property", "OWNERSHIP", None),
    ("property", "OWNERSHIP", _AMB_PROPERTY),
    ("proprietor", "OWNERSHIP", None),
    ("proprietary", "OWNERSHIP", None),
    ("deed", "OWNERSHIP", None),
    ("landlord", "OWNERSHIP", None),
    ("tenant", "OWNERSHIP", None),
    ("freehold", "OWNERSHIP", None),
    ("leasehold", "OWNERSHIP", None),
    ("title", "OWNERSHIP", _AMB_TITLE),
    ("possession", "OWNERSHIP", None),
    ("shareholder", "OWNERSHIP", None),
    ("stake", "OWNERSHIP", _AMB_STAKE),
    ("asset", "OWNERSHIP", None),
    ("assets", "OWNERSHIP", None),
    ("equity", "OWNERSHIP", _AMB_EQUITY),
    ("holdings", "OWNERSHIP", None),
    ("belongs to", "OWNERSHIP", None),
    ("entitled to", "OWNERSHIP", None),
    # ---- PRICE ------------------------------------------------
    ("price", "PRICE", None),
    ("prices", "PRICE", None),
    ("priced", "PRICE", None),
    ("pricing", "PRICE", None),
    ("cost", "PRICE", _AMB_COST),
    ("costs", "PRICE", _AMB_COST),
    ("costly", "PRICE", None),
    ("expensive", "PRICE", None),
    ("cheap", "PRICE", None),
    ("cheaper", "PRICE", None),
    ("afford", "PRICE", None),
    ("affordable", "PRICE", None),
    ("unaffordable", "PRICE", None),
    ("fee", "PRICE", None),
    ("fees", "PRICE", None),
    ("fare", "PRICE", None),
    ("tariff", "PRICE", None),
    ("surcharge", "PRICE", None),
    ("invoice", "PRICE", None),
    ("billed", "PRICE", None),
    ("quote", "PRICE", _AMB_QUOTE),
    ("markup", "PRICE", None),
    ("discount", "PRICE", None),
    ("dollar", "PRICE", None),
    ("dollars", "PRICE", None),
    ("cents", "PRICE", None),
    ("currency", "PRICE", None),
    ("money", "PRICE", None),
    ("monetary", "PRICE", None),
    ("cash", "PRICE", None),
    ("payment", "PRICE", None),
    ("payments", "PRICE", None),
    ("pay", "PRICE", None),
    ("paid", "PRICE", None),
    ("paying", "PRICE", None),
    ("wage", "PRICE", None),
    ("wages", "PRICE", None),
    ("salary", "PRICE", None),
    ("budget", "PRICE", _AMB_BUDGET),
    ("revenue", "PRICE", None),
    ("profit", "PRICE", None),
    ("profitable", "PRICE", None),
    ("margin", "PRICE", _AMB_MARGIN),
    ("subsidy", "PRICE", None),
    ("subsidize", "PRICE", None),
    ("finance", "PRICE", None),
    ("financial", "PRICE", None),
    ("fiscal", "PRICE", None),
    ("compensation", "PRICE", None),
    ("charge", "PRICE", _AMB_CHARGE),
    ("rate", "PRICE", _AMB_RATE),
    # ---- TRANSACTION ------------------------------------------
    ("buy", "TRANSACTION", None),
    ("buys", "TRANSACTION", None),
    ("buying", "TRANSACTION", None),
    ("bought", "TRANSACTION", None),
    ("sell", "TRANSACTION", None),
    ("sells", "TRANSACTION", None),
    ("selling", "TRANSACTION", None),
    ("sold", "TRANSACTION", None),
    ("for sale", "TRANSACTION", None),
    ("purchase", "TRANSACTION", None),
    ("purchased", "TRANSACTION", None),
    ("trade", "TRANSACTION", _AMB_TRADE),
    ("traded", "TRANSACTION", _AMB_TRADE),
    ("exchange", "TRANSACTION", _AMB_EXCHANGE),
    ("transaction", "TRANSACTION", None),
    ("transactions", "TRANSACTION", None),
    ("deal", "TRANSACTION", _AMB_DEAL),
    ("contract", "TRANSACTION", _AMB_CONTRACT),
    ("market", "TRANSACTION", _AMB_MARKET),
    ("markets", "TRANSACTION", _AMB_MARKET),
    ("customer", "TRANSACTION", None),
    ("customers", "TRANSACTION", None),
    ("client", "TRANSACTION", _AMB_CLIENT),
    ("vendor", "TRANSACTION", None),
    ("supplier", "TRANSACTION", None),
    ("consumer", "TRANSACTION", _AMB_CONSUMER),
    ("seller", "TRANSACTION", None),
    ("buyer", "TRANSACTION", None),
    ("negotiate", "TRANSACTION", None),
    ("bid", "TRANSACTION", None),
    ("auction", "TRANSACTION", None),
    ("lease", "TRANSACTION", None),
    ("rent", "TRANSACTION", None),
    ("rental", "TRANSACTION", None),
    ("hire", "TRANSACTION", None),
    ("procurement", "TRANSACTION", None),
    ("procure", "TRANSACTION", None),
    ("monetize", "TRANSACTION", None),
    ("commodity", "TRANSACTION", None),
    ("commerce", "TRANSACTION", None),
    ("commercial", "TRANSACTION", None),
    ("mine", "TRANSACTION", _AMB_MINE),
    # ---- SCARCITY_AS_GIVEN ------------------------------------
    ("scarce", "SCARCITY_AS_GIVEN", None),
    ("scarcity", "SCARCITY_AS_GIVEN", None),
    ("shortage", "SCARCITY_AS_GIVEN", None),
    ("supply and demand", "SCARCITY_AS_GIVEN", None),
    ("market forces", "SCARCITY_AS_GIVEN", None),
    ("free market", "SCARCITY_AS_GIVEN", None),
    ("limited supply", "SCARCITY_AS_GIVEN", None),
    ("zero-sum", "SCARCITY_AS_GIVEN", None),
    ("ration", "SCARCITY_AS_GIVEN", None),
    ("rationing", "SCARCITY_AS_GIVEN", None),
    ("rationed", "SCARCITY_AS_GIVEN", None),
    ("opportunity cost", "SCARCITY_AS_GIVEN", None),
    ("trade-off", "SCARCITY_AS_GIVEN", _AMB_TRADEOFF),
    ("tradeoff", "SCARCITY_AS_GIVEN", _AMB_TRADEOFF),
    ("not enough to go around", "SCARCITY_AS_GIVEN", None),
    ("competition", "SCARCITY_AS_GIVEN", _AMB_COMPETE),
    ("compete", "SCARCITY_AS_GIVEN", _AMB_COMPETE),
    ("competitive", "SCARCITY_AS_GIVEN", _AMB_COMPETE),
    # ---- VALUE_AS_PRICE ---------------------------------------
    ("value", "VALUE_AS_PRICE", _AMB_VALUE),
    ("values", "VALUE_AS_PRICE", _AMB_VALUE),
    ("valued", "VALUE_AS_PRICE", _AMB_VALUE),
    ("valuable", "VALUE_AS_PRICE", None),
    ("valuation", "VALUE_AS_PRICE", None),
    ("worth", "VALUE_AS_PRICE", None),
    ("worth it", "VALUE_AS_PRICE", None),
    ("not worth", "VALUE_AS_PRICE", None),
    ("net worth", "VALUE_AS_PRICE", None),
    ("priceless", "VALUE_AS_PRICE", None),
    ("adds value", "VALUE_AS_PRICE", None),
    ("value proposition", "VALUE_AS_PRICE", None),
    ("return on investment", "VALUE_AS_PRICE", None),
    ("roi", "VALUE_AS_PRICE", None),
    ("cost-effective", "VALUE_AS_PRICE", None),
    ("cost effective", "VALUE_AS_PRICE", None),
    ("cost-benefit", "VALUE_AS_PRICE", None),
    ("cost benefit", "VALUE_AS_PRICE", None),
    ("willingness to pay", "VALUE_AS_PRICE", None),
    ("willing to pay", "VALUE_AS_PRICE", None),
    ("bottom line", "VALUE_AS_PRICE", None),
    ("economic value", "VALUE_AS_PRICE", None),
    ("market value", "VALUE_AS_PRICE", None),
    ("pays for itself", "VALUE_AS_PRICE", None),
    ("efficiency", "VALUE_AS_PRICE", _AMB_EFF),
    ("efficient", "VALUE_AS_PRICE", _AMB_EFF),
    ("claim on", "VALUE_AS_PRICE", _AMB_CLAIM),
)


class RegistryError(Exception):
    """A registry that cannot be loaded is not silently repaired."""


def load_registry(registry=REGISTRY):
    """surface -> (frame, ambiguity_reason).  [CHOICE 5]"""
    out = {}
    for surface, frame, amb in registry:
        key = " ".join(surface.lower().split())
        if frame not in FRAMES:
            raise RegistryError("unknown frame %r for %r" % (frame, key))
        if not key:
            raise RegistryError("empty surface form")
        if key in out:
            raise RegistryError(
                "duplicate surface %r -- a surface form may carry "
                "exactly one frame [CHOICE 5]" % key)
        out[key] = (frame, amb)
    return out


def build_pattern(entries):
    """One alternation, longest surface first.  [CHOICE 1]"""
    keys = sorted(entries, key=lambda s: (-len(s), s))
    alts = []
    for key in keys:
        alts.append(r"\s+".join(re.escape(p) for p in key.split()))
    return re.compile(r"\b(?:" + "|".join(alts) + r")\b", re.I)


_SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+")


def sentence_spans(text):
    """[(start, end)] over the text.  Empty text -> [].  [CHOICE 2]"""
    if not text.strip():
        return []
    spans = []
    start = 0
    for m in _SENTENCE_BREAK.finditer(text):
        spans.append((start, m.start()))
        start = m.end()
    spans.append((start, len(text)))
    return [(a, b) for a, b in spans if text[a:b].strip()]


def zero_counts():
    """Every declared frame present, at zero.

    A frame with no hits is a visible zero, not a missing key.
    A caller cannot tell an absent frame from an unexamined one
    if the key is simply not there."""
    return collections.OrderedDict((f, 0) for f in FRAMES)


def audit(text, registry=REGISTRY):
    entries = load_registry(registry)
    pattern = build_pattern(entries)
    spans = sentence_spans(text)
    starts = [a for a, _ in spans]
    hits = []
    for m in pattern.finditer(text):
        key = " ".join(m.group(0).lower().split())
        frame, amb = entries[key]
        idx = bisect.bisect_right(starts, m.start()) - 1
        if idx < 0:
            idx = 0
        if spans:
            a, b = spans[idx]
            sentence = " ".join(text[a:b].split())
        else:
            sentence = ""
            idx = -1
        hits.append(Hit(
            surface=m.group(0),
            entry=key,
            frame=frame,
            sentence_index=idx,
            char_start=m.start(),
            char_end=m.end(),
            sentence=sentence,
            sense_ambiguous=amb is not None,
            ambiguity_reason=amb,
        ))
    counts = zero_counts()
    unamb = zero_counts()
    amb_counts = zero_counts()
    for hit in hits:
        counts[hit.frame] += 1
        if hit.sense_ambiguous:
            amb_counts[hit.frame] += 1
        else:
            unamb[hit.frame] += 1
    return {
        "hits": hits,
        "counts": counts,
        "counts_unambiguous": unamb,
        "counts_ambiguous": amb_counts,
        "hits_n": len(hits),
        "ambiguous_n": sum(1 for h in hits if h.sense_ambiguous),
        "sentences_n": len(spans),
        "registry_n": len(entries),
        "frames": FRAMES,
        "choices": sorted(CHOICES),
    }


def render(result, source="<text>"):
    lines = []
    lines.append("FRAME AUDIT -- %s" % source)
    lines.append("=" * 62)
    lines.append("registry entries : %d" % result["registry_n"])
    lines.append("sentences        : %d" % result["sentences_n"])
    lines.append("hits             : %d  (of which sense-ambiguous: %d)"
                 % (result["hits_n"], result["ambiguous_n"]))
    lines.append("")
    lines.append("COUNTS BY FRAME   total  unambiguous  ambiguous")
    for frame in FRAMES:
        lines.append("  %-20s %5d  %11d  %9d" % (
            frame,
            result["counts"][frame],
            result["counts_unambiguous"][frame],
            result["counts_ambiguous"][frame]))
    lines.append("")
    lines.append("HITS")
    if not result["hits"]:
        lines.append("  none.  A zero here is a property of the "
                     "registry, not of the text.")
    for hit in result["hits"]:
        mark = " [sense-ambiguous]" if hit.sense_ambiguous else ""
        lines.append("  s%-4d %-20s %-18s %r%s" % (
            hit.sentence_index, hit.frame, hit.entry,
            hit.surface, mark))
        if hit.sense_ambiguous:
            lines.append("        other live sense: %s"
                         % hit.ambiguity_reason)
        lines.append("        %s" % _clip(hit.sentence, 58))
    lines.append("")
    lines.append("This module locates.  It states nothing about what "
                 "any of these")
    lines.append("hits ought to be, and carries no field in which such "
                 "a thing")
    lines.append("could be written.")
    return "\n".join(lines)


def _clip(text, width):
    if len(text) <= width:
        return text
    return text[:width - 3] + "..."


def choices_report():
    out = ["frame_audit [CHOICE n]"]
    for n in sorted(CHOICES):
        out.append("  [CHOICE %d] %s" % (n, CHOICES[n]))
    return "\n".join(out)


USAGE = """usage: python3 frame_audit.py FILE
       python3 frame_audit.py -          (read standard input)
       python3 frame_audit.py --choices

Locates money-frame tokens.  Proposes nothing.
"""


def main(argv):
    args = list(argv[1:])
    if "--selftest" in args:
        sys.stderr.write(
            "frame_audit.py has no selftest of its own.\n"
            "Run: python3 test_substrate.py\n")
        return 2
    if not args or args[0] in ("-h", "--help"):
        sys.stdout.write(USAGE)
        return 0
    if args[0] == "--choices":
        print(choices_report())
        return 0
    if args[0] == "-":
        text = sys.stdin.read()
        source = "<stdin>"
    else:
        with open(args[0]) as handle:
            text = handle.read()
        source = args[0]
    print(render(audit(text), source))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
