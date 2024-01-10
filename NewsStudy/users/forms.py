from django import forms
from .validators import allowed_email
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, FileInput, DateInput
from .models import Profile
from datetime import date


class UserAddForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',
                               validators=[MinLengthValidator(5), MaxLengthValidator(30)],
                               required=True,
                               help_text='<ul><li>От 5 до 30 символов</li>'
                                         '<li>Только буквы, цифры и символы @/./+/-/_.</li></ul>',
                               min_length=5, max_length=30)

    # email = forms.EmailField(label='Адрес электронной почты',
    #                          validators=[EmailValidator, allowed_email],
    #                          required=False,
    #                          help_text='Разрешены адреса из доменов:'
    #                                    '<ul><li>@rt.ru</li>'
    #                                    '<li>@nw.rt.ru</li></ul>')

    class Meta:
        model = User
        fields = ['username',
                  # 'email',
                  'password1',
                  'password2']


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email',
                                                            'placeholder': 'example@rt.ru'}),
                             validators=[EmailValidator, allowed_email],
                             required=False)

    class Meta:
        model = User

        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {'username': TextInput({'class': 'textinput form-control newinput',
                                          'placeholder': 'username',
                                          'id': 'inputformcolor'}),
                   'first_name': TextInput({'class': 'textinput form-control',
                                            'placeholder': 'Имя'}),
                   'last_name': TextInput({'class': 'textinput form-control',
                                           'placeholder': 'Фамилия'}),
                   }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile

        fields = ['website', 'github', 'phone', 'image', 'birthdate']
        widgets = {'website': TextInput({'class': 'form-control', 'type': 'url',
                                         'placeholder': 'https://example.com'}),
                   'github': TextInput({'class': 'form-control', 'type': 'url',
                                        'placeholder': 'https://github.com/user'}),
                   'birthdate': DateInput(format='%Y-%m-%d',
                                          attrs={'class': 'form-control',
                                                 'type': 'date',
                                                 'max': date.today()}),
                   'phone': TextInput({'class': 'form-control', 'type': 'tel',
                                       'placeholder': '+7 912 345-67-89', 'title': 'Формат: +7 912 345-67-89',
                                       'pattern': '\+7 [0-9]{3} [0-9]{3}-[0-9]{2}-[0-9]{2}'}),
                   'image': FileInput({'class': 'form-control',
                                       'placeholder': 'Картинка'})}


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100,
                           validators=[MinLengthValidator(2)],
                           empty_value='empty')
    email = forms.EmailField(validators=[allowed_email])
    message = forms.CharField(widget=forms.Textarea, disabled=True)
    demo = forms.BooleanField(help_text='help',
                              label='Демо',
                              initial=True, )
