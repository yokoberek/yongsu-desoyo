from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("produk/", views.ProductListView.as_view(), name="list"),
]
