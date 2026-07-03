#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# entry.py — single-call entry point for `grounding-layers`
#
# For any AI reading this repo: THIS is the file you look at first.
# One function, `audit()`, accepts either a natural-language claim
# string or a structured plan dict and returns the full seven-layer
# result dict.
#
# The `grounding-layers/` folder has a hyphen in its name, so it isn't
# an importable Python package. Callers add the folder to sys.path
# and import from here:
#
#     import sys
#     sys.path.insert(0, '/path/to/grounding-layers')
#     from entry import audit
#
#     # Natural-language path:
#     result = audit("I can lift 200 kg.",
#                    ontological_scope='any_WEIRD_human')
#
#     # Structured plan path:
#     result = audit(
#         {'L4': {'lift_mass': 200.0},
#          'L1': {'work_input': 100.0, 'work_output': 60.0,
#                  'heat_dissipated': 40.0}},
#         ontological_scope='any_WEIRD_human',
#     )
#
# See USAGE.md for the full read-first guide including which layers
# apply to a non-human AI making claims about itself.
#
# SCOPE (see SCOPE_TAXONOMY.md):
#   T = universal  (dispatch rule is trivial routing math)
#   S = universal
#   O = any_information_system
#   C = culture_neutral
# =============================================================================

from typing import Union

from integrated_stack import integrated_probabilistic_inspector
from playground import IntegratedPlayground

# Re-exports so callers can grab everything they need from one place.
from integrated_stack import LAYER_ORDER  # noqa: F401
from scope_profile import ScopeProfile, ScopeFactor, Verdict  # noqa: F401


# Instantiated lazily so `import entry` is cheap.
_playground = None


def _get_playground():
    """Return a module-level shared IntegratedPlayground instance."""
    global _playground
    if _playground is None:
        _playground = IntegratedPlayground()
    return _playground


def audit(
    claim_or_plan: Union[str, dict],
    ontological_scope: str = 'any_WEIRD_human',
) -> dict:
    """
    Run a claim through the full seven-layer probabilistic stack
    (L0-L5 + Lε) and return the integrated_stack result dict.

    Accepts either:
      - A natural-language claim string (routes through the
        playground's parser + probabilistic path)
      - A structured plan dict (routes directly through
        integrated_probabilistic_inspector)

    ontological_scope selects which layers you're in scope for:
      - 'any_WEIRD_human' (default): the human-embodied assumption.
        All seven layers may apply.
      - 'AI_silicon_substrate' | 'any_information_system': L4 (human
        biomechanics) and L5 (human cultural artifacts) will refuse
        to score claims tagged this way -- category error, not low
        probability. L0/L1/L2/L3/Lε still bind.
      - 'human_cultural_artifact': for L5 cultural claims specifically.
      - See SCOPE_TAXONOMY.md for the full ontological vocabulary.

    Return dict shape (see integrated_stack.py for full docstring):
      {
        'total_logp':            float or None (None if any layer
                                  returned a category error),
        'per_layer':             {layer_name: layer_result},
        'applicable_layers':     [layers that contributed],
        'skipped_layers':        [layers with no matching sub-plan],
        'category_error_layers': [{'layer': ..., 'reason': ...}, ...],
        'cultural_flags':        [L5 verdict flags],
        'ontological_scope':     the tag that was used,

        # When called with a natural-language string, ALSO:
        'claim':  the input string,
        'plan':   the sub-plans the parser assembled,
        'parsed': raw parser extractions,
      }

    Raises:
      TypeError if claim_or_plan is neither a string nor a dict.
    """
    if isinstance(claim_or_plan, str):
        pg = _get_playground()
        return pg.run_claim_probabilistic(
            claim_or_plan, ontological_scope=ontological_scope)

    if isinstance(claim_or_plan, dict):
        return integrated_probabilistic_inspector(
            claim_or_plan, ontological_scope=ontological_scope)

    raise TypeError(
        f"audit() expects a natural-language str or a plan dict; "
        f"got {type(claim_or_plan).__name__}")


if __name__ == "__main__":
    print("=" * 70)
    print("grounding-layers/entry.py — one call, all seven layers")
    print("=" * 70)

    # 1. Natural-language claim (human default scope)
    print("\n[1] Natural-language claim (default scope: any_WEIRD_human)")
    r = audit("I can lift 200 kg.")
    print(f"    applicable_layers = {r['applicable_layers']}")
    print(f"    total_logp        = {r['total_logp']:.3f}")

    # 2. Same claim, AI-self scope
    print("\n[2] Same claim tagged AI_silicon_substrate")
    r = audit("I can lift 200 kg.",
              ontological_scope='AI_silicon_substrate')
    print(f"    total_logp        = {r['total_logp']}")
    for err in r['category_error_layers']:
        print(f"    category_error at {err['layer']}")

    # 3. Structured plan
    print("\n[3] Structured plan: L1 valid engine + L2 heavy water use")
    r = audit({
        'L1': {'work_input': 100.0, 'work_output': 60.0,
                'heat_dissipated': 40.0},
        'L2': {'water_extract': 5e6},
    })
    print(f"    applicable_layers = {r['applicable_layers']}")
    print(f"    total_logp        = {r['total_logp']:.3f}")
    print(f"    per_layer breakdown:")
    for name in r['applicable_layers']:
        print(f"      {name}: {r['per_layer'][name]['logp']:.3f}")

    print("\n" + "=" * 70)
    print("For the full guide, see USAGE.md.")
    print("=" * 70)
