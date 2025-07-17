// ./frontend/src/components/ExpenseList.jsx
/**
 * @file Component to display the list of expenses in a group.
 */
import React from 'react';
import dayjs from 'dayjs';

const listStyle = {
    listStyle: 'none',
    padding: 0
};

const itemStyle = {
    border: '1px solid #444',
    borderRadius: '8px',
    padding: '1rem',
    marginBottom: '1rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
};

function ExpenseList({ expenses, onDelete }) {
  return (
    <div>
      <h3>Expense History</h3>
      {expenses.length === 0 ? (
        <p>No expenses yet. Add one!</p>
      ) : (
        <ul style={listStyle}>
          {expenses.slice().sort((a,b) => new Date(b.date) - new Date(a.date)).map(expense => (
            <li key={expense.id} style={itemStyle}>
              <div>
                <strong>{expense.description}</strong> ({expense.amount.toFixed(2)})
                <br />
                <small>Paid by {expense.payer.display_name} on {dayjs(expense.date).format('MMM D, YYYY')}</small>
                <br />
                <small>For: {expense.participants.map(p => p.user.display_name).join(', ')}</small>
              </div>
              <button onClick={() => onDelete(expense.id)} style={{backgroundColor: '#c0392b'}}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ExpenseList;

