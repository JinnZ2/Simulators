"""Shared constants for orientation-chamber. CC0, stdlib only, parses under 3.8.

PROPOSED | co-authored (JinnZ2 + Claude) | CC0.
"""
import re

PRINCIPLE = ("No error is wrong. A miss is information: it locates where the model of the "
             "world or self differs from what happened. Misses are logged, never scored down.")

# Words the work order bars from output. The principle sentence above is the
# one exemption: it is delivered verbatim and contains one of them. The
# exemption is the exact sentence, masked before the scan, and nothing else.
BANNED = ("wrong", "fail", "bad", "mistake")
# Field names misslog refuses: a scoring field cannot be added by accident.
SCORE_KEYS = re.compile(r"(score|grade|pass|fail|penalt|rank|point|reward|correct)", re.I)

VOCAB = ("MISS", "OFFSET", "UNLOCATED", "MATCH")


def header():
    """The header line every rendered output starts with."""
    return "# orientation-chamber | PROPOSED | " + PRINCIPLE


def banned_hits(text):
    """Banned words in `text`, with the verbatim principle masked first."""
    masked = text.replace(PRINCIPLE, "#" * len(PRINCIPLE))
    return [w for w in BANNED if re.search(r"\b" + w, masked, re.I)]
