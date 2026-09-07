import React from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, Marker } from 'react-leaflet';
import L from 'leaflet';

// Base map center (fictional metro region center)
const DEFAULT_CENTER = [40.7128, -74.0060];

export default function AreaMap({ areas = [], selectedAreaId, onSelectArea }) {
  const getMarkerColor = (emergingRisk) => {
    if (emergingRisk >= 0.75) return 'var(--accent-rose)';
    if (emergingRisk >= 0.45) return 'var(--accent-amber)';
    return 'var(--accent-emerald)';
  };

  return (
    <div style={{ position: 'relative', height: '100%', width: '100%', minHeight: 420 }}>
      <MapContainer center={DEFAULT_CENTER} zoom={11} scrollWheelZoom={false}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

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
                color: isSelected ? '#3b82f6' : color,
                fillColor: color,
                fillOpacity: 0.6,
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
                    <div><strong>Eligible Population:</strong> {area.eligible_population.toLocaleString()}</div>
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
