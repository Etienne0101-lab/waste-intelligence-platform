"""
Waste-to-Resource Knowledge Graph (W2RKG) Schema

Organic waste-centric knowledge graph schema inspired by Nature Communications framework.
Defines node types, edge types, and their properties for the waste intelligence platform.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import json


class NodeType(Enum):
    """Node types in the W2RKG."""
    WASTE_TYPE = "Waste_Type"
    WASTE_STREAM = "Waste_Stream"
    PROCESS = "Process"
    RESOURCE = "Resource"
    FACILITY = "Facility"
    CONSTRAINT = "Constraint"
    ACTOR = "Actor"


class EdgeType(Enum):
    """Edge types in the W2RKG."""
    WASTECANBEPROCESSEDBY = "WASTECANBEPROCESSEDBY"
    PROCESSPRODUCESRESOURCE = "PROCESSPRODUCESRESOURCE"
    FACILITYSUPPORTSPROCESS = "FACILITYSUPPORTSPROCESS"
    FACILITYACCEPTSWASTE = "FACILITYACCEPTSWASTE"
    RESOURCEDEMANDEDBY_ACTOR = "RESOURCEDEMANDEDBY_ACTOR"
    CONSTRAINTAPPLIESTO = "CONSTRAINTAPPLIESTO"
    WASTESTREAMHASWASTETYPE = "WASTESTREAMHASWASTETYPE"
    FACILITYLOCATEDIN = "FACILITYLOCATEDIN"
    ACTOROPERATESFACILITY = "ACTOROPERATESFACILITY"


@dataclass
class Node:
    """Base node class for all W2RKG nodes."""
    node_id: str
    node_type: NodeType
    name: str
    description: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary representation."""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "name": self.name,
            "description": self.description,
            "properties": self.properties
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Node":
        """Create node from dictionary."""
        # Remove node_type from data before passing to __init__
        # since specialized classes already know their type
        init_data = {k: v for k, v in data.items() if k != "node_type"}
        return cls(**init_data)


@dataclass
class Edge:
    """Base edge class for all W2RKG edges."""
    edge_id: str
    edge_type: EdgeType
    source_id: str
    target_id: str
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert edge to dictionary representation."""
        return {
            "edge_id": self.edge_id,
            "edge_type": self.edge_type.value,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "properties": self.properties
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Edge":
        """Create edge from dictionary."""
        # Convert edge_type string to enum
        if isinstance(data.get("edge_type"), str):
            data["edge_type"] = EdgeType(data["edge_type"])
        return cls(**data)


@dataclass
class WasteType(Node):
    """Waste type node (e.g., FoodScraps, YardWaste)."""
    composition: Optional[Dict[str, float]] = None
    moisture_content: Optional[float] = None
    organic_content: Optional[float] = None
    
    def __init__(self, node_id: str, name: str, description: Optional[str] = None,
                 composition: Optional[Dict[str, float]] = None,
                 moisture_content: Optional[float] = None,
                 organic_content: Optional[float] = None,
                 properties: Optional[Dict[str, Any]] = None):
        super().__init__(
            node_id=node_id,
            node_type=NodeType.WASTE_TYPE,
            name=name,
            description=description,
            properties=properties or {}
        )
        self.composition = composition
        self.moisture_content = moisture_content
        self.organic_content = organic_content
        if composition:
            self.properties["composition"] = composition
        if moisture_content is not None:
            self.properties["moisture_content"] = moisture_content
        if organic_content is not None:
            self.properties["organic_content"] = organic_content


@dataclass
class WasteStream(Node):
    """Waste stream node (e.g., ResidentialOrganicsBrooklyn)."""
    source_location: Optional[str] = None
    volume_tonnes_per_year: Optional[float] = None
    collection_frequency: Optional[str] = None
    
    def __init__(self, node_id: str, name: str, description: Optional[str] = None,
                 source_location: Optional[str] = None,
                 volume_tonnes_per_year: Optional[float] = None,
                 collection_frequency: Optional[str] = None,
                 properties: Optional[Dict[str, Any]] = None):
        super().__init__(
            node_id=node_id,
            node_type=NodeType.WASTE_STREAM,
            name=name,
            description=description,
            properties=properties or {}
        )
        self.source_location = source_location
        self.volume_tonnes_per_year = volume_tonnes_per_year
        self.collection_frequency = collection_frequency
        if source_location:
            self.properties["source_location"] = source_location
        if volume_tonnes_per_year is not None:
            self.properties["volume_tonnes_per_year"] = volume_tonnes_per_year
        if collection_frequency:
            self.properties["collection_frequency"] = collection_frequency


@dataclass
class Process(Node):
    """Process node (e.g., AerobicComposting, AnaerobicDigestion)."""
    efficiency: Optional[float] = None
    processing_time_hours: Optional[float] = None
    energy_requirement_kwh_per_tonne: Optional[float] = None
    carbon_footprint_kg_co2_per_tonne: Optional[float] = None
    
    def __init__(self, node_id: str, name: str, description: Optional[str] = None,
                 efficiency: Optional[float] = None,
                 processing_time_hours: Optional[float] = None,
                 energy_requirement_kwh_per_tonne: Optional[float] = None,
                 carbon_footprint_kg_co2_per_tonne: Optional[float] = None,
                 properties: Optional[Dict[str, Any]] = None):
        super().__init__(
            node_id=node_id,
            node_type=NodeType.PROCESS,
            name=name,
            description=description,
            properties=properties or {}
        )
        self.efficiency = efficiency
        self.processing_time_hours = processing_time_hours
        self.energy_requirement_kwh_per_tonne = energy_requirement_kwh_per_tonne
        self.carbon_footprint_kg_co2_per_tonne = carbon_footprint_kg_co2_per_tonne
        if efficiency is not None:
            self.properties["efficiency"] = efficiency
        if processing_time_hours is not None:
            self.properties["processing_time_hours"] = processing_time_hours
        if energy_requirement_kwh_per_tonne is not None:
            self.properties["energy_requirement_kwh_per_tonne"] = energy_requirement_kwh_per_tonne
        if carbon_footprint_kg_co2_per_tonne is not None:
            self.properties["carbon_footprint_kg_co2_per_tonne"] = carbon_footprint_kg_co2_per_tonne


@dataclass
class Resource(Node):
    """Resource node (e.g., CompostAmendment, Biogas)."""
    economic_value_per_tonne: Optional[float] = None
    market_demand: Optional[str] = None
    quality_grade: Optional[str] = None
    
    def __init__(self, node_id: str, name: str, description: Optional[str] = None,
                 economic_value_per_tonne: Optional[float] = None,
                 market_demand: Optional[str] = None,
                 quality_grade: Optional[str] = None,
                 properties: Optional[Dict[str, Any]] = None):
        super().__init__(
            node_id=node_id,
            node_type=NodeType.RESOURCE,
            name=name,
            description=description,
            properties=properties or {}
        )
        self.economic_value_per_tonne = economic_value_per_tonne
        self.market_demand = market_demand
        self.quality_grade = quality_grade
        if economic_value_per_tonne is not None:
            self.properties["economic_value_per_tonne"] = economic_value_per_tonne
        if market_demand:
            self.properties["market_demand"] = market_demand
        if quality_grade:
            self.properties["quality_grade"] = quality_grade


@dataclass
class Facility(Node):
    """Facility node (e.g., FACILITY-BK-COMPOST-01)."""
    location: Optional[Dict[str, float]] = None
    capacity_tonnes_per_year: Optional[float] = None
    operational_status: Optional[str] = None
    contact_info: Optional[str] = None
    
    def __init__(self, node_id: str, name: str, description: Optional[str] = None,
                 location: Optional[Dict[str, float]] = None,
                 capacity_tonnes_per_year: Optional[float] = None,
                 operational_status: Optional[str] = None,
                 contact_info: Optional[str] = None,
                 properties: Optional[Dict[str, Any]] = None):
        super().__init__(
            node_id=node_id,
            node_type=NodeType.FACILITY,
            name=name,
            description=description,
            properties=properties or {}
        )
        self.location = location
        self.capacity_tonnes_per_year = capacity_tonnes_per_year
        self.operational_status = operational_status
        self.contact_info = contact_info
        if location:
            self.properties["location"] = location
        if capacity_tonnes_per_year is not None:
            self.properties["capacity_tonnes_per_year"] = capacity_tonnes_per_year
        if operational_status:
            self.properties["operational_status"] = operational_status
        if contact_info:
            self.properties["contact_info"] = contact_info


@dataclass
class Constraint(Node):
    """Constraint node (e.g., NYCRegulationOrganicWaste)."""
    constraint_type: Optional[str] = None
    severity: Optional[str] = None
    jurisdiction: Optional[str] = None
    
    def __init__(self, node_id: str, name: str, description: Optional[str] = None,
                 constraint_type: Optional[str] = None,
                 severity: Optional[str] = None,
                 jurisdiction: Optional[str] = None,
                 properties: Optional[Dict[str, Any]] = None):
        super().__init__(
            node_id=node_id,
            node_type=NodeType.CONSTRAINT,
            name=name,
            description=description,
            properties=properties or {}
        )
        self.constraint_type = constraint_type
        self.severity = severity
        self.jurisdiction = jurisdiction
        if constraint_type:
            self.properties["constraint_type"] = constraint_type
        if severity:
            self.properties["severity"] = severity
        if jurisdiction:
            self.properties["jurisdiction"] = jurisdiction


@dataclass
class Actor(Node):
    """Actor node (e.g., DSNY, PrivateHauler, UrbanFarm)."""
    actor_type: Optional[str] = None
    scale: Optional[str] = None
    
    def __init__(self, node_id: str, name: str, description: Optional[str] = None,
                 actor_type: Optional[str] = None,
                 scale: Optional[str] = None,
                 properties: Optional[Dict[str, Any]] = None):
        super().__init__(
            node_id=node_id,
            node_type=NodeType.ACTOR,
            name=name,
            description=description,
            properties=properties or {}
        )
        self.actor_type = actor_type
        self.scale = scale
        if actor_type:
            self.properties["actor_type"] = actor_type
        if scale:
            self.properties["scale"] = scale


@dataclass
class KnowledgeGraph:
    """Complete W2RKG graph structure."""
    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)
    
    def add_node(self, node: Node) -> None:
        """Add a node to the graph."""
        self.nodes[node.node_id] = node
    
    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph."""
        self.edges.append(edge)
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID."""
        return self.nodes.get(node_id)
    
    def get_edges_by_type(self, edge_type: EdgeType) -> List[Edge]:
        """Get all edges of a specific type."""
        return [e for e in self.edges if e.edge_type == edge_type]
    
    def get_edges_by_source(self, source_id: str) -> List[Edge]:
        """Get all edges originating from a node."""
        return [e for e in self.edges if e.source_id == source_id]
    
    def get_edges_by_target(self, target_id: str) -> List[Edge]:
        """Get all edges pointing to a node."""
        return [e for e in self.edges if e.target_id == target_id]
    
    def get_nodes_by_type(self, node_type: NodeType) -> List[Node]:
        """Get all nodes of a specific type."""
        return [n for n in self.nodes.values() if n.node_type == node_type]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entire graph to dictionary."""
        return {
            "nodes": {nid: n.to_dict() for nid, n in self.nodes.items()},
            "edges": [e.to_dict() for e in self.edges]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KnowledgeGraph":
        """Create graph from dictionary."""
        kg = cls()
        
        # Node class mapping
        node_class_map = {
            NodeType.WASTE_TYPE: WasteType,
            NodeType.WASTE_STREAM: WasteStream,
            NodeType.PROCESS: Process,
            NodeType.RESOURCE: Resource,
            NodeType.FACILITY: Facility,
            NodeType.CONSTRAINT: Constraint,
            NodeType.ACTOR: Actor
        }
        
        for nid, node_data in data.get("nodes", {}).items():
            node_type = NodeType(node_data["node_type"])
            node_class = node_class_map.get(node_type, Node)
            
            # Use from_dict method which handles node_type properly
            node = node_class.from_dict(node_data)
            kg.nodes[nid] = node
        
        for edge_data in data.get("edges", []):
            edge = Edge.from_dict(edge_data)
            kg.edges.append(edge)
        
        return kg
    
    def to_json(self, indent: int = 2) -> str:
        """Convert graph to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)
    
    @classmethod
    def from_json(cls, json_str: str) -> "KnowledgeGraph":
        """Create graph from JSON string."""
        return cls.from_dict(json.loads(json_str))


# Node factory functions for convenience
def create_waste_type(node_id: str, name: str, **kwargs) -> WasteType:
    """Factory function for creating WasteType nodes."""
    return WasteType(node_id=node_id, name=name, **kwargs)


def create_waste_stream(node_id: str, name: str, **kwargs) -> WasteStream:
    """Factory function for creating WasteStream nodes."""
    return WasteStream(node_id=node_id, name=name, **kwargs)


def create_process(node_id: str, name: str, **kwargs) -> Process:
    """Factory function for creating Process nodes."""
    return Process(node_id=node_id, name=name, **kwargs)


def create_resource(node_id: str, name: str, **kwargs) -> Resource:
    """Factory function for creating Resource nodes."""
    return Resource(node_id=node_id, name=name, **kwargs)


def create_facility(node_id: str, name: str, **kwargs) -> Facility:
    """Factory function for creating Facility nodes."""
    return Facility(node_id=node_id, name=name, **kwargs)


def create_constraint(node_id: str, name: str, **kwargs) -> Constraint:
    """Factory function for creating Constraint nodes."""
    return Constraint(node_id=node_id, name=name, **kwargs)


def create_actor(node_id: str, name: str, **kwargs) -> Actor:
    """Factory function for creating Actor nodes."""
    return Actor(node_id=node_id, name=name, **kwargs)


def create_edge(edge_id: str, edge_type: EdgeType, source_id: str, target_id: str, 
                **kwargs) -> Edge:
    """Factory function for creating Edge."""
    return Edge(edge_id=edge_id, edge_type=edge_type, source_id=source_id, 
                target_id=target_id, properties=kwargs.get("properties", {}))
