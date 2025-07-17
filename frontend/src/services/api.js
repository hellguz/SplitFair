import axios from 'axios';

/**
 * Creates an Axios instance for making API requests.
 * The baseURL is configured to work with the Vite proxy.
 * A 'Client-ID' header will be set dynamically by the ClientProvider.
 */
const api = axios.create({
  baseURL: '/api', // This will be proxied by Vite dev server
});

export default api;