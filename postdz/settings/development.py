from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',  # Nom de votre base de données
        'USER': 'postgres',  # Nom d'utilisateur PostgreSQL
        'PASSWORD': 'dahoumohammed200',  # Mot de passe de l'utilisateur
        'HOST': 'localhost',  # Adresse du serveur (localhost pour local)
        'PORT': '5432',       # Port par défaut pour PostgreSQL
    }
}
