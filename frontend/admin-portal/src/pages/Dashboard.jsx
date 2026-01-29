import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const fullName = localStorage.getItem('full_name') || "Admin";

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="brand">Barangay Admin</div>
        <nav>
          <ul>
            <li className="active">Dashboard</li>
            <li onClick={() => alert('Announcements Page coming soon')}>Post Announcement</li>
            <li onClick={() => alert('Feedback Page coming soon')}>View Feedback</li>
          </ul>
        </nav>
      </aside>
      
      {/* Main Content */}
      <main className="main-content">
        <header className="top-bar">
          <h3>Welcome, {fullName}</h3>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </header>
        
        <div className="content">
          <h1>Admin Dashboard</h1>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Residents</h3>
              <p>0</p>
            </div>
            <div className="stat-card">
              <h3>Announcements</h3>
              <p>0</p>
            </div>
            <div className="stat-card">
              <h3>Pending Feedback</h3>
              <p>0</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;