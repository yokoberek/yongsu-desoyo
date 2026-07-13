from django.views.generic import DetailView, ListView

from .models import Destination


class DestinationListView(ListView):
    context_object_name = "destinations"
    queryset = Destination.objects.filter(is_published=True)


class DestinationDetailView(DetailView):
    context_object_name = "destination"
    queryset = Destination.objects.filter(is_published=True)
