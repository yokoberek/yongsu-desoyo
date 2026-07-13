from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Event


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ("title", "category", "start_date", "location", "is_published")
    list_filter = ("category", "is_published")
    search_fields = ("title", "summary", "location")
    date_hierarchy = "start_date"
    prepopulated_fields = {"slug": ("title",)}
