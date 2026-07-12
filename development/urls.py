from django.urls import path

from . import views

app_name = "development"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="list"),
]
