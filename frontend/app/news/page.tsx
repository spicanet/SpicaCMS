// ./app/news/page.tsx
'use client';

import { useEffect, useState } from 'react';
import api from '../../utils/api';

interface News {
  id: number;
  title: string;
  slug: string;
  content: string;
  author: string;
  published_at: string;
  // Добавьте другие поля по необходимости
}

export default function NewsPage() {
  const [news, setNews] = useState<News[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await api.get('/content/news/');
        setNews(response.data);
      } catch (err) {
        setError('Не удалось загрузить новости');
      } finally {
        setLoading(false);
      }
    };
    fetchNews();
  }, []);

  if (loading) return <p className="p-4">Загрузка...</p>;
  if (error) return <p className="p-4 text-red-500">{error}</p>;

  return (
    <div className="p-6">
      <h1 className="mb-4 text-2xl font-bold">Новости</h1>
      <ul>
        {news.map((item) => (
          <li key={item.id} className="mb-4">
            <h2 className="text-xl font-semibold">
              <a href={`/news/${item.slug}`} className="text-blue-600 hover:underline">
                {item.title}
              </a>
            </h2>
            <p className="text-sm text-gray-500">Автор: {item.author} | Опубликовано: {new Date(item.published_at).toLocaleDateString()}</p>
            <div dangerouslySetInnerHTML={{ __html: item.content }} className="mt-2 text-gray-700" />
          </li>
        ))}
      </ul>
    </div>
  );
}