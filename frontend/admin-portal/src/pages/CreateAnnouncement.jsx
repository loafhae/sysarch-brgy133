import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom'; // I added Link here
import './CreateAnnouncement.css';

const CreateAnnouncement = () => {
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const user_id = localStorage.getItem('user_id');

    // Check if user is logged in
    if (!user_id) {
      alert('You are not logged in. Please login again.');
      navigate('/login');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/announcements', {
        title: title,
        body: body,
        created_by: parseInt(user_id)
      });

      alert('Announcement Posted!');
      navigate('/dashboard');

    } catch (err) {
      console.error(err);
      alert('Failed to post announcement');
    }
  };

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <div className="brand">Barangay Admin</div>
        <nav>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            <li>
              <Link to="/dashboard" className="sidebar-link">Dashboard</Link>
            </li>
            <li>
              {/* Active State for visual feedback */}
              <Link to="/create-announcement" className="sidebar-link active">Post Announcement</Link>
            </li>
          </ul>
        </nav>
      </aside>
      
      <div className="main-wrapper">
        <header className="top-bar">
          <h3>Create Announcement</h3>
        </header>
        
        <div className="content">
          <div className="content-inner">
            <h2 style={{marginTop: 0}}>Post New Announcement</h2>
            <form onSubmit={handleSubmit}>
              
              <div style={{marginBottom: '20px'}}>
                <label style={{display:'block', marginBottom:'8px', fontWeight:'bold'}}>Title</label>
                <input 
                  type="text" 
                  style={{width: '100%', padding: '12px', border: '1px solid #ccc', borderRadius: '4px', boxSizing: 'border-box'}}
                  value={title} 
                  onChange={(e) => setTitle(e.target.value)} 
                  placeholder="e.g. Typhoon Warning"
                  required 
                />
              </div>
              
              <div style={{marginBottom: '20px'}}>
                <label style={{display:'block', marginBottom:'8px', fontWeight:'bold'}}>Message</label>
                <textarea 
                  style={{width: '100%', padding: '12px', border: '1px solid #ccc', borderRadius: '4px', boxSizing: 'border-box', height: '150px'}}
                  value={body} 
                  onChange={(e) => setBody(e.target.value)} 
                  placeholder="Type the details here..."
                  required
                />
              </div>

              <button type="submit" style={{
                padding: '12px 24px', 
                background: '#a83a3f', 
                color: 'white', 
                border: 'none', 
                borderRadius: '6px', 
                cursor: 'pointer', 
                fontWeight: 'bold',
                fontSize: '1rem'
              }}>
                Publish Announcement
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateAnnouncement;