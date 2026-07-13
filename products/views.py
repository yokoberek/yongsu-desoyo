from django.views.generic import DetailView, ListView

from .models import Product


class ProductListView(ListView):
    context_object_name = "products"

    def get_queryset(self):
        queryset = Product.objects.filter(is_published=True)
        category = self.request.GET.get("kategori")
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Product.Category.choices
        context["active_category"] = self.request.GET.get("kategori", "")
        return context


class ProductDetailView(DetailView):
    context_object_name = "product"
    queryset = Product.objects.filter(is_published=True)
