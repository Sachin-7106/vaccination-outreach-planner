import React from 'react';
import { AlertOctagon, HelpCircle, ShieldCheck, ArrowRight } from 'lucide-react';

export default function ErrorAnalysisWidget({ scenarios = [] }) {
  if (!scenarios.length) return null;

  return (
    <div>
      <div style={{ marginBottom: '1.25rem' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <AlertOctagon size={20} style={{ color: 'var(--accent-rose)' }} />
          Algorithmic Failure Mode & Error Analysis
        </h3>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
          Public health planning algorithms have boundary conditions. Below are 4 empirical edge cases where the automated planner struggles, requiring explicit human reviewer control.
        </p>
      </div>

      <div className="grid-2">
        {scenarios.map(sc => (
          <div key={sc.id} className="card" style={{ borderTop: '3px solid var(--accent-rose)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <span className="badge badge-risk">{sc.id}</span>
              <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>
                Target: {sc.area_name}
              </span>
            </div>

            <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
              {sc.title}
            </h4>

            <p style={{ fontSize: '0.825rem', color: 'var(--text-secondary)', marginBottom: '0.75rem', lineHeight: 1.45 }}>
              {sc.description}
            </p>

            <div style={{
              padding: '0.65rem',
              backgroundColor: 'rgba(244, 63, 94, 0.08)',
              borderRadius: 'var(--radius-md)',
              marginBottom: '0.65rem',
              fontSize: '0.8rem',
              color: 'var(--accent-rose)',
              border: '1px solid rgba(244, 63, 94, 0.2)'
            }}>
              <strong>Potential Consequence:</strong> {sc.consequence}
            </div>

            <div style={{
              padding: '0.65rem',
              backgroundColor: 'rgba(16, 185, 129, 0.08)',
              borderRadius: 'var(--radius-md)',
              fontSize: '0.8rem',
              color: 'var(--accent-emerald)',
              border: '1px solid rgba(16, 185, 129, 0.2)',
              display: 'flex',
              alignItems: 'flex-start',
              gap: '0.5rem'
            }}>
              <ShieldCheck size={16} style={{ shrink: 0, marginTop: 2 }} />
              <div>
                <strong>Human Control Mitigation:</strong> {sc.mitigation}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
