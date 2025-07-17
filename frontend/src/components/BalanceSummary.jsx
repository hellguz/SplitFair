import React from 'react';
import './BalanceSummary.css';

/**
 * Displays the calculated balances for each member of the group,
 * indicating who is settled, who owes money, and who is owed money.
 */
function BalanceSummary({ balances, members }) {
  if (!balances || balances.length === 0) {
    return <p>No balances to show yet. Add an expense to get started!</p>;
  }

  const getMemberName = (uuid) => {
    return members.find(m => m.uuid === uuid)?.name || 'Unknown User';
  };

  return (
    <ul className="balance-summary-list">
      {balances.map(({ user_uuid, balance }) => (
        <li key={user_uuid} className="balance-item">
          <span className="member-name">{getMemberName(user_uuid)}</span>
          {balance === 0 && <span className="balance-value settled">is settled up</span>}
          {balance > 0 && <span className="balance-value positive">is owed ${balance.toFixed(2)}</span>}
          {balance < 0 && <span className="balance-value negative">owes ${Math.abs(balance).toFixed(2)}</span>}
        </li>
      ))}
    </ul>
  );
}

export default BalanceSummary;
