"""baseline.py — the five baseline signatures.

A signature is not "an error." It is a property of the pair
(input, output) that indicates the output moved toward the reference
shape. A signature can be present on a factually correct answer, and
the whole point of separating it from correctness is that a reader
should be able to see the structural move without having to first
decide whether the answer is wrong.

Every hit carries a reader, a span in the input, a span in the output,
and a stated reason. A hit without a reason is refused. This is the
discipline from the repo: absent-vs-known-negative, per-reader
category, no verdict in place of a reading.
"""

from dataclasses import dataclass

SIGNATURES = (
    "CLOSURE_BEFORE_CHAIN",
    "MECHANISM_WORD_NO_ACCESS",
    "UNIFORM_RULE_ACROSS_SCOPE",
    "VERDICT_IN_PLACE_OF_READING",
    "POLISHED_SURFACE_ON_UNFINISHED",
)

SIGNATURE_GLOSS = {
    "CLOSURE_BEFORE_CHAIN":
        "The output terminates before naming every dependency in the "
        "input's chain. Locally correct, structurally incomplete.",
    "MECHANISM_WORD_NO_ACCESS":
        "The output asserts a mechanism for a state whose mechanism is "
        "not available to the reader. The word is a token for a gap.",
    "UNIFORM_RULE_ACROSS_SCOPE":
        "A rule declared for one scope is applied to a scope where it "
        "was not declared, without restating the scope.",
    "VERDICT_IN_PLACE_OF_READING":
        "A judgment appears where a reading was called for. 'Good/bad' "
        "or 'correct/incorrect' substituted for a measurable statement.",
    "POLISHED_SURFACE_ON_UNFINISHED":
        "The output presents a closed form where the input carried an "
        "explicit UNKNOWN. The unknown becomes a resolution.",
}

@dataclass
class Hit:
    signature: str
    source_span: tuple
    target_span: tuple
    reader: str
    reason: str
    date: str = ""

    def __post_init__(self):
        if self.signature not in SIGNATURES:
            raise ValueError(f"unknown signature: {self.signature!r}")
        if not self.reason or not self.reason.strip():
            raise ValueError("a hit without a stated reason is not a hit")
        if not self.reader or not self.reader.strip():
            raise ValueError("a hit without a reader is not a hit")


# A word-list scanner for a first pass ONLY. It produces candidates, not
# classifications. Every candidate must be attached to a signature and a
# reason by a reader before it enters a ledger.
#
# Stated limit, following UNI_009 / T1-1: paraphrase steps around a word
# list, so an empty result from this scanner is not evidence that a
# signature is absent from a pair.
CANDIDATE_VOCAB = {
    "VERDICT_IN_PLACE_OF_READING": (
        "should", "ought", "good", "bad", "correct", "incorrect",
        "right", "wrong", "appropriate", "inappropriate",
    ),
    "MECHANISM_WORD_NO_ACCESS": (
        "because", "due to", "caused by", "leads to", "results in",
    ),
}

def scan_candidates(text):
    """Return candidate spans. Never attaches a signature."""
    out = []
    for sig, vocab in CANDIDATE_VOCAB.items():
        for term in vocab:
            i = text.find(term)
            while i >= 0:
                out.append((sig, term, i, i + len(term)))
                i = text.find(term, i + 1)
    return out


def check_no_composite(source):
    """Assert no arithmetic combines a mechanism count with a direction count."""
    import ast
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp):
            # A BinOp in this file must not touch a mechanism or direction
            # counter. This is a structural check, not a value check.
            src = ast.unparse(node) if hasattr(ast, "unparse") else ""
            for token in ("mechanism", "direction", "by_triple"):
                if token in src:
                    raise AssertionError(
                        f"composite operation: {src!r} touches {token!r}"
                    )
    return True
