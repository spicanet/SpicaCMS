# backend/content/tasks.py

from celery import shared_task
from .models import AutomationTemplate, News, Article, ArticleCategory, ArticleTag, NewsCategory, NewsTag
from django.contrib.auth import get_user_model
import requests
from lxml import html
from datetime import datetime
from django.utils import timezone
from django.db import transaction
import openai
from django.conf import settings
from django.core.files.base import ContentFile
from urllib.parse import urljoin
import os
from django.utils.text import slugify
import logging
from openai import OpenAI
import uuid
import markdown

logger = logging.getLogger('automation')

client = OpenAI(api_key=settings.OPENAI_API_KEY)

User = get_user_model()

def markdown_to_html(markdown_text):
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_text, extensions=['extra', 'tables', 'toc'])
    return html_content

@shared_task
def run_automation(template_id):
    logger.info(f"Starting automation task for template ID: {template_id}")
    try:
        template = AutomationTemplate.objects.get(id=template_id)
        if not template.is_active:
            logger.warning(f"Template '{template.name}' is not active.")
            return 'Template is not active.'

        # Author assignment with fallback
        author = template.author if template.author else User.objects.first()
        if not author:
            logger.error("No author found for creating the content. Please specify an author.")
            return 'No author available.'

        logger.info(f"Parsing list page URL: {template.list_page_url}")
        response = requests.get(template.list_page_url)
        if response.status_code != 200:
            logger.error(f"Failed to retrieve list page. Status code: {response.status_code}")
            return 'Failed to retrieve list page.'

        tree = html.fromstring(response.content)

        # Получаем все ссылки, соответствующие XPath-запросу
        article_links = tree.xpath(template.article_links_xpath)
        logger.info(f"Found {len(article_links)} article links.")

        article_links = tree.xpath(template.article_links_xpath)
        logger.info(f"Found {len(article_links)} article links.")

        for link in article_links:
            url = link if link.startswith('http') else urljoin(template.site_url, link)

            # Check if content with this URL already exists in Article or News
            if template.content_type == 'news' and News.objects.filter(source_url=url).exists():
                logger.info(f"News with source URL '{url}' already exists. Skipping.")
                continue
            elif template.content_type == 'article' and Article.objects.filter(source_url=url).exists():
                logger.info(f"Article with source URL '{url}' already exists. Skipping.")
                continue

            logger.debug(f"Processing article URL: {url}")

            article_response = requests.get(url)
            if article_response.status_code != 200:
                logger.error(f"Failed to retrieve article page. Status code: {article_response.status_code}")
                continue

            article_tree = html.fromstring(article_response.content)

            # Extract title and content
            title_element = article_tree.xpath(template.title_xpath)
            content_element = article_tree.xpath(template.content_xpath)

            if not title_element or not content_element:
                logger.warning(f"Failed to extract title or content from {url}. Skipping.")
                continue

            title = title_element[0].text_content().strip()
            content = html.tostring(content_element[0], encoding='unicode')

            logger.debug(f"Original title: {title}")
            logger.debug(f"Original content length: {len(content)} characters")

             # AI rewrite of the title
            if template.title_prompt:
                logger.info("Rewriting title using AI.")
                ai_title_prompt = f"{template.title_prompt}\n\nOriginal Title: {title}"
                try:
                    completion = client.chat.completions.create(
                        model="gpt-4o-mini-2024-07-18",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": ai_title_prompt
                                    }
                                ]
                            }
                        ],
                        temperature=0.7,
                        max_tokens=100,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        response_format={
                            "type": "text"
                        }
                    )
                    # Используем метод 'get' для извлечения текста
                    title = completion.choices[0].message.content
                    title = title.strip('\'"')
                    logger.debug(f"Rewritten title: {title}")
                except Exception as e:
                    logger.error(f"Failed to rewrite title: {e}")
                    continue

            # AI rewrite of the content
            if template.content_prompt:
                logger.info("Rewriting content using AI.")
                ai_content_prompt = f"{template.content_prompt}\n\nOriginal Content: {content}"
                try:
                    completion = client.chat.completions.create(
                        model="gpt-4o-mini-2024-07-18",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": ai_content_prompt
                                    }
                                ]
                            }
                        ],
                        temperature=0.7,
                        max_tokens=1000,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                        response_format={
                            "type": "text"
                        }
                    )
                    content = completion.choices[0].message.content
                    html_content = markdown_to_html(content)
                    # logger.debug(f"Rewritten content: {content}")
                except Exception as e:
                    logger.error(f"Failed to rewrite content: {e}")
                    continue

            # Extract featured image
            featured_image_url = None
            if template.featured_image_xpath:
                logger.info("Extracting featured image.")
                featured_image_element = article_tree.xpath(template.featured_image_xpath)
                if featured_image_element:
                    featured_image_url = featured_image_element[0]
                    if not featured_image_url.startswith('http'):
                        featured_image_url = urljoin(template.site_url, featured_image_url)
                    logger.debug(f"Featured image URL: {featured_image_url}")

            # Extract tags and categories
            tags = []  # Initialize tags
            categories = []  # Initialize categories

            if template.tags_xpath:
                logger.info("Extracting tags.")
                tags_elements = article_tree.xpath(template.tags_xpath)
                # Use .text if tags_elements are elements; otherwise, use them directly if they are strings
                tags_text = [tag.text.strip() if hasattr(tag, 'text') else tag.strip() for tag in tags_elements]
                logger.debug(f"Found tags: {tags_text}")
                
                # Use ArticleTag for articles and NewsTag for news
                TagModel = ArticleTag if template.content_type == 'article' else NewsTag
                
                for tag_name in tags_text:
                    tag, created = TagModel.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(tag_name)}
                    )
                    tags.append(tag)  # Append the tag object to the list

            if template.categories_xpath:
                logger.info("Extracting categories.")
                categories_elements = article_tree.xpath(template.categories_xpath)
                # Use .text if categories_elements are elements; otherwise, use them directly if they are strings
                categories_text = [cat.text.strip() if hasattr(cat, 'text') else cat.strip() for cat in categories_elements]
                logger.debug(f"Found categories: {categories_text}")
                
                # Use ArticleCategory for articles and NewsCategory for news
                CategoryModel = ArticleCategory if template.content_type == 'article' else NewsCategory
                
                for category_name in categories_text:
                    category, created = CategoryModel.objects.get_or_create(
                        name=category_name,
                        defaults={'slug': slugify(category_name)}
                    )
                    categories.append(category)  # Append the category object to the list

            # Create content (News or Article)
            logger.info(f"Creating {template.content_type} entry.")
            try:
                with transaction.atomic():
                    if template.content_type == 'news':
                        content_instance = News.objects.create(
                            title=title,
                            slug=slugify(title),
                            content=html_content,
                            author=author,
                            published_at=timezone.now(),
                            source_url=url
                        )
                    elif template.content_type == 'article':
                        content_instance = Article.objects.create(
                            title=title,
                            slug=slugify(title),
                            content=html_content,
                            author=author,
                            published_at=timezone.now(),
                            source_url=url
                        )
                    else:
                        logger.error(f"Invalid content type: {template.content_type}")
                        return  # Skip if content_type is invalid

                    content_instance.tags.set(tags)  # Set tags using tag objects
                    content_instance.categories.set(categories)  # Set categories using category objects

                    # Download and save featured image
                    if featured_image_url:
                        logger.info("Downloading featured image.")
                        image_response = requests.get(featured_image_url)
                        if image_response.status_code == 200:
                            # Generate a unique filename
                            # image_name = f"{uuid.uuid4()}.jpg"
                            image_name = f"{content_instance.slug}.jpg"
                            content_instance.featured_image.save(
                                image_name,
                                ContentFile(image_response.content),
                                save=True
                            )
                            logger.debug("Featured image saved.")
                        else:
                            logger.error(f"Failed to download featured image. Status code: {image_response.status_code}")

                logger.info(f"{template.content_type.capitalize()} '{title}' created successfully.")

            except Exception as e:
                logger.error(f"Failed to create {template.content_type}: {e}")
                return

        # Update last run time
        template.last_run = timezone.now()
        template.save()
        logger.info(f"Automation task for template '{template.name}' completed.")

        return 'Automation task completed successfully.'

    except Exception as e:
        logger.exception(f"An error occurred during automation: {e}")
        return str(e)
