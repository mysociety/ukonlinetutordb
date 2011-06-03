# Django settings for ukonlinetutordb project.

import logging
logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
)

# Some special mysociety preamble in order to get hold of our config
# file conf/general
import os
import sys
package_dir = os.path.abspath(os.path.split(__file__)[0])

paths = (
    os.path.normpath(package_dir + "/../../pylib"),
    os.path.normpath(package_dir + "/../../pylib/ukotdb-app"),
    os.path.normpath(package_dir + "/../../commonlib/pylib"),
    )

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

try:
    from config_local import config  # put settings in config_local if you're not running in a fill mysociety vhost
    SERVE_STATIC_FILES = True
except ImportError:
    SERVE_STATIC_FILES = False
    from mysociety import config
    config.set_file(os.path.abspath(package_dir + "/../../conf/general"))

# Now follows the normal Django stuff.

if int(config.get('STAGING')):
    DEBUG = True
else:
    DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# TODO - should we use 'django.contrib.gis.db.backends.postgis'?
DATABASE_ENGINE   = 'postgresql_psycopg2'
DATABASE_NAME     = config.get('UKONLINETUTORDB_DB_NAME')
DATABASE_USER     = config.get('UKONLINETUTORDB_DB_USER')
DATABASE_PASSWORD = config.get('UKONLINETUTORDB_DB_PASS')
DATABASE_HOST     = config.get('UKONLINETUTORDB_DB_HOST')
DATABASE_PORT     = config.get('UKONLINETUTORDB_DB_PORT')

# use this so that the test database is gis enabled
TEST_RUNNER='django.contrib.gis.tests.run_tests'

MAPIT_URL = config.get('MAPIT_URL')

# a postGIS template, e.g.: http://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#creating-a-spatial-database-template-for-postgis
POSTGIS_TEMPLATE = 'template_postgis'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-GB'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT      = os.path.join(package_dir, "../../web/static/")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = config.get('DJANGO_SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware', # FIXME - update from 1.1 style
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'ukotdb-app.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(package_dir, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.gis',
    
    'south',

    'tutordb',
    'certificates',

)

AUTHENTICATION_BACKENDS = (
    'ukotdb-app.backends.EmailModelBackend',        # login with an email
    # 'django.contrib.auth.backends.ModelBackend',    # login using username (default)
)

AUTH_PROFILE_MODULE = 'tutordb.UserProfile'

# registration relateh settings
LOGIN_REDIRECT_URL = '/my'



UKONLINE_SERVICES_API_KEY = config.get('UKONLINE_SERVICES_API_KEY')

SRID = 4326      # WGS84, the coordinate system used by the geodjango calculations 
