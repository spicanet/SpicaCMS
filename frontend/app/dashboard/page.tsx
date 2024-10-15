'use client';

import ProtectedRoute from '../../components/ProtectedRoute';

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <div className="p-6">
        <h1 className="text-2xl font-bold">Панель управления</h1>
        {/* Добавьте содержимое панели управления здесь */}
      </div>
    </ProtectedRoute>
  );
}
