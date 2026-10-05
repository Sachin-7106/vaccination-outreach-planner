import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, GeoJSON } from 'react-leaflet';
import { fetchAreasGeoJSON } from '../services/api';

const DEFAULT_CENTER = [40.7128, -74.0060];

export default function AreaMap({ areas = [], selectedAreaId, onSelectArea }) {
  const [geoJsonData, setGeoJsonData] = useState(null);

  useEffect(() => {
    fetchAreasGeoJSON()
      .then(data => setGeoJsonData(data))
      .catch(err => console.error("GeoJSON fetch warning:", err));
  }, []);

  const getMarkerColor = (emergingRisk) => {
    if (emergingRisk >= 0.75) return '#e11d48';
    if (emergingRisk >= 0.45) return '#f59e0b';
    return '#10b981';
  };

  const geoJsonStyle = (feature) => {
    const risk = feature.properties.emerging_risk || 0.4;
    const isSelected = feature.properties.area_id === selectedAreaId;
    return {
      color: isSelected ? '#3b82f6' : getMarkerColor(risk),
      weight: isSelected ? 3 : 1.5,
      fillColor: getMarkerColor(risk),
      fillOpacity: isSelected ? 0.45 : 0.2
    };
  };

  return (
    <div style={{ position: 'relative', height: '100%', width: '100%', minHeight: 420 }}>
      <MapContainer center={DEFAULT_CENTER} zoom={11} scrollWheelZoom={false}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {geoJsonData && (
          <GeoJSON
            key={selectedAreaId || 'geojson-layer'}
            data={geoJsonData}
            style={geoJsonStyle}
            onEachFeature={(feature, layer) => {
              layer.on({
                click: () => onSelectArea && onSelectArea(feature.properties.area_id)
              });
            }}
          />
        )}

        {areas.map(area => {
          const color = getMarkerColor(area.emerging_risk);
          const isSelected = area.area_id === selectedAreaId;
          const radius = Math.max(12, Math.min(26, area.eligible_population / 250));

          return (
            <CircleMarker
              key={area.area_id}
              center={[area.latitude, area.longitude]}
              radius={radius}
              pathOptions={{
                color: isSelected ? '#2563eb' : color,
                fillColor: color,
                fillOpacity: 0.7,
                weight: isSelected ? 4 : 2
              }}
              eventHandlers={{
                click: () => onSelectArea && onSelectArea(area.area_id)
              }}
            >
              <Popup>
                <div style={{ fontFamily: 'sans-serif', padding: '0.2rem' }}>
                  <h4 style={{ margin: '0 0 0.4rem 0', color: '#1e293b' }}>{area.area_name}</h4>
                  <div style={{ fontSize: '0.8rem', color: '#475569', lineHeight: 1.4 }}>
                    <div><strong>Zone:</strong> {area.zone_type}</div>
                    <div><strong>Eligible Population:</strong> {area.eligible_population ? area.eligible_population.toLocaleString() : 0}</div>
                    <div><strong>Vaccination Coverage:</strong> {area.vaccination_coverage}%</div>
                    <div><strong>Emerging Disease Risk:</strong> <span style={{ color: area.emerging_risk > 0.7 ? '#e11d48' : '#059669', fontWeight: 'bold' }}>{area.emerging_risk}</span></div>
                    <div><strong>Mobility Index:</strong> {area.mobility_index}</div>
                    <div><strong>Dist from Health HQ:</strong> {area.distance_from_base_km} km</div>
                  </div>
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>
    </div>
  );
}
