import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import CreateAnnouncement from './pages/CreateAnnouncement'; 
import UserManagement from './pages/UserManagement'; // <--- IMPORT THIS

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/create-announcement" element={<CreateAnnouncement />} />
        
        {/* ADD THIS ROUTE */}
        <Route path="/users" element={<UserManagement />} />
      </Routes>
    </Router>
  );
}

export default App;