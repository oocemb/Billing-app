import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

ALLOWED_HOSTS = [
    "f994-176-59-44-40.eu.ngrok.io",
    "127.0.0.1",
]
CSRF_TRUSTED_ORIGINS = ['https://f994-176-59-44-40.eu.ngrok.io']

BILLING_BASE_URL = os.getenv("BILLING_BASE_URL", "http://127.0.0.1:5000/api/")
BILLING_CREATE_PAYMENT = BILLING_BASE_URL + os.getenv(
    "BILLING_CREATE_PAYMENT", "v1/payment/create/"
)
BILLING_PAYMENT_HISTORY = BILLING_BASE_URL + os.getenv(
    "BILLING_PAYMENT_HISTORY", "v1/user/<user_id>/purchase_history/"
)
BILLING_CANCEL_SUBSCRIPTION = BILLING_BASE_URL + os.getenv(
    "BILLING_PAYMENT_HISTORY", "v1/user/<user_id>/cancel_subscribe/"
)

BILLING_CALLBACK = BILLING_BASE_URL + os.getenv(
    "BILLING_CALLBACK", "v1/callback/<provider>/callback/"
)
BILLING_SUCCESS = BILLING_BASE_URL + os.getenv(
    "BILLING_SUCCESS", "v1/callback/<provider>/success/"
)
BILLING_FAIL = BILLING_BASE_URL + os.getenv(
    "BILLING_FAIL", "v1/callback/<provider>/fail/"
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "social_django",
    "api",
    "my_auth",
    "front_end",
]

AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
    "social_core.backends.vk.VKOAuth2",
    "social_core.backends.facebook.FacebookAppOAuth2",
    "social_core.backends.facebook.FacebookOAuth2",
)


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_VK_OAUTH2_KEY = env("VK_OAUTH2_KEY")
SOCIAL_AUTH_VK_OAUTH2_SECRET = env("VK_OAUTH2_SECRET")
SOCIAL_AUTH_FACEBOOK_KEY = env("FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = env("FACEBOOK_SECRET")


LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
SOCIAL_AUTH_VK_PROFILE_EXTRA_PARAMS = {
    "fields": "id, name, email",
}
SOCIAL_AUTH_FACEBOOK_SCOPE = ["email"]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    "fields": "id, name, email",
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "front_end.context_processors.getting_purchased_movies",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
