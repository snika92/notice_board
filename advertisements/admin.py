from django.contrib import admin

from .models import Advertisement, Review


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "author", "created_at")
    search_fields = ("title", "description")
    list_filter = ("author",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "advertisement", "created_at")
    search_fields = ("text",)
    list_filter = ("author", "advertisement")
