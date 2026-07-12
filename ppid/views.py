from django.views.generic import TemplateView


class PpidHomeView(TemplateView):
    template_name = "ppid/home.html"


class ProfileView(TemplateView):
    template_name = "ppid/profile.html"


class PublicInformationView(TemplateView):
    template_name = "ppid/public_information.html"


class InformationRequestView(TemplateView):
    template_name = "ppid/information_request.html"


class FaqView(TemplateView):
    template_name = "ppid/faq.html"
