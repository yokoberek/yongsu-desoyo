from django.views.generic import TemplateView


class TraditionListView(TemplateView):
    template_name = "culture/tradition_list.html"
