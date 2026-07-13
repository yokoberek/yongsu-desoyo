from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("acara/", views.EventListView.as_view(), name="list"),
    path("acara/<slug:slug>/", views.EventDetailView.as_view(), name="detail"),
]
