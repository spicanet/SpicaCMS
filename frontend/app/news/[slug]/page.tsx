// frontend/app/news/[slug]/page.tsx

import { Metadata } from 'next';
import { fetchNewsBySlug } from '@/services/newsService';
import Image from 'next/image';
import { News } from '@/types/news';

export const metadata: Metadata = {
  title: 'News Detail',
};

export default async function NewsDetailPage({ params }: { params: { slug: string } }) {
  const { slug } = params;
  let news: News | null = null;
  let error = '';

  try {
    news = await fetchNewsBySlug(slug);
  } catch (err: any) {
    error = err.message || 'Failed to load news';
  }

  if (error) {
    return <p className="p-4 text-red-500">{error}</p>;
  }

  if (!news) {
    return null;
  }

  return (
    <div className="container mx-auto p-6">
      <div className="bg-white dark:bg-gray-800 mb-4 rounded-lg shadow">
        {news.featured_image && (
          <Image
            src={news.featured_image}
            alt={news.title}
            width={800}
            height={400}
            className="w-full h-auto object-cover rounded-t-lg"
          />
        )}
        <div className="p-6"> 
          <h1 className="mb-4 text-3xl font-bold">{news.title}</h1>
          <p className="text-sm text-gray-500">
            Author: {news.author} | Posted: {new Date(news.published_at).toLocaleDateString()}
          </p>
          <div
            dangerouslySetInnerHTML={{ __html: news.content }}
            className="mt-4 text-gray-700 dark:text-white"
          />
        </div>
      </div>
    </div>
  );
}