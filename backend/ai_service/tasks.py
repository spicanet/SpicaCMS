# backend/ai_service/tasks.py

from celery import shared_task
from django.conf import settings
from .models import RewrittenItem, RewritePrompt, CommentGenerationConfig
from parsing_service.models import ParsedItem
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
import openai

openai.api_key = settings.OPENAI_API_KEY

@shared_task
def run_rewriting(parsed_item_id, prompt_id):
    try:
        parsed_item = ParsedItem.objects.get(id=parsed_item_id)
        prompt = RewritePrompt.objects.get(id=prompt_id)

        # Создаем промпт для AI
        ai_prompt = f"{prompt.prompt_text}\n\nTitle: {parsed_item.title}\nContent: {parsed_item.content}"

        # Отправляем запрос к OpenAI API
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=ai_prompt,
            max_tokens=1024,
            temperature=0.7,
        )

        rewritten_text = response.choices[0].text.strip()

        # Здесь можно разделить заголовок и контент, если AI возвращает оба
        rewritten_title = parsed_item.title  # Или используйте результат AI

        # Сохраняем рерайтенный материал
        RewrittenItem.objects.create(
            parsed_item=parsed_item,
            rewritten_title=rewritten_title,
            rewritten_content=rewritten_text,
            status='processed'
        )

        parsed_item.status = 'processed'
        parsed_item.save()

        return 'Rewriting completed successfully.'

    except Exception as e:
        parsed_item.status = 'failed'
        parsed_item.save()
        return str(e)

@shared_task
def process_new_parsed_items():
    parsed_items = ParsedItem.objects.filter(status='pending')
    prompt = RewritePrompt.objects.first()  # Выберите подходящий промпт
    for item in parsed_items:
        run_rewriting.delay(item.id, prompt.id)

@shared_task
def generate_comments(rewritten_item_id, config_id):
    try:
        rewritten_item = RewrittenItem.objects.get(id=rewritten_item_id)
        config = CommentGenerationConfig.objects.get(id=config_id)
        content = rewritten_item.rewritten_content

        for _ in range(config.number_of_comments):
            prompt = config.prompt_template.format(content=content)
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                max_tokens=150,
                temperature=0.7,
            )
            comment_text = response.choices[0].text.strip()

            # Создаем комментарий
            Comment.objects.create(
                user=config.created_by,  # Или создайте специального пользователя для автогенерированных комментариев
                content_type=ContentType.objects.get_for_model(RewrittenItem),
                object_id=rewritten_item.id,
                text=comment_text,
                is_generated=True,
            )

        return f'{config.number_of_comments} comments generated successfully.'

    except Exception as e:
        return str(e)
