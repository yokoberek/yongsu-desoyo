from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import HeroSlide, OfficialPosition, Statistic


@admin.register(Statistic)
class StatisticAdmin(ModelAdmin):
    list_display = ("label", "value", "order", "is_published")
    list_editable = ("value", "order")
    list_filter = ("is_published",)


@admin.register(HeroSlide)
class HeroSlideAdmin(ModelAdmin):
    list_display = ("title", "caption", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "subtitle", "caption")


@admin.register(OfficialPosition)
class OfficialPositionAdmin(ModelAdmin):
    list_display = ("position", "group", "name", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("group", "is_published")
    search_fields = ("position", "name")
