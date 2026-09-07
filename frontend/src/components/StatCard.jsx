import React from 'react';

export default function StatCard({ title, value, subtitle, icon: Icon, color = 'blue', trend }) {
  const colorMap = {
    blue: 'var(--accent-blue)',
    cyan: 'var(--accent-cyan)',
    rose: 'var(--accent-rose)',
    emerald: 'var(--accent-emerald)',
    amber: 'var(--accent-amber)',
    purple: 'var(--accent-purple)'
  };

  const accentColor = colorMap[color] || colorMap.blue;

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
        <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
          {title}
        </span>
        {Icon && (
          <div style={{
            padding: '0.4rem',
            borderRadius: 'var(--radius-sm)',
            backgroundColor: `rgba(255, 255, 255, 0.05)`,
            color: accentColor
          }}>
            <Icon size={20} />
          </div>
        )}
      </div>

      <div>
        <div style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
          {value}
        </div>
        {subtitle && (
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
            {subtitle}
          </div>
        )}
      </div>

      {trend && (
        <div style={{
          fontSize: '0.75rem',
          fontWeight: 700,
          marginTop: '0.75rem',
          color: trend.positive ? 'var(--accent-emerald)' : 'var(--accent-rose)'
        }}>
          {trend.positive ? '↑' : '↓'} {trend.text}
        </div>
      )}
    </div>
  );
}
