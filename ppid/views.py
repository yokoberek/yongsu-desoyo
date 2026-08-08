from django.views.generic import TemplateView

from .models import (
    FaqItem,
    InfoClassification,
    LegalBasis,
    PpidRole,
    PpidTask,
    RequestRequirement,
    RequestStep,
)


class PpidHomeView(TemplateView):
    template_name = "ppid/home.html"


class ProfileView(TemplateView):
    template_name = "ppid/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = PpidTask.objects.all()
        context["legal_basis"] = LegalBasis.objects.all()
        context["roles"] = PpidRole.objects.select_related("official")
        return context


class PublicInformationView(TemplateView):
    template_name = "ppid/public_information.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["classifications"] = InfoClassification.objects.prefetch_related("items")
        return context


class InformationRequestView(TemplateView):
    template_name = "ppid/information_request.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["steps"] = RequestStep.objects.all()
        context["requirements"] = RequestRequirement.objects.all()
        return context


class FaqView(TemplateView):
    template_name = "ppid/faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faq_items"] = FaqItem.objects.filter(is_published=True)
        return context
