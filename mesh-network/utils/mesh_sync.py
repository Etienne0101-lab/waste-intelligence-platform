"""Mesh cluster synchronization and state management."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class MeshNode:
    """Represents a single sensor node in the mesh cluster."""
    node_id: str
    last_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    fill_level: float = 0.0
    mass_kg: float = 0.0
    battery_percent: int = 100
    is_active: bool = True


@dataclass
class MeshCluster:
    """Represents a collection of synchronized nodes."""
    cluster_id: str
    nodes: Dict[str, MeshNode] = field(default_factory=dict)
    facility_id: Optional[str] = None

    def add_node(self, node: MeshNode) -> None:
        """Add or update a node in the cluster."""
        self.nodes[node.node_id] = node
        logger.info(f"Node {node.node_id} registered in cluster {self.cluster_id}")

    def remove_node(self, node_id: str) -> None:
        """Remove a node from the cluster."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            logger.info(f"Node {node_id} removed from cluster {self.cluster_id}")

    def get_active_nodes(self) -> List[MeshNode]:
        """Return list of currently active nodes."""
        return [n for n in self.nodes.values() if n.is_active]

    def aggregate_state(self) -> Dict[str, float]:
        """Aggregate state across all active nodes."""
        active = self.get_active_nodes()
        if not active:
            return {"total_mass_kg": 0.0, "avg_fill_level": 0.0}

        return {
            "total_mass_kg": sum(n.mass_kg for n in active),
            "avg_fill_level": sum(n.fill_level for n in active) / len(active),
            "node_count": len(active),
        }
