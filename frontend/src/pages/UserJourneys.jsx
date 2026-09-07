import React, { useState } from 'react';
import { BookOpen, CheckCircle2, ArrowRight, AlertTriangle, ShieldCheck, UserCheck } from 'lucide-react';

export default function UserJourneys() {
  const [selectedJourney, setSelectedJourney] = useState('JOURNEY_B'); // Default to high urgency

  const journeyA = {
    id: 'JOURNEY_A',
    title: 'Journey A — Lower Urgency Routine Outreach',
    area: 'Northwood Hills Suburb (AREA-02)',
    urgency: 'Low / Moderate',
    profile: 'Suburban area with stable seasonal disease risk (0.20), moderate vaccination coverage (86%), and high geographic access (0.88). No immediate risk spike detected.',
    steps: [
      { step: 1, title: 'Dashboard Monitoring', desc: 'Area 02 is displayed in Area Explorer with stable baseline metrics.' },
      { step: 2, title: 'Planner Evaluation', desc: 'Max Eligible Reach engine scores Area 02 with moderate priority score (0.420).' },
      { step: 3, title: 'Recommendation Generation', desc: 'Planner ranks Area 02 as #6 in session queue.' },
      { step: 4, title: 'Human Review', desc: 'Outreach Coordinator reviews recommendation and approves standard routine session.' },
      { step: 5, title: 'Session Execution', desc: 'Mobile health van visits local community clinic on scheduled date.' },
      { step: 6, title: 'Outcome Recording', desc: '290 eligible individuals vaccinated; session utilisation recorded at 96%.' }
    ]
  };

  const journeyB = {
    id: 'JOURNEY_B',
    title: 'Journey B — Higher Urgency Outbreak Response',
    area: 'Eastside Railway Market (AREA-07)',
    urgency: 'CRITICAL / High Urgency',
    profile: 'Under-served mobile vendor settlement with severe emerging infectious disease risk spike (0.96), low historical attendance (95 visits), high mobility corridor index (0.91), and moderate accessibility (0.55).',
    steps: [
      { step: 1, title: 'Surveillance Risk Alert', desc: 'Disease surveillance signal triggers critical emerging risk alert (0.96) for AREA-07.' },
      { step: 2, title: 'Historical Baseline Under-Ranking Failure', desc: 'Historical average baseline ranks AREA-07 low (#10) due to past attendance history (95 visits).' },
      { step: 3, title: 'Emerging Risk Reduction Engine Elevates Area', desc: 'Emerging Risk Engine evaluates risk velocity + unvaccinated gap + mobility, elevating AREA-07 to #1 Priority.' },
      { step: 4, title: 'Constraint & Explainability Check', desc: 'Planner flags SOFT_LOW_ACCESSIBILITY and SOFT_HIGH_MOBILITY_CORRIDOR. Recommends mobile market pop-up unit.' },
      { step: 5, title: 'Authorised Clinician Override & Approval', desc: 'Clinician Reviewer inspects explainability breakdown and approves session, logging override reason for mobile deployment.' },
      { step: 6, title: 'High-Impact Outreach Execution', desc: 'Mobile team deploys on Saturday morning at transit hub, reaching 300 vulnerable mobile vendors.' }
    ]
  };

  const activeJourneyData = selectedJourney === 'JOURNEY_A' ? journeyA : journeyB;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">
          <BookOpen style={{ color: 'var(--accent-cyan)' }} />
          Patient / Person Journey Walkthroughs
        </h1>
        <p className="page-description">
          Step-by-step operational walkthroughs illustrating how the Vaccination Outreach Planner handles routine lower-urgency outreach vs critical higher-urgency outbreak spikes.
        </p>
      </div>

      {/* Journey Selector Tabs */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem' }}>
        <button
          onClick={() => setSelectedJourney('JOURNEY_A')}
          className={`btn ${selectedJourney === 'JOURNEY_A' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ flex: 1, justifyContent: 'center' }}
        >
          <UserCheck size={18} /> Journey A — Lower Urgency (Routine)
        </button>
        <button
          onClick={() => setSelectedJourney('JOURNEY_B')}
          className={`btn ${selectedJourney === 'JOURNEY_B' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ flex: 1, justifyContent: 'center', backgroundColor: selectedJourney === 'JOURNEY_B' ? 'var(--accent-rose)' : undefined }}
        >
          <AlertTriangle size={18} /> Journey B — Higher Urgency (Emerging Spike)
        </button>
      </div>

      {/* Active Journey Content */}
      <div className="card" style={{ borderLeft: `4px solid ${selectedJourney === 'JOURNEY_B' ? 'var(--accent-rose)' : 'var(--accent-blue)'}` }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
          <h2 style={{ fontSize: '1.3rem', fontWeight: 800 }}>{activeJourneyData.title}</h2>
          <span className={`badge ${selectedJourney === 'JOURNEY_B' ? 'badge-risk' : 'badge-success'}`}>
            Target: {activeJourneyData.area}
          </span>
        </div>

        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.5 }}>
          {activeJourneyData.profile}
        </p>

        {/* Steps Timeline */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {activeJourneyData.steps.map((st) => (
            <div key={st.step} style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '1rem',
              padding: '0.85rem',
              backgroundColor: 'rgba(255, 255, 255, 0.02)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid rgba(255, 255, 255, 0.05)'
            }}>
              <div style={{
                width: 32,
                height: 32,
                borderRadius: '50%',
                backgroundColor: selectedJourney === 'JOURNEY_B' ? 'rgba(244, 63, 94, 0.2)' : 'rgba(59, 130, 246, 0.2)',
                color: selectedJourney === 'JOURNEY_B' ? 'var(--accent-rose)' : 'var(--accent-cyan)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 800,
                fontSize: '0.85rem',
                flexShrink: 0
              }}>
                {st.step}
              </div>

              <div>
                <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.2rem' }}>
                  Step {st.step}: {st.title}
                </h4>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                  {st.desc}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
