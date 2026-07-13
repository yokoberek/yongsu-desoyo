from django.views.generic import DetailView, ListView

from .models import Event


class EventListView(ListView):
    context_object_name = "events"
    queryset = Event.objects.filter(is_published=True)


class EventDetailView(DetailView):
    context_object_name = "event"
    queryset = Event.objects.filter(is_published=True).prefetch_related("activities")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["other_events"] = (
            Event.objects.filter(is_published=True).exclude(pk=self.object.pk)[:5]
        )
        return context
