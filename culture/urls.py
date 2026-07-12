from django.urls import path

from . import views

app_name = "culture"

urlpatterns = [
    path("budaya/", views.TraditionListView.as_view(), name="list"),
]
