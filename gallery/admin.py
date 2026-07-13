from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Photo


@admin.register(Photo)
class PhotoAdmin(ModelAdmin):
    list_display = ("title", "order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title",)
