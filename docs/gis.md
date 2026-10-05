# GIS & Spatial Data Integration

## Overview
The Vaccination Outreach Planner incorporates spatial boundaries and Geographic Information System (GIS) mapping for all 12 synthetic city zones. The application supports standard **GeoJSON FeatureCollections** to render polygon zone boundaries alongside interactive mobile outreach markers on the React Leaflet map interface.

---

## 1. GeoJSON Structure

Spatial polygons are stored in `backend/app/data/city_zones.geojson`.

Each feature represents a city zone boundary with properties enriched dynamically from live database models:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "AREA-07",
      "properties": {
        "area_id": "AREA-07",
        "area_name": "Eastside Railway Market",
        "zone_type": "Mobile Vendor Settlement",
        "distance_from_base_km": 7.8,
        "population": 14200,
        "eligible_population": 4800,
        "vaccination_coverage": 20.4,
        "emerging_risk": 0.96,
        "accessibility_index": 0.55
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [-73.9300, 40.7140],
            [-73.9100, 40.7140],
            [-73.9100, 40.6980],
            [-73.9300, 40.6980],
            [-73.9300, 40.7140]
          ]
        ]
      }
    }
  ]
}
```

---

## 2. API Endpoint

### Endpoint: `GET /api/areas/geojson`

- **Description**: Serves the complete city zone polygon GeoJSON FeatureCollection dynamically enriched with real-time vaccination coverage, risk scores, and accessibility metrics from SQLite.
- **Access**: Public / Authenticated.
- **Content-Type**: `application/json`

---

## 3. Frontend Visualization

In the React frontend (`frontend/src/components/AreaMap.jsx`), the map component consumes the `/api/areas/geojson` endpoint and renders:
1. **Interactive GeoJSON Polygon Layers**: Colored dynamically by emerging risk severity (Green $\to$ Yellow $\to$ Red).
2. **Zone Centroid Markers**: Displaying click popups with zone demographics, coverage gaps, and allocated session counts.

---

## 4. Synthetic Data Disclaimer

> [!NOTE]
> All zone geometries, coordinates, and demographic attributes are synthetic datasets designed for demonstration and algorithmic evaluation purposes. They do not represent real-world clinical patient identifiers or exact municipal boundary registries.
