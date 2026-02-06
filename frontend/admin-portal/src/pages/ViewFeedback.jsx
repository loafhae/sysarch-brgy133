import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './Dashboard.css';

const ViewFeedback = () => {
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/feedback').then(res => { setFeedbacks(res.data); setLoading(false); }).catch(err => setLoading(false));
  }, []);

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <div className="brand">Barangay Admin</div>
        <nav><ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            <li><Link to="/dashboard" className="sidebar-link">Dashboard</Link></li>
            <li><Link to="/create-announcement" className="sidebar-link">Post Announcement</Link></li>
            <li><Link to="/view-feedback" className="sidebar-link active">View Feedback</Link></li>
          </ul></nav>
      </aside>
      <div className="main-wrapper">
        <header className="top-bar"><h3>Resident Feedback</h3></header>
        <div className="content">
          <div className="content-inner">
            <h2 style={{marginTop: 0}}>Incoming Messages</h2>
            {loading ? <p>Loading...</p> : feedbacks.length === 0 ? <p>No feedback yet.</p> :
              <div style={{overflowX: 'auto'}}>
                <table style={{width: '100%', borderCollapse: 'collapse', border: '1px solid #333'}}>
                  <thead><tr style={{backgroundColor: '#333', color: '#fff'}}><th style={{padding: '12px', border: '1px solid #333'}}>Date</th><th style={{padding: '12px', border: '1px solid #333'}}>Resident</th><th style={{padding: '12px', border: '1px solid #333'}}>Message</th></tr></thead>
                  <tbody>
                    {feedbacks.map((fb) => (
                      <tr key={fb.id}><td style={{padding: '12px', border: '1px solid #ddd'}}>{fb.date}</td><td style={{padding: '12px', border: '1px solid #ddd', fontWeight: 'bold'}}>{fb.name}</td><td style={{padding: '12px', border: '1px solid #ddd'}}>{fb.message}</td></tr>
                    ))}
                  </tbody>
                </table>
              </div>
            }
          </div>
        </div>
      </div>
    </div>
  );
};
export default ViewFeedback;