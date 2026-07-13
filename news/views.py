from django.views.generic import DetailView, ListView

from .models import Post


class PostListView(ListView):
    context_object_name = "posts"
    queryset = Post.objects.filter(is_published=True)


class PostDetailView(DetailView):
    context_object_name = "post"
    queryset = Post.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_posts"] = (
            Post.objects.filter(is_published=True).exclude(pk=self.object.pk)[:5]
        )
        return context
