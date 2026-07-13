from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from development.models import Project
from news.models import Post
from products.models import Product
from tourism.models import Destination


class StaticViewSitemap(Sitemap):
    """Halaman statis (tanpa model): beranda, profil, katalog, dan PPID."""

    def items(self):
        return [
            "commons:index",
            "commons:about",
            "commons:contact",
            "commons:statistics",
            "tourism:list",
            "products:list",
            "culture:list",
            "news:list",
            "events:list",
            "gallery:list",
            "development:list",
            "ppid:index",
            "ppid:profile",
            "ppid:information",
            "ppid:request",
            "ppid:faq",
        ]

    def location(self, item):
        return reverse(item)

    def changefreq(self, item):
        return "daily" if item == "commons:index" else "monthly"

    def priority(self, item):
        return 1.0 if item == "commons:index" else 0.6


class DestinationSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Destination.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Product.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Project.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at


sitemaps = {
    "static": StaticViewSitemap,
    "destinations": DestinationSitemap,
    "products": ProductSitemap,
    "posts": PostSitemap,
    "projects": ProjectSitemap,
}
