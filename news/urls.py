from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("berita/", views.PostListView.as_view(), name="list"),
]
