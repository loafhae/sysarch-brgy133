import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import UserManagement from './pages/UserManagement';

function App() {
  return (
    <Router>
      <Routes>
        {/* Redirect empty path to login */}
        <Route path="/" element={<Navigate to="/login" replace />} />      
        
        {/* Independent Login Page */}
        <Route path="/login" element={<Login />} />
        
        {/* Dashboard Parent: It MUST stay open to show the sidebar */}
        <Route path="/dashboard" element={<Dashboard />}>
          {/* UserManagement Child: This loads inside the Dashboard's Outlet */}
          <Route path="users" element={<UserManagement />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;