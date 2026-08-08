from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    FaqItem,
    InfoClassification,
    InfoClassificationItem,
    LegalBasis,
    PpidRole,
    PpidTask,
    RequestRequirement,
    RequestStep,
)


@admin.register(PpidTask)
class PpidTaskAdmin(ModelAdmin):
    list_display = ("text", "order")
    list_editable = ("order",)


@admin.register(LegalBasis)
class LegalBasisAdmin(ModelAdmin):
    list_display = ("text", "order")
    list_editable = ("order",)


@admin.register(PpidRole)
class PpidRoleAdmin(ModelAdmin):
    list_display = ("role_label", "official", "order")
    list_editable = ("order",)
    autocomplete_fields = ("official",)


class InfoClassificationItemInline(TabularInline):
    model = InfoClassificationItem
    extra = 1
    fields = ("text", "order")
    ordering = ("order", "id")


@admin.register(InfoClassification)
class InfoClassificationAdmin(ModelAdmin):
    list_display = ("title", "badge_letter", "order")
    list_editable = ("order",)
    inlines = [InfoClassificationItemInline]


@admin.register(RequestStep)
class RequestStepAdmin(ModelAdmin):
    list_display = ("title", "description", "order")
    list_editable = ("order",)


@admin.register(RequestRequirement)
class RequestRequirementAdmin(ModelAdmin):
    list_display = ("text", "order")
    list_editable = ("order",)


@admin.register(FaqItem)
class FaqItemAdmin(ModelAdmin):
    list_display = ("question", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("question", "answer")
