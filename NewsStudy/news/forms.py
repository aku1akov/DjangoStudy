from django import forms
from django.core.validators import MinValueValidator
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple
from .models import Article
from django.utils.translation import gettext_lazy as _


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'anouncement', 'text', 'tags']
        labels = {
            "title": _("Заголовок"),
            "tags": _("Метки"),
        }
        widgets = {
            'title': Textarea(attrs={'rows': 1, 'placeholder': 'Заголовок статьи'}),
            'anouncement': Textarea(attrs={'rows': 1, 'placeholder': 'Анонс статьи'}),
            'text': Textarea(attrs={'rows': 3, 'placeholder': 'Основной текст статьи'}),
            'tags': CheckboxSelectMultiple(),
        }
