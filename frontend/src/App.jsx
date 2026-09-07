import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import AreaExplorer from './pages/AreaExplorer';
import OutreachPlanner from './pages/OutreachPlanner';
import ReviewConsole from './pages/ReviewConsole';
import EvaluationPage from './pages/EvaluationPage';
import UserJourneys from './pages/UserJourneys';

export default function App() {
  const [activePage, setActivePage] = useState('dashboard');
  const [activeRole, setActiveRole] = useState('PLANNER');

  const renderPage = () => {
    switch (activePage) {
      case 'dashboard':
        return <Dashboard setActivePage={setActivePage} />;
      case 'explorer':
        return <AreaExplorer />;
      case 'planner':
        return <OutreachPlanner activeRole={activeRole} />;
      case 'reviews':
        return <ReviewConsole activeRole={activeRole} />;
      case 'eval':
        return <EvaluationPage />;
      case 'journeys':
        return <UserJourneys />;
      default:
        return <Dashboard setActivePage={setActivePage} />;
    }
  };

  return (
    <div className="app-container">
      <Navbar
        activePage={activePage}
        setActivePage={setActivePage}
        activeRole={activeRole}
        setActiveRole={setActiveRole}
      />
      <main className="main-content">
        {renderPage()}
      </main>
      <footer style={{
        borderTop: '1px solid var(--border-color)',
        padding: '1rem 2rem',
        textAlign: 'center',
        fontSize: '0.8rem',
        color: 'var(--text-muted)',
        backgroundColor: 'var(--bg-card)'
      }}>
        City Health Department • Seasonal Infectious Disease Vaccination Outreach Planner • Phase 1 Software Prototype • Synthetic Demo Data
      </footer>
    </div>
  );
}
