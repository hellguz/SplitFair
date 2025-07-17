import React from 'react';

/**
 * Displays the calculated balances and settlement transactions.
 * @param {object} props - The component props.
 * @param {Array<object>} props.balances - List of member balances.
 * @param {Array<object>} props.transactions - List of settlement transactions.
 * @param {Array<object>} props.members - List of all group members.
 * @returns {JSX.Element} The rendered balance view component.
 */
function BalanceView({ balances, transactions, members }) {
  const memberMap = members.reduce((acc, member) => {
    acc[member.id] = member.nickname;
    return acc;
  }, {});

  return (
    <div className="card">
      <h3>Balances</h3>
      <h4>Net Balances</h4>
      <ul>
        {balances.map(({ member_id, balance }) => (
          <li key={member_id} style={{ color: balance < 0 ? '#ffb3b3' : '#a7ffa7' }}>
            {memberMap[member_id] || 'Unknown'}: {balance.toFixed(2)}
          </li>
        ))}
      </ul>
      <h4>How to Settle Up</h4>
      {transactions.length > 0 ? (
        <ul>
          {transactions.map((tx, index) => (
            <li key={index}>
              <strong>{memberMap[tx.from_member_id] || 'Unknown'}</strong> owes{' '}
              <strong>{memberMap[tx.to_member_id] || 'Unknown'}</strong> the amount of{' '}
              <strong>${tx.amount.toFixed(2)}</strong>
            </li>
          ))}
        </ul>
      ) : (
        <p>All settled up!</p>
      )}
    </div>
  );
}

export default BalanceView;

