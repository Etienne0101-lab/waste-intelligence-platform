"""
Tests for W2RKG Schema module.
"""

import unittest
import json
from kg_schema import (
    Node, Edge, NodeType, EdgeType,
    WasteType, WasteStream, Process, Resource, Facility, Constraint, Actor,
    KnowledgeGraph, create_waste_type, create_waste_stream, create_process,
    create_resource, create_facility, create_constraint, create_actor, create_edge
)


class TestNodeTypes(unittest.TestCase):
    """Test node type classes."""
    
    def test_node_creation(self):
        """Test basic node creation."""
        node = Node(
            node_id="test_node",
            node_type=NodeType.WASTE_TYPE,
            name="Test Node",
            description="A test node"
        )
        self.assertEqual(node.node_id, "test_node")
        self.assertEqual(node.node_type, NodeType.WASTE_TYPE)
        self.assertEqual(node.name, "Test Node")
        self.assertEqual(node.description, "A test node")
    
    def test_node_to_dict(self):
        """Test node serialization to dict."""
        node = Node(
            node_id="test_node",
            node_type=NodeType.WASTE_TYPE,
            name="Test Node",
            description="A test node",
            properties={"key": "value"}
        )
        data = node.to_dict()
        self.assertEqual(data["node_id"], "test_node")
        self.assertEqual(data["node_type"], "Waste_Type")
        self.assertEqual(data["name"], "Test Node")
        self.assertEqual(data["description"], "A test node")
        self.assertEqual(data["properties"], {"key": "value"})
    
    def test_node_from_dict(self):
        """Test node deserialization from dict."""
        data = {
            "node_id": "test_node",
            "node_type": "Waste_Type",
            "name": "Test Node",
            "description": "A test node",
            "properties": {"key": "value"}
        }
        node = Node.from_dict(data)
        self.assertEqual(node.node_id, "test_node")
        self.assertEqual(node.node_type, NodeType.WASTE_TYPE)
        self.assertEqual(node.name, "Test Node")
        self.assertEqual(node.description, "A test node")
        self.assertEqual(node.properties, {"key": "value"})
    
    def test_waste_type_creation(self):
        """Test WasteType node creation."""
        waste = create_waste_type(
            node_id="FoodScraps",
            name="Food Scraps",
            description="Organic food waste",
            composition={"carbs": 50.0, "proteins": 20.0},
            moisture_content=70.0,
            organic_content=95.0
        )
        self.assertEqual(waste.node_id, "FoodScraps")
        self.assertEqual(waste.node_type, NodeType.WASTE_TYPE)
        self.assertEqual(waste.name, "Food Scraps")
        self.assertEqual(waste.composition, {"carbs": 50.0, "proteins": 20.0})
        self.assertEqual(waste.moisture_content, 70.0)
        self.assertEqual(waste.organic_content, 95.0)
    
    def test_waste_stream_creation(self):
        """Test WasteStream node creation."""
        stream = create_waste_stream(
            node_id="ResidentialOrganics",
            name="Residential Organics",
            source_location="Brooklyn, NYC",
            volume_tonnes_per_year=100000.0,
            collection_frequency="weekly"
        )
        self.assertEqual(stream.node_id, "ResidentialOrganics")
        self.assertEqual(stream.node_type, NodeType.WASTE_STREAM)
        self.assertEqual(stream.source_location, "Brooklyn, NYC")
        self.assertEqual(stream.volume_tonnes_per_year, 100000.0)
    
    def test_process_creation(self):
        """Test Process node creation."""
        process = create_process(
            node_id="AerobicComposting",
            name="Aerobic Composting",
            efficiency=85.0,
            processing_time_hours=168.0,
            energy_requirement_kwh_per_tonne=25.0,
            carbon_footprint_kg_co2_per_tonne=50.0
        )
        self.assertEqual(process.node_id, "AerobicComposting")
        self.assertEqual(process.node_type, NodeType.PROCESS)
        self.assertEqual(process.efficiency, 85.0)
        self.assertEqual(process.processing_time_hours, 168.0)
    
    def test_resource_creation(self):
        """Test Resource node creation."""
        resource = create_resource(
            node_id="CompostAmendment",
            name="Compost Amendment",
            economic_value_per_tonne=80.0,
            market_demand="high",
            quality_grade="A"
        )
        self.assertEqual(resource.node_id, "CompostAmendment")
        self.assertEqual(resource.node_type, NodeType.RESOURCE)
        self.assertEqual(resource.economic_value_per_tonne, 80.0)
    
    def test_facility_creation(self):
        """Test Facility node creation."""
        facility = create_facility(
            node_id="FACILITY-01",
            name="Facility 01",
            location={"latitude": 40.7, "longitude": -74.0},
            capacity_tonnes_per_year=100000.0,
            operational_status="active"
        )
        self.assertEqual(facility.node_id, "FACILITY-01")
        self.assertEqual(facility.node_type, NodeType.FACILITY)
        self.assertEqual(facility.location, {"latitude": 40.7, "longitude": -74.0})
    
    def test_constraint_creation(self):
        """Test Constraint node creation."""
        constraint = create_constraint(
            node_id="Regulation01",
            name="Regulation 01",
            constraint_type="regulatory",
            severity="high",
            jurisdiction="NYC"
        )
        self.assertEqual(constraint.node_id, "Regulation01")
        self.assertEqual(constraint.node_type, NodeType.CONSTRAINT)
        self.assertEqual(constraint.constraint_type, "regulatory")
    
    def test_actor_creation(self):
        """Test Actor node creation."""
        actor = create_actor(
            node_id="DSNY",
            name="DSNY",
            actor_type="government",
            scale="city"
        )
        self.assertEqual(actor.node_id, "DSNY")
        self.assertEqual(actor.node_type, NodeType.ACTOR)
        self.assertEqual(actor.actor_type, "government")


class TestEdgeTypes(unittest.TestCase):
    """Test edge type classes."""
    
    def test_edge_creation(self):
        """Test basic edge creation."""
        edge = create_edge(
            edge_id="edge_01",
            edge_type=EdgeType.WASTECANBEPROCESSEDBY,
            source_id="FoodScraps",
            target_id="AerobicComposting"
        )
        self.assertEqual(edge.edge_id, "edge_01")
        self.assertEqual(edge.edge_type, EdgeType.WASTECANBEPROCESSEDBY)
        self.assertEqual(edge.source_id, "FoodScraps")
        self.assertEqual(edge.target_id, "AerobicComposting")
    
    def test_edge_to_dict(self):
        """Test edge serialization to dict."""
        edge = Edge(
            edge_id="edge_01",
            edge_type=EdgeType.WASTECANBEPROCESSEDBY,
            source_id="FoodScraps",
            target_id="AerobicComposting",
            properties={"suitability": "high"}
        )
        data = edge.to_dict()
        self.assertEqual(data["edge_id"], "edge_01")
        self.assertEqual(data["edge_type"], "WASTECANBEPROCESSEDBY")
        self.assertEqual(data["source_id"], "FoodScraps")
        self.assertEqual(data["target_id"], "AerobicComposting")
    
    def test_edge_from_dict(self):
        """Test edge deserialization from dict."""
        data = {
            "edge_id": "edge_01",
            "edge_type": "WASTECANBEPROCESSEDBY",
            "source_id": "FoodScraps",
            "target_id": "AerobicComposting",
            "properties": {"suitability": "high"}
        }
        edge = Edge.from_dict(data)
        self.assertEqual(edge.edge_id, "edge_01")
        self.assertEqual(edge.edge_type.value, "WASTECANBEPROCESSEDBY")


class TestKnowledgeGraph(unittest.TestCase):
    """Test KnowledgeGraph class."""
    
    def test_kg_creation(self):
        """Test knowledge graph creation."""
        kg = KnowledgeGraph()
        self.assertEqual(len(kg.nodes), 0)
        self.assertEqual(len(kg.edges), 0)
    
    def test_kg_add_node(self):
        """Test adding nodes to knowledge graph."""
        kg = KnowledgeGraph()
        node = create_waste_type("FoodScraps", "Food Scraps")
        kg.add_node(node)
        self.assertEqual(len(kg.nodes), 1)
        self.assertIn("FoodScraps", kg.nodes)
    
    def test_kg_add_edge(self):
        """Test adding edges to knowledge graph."""
        kg = KnowledgeGraph()
        edge = create_edge(
            "edge_01", EdgeType.WASTECANBEPROCESSEDBY,
            "FoodScraps", "AerobicComposting"
        )
        kg.add_edge(edge)
        self.assertEqual(len(kg.edges), 1)
    
    def test_kg_get_node(self):
        """Test getting node by ID."""
        kg = KnowledgeGraph()
        node = create_waste_type("FoodScraps", "Food Scraps")
        kg.add_node(node)
        retrieved = kg.get_node("FoodScraps")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Food Scraps")
    
    def test_kg_get_nodes_by_type(self):
        """Test getting nodes by type."""
        kg = KnowledgeGraph()
        kg.add_node(create_waste_type("FoodScraps", "Food Scraps"))
        kg.add_node(create_waste_type("YardWaste", "Yard Waste"))
        kg.add_node(create_process("AerobicComposting", "Aerobic Composting"))
        
        waste_types = kg.get_nodes_by_type(NodeType.WASTE_TYPE)
        self.assertEqual(len(waste_types), 2)
        
        processes = kg.get_nodes_by_type(NodeType.PROCESS)
        self.assertEqual(len(processes), 1)
    
    def test_kg_get_edges_by_type(self):
        """Test getting edges by type."""
        kg = KnowledgeGraph()
        kg.add_edge(create_edge("e1", EdgeType.WASTECANBEPROCESSEDBY, "A", "B"))
        kg.add_edge(create_edge("e2", EdgeType.PROCESSPRODUCESRESOURCE, "B", "C"))
        kg.add_edge(create_edge("e3", EdgeType.WASTECANBEPROCESSEDBY, "D", "E"))
        
        waste_edges = kg.get_edges_by_type(EdgeType.WASTECANBEPROCESSEDBY)
        self.assertEqual(len(waste_edges), 2)
    
    def test_kg_to_dict(self):
        """Test knowledge graph serialization."""
        kg = KnowledgeGraph()
        kg.add_node(create_waste_type("FoodScraps", "Food Scraps"))
        kg.add_edge(create_edge("e1", EdgeType.WASTECANBEPROCESSEDBY, "FoodScraps", "AerobicComposting"))
        
        data = kg.to_dict()
        self.assertIn("nodes", data)
        self.assertIn("edges", data)
        self.assertEqual(len(data["nodes"]), 1)
        self.assertEqual(len(data["edges"]), 1)
    
    def test_kg_from_dict(self):
        """Test knowledge graph deserialization."""
        data = {
            "nodes": {
                "FoodScraps": {
                    "node_id": "FoodScraps",
                    "node_type": "Waste_Type",
                    "name": "Food Scraps",
                    "description": "Test"
                }
            },
            "edges": [
                {
                    "edge_id": "e1",
                    "edge_type": "WASTECANBEPROCESSEDBY",
                    "source_id": "FoodScraps",
                    "target_id": "AerobicComposting"
                }
            ]
        }
        kg = KnowledgeGraph.from_dict(data)
        self.assertEqual(len(kg.nodes), 1)
        self.assertEqual(len(kg.edges), 1)
    
    def test_kg_to_json(self):
        """Test knowledge graph JSON serialization."""
        kg = KnowledgeGraph()
        kg.add_node(create_waste_type("FoodScraps", "Food Scraps"))
        
        json_str = kg.to_json()
        self.assertIsInstance(json_str, str)
        
        # Verify it's valid JSON
        parsed = json.loads(json_str)
        self.assertIn("nodes", parsed)
    
    def test_kg_from_json(self):
        """Test knowledge graph JSON deserialization."""
        json_str = '{"nodes": {}, "edges": []}'
        kg = KnowledgeGraph.from_json(json_str)
        self.assertEqual(len(kg.nodes), 0)
        self.assertEqual(len(kg.edges), 0)


if __name__ == '__main__':
    unittest.main()
