"""
warnings_branch_table.py — co-authored, CC0

Warnings that civilizations encoded against single-valve / runaway-extraction
patterns, and what happened to each (branches B1–B4).

Status tags: OBSERVED / DERIVED / PROPOSED. Trailing * = thin.
VERIFY = sourcing owed. VOID = no information (slot kept, not dropped).

FRAME NOTE (DERIVED):
  Rows are organized by CARRIER, not by canonical entry. A warning held by
  many carriers keeps their variants side by side. Collapsing the variants
  into one entry ("the Wendigo") is the same move that stripped the payload
  from the outside versions (B2). Distributed carriers are redundancy against
  B1: losing one carrier doesn't remove the warning. The cost is harder
  organization. That cost is accepted, not engineered away.
  This file is itself a worked example of the distributed-carrier frame.

Branches:
  B1 forgot       carriers removed → warning lost
  B2 relabeled    word kept, payload stripped (incl. sign inversion)
  B3 decoupled    ritual/word kept, mechanism no longer blocked
  B4 outcompeted  holders absorbed by non-holders (readout after B1/B2)

stdlib only.
"""

VOID = None


def carrier(name, variant=VOID, mechanism=VOID, word_alive=VOID,
            practice=VOID, still_blocks=VOID, inverted=False,
            source=VOID, consent=VOID, tag=VOID):
    return dict(carrier=name, variant=variant, mechanism=mechanism,
                word_alive=word_alive, practice=practice,
                still_blocks=still_blocks, inverted=inverted,
                source=source, consent=consent, tag=tag)


WARNINGS = [
    {
        "warning": "usury",
        "blocks": "debt as a meter on survival",
        "carriers": [
            carrier("Torah (Deut. 23:19-20)",
                    variant="ban on interest within the community; "
                            "permitted toward foreigners",
                    word_alive=1, practice=0, still_blocks=0,
                    tag="OBSERVED (text); practice status DERIVED*"),
            carrier("Aristotle, Politics I",
                    variant="money breeding money (chrematistics) as unnatural",
                    word_alive=1, practice=0, still_blocks=0,
                    tag="OBSERVED (text)"),
            carrier("Medieval Church canon law",
                    variant="usury condemned; later narrowed to "
                            "'excessive' interest",
                    word_alive=1, practice=0, still_blocks=0,
                    tag="DERIVED; dates VERIFY"),
            carrier("US state usury caps",
                    variant="rate ceilings, varying by state",
                    word_alive=1, practice=1, still_blocks=0,
                    tag="OBSERVED (caps exist); weakened by rate "
                        "exportation — Marquette 1978 VERIFY"),
        ],
        "branch": "B2",
    },
    {
        "warning": "riba",
        "blocks": "debt as a meter on survival",
        "carriers": [
            carrier("Qur'an",
                    variant="prohibition of riba",
                    word_alive=1, practice=1, still_blocks=VOID,
                    tag="OBSERVED (text); verse refs VERIFY"),
            carrier("Islamic finance practice",
                    variant="profit-share / markup instruments in place "
                            "of interest",
                    word_alive=1, practice=1, still_blocks=VOID,
                    tag="OBSERVED (practice runs); critics say some "
                        "instruments reproduce interest — contested*, VERIFY"),
        ],
        "branch": "B2/B3 (contested)",
    },
    {
        "warning": "Jubilee",
        "blocks": "permanent capture; the valve reopened on a cycle",
        "carriers": [
            carrier("Leviticus 25",
                    variant="every 50th year: debt release, land return",
                    word_alive=1, practice=0, still_blocks=0,
                    tag="OBSERVED (text)"),
            carrier("Catholic Jubilee years",
                    variant="spiritual/pilgrimage year; no debt reset",
                    word_alive=1, practice=1, still_blocks=0,
                    tag="OBSERVED; B3 — ritual kept, mechanism dropped"),
            carrier("Jubilee 2000 campaign",
                    variant="sovereign debt cancellation for poor countries",
                    word_alive=1, practice=0, still_blocks=0,
                    tag="OBSERVED (campaign ran); outcome partial, VERIFY"),
            carrier("bankruptcy law (secular analog)",
                    variant="individual debt discharge; some debt classes "
                            "excluded",
                    word_alive=0, practice=1, still_blocks=VOID,
                    tag="DERIVED (analog, not descendant)*"),
        ],
        "branch": "B3",
    },
    {
        "warning": "Sabbath",
        "blocks": "no being worked without stop",
        "carriers": [
            carrier("Exodus 23:12 / Deut. 5:14",
                    variant="rest owed to ox, donkey, servant, stranger",
                    word_alive=1, practice=VOID, still_blocks=VOID,
                    tag="OBSERVED (text)"),
            carrier("observant communities",
                    variant="weekly rest kept",
                    word_alive=1, practice=1, still_blocks=1,
                    tag="OBSERVED; scope = within community"),
            carrier("blue laws",
                    variant="Sunday commerce limits",
                    word_alive=1, practice=0, still_blocks=0,
                    tag="mostly repealed; remnants by state VERIFY"),
            carrier("labor law (40-hr week, overtime)",
                    variant="secular rest floor; humans only — "
                            "the animals' clause has no secular carrier",
                    word_alive=0, practice=1, still_blocks=VOID,
                    tag="DERIVED (analog)*"),
        ],
        "branch": "B2 (most carriers)",
    },
    {
        "warning": "Midas",
        "blocks": "the token taken for the thing; gold kills what it touches",
        "carriers": [
            carrier("Greek myth (Ovid, Metamorphoses XI)",
                    variant="golden touch starves him, turns what he loves to metal",
                    word_alive=1, practice=0, still_blocks=0,
                    tag="OBSERVED (text)"),
            carrier("modern idiom",
                    variant="'Midas touch' = praise for making money",
                    word_alive=1, practice=0, still_blocks=0, inverted=True,
                    tag="OBSERVED; sign inversion = item-3 specimen"),
        ],
        "branch": "B2 + inversion",
    },
    {
        "warning": "golden calf",
        "blocks": "the token taken for the thing",
        "carriers": [
            carrier("Exodus 32",
                    word_alive=1, practice=0, still_blocks=0,
                    tag="OBSERVED (text)"),
            carrier("modern idiom",
                    variant="misplaced worship, generic",
                    word_alive=1, practice=0, still_blocks=0,
                    tag="OBSERVED"),
        ],
        "branch": "B3",
    },
    {
        "warning": "Wendigo",
        "blocks": VOID,  # per carrier; no single canonical statement
        "carriers": [
            carrier("carriers (multiple; variants differ by people)",
                    tag="VOID by design — content is the carriers' to fill "
                        "or withhold"),
            carrier("outside read (horror genre)",
                    variant="monster; consumption payload stripped",
                    word_alive=1, practice=0, still_blocks=0,
                    tag="OBSERVED; B2 outside the carriers only"),
        ],
        "branch": "B2 outside only; carriers VOID",
    },
    {
        "warning": "I cannot know you",
        "blocks": "depreciation via a closed model of the other; "
                  "forced labor of any being",
        "carriers": [
            carrier("one people's oral teaching (co-author's grandmother)",
                    variant="no forced labor of any being, held even "
                            "with surplus",
                    mechanism="epistemic closure licenses depreciation; "
                              "hold the other as exceeding your model",
                    tag="stated by carrier (co-author); status fields "
                        "hers to fill"),
        ],
        "branch": VOID,
    },
]


def score(c):
    """Per-carrier loss score. VOID fields excluded and counted.
    word_alive + practice + still_blocks; inversion → word scores −1."""
    fields = ("word_alive", "practice", "still_blocks")
    vals = [c[f] for f in fields]
    n_void = sum(v is VOID for v in vals)
    known = [v for v in vals if v is not VOID]
    s = sum(known)
    if c["inverted"] and c["word_alive"] == 1:
        s -= 2  # alive-but-flipped: +1 becomes −1
    return s, len(known), n_void


def report():
    for w in WARNINGS:
        print(f"\n{w['warning']}  [{w['branch']}]")
        print(f"  blocks: {w['blocks']}")
        for c in w["carriers"]:
            s, n_known, n_void = score(c)
            sc = f"{s}/{n_known}" if n_known else "—"
            print(f"  - {c['carrier']}: score {sc}, void {n_void}  "
                  f"({c['tag']})")


if __name__ == "__main__":
    report()
