import React, { useState, useEffect, useContext } from 'react';
import { useParams, Link } from 'react-router-dom';
import { QRCodeSVG } from 'qrcode.react';
import api from '../api';
import { AppContext } from '../context/AppContext';
import AddExpenseForm from '../components/AddExpenseForm';
import BalanceSummary from '../components/BalanceSummary';
import ExpenseList from '../components/ExpenseList';
import './GroupPage.css';

/**
 * Displays the details of a single group, including members,
 * balances, expenses, and forms for interaction.
 */
function GroupPage() {
  const { groupId } = useParams();
  const { user } = useContext(AppContext);
  const [groupDetails, setGroupDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchGroupDetails = async () => {
    setError('');
    try {
      const response = await api.get(`/api/groups/${groupId}`);
      setGroupDetails(response.data);
    } catch (err) {
      console.error("Failed to fetch group details:", err);
      setError(err.response?.data?.detail || "Could not load group details. You may not be a member.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGroupDetails();
  }, [groupId]);

  const onExpenseAdded = () => {
    // Refetch details to show the new expense and updated balances
    fetchGroupDetails();
  };
  
  const onExpenseDeleted = () => {
    fetchGroupDetails();
  }

  if (loading) return <div className="loading">Loading Group...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!groupDetails) return null;

  return (
    <div className="group-page">
      <Link to="/" className="back-link">← Back to All Groups</Link>
      <h2>{groupDetails.name}</h2>
      
      <div className="group-main-content">
        <div className="group-column">
          <div className="container members-container">
            <h3>Members</h3>
            <ul>
              {groupDetails.members.map(member => (
                <li key={member.uuid}>{member.name} {member.uuid === user.uuid && "(You)"}</li>
              ))}
            </ul>
          </div>
          
          <div className="container invite-container">
            <h3>Invite Others</h3>
            <p>Share this code:</p>
            <code className="invite-code">{groupDetails.invite_code}</code>
            <div className="qrcode-container">
              <QRCodeSVG value={groupDetails.invite_code} bgColor="#2f2f2f" fgColor="#ffffff" />
            </div>
          </div>
          
          <div className="container">
            <h3>Add New Expense</h3>
            <AddExpenseForm
              groupId={groupId}
              members={groupDetails.members}
              onExpenseAdded={onExpenseAdded}
            />
          </div>
        </div>

        <div className="group-column">
          <div className="container">
            <h3>Balances</h3>
            <BalanceSummary balances={groupDetails.balances} members={groupDetails.members} />
          </div>
          <div className="container">
            <h3>Expense History</h3>
            <ExpenseList 
              expenses={groupDetails.expenses}
              members={groupDetails.members}
              currentUser={user}
              onExpenseDeleted={onExpenseDeleted}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default GroupPage;
