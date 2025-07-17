// ./frontend/src/contexts/UserContext.jsx
/**
 * @file React Context to manage user's unique ID and joined groups.
 */
import React, { createContext, useContext } from 'react';
import useLocalStorage from '../hooks/useLocalStorage';
import { v4 as uuidv4 } from 'uuid';

const UserContext = createContext();

export const useUser = () => useContext(UserContext);

export const UserProvider = ({ children }) => {
  const [clientUUID, setClientUUID] = useLocalStorage('splitfair_clientUUID', null);
  const [joinedGroups, setJoinedGroups] = useLocalStorage('splitfair_joinedGroups', []);

  // Generate a UUID if one doesn't exist
  if (!clientUUID) {
    setClientUUID(uuidv4());
  }
  
  /**
   * Adds a group ID to the list of joined groups in local storage.
   * @param {string} groupId - The ID of the group to add.
   */
  const addJoinedGroup = (groupId) => {
    if (!joinedGroups.includes(groupId)) {
        setJoinedGroups([...joinedGroups, groupId]);
    }
  };

  const value = {
    clientUUID,
    joinedGroups,
    addJoinedGroup,
  };

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
};


