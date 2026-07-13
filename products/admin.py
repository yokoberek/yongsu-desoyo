from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import Product


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("name", "category", "producer", "price_note", "is_published")
    list_filter = ("category", "is_published")
    search_fields = ("name", "producer", "summary", "description")
    prepopulated_fields = {"slug": ("name",)}
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}
