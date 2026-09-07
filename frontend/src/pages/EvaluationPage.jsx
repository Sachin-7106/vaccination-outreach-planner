import React, { useEffect, useState } from 'react';
import { BarChart3, TrendingUp, AlertOctagon } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';
import ErrorAnalysisWidget from '../components/ErrorAnalysisWidget';
import { fetchEvaluationMetrics, fetchErrorAnalysis } from '../services/api';

export default function EvaluationPage() {
  const [evalMetrics, setEvalMetrics] = useState([]);
  const [errorScenarios, setErrorScenarios] = useState([]);
  const [activeTab, setActiveTab] = useState('METRICS'); // METRICS vs ERROR_ANALYSIS
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadEval() {
      try {
        const [metricsData, errorsData] = await Promise.all([
          fetchEvaluationMetrics(5, 300, 12.0),
          fetchErrorAnalysis()
        ]);
        setEvalMetrics(metricsData);
        setErrorScenarios(errorsData);
      } catch (err) {
        console.error('Error fetching evaluation data:', err);
      } finally {
        setLoading(false);
      }
    }
    loadEval();
  }, []);

  const chartData = evalMetrics.map(m => ({
    name: m.objective === 'HISTORICAL_BASELINE' ? 'Historical Baseline' :
          m.objective === 'MAX_REACH' ? 'Max Eligible Reach' : 'Emerging Risk Reduction',
    'Eligible Reached per Session': m.eligible_reached_per_session,
    'Session Utilisation %': m.session_utilisation_rate,
    'Risk Weighted Coverage Score': Math.round(m.risk_weighted_coverage_score * 100)
  }));

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">
          <BarChart3 style={{ color: 'var(--accent-purple)' }} />
          Comparative Evaluation & Algorithmic Error Analysis
        </h1>
        <p className="page-description">
          Quantitative benchmarking of the proposed Emerging Risk Reduction Planner against historical average baselines, alongside explicit failure mode analysis.
        </p>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
        <button
          onClick={() => setActiveTab('METRICS')}
          className={`btn ${activeTab === 'METRICS' ? 'btn-primary' : 'btn-secondary'}`}
        >
          <TrendingUp size={16} /> Quantitative Metrics
        </button>
        <button
          onClick={() => setActiveTab('ERROR_ANALYSIS')}
          className={`btn ${activeTab === 'ERROR_ANALYSIS' ? 'btn-primary' : 'btn-secondary'}`}
        >
          <AlertOctagon size={16} /> Error & Failure Mode Analysis
        </button>
      </div>

      {activeTab === 'METRICS' ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Main Chart */}
          <div className="card">
            <div className="card-title">
              <span>Primary Metric: Eligible People Reached per Outreach Session</span>
              <span className="badge badge-success">Simulated Benchmark</span>
            </div>

            <div style={{ height: 320, width: '100%', marginTop: '1rem' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#233154" />
                  <XAxis dataKey="name" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip contentStyle={{ backgroundColor: '#131b2e', borderColor: '#233154', color: '#f8fafc' }} />
                  <Legend />
                  <Bar dataKey="Eligible Reached per Session" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="Session Utilisation %" fill="#10b981" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Detailed Metrics Table */}
          <div className="card">
            <div className="card-title">
              <span>Full Comparative Performance Table</span>
            </div>

            <div className="data-table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Planning Model Objective</th>
                    <th>Reached / Session</th>
                    <th>Total Reached</th>
                    <th>Capacity Utilisation</th>
                    <th>Risk-Weighted Coverage</th>
                    <th>Travel Feasibility</th>
                  </tr>
                </thead>
                <tbody>
                  {evalMetrics.map(m => (
                    <tr key={m.objective}>
                      <td style={{ fontWeight: 700 }}>
                        {m.objective === 'HISTORICAL_BASELINE' ? 'Historical Baseline' :
                         m.objective === 'MAX_REACH' ? 'Objective A — Maximum Eligible Reach' : 'Objective B — Emerging Risk Reduction'}
                      </td>
                      <td style={{ fontWeight: 800, color: 'var(--accent-cyan)' }}>{m.eligible_reached_per_session}</td>
                      <td>{m.total_eligible_reached.toLocaleString()}</td>
                      <td>{m.session_utilisation_rate}%</td>
                      <td style={{ fontWeight: 700, color: m.risk_weighted_coverage_score > 0.7 ? 'var(--accent-emerald)' : 'var(--text-primary)' }}>
                        {m.risk_weighted_coverage_score}
                      </td>
                      <td>{m.travel_feasibility_rate}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : (
        <ErrorAnalysisWidget scenarios={errorScenarios} />
      )}
    </div>
  );
}
