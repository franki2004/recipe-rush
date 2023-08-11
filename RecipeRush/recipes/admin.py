from django.contrib import admin
from .models import Recipe, Likes, Comment


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at')
    list_filter = ('category', 'author')
    search_fields = ('title', 'author__username')
    ordering = ('-created_at',)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__title')
    ordering = ('-user',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenter_name', 'recipe', 'timestamp')
    list_filter = ('commenter_name', 'recipe')
    search_fields = ('commenter_name__username', 'recipe__title')
    ordering = ('-timestamp',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Likes, LikeAdmin)
admin.site.register(Recipe, RecipeAdmin)
