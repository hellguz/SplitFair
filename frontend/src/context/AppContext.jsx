import React, { createContext, useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import api from '../api';

export const AppContext = createContext();

/**
 * Provides global state to the application, including user identity,
 * group list, and loading/error states.
 */
export const AppProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [groups, setGroups] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  /**
   * Initializes the user's identity on application load.
   * - Checks for a UUID in localStorage.
   * - If not found, creates a new user via the API.
   * - If found, fetches user data from the API.
   */
  useEffect(() => {
    const initializeUser = async () => {
      setIsLoading(true);
      setError('');
      let userUUID = localStorage.getItem('userUUID');

      try {
        if (!userUUID) {
          userUUID = uuidv4();
          const name = `User-${userUUID.substring(0, 4)}`;
          const response = await api.post('/api/users', { uuid: userUUID, name });
          localStorage.setItem('userUUID', userUUID);
          setUser(response.data);
        } else {
           try {
              const response = await api.get('/api/users/me');
              setUser(response.data);
           } catch (userError) {
              // If user not found on backend (e.g. DB was cleared), re-create them.
              if (userError.response && userError.response.status === 403) {
                  const name = `User-${userUUID.substring(0, 4)}`;
                  const response = await api.post('/api/users', { uuid: userUUID, name });
                  setUser(response.data);
              } else {
                 throw userError;
              }
           }
        }
      } catch (err) {
        console.error("Initialization failed:", err);
        setError('Failed to initialize application. Please try again later.');
        localStorage.removeItem('userUUID'); // Clear bad data
      } finally {
        setIsLoading(false);
      }
    };
    initializeUser();
  }, []);

  /**
   * Fetches the list of groups the user belongs to.
   * This runs whenever the user object is successfully set.
   */
  const fetchGroups = async () => {
      if (!user) return;
      try {
          const response = await api.get('/api/users/me/groups');
          setGroups(response.data);
      } catch (err) {
          console.error("Failed to fetch groups:", err);
          setError('Could not load your groups.');
      }
  };

  useEffect(() => {
    fetchGroups();
  }, [user]);

  const value = {
    user,
    groups,
    isLoading,
    error,
    refreshGroups: fetchGroups,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
