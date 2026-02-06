import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './CreateAnnouncement.css';

const CreateAnnouncement = () => {
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const userId = localStorage.getItem('user_id');

    if (!userId) {
      alert("You must be logged in to post.");
      return;
    }

    try {
      await axios.post('http://127.0.0.1:8000/announcements', {
        title: title,
        body: body,
        created_by: parseInt(userId)
      });

      alert('Announcement Posted Successfully!');
      navigate('/dashboard');
    } catch (error) {
      console.error("Error posting announcement:", error);
      alert('Failed to post announcement.');
    }
  };

  return (
    <div className="announcement-page">
      <div className="form-card">
        <h2>Post New Announcement</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Title</label>
            <input 
              type="text" 
              value={title} 
              onChange={(e) => setTitle(e.target.value)} 
              placeholder="Enter title..." 
              required 
            />
          </div>
          
          <div className="form-group">
            <label>Content</label>
            <textarea 
              value={body} 
              onChange={(e) => setBody(e.target.value)} 
              placeholder="Write your announcement here..." 
              rows="6"
              required 
            />
          </div>

          <div className="form-buttons">
            <button type="submit" className="save-btn">Post Announcement</button>
            <button type="button" className="cancel-btn" onClick={() => navigate('/dashboard')}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateAnnouncement;