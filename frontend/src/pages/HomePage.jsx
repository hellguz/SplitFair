import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';
import useClient from '../hooks/useClient';

/**
 * The home page, displaying a list of joined groups and a form to create a new one.
 * @returns {JSX.Element} The rendered home page.
 */
function HomePage() {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const { clientId } = useClient();
  const navigate = useNavigate();

  // Form state
  const [groupName, setGroupName] = useState('');
  const [nickname, setNickname] = useState('');
  const [error, setError] = useState('');

  const fetchGroups = async () => {
    if (!clientId) return;
    try {
      setLoading(true);
      const response = await api.get('/groups');
      setGroups(response.data);
    } catch (err) {
      console.error('Failed to fetch groups', err);
      setError('Could not load your groups.');
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    fetchGroups();
  }, [clientId]);

  const handleCreateGroup = async (e) => {
    e.preventDefault();
    if (!groupName || !nickname) {
      setError('Please provide a group name and your nickname.');
      return;
    }
    try {
      const response = await api.post('/groups', {
        name: groupName,
        creator_nickname: nickname,
      });
      navigate(`/group/${response.data.id}`);
    } catch (err) {
      setError('Failed to create group.');
      console.error(err);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="card">
        <h3>Create a New Group</h3>
        <form onSubmit={handleCreateGroup}>
          <div className="form-group">
            <label htmlFor="groupName">Group Name</label>
            <input
              id="groupName"
              type="text"
              value={groupName}
              onChange={(e) => setGroupName(e.target.value)}
              placeholder="e.g., Vacation Trip"
            />
          </div>
          <div className="form-group">
            <label htmlFor="nickname">Your Nickname</label>
            <input
              id="nickname"
              type="text"
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
              placeholder="e.g., Alex"
            />
          </div>
          {error && <p className="error">{error}</p>}
          <button type="submit" className="primary">Create Group</button>
        </form>
      </div>

      <div className="card">
        <h3>Your Groups</h3>
        {loading ? (
          <p>Loading groups...</p>
        ) : groups.length > 0 ? (
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {groups.map((group) => (
              <li key={group.id}>
                <Link to={`/group/${group.id}`} style={{ textDecoration: 'none' }}>
                  <div className="card" style={{padding: '1rem'}}>
                    {group.name}
                  </div>
                </Link>
              </li>
            ))}
          </ul>
        ) : (
          <p>You haven't joined any groups yet. Create one above!</p>
        )}
      </div>
    </div>
  );
}

export default HomePage;

