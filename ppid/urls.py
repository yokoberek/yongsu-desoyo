from django.urls import path

from . import views

app_name = "ppid"

urlpatterns = [
    path("", views.PpidHomeView.as_view(), name="index"),
    path("profil/", views.ProfileView.as_view(), name="profile"),
    path("informasi/", views.PublicInformationView.as_view(), name="information"),
    path("permohonan/", views.InformationRequestView.as_view(), name="request"),
    path("faq/", views.FaqView.as_view(), name="faq"),
]
