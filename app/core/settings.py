# app/core/settings.py
import os
from pathlib import Path
import environ

# --- Paths & env -------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Default env values; overridden by .env if present
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    SECRET_KEY=(str, "unsafe-secret-key"),
    ALLOWED_HOSTS=(str, "localhost,127.0.0.1"),
    DATABASE_URL=(str, f"sqlite:///{BASE_DIR/'db.sqlite3'}"),
    REDIS_URL=(str, "redis://localhost:6379/0"),
    CSRF_TRUSTED_ORIGINS=(str, ""),
)

# Load local .env if available
if os.path.exists(BASE_DIR / ".env"):
    environ.Env.read_env(BASE_DIR / ".env")

# --- Core Django settings ----------------------------------------------------
DEBUG = env("DJANGO_DEBUG")
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = [h.strip() for h in env("ALLOWED_HOSTS").split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [u.strip() for u in env("CSRF_TRUSTED_ORIGINS").split(",") if u.strip()]

FIELD_ENCRYPTION_KEYS = [
    key.strip()
    for key in env("FIELD_ENCRYPTION_KEYS", default="").split(",")
    if key.strip()
]

_fallback_field_key = env("FIELD_ENCRYPTION_KEY", default="")
if not FIELD_ENCRYPTION_KEYS and _fallback_field_key:
    FIELD_ENCRYPTION_KEYS = [_fallback_field_key]

FIELD_ENCRYPTION_KEY = FIELD_ENCRYPTION_KEYS[0] if FIELD_ENCRYPTION_KEYS else ""

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "guardian",
    "axes",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_htmx",

    # Project apps
    "app.core",
    "app.pages",
    "app.cms",
    "app.blog",
    "app.events",
    "app.shifts",
    "app.door",
    "app.pos",
    "app.merch",
    "app.inventory",
    "app.accounting",
    "app.social",
    "app.automation",
    "app.maps",
    "app.publicthemes",
    "app.setup",
    "app.users",
    'app.menu',
    "app.bands",  
    "app.assets",
    "app.comms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  
    "django.contrib.sessions.middleware.SessionMiddleware",
    "app.core.middleware.NoStoreForCMSMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "axes.middleware.AxesMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "app.users.middleware.ForcePasswordChangeMiddleware",
    "app.users.middleware.ImpersonateMiddleware", 
]

ROOT_URLCONF = "app.core.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "app" / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request", 
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
            # Project
            "app.core.context_processors.sitecfg",
            "app.setup.context_processors.site_settings_context",
            "app.core.context_processors.inbox_status",
        ],
    },
}]

WSGI_APPLICATION = "app.core.wsgi.application"

# Database
DATABASES = {"default": env.db()}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# i18n / tz
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"  # Set to "Europe/Berlin" if you want EU defaults for currency guessing
USE_I18N = True
USE_TZ = True

# Static / media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "app" / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Whitenoise + default file storage
STORAGES = {
    "default": {  # used for uploads (ImageField/FileField)
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        # (optional) explicitly wire to MEDIA_*; defaults already read these:
        # "OPTIONS": {"location": MEDIA_ROOT, "base_url": MEDIA_URL},
    },
    "staticfiles": {  # used for collectstatic
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Celery / Redis
CELERY_BROKER_URL = env("REDIS_URL")
CELERY_RESULT_BACKEND = env("REDIS_URL")

# Axes (lockout)
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1

# Security
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False if DEBUG else True
CSRF_COOKIE_SECURE = False if DEBUG else True
X_FRAME_OPTIONS = "DENY"

# Auth redirects
LOGIN_REDIRECT_URL = "/cms/dashboard/"
LOGOUT_REDIRECT_URL = "/"

# Impersonate redirects
IMPERSONATE_SESSION_KEY = "impersonate_user_id"
IMPERSONATOR_SESSION_KEY = "impersonator_user_id"

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Auth backends (order matters)
AUTHENTICATION_BACKENDS = (
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)


