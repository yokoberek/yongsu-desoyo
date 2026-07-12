from django.views.generic import TemplateView


class ProjectListView(TemplateView):
    template_name = "development/project_list.html"
