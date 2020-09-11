from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.utils import get_attachment_model
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'posts_number',)
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('post_set')

    def posts_number(self, obj):
        return obj.post_set.all().count()


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'posts_count',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('post_author')

    def posts_count(self, obj):
        count = obj.post_author.all().count()
        link = f'/admin/blog/post/?author__id__exact={obj.id}'
        return format_html(
            f'<a href="{link}" target="_blank">{count} posts</a>')



@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'created', 'moderated', 'image_admin',)
    list_editable = ('moderated',)
    readonly_fields = ('slug',)
    search_fields = ('name',)
    ordering = ('-published',)
    summernote_fields = ('content',)

    def image_admin(self, obj):
        return format_html('<img src="{}" style="max-width: 150px" />',
                           obj.image.url)


admin.site.unregister(get_attachment_model())
admin.site.site_header = 'Admin panel for futureprooof test blog'
