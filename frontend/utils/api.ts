// frontend/utils/api.ts

import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8004/api',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default api;