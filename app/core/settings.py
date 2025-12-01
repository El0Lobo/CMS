# app/core/settings.py
import os
from pathlib import Path

import environ

# --- Paths & env -------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Default env values; overridden by .env if present
env = environ.Env(
    DJANGO_ENV=(str, "production"),  # development, test, staging, production
    DJANGO_DEBUG=(bool, False),
    SECRET_KEY=(str, "unsafe-secret-key"),
    ALLOWED_HOSTS=(str, "localhost,127.0.0.1"),
    DATABASE_URL=(str, f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
    REDIS_URL=(str, "redis://localhost:6379/0"),
    CSRF_TRUSTED_ORIGINS=(str, ""),
)

# Load local .env if available
if os.path.exists(BASE_DIR / ".env"):
    environ.Env.read_env(BASE_DIR / ".env")

# --- Core Django settings ----------------------------------------------------
# Environment (like Rails RAILS_ENV) - separate from DEBUG flag
ENV = env("DJANGO_ENV")  # development, test, staging, production

DEBUG = env("DJANGO_DEBUG")
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = [h.strip() for h in env("ALLOWED_HOSTS").split(",") if h.strip()]
if ".trycloudflare.com" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(".trycloudflare.com")
CSRF_TRUSTED_ORIGINS = [u.strip() for u in env("CSRF_TRUSTED_ORIGINS").split(",") if u.strip()]
cloudflare_origin = "https://*.trycloudflare.com"
if cloudflare_origin not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(cloudflare_origin)

FIELD_ENCRYPTION_KEYS = [
    key.strip() for key in env("FIELD_ENCRYPTION_KEYS", default="").split(",") if key.strip()
]

_fallback_field_key = env("FIELD_ENCRYPTION_KEY", default="")
if not FIELD_ENCRYPTION_KEYS and _fallback_field_key:
    FIELD_ENCRYPTION_KEYS = [_fallback_field_key]

FIELD_ENCRYPTION_KEY = FIELD_ENCRYPTION_KEYS[0] if FIELD_ENCRYPTION_KEYS else ""

INSTALLED_APPS = [
    # Modeltranslation must be before django.contrib.admin
    "modeltranslation",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rosetta",
    "guardian",
    "axes",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_htmx",
    "django_ckeditor_5",
    "rest_framework",
    "auditlog",
    "rules",
    "crispy_forms",
    "crispy_bootstrap5",
    # Project apps
    "app.core",
    "app.api",
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
    "app.menu",
    "app.bands",
    "app.assets",
    "app.comms",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "app.core.middleware.NoStoreForCMSMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "axes.middleware.AxesMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "auditlog.middleware.AuditlogMiddleware",
    "app.users.middleware.ForcePasswordChangeMiddleware",
    "app.users.middleware.ImpersonateMiddleware",
]

ROOT_URLCONF = "app.core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "app" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Project
                "app.core.context_processors.sitecfg",
                "app.setup.context_processors.site_settings_context",
                "app.core.context_processors.inbox_status",
                "app.core.context_processors.site_languages",
            ],
        },
    }
]

WSGI_APPLICATION = "app.core.wsgi.application"

# Database
DATABASES = {"default": env.db()}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 10},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# i18n / tz
LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"  # Set to "Europe/Berlin" if you want EU defaults for currency guessing
USE_I18N = True
USE_TZ = True

# Supported languages for the site
LANGUAGES = [
    ("en", "English"),
    ("es", "Español"),
    ("de", "Deutsch"),
    ("fr", "Français"),
]

# Where Django looks for translation files
LOCALE_PATHS = [BASE_DIR / "locale"]

# Modeltranslation settings
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_LANGUAGES = ("en", "es", "de", "fr")
MODELTRANSLATION_FALLBACK_LANGUAGES = ("en",)
MODELTRANSLATION_PREPOPULATE_LANGUAGE = "en"
MODELTRANSLATION_AUTO_POPULATE = True

# Static / media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "app" / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# WYSIWYG / CKEditor 5
CKEDITOR_5_CONFIGS = {
    "default": {
        "language": "en",
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "underline",
            "strikethrough",
            "link",
            "|",
            "bulletedList",
            "numberedList",
            "outdent",
            "indent",
            "|",
            "blockQuote",
            "codeBlock",
            "insertTable",
            "mediaEmbed",
            "undo",
            "redo",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:inline",
                "imageStyle:block",
                "imageStyle:side",
            ]
        },
        "table": {
            "contentToolbar": ["tableColumn", "tableRow", "mergeTableCells"],
        },
        "mediaEmbed": {"previewsInData": True},
    },
}
CKEDITOR_5_UPLOAD_FILE_TYPES = [
    "jpeg",
    "jpg",
    "png",
    "gif",
    "webp",
    "svg",
    "bmp",
    "tiff",
    "pdf",
    "txt",
    "doc",
    "docx",
    "odt",
]
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"

# Whitenoise + default file storage
STORAGES = {
    "default": {  # used for uploads (ImageField/FileField)
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        # (optional) explicitly wire to MEDIA_*; defaults already read these:
        # "OPTIONS": {"location": MEDIA_ROOT, "base_url": MEDIA_URL},
    },
    "staticfiles": {  # used for collectstatic
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
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
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
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

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
}

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
