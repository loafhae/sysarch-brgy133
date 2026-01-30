import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await axios.post('http://127.0.0.1:8000/login', {
        username: username,
        password: password,
      });

      const data = response.data;
      localStorage.setItem('user_id', data.user_id);
      localStorage.setItem('role', data.role);
      localStorage.setItem('full_name', data.full_name);

      alert(`Welcome, ${data.full_name}!`);
      navigate('/dashboard');

    } catch (err) {
      setError('Invalid username or password');
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo-placeholder">
          133
        </div>
        <h2>Barangay 133 Admin</h2>
        <p className="subtitle">Secure Access Portal</p>

        {error && <p className="error">{error}</p>}

        <form onSubmit={handleLogin}>
          <div>
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
};

export default Login;