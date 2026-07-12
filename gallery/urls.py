from django.urls import path

from . import views

app_name = "gallery"

urlpatterns = [
    path("galeri/", views.PhotoListView.as_view(), name="list"),
]
