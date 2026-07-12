from django_project.settings.base import *  # noqa: F403
from decouple import config

# https://docs.djangoproject.com/en/5.2/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = config("SECRET_KEY")

# https://docs.djangoproject.com/en/5.2/ref/settings/#debug
DEBUG = config("DEBUG", cast=bool)

# https://docs.djangoproject.com/en/5.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")

# https://docs.djangoproject.com/en/5.2/ref/settings/#std-setting-CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="").split(",")

# https://docs.djangoproject.com/en/5.2/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = True

# https://docs.djangoproject.com/en/5.2/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# https://docs.djangoproject.com/en/5.2/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True

# https://docs.djangoproject.com/en/5.2/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

# https://docs.djangoproject.com/en/5.2/ref/middleware/#http-strict-transport-security
SECURE_HSTS_SECONDS = 31536000  # 1 tahun
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DATABASE"),
        "USER": config("POSTGRES_USERNAME"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    }
}

# https://github.com/rq/django-rq?tab=readme-ov-file#django-rq
# RQ_QUEUES = {
#     "default": {
#         "HOST": config("REDIS_HOST"),
#         "PORT": config("REDIS_PORT", cast=int),
#         "DB": config("REDIS_DATABASE", cast=int),
#         "PASSWORD": config("REDIS_PASSWORD"),
#         "DEFAULT_TIMEOUT": 360,
#     },
# }
# RQ_SHOW_ADMIN_LINK = True

# https://docs.djangoproject.com/en/5.2/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
