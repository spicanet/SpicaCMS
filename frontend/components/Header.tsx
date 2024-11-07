// frontend/components/Header.tsx

'use client';

import Link from 'next/link';
import { useAuthContext } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useTheme } from '@/context/ThemeContext';

export default function Header() {
  const { user, logout } = useAuthContext();
  const router = useRouter();
  const { theme, toggleTheme } = useTheme();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  return (
    <header className="bg-navigation text-white">
      <div className="container mx-auto flex items-center justify-between p-4">
        <Link href="/" className="text-lg font-bold">SpicaCMS</Link>
        <nav className="flex items-center space-x-4">
          <Link href="/news" className="hover:text-gray-300">News</Link>
          {user ? (
            <>
              <Link href="/dashboard" className="hover:text-gray-300">Dashboard</Link>
              <button onClick={handleLogout} className="px-3 py-1 bg-primary rounded hover:bg-secondary">
                Выйти
              </button>
            </>
          ) : (
            <Link href="/login" className="px-3 py-1 bg-primary rounded hover:bg-secondary">Login</Link>
          )}
          {/* Кнопка переключения темы */}
          <button onClick={toggleTheme} className="px-3 py-1 bg-primary rounded hover:bg-secondary">
            {theme === 'light' ? 'Темная тема' : 'Светлая тема'}
          </button>
        </nav>
      </div>
    </header>
  );
}