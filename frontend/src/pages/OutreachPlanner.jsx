import React, { useState, useEffect } from 'react';
import { Calendar, Play, Settings2, Sliders, ShieldCheck, Layers } from 'lucide-react';
import RecommendationCard from '../components/RecommendationCard';
import ObjectiveComparer from '../components/ObjectiveComparer';
import HumanReviewModal from '../components/HumanReviewModal';
import { generatePlan, comparePlan, submitReview } from '../services/api';

export default function OutreachPlanner({ activeRole }) {
  const [numSessions, setNumSessions] = useState(5);
  const [capacity, setCapacity] = useState(300);
  const [maxDistance, setMaxDistance] = useState(12.0);
  const [objective, setObjective] = useState('RISK_REDUCTION');
  const [planningPeriod, setPlanningPeriod] = useState('2026-Q4');

  const [recommendations, setRecommendations] = useState([]);
  const [comparisonData, setComparisonData] = useState([]);
  const [activeTab, setActiveTab] = useState('RECOMMENDATIONS'); // RECOMMENDATIONS vs COMPARISON

  const [isGenerating, setIsGenerating] = useState(false);
  const [reviewModalData, setReviewModalData] = useState(null);

  useEffect(() => {
    // Run initial plan generation on mount
    handleRunPlanner();
  }, []);

  const handleRunPlanner = async () => {
    setIsGenerating(true);
    try {
      const planParams = {
        planning_period: planningPeriod,
        num_sessions: parseInt(numSessions, 10),
        session_capacity: parseInt(capacity, 10),
        max_travel_distance_km: parseFloat(maxDistance),
        objective: objective
      };

      const [recs, comp] = await Promise.all([
        generatePlan(planParams),
        comparePlan(planParams)
      ]);

      setRecommendations(recs);
      setComparisonData(comp);
    } catch (err) {
      console.error('Error generating plan:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleOpenReviewModal = (rec, decisionType) => {
    setReviewModalData({ rec, decisionType });
  };

  const handleSubmitReview = async (reviewPayload) => {
    await submitReview(reviewPayload);
    // Refresh current recommendations list
    await handleRunPlanner();
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">
          <Calendar style={{ color: 'var(--accent-emerald)' }} />
          Vaccination Outreach Resource Allocation Planner
        </h1>
        <p className="page-description">
          Configure mobile team session constraints, objective weights, and travel boundaries to generate explainable outreach recommendations.
        </p>
      </div>

      {/* Main Grid: Control Panel + Results */}
      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '1.5rem' }}>
        {/* Control Panel */}
        <div className="card">
          <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '1.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Settings2 size={18} style={{ color: 'var(--accent-blue)' }} />
            Planner Parameters
          </h3>

          <div className="form-group">
            <label className="form-label">Planning Horizon</label>
            <select
              className="form-select"
              value={planningPeriod}
              onChange={e => setPlanningPeriod(e.target.value)}
            >
              <option value="2026-Q4">2026 Q4 (Current Horizon)</option>
              <option value="2027-Q1">2027 Q1 (Upcoming)</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Available Outreach Sessions: <strong>{numSessions}</strong></label>
            <input
              type="range"
              min="1"
              max="10"
              value={numSessions}
              onChange={e => setNumSessions(e.target.value)}
              style={{ width: '100%' }}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Capacity per Session (doses): <strong>{capacity}</strong></label>
            <input
              type="range"
              min="100"
              max="1000"
              step="50"
              value={capacity}
              onChange={e => setCapacity(e.target.value)}
              style={{ width: '100%' }}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Max Travel Limit: <strong>{maxDistance} km</strong></label>
            <input
              type="range"
              min="3"
              max="25"
              step="0.5"
              value={maxDistance}
              onChange={e => setMaxDistance(e.target.value)}
              style={{ width: '100%' }}
            />
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Locations &gt; {maxDistance} km are flagged for Hard Travel Constraint Override.
            </span>
          </div>

          <div className="form-group" style={{ marginTop: '0.5rem' }}>
            <label className="form-label">Planning Objective</label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
              <label style={{ fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                <input
                  type="radio"
                  name="obj"
                  value="RISK_REDUCTION"
                  checked={objective === 'RISK_REDUCTION'}
                  onChange={e => setObjective(e.target.value)}
                />
                <span style={{ fontWeight: objective === 'RISK_REDUCTION' ? 700 : 400, color: objective === 'RISK_REDUCTION' ? 'var(--accent-rose)' : 'var(--text-secondary)' }}>
                  Emerging Risk Reduction (Proposed)
                </span>
              </label>

              <label style={{ fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                <input
                  type="radio"
                  name="obj"
                  value="MAX_REACH"
                  checked={objective === 'MAX_REACH'}
                  onChange={e => setObjective(e.target.value)}
                />
                <span style={{ fontWeight: objective === 'MAX_REACH' ? 700 : 400, color: objective === 'MAX_REACH' ? 'var(--accent-cyan)' : 'var(--text-secondary)' }}>
                  Maximum Eligible Reach
                </span>
              </label>

              <label style={{ fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                <input
                  type="radio"
                  name="obj"
                  value="HISTORICAL_BASELINE"
                  checked={objective === 'HISTORICAL_BASELINE'}
                  onChange={e => setObjective(e.target.value)}
                />
                <span style={{ fontWeight: objective === 'HISTORICAL_BASELINE' ? 700 : 400, color: objective === 'HISTORICAL_BASELINE' ? 'var(--accent-amber)' : 'var(--text-secondary)' }}>
                  Historical Average Baseline
                </span>
              </label>
            </div>
          </div>

          <button
            onClick={handleRunPlanner}
            disabled={isGenerating}
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '1.25rem' }}
          >
            <Play size={18} /> {isGenerating ? 'Generating Plan...' : 'Generate Recommended Plan'}
          </button>
        </div>

        {/* Results Workspace */}
        <div>
          {/* Workspace Tabs */}
          <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
            <button
              onClick={() => setActiveTab('RECOMMENDATIONS')}
              className={`btn ${activeTab === 'RECOMMENDATIONS' ? 'btn-primary' : 'btn-secondary'}`}
            >
              Recommended Sessions ({recommendations.length})
            </button>
            <button
              onClick={() => setActiveTab('COMPARISON')}
              className={`btn ${activeTab === 'COMPARISON' ? 'btn-primary' : 'btn-secondary'}`}
            >
              Objective Comparison Matrix
            </button>
          </div>

          {activeTab === 'RECOMMENDATIONS' ? (
            <div>
              {recommendations.map(rec => (
                <RecommendationCard
                  key={rec.recommendation_id}
                  rec={rec}
                  onOpenReviewModal={handleOpenReviewModal}
                  activeRole={activeRole}
                />
              ))}
            </div>
          ) : (
            <ObjectiveComparer comparisonData={comparisonData} />
          )}
        </div>
      </div>

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
