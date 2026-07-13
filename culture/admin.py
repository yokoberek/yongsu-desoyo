from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Tradition


@admin.register(Tradition)
class TraditionAdmin(ModelAdmin):
    list_display = ("name", "icon", "order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("name", "summary")
