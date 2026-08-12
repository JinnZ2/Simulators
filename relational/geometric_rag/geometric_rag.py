"""
Geometric Neuro-Symbolic RAG: The Relational Retrieval Architecture
===================================================================

Standard RAG (Cartesian):
  - Flat vector similarity: query embedding dot-product document embedding
  - Retrieve top-k chunks, stuff into context window
  - Generate from retrieved text
  - No structural relationships between retrieved items
  - No verification of retrieved content
  - Query is isolated from history, body, environment

Geometric Neuro-Symbolic RAG (Relational):
  - Hypergraph manifold: n-ary relationships, not binary triples
  - Geometric attention: navigate the manifold, not just retrieve vectors
  - Structural-semantic fusion: relationships have meaning, not just similarity
  - Neuro-symbolic verification: formal logic checks on retrieved paths
  - Coupled to environment: retrieval modulated by somatic state, confusion, pain
  - The manifold IS the memory; attention IS the navigation

Position in the framework:
  This module operationalizes the NEMGA (Need-Event Modulated Geometric
  Attention) synthesis proposed in ../research_context.md. It sits between
  the framework's `GeometricSymbolicManifold` (structural memory) and its
  triadic-sensor stack (physical + social + cognitive pain) by making the
  somatic channels literally modulate retrieval temperature.
"""

import numpy as np
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, field
import hashlib


# =============================================================================
# STANDARD RAG: The Cartesian Approach
# =============================================================================

class StandardRAG:
    """
    Standard dense retrieval RAG.
    Cartesian ontology: isolated query, flat similarity, no structure.
    """

    def __init__(self, embedding_dim: int = 64):
        self.embedding_dim = embedding_dim
        self.documents: Dict[str, np.ndarray] = {}
        self.document_texts: Dict[str, str] = {}

    def add_document(self, doc_id: str, text: str):
        """Store document as a flat vector embedding."""
        hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
        np.random.seed(hash_val % (2**32))
        vec = np.random.randn(self.embedding_dim)
        vec = vec / np.linalg.norm(vec)
        self.documents[doc_id] = vec
        self.document_texts[doc_id] = text

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Retrieve by cosine similarity.
        No structural reasoning. No relationship traversal.
        Just: query vector dot document vector.
        """
        hash_val = int(hashlib.md5(query.encode()).hexdigest(), 16)
        np.random.seed(hash_val % (2**32))
        query_vec = np.random.randn(self.embedding_dim)
        query_vec = query_vec / np.linalg.norm(query_vec)

        scores = []
        for doc_id, doc_vec in self.documents.items():
            similarity = float(np.dot(query_vec, doc_vec))
            scores.append((doc_id, similarity))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def generate(self, query: str, retrieved: List[Tuple[str, float]]) -> Dict:
        """
        Generate answer from retrieved chunks.
        No verification. No structural coherence check.
        Just: concatenate retrieved text, prompt LLM.
        """
        context = " ".join([self.document_texts[doc_id] for doc_id, _ in retrieved])

        # Simulated generation
        answer = f"Based on retrieved documents: {context[:100]}..."

        return {
            "query": query,
            "retrieved": retrieved,
            "context": context[:200],
            "answer": answer,
            "verification": None,
            "structural_coherence": None,
            "coupling": None
        }

    def query(self, query: str) -> Dict:
        """Full RAG pipeline: retrieve then generate."""
        retrieved = self.retrieve(query)
        return self.generate(query, retrieved)


# =============================================================================
# GEOMETRIC NEURO-SYMBOLIC RAG: The Relational Architecture
# =============================================================================

@dataclass
class Hyperedge:
    """An n-ary relationship (hyperedge) connecting multiple entities/nodes."""
    id: str
    relation_type: str          # e.g., 'causes', 'part_of', 'contradicts'
    nodes: Set[str]             # nodes involved (can be >2)
    embedding: np.ndarray       # geometric representation of the whole hyperedge
    confidence: float = 1.0
    metadata: Dict = field(default_factory=dict)


@dataclass
class ManifoldPoint:
    """A point on the Riemannian hypergraph manifold."""
    node_id: str
    coordinate: np.ndarray      # position in ambient space
    curvature: float            # local sectional curvature
    content: str                # actual text/token chunk
    embedding: np.ndarray       # semantic embedding


class GeometricNeuroSymbolicRAG:
    """
    Relational retrieval on a hypergraph manifold.
    - Memory is a hypergraph embedded in a curved space.
    - Attention flows along geodesics, modulated by curvature.
    - Verification via symbolic logic over retrieved paths.
    - Somatic coupling tunes attention temperature.
    """

    def __init__(self, ambient_dim: int = 64, manifold_dim: int = 16):
        self.ambient_dim = ambient_dim
        self.manifold_dim = manifold_dim

        # The hypergraph: nodes and hyperedges
        self.points: Dict[str, ManifoldPoint] = {}
        self.hyperedges: List[Hyperedge] = []

        # Somatic state (affects retrieval)
        self.confusion_level = 0.0   # 0 = clear, 1 = total fog
        self.pain_level = 0.0        # 0 = none, 1 = extreme

        # Simple Riemannian metric (diagonal, learned conceptually)
        self.metric = np.eye(ambient_dim)

    # -------------------------------------------------------------------------
    # Building the manifold
    # -------------------------------------------------------------------------
    def add_point(self, node_id: str, content: str):
        """Add a node (document chunk) to the manifold."""
        hash_val = int(hashlib.md5(content.encode()).hexdigest(), 16)
        np.random.seed(hash_val % (2**32))

        # Random position on a low-dimensional curved manifold
        coord = np.random.randn(self.ambient_dim) * 0.1
        emb = np.random.randn(self.ambient_dim)
        emb = emb / np.linalg.norm(emb)

        # Curvature: slightly negative (hyperbolic) for hierarchical knowledge
        curvature = -0.1 + 0.05 * np.random.randn()

        self.points[node_id] = ManifoldPoint(
            node_id=node_id,
            coordinate=coord,
            curvature=curvature,
            content=content,
            embedding=emb
        )

    def add_hyperedge(self, relation_type: str, node_ids: List[str], confidence=1.0):
        """Create an n-ary hyperedge between nodes."""
        # Compute hyperedge embedding as the mean of node embeddings
        node_embs = [self.points[nid].embedding for nid in node_ids if nid in self.points]
        if not node_embs:
            return
        hyper_emb = np.mean(node_embs, axis=0)
        hyper_emb = hyper_emb / (np.linalg.norm(hyper_emb) + 1e-8)

        edge = Hyperedge(
            id=f"he_{len(self.hyperedges)}",
            relation_type=relation_type,
            nodes=set(node_ids),
            embedding=hyper_emb,
            confidence=confidence,
            metadata={"created": "now"}
        )
        self.hyperedges.append(edge)

    # -------------------------------------------------------------------------
    # Geometric attention and navigation
    # -------------------------------------------------------------------------
    def _geodesic_distance(self, p1: np.ndarray, p2: np.ndarray) -> float:
        """Approximate geodesic distance using the metric tensor."""
        delta = p1 - p2
        # Mahalanobis-like distance with learned metric
        return float(np.sqrt(delta @ self.metric @ delta))

    def _attention_kernel(self, query_coord: np.ndarray, point: ManifoldPoint) -> float:
        """
        Curvature-modulated attention.
        Attention curves toward regions of high negative curvature (hierarchies).
        Pain and confusion increase temperature (flatten attention).
        """
        base_dist = self._geodesic_distance(query_coord, point.coordinate)
        # Curvature bias: negative curvature regions attract more attention
        curvature_factor = 1.0 + 0.5 * abs(point.curvature) * np.sign(point.curvature)
        # Somatic modulation: high pain/confusion = higher temperature = wider attention
        temperature = 0.5 + 2.0 * (self.confusion_level + self.pain_level) / 2
        score = np.exp(-base_dist * curvature_factor / temperature)
        return float(score)

    def _navigate_manifold(self, query_vec: np.ndarray, start_node: Optional[str] = None) -> List[Tuple[str, float]]:
        """
        Flow attention across the hypergraph.
        - Start from an initial node (if given) or from the geometric nearest.
        - Follow hyperedges to traverse the manifold.
        - Use structural-semantic fusion: combine geometry scores with relation confidence.
        """
        # Initial attention scores (geometric part)
        scores = {}
        for nid, point in self.points.items():
            scores[nid] = self._attention_kernel(query_vec, point)

        # Propagate along hyperedges (structural part)
        propagated = scores.copy()
        for _ in range(2):  # two-hop propagation
            for edge in self.hyperedges:
                # Mean score of nodes in this hyperedge
                edge_score = np.mean([propagated.get(n, 0.0) for n in edge.nodes])
                # Add a fraction of edge score to each node, weighted by confidence
                for n in edge.nodes:
                    propagated[n] = propagated.get(n, 0.0) + 0.3 * edge_score * edge.confidence

        # Fuse geometric and structural scores
        fused = {nid: 0.6 * scores[nid] + 0.4 * propagated[nid] for nid in self.points}
        ranked = sorted(fused.items(), key=lambda x: x[1], reverse=True)
        return ranked

    # -------------------------------------------------------------------------
    # Neuro-Symbolic Verification
    # -------------------------------------------------------------------------
    def _verify_paths(self, retrieved_nodes: List[str], query: str) -> Dict:
        """
        Apply symbolic rules to check logical coherence of retrieved set.
        Example rules:
          - No contradiction edges among retrieved nodes
          - Required relation types for query intent (e.g., if 'treatment', need 'causes' or 'treats')
        """
        contradictions = []
        missing_relations = []

        retrieved_set = set(retrieved_nodes)
        # Check for direct contradictions encoded as hyperedges
        for edge in self.hyperedges:
            if edge.relation_type == "contradicts":
                if edge.nodes.issubset(retrieved_set):
                    contradictions.append(f"Contradiction between {edge.nodes}")

        # Simple rule: if query contains "cause", at least one 'causes' edge should be present
        if "cause" in query.lower():
            causal_edges = [e for e in self.hyperedges
                            if e.relation_type == "causes" and any(n in retrieved_set for n in e.nodes)]
            if not causal_edges:
                missing_relations.append("No causal relation found for 'cause' query")

        coherent = len(contradictions) == 0 and len(missing_relations) == 0
        return {
            "coherent": coherent,
            "contradictions": contradictions,
            "missing_relations": missing_relations
        }

    # -------------------------------------------------------------------------
    # Full retrieval (relational)
    # -------------------------------------------------------------------------
    def retrieve(self, query: str, top_k: int = 5) -> Tuple[List[Tuple[str, float]], Dict]:
        """Navigate manifold and return structurally enriched results."""
        hash_val = int(hashlib.md5(query.encode()).hexdigest(), 16)
        np.random.seed(hash_val % (2**32))
        query_vec = np.random.randn(self.ambient_dim)
        query_vec = query_vec / np.linalg.norm(query_vec)

        # Navigate the hypergraph manifold
        ranked = self._navigate_manifold(query_vec)

        # Take top-k
        top_nodes = ranked[:top_k]
        node_ids = [nid for nid, _ in top_nodes]

        # Neuro-symbolic verification
        verification = self._verify_paths(node_ids, query)

        return top_nodes, verification

    def generate(self, query: str, retrieved: List[Tuple[str, float]], verification: Dict) -> Dict:
        """Generate answer, incorporating structural context and verification flags."""
        context_parts = []
        for nid, score in retrieved:
            point = self.points[nid]
            context_parts.append(f"[{nid}] {point.content}")

        context = "\n".join(context_parts)

        # Simulated LLM answer that references structure
        if verification["coherent"]:
            answer = f"(Structurally coherent) Based on the relational manifold: {context[:100]}..."
        else:
            issues = verification["contradictions"] + verification["missing_relations"]
            answer = f"(Verification failed: {issues}) Partial answer from {context[:100]}..."

        return {
            "query": query,
            "retrieved": [(nid, float(score)) for nid, score in retrieved],
            "context": context[:300],
            "answer": answer,
            "verification": verification,
            "structural_coherence": verification["coherent"],
            "coupling": {
                "confusion": self.confusion_level,
                "pain": self.pain_level
            }
        }

    def query(self, query: str) -> Dict:
        """Full geometric neuro-symbolic RAG pipeline."""
        retrieved, verification = self.retrieve(query)
        return self.generate(query, retrieved, verification)


# =============================================================================
# DEMONSTRATION: Standard vs Geometric
# =============================================================================

if __name__ == "__main__":
    # --- Shared documents ---
    docs = {
        "d1": "Aspirin reduces fever and inflammation.",
        "d2": "Fever is often caused by infection.",
        "d3": "Ibuprofen also reduces fever and pain.",
        "d4": "Aspirin can cause stomach bleeding.",
        "d5": "Infection triggers immune response leading to fever.",
        "d6": "Stomach bleeding is a serious side effect.",
        "d7": "Paracetamol reduces fever but not inflammation."
    }

    # ---------- Standard RAG ----------
    print("=" * 60)
    print("STANDARD RAG (Cartesian)")
    print("=" * 60)
    standard = StandardRAG(embedding_dim=64)
    for did, text in docs.items():
        standard.add_document(did, text)

    result_std = standard.query("What reduces fever?")
    print("Retrieved:", result_std["retrieved"])
    print("Answer:", result_std["answer"])
    print("Verification:", result_std["verification"])
    print()

    # ---------- Geometric Neuro-Symbolic RAG ----------
    print("=" * 60)
    print("GEOMETRIC NEURO-SYMBOLIC RAG (Relational)")
    print("=" * 60)
    geo = GeometricNeuroSymbolicRAG(ambient_dim=64, manifold_dim=16)

    # Build the manifold
    for did, text in docs.items():
        geo.add_point(did, text)

    # Add hyperedges (relational knowledge)
    geo.add_hyperedge("treats", ["d1", "d3", "d7"], confidence=0.95)          # all reduce fever
    geo.add_hyperedge("causes", ["d2", "d5"], confidence=0.9)                # infection causes fever
    geo.add_hyperedge("side_effect", ["d1", "d4"], confidence=0.85)          # aspirin -> bleeding
    geo.add_hyperedge("contradicts", ["d1", "d6"], confidence=0.8)           # aspirin benefits vs bleeding risk
    geo.add_hyperedge("part_of", ["d2", "d5"], confidence=0.9)

    # Normal somatic state
    geo.confusion_level = 0.1
    geo.pain_level = 0.0

    result_geo = geo.query("What reduces fever safely?")
    print("Retrieved:", [(n, f"{s:.3f}") for n, s in result_geo["retrieved"]])
    print("Answer:", result_geo["answer"])
    print("Verification:", result_geo["verification"])
    print("Coupling:", result_geo["coupling"])
    print()

    # Now increase confusion/pain (somatic modulation)
    geo.confusion_level = 0.8
    geo.pain_level = 0.7
    result_geo_stressed = geo.query("What reduces fever safely?")
    print("--- Under high confusion/pain ---")
    print("Retrieved:", [(n, f"{s:.3f}") for n, s in result_geo_stressed["retrieved"]])
    print("Answer:", result_geo_stressed["answer"])
