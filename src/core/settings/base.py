"""Common settings and globals."""


from os.path import basename, join, normpath
from sys import path
from unipath import Path
from logging.handlers import SysLogHandler


# ######### PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = Path(__file__).ancestor(3)

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = DJANGO_ROOT.ancestor(1)

# Site name:
SITE_NAME = basename(SITE_ROOT)

# Path to the project Configuration app
CONFIGURATION_APP_ROOT = Path(__file__).ancestor(2)

# Path to public files (served by the web server)
PUBLIC_ROOT = SITE_ROOT.child('public')

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
path.append(CONFIGURATION_APP_ROOT)
# ######### END PATH CONFIGURATION


# ######### DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
# ######### END DEBUG CONFIGURATION


# ######### MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Matthieu Lamy', 'matthieu@talengi.fr'),
    ('Thibault Jouannic', 'thibault@jouannic.fr'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# ######### END MANAGER CONFIGURATION


# ######### DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(DJANGO_ROOT, 'phase.db')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
# ######### END DATABASE CONFIGURATION


# ######### GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/Paris'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# ######### END GENERAL CONFIGURATION


# ######### MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = PUBLIC_ROOT.child('media')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
# ######### END MEDIA CONFIGURATION


# ######### STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = PUBLIC_ROOT.child('static')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    DJANGO_ROOT.child('static'),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
# ######### END STATIC FILE CONFIGURATION


# ######### SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = r"This is a dummy secret key!"
# ######### END SECRET CONFIGURATION


# ######### FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    DJANGO_ROOT.child('fixtures'),
)
# ######### END FIXTURE CONFIGURATION


# ######### TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'accounts.context_processors.navigation',
    'notifications.context_processors.notifications',
    'reviews.context_processors.reviews',
    'dashboards.context_processors.dashboards',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    DJANGO_ROOT.child('templates'),
)
# ######### END TEMPLATE CONFIGURATION


# ######### MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    # Performance middlewares
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',

    # Default Django middleware.
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
# ######### END MIDDLEWARE CONFIGURATION


# ######### URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'core.urls'
# ######### END URL CONFIGURATION


# ######### APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Admin panel and documentation:
    'django.contrib.admin',
    # 'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    # Database migration helpers:
    'pipeline',
    'widget_tweaks',
    'crispy_forms',
    'rest_framework',
    'django_extensions',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'accounts',
    'categories',
    'documents',
    'discussion',
    'notifications',
    'reviews',
    'default_documents',
    'metadata',
    'favorites',
    'bootstrap',
    'restapi',
    'breadcrumbs',
    'imports',
    'search',
    'bookmarks',
    'transmittals',
    'dashboards',
    'privatemedia',
    'tools',
)

# Load custom documents
DOC_APPS = tuple()
try:
    import doc_apps
    DOC_APPS = getattr(doc_apps, 'DOC_APPS')
except:
    pass

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS + DOC_APPS
# ######### END APP CONFIGURATION


# ######### LOGGING CONFIGURATION
# See http://www.miximum.fr/bien-developper/876-an-effective-logging-strategy-with-django
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[phase] %(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        # Send info messages to syslog
        'syslog': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'facility': SysLogHandler.LOG_LOCAL2,
            'address': '/dev/log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        # This is the "catch all" logger
        '': {
            'handlers': ['console', 'syslog', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # We have to redefine this. See
        # http://stackoverflow.com/questions/20282521/django-request-logger-not-propagated-to-root
        'django.request': {
            'propagate': True,
        },
        'elasticsearch': {
            'handlers': ['console', 'syslog', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'elasticsearch.trace': {
            'handlers': ['syslog', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}
# ######### END LOGGING CONFIGURATION


# ######### WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'
# ######### END WSGI CONFIGURATION

# ######### PIPELINE CONFIGURATION
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE_DISABLE_WRAPPER = True

PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'css/phase-bootstrap.css',
            'css/jquery-ui.css',
            # must be loaded after jquery-ui js to avoid conflicts
            'css/datepicker.css',
            'css/project.css',
        ),
        'output_filename': 'css/base.css',
    },
    'detail': {
        'source_filenames': (
            'css/jquery.multiselect.css',
            'css/jquery.multiselect.filter.css',
            'css/selectize.css',
        ),
        'output_filename': 'css/detail.css',
    },
}

PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'js/vendor/jquery.js',
            'js/vendor/jquery-ui.min.js',
            # both bootstrap and bootstrap-datepicker must be loaded
            # after jquery-ui js to avoid conflicts
            'js/phase-bootstrap.js',
            'js/vendor/bootstrap-datepicker.js',
            'js/vendor/underscore.js',
            'js/vendor/backbone.js',
            'js/backbone-config.js',
            'js/events.js',
            'js/notifications/models.js',
            'js/notifications/collections.js',
            'js/notifications/views.js',
            'js/notifications/app.js',
            'js/ui/views.js',
            'js/ui/app.js',
        ),
        'output_filename': 'js/base.js',
    },
    'backbone': {
        'source_filenames': (
        ),
        'output_filename': 'js/backbone.js',
    },
    'list': {
        'source_filenames': (
            'js/vendor/jquery.inview.js',
            'js/querystring.js',
            'js/documents/models.js',
            'js/documents/collections.js',
            'js/documents/views.js',
            'js/favorites/models.js',
            'js/favorites/collections.js',
            'js/bookmarks/models.js',
            'js/bookmarks/collections.js',
            'js/bookmarks/views.js',
            'js/documents/routers.js',
            'js/documents/app.js',
        ),
        'output_filename': 'js/document-list.js',
    },
    'document_detail': {
        'source_filenames': (
            'js/vendor/jquery.multiselect.js',
            'js/vendor/jquery.multiselect.filter.js',
            'js/vendor/selectize.js',
            'js/autocomplete.js',
            'js/discussion/models.js',
            'js/discussion/collections.js',
            'js/discussion/views.js',
            'js/documents/routers.js',
            'js/documents/detail_app.js',
            'js/document-detail.js',
        ),
        'output_filename': 'js/document_detail.js',
    },
    'document_edit': {
        'source_filenames': (
            'js/vendor/jquery.multiselect.js',
            'js/vendor/jquery.multiselect.filter.js',
            'js/vendor/selectize.js',
            'js/autocomplete.js',
            'js/document-detail.js',
        ),
        'output_filename': 'js/document_edit.js',
    },
    'review_list': {
        'source_filenames': (
            'js/review-list.js',
        ),
        'output_filename': 'js/review-list.js',
    },
    'review': {
        'source_filenames': (
            'js/discussion/models.js',
            'js/discussion/collections.js',
            'js/discussion/views.js',
            'js/discussion/routers.js',
            'js/reviews/app.js',
        ),
        'output_filename': 'js/review.js',
    },
    'transmittal_list': {
        'source_filenames': (
            'js/transmittals/views.js',
            'js/transmittals/app.js',
        ),
        'output_filename': 'js/transmittal-list.js',
    },
}
# ######### END PIPELINE CONFIGURATION

# ######### EMAIL CONFIGURATION
DEFAULT_FROM_EMAIL = 'admin@phase.fr'
# ######### END EMAIL CONFIGURATION

# ######### API CONFIGURATION
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# ######### CELERY CONFIG
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERY_ACCEPT_CONTENT = ['betterjson']
CELERY_TASK_SERIALIZER = 'betterjson'
CELERY_RESULT_SERIALIZER = 'betterjson'
CELERY_RESULT_BACKEND = 'amqp'

# ######### SEARCH CONFIG
ELASTIC_HOSTS = [{'host': 'localhost', 'port': 9200}]
ELASTIC_INDEX = 'documents'
ELASTIC_BULK_SIZE = 150
ELASTIC_AUTOINDEX = True

# ######### CUSTOM CONFIGURATION
PAGINATE_BY = 50  # Document list pagination
API_PAGINATE_BY = 10
CACHE_TIMEOUT_SECONDS = 300  # seconds == 5 minutes
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'login'
CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = False
REVIEW_DURATION = 13
DISPLAY_NOTIFICATION_COUNT = 5

# Path to private files (must be served with X-SENDFILE)
PRIVATE_ROOT = SITE_ROOT.child('private')
PRIVATE_URL = '/private/'
NGING_X_ACCEL_PREFIX = '/xaccel/'
USE_X_SENDFILE = False

# Where to look for files to import?
IMPORT_ROOT = SITE_ROOT.child('import')

# ######### END CUSTOM CONFIGURATION
