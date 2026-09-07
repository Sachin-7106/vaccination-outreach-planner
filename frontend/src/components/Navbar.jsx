import React from 'react';
import { Shield, Activity, MapPin, Calendar, CheckSquare, BarChart3, UserCheck, BookOpen } from 'lucide-react';

export default function Navbar({ activePage, setActivePage, activeRole, setActiveRole }) {
  const roles = [
    { id: 'PLANNER', label: 'Public Health Planner', badge: 'Planner' },
    { id: 'COORDINATOR', label: 'Outreach Coordinator', badge: 'Operations' },
    { id: 'CLINICIAN', label: 'Clinician / Authorised Reviewer', badge: 'Approval Auth' },
    { id: 'COMMUNITY_REP', label: 'Under-Served Population Rep', badge: 'Advocate' }
  ];

  return (
    <header style={{
      backgroundColor: 'var(--bg-card)',
      borderBottom: '1px solid var(--border-color)',
      padding: '0.85rem 2rem',
      position: 'sticky',
      top: 0,
      zIndex: 100
    }}>
      <div style={{
        maxWidth: 1440,
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        {/* Logo & Title */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div style={{
            background: 'linear-gradient(135deg, var(--accent-blue), var(--accent-cyan))',
            padding: '0.5rem',
            borderRadius: 'var(--radius-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            boxShadow: 'var(--shadow-glow-blue)'
          }}>
            <Shield size={24} />
          </div>
          <div>
            <div style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.01em' }}>
              City Health Department
            </div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span>Seasonal Infectious Disease Planner</span>
              <span style={{
                fontSize: '0.65rem',
                padding: '0.1rem 0.4rem',
                borderRadius: '4px',
                background: 'rgba(59, 130, 246, 0.2)',
                color: 'var(--accent-blue)',
                fontWeight: 700
              }}>
                DEMO / SYNTHETIC DATA ONLY
              </span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
          {[
            { id: 'dashboard', label: 'Dashboard', icon: Activity },
            { id: 'explorer', label: 'Area Explorer', icon: MapPin },
            { id: 'planner', label: 'Outreach Planner', icon: Calendar },
            { id: 'reviews', label: 'Review Console', icon: CheckSquare },
            { id: 'eval', label: 'Evaluation & Error Analysis', icon: BarChart3 },
            { id: 'journeys', label: 'User Journeys', icon: BookOpen }
          ].map(nav => {
            const Icon = nav.icon;
            const isActive = activePage === nav.id;
            return (
              <button
                key={nav.id}
                onClick={() => setActivePage(nav.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.45rem',
                  padding: '0.5rem 0.85rem',
                  borderRadius: 'var(--radius-md)',
                  fontSize: '0.85rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  border: 'none',
                  backgroundColor: isActive ? 'rgba(59, 130, 246, 0.15)' : 'transparent',
                  color: isActive ? 'var(--accent-cyan)' : 'var(--text-secondary)',
                  transition: 'all 0.15s ease'
                }}
              >
                <Icon size={16} />
                <span>{nav.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Role Selector */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <UserCheck size={16} style={{ color: 'var(--accent-teal)' }} />
          <select
            value={activeRole}
            onChange={(e) => setActiveRole(e.target.value)}
            className="form-select"
            style={{ fontSize: '0.8rem', padding: '0.35rem 0.65rem' }}
          >
            {roles.map(r => (
              <option key={r.id} value={r.id}>
                {r.label} ({r.badge})
              </option>
            ))}
          </select>
        </div>
      </div>
    </header>
  );
}
