from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "country", "author", "created_at", "views")
    search_fields = ("title", "country", "city_or_region", "short_description")
    list_filter = ("country", "created_at")
    prepopulated_fields = {"slug": ("title",)}
