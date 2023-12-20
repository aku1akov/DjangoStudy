from django.contrib import admin
from .models import *
# Register your models here.


# class AccountAdmin(admin.ModelAdmin):
#     list_display = ['user', 'gender', 'acc_image']
#     list_filter = ['user', 'gender']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'image']
    list_filter = ['user', 'gender']


# admin.site.register(Account, AccountAdmin)
admin.site.register(Profile, ProfileAdmin)
