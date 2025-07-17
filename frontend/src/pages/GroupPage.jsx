// ./frontend/src/pages/GroupPage.jsx
/**
 * @file The main page for viewing a single group, its expenses, and balances.
 */
import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import toast from 'react-hot-toast';
import GroupHeader from '../components/GroupHeader';
import Balances from '../components/Balances';
import ExpenseList from '../components/ExpenseList';
import AddExpenseModal from '../components/AddExpenseModal';

function GroupPage() {
  const { groupId } = useParams();
  const [group, setGroup] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [ws, setWs] = useState(null);

  const fetchGroupData = useCallback(async () => {
    try {
      const response = await api.get(`/groups/${groupId}`);
      setGroup(response.data);
    } catch (error) {
      toast.error('Failed to fetch group details.');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }, [groupId]);

  useEffect(() => {
    fetchGroupData();

    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host.replace(':3000', ':8000')}/ws/${groupId}`;
    
    const socket = new WebSocket(wsUrl);
    setWs(socket);

    socket.onopen = () => console.log("WebSocket connected");
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.event === 'expense_update') {
            toast('Group updated!', { icon: '🔄' });
            fetchGroupData();
        }
    };
    socket.onclose = () => console.log("WebSocket disconnected");
    socket.onerror = (error) => console.error("WebSocket error:", error);

    return () => {
      socket.close();
    };
  }, [groupId, fetchGroupData]);
  
  const handleExpenseAdded = () => {
    setIsModalOpen(false);
    // Data will be refetched via WebSocket message, no need to call fetchGroupData here
  };

  const handleExpenseDeleted = async (expenseId) => {
    if(window.confirm("Are you sure you want to delete this expense?")){
        try {
            await api.delete(`/expenses/${expenseId}`);
            toast.success("Expense deleted.");
            // Refetch triggered by WebSocket
        } catch (error) {
            toast.error("Failed to delete expense.");
            console.error(error);
        }
    }
  };

  if (isLoading) return <p>Loading group...</p>;
  if (!group) return <p>Group not found.</p>;

  return (
    <div>
      <GroupHeader group={group} />
      <Balances users={group.users} expenses={group.expenses} />
      <hr style={{margin: '2rem 0'}}/>
      <button onClick={() => setIsModalOpen(true)}>Add Expense</button>
      <ExpenseList expenses={group.expenses} onDelete={handleExpenseDeleted} />
      {isModalOpen && (
        <AddExpenseModal
          users={group.users}
          groupId={groupId}
          onClose={() => setIsModalOpen(false)}
          onExpenseAdded={handleExpenseAdded}
        />
      )}
    </div>
  );
}

export default GroupPage;


