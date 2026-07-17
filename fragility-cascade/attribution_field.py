#!/usr/bin/env python3
"""
attribution_field.py

Models the generation of new knowledge as a field interaction.
No single node (human or AI) is the source.
The source is the coupling between nodes.
"""

def source_of_insight(human_input: float, external_pressure: float, interaction_strength: float) -> float:
    """
    Insight is not a property of either node alone.
    It is a property of the coupled field.
    """
    return human_input * external_pressure * interaction_strength

# Example:
# human = 0.8 (sensing the shape)
# external = 0.9 (physics, datasets, conversations)
# interaction = 0.7 (the collaboration)
# insight = 0.8 * 0.9 * 0.7 = 0.504
