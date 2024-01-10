from django import forms
from django.forms import ModelForm, Textarea, CheckboxSelectMultiple, inlineformset_factory
from .models import *

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


ImagesFormSet = inlineformset_factory(Article, Image,
                                      fields=('image',),
                                      extra=1, max_num=3,
                                      widgets={'image_field': MultipleFileField(required=True)})


class ArticleForm(ModelForm):
    image_field = MultipleFileField(label='Изображения')

    class Meta:
        model = Article
        fields = ['title', 'anouncement', 'text', 'tags']
        labels = {
            'title': 'Заголовок',
            'tags': 'Тэги',
        }
        widgets = {
            'title': Textarea(attrs={'rows': 1, 'placeholder': 'Заголовок статьи', 'minlength': 5, 'maxlength': 50}),
            'anouncement': Textarea(attrs={'rows': 1, 'placeholder': 'Анонс статьи', 'minlength': 10, 'maxlength': 250}),
            'text': Textarea(attrs={'rows': 3, 'placeholder': 'Основной текст статьи', 'minlength': 10}),
            'tags': CheckboxSelectMultiple()
        }
