// ./frontend/src/components/Balances.jsx
/**
 * @file Component to calculate and display user balances.
 */
import React from 'react';

function Balances({ users, expenses }) {
  /**
   * Calculates the final balance for each user.
   * @returns {Array<{user: object, balance: number}>} An array of objects with user info and their balance.
   */
  const calculateBalances = () => {
    const balances = users.map(user => ({ user, balance: 0 }));

    expenses.forEach(expense => {
      const payer = balances.find(b => b.user.id === expense.payer.id);
      const numParticipants = expense.participants.length;
      if (numParticipants === 0) return;

      const share = expense.amount / numParticipants;

      // Add to the payer's balance
      if(payer) {
        payer.balance += expense.amount;
      }

      // Subtract from each participant's balance
      expense.participants.forEach(p => {
        const participant = balances.find(b => b.user.id === p.user.id);
        if (participant) {
          participant.balance -= share;
        }
      });
    });

    return balances;
  };

  const balances = calculateBalances();

  return (
    <div>
      <h3>Balances</h3>
      <ul style={{listStyle: 'none', padding: 0}}>
        {balances.map(({ user, balance }) => (
          <li key={user.id} style={{ color: balance >= 0 ? 'green' : 'red' }}>
            {user.display_name}: {balance.toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Balances;


