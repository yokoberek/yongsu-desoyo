from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import Destination


@admin.register(Destination)
class DestinationAdmin(ModelAdmin):
    list_display = ("name", "category", "is_published", "created_at")
    list_filter = ("category", "is_published")
    search_fields = ("name", "summary", "description")
    prepopulated_fields = {"slug": ("name",)}
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}
