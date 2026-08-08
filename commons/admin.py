from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, StackedInline
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import (
    SECTIONS_WITH_FEATURE,
    ContactChannel,
    FastFact,
    HeroSlide,
    MissionPoint,
    OfficialPosition,
    PageBanner,
    PageSection,
    SectionFeature,
    SiteSettings,
    SocialLink,
    Statistic,
)


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


@admin.register(PageBanner)
class PageBannerAdmin(ModelAdmin):
    list_display = ("label", "key", "photo")
    search_fields = ("label", "key")
    readonly_fields = ("key",)
    autocomplete_fields = ("photo",)


class SectionFeatureInline(StackedInline):
    model = SectionFeature
    autocomplete_fields = ("photo", "photo_secondary")
    can_delete = False
    max_num = 1


@admin.register(PageSection)
class PageSectionAdmin(ModelAdmin):
    list_display = ("label", "page", "heading")
    list_filter = ("page",)
    search_fields = ("label", "key", "heading", "body")
    readonly_fields = ("key",)
    fields = ("key", "label", "eyebrow", "heading", "body")
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}

    def get_inlines(self, request, obj=None):
        """Panel foto/lencana/kutipan hanya untuk bagian yang templatenya merender."""
        return [SectionFeatureInline] if obj and obj.key in SECTIONS_WITH_FEATURE else []

    # Daftar bagian ditentukan template, bukan admin -- baris baru tidak akan tampil
    # di mana pun, dan baris yang hilang membuat judul bagian menghilang dari situs.
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    list_display = ("email", "phone_display")

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactChannel)
class ContactChannelAdmin(ModelAdmin):
    list_display = ("label", "line1", "line2", "order")
    list_editable = ("order",)
    readonly_fields = ("key",)


@admin.register(SocialLink)
class SocialLinkAdmin(ModelAdmin):
    list_display = ("label", "url", "order")
    list_editable = ("order",)
    readonly_fields = ("key",)


@admin.register(FastFact)
class FastFactAdmin(ModelAdmin):
    list_display = ("label", "value", "group", "order")
    list_editable = ("order",)
    list_filter = ("group",)


@admin.register(MissionPoint)
class MissionPointAdmin(ModelAdmin):
    list_display = ("text", "order")
    list_editable = ("order",)
