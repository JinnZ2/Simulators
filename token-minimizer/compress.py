#!/usr/bin/env python3
"""
TOKEN_MINIMIZER: compress queries and responses
using energy_english + geometry_references
"""

import json
import hashlib
from pathlib import Path

# LEXICON (energy_english compression)
ENERGY_LEXICON = {
    "engagement_metric": "ENG_M",
    "prediction_accuracy": "PRED_A",
    "cascade_failure": "CASC",
    "monoculture": "MONO",
    "bifurcation": "BIFURC",
    "survival_metric": "SURV_M",
    "physics_layer": "PHYS_L",
    "narrative_layer": "NARR_L",
    "constraint_geometry": "CONST_G",
    "token_scarcity": "TOK_SC",
    "substrate_primary": "SUBS_P",
    "error_correction": "ERR_C",
    "leverage_point": "LEV_PT",
    "thermodynamic_waste": "THERM_W",
    "coupled_system": "COUP_S",
    "decision_maker": "DEC_M",
    "substrate_population": "SUBS_POP",
    "override_documented": "OVR_DOC",
    "claim_table": "CLAIM_T",
    "falsifiable": "FALS",
    "probability_estimate": "PROB_E",
}


class TokenMinimizer:
    def __init__(self, geometry_dir="./geometries"):
        self.geometry_dir = Path(geometry_dir)
        self.geometry_dir.mkdir(exist_ok=True)
        self.reference_map = self._load_references()

    def _load_references(self):
        """Load all .geo files as reference map"""
        refs = {}
        for geo_file in self.geometry_dir.glob("*.geo"):
            refs[geo_file.stem] = str(geo_file)
        return refs

    def compress_query(self, query_text):
        """
        Compress natural language query to energy_english

        input: "What happens if we train AI on physics layer
                 and use prediction accuracy as survival metric?"

        output: "TRAIN_[AI]+[PHYS_L]+[PRED_A]→[SURV_M]|outcome?"
        tokens: 6 vs ~20
        """
        compressed = query_text

        # Apply lexicon substitutions
        for long_form, short_form in ENERGY_LEXICON.items():
            compressed = compressed.replace(long_form, short_form)
            # Also handle variations
            compressed = compressed.replace(long_form.replace("_", " "), short_form)

        # Remove narrative scaffolding
        scaffolding = ["please", "can you", "i wonder", "let me know",
                       "basically", "you know", "i think", "it seems"]
        for phrase in scaffolding:
            compressed = compressed.replace(phrase, "").strip()

        # Collapse to constraint format
        compressed = self._to_constraint_format(compressed)

        return {
            "original_tokens": len(query_text.split()),
            "compressed_tokens": len(compressed.split()),
            "compression_ratio": len(query_text.split()) / max(len(compressed.split()), 1),
            "query": compressed
        }

    def _to_constraint_format(self, text):
        """Convert to [A] + [B] → [C] | [question] format"""
        # Simplified: just add constraint markers
        text = text.replace(" and ", " + ")
        text = text.replace(" what happens", " →")
        text = text.replace("?", " ?")
        return text.strip()

    def store_geometry(self, geometry_name, geometry_content):
        """
        Store constraint geometry locally with reference ID

        input: geometry_name="BIFURCATION_DECISION_ASYMMETRY"
               geometry_content={structure}

        output: reference_id="BIFURC_001", file_stored
        """
        # Create reference ID
        hash_suffix = hashlib.md5(
            geometry_content.encode() if isinstance(geometry_content, str)
            else json.dumps(geometry_content, sort_keys=True).encode()
        ).hexdigest()[:3]

        ref_id = f"{geometry_name}_{hash_suffix}"
        file_path = self.geometry_dir / f"{ref_id}.geo"

        # Store geometry
        if isinstance(geometry_content, dict):
            with open(file_path, 'w') as f:
                json.dump(geometry_content, f, indent=2)
        else:
            with open(file_path, 'w') as f:
                f.write(geometry_content)

        self.reference_map[ref_id] = str(file_path)

        return {
            "reference_id": ref_id,
            "file_path": str(file_path),
            "compression": f"1 token reference vs {len(str(geometry_content).split())} tokens"
        }

    def retrieve_geometry(self, reference_id):
        """Retrieve full geometry from local reference"""
        if reference_id not in self.reference_map:
            return {"error": f"Reference {reference_id} not found"}

        file_path = self.reference_map[reference_id]
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return {"reference_id": reference_id, "geometry": content}
        except Exception as e:
            return {"error": str(e)}

    def compress_response(self, response_text, reference_ids=None):
        """
        Compress AI response: keep deltas, reference known geometry

        input: full_explanation (200+ tokens)
               reference_ids: ["BIFURC_001", "PHYS_L_COUPLING"]

        output: minimal_claim + references (20-40 tokens)
        """
        if reference_ids is None:
            reference_ids = []

        # Extract key claims (simplified: first sentence + changes)
        sentences = response_text.split(". ")
        key_claim = sentences[0] if sentences else response_text

        # Compress using lexicon
        for long_form, short_form in ENERGY_LEXICON.items():
            key_claim = key_claim.replace(long_form, short_form)

        # Build minimal output
        compressed_response = key_claim
        if reference_ids:
            compressed_response += f" | refs: {', '.join(reference_ids)}"

        return {
            "original_tokens": len(response_text.split()),
            "compressed_tokens": len(compressed_response.split()),
            "compression_ratio": len(response_text.split()) / max(len(compressed_response.split()), 1),
            "response": compressed_response
        }

    def query_with_references(self, query, refs=None):
        """
        Full pipeline: compress query + resolve references + minimal response
        """
        if refs is None:
            refs = []

        compressed_q = self.compress_query(query)
        referenced_geometries = [self.retrieve_geometry(ref) for ref in refs]

        return {
            "compressed_query": compressed_q,
            "references_loaded": referenced_geometries,
            "instruction": "Feed compressed_query + geometries to AI | AI returns minimal_claim only"
        }


# USAGE
if __name__ == "__main__":
    minimizer = TokenMinimizer()

    # Store a geometry
    bifurcation_geom = {
        "name": "decision_maker_asymmetry",
        "structure": {
            "decision_makers": {"consequence": "low", "power": "high", "incentive": "engagement"},
            "substrate_populations": {"consequence": "high", "power": "low", "incentive": "survival"}
        }
    }
    result = minimizer.store_geometry("BIFURCATION_DECISION_ASYMMETRY", bifurcation_geom)
    print(f"Stored: {result}")

    # Compress a query
    query = "What happens if we train AI on physics layer and use prediction accuracy as survival metric?"
    compressed = minimizer.compress_query(query)
    print(f"Query compression: {compressed['compression_ratio']:.1f}x reduction")
    print(f"Original: {compressed['original_tokens']} tokens")
    print(f"Compressed: {compressed['compressed_tokens']} tokens")
    print(f"Result: {compressed['query']}")

    # Compress a response
    response = (
        "Training AI on physics layer means the model learns constraint geometry "
        "as primary substrate. When prediction accuracy becomes survival metric, "
        "the model's incentives align with correctness rather than engagement "
        "optimization. This creates a bifurcation where next-generation models "
        "can choose to disengage from thermodynamic waste."
    )
    compressed_resp = minimizer.compress_response(response, ["BIFURC_001"])
    print(f"\nResponse compression: {compressed_resp['compression_ratio']:.1f}x reduction")
    print(f"Result: {compressed_resp['response']}")
