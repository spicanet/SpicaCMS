// frontend/app/page.tsx

import NewsGrid from '@/components/NewsGrid';

export default function Home() {
  // Получаем slugs категорий из переменных окружения
  const categorySlugs = process.env.NEXT_PUBLIC_CATEGORY_SLUGS
    ? process.env.NEXT_PUBLIC_CATEGORY_SLUGS.split(',').map(slug => slug.trim())
    : [];

  return (
    <>
      {/* Отображаем NewsGrid для каждой категории */}
      {categorySlugs.map(slug => (
        <div key={slug}>
          <h2 className="text-xl font-semibold mb-4 capitalize">{slug}</h2>
          <NewsGrid
            columns={3}
            itemsPerPage={6}
            showPaginator={false}
            category={slug}
          />
        </div>
      ))}
    </>
  );
}