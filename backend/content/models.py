# backend/content/models.py

from django.db import models
from django.contrib.auth import get_user_model
from media_service.models import Image, Audio, Video, Gallery
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
from django.utils import timezone

User = get_user_model()

class NewsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"

    def __str__(self):
        return self.name

class NewsTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "News Tag"
        verbose_name_plural = "News Tags"

    def __str__(self):
        return self.name

class ArticleCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Article Category"
        verbose_name_plural = "Article Categories"

    def __str__(self):
        return self.name

class ArticleTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Article Tag"
        verbose_name_plural = "Article Tags"

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    categories = models.ManyToManyField(NewsCategory, related_name='news')
    tags = models.ManyToManyField(NewsTag, related_name='news')
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO поля
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=500, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)

    # Featured Image
    featured_image = models.ImageField(upload_to='news_featured_images/', blank=True, null=True)

    # Прикрепленные медиа
    galleries = models.ManyToManyField(Gallery, related_name='news', blank=True)
    audio_files = models.ManyToManyField(Audio, related_name='news', blank=True)
    video_files = models.ManyToManyField(Video, related_name='news', blank=True)

    source_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        permissions = [
            ("publish_news", "Can publish news"),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)

class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    categories = models.ManyToManyField(ArticleCategory, related_name='articles')
    tags = models.ManyToManyField(ArticleTag, related_name='articles')
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # SEO поля
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=500, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)

    # Featured Image
    featured_image = models.ImageField(upload_to='article_featured_images/', blank=True, null=True)

    # Прикрепленные медиа
    galleries = models.ManyToManyField(Gallery, related_name='articles', blank=True)
    audio_files = models.ManyToManyField(Audio, related_name='articles', blank=True)
    video_files = models.ManyToManyField(Video, related_name='articles', blank=True)

    source_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        permissions = [
            ("publish_article", "Can publish article"),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    # SEO поля
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=500, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)

    # Убраны поля og_image и canonical_url

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        permissions = [
            ("publish_page", "Can publish page"),
        ]

    def __str__(self):
        return self.title
    

class AutomationTemplate(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('news', 'News'),
        ('article', 'Article'),
    )

    name = models.CharField(max_length=255)
    content_type = models.CharField(
        max_length=10,
        choices=CONTENT_TYPE_CHOICES,
        default='news',
        help_text="Select whether to create News or Article entries."
    )
    site_url = models.URLField(help_text="Base URL of the site to parse.")
    list_page_url = models.URLField(help_text="URL of the page containing the list of articles.")
    pagination_xpath = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="XPath expression to the pagination links (if any)."
    )
    article_links_xpath = models.CharField(
        max_length=255,
        help_text="XPath expression to the article links on the list page."
    )
    title_xpath = models.CharField(
        max_length=255,
        help_text="XPath expression to the article title."
    )
    content_xpath = models.CharField(
        max_length=255,
        help_text="XPath expression to the article content."
    )
    featured_image_xpath = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="XPath expression to the featured image URL."
    )
    title_prompt = models.TextField(
        blank=True,
        null=True,
        help_text="AI prompt for rewriting the title."
    )
    content_prompt = models.TextField(
        blank=True,
        null=True,
        help_text="AI prompt for rewriting the content."
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='automation_templates',
        help_text="Select an existing author."
    )
    tags_xpath = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="XPath expression to the article tags."
    )
    categories_xpath = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="XPath expression to the article categories."
    )
    is_active = models.BooleanField(default=True)
    schedule = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="CRON expression for scheduling the automation."
    )
    last_run = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
