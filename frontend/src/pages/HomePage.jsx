import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AppContext } from '../context/AppContext';
import api from '../api';
import './HomePage.css';

/**
 * The main landing page. Displays the user's groups and forms
 * for creating a new group or joining an existing one.
 */
function HomePage() {
  const { user, groups, refreshGroups } = useContext(AppContext);
  const [newGroupName, setNewGroupName] = useState('');
  const [joinCode, setJoinCode] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleCreateGroup = async (e) => {
    e.preventDefault();
    if (!newGroupName.trim()) {
      setError('Group name cannot be empty.');
      return;
    }
    setError('');
    try {
      await api.post('/api/groups', { name: newGroupName });
      setNewGroupName('');
      refreshGroups(); // Refresh the list of groups
    } catch (err) {
      console.error('Failed to create group:', err);
      setError(err.response?.data?.detail || 'Failed to create group.');
    }
  };

  const handleJoinGroup = async (e) => {
    e.preventDefault();
    if (!joinCode.trim()) {
      setError('Invite code cannot be empty.');
      return;
    }
    setError('');
    try {
      const response = await api.post('/api/groups/join', { invite_code: joinCode });
      setJoinCode('');
      refreshGroups();
      navigate(`/group/${response.data.id}`); // Navigate to the newly joined group
    } catch (err) {
      console.error('Failed to join group:', err);
      setError(err.response?.data?.detail || 'Failed to join group. Check the code.');
    }
  };

  return (
    <div className="homepage">
      <h2>Welcome, {user?.name}!</h2>
      <p>Your unique ID: <code>{user?.uuid}</code></p>
      
      <div className="form-container">
        <form onSubmit={handleCreateGroup} className="group-form">
          <h3>Create a New Group</h3>
          <input
            type="text"
            value={newGroupName}
            onChange={(e) => setNewGroupName(e.target.value)}
            placeholder="New Group Name"
          />
          <button type="submit">Create</button>
        </form>
        
        <form onSubmit={handleJoinGroup} className="group-form">
          <h3>Join a Group</h3>
          <input
            type="text"
            value={joinCode}
            onChange={(e) => setJoinCode(e.target.value)}
            placeholder="Enter Invite Code"
          />
          <button type="submit">Join</button>
        </form>
      </div>

      {error && <p className="error">{error}</p>}

      <div className="group-list-container">
        <h3>Your Groups</h3>
        {groups.length > 0 ? (
          <ul className="group-list">
            {groups.map(group => (
              <li key={group.id} className="group-list-item">
                <Link to={`/group/${group.id}`}>{group.name}</Link>
              </li>
            ))}
          </ul>
        ) : (
          <p>You are not a member of any groups yet. Create one or join one!</p>
        )}
      </div>
    </div>
  );
}

export default HomePage;
