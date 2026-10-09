"""
Waste-to-Resource Knowledge Graph (W2RKG) Module

This module provides a semantic layer for the Waste Intelligence Platform,
enabling waste-to-resource pathway analysis, facility routing optimization,
and industrial symbiosis discovery.

Main components:
- kg_schema.py: Node and edge type definitions
- kg_loader.py: Data loading from JSON, CSV, and LLM-extracted triples
- kg_query.py: High-level query functions for the knowledge graph

Example usage:
    from kg_schema import KnowledgeGraph, WasteType, Process, Resource
    from kg_loader import KGLoader
    from kg_query import KGQueryEngine
    
    # Create and load a knowledge graph
    loader = KGLoader()
    kg = loader.load_json("data/w2rkg.json")
    
    # Query the graph
    engine = KGQueryEngine(kg)
    pathways = engine.get_top_resource_pathways("FoodScraps", quantity_kg=50000)
    
    # Get symbiosis suggestions
    symbiosis = engine.suggest_symbiosis_for_facility(
        "FACILITY-BK-COMPOST-01",
        {"FoodScraps": 50000, "YardWaste": 20000}
    )
"""

from .kg_schema import (
    KnowledgeGraph, Node, Edge, NodeType, EdgeType,
    WasteType, WasteStream, Process, Resource, Facility, Constraint, Actor,
    create_waste_type, create_waste_stream, create_process, create_resource,
    create_facility, create_constraint, create_actor, create_edge
)

from .kg_loader import (
    KGLoader,
    load_kg_from_json, load_kg_from_csv, load_kg_from_triples,
    save_kg_to_json, save_kg_to_csv
)

from .kg_query import (
    KGQueryEngine,
    Pathway, RouteSuggestion, SymbiosisResult,
    get_query_engine, suggest_symbiosis, suggest_routes, list_resources, get_top_pathways
)

__all__ = [
    # Schema
    'KnowledgeGraph', 'Node', 'Edge', 'NodeType', 'EdgeType',
    'WasteType', 'WasteStream', 'Process', 'Resource', 'Facility', 'Constraint', 'Actor',
    'create_waste_type', 'create_waste_stream', 'create_process', 'create_resource',
    'create_facility', 'create_constraint', 'create_actor', 'create_edge',
    # Loader
    'KGLoader',
    'load_kg_from_json', 'load_kg_from_csv', 'load_kg_from_triples',
    'save_kg_to_json', 'save_kg_to_csv',
    # Query
    'KGQueryEngine',
    'Pathway', 'RouteSuggestion', 'SymbiosisResult',
    'get_query_engine', 'suggest_symbiosis', 'suggest_routes', 'list_resources', 'get_top_pathways'
]

__version__ = "1.0.0"
