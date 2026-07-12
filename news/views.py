from django.views.generic import TemplateView


class PostListView(TemplateView):
    template_name = "news/post_list.html"
