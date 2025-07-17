// ./frontend/src/api/index.js
/**
 * @file Axios instance configuration for making API requests to the backend.
 */
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

export default api;


