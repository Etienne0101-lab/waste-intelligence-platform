"""Mesh cluster synchronization and state management."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional


@dataclass
class MeshNode:
    node_id: str
    last_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    fill_level: float = 0.0
    mass_kg: float = 0.0
    battery_percent: int = 100
    is_active: bool = True


@dataclass
class MeshCluster:
    cluster_id: str
    nodes: Dict[str, MeshNode] = field(default_factory=dict)
    facility_id: Optional[str] = None

    def add_node(self, node: MeshNode) -> None:
        self.nodes[node.node_id] = node

    def remove_node(self, node_id: str) -> None:
        if node_id in self.nodes:
            del self.nodes[node_id]

    def get_active_nodes(self) -> List[MeshNode]:
        return [n for n in self.nodes.values() if n.is_active]

    def aggregate_state(self) -> Dict[str, float]:
        active = self.get_active_nodes()
        if not active:
            return {"total_mass_kg": 0.0, "avg_fill_level": 0.0, "node_count": 0}
        return {
            "total_mass_kg": sum(n.mass_kg for n in active),
            "avg_fill_level": sum(n.fill_level for n in active) / len(active),
            "node_count": len(active),
        }
