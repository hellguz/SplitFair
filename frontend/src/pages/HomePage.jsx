// ./frontend/src/pages/HomePage.jsx
/**
 * @file The home page, displaying a list of joined groups and a form to create a new one.
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../contexts/UserContext';
import api from '../api';
import toast from 'react-hot-toast';

function HomePage() {
  const [groups, setGroups] = useState([]);
  const [newGroupName, setNewGroupName] = useState('');
  const [userName, setUserName] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const { clientUUID, addJoinedGroup } = useUser();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchGroups = async () => {
      if (!clientUUID) return;
      try {
        setIsLoading(true);
        const response = await api.get('/groups', { params: { client_uuid: clientUUID } });
        setGroups(response.data);
      } catch (error) {
        toast.error('Failed to fetch your groups.');
        console.error(error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchGroups();
  }, [clientUUID]);

  const handleCreateGroup = async (e) => {
    e.preventDefault();
    if (!newGroupName.trim() || !userName.trim()) {
        toast.error("Group name and your name are required.");
        return;
    }
    try {
        const payload = {
            name: newGroupName,
            client_uuid: clientUUID,
            user_display_name: userName,
        };
        const response = await api.post('/groups', payload);
        const newGroup = response.data;
        addJoinedGroup(newGroup.id);
        toast.success(`Group "${newGroup.name}" created!`);
        navigate(`/group/${newGroup.id}`);
    } catch (error) {
        toast.error('Failed to create group.');
        console.error(error);
    }
  };

  return (
    <div>
      <h2>My Groups</h2>
      {isLoading ? (
        <p>Loading groups...</p>
      ) : groups.length > 0 ? (
        <ul>
          {groups.map((group) => (
            <li key={group.id} onClick={() => navigate(`/group/${group.id}`)} style={{cursor: 'pointer'}}>
              {group.name}
            </li>
          ))}
        </ul>
      ) : (
        <p>You haven't joined any groups yet. Create one below!</p>
      )}

      <hr style={{margin: '2rem 0'}}/>

      <h2>Create a New Group</h2>
      <form onSubmit={handleCreateGroup}>
        <div>
          <input
            type="text"
            value={newGroupName}
            onChange={(e) => setNewGroupName(e.target.value)}
            placeholder="Group Name (e.g., Vacation Trip)"
            required
          />
        </div>
        <div>
          <input
            type="text"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
            placeholder="Your Name"
            required
          />
        </div>
        <button type="submit">Create Group</button>
      </form>
    </div>
  );
}

export default HomePage;

