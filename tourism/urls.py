from django.urls import path

from . import views

app_name = "tourism"

urlpatterns = [
    path("wisata/", views.DestinationListView.as_view(), name="list"),
]
