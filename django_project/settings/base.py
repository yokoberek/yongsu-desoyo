from pathlib import Path
from decouple import config
from django.templatetags.static import static
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition
# https://docs.djangoproject.com/en/5.2/ref/settings/#installed-apps
INSTALLED_APPS = [
    # 3rd-party apps for django-unfold
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    # Built-in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.humanize",  # Added for humanize filter
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # 3rd-party app
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    # 3rd-party apps
    "tailwind",
    "theme",
    # Local apps
    "commons.apps.CommonsConfig",
    "tourism.apps.TourismConfig",
    "products.apps.ProductsConfig",
    "culture.apps.CultureConfig",
    "news.apps.NewsConfig",
    "events.apps.EventsConfig",
    "gallery.apps.GalleryConfig",
    "development.apps.DevelopmentConfig",
    "ppid.apps.PpidConfig",
]

# Middleware
# https://docs.djangoproject.com/en/5.2/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # 3rd-party
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# https://docs.djangoproject.com/en/5.2/ref/settings/#root-urlconf
ROOT_URLCONF = "django_project.urls"

# Templates
# https://docs.djangoproject.com/en/5.2/ref/models/fields/#bigautofield
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "commons.context_processors.site_settings",
            ],
        },
    },
]

# https://docs.djangoproject.com/en/5.2/ref/settings/#wsgi-application
WSGI_APPLICATION = "django_project.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = "id-id"

# https://docs.djangoproject.com/en/5.2/ref/settings/#time-zone
TIME_ZONE = "Asia/Jayapura"

# https://docs.djangoproject.com/en/5.2/ref/settings/#std:setting-USE_I18N
USE_I18N = True

# https://docs.djangoproject.com/en/5.2/ref/settings/#use-l10n
USE_L10N = True  # Mengaktifkan lokalalisasi format data

# https://docs.djangoproject.com/en/5.2/ref/settings/#use-tz
USE_TZ = True

# https://whitenoise.readthedocs.io/en/latest/django.html
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# https://docs.djangoproject.com/en/5.2/ref/settings/#media-url
MEDIA_URL = "/media/"

# https://docs.djangoproject.com/en/5.2/ref/settings/#media-root
MEDIA_ROOT = BASE_DIR / "mediafiles"  # noqa: F405

# https://docs.djangoproject.com/en/5.2/ref/settings/#static-root

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa: F405
STATICFILES_DIRS = [BASE_DIR / "static"]  # noqa: F405

# https://docs.djangoproject.com/en/5.2/ref/contrib/sites/#enabling-the-sites-framework
SITE_ID = 1

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-user-model
# AUTH_USER_MODEL = "accounts.User"

# https://docs.djangoproject.com/en/5.2/ref/settings/#std-setting-LOGIN_URL
# LOGIN_URL = "accounts:login"
# LOGIN_REDIRECT_URL = "contacts:dashboard"
# LOGOUT_REDIRECT_URL = "accounts:login"

# https://docs.djangoproject.com/en/5.2/ref/settings/#email-backend
# EMAIL_HOST = config("EMAIL_HOST")
# EMAIL_PORT = config("EMAIL_PORT")
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = config("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

# Django-tailwind config
# https://django-tailwind.readthedocs.io/en/latest/installation.html#installation
TAILWIND_APP_NAME = "theme"


# Unfold config
# https://unfoldadmin.com/docs/configuration/settings/
UNFOLD = {
    # ── Site identity ────────────────────────────────────────────────────────
    "SITE_TITLE": "Site Administration - Kampung Yongsu Desoyo",
    "SITE_HEADER": "Yongsu Desoyo",
    "SITE_SUBHEADER": "Distrik Ravenirara, Kab. Jayapura",
    "SITE_URL": "/",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda _request: static("favicon/favicon.ico"),
        },
    ],
    # ── Appearance ───────────────────────────────────────────────────────────
    "SHOW_BACK_BUTTON": True,
    "THEME": "light",
    "BORDER_RADIUS": "8px",
    "COLORS": {
        "base": {
            "50": "250, 250, 250",
            "100": "245, 245, 245",
            "200": "229, 229, 229",
            "300": "212, 212, 212",
            "400": "163, 163, 163",
            "500": "115, 115, 115",
            "600": "82, 82, 82",
            "700": "64, 64, 64",
            "800": "38, 38, 38",
            "900": "23, 23, 23",
            "950": "10, 10, 10",
        },
        "primary": {
            "50": "250, 250, 250",
            "100": "245, 245, 245",
            "200": "229, 229, 229",
            "300": "212, 212, 212",
            "400": "163, 163, 163",
            "500": "115, 115, 115",
            "600": "82, 82, 82",
            "700": "64, 64, 64",
            "800": "38, 38, 38",
            "900": "23, 23, 23",
            "950": "10, 10, 10",
        },
    },
    # ── Sidebar navigation ───────────────────────────────────────────────────
    "SIDEBAR": {
        "navigation": [
            {
                "title": "Beranda & Profil",
                "separator": False,
                "collapsible": False,
                "items": [
                    {
                        "title": "Hero Slide",
                        "icon": "view_carousel",
                        "link": reverse_lazy("admin:commons_heroslide_changelist"),
                    },
                    {
                        "title": "Banner Halaman",
                        "icon": "wallpaper",
                        "link": reverse_lazy("admin:commons_pagebanner_changelist"),
                    },
                    {
                        "title": "Teks Bagian Halaman",
                        "icon": "auto_stories",
                        "link": reverse_lazy("admin:commons_pagesection_changelist"),
                    },
                    {
                        "title": "Struktur Pemerintahan",
                        "icon": "account_balance",
                        "link": reverse_lazy(
                            "admin:commons_officialposition_changelist"
                        ),
                    },
                    {
                        "title": "Statistik",
                        "icon": "monitoring",
                        "link": reverse_lazy("admin:commons_statistic_changelist"),
                    },
                    {
                        "title": "Fakta Singkat",
                        "icon": "fact_check",
                        "link": reverse_lazy("admin:commons_fastfact_changelist"),
                    },
                    {
                        "title": "Poin Misi",
                        "icon": "checklist",
                        "link": reverse_lazy("admin:commons_missionpoint_changelist"),
                    },
                    {
                        "title": "Kanal Kontak",
                        "icon": "call",
                        "link": reverse_lazy("admin:commons_contactchannel_changelist"),
                    },
                    {
                        "title": "Tautan Sosial Media",
                        "icon": "share",
                        "link": reverse_lazy("admin:commons_sociallink_changelist"),
                    },
                    {
                        "title": "Pengaturan Situs",
                        "icon": "settings",
                        "link": reverse_lazy("admin:commons_sitesettings_changelist"),
                    },
                ],
            },
            {
                "title": "Konten Kampung",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Objek Wisata",
                        "icon": "landscape",
                        "link": reverse_lazy("admin:tourism_destination_changelist"),
                    },
                    {
                        "title": "Produk Lokal",
                        "icon": "storefront",
                        "link": reverse_lazy("admin:products_product_changelist"),
                    },
                    {
                        "title": "Budaya & Tradisi",
                        "icon": "diversity_3",
                        "link": reverse_lazy("admin:culture_tradition_changelist"),
                    },
                    {
                        "title": "Galeri Foto",
                        "icon": "photo_library",
                        "link": reverse_lazy("admin:gallery_photo_changelist"),
                    },
                ],
            },
            {
                "title": "Informasi & Kegiatan",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Berita & Pengumuman",
                        "icon": "article",
                        "link": reverse_lazy("admin:news_post_changelist"),
                    },
                    {
                        "title": "Acara & Kegiatan",
                        "icon": "event",
                        "link": reverse_lazy("admin:events_event_changelist"),
                    },
                ],
            },
            {
                "title": "Pembangunan",
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": "Program & Proyek",
                        "icon": "construction",
                        "link": reverse_lazy("admin:development_project_changelist"),
                    },
                ],
            },
            {
                "title": "Manajemen Pengguna",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Pengguna",
                        "icon": "manage_accounts",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": "Grup & Hak Akses",
                        "icon": "shield_person",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": "Sistem",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Pengaturan Situs",
                        "icon": "language",
                        "link": reverse_lazy("admin:sites_site_changelist"),
                    },
                ],
            },
        ],
    },
}
