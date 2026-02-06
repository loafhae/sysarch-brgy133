import React, { useState, useEffect } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const fullName = localStorage.getItem('full_name') || "Admin";

  // State for Live Stats
  const [stats, setStats] = useState({
    residents: 0,
    announcements: 0,
    feedback: 0
  });

  // Fetch Real Data from Backend on Load
  useEffect(() => {
    const fetchStats = async () => {
      try {
        // 1. Get Users to count Residents
        const usersRes = await axios.get('http://127.0.0.1:8000/users');
        const residentCount = usersRes.data.filter(u => u.role === 'Resident').length;

        // 2. Get Announcements to count them
        const annRes = await axios.get('http://127.0.0.1:8000/announcements');
        
        // 3. Update State (Feedback is 0 for now until we add that endpoint)
        setStats({
          residents: residentCount,
          announcements: annRes.data.length,
          feedback: 0 
        });
      } catch (error) {
        console.error("Error fetching dashboard stats:", error);
      }
    };

    fetchStats();
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  // Helper to check active link
  const isActive = (path) => location.pathname === path ? "sidebar-link active" : "sidebar-link";

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="brand">Barangay 133 Admin</div>
        <nav>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            <li>
              <Link to="/dashboard" className={isActive('/dashboard')}>Dashboard</Link>
            </li>
            
            {/* --- NEW: USER MANAGEMENT LINK --- */}
            <li>
              <Link to="/users" className={isActive('/users')}>User Management</Link>
            </li>

            <li>
              <Link to="/create-announcement" className={isActive('/create-announcement')}>Post Announcement</Link>
            </li>
            <li>
              <Link to="/view-feedback" className={isActive('/view-feedback')}>View Feedback</Link>
            </li>
          </ul>
        </nav>
      </aside>
      
      {/* Main Content */}
      <div className="main-wrapper">
        
        {/* Top Bar */}
        <header className="top-bar">
          <h3>Welcome, {fullName}</h3>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </header>
        
        {/* Content Area */}
        <div className="content">
          <div className="content-inner">
            <h1 style={{marginTop: 0}}>Admin Dashboard</h1>
            
            {/* Live Stats Grid */}
            <div className="centered-grid">
              <div className="stat-card">
                <h3>Total Residents</h3>
                <p>{stats.residents}</p>
              </div>
              <div className="stat-card">
                <h3>Announcements</h3>
                <p>{stats.announcements}</p>
              </div>
              <div className="stat-card">
                <h3>Pending Feedback</h3>
                <p>{stats.feedback}</p>
              </div>
            </div>

          </div>
        </div>

        <footer className="main-footer">
          <span>&copy; 2026 Barangay 133 System</span>
        </footer>

      </div>
    </div>
  );
};

export default Dashboard;