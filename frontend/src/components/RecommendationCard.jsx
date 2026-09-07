import React from 'react';
import { AlertTriangle, CheckCircle, XCircle, Info, ShieldAlert, ArrowUpRight } from 'lucide-react';

export default function RecommendationCard({ rec, onOpenReviewModal, activeRole }) {
  const isPending = rec.status === 'PENDING';
  const hasHardViolation = !rec.hard_constraint_passed;
  const isOverridden = rec.status === 'OVERRIDDEN';

  const getObjectiveBadgeClass = (obj) => {
    if (obj === 'RISK_REDUCTION') return 'badge-risk';
    if (obj === 'MAX_REACH') return 'badge-reach';
    return 'badge-baseline';
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'ACCEPTED':
        return <span className="badge badge-success"><CheckCircle size={12} /> Accepted</span>;
      case 'OVERRIDDEN':
        return <span className="badge badge-warning"><ShieldAlert size={12} /> Overridden</span>;
      case 'MODIFIED':
        return <span className="badge badge-reach"><Info size={12} /> Modified</span>;
      case 'REJECTED':
        return <span className="badge badge-risk"><XCircle size={12} /> Rejected</span>;
      default:
        return <span className="badge badge-warning"><Info size={12} /> Pending Review</span>;
    }
  };

  return (
    <div className="card" style={{
      borderLeft: hasHardViolation ? '4px solid var(--accent-rose)' : '4px solid var(--accent-blue)',
      marginBottom: '1rem'
    }}>
      {/* Top Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <span style={{
              background: 'rgba(59, 130, 246, 0.2)',
              color: 'var(--accent-cyan)',
              fontWeight: 800,
              fontSize: '0.8rem',
              padding: '0.15rem 0.5rem',
              borderRadius: 'var(--radius-sm)'
            }}>
              RANK #{rec.rank}
            </span>
            <span className={`badge ${getObjectiveBadgeClass(rec.objective)}`}>
              {rec.objective.replace('_', ' ')}
            </span>
            {getStatusBadge(rec.status)}
          </div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--text-primary)' }}>
            {rec.area_name}
          </h3>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            Zone: {rec.zone_type} • Distance: {rec.distance_from_base_km} km from Health Base
          </div>
        </div>

        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Priority Score</div>
          <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--accent-cyan)' }}>
            {rec.priority_score.toFixed(3)}
          </div>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
            Target Reach: <strong>{rec.expected_reach} doses</strong>
          </div>
        </div>
      </div>

      {/* Reason Summary */}
      <div style={{
        marginTop: '1rem',
        padding: '0.75rem',
        backgroundColor: 'rgba(255, 255, 255, 0.02)',
        borderRadius: 'var(--radius-md)',
        fontSize: '0.85rem',
        color: 'var(--text-secondary)',
        border: '1px solid rgba(255, 255, 255, 0.05)'
      }}>
        <div style={{ fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.25rem' }}>
          Explainability Breakdown:
        </div>
        <div>{rec.reason?.summary}</div>

        {/* Factors Bar */}
        {rec.reason?.factors && (
          <div style={{ marginTop: '0.65rem', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
            {rec.reason.factors.map((f, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.78rem' }}>
                <span style={{ color: 'var(--text-muted)' }}>• {f.factor}:</span>
                <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{f.value} ({f.impact})</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Constraint Warnings */}
      {rec.constraint_flags && rec.constraint_flags.length > 0 && (
        <div style={{ marginTop: '0.85rem' }}>
          {rec.constraint_flags.map((flag, idx) => (
            <div key={idx} style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              fontSize: '0.8rem',
              padding: '0.4rem 0.65rem',
              borderRadius: 'var(--radius-sm)',
              marginBottom: '0.35rem',
              backgroundColor: flag.severity === 'HARD' ? 'rgba(244, 63, 94, 0.15)' : 'rgba(245, 158, 11, 0.15)',
              color: flag.severity === 'HARD' ? 'var(--accent-rose)' : 'var(--accent-amber)',
              border: `1px solid ${flag.severity === 'HARD' ? 'rgba(244, 63, 94, 0.3)' : 'rgba(245, 158, 11, 0.3)'}`
            }}>
              <AlertTriangle size={14} />
              <span><strong>[{flag.severity} CONSTRAINT]:</strong> {flag.message}</span>
            </div>
          ))}
        </div>
      )}

      {/* Human Review Action Controls */}
      <div style={{
        marginTop: '1.25rem',
        paddingTop: '0.85rem',
        borderTop: '1px solid var(--border-color)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '0.5rem'
      }}>
        <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
          Human Oversight: Final approval required by authorised clinician/reviewer.
        </div>

        <div style={{ display: 'flex', gap: '0.5rem' }}>
          {hasHardViolation ? (
            <button
              onClick={() => onOpenReviewModal(rec, 'OVERRIDDEN')}
              className="btn btn-danger"
              style={{ fontSize: '0.8rem', padding: '0.45rem 0.85rem' }}
            >
              <ShieldAlert size={14} /> Override Hard Constraint
            </button>
          ) : (
            <>
              <button
                onClick={() => onOpenReviewModal(rec, 'ACCEPTED')}
                className="btn btn-primary"
                disabled={!isPending}
                style={{ fontSize: '0.8rem', padding: '0.45rem 0.85rem', opacity: isPending ? 1 : 0.6 }}
              >
                <CheckCircle size={14} /> Accept
              </button>
              <button
                onClick={() => onOpenReviewModal(rec, 'MODIFIED')}
                className="btn btn-secondary"
                disabled={!isPending}
                style={{ fontSize: '0.8rem', padding: '0.45rem 0.85rem', opacity: isPending ? 1 : 0.6 }}
              >
                Modify Session
              </button>
              <button
                onClick={() => onOpenReviewModal(rec, 'REJECTED')}
                className="btn btn-secondary"
                disabled={!isPending}
                style={{ fontSize: '0.8rem', padding: '0.45rem 0.85rem', color: 'var(--accent-rose)', opacity: isPending ? 1 : 0.6 }}
              >
                Reject
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
