import { useContext } from 'react';
import { ClientContext } from '../contexts/ClientProvider';

/**
 * Custom hook to access the client context.
 * @returns {object} The client context value.
 */
const useClient = () => {
  return useContext(ClientContext);
};

export default useClient;

