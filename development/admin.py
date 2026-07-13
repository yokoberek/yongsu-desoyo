from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import Project


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ("title", "status", "progress", "year", "is_published")
    list_filter = ("status", "is_published")
    search_fields = ("title", "summary", "description")
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}
