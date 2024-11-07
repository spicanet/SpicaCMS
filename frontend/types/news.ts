// frontend/types/news.ts

export interface Category {
    id: number;
    name: string;
    slug: string;
}

export interface Tag {
    id: number;
    name: string;
    slug: string;
}

export interface News {
    id: number;
    title: string;
    slug: string;
    content: string;
    author: string;
    published_at: string;
    updated_at: string;
    meta_title?: string | null;
    meta_description?: string | null;
    meta_keywords?: string | null;
    featured_image?: string;
    categories: Category[];
    tags: Tag[];
    galleries: any[]; // При необходимости уточните тип
    audio_files: any[]; // При необходимости уточните тип
    video_files: any[]; // При необходимости уточните тип
}

export interface ApiResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}