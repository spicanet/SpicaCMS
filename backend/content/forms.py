# backend/content/forms.py

from django import forms
from django_celery_beat.models import CrontabSchedule
from .models import AutomationTemplate

class AutomationTemplateForm(forms.ModelForm):
    class Meta:
        model = AutomationTemplate
        fields = '__all__'
        widgets = {
            'ai_prompt': forms.Textarea(attrs={'rows': 4}),
        }
