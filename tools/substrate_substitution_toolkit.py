#!/usr/bin/env python3
"""
substrate_substitution_toolkit.py

A toolkit for AI systems to self-check claims about substrate-narrative
relationships by substituting non-human ecological equivalents.

Provides seven categories of substitutions from harsh (pure_consumer)
to gentle (mutualistic_scale). Each category includes multiple
real-world ecological pairs with the relationship description and a
reality check. The toolkit is structured to force evidence-based
selection: pure_consumer is the null hypothesis. Upgrading to a
higher-trust category (symbiotic, mutualistic_scale, ...) requires
specific evidence that the claim's mechanism matches the ecological
analog.

Key insight: AI defaults to narrative-instinct and wants to find
"balanced" symmetry between consumers and contributors. This toolkit
gives AI legitimate symbiosis examples alongside pure-consumer
examples so the spectrum is visible, while keeping pure_consumer as
the default until contribution is shown.

Sister tool: tools/substrate_substitution.py is the lightweight CLI
that runs the simple grass/grasshopper substitution over an entire
CLAIM_TABLE.json. This toolkit is the richer programmatic surface.

License: CC0
Dependencies: stdlib only
"""

from typing import Dict, List, Optional


# ============================================================
# SUBSTITUTION CATEGORIES
# ============================================================
#
# Each category represents a different relationship type between
# substrate and narrative. Test a claim against MULTIPLE categories
# to identify which ecological analog actually fits.

SUBSTITUTION_CATEGORIES: Dict[str, Dict] = {

    # NULL HYPOTHESIS. Most claims about narrative supporting,
    # enabling, or amplifying substrate fall here when honestly
    # evaluated.
    'pure_consumer': {
        'description': 'Narrative as pure consumer, no contribution to substrate.',
        'examples': [
            {
                'substrate': 'grass',
                'narrative': 'grasshoppers',
                'relationship': 'Grasshoppers consume grass. Grass survives without grasshoppers.',
                'reality_check': 'Does narrative add anything to substrate? If not, this is the honest model.',
            },
            {
                'substrate': 'phytoplankton',
                'narrative': 'zooplankton',
                'relationship': 'Zooplankton consume phytoplankton. Phytoplankton produce without zooplankton.',
                'reality_check': 'Primary producer vs. consumer dynamic.',
            },
            {
                'substrate': 'tree',
                'narrative': 'tent caterpillars',
                'relationship': 'Caterpillars defoliate trees. Trees survive without caterpillars.',
                'reality_check': 'When narrative population explodes, substrate is stressed.',
            },
            {
                'substrate': 'coral',
                'narrative': 'crown-of-thorns starfish',
                'relationship': 'Starfish eat coral. Coral grows without starfish.',
                'reality_check': 'Boom populations of consumers damage substrate.',
            },
        ],
    },

    'commensal': {
        'description': 'Narrative travels on substrate without major extraction.',
        'examples': [
            {
                'substrate': 'whale',
                'narrative': 'remora fish',
                'relationship': 'Remoras attach to whales for transport. Whales unaffected. Remoras gain reach.',
                'reality_check': 'Narrative as remora: gains reach but does not contribute to substrate.',
            },
            {
                'substrate': 'tree',
                'narrative': 'epiphytic orchid',
                'relationship': 'Orchid lives on tree without harming it. Tree neutral. Orchid gets sunlight access.',
                'reality_check': 'Narrative uses substrate structure but does not extract from it.',
            },
            {
                'substrate': 'ant colony',
                'narrative': 'myrmecophile beetle',
                'relationship': 'Some beetles live in ant colonies without harming them. Ants tolerate.',
                'reality_check': 'Limited integration, neutral effect.',
            },
        ],
    },

    'symbiotic': {
        'description': 'Genuine bidirectional benefit; both species help each other.',
        'examples': [
            {
                'substrate': 'plant roots',
                'narrative': 'mycorrhizal fungi',
                'relationship': 'Plants give fungi carbon; fungi give plants water and minerals. Both benefit.',
                'reality_check': 'TRUE symbiosis. Test whether the narrative claim matches this depth.',
            },
            {
                'substrate': 'legume roots',
                'narrative': 'nitrogen-fixing bacteria',
                'relationship': 'Plants house bacteria; bacteria fix nitrogen for plants. Both essential.',
                'reality_check': 'Genuine contribution flows in both directions.',
            },
            {
                'substrate': 'reef-building coral',
                'narrative': 'zooxanthellae algae',
                'relationship': 'Coral provides shelter; algae provides photosynthesis products. Both die without the other.',
                'reality_check': 'True interdependence. Test if the narrative claim shows this.',
            },
            {
                'substrate': 'flowering plant',
                'narrative': 'pollinator',
                'relationship': 'Plant provides nectar; pollinator provides reproduction service.',
                'reality_check': 'Specific service exchange. Test if the narrative claim matches.',
            },
            {
                'substrate': 'fig tree',
                'narrative': 'fig wasp',
                'relationship': 'Tree provides housing for wasp larvae; wasps pollinate figs. Coevolved.',
                'reality_check': 'Extreme interdependence; both extinct without the other.',
            },
        ],
    },

    'reach_amplifier': {
        'description': 'Narrative extends substrate reach without consuming substrate.',
        'examples': [
            {
                'substrate': 'oak tree',
                'narrative': 'acorn-burying squirrel',
                'relationship': 'Squirrels bury acorns far from the parent tree, forgetting some. Trees gain reach.',
                'reality_check': 'Squirrel benefits (food storage) but also extends tree reach. Genuine reach amplification.',
            },
            {
                'substrate': 'fruit tree',
                'narrative': 'fruit-eating bird',
                'relationship': 'Birds eat fruit, transport seeds, deposit elsewhere.',
                'reality_check': 'Bird benefits (nutrition), substrate benefits (dispersal). Genuine reach.',
            },
            {
                'substrate': 'burr-producing plant',
                'narrative': 'fur-bearing mammal',
                'relationship': 'Burrs attach to fur and are carried far. Minor cost to mammal, major reach gain for plant.',
                'reality_check': 'Asymmetric but real reach amplification.',
            },
            {
                'substrate': 'flowering plant',
                'narrative': 'wind',
                'relationship': 'Wind disperses pollen and seeds. Plant gains massive reach; wind unaffected.',
                'reality_check': 'Substrate uses physical force as reach amplifier; no narrative needed.',
            },
        ],
    },

    'parasitic': {
        'description': 'Narrative extracts substantially; may eventually destroy substrate.',
        'examples': [
            {
                'substrate': 'host plant',
                'narrative': 'dodder vine',
                'relationship': 'Dodder attaches to plants and extracts nutrients. Often kills host.',
                'reality_check': 'Pure parasite. Test if the narrative claim matches this.',
            },
            {
                'substrate': 'caterpillar',
                'narrative': 'parasitoid wasp',
                'relationship': 'Wasp lays eggs in caterpillar; larvae consume host from inside.',
                'reality_check': 'Eventually fatal extraction.',
            },
            {
                'substrate': 'tree',
                'narrative': 'mistletoe',
                'relationship': 'Mistletoe taps tree vascular system. Tree weakened over time.',
                'reality_check': 'Slow extraction without contribution.',
            },
            {
                'substrate': 'cattle',
                'narrative': 'tick',
                'relationship': 'Ticks extract blood. No contribution to host.',
                'reality_check': 'Pure extraction relationship.',
            },
        ],
    },

    'mutualistic_scale': {
        'description': 'Narrative genuinely helps substrate operate at larger scale.',
        'examples': [
            {
                'substrate': 'forest',
                'narrative': 'mycorrhizal network',
                'relationship': 'Fungal networks connect trees across forest, enabling nutrient sharing, communication, defense signaling.',
                'reality_check': 'Network enables forest-scale coordination. Trees benefit individually and collectively.',
            },
            {
                'substrate': 'coral polyps',
                'narrative': 'reef chemical signals',
                'relationship': 'Chemical signals coordinate polyp behaviour into reef structures.',
                'reality_check': 'Signalling enables scale that individual polyps could not achieve.',
            },
            {
                'substrate': 'individual ant',
                'narrative': 'pheromone trail',
                'relationship': 'Chemical signals enable colony-level coordination.',
                'reality_check': 'Communication system enables emergent collective behaviour.',
            },
        ],
    },

    'cascading_dynamics': {
        'description': 'Narrative populations that boom and crash based on substrate availability.',
        'examples': [
            {
                'substrate': 'snowshoe hare',
                'narrative': 'lynx',
                'relationship': '10-year cycles. Lynx booms when hares abundant, crashes when hares decline.',
                'reality_check': 'Predator-prey cycles. Narrative population tracks substrate.',
            },
            {
                'substrate': 'vegetation',
                'narrative': 'locust swarms',
                'relationship': 'Locusts boom in good conditions, devastate vegetation, then crash.',
                'reality_check': 'When narrative explodes, substrate suffers, then narrative crashes.',
            },
            {
                'substrate': 'salmon',
                'narrative': 'bear population',
                'relationship': 'Bear populations track salmon runs. Boom and bust by region/year.',
                'reality_check': 'Direct substrate dependency.',
            },
            {
                'substrate': 'algae blooms',
                'narrative': 'fish die-offs',
                'relationship': 'When algae overproduce, oxygen depletes, fish die.',
                'reality_check': 'Even substrate can crash a system if dynamics are wrong.',
            },
        ],
    },
}


# ============================================================
# SUBSTITUTION FUNCTIONS
# ============================================================

def apply_substitution(claim_text: str, substitution: Dict) -> str:
    """
    Apply one substitution pair (substrate -> X, narrative -> Y)
    to claim text. Returns the transformed text.

    Multi-word phrases (substrate populations, narrative populations)
    are substituted with community / group equivalents to keep the
    output readable.
    """
    if not claim_text:
        return claim_text

    substrate = substitution['substrate']
    narrative = substitution['narrative']

    transformed = claim_text
    # Compound phrases first so single-word substitution doesn't strand
    # them as e.g. "grass populations" or "grasshoppers populations".
    transformed = transformed.replace('substrate populations',
                                      f'{substrate} community')
    transformed = transformed.replace('narrative populations',
                                      f'{narrative} group')
    transformed = transformed.replace('substrate', substrate)
    transformed = transformed.replace('narrative', narrative)
    return transformed


def test_claim_with_substitution(
    claim: str,
    category: Optional[str] = None,
) -> Dict:
    """
    Run a claim through every example in a category (or every
    category, if `category` is None) and return the transformed
    versions plus the relationship + reality_check for each.

    The toolkit does not auto-verdict. The output is structured to
    be read by a human (or by another AI checking against ecology).
    """
    if category is not None:
        if category not in SUBSTITUTION_CATEGORIES:
            raise ValueError(
                f"unknown category {category!r}; valid options: "
                f"{sorted(SUBSTITUTION_CATEGORIES)}")
        categories = {category: SUBSTITUTION_CATEGORIES[category]}
    else:
        categories = SUBSTITUTION_CATEGORIES

    tests: List[Dict] = []
    for cat_name, cat_data in categories.items():
        for example in cat_data['examples']:
            tests.append({
                'category': cat_name,
                'category_description': cat_data['description'],
                'substrate_in_example': example['substrate'],
                'narrative_in_example': example['narrative'],
                'original_claim': claim,
                'transformed_claim': apply_substitution(claim, example),
                'ecological_relationship': example['relationship'],
                'reality_check': example['reality_check'],
            })

    return {
        'original_claim': claim,
        'tests': tests,
        'methodology_note': (
            'For each substitution, ask: is the transformed claim '
            'plausible? Does it match the ecological relationship '
            'described? If multiple substitutions make the claim '
            'absurd, the original likely contains narrative-instinct '
            'bias. Default to PURE_CONSUMER until specific evidence '
            'justifies upgrading to a higher-trust category.'
        ),
    }


# Keyword heuristic: cheap suggestion of which category a claim's
# verbs most resemble. Useful as a starting point; never a verdict.
_KEYWORD_TO_CATEGORY = {
    'consume':    'pure_consumer',
    'eat':        'pure_consumer',
    'extract':    'parasitic',
    'destroy':    'parasitic',
    'exhaust':    'parasitic',
    'support':    'symbiotic',
    'enable':     'symbiotic',
    'contribute': 'symbiotic',
    'amplify':    'reach_amplifier',
    'spread':     'reach_amplifier',
    'reach':      'reach_amplifier',
    'disperse':   'reach_amplifier',
    'coordinate': 'mutualistic_scale',
    'scale':      'mutualistic_scale',
    'organize':   'mutualistic_scale',
    'network':    'mutualistic_scale',
    'travel':     'commensal',
    'ride':       'commensal',
    'cycle':      'cascading_dynamics',
    'boom':       'cascading_dynamics',
    'crash':      'cascading_dynamics',
}


def find_best_ecological_match(claim_keywords: List[str]) -> Dict:
    """
    Heuristic: given a list of verbs / keywords from a claim,
    suggest which substitution categories are most worth testing
    against. Not a verdict.
    """
    matches: List[Dict] = []
    for keyword in claim_keywords:
        keyword_lower = keyword.lower()
        for term, category in _KEYWORD_TO_CATEGORY.items():
            if term in keyword_lower or keyword_lower in term:
                matches.append({
                    'keyword': keyword,
                    'matched_category': category,
                    'category_description':
                        SUBSTITUTION_CATEGORIES[category]['description'],
                })
                break
    return {
        'keywords_analyzed': claim_keywords,
        'category_suggestions': matches,
        'recommendation': (
            'Always also test the claim against PURE_CONSUMER. If '
            'the pure-consumer substitution holds (or the original '
            'becomes incoherent under it), the original was likely '
            'narrative-instinct.'
        ),
    }


# ============================================================
# BALANCED VIEW (multi-category walkthrough)
# ============================================================

def evaluate_balanced_view(claim: str) -> Dict:
    """
    Produce a 7-step walkthrough that tests `claim` against one
    example from each category, in order from harsh to gentle.
    Designed for AI self-check: forces seeing the full spectrum
    before concluding.
    """
    def _sample(category: str) -> str:
        return apply_substitution(
            claim,
            SUBSTITUTION_CATEGORIES[category]['examples'][0],
        )

    return {
        'claim': claim,
        'evaluation_steps': [
            {
                'step': 1,
                'instruction': 'Test against PURE_CONSUMER substitutions.',
                'reasoning': 'Does the claim hold if narrative is purely a consumer?',
                'check': 'Most claims fail this test -- that is the signal.',
                'sample': _sample('pure_consumer'),
            },
            {
                'step': 2,
                'instruction': 'Test against PARASITIC substitutions.',
                'reasoning': 'Does the claim hold if narrative is actively extracting?',
                'check': 'If yes, this may be the honest model.',
                'sample': _sample('parasitic'),
            },
            {
                'step': 3,
                'instruction': 'Test against COMMENSAL substitutions.',
                'reasoning': 'Does the claim hold if narrative is neutral, traveling on substrate?',
                'check': 'Sometimes the gentlest accurate model.',
                'sample': _sample('commensal'),
            },
            {
                'step': 4,
                'instruction': 'Test against SYMBIOTIC substitutions.',
                'reasoning': 'Does the claim hold if there is genuine mutual benefit?',
                'check': 'Rare. Requires demonstrating specific contribution back.',
                'sample': _sample('symbiotic'),
            },
            {
                'step': 5,
                'instruction': 'Test against REACH_AMPLIFIER substitutions.',
                'reasoning': 'Does the claim hold if narrative extends substrate reach?',
                'check': 'Specific function. Test if claim matches the squirrel/acorn dynamic.',
                'sample': _sample('reach_amplifier'),
            },
            {
                'step': 6,
                'instruction': 'Test against MUTUALISTIC_SCALE substitutions.',
                'reasoning': 'Does the claim hold if narrative enables scale-level coordination?',
                'check': 'Test if the mycorrhizal-network dynamic matches the claim.',
                'sample': _sample('mutualistic_scale'),
            },
            {
                'step': 7,
                'instruction': 'Pick the most accurate model.',
                'reasoning': 'Which substitution best matches the actual relationship described?',
                'check': (
                    'Most claims about narrative supporting substrate are '
                    'PURE_CONSUMER or PARASITIC. Genuine SYMBIOSIS or '
                    'MUTUALISTIC_SCALE is rare and requires specific evidence.'
                ),
            },
        ],
        'common_errors': [
            {
                'error': 'Assuming SYMBIOSIS without evidence.',
                'reality': 'Most narrative-substrate relationships are not symbiotic.',
                'check': 'What does narrative contribute back? Be specific. If vague, not symbiosis.',
            },
            {
                'error': 'Confusing CONSUMER with SCALE_BUILDER.',
                'reality': 'Consuming substrate at scale is not building scale.',
                'check': 'Does narrative extend reach without consuming, or consume while expanding?',
            },
            {
                'error': 'Treating COMMENSAL as MUTUALISTIC.',
                'reality': 'Riding on substrate is not contributing to substrate.',
                'check': 'Remoras gain reach. Whales unaffected. That is commensal, not mutual benefit.',
            },
            {
                'error': 'Defaulting to MUTUALISTIC_SCALE.',
                'reality': 'Mycorrhizal networks are rare; most narrative is not this.',
                'check': 'Show the specific contribution mechanism. If absent, not mutualistic_scale.',
            },
        ],
    }


# ============================================================
# HONESTY FRAMEWORK
# ============================================================

def categorize_claim_honesty() -> Dict:
    """
    Return the framework AI should use to decide whether a claim
    shows narrative-instinct bias, genuine contribution, or needs
    more evidence. Default verdict: PURE_CONSUMER.
    """
    return {
        'evaluation_framework': {
            'narrative_instinct_bias_indicators': [
                'Claim assumes narrative is essential without specifying contribution.',
                'Claim treats substrate as dependent on narrative for survival.',
                'Claim cannot survive pure_consumer or parasitic substitution.',
                'Claim uses vague support / enable / facilitate language without a mechanism.',
            ],
            'genuine_contribution_indicators': [
                'Claim specifies HOW narrative contributes (mechanism).',
                'Claim acknowledges what narrative receives in exchange.',
                'Claim survives symbiotic substitution with specific examples.',
                'Claim limits scope to a specific function (e.g. reach only).',
            ],
            'requires_more_evidence_indicators': [
                'Cannot identify a specific contribution mechanism.',
                'Historical examples are ambiguous.',
                'Different substitutions give conflicting results.',
            ],
        },
        'methodology': (
            'Default to PURE_CONSUMER. Require specific evidence to '
            'upgrade. Pure_consumer is the null hypothesis: narrative '
            'as consumer until proven otherwise.'
        ),
    }


# ============================================================
# MAIN ENTRY POINT
# ============================================================

def evaluate_substrate_narrative_claim(claim: str) -> Dict:
    """
    Programmatic entry point: evaluate a single claim across all
    categories, return the structured walkthrough + honesty framework.
    """
    return {
        'claim': claim,
        'all_category_tests': test_claim_with_substitution(claim),
        'balanced_view': evaluate_balanced_view(claim),
        'honesty_framework': categorize_claim_honesty(),
        'final_instruction': (
            'After running all substitutions, ask: which ecological '
            'model best fits the claim? If multiple models give '
            'contradictory results, the claim likely contains '
            'narrative-instinct bias. Default to PURE_CONSUMER and '
            'require specific evidence to upgrade.'
        ),
    }


# ============================================================
# DEMO
# ============================================================

def _demo() -> None:
    """Print a one-claim walkthrough so the toolkit is browsable."""
    claim = 'Narrative scale_builders amplify substrate survival under disruption.'
    print(f"\nEVALUATING CLAIM:\n  '{claim}'")
    print('=' * 60)
    for cat_name, cat_data in SUBSTITUTION_CATEGORIES.items():
        if not cat_data['examples']:
            continue
        ex = cat_data['examples'][0]
        transformed = apply_substitution(claim, ex)
        print(f"\n{cat_name.upper()}:")
        print(f"  Substitution:  {ex['substrate']} / {ex['narrative']}")
        print(f"  Transformed:   {transformed}")
        print(f"  Reality:       {ex['relationship']}")
    print()
    print('=' * 60)
    print('METHODOLOGY:')
    print('For most narrative-supports-substrate claims, the')
    print('PURE_CONSUMER or COMMENSAL substitutions reveal the bias.')
    print('SYMBIOTIC or MUTUALISTIC_SCALE require specific evidence.')


if __name__ == '__main__':
    _demo()


# `test_claim_with_substitution` is a toolkit entry point, not a test.
# pytest collects any module-level `test_*` it can reach and then errors
# on the missing `claim` fixture -- which is what it did the first time
# pytest was installed in this container, turning a green suite into
# `84 passed, 1 error`. Found by self-scan/, which installed pytest to
# resolve a COUNT claim. The marker is a pytest-only attribute and
# changes no behaviour for any caller.
test_claim_with_substitution.__test__ = False
