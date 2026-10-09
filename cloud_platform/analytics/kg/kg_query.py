"""
Waste-to-Resource Knowledge Graph (W2RKG) Query Engine

High-level query functions for the waste intelligence platform.
Provides semantic queries for waste-to-resource pathway analysis, 
facility routing optimization, and industrial symbiosis discovery.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
import math
from collections import defaultdict

from .kg_schema import (
    KnowledgeGraph, Node, Edge, NodeType, EdgeType,
    WasteType, WasteStream, Process, Resource, Facility, Constraint, Actor
)


@dataclass
class Pathway:
    """Represents a waste-to-resource pathway."""
    waste_type: WasteType
    process: Process
    resource: Resource
    facilities: List[Facility]
    constraints: List[Constraint]
    efficiency: float
    economic_value: float
    carbon_footprint: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "waste_type": self.waste_type.name,
            "process": self.process.name,
            "resource": self.resource.name,
            "facilities": [f.name for f in self.facilities],
            "constraints": [c.name for c in self.constraints],
            "efficiency": self.efficiency,
            "economic_value": self.economic_value,
            "carbon_footprint": self.carbon_footprint
        }


@dataclass
class RouteSuggestion:
    """Represents a routing suggestion for waste streams."""
    facility: Facility
    process: Process
    resource: Resource
    distance_km: float
    transport_cost: float
    processing_cost: float
    total_cost: float
    resource_value: float
    net_value: float
    constraints: List[Constraint]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "facility": self.facility.name,
            "process": self.process.name,
            "resource": self.resource.name,
            "distance_km": self.distance_km,
            "transport_cost": self.transport_cost,
            "processing_cost": self.processing_cost,
            "total_cost": self.total_cost,
            "resource_value": self.resource_value,
            "net_value": self.net_value,
            "constraints": [c.name for c in self.constraints]
        }


@dataclass
class SymbiosisResult:
    """Represents industrial symbiosis opportunities."""
    waste_stream: WasteStream
    facility: Facility
    process: Process
    resource: Resource
    actors: List[Actor]
    synergy_score: float
    environmental_benefit: float
    economic_benefit: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "waste_stream": self.waste_stream.name,
            "facility": self.facility.name,
            "process": self.process.name,
            "resource": self.resource.name,
            "actors": [a.name for a in self.actors],
            "synergy_score": self.synergy_score,
            "environmental_benefit": self.environmental_benefit,
            "economic_benefit": self.economic_benefit
        }


class KGQueryEngine:
    """Query engine for W2RKG."""
    
    def __init__(self, kg: KnowledgeGraph):
        """Initialize query engine with a knowledge graph."""
        self.kg = kg
        self._index_nodes()
    
    def _index_nodes(self) -> None:
        """Create indexes for faster querying."""
        self._nodes_by_type: Dict[NodeType, List[Node]] = defaultdict(list)
        self._edges_by_type: Dict[EdgeType, List[Edge]] = defaultdict(list)
        self._edges_by_source: Dict[str, List[Edge]] = defaultdict(list)
        self._edges_by_target: Dict[str, List[Edge]] = defaultdict(list)
        
        for node in self.kg.nodes.values():
            self._nodes_by_type[node.node_type].append(node)
        
        for edge in self.kg.edges:
            self._edges_by_type[edge.edge_type].append(edge)
            self._edges_by_source[edge.source_id].append(edge)
            self._edges_by_target[edge.target_id].append(edge)
    
    def _get_waste_process_edges(self, waste_type_id: str) -> List[Edge]:
        """Get edges showing which processes can handle a waste type."""
        return [e for e in self._edges_by_source.get(waste_type_id, [])
                if e.edge_type == EdgeType.WASTECANBEPROCESSEDBY]
    
    def _get_process_resource_edges(self, process_id: str) -> List[Edge]:
        """Get edges showing which resources a process produces."""
        return [e for e in self._edges_by_source.get(process_id, [])
                if e.edge_type == EdgeType.PROCESSPRODUCESRESOURCE]
    
    def _get_facility_process_edges(self, facility_id: str) -> List[Edge]:
        """Get edges showing which processes a facility supports."""
        return [e for e in self._edges_by_source.get(facility_id, [])
                if e.edge_type == EdgeType.FACILITYSUPPORTSPROCESS]
    
    def _get_facility_waste_edges(self, facility_id: str) -> List[Edge]:
        """Get edges showing which waste types a facility accepts."""
        return [e for e in self._edges_by_source.get(facility_id, [])
                if e.edge_type == EdgeType.FACILITYACCEPTSWASTE]
    
    def _get_resource_actor_edges(self, resource_id: str) -> List[Edge]:
        """Get edges showing which actors demand a resource."""
        return [e for e in self._edges_by_source.get(resource_id, [])
                if e.edge_type == EdgeType.RESOURCEDEMANDEDBY_ACTOR]
    
    def _get_constraint_edges(self, target_id: str) -> List[Edge]:
        """Get all constraint edges that apply to a node."""
        return [e for e in self._edges_by_target.get(target_id, [])
                if e.edge_type == EdgeType.CONSTRAINTAPPLIESTO]
    
    def suggest_symbiosis_for_facility(self, facility_id: str, waste_profile: Dict[str, float]) -> List[SymbiosisResult]:
        """
        Suggest industrial symbiosis opportunities for a facility given a waste profile.
        
        Args:
            facility_id: ID of the facility
            waste_profile: Dictionary of waste type IDs to quantities (kg)
        
        Returns:
            List of symbiosis results ranked by synergy score
        """
        results = []
        
        facility = self.kg.get_node(facility_id)
        if not facility or not isinstance(facility, Facility):
            return results
        
        # Get processes supported by this facility
        process_edges = self._get_facility_process_edges(facility_id)
        supported_processes = [self.kg.get_node(e.target_id) for e in process_edges]
        supported_processes = [p for p in supported_processes if p and isinstance(p, Process)]
        
        # Get waste types accepted by this facility
        waste_edges = self._get_facility_waste_edges(facility_id)
        accepted_wastes = [self.kg.get_node(e.target_id) for e in waste_edges]
        accepted_wastes = [w for w in accepted_wastes if w and isinstance(w, WasteType)]
        
        # For each waste type in profile that the facility accepts
        for waste_type_id, quantity in waste_profile.items():
            if waste_type_id not in [w.node_id for w in accepted_wastes]:
                continue
            
            waste_type = self.kg.get_node(waste_type_id)
            if not waste_type or not isinstance(waste_type, WasteType):
                continue
            
            # Find processes that can handle this waste
            waste_process_edges = self._get_waste_process_edges(waste_type_id)
            compatible_processes = []
            
            for edge in waste_process_edges:
                process = self.kg.get_node(edge.target_id)
                if process and isinstance(process, Process):
                    compatible_processes.append(process)
            
            # Intersect with facility's supported processes
            usable_processes = [p for p in compatible_processes 
                               if p in supported_processes]
            
            for process in usable_processes:
                # Find resources produced by this process
                resource_edges = self._get_process_resource_edges(process.node_id)
                produced_resources = []
                
                for edge in resource_edges:
                    resource = self.kg.get_node(edge.target_id)
                    if resource and isinstance(resource, Resource):
                        produced_resources.append(resource)
                
                for resource in produced_resources:
                    # Find actors that demand this resource
                    actor_edges = self._get_resource_actor_edges(resource.node_id)
                    demanding_actors = [self.kg.get_node(e.target_id) 
                                      for e in actor_edges]
                    demanding_actors = [a for a in demanding_actors 
                                      if a and isinstance(a, Actor)]
                    
                    # Calculate synergy score (0-100)
                    synergy_score = self._calculate_symbiosis_score(
                        facility, process, resource, demanding_actors, quantity
                    )
                    
                    # Calculate benefits
                    environmental_benefit = self._calculate_environmental_benefit(
                        process, resource, quantity
                    )
                    economic_benefit = self._calculate_economic_benefit(
                        process, resource, quantity
                    )
                    
                    result = SymbiosisResult(
                        waste_stream=WasteStream(
                            node_id=f"waste_stream_{waste_type_id}",
                            name=f"Stream of {waste_type.name}",
                            description=f"Waste stream with {quantity} kg of {waste_type.name}"
                        ),
                        facility=facility,
                        process=process,
                        resource=resource,
                        actors=demanding_actors,
                        synergy_score=synergy_score,
                        environmental_benefit=environmental_benefit,
                        economic_benefit=economic_benefit
                    )
                    results.append(result)
        
        # Sort by synergy score (descending)
        results.sort(key=lambda x: x.synergy_score, reverse=True)
        return results
    
    def suggest_alternative_routes(self, cluster_id: str, waste_type_id: str,
                                  max_results: int = 5) -> List[RouteSuggestion]:
        """
        Suggest alternative routing options for a waste stream.
        
        Args:
            cluster_id: ID of the cluster/location
            waste_type_id: ID of the waste type
            max_results: Maximum number of suggestions to return
        
        Returns:
            List of route suggestions ranked by net value
        """
        results = []
        
        waste_type = self.kg.get_node(waste_type_id)
        if not waste_type or not isinstance(waste_type, WasteType):
            return results
        
        # Find all facilities that accept this waste type
        all_facilities = self._nodes_by_type.get(NodeType.FACILITY, [])
        
        for facility in all_facilities:
            facility_waste_edges = self._get_facility_waste_edges(facility.node_id)
            accepts_waste = any(e.target_id == waste_type_id for e in facility_waste_edges)
            
            if not accepts_waste:
                continue
            
            # Find processes that can handle this waste
            waste_process_edges = self._get_waste_process_edges(waste_type_id)
            compatible_processes = []
            
            for edge in waste_process_edges:
                process = self.kg.get_node(edge.target_id)
                if process and isinstance(process, Process):
                    compatible_processes.append(process)
            
            # Find processes supported by this facility
            facility_process_edges = self._get_facility_process_edges(facility.node_id)
            supported_processes = [self.kg.get_node(e.target_id) 
                                  for e in facility_process_edges]
            supported_processes = [p for p in supported_processes 
                                  if p and isinstance(p, Process)]
            
            # Find intersection
            usable_processes = [p for p in compatible_processes 
                               if p in supported_processes]
            
            if not usable_processes:
                continue
            
            # For simplicity, use the first process (could be enhanced)
            process = usable_processes[0]
            
            # Find resources produced
            resource_edges = self._get_process_resource_edges(process.node_id)
            produced_resources = []
            
            for edge in resource_edges:
                resource = self.kg.get_node(edge.target_id)
                if resource and isinstance(resource, Resource):
                    produced_resources.append(resource)
            
            if not produced_resources:
                continue
            
            resource = produced_resources[0]
            
            # Calculate costs and values (simplified for now)
            # In a real implementation, these would come from the node properties
            distance_km = 10.0  # Placeholder - would come from geospatial data
            transport_cost = distance_km * 0.5  # $0.50 per km per tonne
            processing_cost = process.energy_requirement_kwh_per_tonne or 50.0  # Placeholder
            resource_value = resource.economic_value_per_tonne or 100.0  # Placeholder
            
            total_cost = transport_cost + processing_cost
            net_value = resource_value - total_cost
            
            # Get constraints
            constraints = []
            facility_constraints = self._get_constraint_edges(facility.node_id)
            process_constraints = self._get_constraint_edges(process.node_id)
            
            for edge in facility_constraints + process_constraints:
                constraint = self.kg.get_node(edge.source_id)
                if constraint and isinstance(constraint, Constraint):
                    constraints.append(constraint)
            
            suggestion = RouteSuggestion(
                facility=facility,
                process=process,
                resource=resource,
                distance_km=distance_km,
                transport_cost=transport_cost,
                processing_cost=processing_cost,
                total_cost=total_cost,
                resource_value=resource_value,
                net_value=net_value,
                constraints=constraints
            )
            results.append(suggestion)
        
        # Sort by net value (descending)
        results.sort(key=lambda x: x.net_value, reverse=True)
        return results[:max_results]
    
    def list_resources_from_stream(self, waste_stream_id: str) -> List[Dict[str, Any]]:
        """
        List all possible resources that can be produced from a waste stream.
        
        Args:
            waste_stream_id: ID of the waste stream
        
        Returns:
            List of resource information dictionaries
        """
        results = []
        
        waste_stream = self.kg.get_node(waste_stream_id)
        if not waste_stream or not isinstance(waste_stream, WasteStream):
            return results
        
        # Get waste types in this stream (via WASTESTREAMHASWASTETYPE edges)
        stream_waste_edges = [e for e in self._edges_by_source.get(waste_stream_id, [])
                             if e.edge_type == EdgeType.WASTESTREAMHASWASTETYPE]
        
        waste_types = []
        for edge in stream_waste_edges:
            waste_type = self.kg.get_node(edge.target_id)
            if waste_type and isinstance(waste_type, WasteType):
                waste_types.append(waste_type)
        
        # If no specific waste types, try to infer from stream name or use all waste types
        if not waste_types:
            # Look for waste types that might be related
            all_waste_types = self._nodes_by_type.get(NodeType.WASTE_TYPE, [])
            waste_types = all_waste_types
        
        # For each waste type, find all possible resource pathways
        for waste_type in waste_types:
            # Find processes that can handle this waste
            waste_process_edges = self._get_waste_process_edges(waste_type.node_id)
            
            for edge in waste_process_edges:
                process = self.kg.get_node(edge.target_id)
                if not process or not isinstance(process, Process):
                    continue
                
                # Find resources produced by this process
                resource_edges = self._get_process_resource_edges(process.node_id)
                
                for res_edge in resource_edges:
                    resource = self.kg.get_node(res_edge.target_id)
                    if resource and isinstance(resource, Resource):
                        results.append({
                            "waste_type": waste_type.name,
                            "process": process.name,
                            "resource": resource.name,
                            "resource_id": resource.node_id,
                            "economic_value": resource.economic_value_per_tonne,
                            "quality_grade": resource.quality_grade,
                            "market_demand": resource.market_demand
                        })
        
        return results
    
    def get_top_resource_pathways(self, waste_type_id: str, quantity_kg: float = 1000.0,
                                  max_results: int = 3) -> List[Pathway]:
        """
        Get top resource pathways for a given waste type and quantity.
        
        This is the main query function called by the ML layer after forecasting.
        
        Args:
            waste_type_id: ID of the waste type
            quantity_kg: Quantity of waste in kg
            max_results: Maximum number of pathways to return
        
        Returns:
            List of pathways ranked by efficiency and economic value
        """
        pathways = []
        
        waste_type = self.kg.get_node(waste_type_id)
        if not waste_type or not isinstance(waste_type, WasteType):
            return pathways
        
        # Find processes that can handle this waste
        waste_process_edges = self._get_waste_process_edges(waste_type_id)
        
        for edge in waste_process_edges:
            process = self.kg.get_node(edge.target_id)
            if not process or not isinstance(process, Process):
                continue
            
            # Find resources produced by this process
            resource_edges = self._get_process_resource_edges(process.node_id)
            
            for res_edge in resource_edges:
                resource = self.kg.get_node(res_edge.target_id)
                if not resource or not isinstance(resource, Resource):
                    continue
                
                # Find facilities that support this process and accept this waste
                facilities = self._find_compatible_facilities(waste_type_id, process.node_id)
                
                # Get constraints
                constraints = self._get_all_constraints(waste_type_id, process.node_id, 
                                                        [f.node_id for f in facilities])
                
                # Calculate pathway metrics
                efficiency = process.efficiency or 80.0  # Default 80%
                economic_value = (resource.economic_value_per_tonne or 0.0) * (quantity_kg / 1000)
                carbon_footprint = (process.carbon_footprint_kg_co2_per_tonne or 0.0) * (quantity_kg / 1000)
                
                pathway = Pathway(
                    waste_type=waste_type,
                    process=process,
                    resource=resource,
                    facilities=facilities,
                    constraints=constraints,
                    efficiency=efficiency,
                    economic_value=economic_value,
                    carbon_footprint=carbon_footprint
                )
                pathways.append(pathway)
        
        # Sort by economic value (descending), then by efficiency
        pathways.sort(key=lambda x: (x.economic_value, x.efficiency), reverse=True)
        return pathways[:max_results]
    
    def _find_compatible_facilities(self, waste_type_id: str, process_id: str) -> List[Facility]:
        """Find facilities that can handle a waste type with a specific process."""
        facilities = []
        
        all_facilities = self._nodes_by_type.get(NodeType.FACILITY, [])
        
        for facility in all_facilities:
            # Check if facility accepts the waste type
            waste_edges = self._get_facility_waste_edges(facility.node_id)
            accepts_waste = any(e.target_id == waste_type_id for e in waste_edges)
            
            if not accepts_waste:
                continue
            
            # Check if facility supports the process
            process_edges = self._get_facility_process_edges(facility.node_id)
            supports_process = any(e.target_id == process_id for e in process_edges)
            
            if supports_process:
                facilities.append(facility)
        
        return facilities
    
    def _get_all_constraints(self, waste_type_id: str, process_id: str, 
                           facility_ids: List[str]) -> List[Constraint]:
        """Get all constraints that apply to a waste-process-facility combination."""
        constraints = []
        seen_ids = set()
        
        # Get constraints for waste type
        for edge in self._get_constraint_edges(waste_type_id):
            constraint = self.kg.get_node(edge.source_id)
            if constraint and isinstance(constraint, Constraint) and constraint.node_id not in seen_ids:
                constraints.append(constraint)
                seen_ids.add(constraint.node_id)
        
        # Get constraints for process
        for edge in self._get_constraint_edges(process_id):
            constraint = self.kg.get_node(edge.source_id)
            if constraint and isinstance(constraint, Constraint) and constraint.node_id not in seen_ids:
                constraints.append(constraint)
                seen_ids.add(constraint.node_id)
        
        # Get constraints for each facility
        for fac_id in facility_ids:
            for edge in self._get_constraint_edges(fac_id):
                constraint = self.kg.get_node(edge.source_id)
                if constraint and isinstance(constraint, Constraint) and constraint.node_id not in seen_ids:
                    constraints.append(constraint)
                    seen_ids.add(constraint.node_id)
        
        return constraints
    
    def _calculate_symbiosis_score(self, facility: Facility, process: Process,
                                   resource: Resource, actors: List[Actor],
                                   quantity: float) -> float:
        """Calculate synergy score for symbiosis (0-100)."""
        score = 0.0
        
        # Economic factor (0-40 points)
        resource_value = resource.economic_value_per_tonne or 0.0
        economic_score = min(resource_value / 200 * 40, 40)  # Cap at 40
        score += economic_score
        
        # Environmental factor (0-30 points)
        carbon_reduction = 0.0
        if process.carbon_footprint_kg_co2_per_tonne:
            # Assume waste would otherwise emit CH4 (25x CO2 equivalent)
            baseline = quantity * 0.1 * 25  # 10% of waste as CH4
            process_emissions = process.carbon_footprint_kg_co2_per_tonne * (quantity / 1000)
            carbon_reduction = baseline - process_emissions
        env_score = min(carbon_reduction / 100 * 30, 30)  # Cap at 30
        score += env_score
        
        # Actor demand factor (0-20 points)
        demand_score = min(len(actors) * 5, 20)  # 5 points per actor, max 20
        score += demand_score
        
        # Facility capacity factor (0-10 points)
        capacity = facility.capacity_tonnes_per_year or 10000
        capacity_score = min((quantity / 1000) / capacity * 100 * 0.1, 10)
        score += capacity_score
        
        return min(score, 100)
    
    def _calculate_environmental_benefit(self, process: Process, resource: Resource,
                                       quantity: float) -> float:
        """Calculate environmental benefit in kg CO2e avoided."""
        # Baseline: waste going to landfill emits CH4
        # 1 tonne of organic waste in landfill ≈ 200 kg CH4 ≈ 5000 kg CO2e
        baseline_emissions = quantity / 1000 * 5000
        
        # Process emissions
        process_emissions = (process.carbon_footprint_kg_co2_per_tonne or 0.0) * (quantity / 1000)
        
        # Net benefit
        return baseline_emissions - process_emissions
    
    def _calculate_economic_benefit(self, process: Process, resource: Resource,
                                   quantity: float) -> float:
        """Calculate economic benefit in USD."""
        # Resource value
        resource_value = (resource.economic_value_per_tonne or 0.0) * (quantity / 1000)
        
        # Processing cost
        processing_cost = (process.energy_requirement_kwh_per_tonne or 50.0) * 0.10 * (quantity / 1000)
        
        # Net benefit
        return resource_value - processing_cost
    
    def query_graph(self, cypher_query: str) -> List[Dict[str, Any]]:
        """
        Execute a Cypher-like query on the knowledge graph.
        
        This is a simplified implementation that can be extended to support
        a full query language or integrate with Neo4j.
        
        Args:
            cypher_query: Query string in simplified format
        
        Returns:
            List of result dictionaries
        """
        # Parse simple queries
        query_lower = cypher_query.lower().strip()
        
        if query_lower.startswith("match waste_type"):
            # Example: "MATCH Waste_Type->Process->Resource RETURN *"
            return self._execute_match_query(query_lower)
        elif query_lower.startswith("find pathways"):
            # Example: "FIND PATHWAYS FOR FoodScraps"
            return self._execute_find_pathways(query_lower)
        else:
            # Default: return all nodes
            return [n.to_dict() for n in self.kg.nodes.values()]
    
    def _execute_match_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a MATCH query."""
        results = []
        
        # Simple pattern: MATCH Waste_Type->Process->Resource
        if "->process->resource" in query:
            waste_types = self._nodes_by_type.get(NodeType.WASTE_TYPE, [])
            for wt in waste_types:
                # Find processes for this waste
                for edge in self._get_waste_process_edges(wt.node_id):
                    process = self.kg.get_node(edge.target_id)
                    if not process or not isinstance(process, Process):
                        continue
                    # Find resources from this process
                    for res_edge in self._get_process_resource_edges(process.node_id):
                        resource = self.kg.get_node(res_edge.target_id)
                        if resource and isinstance(resource, Resource):
                            results.append({
                                "waste_type": wt.name,
                                "process": process.name,
                                "resource": resource.name
                            })
        
        return results
    
    def _execute_find_pathways(self, query: str) -> List[Dict[str, Any]]:
        """Execute a FIND PATHWAYS query."""
        # Extract waste type from query
        parts = query.split()
        if len(parts) >= 4 and parts[2] == "for":
            waste_name = ' '.join(parts[3:])
            # Find waste type by name
            for node in self._nodes_by_type.get(NodeType.WASTE_TYPE, []):
                if node.name.lower() == waste_name.lower():
                    pathways = self.get_top_resource_pathways(node.node_id)
                    return [p.to_dict() for p in pathways]
        
        return []


# Convenience functions
def get_query_engine(kg: KnowledgeGraph) -> KGQueryEngine:
    """Get a query engine for the given knowledge graph."""
    return KGQueryEngine(kg)


def suggest_symbiosis(kg: KnowledgeGraph, facility_id: str, waste_profile: Dict[str, float]) -> List[SymbiosisResult]:
    """Suggest symbiosis for a facility."""
    engine = KGQueryEngine(kg)
    return engine.suggest_symbiosis_for_facility(facility_id, waste_profile)


def suggest_routes(kg: KnowledgeGraph, cluster_id: str, waste_type_id: str, max_results: int = 5) -> List[RouteSuggestion]:
    """Suggest alternative routes."""
    engine = KGQueryEngine(kg)
    return engine.suggest_alternative_routes(cluster_id, waste_type_id, max_results)


def list_resources(kg: KnowledgeGraph, waste_stream_id: str) -> List[Dict[str, Any]]:
    """List resources from a waste stream."""
    engine = KGQueryEngine(kg)
    return engine.list_resources_from_stream(waste_stream_id)


def get_top_pathways(kg: KnowledgeGraph, waste_type_id: str, quantity_kg: float = 1000.0, 
                     max_results: int = 3) -> List[Pathway]:
    """Get top resource pathways."""
    engine = KGQueryEngine(kg)
    return engine.get_top_resource_pathways(waste_type_id, quantity_kg, max_results)
