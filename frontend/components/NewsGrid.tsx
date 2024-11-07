// frontend/components/NewsGrid.tsx

'use client';

import { useState, useEffect } from 'react';
import { News, ApiResponse } from '@/types/news';
import Paginator from '@/components/Paginator';
import Link from 'next/link';
import Image from 'next/image';
import { stripHtml } from '@/utils/stripHtml';
import { fetchFilteredNews } from '@/services/newsService';

interface NewsGridProps {
  columns: number;
  itemsPerPage: number;
  showPaginator: boolean;
  category?: string;
  tag?: string;
  author?: string;
  dateRange?: { start: string; end: string };
}

const NewsGrid: React.FC<NewsGridProps> = ({
  columns,
  itemsPerPage,
  showPaginator,
  category,
  tag,
  author,
  dateRange,
}) => {
  const [news, setNews] = useState<News[]>([]);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    const fetchNewsData = async () => {
      try {
        const params: any = {
          page: currentPage,
          limit: itemsPerPage,
        };

        if (category) params.category = category;
        if (tag) params.tag = tag;
        if (author) params.author = author;
        if (dateRange) {
          params.start_date = dateRange.start;
          params.end_date = dateRange.end;
        }

        const data: ApiResponse<News> = await fetchFilteredNews(params);
        setNews(data.results);
        setTotalPages(Math.ceil(data.count / itemsPerPage));
      } catch (err: any) {
        setError(err.message || 'Неизвестная ошибка');
      }
    };

    fetchNewsData();
  }, [currentPage, itemsPerPage, category, tag, author, dateRange]);

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  if (error) {
    return <p className="p-4 text-red-500">{error}</p>;
  }

  return (
    <div>
      <div
        className={`grid gap-6 ${
          columns === 1
            ? 'grid-cols-1'
            : columns === 2
            ? 'grid-cols-2'
            : 'grid-cols-3'
        }`}
      >
        {news.map((item: News) => (
          <div key={item.id} className="bg-lcard dark:bg-dcard rounded-lg shadow">
            {item.featured_image && (
              <Link href={`/news/${item.slug}`}>
                <Image
                  src={item.featured_image}
                  alt={item.title}
                  width={800}
                  height={400}
                  className="w-full h-auto object-cover rounded-t-lg"
                />
              </Link>
            )}
            <div className="p-4">
              <h2 className="text-xl font-semibold mb-2">
                <Link href={`/news/${item.slug}`} className="text-primary hover:underline">
                  {item.title}
                </Link>
              </h2>
              <p className="text-sm text-gray-500">
                Author: {item.author} | Posted: {new Date(item.published_at).toLocaleDateString()}
              </p>
              <p className="mt-2 text-dtext dark:text-ltext">
                {stripHtml(item.content).length > 200
                  ? `${stripHtml(item.content).slice(0, 200)}...`
                  : stripHtml(item.content)}
              </p>
            </div>
          </div>
        ))}
      </div>

      {showPaginator && (
        <Paginator totalPages={totalPages} currentPage={currentPage} onPageChange={handlePageChange} />
      )}
    </div>
  );
};

export default NewsGrid;