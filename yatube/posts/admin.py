from django.contrib import admin
from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Post.

    Отображает поля pk, text, author, group, pub_date.
    Включает возможность поиска по тексту и фильтрации по дате публикации.
    Поле group редактируемое в списке.
    """
    list_display = ('pk',
                    'text',
                    'author',
                    'group',
                    'pub_date',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    list_editable = ('group',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
