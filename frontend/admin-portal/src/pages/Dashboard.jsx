import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
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
        <div className="brand">Barangay 133 Admin</div>
        <nav>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            {/* Using className="sidebar-link" to match CSS */}
            <li>
              <Link to="/dashboard" className="sidebar-link active">Dashboard</Link>
            </li>
            <li>
              <Link to="/create-announcement" className="sidebar-link">Post Announcement</Link>
            </li>
            <li>
              <Link to="/view-feedback" className="sidebar-link">View Feedback</Link>
            </li>
          </ul>
        </nav>
      </aside>
      
      {/* Main Wrapper (Required by your CSS) */}
      <div className="main-wrapper">
        
        {/* Top Bar */}
        <header className="top-bar">
          <h3>Welcome, {fullName}</h3>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </header>
        
        {/* Content Area */}
        <div className="content">
          
          {/* Inner White Panel */}
          <div className="content-inner">
            <h1 style={{marginTop: 0}}>Admin Dashboard</h1>
            
            {/* Stats Grid */}
            <div className="centered-grid">
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

        </div>

        {/* Footer (Required by your CSS) */}
        <footer className="main-footer">
          <span>&copy; 2023 Barangay 133 System</span>
        </footer>

      </div>
    </div>
  );
};

export default Dashboard;