"""
Tests for W2RKG Loader module.
"""

import unittest
import json
import tempfile
import os
from pathlib import Path
from kg_schema import (
    KnowledgeGraph, NodeType, EdgeType,
    WasteType, Process, Resource, Facility
)
from kg_loader import (
    KGLoader,
    load_kg_from_json, load_kg_from_csv, load_kg_from_triples,
    save_kg_to_json, save_kg_to_csv
)


class TestKGLoader(unittest.TestCase):
    """Test KGLoader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.kg = KnowledgeGraph()
        self.loader = KGLoader(self.kg)
    
    def test_load_json(self):
        """Test loading from JSON file."""
        # Create a temporary JSON file
        data = {
            "nodes": {
                "FoodScraps": {
                    "node_id": "FoodScraps",
                    "node_type": "Waste_Type",
                    "name": "Food Scraps",
                    "description": "Test waste"
                }
            },
            "edges": []
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        
        try:
            kg = self.loader.load_json(temp_path)
            self.assertEqual(len(kg.nodes), 1)
            self.assertIn("FoodScraps", kg.nodes)
        finally:
            os.unlink(temp_path)
    
    def test_load_json_string(self):
        """Test loading from JSON string."""
        json_str = '{"nodes": {"FoodScraps": {"node_id": "FoodScraps", "node_type": "Waste_Type", "name": "Food Scraps"}}, "edges": []}'
        kg = self.loader.load_json_string(json_str)
        self.assertEqual(len(kg.nodes), 1)
    
    def test_load_csv_nodes(self):
        """Test loading nodes from CSV."""
        csv_content = """node_id,node_type,name,description
FoodScraps,Waste_Type,Food Scraps,Organic food waste
YardWaste,Waste_Type,Yard Waste,Garden waste
AerobicComposting,Process,Aerobic Composting,Composting process
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            kg = self.loader.load_csv(temp_path, node_type=NodeType.WASTE_TYPE)
            # Should load only Waste_Type nodes
            self.assertEqual(len(kg.nodes), 2)
        finally:
            os.unlink(temp_path)
    
    def test_load_csv_edges(self):
        """Test loading edges from CSV."""
        csv_content = """edge_id,edge_type,source_id,target_id
edge1,WASTECANBEPROCESSEDBY,FoodScraps,AerobicComposting
edge2,PROCESSPRODUCESRESOURCE,AerobicComposting,CompostAmendment
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            kg = self.loader.load_csv(temp_path, edge_type=EdgeType.WASTECANBEPROCESSEDBY)
            self.assertEqual(len(kg.edges), 1)
        finally:
            os.unlink(temp_path)
    
    def test_load_triples(self):
        """Test loading from triples."""
        triples = [
            ("FoodScraps", "can be processed by", "AerobicComposting"),
            ("AerobicComposting", "produces", "CompostAmendment"),
            ("YardWaste", "can be processed by", "AerobicComposting")
        ]
        kg = self.loader.load_triples(triples)
        
        # Should have created nodes and edges
        self.assertGreaterEqual(len(kg.nodes), 3)
        self.assertGreaterEqual(len(kg.edges), 3)
    
    def test_load_triples_with_types(self):
        """Test loading triples with specified types."""
        triples = [
            ("FoodScraps", "can be processed by", "AerobicComposting")
        ]
        kg = self.loader.load_triples(
            triples,
            source_type=NodeType.WASTE_TYPE,
            target_type=NodeType.PROCESS
        )
        self.assertEqual(len(kg.nodes), 2)
        self.assertEqual(len(kg.edges), 1)
    
    def test_save_json(self):
        """Test saving to JSON file."""
        self.loader.kg.add_node(Process(
            node_id="AerobicComposting",
            node_type=NodeType.PROCESS,
            name="Aerobic Composting"
        ))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            self.loader.save_json(temp_path)
            
            # Verify the file was created and is valid JSON
            with open(temp_path, 'r') as f:
                data = json.load(f)
            
            self.assertIn("nodes", data)
            self.assertIn("edges", data)
        finally:
            os.unlink(temp_path)
    
    def test_save_csv(self):
        """Test saving to CSV file."""
        self.loader.kg.add_node(Process(
            node_id="AerobicComposting",
            node_type=NodeType.PROCESS,
            name="Aerobic Composting",
            efficiency=85.0
        ))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name
        
        try:
            self.loader.save_csv(temp_path, node_type=NodeType.PROCESS)
            
            # Verify the file was created
            with open(temp_path, 'r') as f:
                content = f.read()
            
            self.assertIn("AerobicComposting", content)
            self.assertIn("Process", content)
        finally:
            os.unlink(temp_path)
    
    def test_merge_kg(self):
        """Test merging knowledge graphs."""
        kg1 = KnowledgeGraph()
        kg1.add_node(WasteType(
            node_id="FoodScraps",
            node_type=NodeType.WASTE_TYPE,
            name="Food Scraps"
        ))
        
        kg2 = KnowledgeGraph()
        kg2.add_node(Process(
            node_id="AerobicComposting",
            node_type=NodeType.PROCESS,
            name="Aerobic Composting"
        ))
        
        loader = KGLoader(kg1)
        loader._merge_kg(kg2)
        
        self.assertEqual(len(loader.kg.nodes), 2)
    
    def test_normalize_id(self):
        """Test ID normalization."""
        loader = KGLoader()
        
        self.assertEqual(loader._normalize_id("Food Scraps"), "food_scraps")
        self.assertEqual(loader._normalize_id("Yard-Waste"), "yard_waste")
        self.assertEqual(loader._normalize_id("Anaerobic Digestion"), "anaerobic_digestion")


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def test_load_kg_from_json(self):
        """Test load_kg_from_json function."""
        data = {
            "nodes": {
                "FoodScraps": {
                    "node_id": "FoodScraps",
                    "node_type": "Waste_Type",
                    "name": "Food Scraps"
                }
            },
            "edges": []
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        
        try:
            kg = load_kg_from_json(temp_path)
            self.assertEqual(len(kg.nodes), 1)
        finally:
            os.unlink(temp_path)
    
    def test_load_kg_from_csv(self):
        """Test load_kg_from_csv function."""
        csv_content = """node_id,node_type,name
FoodScraps,Waste_Type,Food Scraps
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            kg = load_kg_from_csv(temp_path, node_type=NodeType.WASTE_TYPE)
            self.assertEqual(len(kg.nodes), 1)
        finally:
            os.unlink(temp_path)
    
    def test_load_kg_from_triples(self):
        """Test load_kg_from_triples function."""
        triples = [("FoodScraps", "can be processed by", "AerobicComposting")]
        kg = load_kg_from_triples(triples)
        self.assertGreaterEqual(len(kg.nodes), 2)
        self.assertGreaterEqual(len(kg.edges), 1)
    
    def test_save_kg_to_json(self):
        """Test save_kg_to_json function."""
        kg = KnowledgeGraph()
        kg.add_node(WasteType(
            node_id="FoodScraps",
            node_type=NodeType.WASTE_TYPE,
            name="Food Scraps"
        ))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            save_kg_to_json(kg, temp_path)
            
            with open(temp_path, 'r') as f:
                data = json.load(f)
            
            self.assertIn("nodes", data)
        finally:
            os.unlink(temp_path)
    
    def test_save_kg_to_csv(self):
        """Test save_kg_to_csv function."""
        kg = KnowledgeGraph()
        kg.add_node(WasteType(
            node_id="FoodScraps",
            node_type=NodeType.WASTE_TYPE,
            name="Food Scraps"
        ))
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name
        
        try:
            save_kg_to_csv(kg, temp_path, node_type=NodeType.WASTE_TYPE)
            
            with open(temp_path, 'r') as f:
                content = f.read()
            
            self.assertIn("FoodScraps", content)
        finally:
            os.unlink(temp_path)


class TestNodeCreationFromName(unittest.TestCase):
    """Test node creation from name inference."""
    
    def test_infer_waste_type(self):
        """Test inference of waste type from name."""
        loader = KGLoader()
        node = loader._create_node_from_name("Food Scraps", None)
        self.assertEqual(node.node_type, NodeType.WASTE_TYPE)
    
    def test_infer_process(self):
        """Test inference of process from name."""
        loader = KGLoader()
        node = loader._create_node_from_name("Anaerobic Digestion", None)
        self.assertEqual(node.node_type, NodeType.PROCESS)
    
    def test_infer_resource(self):
        """Test inference of resource from name."""
        loader = KGLoader()
        node = loader._create_node_from_name("Compost Amendment", None)
        self.assertEqual(node.node_type, NodeType.RESOURCE)
    
    def test_infer_facility(self):
        """Test inference of facility from name."""
        loader = KGLoader()
        node = loader._create_node_from_name("Composting Plant", None)
        self.assertEqual(node.node_type, NodeType.FACILITY)
    
    def test_infer_constraint(self):
        """Test inference of constraint from name."""
        loader = KGLoader()
        node = loader._create_node_from_name("NYC Regulation", None)
        self.assertEqual(node.node_type, NodeType.CONSTRAINT)
    
    def test_infer_actor(self):
        """Test inference of actor from name."""
        loader = KGLoader()
        node = loader._create_node_from_name("DSNY", None)
        self.assertEqual(node.node_type, NodeType.ACTOR)


if __name__ == '__main__':
    unittest.main()
