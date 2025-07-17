import React from 'react';
import api from '../api';
import './ExpenseList.css';

/**
 * Renders the list of past expenses for a group.
 * Allows the payer of an expense to delete it.
 */
function ExpenseList({ expenses, members, currentUser, onExpenseDeleted }) {

  if (!expenses || expenses.length === 0) {
    return <p>No expenses recorded in this group yet.</p>;
  }

  const getMemberName = (id) => {
    return members.find(m => m.id === id)?.name || 'Unknown';
  };
  
  const handleDelete = async (expenseId) => {
      if (window.confirm("Are you sure you want to delete this expense?")) {
          try {
              await api.delete(`/api/expenses/${expenseId}`);
              onExpenseDeleted();
          } catch (err) {
              console.error("Failed to delete expense", err);
              alert(err.response?.data?.detail || "Could not delete expense.");
          }
      }
  }

  return (
    <ul className="expense-list">
      {expenses.map(expense => (
        <li key={expense.id} className="expense-item">
          <div className="expense-details">
            <span className="expense-date">{new Date(expense.created_at).toLocaleDateString()}</span>
            <span className="expense-desc">{expense.description}</span>
          </div>
          <div className="expense-info">
            <span>{getMemberName(expense.payer_id)} paid <strong>${expense.amount.toFixed(2)}</strong></span>
            {currentUser.id === expense.payer_id && (
                <button className="delete-btn" onClick={() => handleDelete(expense.id)}>×</button>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
}

export default ExpenseList;
