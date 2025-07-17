import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import GroupHeader from '../components/GroupHeader';
import BalanceView from '../components/BalanceView';
import ExpenseList from '../components/ExpenseList';
import ExpenseForm from '../components/ExpenseForm';

/**
 * Page component for displaying a single group's details.
 * @returns {JSX.Element} The rendered group page.
 */
function GroupPage() {
  const { groupId } = useParams();
  const [group, setGroup] = useState(null);
  const [expenses, setExpenses] = useState([]);
  const [balances, setBalances] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const groupRes = await api.get(`/groups/${groupId}`);
      const expensesRes = await api.get(`/groups/${groupId}/expenses`);
      const balancesRes = await api.get(`/groups/${groupId}/balances`);
      
      setGroup(groupRes.data);
      setExpenses(expensesRes.data);
      setBalances(balancesRes.data);
      setError('');
    } catch (err) {
      setError('Failed to load group data. The group may not exist.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [groupId]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (loading) return <div>Loading group...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!group) return <div>Group not found.</div>;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <Link to="/">&larr; Back to all groups</Link>
      <GroupHeader name={group.name} inviteCode={group.invite_code} />
      {balances && <BalanceView balances={balances.balances} transactions={balances.transactions} members={group.members} />}
      <ExpenseForm groupId={group.id} members={group.members} onExpenseAdded={fetchData} />
      <ExpenseList expenses={expenses} onExpenseDeleted={fetchData} />
    </div>
  );
}

export default GroupPage;

