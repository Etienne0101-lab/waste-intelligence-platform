# Hub-and-Spoke Model

## Components

- Spokes: waste bins and autonomous sensor nodes
- Mesh clusters: local aggregation nodes across buildings and blocks
- Hubs: composting, recycling, remediation, or transfer facilities

## Routing logic

The hub layer calculates facility catchment relationships using proximity and operational capacity. Haversine distance is used for geospatial comparisons between bin locations and nearby facilities.

## Regional behavior

The hub layer provides:
- facility-level load forecasting
- route recommendations
- diversion metrics by facility catchment
- dynamic reporting for DSNY operational teams

## Benefits

This architecture reduces dependence on a single centralized cloud path and enables regionally optimized operational decisions.
