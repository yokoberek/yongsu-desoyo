from django.urls import path

from . import views

app_name = "commons"

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("tentang/", views.AboutView.as_view(), name="about"),
    path("kontak/", views.ContactView.as_view(), name="contact"),
    path("statistik/", views.StatisticsView.as_view(), name="statistics"),
]
