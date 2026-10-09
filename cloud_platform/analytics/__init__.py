# Package marker for analytics modules
try:
    from .kg import (
        KnowledgeGraph, Node, Edge, NodeType, EdgeType,
        WasteType, WasteStream, Process, Resource, Facility, Constraint, Actor,
        KGLoader, KGQueryEngine,
        load_kg_from_json, load_kg_from_csv, load_kg_from_triples,
        save_kg_to_json, save_kg_to_csv,
        get_query_engine, suggest_symbiosis, suggest_routes, list_resources, get_top_pathways
    )
except ImportError:
    pass
