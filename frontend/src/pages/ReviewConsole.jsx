import React, { useEffect, useState } from 'react';
import { CheckSquare, ShieldCheck, History, AlertCircle } from 'lucide-react';
import RecommendationCard from '../components/RecommendationCard';
import HumanReviewModal from '../components/HumanReviewModal';
import { fetchRecommendations, fetchAuditTrail, submitReview } from '../services/api';

export default function ReviewConsole({ activeRole }) {
  const [recommendations, setRecommendations] = useState([]);
  const [auditTrail, setAuditTrail] = useState([]);
  const [activeTab, setActiveTab] = useState('PENDING'); // PENDING vs AUDIT
  const [loading, setLoading] = useState(true);
  const [reviewModalData, setReviewModalData] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [recs, audit] = await Promise.all([
        fetchRecommendations(),
        fetchAuditTrail()
      ]);
      setRecommendations(recs);
      setAuditTrail(audit);
    } catch (err) {
      console.error('Error loading review console:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenReviewModal = (rec, decisionType) => {
    setReviewModalData({ rec, decisionType });
  };

  const handleSubmitReview = async (payload) => {
    await submitReview(payload);
    await loadData();
  };

  const pendingRecs = recommendations.filter(r => r.status === 'PENDING');

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">
          <CheckSquare style={{ color: 'var(--accent-teal)' }} />
          Human Oversight & Review Console
        </h1>
        <p className="page-description">
          Review, modify, approve, or record justified overrides for automated outreach recommendations. All actions are recorded in an immutable audit trail.
        </p>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
        <button
          onClick={() => setActiveTab('PENDING')}
          className={`btn ${activeTab === 'PENDING' ? 'btn-primary' : 'btn-secondary'}`}
        >
          Pending Review ({pendingRecs.length})
        </button>
        <button
          onClick={() => setActiveTab('AUDIT')}
          className={`btn ${activeTab === 'AUDIT' ? 'btn-primary' : 'btn-secondary'}`}
        >
          <History size={16} /> Public Health Audit Log ({auditTrail.length})
        </button>
      </div>

      {activeTab === 'PENDING' ? (
        <div>
          {pendingRecs.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: '3rem 1.5rem', color: 'var(--text-muted)' }}>
              <ShieldCheck size={36} style={{ color: 'var(--accent-emerald)', marginBottom: '0.5rem' }} />
              <h3>All Recommendations Reviewed</h3>
              <p style={{ fontSize: '0.85rem' }}>No pending recommendations require human decision at this time.</p>
            </div>
          ) : (
            pendingRecs.map(rec => (
              <RecommendationCard
                key={rec.recommendation_id}
                rec={rec}
                onOpenReviewModal={handleOpenReviewModal}
                activeRole={activeRole}
              />
            ))
          )}
        </div>
      ) : (
        <div className="card">
          <div className="card-title">
            <span>Immutable Human Oversight Audit Trail</span>
            <span className="badge badge-success">Audit Compliance Ready</span>
          </div>

          <div className="data-table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Timestamp (UTC)</th>
                  <th>Reviewer ID & Role</th>
                  <th>Decision</th>
                  <th>Override / Modification Reason</th>
                </tr>
              </thead>
              <tbody>
                {auditTrail.length === 0 ? (
                  <tr>
                    <td colSpan="4" style={{ textAlign: 'center', color: 'var(--text-muted)' }}>
                      No human review records logged yet.
                    </td>
                  </tr>
                ) : (
                  auditTrail.map(log => (
                    <tr key={log.review_id}>
                      <td style={{ fontSize: '0.8rem', fontFamily: 'var(--font-mono)' }}>
                        {new Date(log.timestamp).toLocaleString()}
                      </td>
                      <td>
                        <strong>{log.reviewer_id}</strong>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{log.reviewer_role}</div>
                      </td>
                      <td>
                        <span className={`badge ${
                          log.decision === 'ACCEPTED' ? 'badge-success' :
                          log.decision === 'OVERRIDDEN' ? 'badge-warning' :
                          log.decision === 'MODIFIED' ? 'badge-reach' : 'badge-risk'
                        }`}>
                          {log.decision}
                        </span>
                      </td>
                      <td style={{ fontSize: '0.85rem' }}>
                        {log.override_reason ? (
                          <span style={{ color: 'var(--accent-amber)', fontStyle: 'italic' }}>
                            "{log.override_reason}"
                          </span>
                        ) : log.modified_capacity ? (
                          <span>Capacity adjusted to {log.modified_capacity} doses</span>
                        ) : (
                          <span style={{ color: 'var(--text-muted)' }}>Standard Approval</span>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Review Modal */}
      {reviewModalData && (
        <HumanReviewModal
          recommendation={reviewModalData.rec}
          decisionType={reviewModalData.decisionType}
          onClose={() => setReviewModalData(null)}
          onSubmitReview={handleSubmitReview}
          activeRole={activeRole}
        />
      )}
    </div>
  );
}
