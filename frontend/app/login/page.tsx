// ./app/login/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../context/AuthContext';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const router = useRouter();
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(username, password);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form onSubmit={handleSubmit} className="p-6 bg-white rounded shadow-md w-full max-w-sm">
        <h2 className="mb-4 text-xl font-bold text-center">Вход в SpicaCMS</h2>
        {error && <p className="mb-4 text-red-500">{error}</p>}
        <div className="mb-4">
          <label className="block mb-1" htmlFor="username">Имя пользователя</label>
          <input
            id="username"
            type="text"
            className="w-full px-3 py-2 border rounded"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-4">
          <label className="block mb-1" htmlFor="password">Пароль</label>
          <input
            id="password"
            type="password"
            className="w-full px-3 py-2 border rounded"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="w-full px-3 py-2 text-white bg-blue-500 rounded hover:bg-blue-600">
          Войти
        </button>
      </form>
    </div>
  );
}