from django import forms
from django.core.validators import MinValueValidator
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple
from .models import Article
from django.utils.translation import gettext_lazy as _


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ArticleForm(ModelForm):
    image_field = MultipleFileField()

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
