# backend/autoposter/tasks.py

from celery import shared_task
from ai_service.models import RewrittenItem, CommentGenerationConfig
from content.models import News
from django.contrib.auth.models import User
from ai_service.tasks import generate_comments

@shared_task
def run_autoposting():
    rewritten_items = RewrittenItem.objects.filter(status='processed')
    author = User.objects.first()  # Выберите автора или создайте отдельного пользователя для автопостинга

    # Получаем конфигурацию генерации комментариев
    comment_config = CommentGenerationConfig.objects.first()  # Или выберите соответствующую конфигурацию

    for item in rewritten_items:
        # Создайте новую запись в модели News
        news = News.objects.create(
            title=item.rewritten_title,
            content=item.rewritten_content,
            author=author,
            # Установите необходимые поля, например, категории, теги
        )

        # Связываем RewrittenItem с созданной новостью
        item.status = 'published'
        item.save()

        # Запускаем задачу генерации комментариев
        generate_comments.delay(item.id, comment_config.id)

    return 'Autoposting completed successfully.'
