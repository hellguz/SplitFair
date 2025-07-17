// ./frontend/src/hooks/useLocalStorage.js
/**
 * @file Custom React hook to manage state in Local Storage.
 */
import { useState, useEffect } from 'react';

/**
 * A custom hook that syncs a state with Local Storage.
 * @param {string} key - The key to use in Local Storage.
 * @param {*} initialValue - The initial value to use if nothing is in Local Storage.
 * @returns {[any, function]} - A stateful value, and a function to update it.
 */
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  const setValue = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(error);
    }
  };

  return [storedValue, setValue];
}

export default useLocalStorage;


