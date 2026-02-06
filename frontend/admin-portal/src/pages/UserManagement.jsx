import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './UserManagement.css';

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [view, setView] = useState('list');
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({ username: '', role: '', password: '' });
  
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRole, setFilterRole] = useState('');

  const [showModal, setShowModal] = useState(false);
  const [modalAction, setModalAction] = useState('');
  const [selectedUserId, setSelectedUserId] = useState(null);

  // Correct Backend URL
  const API_URL = 'http://127.0.0.1:8000/users';

  const fetchUsers = async () => {
    try {
      const response = await axios.get(API_URL);
      setUsers(response.data);
    } catch (error) {
      console.error("Error loading users:", error);
    }
  };

  useEffect(() => { fetchUsers(); }, []);

  const filteredUsers = users.filter(user => {
    const matchesSearch = user.username.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterRole === '' || user.role === filterRole;
    return matchesSearch && matchesFilter;
  });

  const handleActionRequest = (action, id = null) => {
    setModalAction(action);
    setSelectedUserId(id);
    setShowModal(true);
  };

  const confirmAction = async () => {
    try {
      if (modalAction === 'ADD') {
        await axios.post(API_URL, formData);
      } else if (modalAction === 'DELETE') {
        await axios.delete(`${API_URL}/${selectedUserId}`);
      }
      
      setShowModal(false);
      setView('list');
      setFormData({ username: '', role: '', password: '' });
      fetchUsers();
    } catch (error) {
      alert(`Database error: ${error.message}`);
    }
  };

  return (
    <div className="management-page">
      {view === 'list' ? (
        <div className="table-view">
          
          {/* Header with Search and Add Button */}
          <div className="table-header">
            <div className="header-left">
              <div className="search-box">
                <span>🔍</span>
                <input 
                  type="text" 
                  placeholder="Search users..." 
                  onChange={(e) => setSearchTerm(e.target.value)} 
                />
              </div>
              
              <select className="filter-select" onChange={(e) => setFilterRole(e.target.value)}>
                <option value="">Filter by Role</option>
                <option value="Admin">Admin</option>
                <option value="Official">Official</option>
                <option value="Resident">Resident</option>
              </select>
            </div>

            <button className="add-new-btn" onClick={() => { setView('form'); setIsEditing(false); }}>
              <span>⊕</span> Add User
            </button>
          </div>
          
          {/* SCROLLABLE TABLE WRAPPER (Critical for Mobile) */}
          <div className="table-responsive">
            <table className="user-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Username</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.map((user, index) => (
                  <tr key={user.id}>
                    <td>{index + 1}</td>
                    <td>{user.username}</td>
                    <td>{user.role}</td>
                    <td><span className="status-badge">Active</span></td>
                    <td className="actions-cell">
                      {/* Delete Button (Only if not Admin) */}
                      {user.username !== 'admin' && (
                        <button className="action-icon delete" onClick={() => handleActionRequest('DELETE', user.id)}>
                          🗑️
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
                  </table>
                  </div>
                </div>
              ) : (
                /* Add User Form */
                <div className="form-card" style={{ margin: 'auto', marginTop: '20px' }}>
                  <h2>Add New User</h2>
                  <div className="form-group">
                    <label>Username</label>
                    <input type="text" placeholder="Enter username" value={formData.username} onChange={(e) => setFormData({...formData, username: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label>Role</label>
                    <select value={formData.role} onChange={(e) => setFormData({...formData, role: e.target.value})}>
                      <option value="">Select Role</option>
                      <option value="Admin">Admin</option>
                      <option value="Official">Official</option>
                      <option value="Resident">Resident</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Password</label>
                    <input type="password" placeholder="Enter password" value={formData.password} onChange={(e) => setFormData({...formData, password: e.target.value})} />
                  </div>
                  <button onClick={() => handleActionRequest('ADD')}>Add User</button>
                  <button onClick={() => { setView('list'); setFormData({ username: '', role: '', password: '' }); }}>Cancel</button>
                </div>
              )}
  
              {/* Confirmation Modal */}
              {showModal && (
                <div className="modal-overlay">
                  <div className="modal-content">
                    <h3>Confirm {modalAction}</h3>
                    <p>Are you sure you want to {modalAction.toLowerCase()}?</p>
                    <button onClick={confirmAction}>Yes</button>
                    <button onClick={() => setShowModal(false)}>No</button>
                  </div>
                </div>
              )}
            </div>
        );
      };
      
      export default UserManagement;