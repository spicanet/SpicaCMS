// ./context/AuthContext.tsx
'use client';

import { createContext, useState, useContext, ReactNode, useEffect } from 'react';
import api from '../utils/api';

interface AuthContextProps {
  user: any;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextProps | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          // Предполагается, что есть эндпоинт для получения текущего пользователя
          const response = await api.get('/users/users/me/');
          setUser(response.data);
        } catch (error) {
          console.error(error);
          logout();
        }
      }
    };
    fetchUser();
  }, []);

  const login = async (username: string, password: string) => {
    try {
      const response = await api.post('/users/token/', { username, password });
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      // Получение данных пользователя
      const userResponse = await api.get('/users/users/me/');
      setUser(userResponse.data);
    } catch (error) {
      throw new Error('Неверные имя пользователя или пароль');
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth должен использоваться внутри AuthProvider');
  return context;
};