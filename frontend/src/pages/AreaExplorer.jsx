import React, { useEffect, useState } from 'react';
import { MapPin, Search, Filter, ShieldAlert, CheckCircle2 } from 'lucide-react';
import AreaMap from '../components/AreaMap';
import { fetchAreas } from '../services/api';

export default function AreaExplorer() {
  const [areas, setAreas] = useState([]);
  const [search, setSearch] = useState('');
  const [selectedZoneType, setSelectedZoneType] = useState('ALL');
  const [selectedAreaId, setSelectedAreaId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAreas() {
      try {
        const data = await fetchAreas();
        setAreas(data);
        if (data.length > 0) setSelectedAreaId(data[0].area_id);
      } catch (err) {
        console.error('Error fetching areas:', err);
      } finally {
        setLoading(false);
      }
    }
    loadAreas();
  }, []);

  const filteredAreas = areas.filter(a => {
    const matchesSearch = a.area_name.toLowerCase().includes(search.toLowerCase()) || a.area_id.toLowerCase().includes(search.toLowerCase());
    const matchesZone = selectedZoneType === 'ALL' || a.zone_type === selectedZoneType;
    return matchesSearch && matchesZone;
  });

  const zoneTypes = ['ALL', ...Array.from(new Set(areas.map(a => a.zone_type)))];

  const selectedArea = areas.find(a => a.area_id === selectedAreaId);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">
          <MapPin style={{ color: 'var(--accent-cyan)' }} />
          City Area & Population Surveillance Explorer
        </h1>
        <p className="page-description">
          Explore aggregate demographic indicators, historical vaccination coverage ratios, emerging disease risk indices, and mobility corridors across all 12 city zones.
        </p>
      </div>

      {/* Filter Toolbar */}
      <div className="card" style={{ marginBottom: '1.5rem', padding: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={{ position: 'relative', flex: 1, minWidth: 240 }}>
            <Search size={18} style={{ position: 'absolute', left: 12, top: 12, color: 'var(--text-muted)' }} />
            <input
              type="text"
              placeholder="Search area by name or ID..."
              className="form-input"
              style={{ paddingLeft: '2.4rem', width: '100%' }}
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Filter size={18} style={{ color: 'var(--text-muted)' }} />
            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Zone Type:</span>
            <select
              className="form-select"
              value={selectedZoneType}
              onChange={e => setSelectedZoneType(e.target.value)}
            >
              {zoneTypes.map(zt => (
                <option key={zt} value={zt}>{zt}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Main Grid: Data Table + Interactive Map */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '1.5rem' }}>
        {/* Table View */}
        <div className="card">
          <div className="card-title">
            <span>Aggregated City Zones ({filteredAreas.length})</span>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
              Non-discriminatory Operational Variables
            </span>
          </div>

          <div className="data-table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Area Name</th>
                  <th>Eligible Pop</th>
                  <th>Coverage</th>
                  <th>Emerging Risk</th>
                  <th>Mobility</th>
                  <th>Dist (km)</th>
                </tr>
              </thead>
              <tbody>
                {filteredAreas.map(area => {
                  const isSelected = area.area_id === selectedAreaId;
                  const isHighRisk = area.emerging_risk >= 0.70;

                  return (
                    <tr
                      key={area.area_id}
                      onClick={() => setSelectedAreaId(area.area_id)}
                      style={{
                        cursor: 'pointer',
                        backgroundColor: isSelected ? 'rgba(59, 130, 246, 0.15)' : isHighRisk ? 'rgba(244, 63, 94, 0.05)' : 'transparent'
                      }}
                    >
                      <td style={{ fontWeight: 700 }}>
                        {area.area_name}
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 'normal' }}>
                          {area.zone_type}
                        </div>
                      </td>
                      <td>{area.eligible_population.toLocaleString()}</td>
                      <td>
                        <span style={{
                          fontWeight: 700,
                          color: area.vaccination_coverage < 40 ? 'var(--accent-amber)' : 'var(--accent-emerald)'
                        }}>
                          {area.vaccination_coverage}%
                        </span>
                      </td>
                      <td>
                        <span className={`badge ${isHighRisk ? 'badge-risk' : 'badge-success'}`}>
                          {area.emerging_risk}
                        </span>
                      </td>
                      <td>{area.mobility_index}</td>
                      <td>{area.distance_from_base_km} km</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Leaflet Map & Selected Detail Card */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div className="card" style={{ padding: 0, overflow: 'hidden', height: 420 }}>
            <AreaMap
              areas={filteredAreas}
              selectedAreaId={selectedAreaId}
              onSelectArea={(id) => setSelectedAreaId(id)}
            />
          </div>

          {selectedArea && (
            <div className="card">
              <h4 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
                Selected Zone Details: {selectedArea.area_name}
              </h4>
              <div className="grid-2" style={{ fontSize: '0.825rem', gap: '0.5rem' }}>
                <div><strong>Zone Type:</strong> {selectedArea.zone_type}</div>
                <div><strong>Total Pop:</strong> {selectedArea.population.toLocaleString()}</div>
                <div><strong>Eligible Target:</strong> {selectedArea.eligible_population.toLocaleString()}</div>
                <div><strong>Vaccinated:</strong> {selectedArea.vaccinated_count.toLocaleString()} ({selectedArea.vaccination_coverage}%)</div>
                <div><strong>Emerging Risk Index:</strong> <span style={{ color: 'var(--accent-rose)', fontWeight: 700 }}>{selectedArea.emerging_risk}</span></div>
                <div><strong>Seasonal Risk Index:</strong> {selectedArea.seasonal_risk}</div>
                <div><strong>Mobility Index:</strong> {selectedArea.mobility_index}</div>
                <div><strong>Access Index:</strong> {selectedArea.accessibility_index}</div>
                <div><strong>Historical Demand:</strong> {selectedArea.historical_demand} visits</div>
                <div><strong>Base Distance:</strong> {selectedArea.distance_from_base_km} km</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
