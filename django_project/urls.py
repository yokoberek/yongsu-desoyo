from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("site-manager/", admin.site.urls),
    # URL publik flat & bersih; tiap app punya path Indonesia sendiri.
    path("", include("commons.urls")),
    path("", include("tourism.urls")),
    path("", include("products.urls")),
    path("", include("culture.urls")),
    path("", include("news.urls")),
    path("", include("events.urls")),
    path("", include("gallery.urls")),
    path("pembangunan/", include("development.urls")),
    path("ppid/", include("ppid.urls")),
]


if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    # Rute custom untuk debugging di development environment
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += debug_toolbar_urls()

    # Static dan Media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
