import React from 'react';
import api from '../services/api';

/**
 * Displays a list of expenses for a group.
 * @param {object} props - The component props.
 * @param {Array<object>} props.expenses - List of expenses to display.
 * @param {Function} props.onExpenseDeleted - Callback after an expense is deleted.
 * @returns {JSX.Element} The rendered expense list component.
 */
function ExpenseList({ expenses, onExpenseDeleted }) {
  const handleDelete = async (expenseId) => {
    if (window.confirm('Are you sure you want to delete this expense?')) {
      try {
        await api.delete(`/expenses/${expenseId}`);
        onExpenseDeleted();
      } catch (err) {
        console.error('Failed to delete expense', err);
        alert('Failed to delete expense.');
      }
    }
  };

  return (
    <div className="card">
      <h3>Expense History</h3>
      {expenses.length === 0 ? (
        <p>No expenses yet. Add one above!</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {expenses.map((expense) => (
            <li key={expense.id} style={{ borderBottom: '1px solid #444', padding: '1rem 0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong>{expense.description}</strong>
                <div style={{ fontSize: '0.9em', opacity: 0.8 }}>
                  Paid by {expense.payer.nickname} on {new Date(expense.date).toLocaleDateString()}
                </div>
                <div style={{ fontSize: '1.2em', fontWeight: 'bold' }}>
                  ${expense.amount.toFixed(2)}
                </div>
              </div>
              <button onClick={() => handleDelete(expense.id)} style={{backgroundColor: '#5e2a2a'}}>
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ExpenseList;

