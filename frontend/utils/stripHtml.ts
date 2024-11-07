// frontend/utils/stripHtml.ts

/**
 * Функция для удаления HTML-тегов из строки.
 * @param html Строка с HTML.
 * @returns Чистый текст без HTML.
 */
export function stripHtml(html: string): string {
    if (typeof window !== 'undefined') {
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = html;
      return tempDiv.textContent || tempDiv.innerText || '';
    } else {
      // Для серверной стороны используем регулярное выражение
      return html.replace(/<\/?[^>]+(>|$)/g, "");
    }
  }