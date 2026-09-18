from django.contrib import admin

from .models import Research, Article


@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "topic",
        "article_length",
        "tone",
        "status",
        "created_at",
    )
    list_filter = ("status", "article_length", "tone")
    search_fields = ("topic", "instructions")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "research",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "content")