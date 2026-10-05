import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import AreaExplorer from './pages/AreaExplorer';
import OutreachPlanner from './pages/OutreachPlanner';
import ReviewConsole from './pages/ReviewConsole';
import EvaluationPage from './pages/EvaluationPage';
import UserJourneys from './pages/UserJourneys';
import { loginUser, getStoredUser, getAuthToken } from './services/api';

export default function App() {
  const [activePage, setActivePage] = useState('dashboard');
  const [currentUser, setCurrentUser] = useState(getStoredUser());
  const [authError, setAuthError] = useState(null);

  // Initialize auth token on startup
  useEffect(() => {
    const initAuth = async () => {
      try {
        if (!getAuthToken() || !currentUser) {
          const res = await loginUser('clinician', 'ClinicianPass123!');
          setCurrentUser({
            user_id: res.user_id,
            username: res.username,
            role: res.role,
            full_name: res.full_name
          });
        }
      } catch (err) {
        console.error("Auth init warning:", err);
        setAuthError(err.message);
      }
    };
    initAuth();
  }, []);

  const handleSwitchUser = async (targetRole) => {
    try {
      setAuthError(null);
      let res;
      if (targetRole === 'ADMIN') {
        res = await loginUser('admin', 'AdminPass123!');
      } else {
        res = await loginUser('clinician', 'ClinicianPass123!');
      }
      setCurrentUser({
        user_id: res.user_id,
        username: res.username,
        role: res.role,
        full_name: res.full_name
      });
    } catch (err) {
      console.error("Switch role failed:", err);
      setAuthError(`Role switch failed: ${err.message}`);
    }
  };

  const activeRole = currentUser?.role || 'CLINICIAN';

  const renderPage = () => {
    switch (activePage) {
      case 'dashboard':
        return <Dashboard setActivePage={setActivePage} />;
      case 'explorer':
        return <AreaExplorer />;
      case 'planner':
        return <OutreachPlanner activeRole={activeRole} currentUser={currentUser} />;
      case 'reviews':
        return <ReviewConsole activeRole={activeRole} currentUser={currentUser} />;
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
        activeUser={currentUser}
        onSwitchUser={handleSwitchUser}
      />
      
      {authError && (
        <div style={{
          backgroundColor: 'rgba(244, 63, 94, 0.15)',
          borderBottom: '1px solid rgba(244, 63, 94, 0.3)',
          color: 'var(--accent-rose)',
          padding: '0.5rem 2rem',
          fontSize: '0.8rem',
          textAlign: 'center'
        }}>
          {authError}
        </div>
      )}

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
        City Health Department • Seasonal Infectious Disease Vaccination Outreach Planner • Final Production Implementation • Authenticated User: {currentUser?.full_name || 'Clinician'} ({activeRole})
      </footer>
    </div>
  );
}
