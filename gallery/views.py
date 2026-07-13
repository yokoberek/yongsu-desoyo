from django.views.generic import ListView

from .models import Photo


class PhotoListView(ListView):
    context_object_name = "photos"
    queryset = Photo.objects.filter(is_published=True)
