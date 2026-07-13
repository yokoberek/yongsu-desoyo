from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import Post


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ("title", "category", "published_at", "is_published")
    list_filter = ("category", "is_published")
    search_fields = ("title", "summary", "body")
    date_hierarchy = "published_at"
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}
