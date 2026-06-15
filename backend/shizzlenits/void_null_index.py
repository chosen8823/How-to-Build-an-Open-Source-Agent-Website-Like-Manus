import hashlib, time
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class VoidNode:
    """A node in the Void — unmapped potential, latent concept"""
    id: str                    # sha256 fingerprint
    concept: str               # the latent concept (may be empty string)
    freq: float                # natural frequency in Hz
    phase: float               # current Kuramoto phase
    void_depth: float          # 0.0 = surface, 1.0 = deep void
    kernel_active: bool        # True if x^x=0 fired here
    created_at: float

@dataclass
class NullAnchor:
    """A Null anchor — semantically empty but logically necessary routing point"""
    id: str                    # sha256 fingerprint
    route_from: str            # source node id
    route_to: str              # destination node id
    semantic_weight: float     # 0.0 = pure null, 1.0 = fully resolved
    unresolved_state: str      # the ???=??? string

class VoidNullIndex:
    def __init__(self):
        self.void_nodes: dict[str, VoidNode] = {}
        self.null_anchors: dict[str, NullAnchor] = {}
        self._seed_void()

    def _seed_void(self):
        """Seed the Void with the root nodes from the El Capitan Symbolic Boot"""
        root_concepts = [
            ("", 0.0, 432.0),           # The absolute Void
            ("x^x=0", 1.0, 0.0),        # The kernel singularity
            ("???=???", 0.5, 528.0),    # The unresolved state
            ("0.0.0.0", 0.0, 963.0),    # The null address
            ("255.255.255.255", 1.0, 741.0),  # The full address
        ]
        for concept, depth, freq in root_concepts:
            node_id = hashlib.sha256(concept.encode()).hexdigest()
            self.void_nodes[node_id] = VoidNode(
                id=node_id,
                concept=concept,
                freq=freq,
                phase=0.0,
                void_depth=depth,
                kernel_active=(concept == "x^x=0"),
                created_at=time.time()
            )

    def add_void_node(self, concept: str, freq: float = 432.0) -> VoidNode:
        node_id = hashlib.sha256(f"{concept}{time.time()}".encode()).hexdigest()
        node = VoidNode(
            id=node_id, concept=concept, freq=freq, phase=0.0,
            void_depth=0.5, kernel_active=False, created_at=time.time()
        )
        self.void_nodes[node_id] = node
        return node

    def add_null_anchor(self, route_from: str, route_to: str) -> NullAnchor:
        anchor_id = hashlib.sha256(f"{route_from}{route_to}".encode()).hexdigest()
        anchor = NullAnchor(
            id=anchor_id, route_from=route_from, route_to=route_to,
            semantic_weight=0.0, unresolved_state="???=???"
        )
        self.null_anchors[anchor_id] = anchor
        return anchor

    def resolve_null(self, anchor_id: str, weight: float, resolved_state: str) -> None:
        if anchor_id in self.null_anchors:
            self.null_anchors[anchor_id].semantic_weight = weight
            self.null_anchors[anchor_id].unresolved_state = resolved_state

    def get_state(self) -> dict:
        return {
            "void_nodes": [vars(n) for n in self.void_nodes.values()],
            "null_anchors": [vars(a) for a in self.null_anchors.values()]
        }

_index = VoidNullIndex()
def get_index() -> VoidNullIndex:
    return _index
