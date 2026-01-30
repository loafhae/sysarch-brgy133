import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css'; // Make sure this file exists for your styling

const Login = () => {
  // 1. Setup state to capture what you type
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  // 2. The Login Function
  const handleLogin = async (e) => {
    e.preventDefault(); // Prevents the page from refreshing
    try {
      // Sends data to your Python backend
      const response = await axios.post('http://localhost:8000/login', {
        username: username,
        password: password
      });

      if (response.data) {
        // Save session data to browser memory
        localStorage.setItem('full_name', response.data.full_name);
        localStorage.setItem('role', response.data.role);
        
        // JUMP TO DASHBOARD - This is what stops you from being "stuck"
        navigate('/dashboard'); 
      }
    } catch (err) {
      console.error("Login Error:", err);
      alert("Invalid credentials. Please try again.");
    }
  };

  return (
    <div className="login-wrapper">
      <form onSubmit={handleLogin} className="login-card">
        <h2>Barangay 133 Admin</h2>
        <p>Secure Access Portal</p>
        
        <div className="input-group">
          <label>Username</label>
          <input 
            type="text" 
            value={username}
            onChange={(e) => setUsername(e.target.value)} 
            required 
          />
        </div>

        <div className="input-group">
          <label>Password</label>
          <input 
            type="password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
        </div>

        <button type="submit" className="login-btn">Login</button>
      </form>
    </div>
  );
};

// IMPORTANT: This line fixes the "SyntaxError: does not provide an export named default"
export default Login;