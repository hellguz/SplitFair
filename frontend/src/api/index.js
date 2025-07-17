import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
});

/**
 * Interceptor to add the user's unique ID to every outgoing request header.
 * This is how the backend identifies the user without traditional authentication.
 */
api.interceptors.request.use((config) => {
  const userId = localStorage.getItem('userUUID');
  if (userId) {
    config.headers['X-User-ID'] = userId;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default api;
