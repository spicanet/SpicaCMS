# backend/content/admin.py

from django.contrib import admin
from .models import (
    News,
    Article,
    Page,
    NewsCategory,
    NewsTag,
    ArticleCategory,
    ArticleTag,
    AutomationTemplate
)
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .forms import AutomationTemplateForm
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'

class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'

class PageForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Page
        fields = '__all__'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('title', 'author', 'published_at')
    list_filter = ('categories', 'tags', 'published_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('published_at', 'updated_at')
    filter_horizontal = ('categories', 'tags', 'galleries', 'audio_files', 'video_files')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'author', 'published_at')
    list_filter = ('categories', 'tags', 'published_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('published_at', 'updated_at')
    filter_horizontal = ('categories', 'tags', 'galleries', 'audio_files', 'video_files')

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageForm
    list_display = ('title', 'author', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class AutomationTemplateForm(forms.ModelForm):
    class Meta:
        model = AutomationTemplate
        fields = [
            'name',
            'content_type',
            'site_url',
            'list_page_url',
            'pagination_xpath',
            'article_links_xpath',
            'title_xpath',
            'content_xpath',
            'featured_image_xpath',
            'title_prompt',
            'content_prompt',
            'author',
            'tags_xpath',
            'categories_xpath',
            'is_active',
            'schedule',
        ]
        widgets = {
            'title_prompt': forms.Textarea(attrs={'rows': 4}),
            'content_prompt': forms.Textarea(attrs={'rows': 4}),
            'schedule': forms.TextInput(attrs={'placeholder': 'CRON expression'}),
        }

@admin.register(AutomationTemplate)
class AutomationTemplateAdmin(admin.ModelAdmin):
    form = AutomationTemplateForm
    list_display = ('name', 'content_type', 'site_url', 'is_active', 'last_run')
    list_filter = ('is_active', 'content_type')
    search_fields = ('name', 'site_url')
    actions = ['run_automation_now']

    def run_automation_now(self, request, queryset):
        for template in queryset:
            from .tasks import run_automation
            run_automation.delay(template.id)
        self.message_user(request, "Automation tasks have been scheduled to run.")
    run_automation_now.short_description = "Run selected automation templates now"
