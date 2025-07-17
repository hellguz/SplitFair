import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import useClient from '../hooks/useClient';

/**
 * Page for joining a group via an invite link.
 * @returns {JSX.Element} The rendered join group page.
 */
function JoinGroupPage() {
  const { inviteCode } = useParams();
  const navigate = useNavigate();
  const { addJoinedGroup } = useClient();

  const [group, setGroup] = useState(null);
  const [nickname, setNickname] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isMember, setIsMember] = useState(false);

  useEffect(() => {
    const fetchGroupInfo = async () => {
      try {
        const response = await api.get(`/groups/join/${inviteCode}`);
        setGroup(response.data);
        // Check if current user is already a member
        const myGroupsRes = await api.get('/groups');
        if (myGroupsRes.data.some(g => g.id === response.data.id)) {
            setIsMember(true);
        }
      } catch (err) {
        setError('Invalid invite link or group not found.');
      } finally {
        setLoading(false);
      }
    };
    fetchGroupInfo();
  }, [inviteCode]);

  const handleJoin = async (e) => {
    e.preventDefault();
    if (!nickname) {
      setError('Please enter a nickname to join.');
      return;
    }
    try {
      await api.post(`/groups/${group.id}/join`, { nickname });
      addJoinedGroup(group.id);
      navigate(`/group/${group.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to join group.');
    }
  };

  if (loading) return <div>Verifying invite...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="card">
      <h2>Join "{group.name}"</h2>
      {isMember ? (
         <div>
            <p>You are already a member of this group.</p>
            <button onClick={() => navigate(`/group/${group.id}`)}>Go to Group</button>
         </div> 
      ) : (
        <form onSubmit={handleJoin}>
            <p>Enter a nickname for this group:</p>
            <div className="form-group">
            <input
                type="text"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
                placeholder="Your Nickname"
                required
            />
            </div>
            <button type="submit" className="primary">Join Group</button>
        </form>
      )}
    </div>
  );
}

export default JoinGroupPage;

