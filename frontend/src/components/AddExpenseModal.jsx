// ./frontend/src/components/AddExpenseModal.jsx
/**
 * @file Modal form for adding a new expense.
 */
import React, { useState } from 'react';
import api from '../api';
import toast from 'react-hot-toast';

const modalOverlayStyle = {
  position: 'fixed',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  backgroundColor: 'rgba(0, 0, 0, 0.7)',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  zIndex: 1000,
};

const modalContentStyle = {
  backgroundColor: '#333',
  color: '#fff',
  padding: '20px',
  borderRadius: '8px',
  width: '90%',
  maxWidth: '500px',
};

function AddExpenseModal({ users, groupId, onClose, onExpenseAdded }) {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [payerId, setPayerId] = useState(users[0]?.id || '');
  const [participantIds, setParticipantIds] = useState(users.map(u => u.id));

  const handleParticipantChange = (userId) => {
    setParticipantIds(prev =>
      prev.includes(userId) ? prev.filter(id => id !== userId) : [...prev, userId]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!description || !amount || !payerId || participantIds.length === 0) {
      toast.error('Please fill out all fields.');
      return;
    }
    
    const payload = {
      description,
      amount: parseFloat(amount),
      payer_id: payerId,
      participant_ids: participantIds,
    };
    
    try {
      await api.post(`/groups/${groupId}/expenses`, payload);
      toast.success('Expense added!');
      onExpenseAdded();
    } catch (error) {
      toast.error('Failed to add expense.');
      console.error(error);
    }
  };

  return (
    <div style={modalOverlayStyle} onClick={onClose}>
      <div style={modalContentStyle} onClick={(e) => e.stopPropagation()}>
        <h3>Add New Expense</h3>
        <form onSubmit={handleSubmit}>
          <div>
            <input
              type="text"
              placeholder="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </div>
          <div>
            <input
              type="number"
              placeholder="Amount"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              required
              step="0.01"
            />
          </div>
          <div>
            <label>Paid by: </label>
            <select value={payerId} onChange={(e) => setPayerId(e.target.value)}>
              {users.map(user => (
                <option key={user.id} value={user.id}>{user.display_name}</option>
              ))}
            </select>
          </div>
          <div>
            <p>For whom?</p>
            {users.map(user => (
              <div key={user.id}>
                <label>
                  <input
                    type="checkbox"
                    checked={participantIds.includes(user.id)}
                    onChange={() => handleParticipantChange(user.id)}
                  />
                  {user.display_name}
                </label>
              </div>
            ))}
          </div>
          <div style={{ marginTop: '1rem' }}>
            <button type="submit">Add Expense</button>
            <button type="button" onClick={onClose} style={{ marginLeft: '1rem', backgroundColor: '#555' }}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AddExpenseModal;