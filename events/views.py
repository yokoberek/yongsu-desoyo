from django.views.generic import TemplateView


class EventListView(TemplateView):
    template_name = "events/event_list.html"
