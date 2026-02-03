import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import CreateAnnouncement from './pages/CreateAnnouncement'; // Import the page

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        
        {/* THIS IS THE MISSING LINK */}
        <Route path="/create-announcement" element={<CreateAnnouncement />} />
      </Routes>
    </Router>
  );
}

export default App;