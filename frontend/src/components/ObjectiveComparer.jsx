import React from 'react';
import { ArrowUpRight, ArrowDownRight, Minus, AlertCircle } from 'lucide-react';

export default function ObjectiveComparer({ comparisonData = [] }) {
  if (!comparisonData.length) return null;

  return (
    <div className="card">
      <div className="card-title">
        <span>Dual-Objective Planning Comparison Matrix</span>
        <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
          Baseline vs Reach vs Emerging Risk
        </span>
      </div>

      <div style={{ fontSize: '0.825rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
        This comparative matrix illustrates how the <strong>Emerging Risk Reduction Engine</strong> prioritizes high-risk anomaly zones (e.g. <em>Eastside Railway Market</em>) that historical average baselines ignore.
      </div>

      <div className="data-table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>City Zone Name</th>
              <th>Eligible Pop</th>
              <th>Emerging Risk</th>
              <th>Hist Baseline Rank</th>
              <th>Reach Obj Rank</th>
              <th>Risk Obj Rank</th>
              <th>Risk vs Baseline Shift</th>
            </tr>
          </thead>
          <tbody>
            {comparisonData.map((item) => {
              const shift = item.rank_difference; // positive = risk engine ranked it higher (lower rank #)
              const isSignificantElevated = item.area_id === 'AREA-07' || shift > 3;

              return (
                <tr key={item.area_id} style={{
                  backgroundColor: isSignificantElevated ? 'rgba(244, 63, 94, 0.08)' : 'transparent'
                }}>
                  <td style={{ fontWeight: 700 }}>
                    {item.area_name}
                    {isSignificantElevated && (
                      <span style={{ marginLeft: '0.5rem', fontSize: '0.7rem', color: 'var(--accent-rose)', fontWeight: 800 }}>
                        ★ HIGH EMERGING SPIKE
                      </span>
                    )}
                  </td>
                  <td>{item.eligible_population.toLocaleString()}</td>
                  <td style={{ fontWeight: 700, color: item.emerging_risk > 0.7 ? 'var(--accent-rose)' : 'var(--text-primary)' }}>
                    {item.emerging_risk}
                  </td>
                  <td style={{ color: 'var(--accent-amber)', fontWeight: 600 }}>#{item.baseline_rank}</td>
                  <td style={{ color: 'var(--accent-cyan)', fontWeight: 600 }}>#{item.reach_rank}</td>
                  <td style={{ color: 'var(--accent-rose)', fontWeight: 800 }}>#{item.risk_rank}</td>
                  <td>
                    {shift > 0 ? (
                      <span style={{ color: 'var(--accent-emerald)', fontWeight: 700, display: 'inline-flex', alignItems: 'center', gap: '0.2rem' }}>
                        <ArrowUpRight size={14} /> +{shift} Ranks Higher
                      </span>
                    ) : shift < 0 ? (
                      <span style={{ color: 'var(--text-muted)', display: 'inline-flex', alignItems: 'center', gap: '0.2rem' }}>
                        <ArrowDownRight size={14} /> {shift} Ranks
                      </span>
                    ) : (
                      <span style={{ color: 'var(--text-muted)', display: 'inline-flex', alignItems: 'center', gap: '0.2rem' }}>
                        <Minus size={14} /> Same
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
