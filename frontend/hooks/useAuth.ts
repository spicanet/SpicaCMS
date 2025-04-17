// frontend/hooks/useAuth.ts

import { useState, useEffect } from 'react';
import { loginUser, getCurrentUser } from '@/services/authService';
import { User } from '@/types/user';
import axios, { AxiosError } from 'axios';

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchUser = async () => {
      setLoading(true);
      setError('');
      try {
        const currentUser = await getCurrentUser();
        setUser(currentUser);
      } catch (err: any) {
        if (axios.isAxiosError(err) && err.response && err.response.status === 401) {
          // Не аутентифицирован, разлогиниваемся
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        }
        setError(err.response?.data?.detail || 'Ошибка при получении пользователя');
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      const tokens = await loginUser(username, password);
      localStorage.setItem('access_token', tokens.access);
      localStorage.setItem('refresh_token', tokens.refresh);
      const currentUser = await getCurrentUser();
      setUser(currentUser);
    } catch (err: any) {
      if (axios.isAxiosError(err) && err.response) {
        throw new Error(err.response.data.detail || 'Не удалось выполнить вход');
      } else {
        throw new Error('Не удалось выполнить вход');
      }
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };

  return { user, loading, error, login, logout };
};