# backend/parsing_service/tasks.py

from celery import shared_task
from .models import ParsingTemplate, ParsedItem
import requests
from lxml import html
from datetime import datetime
from django.utils import timezone

@shared_task
def run_parsing(template_id):
    try:
        template = ParsingTemplate.objects.get(id=template_id)
        if not template.is_active:
            return 'Template is not active.'

        response = requests.get(template.list_page_url)
        tree = html.fromstring(response.content)
        article_links = tree.xpath(template.article_links_xpath)

        for link in article_links:
            url = link if link.startswith('http') else template.site_url + link
            # Проверка на существование ParsedItem с таким URL
            if ParsedItem.objects.filter(url=url, template=template).exists():
                continue

            article_response = requests.get(url)
            article_tree = html.fromstring(article_response.content)
            title = article_tree.xpath(template.title_xpath)
            content = article_tree.xpath(template.content_xpath)
            author = article_tree.xpath(template.author_xpath) if template.author_xpath else ''
            publish_date = article_tree.xpath(template.publish_date_xpath) if template.publish_date_xpath else ''

            # Обработка и очистка данных
            title = title[0].text_content().strip() if title else 'No Title'
            content = content[0].text_content().strip() if content else 'No Content'
            author = author[0].text_content().strip() if author else ''
            if publish_date:
                publish_date = publish_date[0].text_content().strip()
                try:
                    publish_date = datetime.strptime(publish_date, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    publish_date = timezone.now()
            else:
                publish_date = timezone.now()

            ParsedItem.objects.create(
                template=template,
                url=url,
                title=title,
                content=content,
                author=author,
                publish_date=publish_date,
                status='pending'
            )

        return 'Parsing completed successfully.'

    except Exception as e:
        return str(e)

@shared_task
def run_all_parsing():
    templates = ParsingTemplate.objects.filter(is_active=True)
    for template in templates:
        run_parsing.delay(template.id)
