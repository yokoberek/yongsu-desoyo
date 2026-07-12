from django.views.generic import TemplateView


class DestinationListView(TemplateView):
    template_name = "tourism/destination_list.html"
