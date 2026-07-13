from django.views.generic import ListView

from .models import Tradition


class TraditionListView(ListView):
    context_object_name = "traditions"
    queryset = Tradition.objects.filter(is_published=True)
