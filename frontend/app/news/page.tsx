// frontend/app/news/page.tsx

import NewsGrid from '@/components/NewsGrid';
import { fetchFilteredNews } from '@/services/newsService';
import { News, ApiResponse } from '@/types/news';

interface NewsPageProps {
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function NewsPage({ searchParams }: NewsPageProps) {
  const category = searchParams.category ? String(searchParams.category) : undefined;
  const tag = searchParams.tag ? String(searchParams.tag) : undefined;
  const author = searchParams.author ? String(searchParams.author) : undefined;
  const startDate = searchParams.start_date ? String(searchParams.start_date) : undefined;
  const endDate = searchParams.end_date ? String(searchParams.end_date) : undefined;
  const page = searchParams.page ? parseInt(String(searchParams.page), 10) : 1;
  const itemsPerPage = 30;

  const dateRange = startDate && endDate ? { start: startDate, end: endDate } : undefined;

  try {
    const params: any = {
      page,
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

    return (
      <>
        <h1 className="mb-4 text-2xl font-bold">Новости</h1>
        <NewsGrid
          columns={3}
          itemsPerPage={itemsPerPage}
          showPaginator={true}
          category={category}
          tag={tag}
          author={author}
          dateRange={dateRange}
        />
      </>
    );
  } catch (error: any) {
    return <p className="p-4 text-red-500">{error.message || 'Ошибка при загрузке новостей'}</p>;
  }
}