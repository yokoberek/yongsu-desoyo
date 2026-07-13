from django.views.generic import ListView

from .models import Event


class EventListView(ListView):
    context_object_name = "events"
    queryset = Event.objects.filter(is_published=True)
