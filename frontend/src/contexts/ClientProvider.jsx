import React, { createContext, useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import api from '../services/api';

export const ClientContext = createContext();

/**
 * Provides a unique client ID and manages the list of joined groups.
 * The client ID is persisted in localStorage.
 * @param {object} props - The component props.
 * @param {React.ReactNode} props.children - The child components.
 * @returns {JSX.Element} The context provider component.
 */
export const ClientProvider = ({ children }) => {
  const [clientId, setClientId] = useState(null);
  const [joinedGroupIds, setJoinedGroupIds] = useState([]);

  useEffect(() => {
    let storedClientId = localStorage.getItem('clientId');
    if (!storedClientId) {
      storedClientId = uuidv4();
      localStorage.setItem('clientId', storedClientId);
    }
    setClientId(storedClientId);
    api.defaults.headers.common['Client-ID'] = storedClientId;

    const storedGroupIds = JSON.parse(localStorage.getItem('joinedGroupIds') || '[]');
    setJoinedGroupIds(storedGroupIds);
  }, []);

  const addJoinedGroup = (groupId) => {
    if (!joinedGroupIds.includes(groupId)) {
      const newGroupIds = [...joinedGroupIds, groupId];
      setJoinedGroupIds(newGroupIds);
      localStorage.setItem('joinedGroupIds', JSON.stringify(newGroupIds));
    }
  };

  const value = { clientId, joinedGroupIds, addJoinedGroup };

  return (
    <ClientContext.Provider value={value}>
      {clientId ? children : <div>Loading...</div>}
    </ClientContext.Provider>
  );
};

