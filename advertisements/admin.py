from django.contrib import admin

from .models import Advertisement, Comment


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "price", "author", "created_at")
    search_fields = ("title", "description")
    list_filter = ("author",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "advertisement", "created_at")
    search_fields = ("text",)
    list_filter = ("author", "advertisement")
