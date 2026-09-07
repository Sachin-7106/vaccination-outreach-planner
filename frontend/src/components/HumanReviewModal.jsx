import React, { useState } from 'react';
import { X, ShieldAlert, CheckCircle, Edit, AlertCircle } from 'lucide-react';

export default function HumanReviewModal({ recommendation, decisionType, onClose, onSubmitReview, activeRole }) {
  const [overrideReason, setOverrideReason] = useState('');
  const [modifiedCapacity, setModifiedCapacity] = useState(recommendation?.expected_reach || 300);
  const [errorMsg, setErrorMsg] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!recommendation) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');

    if (decisionType === 'OVERRIDDEN' && (!overrideReason || overrideReason.trim().length < 5)) {
      setErrorMsg('Mandatory Audit Rule: Overriding a hard operational constraint requires a documented reason (min 5 characters).');
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmitReview({
        recommendation_id: recommendation.recommendation_id,
        reviewer_id: activeRole === 'CLINICIAN' ? 'Clinician.Dr-Vance' : 'Planner.Officer-402',
        reviewer_role: activeRole,
        decision: decisionType,
        override_reason: overrideReason,
        modified_capacity: decisionType === 'MODIFIED' ? parseInt(modifiedCapacity, 10) : undefined
      });
      onClose();
    } catch (err) {
      setErrorMsg(err.message || 'Error submitting review');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            {decisionType === 'OVERRIDDEN' ? (
              <ShieldAlert size={22} style={{ color: 'var(--accent-rose)' }} />
            ) : decisionType === 'ACCEPTED' ? (
              <CheckCircle size={22} style={{ color: 'var(--accent-emerald)' }} />
            ) : (
              <Edit size={22} style={{ color: 'var(--accent-cyan)' }} />
            )}
            <h3 style={{ fontSize: '1.15rem', fontWeight: 800 }}>
              {decisionType === 'OVERRIDDEN' ? 'Override Hard Constraint' : `${decisionType} Recommendation`}
            </h3>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
            <X size={20} />
          </button>
        </div>

        <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '1rem', lineHeight: 1.5 }}>
          Target Location: <strong style={{ color: 'var(--text-primary)' }}>{recommendation.area_name}</strong><br />
          Current Status: <span className="badge badge-warning">{recommendation.status}</span>
        </div>

        {errorMsg && (
          <div style={{
            padding: '0.65rem 0.85rem',
            borderRadius: 'var(--radius-md)',
            backgroundColor: 'rgba(244, 63, 94, 0.15)',
            border: '1px solid rgba(244, 63, 94, 0.3)',
            color: 'var(--accent-rose)',
            fontSize: '0.8rem',
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <AlertCircle size={16} />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {decisionType === 'MODIFIED' && (
            <div className="form-group">
              <label className="form-label">Adjust Session Reach Capacity (doses)</label>
              <input
                type="number"
                min="50"
                max="2000"
                className="form-input"
                value={modifiedCapacity}
                onChange={e => setModifiedCapacity(e.target.value)}
                required
              />
            </div>
          )}

          {decisionType === 'OVERRIDDEN' && (
            <div className="form-group">
              <label className="form-label">
                Operational Override Justification <span style={{ color: 'var(--accent-rose)' }}>* (Required)</span>
              </label>
              <textarea
                className="form-input"
                rows="3"
                placeholder="e.g., Authorized secondary mobile transit bus allocated; road detour bypass approved."
                value={overrideReason}
                onChange={e => setOverrideReason(e.target.value)}
                required
              />
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
                This statement will be permanently recorded in the immutable public health audit log.
              </span>
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem', marginTop: '1.5rem' }}>
            <button type="button" onClick={onClose} className="btn btn-secondary">
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className={`btn ${decisionType === 'OVERRIDDEN' ? 'btn-danger' : 'btn-primary'}`}
            >
              {isSubmitting ? 'Recording...' : `Confirm ${decisionType}`}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
