from pathlib import Path
import os 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

from decouple import config

STRIPE_TEST_PUBLIC_KEY = config('STRIPE_TEST_PUBLIC_KEY')
STRIPE_TEST_SECRET_KEY = config('STRIPE_TEST_SECRET_KEY')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-in(43*hkeezn*7g%p$%5@#n0n(#2$&m%97u4=s=!*op#sck2+!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ecom-project-qt91.onrender.com', '127.0.0.1', 'yummytummies-backend.onrender.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'user_management',
	'product_management',
	'browse_management',
	'cart_management',
	'checkout_management',
	'api_management',
    'contact_us',

	'rest_framework',
    'corsheaders',
    
    #for api documentation
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:3000',  # Add your frontend origin here
    'http://localhost:3000',  # Add if needed
    'https://yummytummies.onrender.com', #deployed fronted
]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",  # React app origin
    "http://localhost:3000",
    'https://yummytummies.onrender.com', #deployed fronted
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'ecom_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
			'browse_management/html_templates',
			'api_management/html_templates',
			'checkout_management/html_templates',
			'cart_management/html_templates',
			'product_management/html_templates',
			'user_management/templates/user_management',
		],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neondb',  # Database name
        'USER': 'neondb_owner',  # User for the database
        'PASSWORD': 'npg_s5XLyrzb2fDx',  # Password for the database
        'HOST': 'ep-dark-dawn-a2hjfd5l-pooler.eu-central-1.aws.neon.tech',  # Host for NeonDB
        'PORT': '5432',  # Default PostgreSQL port
        'OPTIONS': {
            'sslmode': 'require',  # Ensures secure SSL connection
        },
    }
}
"""
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#AUTHENTICATION MECHANISMS
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Or another permission class
    ],
}

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#AUTH_USER_MODEL = 'user_management.User'
