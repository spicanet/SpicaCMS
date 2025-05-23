// frontend/services/newsService.ts

import api from '@/utils/api';
import { News, ApiResponse } from '@/types/news';

interface FetchNewsParams {
  page?: number;
  page_size?: number;
  category?: string;
  tag?: string;
  author?: string;
  start_date?: string;
  end_date?: string;
}

export const fetchFilteredNews = async (params: FetchNewsParams): Promise<ApiResponse<News>> => {
  const response = await api.get<ApiResponse<News>>('/content/news/', { params });
  return response.data;
};

export const fetchNewsBySlug = async (slug: string): Promise<News> => {
  const response = await api.get<ApiResponse<News>>('/content/news/', { params: { slug } });
  if (response.data.results.length === 0) {
    throw new Error('News not found');
  }
  return response.data.results[0];
};