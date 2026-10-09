"""
Waste-to-Resource Knowledge Graph (W2RKG) Loader

Loads graph data from various sources: JSON, CSV, and LLM-extracted triples.
Supports incremental loading and merging of knowledge graph data.
"""

import csv
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
import uuid

from .kg_schema import (
    KnowledgeGraph, Node, Edge, NodeType, EdgeType,
    WasteType, WasteStream, Process, Resource, Facility, Constraint, Actor,
    create_waste_type, create_waste_stream, create_process, create_resource,
    create_facility, create_constraint, create_actor, create_edge
)


class KGLoader:
    """Loader for W2RKG data from various sources."""
    
    def __init__(self, kg: Optional[KnowledgeGraph] = None):
        """Initialize loader with optional existing graph."""
        self.kg = kg or KnowledgeGraph()
        self._node_id_map: Dict[str, str] = {}  # For tracking ID mappings
        self._edge_id_map: Dict[str, str] = {}  # For tracking edge ID mappings
    
    def load_json(self, file_path: Union[str, Path]) -> KnowledgeGraph:
        """Load knowledge graph from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        loaded_kg = KnowledgeGraph.from_dict(data)
        self._merge_kg(loaded_kg)
        return self.kg
    
    def load_json_string(self, json_str: str) -> KnowledgeGraph:
        """Load knowledge graph from JSON string."""
        data = json.loads(json_str)
        loaded_kg = KnowledgeGraph.from_dict(data)
        self._merge_kg(loaded_kg)
        return self.kg
    
    def load_csv(self, file_path: Union[str, Path], node_type: Optional[NodeType] = None,
                 edge_type: Optional[EdgeType] = None) -> KnowledgeGraph:
        """
        Load nodes or edges from CSV file.
        
        CSV format for nodes:
        - Required columns: id, name, type
        - Optional columns: description, and type-specific properties
        
        CSV format for edges:
        - Required columns: id, source_id, target_id, type
        - Optional columns: properties (as JSON string)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            if edge_type:
                # Loading edges
                for row in reader:
                    edge = self._parse_edge_row(row, edge_type)
                    if edge:
                        self.kg.add_edge(edge)
            elif node_type:
                # Loading nodes of specific type
                for row in reader:
                    node = self._parse_node_row(row, node_type)
                    if node:
                        self.kg.add_node(node)
            else:
                # Auto-detect from 'type' column
                for row in reader:
                    row_type = row.get('type', '')
                    if row_type in [e.value for e in EdgeType]:
                        edge = self._parse_edge_row(row, EdgeType(row_type))
                        if edge:
                            self.kg.add_edge(edge)
                    elif row_type in [n.value for n in NodeType]:
                        node = self._parse_node_row(row, NodeType(row_type))
                        if node:
                            self.kg.add_node(node)
        
        return self.kg
    
    def _parse_node_row(self, row: Dict[str, str], node_type: NodeType) -> Optional[Node]:
        """Parse a CSV row into a node."""
        node_id = row.get('id') or row.get('node_id')
        if not node_id:
            return None
        
        name = row.get('name', node_id)
        description = row.get('description')
        
        # Parse properties
        properties = {}
        for key, value in row.items():
            if key not in ['id', 'node_id', 'name', 'type', 'description']:
                try:
                    # Try to parse as JSON for complex types
                    properties[key] = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    properties[key] = value
        
        # Create appropriate node type
        node_class_map = {
            NodeType.WASTE_TYPE: WasteType,
            NodeType.WASTE_STREAM: WasteStream,
            NodeType.PROCESS: Process,
            NodeType.RESOURCE: Resource,
            NodeType.FACILITY: Facility,
            NodeType.CONSTRAINT: Constraint,
            NodeType.ACTOR: Actor
        }
        
        node_class = node_class_map.get(node_type, Node)
        
        # Use factory functions for proper initialization
        if node_type == NodeType.WASTE_TYPE:
            composition = properties.pop('composition', None)
            moisture = properties.pop('moisture_content', None)
            organic = properties.pop('organic_content', None)
            return create_waste_type(
                node_id=node_id, name=name, description=description,
                composition=composition, moisture_content=moisture,
                organic_content=organic, properties=properties
            )
        elif node_type == NodeType.WASTE_STREAM:
            location = properties.pop('source_location', None)
            volume = properties.pop('volume_tonnes_per_year', None)
            frequency = properties.pop('collection_frequency', None)
            return create_waste_stream(
                node_id=node_id, name=name, description=description,
                source_location=location, volume_tonnes_per_year=volume,
                collection_frequency=frequency, properties=properties
            )
        elif node_type == NodeType.PROCESS:
            efficiency = properties.pop('efficiency', None)
            time_hours = properties.pop('processing_time_hours', None)
            energy = properties.pop('energy_requirement_kwh_per_tonne', None)
            carbon = properties.pop('carbon_footprint_kg_co2_per_tonne', None)
            return create_process(
                node_id=node_id, name=name, description=description,
                efficiency=efficiency, processing_time_hours=time_hours,
                energy_requirement_kwh_per_tonne=energy,
                carbon_footprint_kg_co2_per_tonne=carbon, properties=properties
            )
        elif node_type == NodeType.RESOURCE:
            value = properties.pop('economic_value_per_tonne', None)
            demand = properties.pop('market_demand', None)
            grade = properties.pop('quality_grade', None)
            return create_resource(
                node_id=node_id, name=name, description=description,
                economic_value_per_tonne=value, market_demand=demand,
                quality_grade=grade, properties=properties
            )
        elif node_type == NodeType.FACILITY:
            location = properties.pop('location', None)
            capacity = properties.pop('capacity_tonnes_per_year', None)
            status = properties.pop('operational_status', None)
            contact = properties.pop('contact_info', None)
            return create_facility(
                node_id=node_id, name=name, description=description,
                location=location, capacity_tonnes_per_year=capacity,
                operational_status=status, contact_info=contact, properties=properties
            )
        elif node_type == NodeType.CONSTRAINT:
            ctype = properties.pop('constraint_type', None)
            severity = properties.pop('severity', None)
            jurisdiction = properties.pop('jurisdiction', None)
            return create_constraint(
                node_id=node_id, name=name, description=description,
                constraint_type=ctype, severity=severity,
                jurisdiction=jurisdiction, properties=properties
            )
        elif node_type == NodeType.ACTOR:
            atype = properties.pop('actor_type', None)
            scale = properties.pop('scale', None)
            return create_actor(
                node_id=node_id, name=name, description=description,
                actor_type=atype, scale=scale, properties=properties
            )
        else:
            return Node(
                node_id=node_id, node_type=node_type, name=name,
                description=description, properties=properties
            )
    
    def _parse_edge_row(self, row: Dict[str, str], edge_type: EdgeType) -> Optional[Edge]:
        """Parse a CSV row into an edge."""
        edge_id = row.get('id') or row.get('edge_id')
        if not edge_id:
            edge_id = f"edge_{uuid.uuid4().hex[:8]}"
        
        source_id = row.get('source_id') or row.get('source')
        target_id = row.get('target_id') or row.get('target')
        
        if not source_id or not target_id:
            return None
        
        # Parse properties
        properties = {}
        props_str = row.get('properties', '{}')
        try:
            properties = json.loads(props_str)
        except (json.JSONDecodeError, TypeError):
            pass
        
        return create_edge(
            edge_id=edge_id, edge_type=edge_type,
            source_id=source_id, target_id=target_id, properties=properties
        )
    
    def load_triples(self, triples: List[Tuple[str, str, str]], 
                     edge_type: EdgeType = EdgeType.WASTECANBEPROCESSEDBY,
                     source_type: Optional[NodeType] = None,
                     target_type: Optional[NodeType] = None) -> KnowledgeGraph:
        """
        Load triples (subject, predicate, object) into the knowledge graph.
        
        Used for LLM-extracted triples where the relationship is given as text.
        Auto-creates nodes if they don't exist.
        """
        for subject, predicate, obj in triples:
            # Normalize IDs
            subject_id = self._normalize_id(subject)
            object_id = self._normalize_id(obj)
            
            # Map predicate to edge type
            edge_type_map = {
                "can be processed by": EdgeType.WASTECANBEPROCESSEDBY,
                "produces": EdgeType.PROCESSPRODUCESRESOURCE,
                "supports": EdgeType.FACILITYSUPPORTSPROCESS,
                "accepts": EdgeType.FACILITYACCEPTSWASTE,
                "demanded by": EdgeType.RESOURCEDEMANDEDBY_ACTOR,
                "applies to": EdgeType.CONSTRAINTAPPLIESTO,
                "has": EdgeType.WASTESTREAMHASWASTETYPE,
                "located in": EdgeType.FACILITYLOCATEDIN,
                "operates": EdgeType.ACTOROPERATESFACILITY,
            }
            
            actual_edge_type = edge_type_map.get(predicate.lower(), edge_type)
            
            # Create nodes if they don't exist
            if subject_id not in self.kg.nodes:
                node = self._create_node_from_name(subject, source_type)
                self.kg.add_node(node)
            
            if object_id not in self.kg.nodes:
                node = self._create_node_from_name(obj, target_type)
                self.kg.add_node(node)
            
            # Create edge
            edge_id = f"{subject_id}_{actual_edge_type.value}_{object_id}"
            edge = create_edge(
                edge_id=edge_id, edge_type=actual_edge_type,
                source_id=subject_id, target_id=object_id
            )
            self.kg.add_edge(edge)
        
        return self.kg
    
    def _normalize_id(self, name: str) -> str:
        """Normalize a name into a valid node ID."""
        # Replace spaces and special characters
        normalized = name.strip().lower()
        normalized = normalized.replace(' ', '_')
        normalized = normalized.replace('-', '_')
        normalized = normalized.replace('.', '')
        normalized = ''.join(c for c in normalized if c.isalnum() or c == '_')
        return normalized
    
    def _create_node_from_name(self, name: str, node_type: Optional[NodeType] = None) -> Node:
        """Create a node from a name, inferring type if not specified."""
        node_id = self._normalize_id(name)
        
        # Try to infer node type from name patterns
        if not node_type:
            name_lower = name.lower()
            
            # Check for waste types
            waste_patterns = ['food scraps', 'yard waste', 'coffee grounds', 'spent grain', 
                             'fats oils grease', 'food waste', 'green waste', 'manure']
            if any(pattern in name_lower for pattern in waste_patterns):
                node_type = NodeType.WASTE_TYPE
            
            # Check for processes
            process_patterns = ['composting', 'digestion', 'anaerobic', 'aerobic',
                              'biochar', 'pyrolysis', 'gasification', 'bsfl',
                              'black soldier fly', 'vermicomposting']
            if any(pattern in name_lower for pattern in process_patterns):
                node_type = NodeType.PROCESS
            
            # Check for resources
            resource_patterns = ['compost', 'biogas', 'digestate', 'fertilizer',
                                'animal feed', 'soil conditioner', 'biochar', 'biofuel']
            if any(pattern in name_lower for pattern in resource_patterns):
                node_type = NodeType.RESOURCE
            
            # Check for facilities
            facility_patterns = ['facility', 'plant', 'center', 'site', 'station']
            if any(pattern in name_lower for pattern in facility_patterns):
                node_type = NodeType.FACILITY
            
            # Check for constraints
            constraint_patterns = ['regulation', 'law', 'requirement', 'limit',
                                 'standard', 'policy', 'constraint']
            if any(pattern in name_lower for pattern in constraint_patterns):
                node_type = NodeType.CONSTRAINT
            
            # Check for actors
            actor_patterns = ['dsny', 'hauler', 'urban farm', 'waste processor',
                             'municipality', 'company', 'organization']
            if any(pattern in name_lower for pattern in actor_patterns):
                node_type = NodeType.ACTOR
            
            # Default to generic node
            if node_type is None:
                node_type = NodeType.WASTE_TYPE  # Default assumption
        
        # Create appropriate node
        if node_type == NodeType.WASTE_TYPE:
            return create_waste_type(node_id=node_id, name=name)
        elif node_type == NodeType.WASTE_STREAM:
            return create_waste_stream(node_id=node_id, name=name)
        elif node_type == NodeType.PROCESS:
            return create_process(node_id=node_id, name=name)
        elif node_type == NodeType.RESOURCE:
            return create_resource(node_id=node_id, name=name)
        elif node_type == NodeType.FACILITY:
            return create_facility(node_id=node_id, name=name)
        elif node_type == NodeType.CONSTRAINT:
            return create_constraint(node_id=node_id, name=name)
        elif node_type == NodeType.ACTOR:
            return create_actor(node_id=node_id, name=name)
        else:
            return Node(node_id=node_id, node_type=node_type, name=name)
    
    def _merge_kg(self, other_kg: KnowledgeGraph) -> None:
        """Merge another knowledge graph into this one."""
        # Merge nodes
        for node_id, node in other_kg.nodes.items():
            if node_id not in self.kg.nodes:
                self.kg.add_node(node)
            else:
                # Update existing node with new properties
                existing = self.kg.nodes[node_id]
                existing.properties.update(node.properties)
        
        # Merge edges
        existing_edge_ids = {e.edge_id for e in self.kg.edges}
        for edge in other_kg.edges:
            if edge.edge_id not in existing_edge_ids:
                self.kg.add_edge(edge)
    
    def load_directory(self, directory_path: Union[str, Path]) -> KnowledgeGraph:
        """Load all JSON and CSV files from a directory."""
        path = Path(directory_path)
        
        for json_file in path.glob('*.json'):
            self.load_json(json_file)
        
        for csv_file in path.glob('*.csv'):
            self.load_csv(csv_file)
        
        return self.kg
    
    def save_json(self, file_path: Union[str, Path], indent: int = 2) -> None:
        """Save knowledge graph to JSON file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.kg.to_dict(), f, indent=indent)
    
    def save_csv(self, file_path: Union[str, Path], node_type: Optional[NodeType] = None,
                 edge_type: Optional[EdgeType] = None) -> None:
        """Save nodes or edges to CSV file."""
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            if edge_type:
                # Write edges
                edges = [e for e in self.kg.edges if e.edge_type == edge_type]
                if edges:
                    headers = ['edge_id', 'edge_type', 'source_id', 'target_id', 'properties']
                    writer.writerow(headers)
                    for edge in edges:
                        writer.writerow([
                            edge.edge_id,
                            edge.edge_type.value,
                            edge.source_id,
                            edge.target_id,
                            json.dumps(edge.properties)
                        ])
            elif node_type:
                # Write nodes of specific type
                nodes = [n for n in self.kg.nodes.values() if n.node_type == node_type]
                if nodes:
                    # Get all possible property keys
                    all_keys = set(['node_id', 'node_type', 'name', 'description'])
                    for node in nodes:
                        all_keys.update(node.properties.keys())
                    
                    headers = sorted(list(all_keys))
                    writer.writerow(headers)
                    
                    for node in nodes:
                        row = {
                            'node_id': node.node_id,
                            'node_type': node.node_type.value,
                            'name': node.name,
                            'description': node.description or ''
                        }
                        row.update(node.properties)
                        writer.writerow([row.get(k, '') for k in headers])
            else:
                # Write all nodes
                all_nodes = list(self.kg.nodes.values())
                if all_nodes:
                    all_keys = set(['node_id', 'node_type', 'name', 'description'])
                    for node in all_nodes:
                        all_keys.update(node.properties.keys())
                    
                    headers = sorted(list(all_keys))
                    writer.writerow(headers)
                    
                    for node in all_nodes:
                        row = {
                            'node_id': node.node_id,
                            'node_type': node.node_type.value,
                            'name': node.name,
                            'description': node.description or ''
                        }
                        row.update(node.properties)
                        writer.writerow([row.get(k, '') for k in headers])
    
    def get_graph(self) -> KnowledgeGraph:
        """Get the current knowledge graph."""
        return self.kg
    
    def reset(self) -> None:
        """Reset the loader with a new empty graph."""
        self.kg = KnowledgeGraph()
        self._node_id_map.clear()
        self._edge_id_map.clear()


# Convenience functions
def load_kg_from_json(file_path: Union[str, Path]) -> KnowledgeGraph:
    """Load knowledge graph from JSON file."""
    loader = KGLoader()
    return loader.load_json(file_path)


def load_kg_from_csv(file_path: Union[str, Path], node_type: Optional[NodeType] = None,
                    edge_type: Optional[EdgeType] = None) -> KnowledgeGraph:
    """Load knowledge graph from CSV file."""
    loader = KGLoader()
    return loader.load_csv(file_path, node_type, edge_type)


def load_kg_from_triples(triples: List[Tuple[str, str, str]]) -> KnowledgeGraph:
    """Load knowledge graph from triples."""
    loader = KGLoader()
    return loader.load_triples(triples)


def save_kg_to_json(kg: KnowledgeGraph, file_path: Union[str, Path], indent: int = 2) -> None:
    """Save knowledge graph to JSON file."""
    loader = KGLoader(kg)
    loader.save_json(file_path, indent)


def save_kg_to_csv(kg: KnowledgeGraph, file_path: Union[str, Path], 
                   node_type: Optional[NodeType] = None,
                   edge_type: Optional[EdgeType] = None) -> None:
    """Save knowledge graph to CSV file."""
    loader = KGLoader(kg)
    loader.save_csv(file_path, node_type, edge_type)
