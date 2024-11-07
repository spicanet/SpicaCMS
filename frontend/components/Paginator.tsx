// frontend/components/Paginator.tsx

'use client';

import Link from 'next/link';

interface PaginatorProps {
  totalPages: number;
  currentPage: number;
  onPageChange: (page: number) => void;
}

const Paginator: React.FC<PaginatorProps> = ({ totalPages, currentPage, onPageChange }) => {
  if (totalPages === 1) return null;

  const handleClick = (page: number) => {
    onPageChange(page);
  };

  return (
    <div className="flex justify-center mt-6">
      {currentPage > 1 && (
        <button
          onClick={() => handleClick(currentPage - 1)}
          className="px-4 py-2 mx-1 rounded bg-primary text-white hover:bg-secondary"
        >
          Назад
        </button>
      )}
      {Array.from({ length: totalPages }, (_, index) => (
        <button
          key={index + 1}
          onClick={() => handleClick(index + 1)}
          className={`px-4 py-2 mx-1 rounded ${
            currentPage === index + 1
              ? 'bg-primary text-white'
              : 'bg-primary text-white hover:bg-secondary'
          }`}
        >
          {index + 1}
        </button>
      ))}
      {currentPage < totalPages && (
        <button
          onClick={() => handleClick(currentPage + 1)}
          className="px-4 py-2 mx-1 rounded bg-primary text-white hover:bg-secondary"
        >
          Далее
        </button>
      )}
    </div>
  );
};

export default Paginator;