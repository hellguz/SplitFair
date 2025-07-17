import React, { useState, useContext } from 'react';
import api from '../api';
import { AppContext } from '../context/AppContext';
import './AddExpenseForm.css';

/**
 * A form for adding a new expense to a group. It allows selecting
 * who paid and who participated in the expense.
 */
function AddExpenseForm({ groupId, members, onExpenseAdded }) {
  const { user } = useContext(AppContext);
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [participants, setParticipants] = useState([]);
  const [error, setError] = useState('');

  // Pre-select all members by default when the component loads or members change
  React.useEffect(() => {
    setParticipants(members.map(m => m.uuid));
  }, [members]);

  const handleParticipantChange = (e) => {
    const { value, checked } = e.target;
    if (checked) {
      setParticipants(prev => [...prev, value]);
    } else {
      setParticipants(prev => prev.filter(p => p !== value));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!description.trim() || !amount || parseFloat(amount) <= 0 || participants.length === 0) {
      setError('Please fill all fields correctly. At least one participant must be selected.');
      return;
    }

    const expenseData = {
      description,
      amount: parseFloat(amount),
      payer_uuid: user.uuid,
      participant_uuids: participants,
    };

    try {
      await api.post(`/api/groups/${groupId}/expenses`, expenseData);
      // Reset form
      setDescription('');
      setAmount('');
      setParticipants(members.map(m => m.uuid));
      onExpenseAdded(); // Notify parent component
    } catch (err) {
      console.error('Failed to add expense:', err);
      setError(err.response?.data?.detail || 'Failed to add expense.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="add-expense-form">
      <input
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Expense Description (e.g., Groceries)"
        required
      />
      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        placeholder="Amount"
        min="0.01"
        step="0.01"
        required
      />
      <div className="participants-selector">
        <p>Split between:</p>
        <div className="checkbox-group">
            {members.map(member => (
              <label key={member.uuid}>
                <input
                  type="checkbox"
                  value={member.uuid}
                  checked={participants.includes(member.uuid)}
                  onChange={handleParticipantChange}
                />
                {member.name}
              </label>
            ))}
        </div>
      </div>
      {error && <p className="error">{error}</p>}
      <button type="submit">Add Expense</button>
    </form>
  );
}

export default AddExpenseForm;
