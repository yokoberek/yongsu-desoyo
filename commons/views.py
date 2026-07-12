from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "commons/index.html"


class AboutView(TemplateView):
    template_name = "commons/about.html"


class ContactView(TemplateView):
    template_name = "commons/contact.html"


class StatisticsView(TemplateView):
    template_name = "commons/statistics.html"
