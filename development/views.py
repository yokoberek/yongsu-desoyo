from django.views.generic import DetailView, ListView

from .models import Project


class ProjectListView(ListView):
    context_object_name = "projects"
    queryset = Project.objects.filter(is_published=True)


class ProjectDetailView(DetailView):
    context_object_name = "project"
    queryset = Project.objects.filter(is_published=True)
