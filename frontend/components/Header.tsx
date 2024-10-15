// ./components/Header.tsx
'use client';

import Link from 'next/link';
import { useAuth } from '../context/AuthContext';
import { useRouter } from 'next/navigation';

export default function Header() {
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <header className="flex items-center justify-between p-4 bg-gray-800 text-white">
      <Link href="/" className="text-lg font-bold">SpicaCMS</Link>
      <nav>
        <Link href="/news" className="mr-4">Новости</Link>
        {user ? (
          <>
            <Link href="/dashboard" className="mr-4">Панель управления</Link>
            <button onClick={handleLogout} className="px-3 py-1 bg-red-500 rounded hover:bg-red-600">
              Выйти
            </button>
          </>
        ) : (
          <Link href="/login" className="px-3 py-1 bg-blue-500 rounded hover:bg-blue-600">Войти</Link>
        )}
      </nav>
    </header>
  );
}