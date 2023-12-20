from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# class Account(models.Model):
#     gender_choices = (('M', 'Male'),
#                       ('F', 'Female'),
#                       ('N/A', 'Not answered'))
#     user = models.OneToOneField(User, on_delete=models.CASCADE,
#                                 primary_key=True)
#     nickname = models.CharField(max_length=100)
#     birthdate = models.DateField(null=True)
#     gender = models.CharField(choices=gender_choices, max_length=20)
#     acc_image = models.ImageField(default='default.png',
#                                   upload_to='acc_images')
#
#     def __str__(self):
#         return f"{self.user.username}'s account"


class Profile(models.Model):
    gender_choices = (('M', 'Male'), ('F', "Female"))
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, verbose_name='Пользователь')
    nickname = models.CharField(verbose_name='Никнейм', max_length=100)
    birthdate = models.DateField(verbose_name='Дата рождения', null=True)
    gender = models.CharField(verbose_name='Пол', choices=gender_choices, max_length=20)
    image = models.ImageField(verbose_name='Картинка', default='default.png',
                              upload_to='profile_img')

    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили пользователей'

