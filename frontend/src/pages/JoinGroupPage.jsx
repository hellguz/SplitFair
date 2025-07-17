// ./frontend/src/pages/JoinGroupPage.jsx
/**
 * @file Page for joining a group via an invite link.
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useUser } from '../contexts/UserContext';
import api from '../api';
import toast from 'react-hot-toast';

function JoinGroupPage() {
  const { inviteCode } = useParams();
  const navigate = useNavigate();
  const { clientUUID, addJoinedGroup } = useUser();
  const [displayName, setDisplayName] = useState('');

  const handleJoin = async (e) => {
    e.preventDefault();
    if (!displayName.trim()) {
        toast.error("Please enter your name.");
        return;
    }
    try {
        const payload = {
            client_uuid: clientUUID,
            display_name: displayName,
        };
        const response = await api.post(`/groups/join/${inviteCode}`, payload);
        const joinedGroup = response.data;
        addJoinedGroup(joinedGroup.id);
        toast.success(`Welcome to "${joinedGroup.name}"!`);
        navigate(`/group/${joinedGroup.id}`);
    } catch (error) {
        toast.error('Failed to join group. The invite code may be invalid.');
        console.error(error);
    }
  };

  return (
    <div>
      <h2>Join Group</h2>
      <p>You've been invited to join a group! Please enter your name to continue.</p>
      <form onSubmit={handleJoin}>
        <input
          type="text"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          placeholder="Your Name for this Group"
          required
        />
        <button type="submit">Join Group</button>
      </form>
    </div>
  );
}

export default JoinGroupPage;


