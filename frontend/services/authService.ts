// frontend/services/authService.ts

import api from '@/utils/api';

interface AuthResponse {
  access: string;
  refresh: string;
}

interface UserResponse {
  id: number;
  username: string;
  email: string;
  // Добавьте другие поля по необходимости
}

/**
 * Выполняет вход пользователя.
 * @param username Имя пользователя.
 * @param password Пароль.
 * @returns Токены доступа и обновления.
 */
export const loginUser = async (username: string, password: string): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>('/users/token/', { username, password });
  return response.data;
};

/**
 * Получает информацию о текущем пользователе.
 * @returns Информация о пользователе.
 */
export const getCurrentUser = async (): Promise<UserResponse> => {
  const response = await api.get<UserResponse>('/users/users/me/');
  return response.data;
};