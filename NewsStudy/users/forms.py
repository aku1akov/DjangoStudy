from django import forms
from .validators import allowed_email
from django.core.validators import MinLengthValidator


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100,
                           validators=[MinLengthValidator(2)],
                           empty_value='empty')
    email = forms.EmailField(validators=[allowed_email])
    message = forms.CharField(widget=forms.Textarea, disabled=True)
    demo = forms.BooleanField(help_text='help',
                              label='Демо',
                              initial=True,)

