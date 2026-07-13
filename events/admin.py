from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import Event, EventActivity


class EventActivityInline(TabularInline):
    model = EventActivity
    extra = 1
    fields = ("title", "order")
    ordering = ("order", "id")


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ("title", "category", "start_date", "location", "is_published")
    list_filter = ("category", "is_published")
    search_fields = ("title", "summary", "location")
    date_hierarchy = "start_date"
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}
    inlines = [EventActivityInline]
