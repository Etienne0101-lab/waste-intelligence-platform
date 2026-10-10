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

try:
    from .ml import (
        ContaminationCNN,
        ClusterAnomalyDetector,
        ModelRegistry,
        MLInferenceEngine,
    )
    from .ml.training import (
        train_contamination_model,
        train_forecasting_model,
        train_anomaly_model,
    )
    from .ml.utils import (
        add_lag_features,
        add_temporal_features,
        build_spatial_features,
        compute_classification_metrics,
        compute_regression_metrics,
        normalize_numeric_columns,
        prepare_time_series_dataframe,
        set_deterministic_seed,
    )
except ImportError:
    pass
