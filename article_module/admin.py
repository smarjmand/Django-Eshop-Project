from django.contrib import admin
from .models import ArticleCategory, Articles, ArticleComments


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent_category','url_title', 'is_active']
    list_editable = ['parent_category', 'is_active']


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'is_active']
    list_editable = ['is_active']

    def save_model(self, request, obj, form, change):
        if change:
            obj.author = request.user
        return super().save_model(request, obj, form, change)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['article', 'parent', 'user', 'is_active']
    list_editable = ['is_active']


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Articles, ArticlesAdmin)
admin.site.register(ArticleComments, CommentsAdmin)
