import React from 'react';
import { Link, NavLink, Outlet, useNavigate, useLocation } from 'react-router-dom'; // Add Link here!
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const fullName = localStorage.getItem('full_name') || "John Doe";

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const isDashboardHome = location.pathname === '/dashboard';

  return (
    <div className="dashboard-container">
      {/* LEFT SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-logo">☒</div>
          <h2>BARANGAY 133</h2>
        </div>
        <nav className="sidebar-nav">
          <ul>
            <li>
              <NavLink to="/dashboard" end className={({ isActive }) => isActive ? 'sidebar-link active' : 'sidebar-link'}>
                Dashboard
              </NavLink>
            </li>
            <li>
              <NavLink to="/dashboard/users" className={({ isActive }) => isActive ? 'sidebar-link active' : 'sidebar-link'}>
                User Management
              </NavLink>
            </li>
            <li className="sidebar-link-placeholder">Residents Record</li>
            <li className="sidebar-link-placeholder">Feedback</li>
            <li className="sidebar-link-placeholder">System Settings</li>
          </ul>
        </nav>
        <div className="sidebar-footer">
          <button onClick={handleLogout} className="logout-btn-red">Logout</button>
        </div>
      </aside>

      {/* RIGHT SIDE WRAPPER */}
      <div className="main-wrapper">
        <header className="top-bar">
          <div className="user-info">
            <span className="user-icon">👤</span>
            <span className="welcome-text">Welcome! {fullName}</span>
          </div>
          <div className="header-icons">

          </div>
        </header>

        <main className="content" role="main">
          <div className="content-inner" aria-live="polite">
            {isDashboardHome ? (
              <div className="centered-grid" role="region" aria-label="Dashboard statistics">
                <div className="stat-card">
                  <span className="card-label">Number Of Users</span>
                  <span className="card-value">970</span>
                </div>
                <div className="stat-card">
                  <span className="card-label">Number Of Residents</span>
                  <span className="card-value">5,000</span>
                </div>
                <div className="stat-card full-width">
                  <span className="card-label">Pending Feedback</span>
                  <span className="card-value">200</span>
                </div>
              </div>
            ) : (
              <div className="outlet-container">
                <Outlet />
              </div>
            )}
          </div>
        </main>

        <footer className="main-footer">

        </footer>
      </div>
    </div>
  );
};

export default Dashboard;