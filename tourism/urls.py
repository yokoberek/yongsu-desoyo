from django.urls import path

from . import views

app_name = "tourism"

urlpatterns = [
    path("wisata/", views.DestinationListView.as_view(), name="list"),
    path("wisata/<slug:slug>/", views.DestinationDetailView.as_view(), name="detail"),
]
