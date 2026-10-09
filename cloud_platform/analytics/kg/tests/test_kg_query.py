"""
Tests for W2RKG Query Engine module.
"""

import unittest
from kg_schema import (
    KnowledgeGraph, NodeType, EdgeType,
    WasteType, WasteStream, Process, Resource, Facility, Constraint, Actor,
    create_waste_type, create_waste_stream, create_process, create_resource,
    create_facility, create_constraint, create_actor, create_edge
)
from kg_query import (
    KGQueryEngine,
    Pathway, RouteSuggestion, SymbiosisResult,
    get_query_engine, suggest_symbiosis, suggest_routes, list_resources, get_top_pathways
)


class TestKGQueryEngine(unittest.TestCase):
    """Test KGQueryEngine class."""
    
    def setUp(self):
        """Set up test knowledge graph."""
        self.kg = KnowledgeGraph()
        
        # Add nodes
        self.food_scraps = create_waste_type(
            node_id="FoodScraps",
            name="Food Scraps",
            description="Organic food waste",
            moisture_content=70.0,
            organic_content=95.0
        )
        self.kg.add_node(self.food_scraps)
        
        self.yard_waste = create_waste_type(
            node_id="YardWaste",
            name="Yard Waste",
            description="Garden waste"
        )
        self.kg.add_node(self.yard_waste)
        
        self.aerobic_composting = create_process(
            node_id="AerobicComposting",
            name="Aerobic Composting",
            efficiency=85.0,
            processing_time_hours=168.0,
            energy_requirement_kwh_per_tonne=25.0,
            carbon_footprint_kg_co2_per_tonne=50.0
        )
        self.kg.add_node(self.aerobic_composting)
        
        self.anaerobic_digestion = create_process(
            node_id="AnaerobicDigestion",
            name="Anaerobic Digestion",
            efficiency=90.0,
            processing_time_hours=336.0,
            energy_requirement_kwh_per_tonne=45.0,
            carbon_footprint_kg_co2_per_tonne=30.0
        )
        self.kg.add_node(self.anaerobic_digestion)
        
        self.compost_amendment = create_resource(
            node_id="CompostAmendment",
            name="Compost Amendment",
            economic_value_per_tonne=80.0,
            market_demand="high",
            quality_grade="A"
        )
        self.kg.add_node(self.compost_amendment)
        
        self.biogas = create_resource(
            node_id="Biogas",
            name="Biogas",
            economic_value_per_tonne=400.0,
            market_demand="very_high",
            quality_grade="A"
        )
        self.kg.add_node(self.biogas)
        
        self.facility_01 = create_facility(
            node_id="FACILITY-01",
            name="Facility 01",
            location={"latitude": 40.7, "longitude": -74.0},
            capacity_tonnes_per_year=100000.0
        )
        self.kg.add_node(self.facility_01)
        
        self.facility_02 = create_facility(
            node_id="FACILITY-02",
            name="Facility 02",
            location={"latitude": 40.8, "longitude": -73.9},
            capacity_tonnes_per_year=200000.0
        )
        self.kg.add_node(self.facility_02)
        
        self.urban_farm = create_actor(
            node_id="UrbanFarm",
            name="Urban Farm",
            actor_type="community",
            scale="neighborhood"
        )
        self.kg.add_node(self.urban_farm)
        
        # Add edges
        self.kg.add_edge(create_edge(
            "edge1", EdgeType.WASTECANBEPROCESSEDBY,
            "FoodScraps", "AerobicComposting"
        ))
        self.kg.add_edge(create_edge(
            "edge2", EdgeType.WASTECANBEPROCESSEDBY,
            "FoodScraps", "AnaerobicDigestion"
        ))
        self.kg.add_edge(create_edge(
            "edge3", EdgeType.WASTECANBEPROCESSEDBY,
            "YardWaste", "AerobicComposting"
        ))
        self.kg.add_edge(create_edge(
            "edge4", EdgeType.PROCESSPRODUCESRESOURCE,
            "AerobicComposting", "CompostAmendment"
        ))
        self.kg.add_edge(create_edge(
            "edge5", EdgeType.PROCESSPRODUCESRESOURCE,
            "AnaerobicDigestion", "Biogas"
        ))
        self.kg.add_edge(create_edge(
            "edge6", EdgeType.FACILITYSUPPORTSPROCESS,
            "FACILITY-01", "AerobicComposting"
        ))
        self.kg.add_edge(create_edge(
            "edge7", EdgeType.FACILITYSUPPORTSPROCESS,
            "FACILITY-02", "AnaerobicDigestion"
        ))
        self.kg.add_edge(create_edge(
            "edge8", EdgeType.FACILITYACCEPTSWASTE,
            "FACILITY-01", "FoodScraps"
        ))
        self.kg.add_edge(create_edge(
            "edge9", EdgeType.FACILITYACCEPTSWASTE,
            "FACILITY-02", "FoodScraps"
        ))
        self.kg.add_edge(create_edge(
            "edge10", EdgeType.RESOURCEDEMANDEDBY_ACTOR,
            "CompostAmendment", "UrbanFarm"
        ))
        
        self.engine = KGQueryEngine(self.kg)
    
    def test_get_top_resource_pathways(self):
        """Test getting top resource pathways."""
        pathways = self.engine.get_top_resource_pathways("FoodScraps", quantity_kg=1000.0)
        
        self.assertGreaterEqual(len(pathways), 2)
        
        # Check that pathways have correct structure
        for pathway in pathways:
            self.assertIsInstance(pathway, Pathway)
            self.assertEqual(pathway.waste_type.node_id, "FoodScraps")
            self.assertIsNotNone(pathway.process)
            self.assertIsNotNone(pathway.resource)
    
    def test_list_resources_from_stream(self):
        """Test listing resources from waste stream."""
        # Create a waste stream
        stream = create_waste_stream(
            node_id="TestStream",
            name="Test Stream"
        )
        self.kg.add_node(stream)
        
        # Add waste type to stream
        self.kg.add_edge(create_edge(
            "stream_edge", EdgeType.WASTESTREAMHASWASTETYPE,
            "TestStream", "FoodScraps"
        ))
        
        resources = self.engine.list_resources_from_stream("TestStream")
        
        # Should find compost and biogas through FoodScraps
        self.assertGreaterEqual(len(resources), 2)
        
        resource_names = [r["resource"] for r in resources]
        self.assertIn("Compost Amendment", resource_names)
        self.assertIn("Biogas", resource_names)
    
    def test_suggest_alternative_routes(self):
        """Test suggesting alternative routes."""
        routes = self.engine.suggest_alternative_routes("cluster_01", "FoodScraps", max_results=5)
        
        self.assertGreaterEqual(len(routes), 1)
        
        for route in routes:
            self.assertIsInstance(route, RouteSuggestion)
            self.assertIsNotNone(route.facility)
            self.assertIsNotNone(route.process)
            self.assertIsNotNone(route.resource)
    
    def test_suggest_symbiosis_for_facility(self):
        """Test suggesting symbiosis for facility."""
        waste_profile = {"FoodScraps": 10000.0}
        symbiosis = self.engine.suggest_symbiosis_for_facility("FACILITY-01", waste_profile)
        
        self.assertGreaterEqual(len(symbiosis), 1)
        
        for result in symbiosis:
            self.assertIsInstance(result, SymbiosisResult)
            self.assertIsNotNone(result.facility)
            self.assertIsNotNone(result.process)
            self.assertIsNotNone(result.resource)
            self.assertGreater(result.synergy_score, 0)
    
    def test_query_graph_match(self):
        """Test MATCH query."""
        results = self.engine.query_graph("MATCH Waste_Type->Process->Resource RETURN *")
        
        self.assertGreaterEqual(len(results), 2)
        
        # Check structure
        for result in results:
            self.assertIn("waste_type", result)
            self.assertIn("process", result)
            self.assertIn("resource", result)
    
    def test_query_graph_find_pathways(self):
        """Test FIND PATHWAYS query."""
        results = self.engine.query_graph("FIND PATHWAYS FOR Food Scraps")
        
        self.assertGreaterEqual(len(results), 2)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""
    
    def setUp(self):
        """Set up test knowledge graph."""
        self.kg = KnowledgeGraph()
        
        # Add basic nodes and edges
        self.kg.add_node(create_waste_type("FoodScraps", "Food Scraps"))
        self.kg.add_node(create_process("AerobicComposting", "Aerobic Composting"))
        self.kg.add_node(create_resource("CompostAmendment", "Compost Amendment"))
        
        self.kg.add_edge(create_edge(
            "edge1", EdgeType.WASTECANBEPROCESSEDBY,
            "FoodScraps", "AerobicComposting"
        ))
        self.kg.add_edge(create_edge(
            "edge2", EdgeType.PROCESSPRODUCESRESOURCE,
            "AerobicComposting", "CompostAmendment"
        ))
    
    def test_get_query_engine(self):
        """Test get_query_engine function."""
        engine = get_query_engine(self.kg)
        self.assertIsInstance(engine, KGQueryEngine)
    
    def test_get_top_pathways(self):
        """Test get_top_pathways function."""
        pathways = get_top_pathways(self.kg, "FoodScraps", 1000.0)
        self.assertGreaterEqual(len(pathways), 1)
    
    def test_list_resources(self):
        """Test list_resources function."""
        # Add a waste stream
        self.kg.add_node(create_waste_stream("Stream01", "Stream 01"))
        self.kg.add_edge(create_edge(
            "stream_edge", EdgeType.WASTESTREAMHASWASTETYPE,
            "Stream01", "FoodScraps"
        ))
        
        resources = list_resources(self.kg, "Stream01")
        self.assertGreaterEqual(len(resources), 1)
    
    def test_suggest_routes(self):
        """Test suggest_routes function."""
        routes = suggest_routes(self.kg, "cluster_01", "FoodScraps")
        self.assertIsInstance(routes, list)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_graph(self):
        """Test queries on empty graph."""
        kg = KnowledgeGraph()
        engine = KGQueryEngine(kg)
        
        pathways = engine.get_top_resource_pathways("FoodScraps", 1000.0)
        self.assertEqual(len(pathways), 0)
        
        routes = engine.suggest_alternative_routes("cluster_01", "FoodScraps")
        self.assertEqual(len(routes), 0)
        
        symbiosis = engine.suggest_symbiosis_for_facility("FACILITY-01", {"FoodScraps": 1000.0})
        self.assertEqual(len(symbiosis), 0)
    
    def test_nonexistent_node(self):
        """Test queries with non-existent nodes."""
        kg = KnowledgeGraph()
        engine = KGQueryEngine(kg)
        
        pathways = engine.get_top_resource_pathways("NonExistent", 1000.0)
        self.assertEqual(len(pathways), 0)
        
        resources = engine.list_resources_from_stream("NonExistent")
        self.assertEqual(len(resources), 0)
    
    def test_node_with_no_connections(self):
        """Test queries with nodes that have no connections."""
        kg = KnowledgeGraph()
        kg.add_node(create_waste_type("IsolatedWaste", "Isolated Waste"))
        engine = KGQueryEngine(kg)
        
        pathways = engine.get_top_resource_pathways("IsolatedWaste", 1000.0)
        self.assertEqual(len(pathways), 0)


if __name__ == '__main__':
    unittest.main()
