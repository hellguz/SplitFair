import React, { useState } from 'react';
import api from '../services/api';

/**
 * Form for adding a new expense to a group.
 * @param {object} props - The component props.
 * @param {number} props.groupId - The ID of the current group.
 * @param {Array<object>} props.members - List of members in the group.
 * @param {Function} props.onExpenseAdded - Callback function after an expense is added.
 * @returns {JSX.Element} The rendered expense form component.
 */
function ExpenseForm({ groupId, members, onExpenseAdded }) {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [paidByMemberId, setPaidByMemberId] = useState('');
  const [participantIds, setParticipantIds] = useState([]);
  const [error, setError] = useState('');

  const handleParticipantChange = (memberId) => {
    setParticipantIds((prev) =>
      prev.includes(memberId)
        ? prev.filter((id) => id !== memberId)
        : [...prev, memberId]
    );
  };
  
  const selectAllParticipants = () => {
    setParticipantIds(members.map(m => m.id));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!description || !amount || !paidByMemberId || participantIds.length === 0) {
      setError('Please fill all fields and select participants.');
      return;
    }
    setError('');

    try {
      const expenseData = {
        description,
        amount: parseFloat(amount),
        group_id: groupId,
        paid_by_member_id: parseInt(paidByMemberId),
        participant_member_ids: participantIds,
      };
      await api.post('/expenses', expenseData);
      onExpenseAdded();
      // Reset form
      setDescription('');
      setAmount('');
      setPaidByMemberId('');
      setParticipantIds([]);
    } catch (err) {
      setError('Failed to add expense. ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="card">
      <h3>Add New Expense</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Description</label>
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="e.g., Groceries"
            required
          />
        </div>
        <div className="form-group">
          <label>Amount</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="0.00"
            required
            step="0.01"
          />
        </div>
        <div className="form-group">
          <label>Paid by</label>
          <select value={paidByMemberId} onChange={(e) => setPaidByMemberId(e.target.value)} required>
            <option value="">Select who paid</option>
            {members.map((member) => (
              <option key={member.id} value={member.id}>{member.nickname}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>For whom?</label>
          <div>
            {members.map((member) => (
              <div key={member.id}>
                <input
                  type="checkbox"
                  id={`member-${member.id}`}
                  checked={participantIds.includes(member.id)}
                  onChange={() => handleParticipantChange(member.id)}
                />
                <label htmlFor={`member-${member.id}`} style={{ marginLeft: '8px' }}>
                  {member.nickname}
                </label>
              </div>
            ))}
             <button type="button" onClick={selectAllParticipants} style={{marginTop: '10px', fontSize: '0.8em'}}>Select All</button>
          </div>
        </div>
        {error && <p className="error">{error}</p>}
        <button type="submit" className="primary">Add Expense</button>
      </form>
    </div>
  );
}

export default ExpenseForm;

