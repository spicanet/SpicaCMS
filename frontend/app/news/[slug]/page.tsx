// ./app/news/[slug]/page.tsx
'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import api from '../../../utils/api';

interface News {
  id: number;
  title: string;
  slug: string;
  content: string;
  author: string;
  published_at: string;
  // Добавьте другие поля по необходимости
}

export default function NewsDetailPage({ params }: { params: { slug: string } }) {
  const router = useRouter();
  const { slug } = params;
  const [news, setNews] = useState<News | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchNewsDetail = async () => {
      try {
        const response = await api.get(`/content/news/?slug=${slug}`);
        if (response.data.length > 0) {
          setNews(response.data[0]);
        } else {
          setError('Новость не найдена');
        }
      } catch (err) {
        setError('Не удалось загрузить новость');
      } finally {
        setLoading(false);
      }
    };
    fetchNewsDetail();
  }, [slug]);

  if (loading) return <p className="p-4">Загрузка...</p>;
  if (error) return <p className="p-4 text-red-500">{error}</p>;
  if (!news) return null;

  return (
    <div className="p-6">
      <h1 className="mb-4 text-3xl font-bold">{news.title}</h1>
      <p className="text-sm text-gray-500">Автор: {news.author} | Опубликовано: {new Date(news.published_at).toLocaleDateString()}</p>
      <div dangerouslySetInnerHTML={{ __html: news.content }} className="mt-4 text-gray-700" />
      {/* Добавьте дополнительные элементы, такие как изображения, теги и т.д. */}
    </div>
  );
}