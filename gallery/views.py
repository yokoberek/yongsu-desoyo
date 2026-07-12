from django.views.generic import TemplateView


class PhotoListView(TemplateView):
    template_name = "gallery/photo_list.html"
