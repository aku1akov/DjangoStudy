from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .models import *
# Register your models here.


@admin.register(FavoriteArticle)
class FavoriteArticleAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'article',
                    'date']
    list_filter = ['user']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'article_count',
                    'comment_count',
                    'image_tag']
    list_filter = ['user']
    list_per_page = 5

    @admin.display(description='Новостей')
    def article_count(self, profile: Profile):
        return profile.art_count()

    @admin.display(description='Комментариев')
    def comment_count(self, profile: Profile):
        return profile.com_count()


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    list_display = ['name', 'users_count']

    @admin.display(description='Количество пользователей')
    def users_count(self, obj):
        return User.objects.filter(groups=obj).count()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_staff', 'get_groups']
    list_filter = ['is_staff', 'groups']
    actions = ['set_author', 'set_reader']

    @admin.display(description='Группа')
    def get_groups(self, obj):
        return ' '.join(g.name for g in obj.groups.all())

    @admin.action(description='Предоставить права автора')
    def set_author(self, request, queryset):
        group = Group.objects.get(name='Author')
        for user in queryset:
            user.groups.clear()
            user.groups.add(group)
        self.message_user(request, 'Выбранным пользователям были назначены права автора')

    @admin.action(description='Предоставить права читателя')
    def set_reader(self, request, queryset):
        group = Group.objects.get(name='Reader')
        for user in queryset:
            user.groups.clear()
            user.groups.add(group)
        self.message_user(request, 'Выбранным пользователям были назначены права читателя')
