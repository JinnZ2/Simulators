#!/usr/bin/env python3
"""
substrate_substitution.py

Lightweight CLI: walk a CLAIM_TABLE.json file and print the
grass / grasshopper substitution next to each claim. The structural
enforcement is in the simplicity -- one substitution per claim, side
by side, ready for a reviewer's eyes.

For richer programmatic analysis (seven categories from harsh to
gentle, balanced-view walkthrough, honesty framework), use the sister
module `tools/substrate_substitution_toolkit.py`. This file's
ECOLOGICAL_SUBSTITUTIONS list is the toolkit's PURE_CONSUMER pair
expanded with the narrative-system-specific phrases that show up in
this repo's claim tables.

Premise: narrative-instinct (the tendency of narrative-trained
systems to project narrative scope onto substrate) is hard to catch
from inside narrative scope. Substituting non-human ecological terms
forces a sanity check. If the substituted version is incoherent or
absurd, the original almost certainly contains narrative-instinct
bias.

Example:
    Original:    "scale_builder narrative amplifies substrate reach"
    Substituted: "wind-dispersed insects amplify grass reach"

    The substituted version is not a known ecological mechanism;
    the original was narrative-instinct.

CLI:
    python3 tools/substrate_substitution.py <CLAIM_TABLE.json>

This is a structural enforcement tool, not a verdict generator.
Output requires human review.

License: CC0
Dependencies: stdlib only
"""

import json
import sys
from pathlib import Path
from typing import Dict, List


# Order matters: longer phrases first so they're substituted before
# their constituent words (e.g. "narrative_population" before
# "narrative").
ECOLOGICAL_SUBSTITUTIONS = [
    # Multi-word phrases first
    ('narrative_recognition_of_substrate', 'grasshopper recognition of grass'),
    ('narrative_supports_substrate',       'grasshoppers support grass'),
    ('narrative_amplifies_substrate',      'grasshoppers amplify grass'),
    ('substrate_population',               'grass community'),
    ('narrative_population',               'grasshopper swarm'),
    ('narrative_civilization',             'grasshopper aggregation'),
    ('narrative_authority',                'grasshopper density'),
    ('first_principles_narrative',         'wind-dispersed insect'),
    ('inverted_narrative',                 'overgrazing grasshopper density'),
    ('scale_builder',                      'wind-dispersed insect'),
    ('scale-builder',                      'wind-dispersed insect'),
    # Single words
    ('substrate',                          'grass'),
    ('narrative',                          'grasshoppers'),
    # Case variants
    ('Substrate',                          'Grass'),
    ('Narrative',                          'Grasshoppers'),
]


def substitute_claim(text: str) -> str:
    """Apply ecological substitution to expose narrative-instinct bias."""
    if not text:
        return text
    out = text
    for original, ecological in ECOLOGICAL_SUBSTITUTIONS:
        out = out.replace(original, ecological)
    return out


def evaluate_claim_with_substitution(claim: Dict) -> Dict:
    """
    Apply substitution to a claim and return both versions plus
    flags. The 'requires_review' flag is always True -- this tool
    does not auto-verdict; it presents the substituted version for
    a human (or another AI checking against ecology) to assess.
    """
    fields = ('statement', 'hypothesis', 'prediction',
              'falsification_criteria', 'notes')
    substituted: Dict[str, str] = {}
    any_change = False
    for f in fields:
        original = claim.get(f) or ''
        if not isinstance(original, str):
            continue
        sub = substitute_claim(original)
        if sub != original:
            any_change = True
        substituted[f] = sub

    return {
        'claim_id': claim.get('claim_id', '?'),
        'status': claim.get('status'),
        'original': {f: claim.get(f) for f in fields if claim.get(f)},
        'substituted': substituted,
        'changed': any_change,
        'requires_review': True,
        'note': (
            'If the ecological substitution is absurd or incoherent, '
            'the original claim contains narrative-instinct bias. '
            'Substrate-narrative relationships should map cleanly onto '
            'grass-grasshopper relationships when described honestly.'
        ),
    }


def evaluate_claim_table(path: Path) -> Dict:
    """Load and apply the substitution test to every claim in a file."""
    data = json.loads(path.read_text())
    claims = data.get('claims', [])
    evaluations = [evaluate_claim_with_substitution(c) for c in claims
                   if isinstance(c, dict)]
    return {
        'source_file': str(path),
        'claim_count': len(evaluations),
        'changed_count': sum(1 for e in evaluations if e['changed']),
        'evaluations': evaluations,
    }


def _print_table(report: Dict) -> None:
    print(f"\n{report['source_file']}")
    print(f"  claims:            {report['claim_count']}")
    print(f"  contained substrate/narrative terms: {report['changed_count']}")
    for ev in report['evaluations']:
        if not ev['changed']:
            continue
        print(f"\n  --- {ev['claim_id']} ({ev['status']}) ---")
        for field in ('statement', 'prediction'):
            orig = ev['original'].get(field)
            sub = ev['substituted'].get(field)
            if orig and sub and orig != sub:
                print(f"    [{field} ORIGINAL]")
                print(f"      {orig}")
                print(f"    [{field} SUBSTITUTED]")
                print(f"      {sub}")


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("usage: substrate_substitution.py <CLAIM_TABLE.json> [...]",
              file=sys.stderr)
        return 2
    for arg in argv[1:]:
        report = evaluate_claim_table(Path(arg))
        _print_table(report)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
