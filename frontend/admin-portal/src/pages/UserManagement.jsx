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
      } else if (modalAction === 'SAVE') {
        await axios.put(`${API_URL}/${selectedUserId}`, formData);
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
                <option value="">Filter by</option>
                <option value="Admin">Admin</option>
                <option value="Official">Official</option>
                <option value="Resident">Resident</option>
              </select>
            </div>

            <button className="add-new-btn" onClick={() => { setView('form'); setIsEditing(false); }}>
              <span>⊕</span> Add New User
            </button>
          </div>
          
          <table className="user-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Username</th>
                <th className="spacer-col"></th> {/* Empty Column Header */}
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
                  <td className="spacer-col"></td> {/* Empty Column Cell */}
                  <td>{user.role}</td>
                  <td><span className={`status-badge ${user.status === 'Inactive' ? 'inactive' : 'active'}`}>
                    {user.status || 'Active'}
                  </span></td>
                  <td className="actions-cell">
                    <button className="action-icon edit" onClick={() => { setView('form'); setIsEditing(true); setFormData(user); setSelectedUserId(user.id); }}>✏️</button>
                    <button className="action-icon delete" onClick={() => handleActionRequest('DELETE', user.id)}>🗑️</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="form-card">
          <h2>{isEditing ? 'Edit User' : 'Add New User'}</h2>
          <div className="form-group">
            <input type="text" placeholder="Username" value={formData.username} 
                   onChange={(e) => setFormData({...formData, username: e.target.value})} />
            
            <select value={formData.role} onChange={(e) => setFormData({...formData, role: e.target.value})}>
              <option value="">Select Role</option>
              <option value="Admin">Admin</option>
              <option value="Official">Official</option>
              <option value="Resident">Resident</option>
            </select>

            <input type="password" placeholder="Password" 
                   onChange={(e) => setFormData({...formData, password: e.target.value})} />
          </div>

          <div className="form-buttons">
            <button className="save-btn" onClick={() => handleActionRequest(isEditing ? 'SAVE' : 'ADD')}>
              {isEditing ? 'Save Changes' : 'Confirm Add'}
            </button>
            <button onClick={() => setView('list')} className="cancel-btn">Cancel</button>
          </div>
        </div>
      )}

      {showModal && (
        <div className="modal-overlay">
          <div className="modal-box">
            <h3>Are you sure you want to {modalAction} this user?</h3>
            <div className="modal-actions">
              <button className="yes-btn" onClick={confirmAction}>YES</button>
              <button className="no-btn" onClick={() => setShowModal(false)}>NO</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserManagement;