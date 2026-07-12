from django_project.settings.base import *  # noqa: F403
from decouple import config

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# https://docs.djangoproject.com/en/5.2/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# https://docs.djangoproject.com/en/5.2/ref/settings/#debug
DEBUG = config("DEBUG", cast=bool)

# https://docs.djangoproject.com/en/5.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# https://docs.djangoproject.com/en/5.2/ref/settings/#installed-apps
INSTALLED_APPS += [  # noqa: F405
    # 3rd-party
    "django_browser_reload",
    "debug_toolbar",
]

# https://docs.djangoproject.com/en/5.2/ref/settings/#middleware
MIDDLEWARE += [  # noqa: F405
    # 3rd-party
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

# https://docs.djangoproject.com/en/5.2/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# https://docs.djangoproject.com/en/5.2/ref/settings/#internal-ips
INTERNAL_IPS = [
    "127.0.0.1",
]
